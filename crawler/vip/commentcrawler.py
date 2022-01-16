import json
from time import sleep
import requests
import os,sys
from tqdm import tqdm
from random import randint

from requests.api import head
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

headers = {
        'Cookie': 'vip_address=%7B%22pid%22%3A%22103101%22%2C%22cid%22%3A%22103101101%22%2C%22pname%22%3A%22%5Cu4e0a%5Cu6d77%5Cu5e02%22%2C%22cname%22%3A%22%5Cu4e0a%5Cu6d77%5Cu5e02%22%7D; vip_province=103101; vip_province_name=%E4%B8%8A%E6%B5%B7%E5%B8%82; vip_city_name=%E4%B8%8A%E6%B5%B7%E5%B8%82; vip_city_code=103101101; vip_wh=VIP_SH; user_class=a; mst_area_code=104104; mars_cid=1642140738769_e630b126a206fa7f9a1e0b36185e7c0f; mars_sid=dae8094e21d163abeb849cab01b78004; VIP_QR_FIRST=1; VipUINFO=luc:a|suc:a|bct:c_new|hct:c_new|bdts:0|bcts:0|kfts:0|c10:0|rcabt:0|p2:0|p3:1|p4:0|p5:1|ul:3105; vip_tracker_source_from=; vpc_uinfo=fr713:0,fr674:D1,fr1051:0,fr766:0,fr259:S0-4,fr896:0,fr0901:0,fr863:0,fr392:310505,fr398:0,fr408:0,fr251:A,fr344:0,fr444:A,fr848:0,fr249:A1,fr328:3105,fr902:0,fr901:0; vip_access_times={"list":7,"detail":3}; pg_session_no=41; VipDFT=0',

    'Referer': 'https://detail.vip.com/',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
}


def crawl_comment(search_keyword):
    index_datas=[]
    try:
        f=open(f"data-{search_keyword}.json",encoding='utf-8')
        index_datas=json.load(f)
    except Exception as e:
        print("No product index json files of such keyword!")
    url_comment_template="https://mapi.vip.com/vips-mobile/rest/content/reputation/queryBySpuId_for_pc?api_key=70f71280d5d547b2a7bb370a529aeea1&&spuId={}&brandId={}&page={}&pageSize=10"
    url_comment_template="https://mapi.vip.com/vips-mobile/rest/content/reputation/queryBySpuId_for_pc?callback=getCommentDataCb&app_name=shop_pc&app_version=4.0&warehouse=VIP_SH&fdc_area_id=103101101&client=pc&mobile_platform=1&province_id=103101&api_key=70f71280d5d547b2a7bb370a529aeea1&user_id=&mars_cid=1642140738769_e630b126a206fa7f9a1e0b36185e7c0f&wap_consumer=a&spuId={}&brandId={}&page={}&pageSize=10&timestamp=1642177886000&_=1642177818698"
    
    _i=0
    comment_tot_data=json.loads(json.dumps({}))
    for index_data in tqdm(index_datas,desc="COMMENT"):
        pid=index_data['productId']
        spuId=index_data['spuId']
        brandId=index_data['brandId']
        comment_json_data=[]
        for page in range(1,11):
            url_comment=url_comment_template.format(spuId,brandId,page)
            try:
                comment_html=requests.get(url_comment,headers=headers)
                if 'data' not in json.loads(comment_html.text):
                    break
                comment_json_data += json.loads(comment_html.text)['data']
            except Exception as e:
                pass
        comment_tot_data[pid]=comment_json_data
        _i+=1
        if _i%(int(len(index_datas)/10))==0 or _i==len(index_datas) or _i==len(index_datas)-1:
            with open(f'comment-{search_keyword}.json', 'w', encoding='utf-8') as f:
                json.dump(comment_tot_data, f, ensure_ascii=False, indent=4)
            sleep(randint(5,10))

if __name__=="__main__":
    if len(sys.argv) == 2:
        search_keyword=sys.argv[1]
        print(search_keyword)
    else :
        search_keyword=input("Please input the keyword:")
    print("#"*10+"Now CRAWL COMMENTS"+"#"*10)

    crawl_comment(search_keyword)