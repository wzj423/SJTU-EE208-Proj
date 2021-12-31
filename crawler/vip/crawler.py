import json
from time import sleep
import requests
import os,sys
from tqdm import tqdm
from random import randint

from requests.api import head

from indexcralwer import crawl_index
from infocralwer import crawl_detail
from commentcrawler import crawl_comment
from nlpcrawler import crawl_comment_nlp

from detailcleaner import clean_detail
from commentcleaner import clean_comments

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
    
    crawl_index(search_keyword,page_num)
    crawl_comment(search_keyword)
    crawl_detail(search_keyword)
    crawl_comment(search_keyword)
    crawl_comment_nlp(search_keyword)

    clean_detail(search_keyword)
    clean_comments(search_keyword)

