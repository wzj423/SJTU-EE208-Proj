import json
from time import sleep
import requests
import os,sys
from tqdm import tqdm
from random import randint
from multiprocessing import Process,Pool
from requests.api import head

from indexcralwer import crawl_index
from infocralwer import crawl_detail
from commentcrawler import crawl_comment
from nlpcrawler import crawl_comment_nlp

from detailcleaner import clean_detail
from commentcleaner import clean_comments

from datamerger import merge_data

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

if __name__=="__main__":
    if len(sys.argv) == 3:
        search_keyword=sys.argv[1]
        page_num=int(sys.argv[2])
        print(search_keyword,page_num)
    else :
        search_keyword=input("Please input the keyword:")
        page_num=int(input("Please input the number of pages to crawl (120 items per page):"))
    
    '''
        Cralwer Usage
        This is a glue script as well as a top layer of the cralwer scripts.
        Notice: no error recovery is guaranteed, so please do not cralwer an excessively large number of items(>=2000) at one time.
            Since you will have to re-run this script if one of them crashed.
        
        Usage: Set your keyword. It is recommended to set the keyword in the form "{brandName}{itemClass}", for example "耐克运动鞋" "李宁袜子" "安踏裤子".
                Keyword can be set from commandline arguments , or, from manually entering the keyword if null commandline arguments were received. 
    '''




    # First we need to crawl the index of the items, without the data-{keyword}.json the following procedures cannot be runed.
    crawl_index(search_keyword,page_num)

    sub_crawl=(crawl_comment,crawl_detail,crawl_comment_nlp)
    p = Pool(3)
    for i in sub_crawl:
        p.apply_async(i, args=(search_keyword,))
    print('Waiting for all subprocesses done...')    
    p.close()
    p.join()
    print("All done")
    # These 4 functions rely on  crawl_index but are indepedent from each other.
    #crawl_comment(search_keyword)
    #crawl_detail(search_keyword)
    #crawl_comment_nlp(search_keyword)

    # The clean_XXX functions rely on crawl_XXX functions 
    print("Start data cleaning")
    clean_detail(search_keyword)
    clean_comments(search_keyword)

    merge_data(search_keyword)

