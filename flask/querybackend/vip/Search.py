#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene

import jieba
from java.io import File
from java.nio.file import Path
from org.apache.lucene.analysis.cjk import CJKAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.analysis.core import SimpleAnalyzer,WhitespaceAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
BRAND=["李宁","安踏","耐克","阿迪达斯","特步","匹克","鸿星尔克"]
INTERNAL_DIR=os.path.dirname(__file__)
def keywordQueryWrapped(keyword):
    STORE_DIR = "index"
    #lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    #print('lucene', lucene.VERSION)
    directory = SimpleFSDirectory(File(os.path.join(INTERNAL_DIR, STORE_DIR)).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer()
    print ("Hit enter with no input to quit.")
    command = keyword
    print ("Searching for:", command)
    querys = BooleanQuery.Builder()
    jieba.load_userdict(os.path.join(INTERNAL_DIR, "usedict.txt"))
    command=jieba.cut_for_search(command)
    command=list(command)
    #逻辑：先进行品牌的搜索，如果出现了品牌，就必须要对索引中的内容的品牌进行限定
    for word in command:
        print(word)
        if "季" in word:
            command.append(word[0])
        if word in BRAND:
            query= QueryParser("brand",analyzer).parse(word)
            querys.add(query,BooleanClause.Occur.MUST)
        else:
            query = QueryParser("title", analyzer).parse(word)
            querys.add(query, BooleanClause.Occur.SHOULD)
            query = QueryParser("attrs",analyzer).parse(word)
            querys.add(query, BooleanClause.Occur.SHOULD)
    scoreDocs = searcher.search(querys.build(), 400).scoreDocs
    print("%s total matching documents." % len(scoreDocs))
    Related_Id=list()
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        Related_Id.append(doc.get("id"))
    del searcher
    return Related_Id

if __name__=="__main__":
    keywordQueryWrapped("安踏秋季运动鞋")