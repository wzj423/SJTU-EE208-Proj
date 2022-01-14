import json
from time import sleep
from typing import cast
import requests
import os,sys
from tqdm import tqdm
from random import randint

def clean_detail(search_keyword):
    detail_datas = []
    try:
        with open(f"detail-{search_keyword}.json", encoding='utf-8') as f:
            detail_datas = json.load(f)
    except Exception as e:
        print("No product index json files of such keyword!")

    target_word = ("spuId",
                "productId",
                "brandId",
                'title', 
                'vipshopPrice', 
                'marketPrice', 
                'smallImage', 
                #'previewImages', 
                'itemDetail', 
                #'detailImages', 
                'brandStoreLogo', 
                'brandStoreWhiteLogo', 
                'brandStoreName',
                'props',
                'categoryId')

    cleaned_detail_datas = json.loads(json.dumps({}))


    for pid,detail_data in detail_datas.items():
        cleaned_detail_datas[pid] = dict(filter(lambda elem:elem[0] in target_word,detail_data['product'].items()))
        try:
            cleaned_detail_datas[pid]['images']=[ x['imageUrl'] if x['imageUrl'].startswith('http') else "http://a.vpimg4.com"+x['imageUrl'] for x in detail_data['product']['detailImages']]+\
                [ x['imageUrl'] if x['imageUrl'].startswith('http') else "http://a.vpimg4.com"+x['imageUrl'] for x in detail_data['product']['previewImages']]
            cleaned_detail_datas[pid]
            pass
        except Exception as e:
            pass
    with open(f"cleaned-detail-{search_keyword}.json", "w", encoding='utf-8') as f:
        json.dump(cleaned_detail_datas, f, ensure_ascii=False, indent=4)


if __name__=="__main__":
    if len(sys.argv) == 2:
        search_keyword=sys.argv[1]
        print(search_keyword)
    else :
        search_keyword=input("Please input the keyword:")
    print("#"*10+"Now CLEANING DETAILS"+"#"*10)
    clean_detail(search_keyword)