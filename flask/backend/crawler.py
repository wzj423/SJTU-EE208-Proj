# SJTU EE208

import os
import queue
import re
import string
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.response
import shutil

import chardet
from bs4 import BeautifulSoup


def get_encoding(soup):
    if soup and soup.meta:
        encod = soup.meta.get('charset')
        if encod == None:
            encod = soup.meta.get('content-type')
            if encod == None:
                content = soup.meta.get('content')
                match = re.search('charset=(.*)', content)
                if match:
                    encod = match.group(1)
                else:
                    raise ValueError('unable to find encoding')
    else:
        raise ValueError('unable to find encoding')
    return encod

def valid_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    if(len(s) > 64):
        s = s[0:31]+s[-32:-1]
    return s

INTERNAL_DIR=os.path.dirname(__file__)
index_filename = ''  # index.txt中每行是'网址 对应的文件名'
folder = ''  # 存放网页的文件夹
new_instance=""

def set_workdir(work_folder,index_name,new_proj=False):
    global index_filename,folder,new_instance
    index_filename=index_name
    folder=work_folder
    new_instance=new_proj
    if  new_instance :
        try:
            shutil.rmtree(os.path.join(INTERNAL_DIR,folder),ignore_errors=True)
            os.remove(os.path.join(INTERNAL_DIR,folder,index_name))
        except Exception as e:
            pass
        os.mkdir(os.path.join(INTERNAL_DIR,folder))
        with open(os.path.join(INTERNAL_DIR,folder,index_filename),"w") as f:
            pass


def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    if not content or not page:
        return

    filename = valid_filename(page)+".html"  # 将网址变成合法的文件名
    index = open(os.path.join(INTERNAL_DIR,folder,index_filename), 'a')
    index.write(str(page.encode('ascii', 'ignore')).strip(
        'b\'') + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(os.path.join(INTERNAL_DIR,folder)):  # 如果文件夹不存在则新建
        os.mkdir(os.path.join(INTERNAL_DIR,folder))
    f = open(os.path.join(INTERNAL_DIR, folder, filename), 'wb')
    f.write(content)  # 将网页存入文件
    f.close()


def get_page(page, id=1):
    varLock.acquire()
    print('downloading page %s from thread ID %d' % (page, id))
    varLock.release()
    # time.sleep(0.5)
    try:
        # 要伪装成用户请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        request = urllib.request.Request(page, headers=headers)
        response = urllib.request.urlopen(request, timeout=30)
        content = response.read()
    except Exception as e:
        print(e)
        print(page+"请求错误")
        return None
    return content

invalidSuffix=('.zip','.rar','.7z','.exe','.jpg','pdf','.gif','.png')
def get_all_links(content, page):
    links = []
    urlset = set()
    try:
        #print(chardet.detect(content))
        # rawdata=content.decode(chardet.detect(content)['encoding'])
        soup = BeautifulSoup(content, "lxml")
                             #from_encoding=get_encoding(soup))#chardet.detect(content)['encoding'])
    except Exception as e:
        print(page+"解析错误")
        return[]
    # print(rawdata)

    for a_link in soup.find_all('a', href=True):
        if (re.search('(^http|^ftp|^/).+', a_link['href'])):
            if(re.search('gov', a_link['href'])):
                continue
            #if(not re.search('bokee',a_link['href'])):
            #    continue
            s=str(a_link['href'])
            if s.endswith(invalidSuffix):
                continue
            # a_link['href'][0]=='/':
            if not re.search("^http|^ftp", a_link['href']):
                urlset.add(urllib.parse.urljoin(page, a_link['href']))
            else:
                urlset.add(a_link['href'])
    links = urlset
    return links


def working(threadId):
    global totCrawled
    global crawlLimit
    while totCrawled < crawlLimit:
        page = q.get(timeout=100)
        # if varLock.acquire():
        if page not in crawled:

            # varLock.release()
            # else:
            # varLock.release()
            content = get_page(page, threadId)
            if(content):
                totCrawled += 1
                print("crawled %d page\n" % totCrawled)
            outlinks = get_all_links(content, page)
            for link in outlinks:
                if totCrawled<crawlLimit:
                    q.put(link)
            if varLock.acquire():
                graph[page] = outlinks
                crawled.append(page)
                varLock.release()
            add_page_to_folder(page, content)
            q.task_done()
    else:
        return
        while not q.empty():  # 清空Queue，否则主线程的q.join()会deadlock https://stackoverflow.com/questions/31665328/python-3-multiprocessing-queue-deadlock-when-calling-join-before-the-queue-is-em
            #print(f"Thread {threadId} cleaning with {q.qsize()} items remaining")
            q.get(timeout=1)
            q.task_done()
        print("Thread {} done".format(threadId))
    #print("Thread {} done".format(threadId))


set_workdir("img_html_3","index.txt",False)

crawlLimit = 1500
totCrawled = 0
start = time.time()
NUM = 32
crawled = []
graph = {}
varLock = threading.Lock()
q = queue.Queue()
q.put("http://www.9kd.com/")
#q.put("http://blog.sohu.com/")
for i in range(NUM):
    t = threading.Thread(target=working, args={i})
    t.setDaemon(True)
    t.start()
    t.join()
#q.join()

end = time.time()
print(end - start)
