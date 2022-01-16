from gettext import find
import json
import os,sys
from threading import local
from urllib import response
import requests
from playwright.sync_api import sync_playwright
from requests.api import head
from tqdm import tqdm

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

headers = {
    'Cookie': 'vip_address=%7B%22pid%22%3A%22103101%22%2C%22cid%22%3A%22103101101%22%2C%22pname%22%3A%22%5Cu4e0a%5Cu6d77%5Cu5e02%22%2C%22cname%22%3A%22%5Cu4e0a%5Cu6d77%5Cu5e02%22%7D; vip_province=103101; vip_province_name=%E4%B8%8A%E6%B5%B7%E5%B8%82; vip_city_name=%E4%B8%8A%E6%B5%B7%E5%B8%82; vip_city_code=103101101; vip_wh=VIP_SH; vip_ipver=31; user_class=a; mars_cid=1640401339247_dc74b1566f36bcdd4e14e753d82d4f50; mars_sid=baf363d54d8ea5a8bb5ae890e6898365; VIP_QR_FIRST=1; VipUINFO=luc:a|suc:a|bct:c_new|hct:c_new|bdts:0|bcts:0|kfts:0|c10:0|rcabt:0|p2:0|p3:1|p4:0|p5:0|ul:3105; vip_tracker_source_from=; vipshop_passport_src=https://list.vip.com/brand.html?sn=10015613; VipDFT=0; pg_session_no=18; vip_access_times={"list":0,"detail":4}',
    'Referer': 'https://detail.vip.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}
cur_detailed_data=[]
def crawl_comment_ex(search_keyword):
    global cur_detailed_data
    index_datas=[]
    try:
        f=open(f"data-{search_keyword}.json",encoding='utf-8')
        index_datas=json.load(f)
    except Exception as e:
        print("No product index json files of such keyword!")
    with open(f'detail-{search_keyword}.json', 'w', encoding='utf-8') as f:
        pass

    ful_detailed_data=json.loads(json.dumps({}))
    def select(response):
        if response.url.find('getCommentDataCb') !=-1:
            global cur_detailed_data
            t=response.body().decode()
            json_start = t.index('{')
            json_end = t.index('})')+1
            json_data=json.loads(t[json_start:json_end])['data']
            cur_detailed_data=json_data
#            print(json_data)   
        elif response.url.find('Comment')!=-1:
            #print(response.url)
            pass

    def crawl(playwright):
        global cur_detailed_data
        chromium = playwright.chromium
        browser = chromium.launch(headless=True)#False,slow_mo=100)

        _i=0
        for index_data in tqdm(index_datas,desc="COMMENT"):
            pid=index_data['productId']
            spuId=index_data['spuId']
            brandId=index_data['brandId']
        
            page = browser.new_page()
            page.on("response", select)
            #page.on('request',select)
            page.route("**/*", lambda route: route.abort() 
                if route.request.resource_type in ("image","font") 
                else route.continue_() 
            
             )
            #page.on("request", lambda request: print(">>", request.method, request.url))
            #page.on("response", lambda response: print("<<", response.status, response.url))
            page.goto(f"https://detail.vip.com/detail-{brandId}-{pid}.html#J-FW-prdComment")
            #page.evaluate('window.scrollTo(0,document.body.scrollHeight);')
            #page.evaluate('if(document.getElementsByClassName("dt-list-item J-topbar-tabs J-detail-commentCnt")[0])document.getElementsByClassName("dt-list-item J-topbar-tabs J-detail-commentCnt")[0].click();')
            #page.wait_for_timeout(1000)
            #page.wait_for_load_state(state='networkidle',)
            page.click(".dt-list-item.J-topbar-tabs.J-detail-commentCnt")
            #page.wait_for_timeout(900)
            page.wait_for_load_state(state='networkidle',)
            page.close()

            ful_detailed_data[pid]=cur_detailed_data
            cur_detailed_data=[]
            _i+=1
            if(_i==len(index_datas) or _i==len(index_datas)-1 or _i%30==0):
                with open(f'comment-{search_keyword}.json', 'w', encoding='utf-8') as f:
                    json.dump(ful_detailed_data, f, ensure_ascii=False, indent=4)
        
    with sync_playwright() as playwright:
        crawl(playwright)

if __name__=="__main__":
    if len(sys.argv) == 2:
        search_keyword=sys.argv[1]
        print(search_keyword)
    else :
        search_keyword=input("Please input the keyword:")
    print("#"*10+"Now CRAWLING DETAIL INFO"+"#"*10)

    crawl_comment_ex(search_keyword)