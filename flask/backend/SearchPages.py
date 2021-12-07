# SJTU EE208

import os
import sys
import threading
import time
from datetime import datetime
from urllib.parse import urlparse

import chardet
import jieba
import lucene
import lxml
import tldextract
from bs4 import BeautifulSoup, element
from java.io import File
from java.nio.file import Path, Paths
from java.lang import Boolean
from org.apache.lucene.analysis import Analyzer, TokenStream
from org.apache.lucene.analysis.cjk import CJKAnalyzer
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.document import (Document, Field, FieldType,
                                        StringField, TextField)
from org.apache.lucene.index import (DirectoryReader, FieldInfo, IndexOptions,
                                     IndexReader, IndexWriter,
                                     IndexWriterConfig)
from org.apache.lucene.queryparser.classic import QueryParser
# from java.io import File
from org.apache.lucene.search import (BooleanClause, BooleanQuery,
                                      IndexSearcher, Query, TopDocs)
from org.apache.lucene.search.highlight import (Formatter, Fragmenter,
                                                Highlighter, QueryScorer,
                                                SimpleHTMLFormatter,
                                                SimpleSpanFragmenter,
                                                TokenSources)
from org.apache.lucene.store import Directory, FSDirectory, SimpleFSDirectory
from org.apache.lucene.util import Version

INDEX_DIR = "IndexFiles.index"


"""
This script is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""


def parseCommand(command):
    '''
    input: C title:T author:A language:L
    output: {'contents':C, 'title':T, 'author':A, 'language':L}

    Sample:
    input:'contenance title:henri language:french author:william shakespeare'
    output:{'author': ' william shakespeare',
                   'language': ' french',
                   'contents': ' contenance',
                   'title': ' henri'}
    '''
    allowed_opt = ['site']
    command_dict = {}
    opt = 'contents'
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                command_dict[opt] = command_dict.get(opt, '') + ' ' + value
        else:
            command_dict[opt] = command_dict.get(opt, '') + ' ' + ' '.join(jieba.cut_for_search(i))
    print(command_dict)
    return command_dict


def run(searcher, analyzer, command):
    if command == '':
        return False
    print("Searching for:", command)
    actual_word = ""
    command_dict = parseCommand(command)
    querys = BooleanQuery.Builder()
    for k, v in command_dict.items():
        query = QueryParser(k, analyzer)
        query=query.parse(v.strip())
        querys.add(query, BooleanClause.Occur.MUST)
        print(k, v)
        if(k == 'contents'):
            actual_word = v

    final_query = querys.build()
    scoreDocs = searcher.search(final_query, 50).scoreDocs
    print("%s total matching documents." % len(scoreDocs))

    search_results=[]
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        id = scoreDoc.doc
##            explanation = searcher.explain(query, scoreDoc.doc)
        print("------------------------")
        print('path:', doc.get("path"))
        print('name:', doc.get("name"))
        print('title:', doc.get('title'))
        print('url:', doc.get('url'))
        print('site:', doc.get('site'))
        print('score:', scoreDoc.score)
        # print 'explain:', searcher.explain(query, scoreDoc.doc)
        highlighter = Highlighter(
            SimpleHTMLFormatter(), QueryScorer(final_query))
        full_content = doc.get('contents')
        tokenStream = TokenSources.getAnyTokenStream(
            searcher.getIndexReader(), id, "contents", analyzer)
        frags = highlighter.getBestFragments(tokenStream, full_content, 4)
        frag = str(frags[0]).replace(" ", "")
        print(frags, '\n', frag)
        def cleanJString(x):
            return str(x).replace(" ","")
        search_results.append( ( doc.get('title'), doc.get('url'), doc.get('site'), list(map(cleanJString,frags)), scoreDoc.score))
    return search_results



def init_lucene():
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)    

def init_search_handler():
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    print(__file__)
    INTERNAL_DIR = os.path.dirname(__file__)
    STORE_DIR = os.path.join(INTERNAL_DIR, "index")
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    global directory,searcher,analyzer
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer()


def build_search_handler() :
    global searcher,analyzer
    def search_handler(queryWords):
        return run(searcher,analyzer,queryWords)
    return search_handler

def get_search_handler() :
    return build_search_handler()

#def search_handler(queryWords) :
#    global searcher,analyzer
#    run(searcher,analyzer,queryWords)
#run(searcher,analyzer,"中国")
#search_handler("中国")

