from ast import Index
import lucene
import json
from Index import Index_Building
from logo_derive_feature import Search_for_logo
from search_for_product import Find_Similiarity
from Search import keywordQueryWrapped
DATA_NUM=1 #JSON_DATA数量
INTERNAL_DIR=os.path.dirname(__file__)
if __name__=="__main__":
    #使用Index和Search时，需启动虚拟机
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    #传入初始数据，数据从Json文件中读取
    Data=list()
    for i in range(DATA_NUM):
        #open内为json_data保存路径，格式见内
        with open("./data%d.json"%i,'r',encoding='utf8') as data_json:
            Data+=json.load(data_json)
    Index_Building(Data)
    keywordQueryWrapped(input_keyword)
    Find_Similiarity(search_img,Data)
    Search_for_logo(logo_photo)