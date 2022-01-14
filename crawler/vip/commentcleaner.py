import json
from time import sleep
import requests
import os,sys
from tqdm import tqdm
from random import randint



def clean_comments(search_keyword):
    cmt_datas=[]
    try:
        with open(f"comment-{search_keyword}.json",encoding='utf-8') as f:
            cmt_datas=json.load(f)
    except Exception as e:
        print("No comment json files of such keyword!")

    cleaned_cmt_data=json.loads(json.dumps({}))

    for pid,cmt_data in cmt_datas.items():
        cleaned_cmt_data[pid]=[{'content': x['reputation']['content'],'nlpScore':x['reputation']['nlpScore'],'satisfiedStatus':x['reputation']['satisfiedStatus']} for x in cmt_data]
    with open(f"cleaned-comment-{search_keyword}.json","w",encoding='utf-8') as f:
        json.dump(cleaned_cmt_data,f, ensure_ascii=False, indent=4)

if __name__=="__main__":
    if len(sys.argv) == 2:
        search_keyword=sys.argv[1]
        print(search_keyword)
    else :
        search_keyword=input("Please input the keyword:")
    print("#"*10+"Now CLEANING COMMENTS"+"#"*10)
    clean_comments(search_keyword)
