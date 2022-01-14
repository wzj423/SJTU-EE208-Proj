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
    'Cookie': 'vip_address=%7B%22pid%22%3A%22103101%22%2C%22cid%22%3A%22103101101%22%2C%22pname%22%3A%22%5Cu4e0a%5Cu6d77%5Cu5e02%22%2C%22cname%22%3A%22%5Cu4e0a%5Cu6d77%5Cu5e02%22%7D; vip_province=103101; vip_province_name=%E4%B8%8A%E6%B5%B7%E5%B8%82; vip_city_name=%E4%B8%8A%E6%B5%B7%E5%B8%82; vip_city_code=103101101; vip_wh=VIP_SH; vip_ipver=31; user_class=a; mars_cid=1640401339247_dc74b1566f36bcdd4e14e753d82d4f50; mars_sid=baf363d54d8ea5a8bb5ae890e6898365; VIP_QR_FIRST=1; VipUINFO=luc:a|suc:a|bct:c_new|hct:c_new|bdts:0|bcts:0|kfts:0|c10:0|rcabt:0|p2:0|p3:1|p4:0|p5:0|ul:3105; vip_tracker_source_from=; vipshop_passport_src=https://list.vip.com/brand.html?sn=10015613; VipDFT=0; pg_session_no=18; vip_access_times={"list":0,"detail":4}',
    'Referer': 'https://detail.vip.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

def crawl_comment_nlp(search_keyword):
    index_datas = []
    try:
        f = open(f"data-{search_keyword}.json", encoding='utf-8')
        index_datas = json.load(f)
    except Exception as e:
        print("No product index json files of such keyword!")

    url_comment_template = "https://mapi.vip.com/vips-mobile/rest/ugc/reputation/getSpuIdNlpKeywordV2_for_pc?callback=getSpuIdNlpKeywordCb&app_name=shop_pc&app_version=4.0&warehouse=VIP_SH&fdc_area_id=103101101&client=pc&mobile_platform=1&province_id=103101&api_key=70f71280d5d547b2a7bb370a529aeea1&user_id=&mars_cid=1640401339247_dc74b1566f36bcdd4e14e753d82d4f50&wap_consumer=a&showTagOther=1&spuId=1664157099241238534&_=1640412803841"
    _i = 0
    comment_tot_data = json.loads(json.dumps({}))
    for index_data in tqdm(index_datas,desc="COMMENT-NLP"):
        pid = index_data['productId']
        spuId = index_data['spuId']
        brandId = index_data['brandId']

        url_comment = url_comment_template
        comment_html = requests.get(url_comment, headers=headers)
        #print(comment_html.text)
        start = comment_html.text.index('{')
        end = comment_html.text.index('})')+1
        json_comment=json.loads(comment_html.text[start:end])['data']
        #print(json_comment)
        comment_tot_data[pid] = json_comment
        _i += 1
        if _i % 20 == 0:
            with open(f'comment-{search_keyword}-nlp-keywords.json', 'w', encoding='utf-8') as f:
                json.dump(comment_tot_data, f, ensure_ascii=False, indent=4)
            sleep(randint(5, 10))

if __name__=="__main__":
    if len(sys.argv) == 2:
        search_keyword=sys.argv[1]
        print(search_keyword)
    else :
        search_keyword=input("Please input the keyword:")
    print("#"*10+"Now CRAWLING NLP ANALYSIS INFO OF COMMENTS"+"#"*10)
    crawl_comment_nlp(search_keyword)