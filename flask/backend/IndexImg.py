# SJTU EE208

INDEX_DIR = "IndexFiles.index"

from logging import error
from typing import Text
import chardet,tldextract
from urllib.parse import urlparse,urljoin
from bs4 import BeautifulSoup, element
import sys, os, lucene, threading, time
from datetime import datetime
import re,jieba
from tqdm import tqdm
from requests import get
from io import BytesIO
from PIL import Image
from bloom_filter2 import BloomFilter

# from java.io import File
from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.analysis.cjk import CJKAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, StringField, TextField
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexReader ,IndexWriterConfig, Term, DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""
def valid_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    if(len(s) > 64):
        s = s[0:31]+s[-32:-1]
    return s

INTERNAL_DIR=os.path.dirname(__file__)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir):

        root=os.path.join(INTERNAL_DIR,root)
        storeDir=os.path.join(INTERNAL_DIR,storeDir)

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)


        # store = SimpleFSDirectory(File(storeDir).toPath())
        store = SimpleFSDirectory(Paths.get(storeDir))
        analyzer = WhitespaceAnalyzer()
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        '''lab-needed datas'''
        self.targetSuffix=('.html',)
        self.UrlTable=dict()
        self.initUrlTabl(root)
        self.imgurl_bloom=BloomFilter(max_elements=1000000,error_rate=0.01)

        #self.indexDocs(root, writer)
        #writer.deleteDocuments(Term("localtext",""))
        self.indexPics(root,writer)
        print('commit index')
        writer.commit()
        writer.close()
        print('done')

    def initUrlTabl(self,root):
        path=os.path.join(root, 'index.txt')
        with  open(path,"r") as f :
            for line in f:
                elements=line.strip().split('\t')
                if(len(elements)==2):
                    self.UrlTable[elements[1]]=elements[0]

    def removeScriptandCss(self,soup) :
        for script in soup(["script", "style"]):
            script.extract()    # rip it out   

    def cleanText(self,text):
        if not text :return ""
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = ' '.join(chunk for chunk in chunks if chunk)
        text = ' '.join(jieba.cut(text))
        return text

    def getPics(self,root,filename):
        try:
            #read files
            path = os.path.join(root, filename)
            file = open(path,"rb")
            rawdata=file.read()
            file.close()   
            soup=BeautifulSoup(rawdata,features="lxml")
            self.removeScriptandCss(soup)

            title=str(soup.find('title').string)
            url=self.UrlTable[filename]
            extracted_url=tldextract.extract(url)
            domain=extracted_url.domain+"."+extracted_url.suffix

            imgset=[]
            imgurl=""

            for a_link in soup.find_all('img'):
                if(not a_link.get('src')): continue

                if (re.search('(^http|^ftp|^/|^\.).+',a_link['src'])):
                    if(re.search('gov',a_link['src'])):
                        continue
                    if not re.search("^http|^ftp",a_link['src']):#a_link['href'][0]=='/':
                        imgurl=urljoin(url,a_link['src'])
                    else:
                        imgurl=a_link['src']

                    if imgurl in self.imgurl_bloom : continue
                    else :self.imgurl_bloom.add(imgurl)

                    #print(imgurl)
                    altText=self.cleanText( a_link.get('alt') if a_link.get('alt') else "" )                   
                    parentText=self.cleanText(a_link.parent.get_text())
                    grandparentText=self.cleanText(a_link.parent.parent.get_text())
                    if( not parentText) :continue
                    
                    adjacent_text=""
                    t=a_link.next_element
                    for id,ele in enumerate(a_link.next_elements):
                        if(len(self.cleanText(ele.string).strip())>0):
                            adjacent_text+=self.cleanText(ele.string).strip()
                            break
                        if id>100:
                            break
                    for id,ele in enumerate(a_link.previous_elements):
                        if(len(self.cleanText(ele.string).strip())>0):
                            adjacent_text+=' '+self.cleanText(ele.string).strip()
                            break
                        if id>100:
                            break                    
                    
                    image_raw = get(imgurl)
                    image = Image.open(BytesIO(image_raw.content))
                    width, height = image.size
                    if(width<200 or height<200) :continue
                    print(width,height)

                    imgset.append((imgurl,url,title,altText,adjacent_text, parentText,grandparentText))
                    #print((imgurl,title,adjacentText))
            return imgset
        except Exception as e:
            print("Failed in getPics",e)
            return []

    def indexPics(self,root,writer): 
        for root, dirnames, filenames in os.walk(root):
            for filename in tqdm(filenames):
                if not filename.endswith(self.targetSuffix):
                    continue
                print("adding", filename)
                for imgurl,url,title,altText,adjacent_text,parentText,grandparentText in self.getPics(root,filename):
                    try:
                        doc = Document()
                        doc.add(StringField("imgurl", imgurl, Field.Store.YES))
                        doc.add(StringField("url", url, Field.Store.YES))
                        doc.add(TextField("title",title,Field.Store.YES))
                        doc.add(TextField("description",altText,Field.Store.YES))
                        doc.add(TextField("neartext",adjacent_text,Field.Store.YES))
                        doc.add(TextField("localtext",parentText,Field.Store.YES))
                        doc.add(TextField("remotetext",grandparentText,Field.Store.YES))
                        writer.addDocument(doc)
                    except Exception as e:
                        print("Failed in indexDocs:", e)        


if __name__ == '__main__':
    lucene.initVM()#vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    # import ipdb; ipdb.set_trace()
    start = datetime.now()
    try:
        IndexFiles('img_html_3', "img_index_3")
        end = datetime.now()
        print(end - start)
    except Exception as e:
        print("Failed: ", e)
        raise e
