import json
import requests
import os

from requests.api import head
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

headers = {
    'Cookie': 'vip_province_name=%E6%B2%B3%E5%8D%97%E7%9C%81; vip_city_name=%E4%BF%A1%E9%98%B3%E5%B8%82; vip_city_code=104101115; vip_wh=VIP_HZ; vip_ipver=31; user_class=a; mars_sid=ff7be68ad4dc97e589a1673f7154c9f9; VipUINFO=luc%3Aa%7Csuc%3Aa%7Cbct%3Ac_new%7Chct%3Ac_new%7Cbdts%3A0%7Cbcts%3A0%7Ckfts%3A0%7Cc10%3A0%7Crcabt%3A0%7Cp2%3A0%7Cp3%3A1%7Cp4%3A0%7Cp5%3A0%7Cul%3A3105; mars_pid=0; visit_id=98C7BA95D1CA0C0E518537BD0B4ABEA0; vip_tracker_source_from=; pg_session_no=5; mars_cid=1600153235012_7a06e53de69c79c1bad28061c13e9375',
    'Referer': 'https://category.vip.com/suggest.php?keyword=%E6%8A%A4%E8%82%A4&ff=235|12|1|1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

search_keyword="包"
n = 20  # n就是用来确定请求的页数，可以使用input语句替代
for num in range(0, (n+1)*120, 120):  # 这里是从第二页开始取数据了，第一个参数可以设置为0
    #url = f'https://mapi.vip.com/vips-mobile/rest/shopping/pc/search/product/rank?callback=getMerchandiseIds&app_name=shop_pc&app_version=4.0&warehouse=VIP_HZ&fdc_area_id=104101115&client=pc&mobile_platform=1&province_id=104101&api_key=70f71280d5d547b2a7bb370a529aeea1&user_id=&mars_cid=1600153235012_7a06e53de69c79c1bad28061c13e9375&wap_consumer=a&standby_id=nature&keyword=%E6%8A%A4%E8%82%A4%E5%A5%97%E8%A3%85&lv3CatIds=&lv2CatIds=&lv1CatIds=&brandStoreSns=&props=&priceMin=&priceMax=&vipService=&sort=0&pageOffset={num}&channelId=1&gPlatform=PC&batchSize=120&_=1600158865435'
    
    url=f'https://mapi.vip.com/vips-mobile/rest/shopping/pc/search/product/rank?callback=getMerchandiseIds&app_name=shop_pc&app_version=4.0&warehouse=VIP_SH&fdc_area_id=103101101&client=pc&mobile_platform=1&province_id=103101&api_key=70f71280d5d547b2a7bb370a529aeea1&user_id=&mars_cid=1640401339247_dc74b1566f36bcdd4e14e753d82d4f50&wap_consumer=a&standby_id=nature&keyword={search_keyword}&lv3CatIds=&lv2CatIds=&lv1CatIds=&brandStoreSns=&props=&priceMin=&priceMax=&vipService=&sort=0&pageOffset={num}&channelId=1&gPlatform=PC&batchSize=120&_=1640402620351'
    html = requests.get(url, headers=headers)
    start = html.text.index('{')
    end = html.text.index('})')+1
    json_data = json.loads(html.text[start:end])
    if('products' not in json_data['data']):
        break
    product_ids = json_data['data']['products']

    '''
    for product_id in product_ids:
        print('商品id',product_id['pid'])
        product_url = 'https://mapi.vip.com/vips-mobile/rest/shopping/pc/product/module/list/v2?callback=getMerchandiseDroplets3&app_name=shop_pc&app_version=4.0&warehouse=VIP_HZ&fdc_area_id=104101115&client=pc&mobile_platform=1&province_id=104101&api_key=70f71280d5d547b2a7bb370a529aeea1&user_id=&mars_cid=1600153235012_7a06e53de69c79c1bad28061c13e9375&wap_consumer=a&productIds={}%2C&scene=search&standby_id=nature&extParams=%7B%22stdSizeVids%22%3A%22%22%2C%22preheatTipsVer%22%3A%223%22%2C%22couponVer%22%3A%22v2%22%2C%22exclusivePrice%22%3A%221%22%2C%22iconSpec%22%3A%222x%22%7D&context=&_=1600164018137'.format(product_id['pid'])
        product_html = requests.get(product_url,headers = headers)
        product_start = product_html.text.index('{')
        product_end = product_html.text.index('})')+1
        product_json_data = json.loads(product_html.text[product_start:product_end])
        product_info_data = product_json_data['data']['products'][0]
        # print(product_info_data)
        product_title = product_info_data['title']
        product_brand = product_info_data['brandShowName']
        product_price = product_info_data['price']['salePrice']
        print('商品名称：{}，品牌：{}，折后价格：{}'.format(product_title,product_brand,product_price))
        with open('vip.txt','a+',encoding = 'utf-8') as f:
            f.write('商品名称：{}，品牌：{}，折后价格：{}\n'.format(product_title,product_brand,product_price))
    '''
    tot_data=None
    for batch_product in batch(product_ids,50):
        product_tot_url='https://mapi.vip.com/vips-mobile/rest/shopping/pc/product/module/list/v2?callback=getMerchandiseDroplets3&app_name=shop_pc&app_version=4.0&warehouse=VIP_HZ&fdc_area_id=104101115&client=pc&mobile_platform=1&province_id=104101&api_key=70f71280d5d547b2a7bb370a529aeea1&user_id=&mars_cid=1600153235012_7a06e53de69c79c1bad28061c13e9375&wap_consumer=a&productIds={}%2C&scene=search&standby_id=nature&extParams=%7B%22stdSizeVids%22%3A%22%22%2C%22preheatTipsVer%22%3A%223%22%2C%22couponVer%22%3A%22v2%22%2C%22exclusivePrice%22%3A%221%22%2C%22iconSpec%22%3A%222x%22%7D&context=&_=1600164018137'.format(",".join([x['pid'] for x in batch_product]))
        product_tot_html=requests.get(product_tot_url,headers=headers)
        product_start = product_tot_html.text.index('{')
        product_end = product_tot_html.text.index('})')+1
        product_json_data = json.loads(product_tot_html.text[product_start:product_end])
        product_info_data = product_json_data['data']['products']   
        with open(f'data-{search_keyword}-tmp.json', 'a', encoding='utf-8') as f:
            json.dump(product_info_data, f, ensure_ascii=False, indent=4)
with open(f'data-{search_keyword}-tmp.json', 'r', encoding='utf-8') as fin:
    with open(f'data-{search_keyword}.json', 'w', encoding='utf-8') as fout:
        fout.write(fin.read().replace("][",","))
with open(f'data-{search_keyword}-tmp.json', 'w', encoding='utf-8') as f:
    pass
    #delete temp files