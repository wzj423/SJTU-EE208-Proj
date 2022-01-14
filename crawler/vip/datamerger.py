import json
from time import sleep
from typing import cast
import requests
import os,sys
from tqdm import tqdm
from random import randint

def merge_data(search_keyword) :
    detail_datas=[]
    index_datas=[]
    comment_datas=[]
    try:
        f=open(f"data-{search_keyword}.json",encoding='utf-8')
        index_datas=json.load(f)
    except Exception as e:
        print("No index json files of such keyword!")
        return
        
    try:
        with open(f"cleaned-detail-{search_keyword}.json", encoding='utf-8') as f:
            detail_datas = json.load(f)
    except Exception as e:
        print("No product index json files of such keyword!")
        return

    try:
        with open(f"cleaned-comment-{search_keyword}.json",encoding='utf-8') as f:
            comment_datas=json.load(f)
    except Exception as e:
        print("No comment json files of such keyword!")
        return

    def clean_index_data(data):
        uselesskeys=('status','labels','flags','itemDetail','skuId','categoryId','icon')
        for uselesskey in  uselesskeys:
            data.pop(uselesskey,None)

    def merge_props_and_attrs(data):
        props=data['props']
        for prop in props:
            prop.pop('hasOpts',None)
            prop.pop('optsList',None)

        ret=[]
        for x in data['attrs']:
            for prop in props:
                if x['name']==prop['name']:
                    break
            else:
                ret.append(x)
        ret+=props
        #data['attrs']=list(set(data['attrs']),set(data['props']))
        data.pop('props','None')
        data['attrs']=ret
    
    merged_data=json.loads(json.dumps({}))
    for index_data in tqdm(index_datas,desc="Final Merge"):
        pid=index_data['productId']
        spuId=index_data['spuId']
        brandId=index_data['brandId']

        detail=detail_datas[pid]
        comment=comment_datas[pid]
        index_data2=index_data
        clean_index_data(index_data2)
        merged_data[pid]={**detail,**{'comments':comment},**index_data2}
        merge_props_and_attrs(merged_data[pid])
        clean_index_data(merged_data[pid])
        merged_data[pid]['vipshopPrice']=merged_data[pid]['price']['salePrice']
        

    with open(f'final-merged-data-{search_keyword}.json', 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)


if __name__=="__main__":
    if len(sys.argv) == 2:
        search_keyword=sys.argv[1]
        print(search_keyword)
    else :
        search_keyword=input("Please input the keyword:")
    print("#"*10+"Now MERGE DATA"+"#"*10)
    merge_data(search_keyword)