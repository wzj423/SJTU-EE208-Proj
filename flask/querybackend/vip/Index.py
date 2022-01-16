# SJTU EE208

INDEX_DIR = "IndexFiles.index"
DATA_NUM=1
INTERNAL_DIR=os.path.dirname(__file__)
import json
import sys, os, lucene, threading, time, re
import jieba
from datetime import datetime
from bs4 import BeautifulSoup
from java.io import File
from java.nio.file import Path
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.cjk import CJKAnalyzer
from org.apache.lucene.analysis.core import SimpleAnalyzer,WhitespaceAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, StringField, TextField
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig,IndexOptions,Term
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

class Ticker(object):
    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

def Index_Building(data):
    #preprocessing
    storeDir="index"
    if not os.path.exists(storeDir):
        os.mkdir(storeDir)
    analyzer = WhitespaceAnalyzer()
    store = SimpleFSDirectory(File(storeDir).toPath())
    analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)
    #start building
    t1 = FieldType()
    t1.setStored(True)
    t1.setTokenized(False)
    t1.setIndexOptions(IndexOptions.NONE)  # Not Indexed

    t2 = FieldType()
    t2.setStored(True)
    t2.setTokenized(True)
    t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
    count=0
    for i in range(len(data)):
        if not data[i]:
            continue
        try:
            print("adding", data[i]["title"])
            count+=1
            value_rec=list()
            for item_dict in data[i]["attrs"]:
                value=item_dict["value"]
                value=value.replace('/',' ')
                value_rec.append(value)
            attrs=' '.join(value_rec)
            doc = Document()
            doc.add(Field("id", data[i]["productId"], t1))
            doc.add(Field("attrs",attrs,t2))
            doc.add(Field("brand",data[i]["brandShowName"],t2))
            title=' '.join(str(i) for i in jieba.lcut(data[i]["title"]))
            if len(title) > 0:
                doc.add(Field("title", title, t2))
                writer.addDocument(doc)
            else:
                print("warning: no content in product %d"%data[i]["productId"])
        except Exception as e:
            print("Failed in indexDocs:", e)
    print("totally add %d data"%count)

    #finish building
    ticker = Ticker()
    print('commit index')
    threading.Thread(target=ticker.run).start()
    writer.commit()
    writer.close()
    ticker.tick = False
    print('done')

if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    #print('lucene', lucene.VERSION)
    Data=list()
    for i in range(DATA_NUM):
        with open("./data%d.json"%i,'r',encoding='utf8') as data_json:
            Data+=json.load(data_json)
    #Data包含了所有Data为名的json数据，为列表类型。
    try:
        Index_Building(Data)
    except Exception as e:
        print("Failed: ", e)
        raise e