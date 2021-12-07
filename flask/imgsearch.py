import functools
from os import ttyname

from backend.SearchImg import get_search_handler,init_search_handler,lucene
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
print(__name__)
bp = Blueprint('imgsearch', __name__, url_prefix='/imgsearch')


@bp.before_app_first_request
def init_websearch_handler():
    init_search_handler()
    global handler
    handler=get_search_handler()

@bp.route('/',methods=('GET','POST'))
def search_webpages():
    if request.method=='GET':
        return render_template('imgsearch/search_box.html')
    else:
        print(request)
        return redirect(url_for("imgsearch.search_results",keywords=request.form['keywords']))

@bp.route('/results',methods=('GET',))
def search_results():
    global handler
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()#https://stackoverflow.com/questions/6536179/where-is-the-best-place-to-do-initvm-and-attachcurrentthread-when-using-pylucene/6543987#6543987
    keywords=request.args.get('keywords')
    results=handler(keywords)
    lucene_results=results
    return render_template('imgsearch/imgsearch_results.html',lucene_results=lucene_results)
    if results:
        title,url,site,frags,score=results[0]
        return keywords+title+url+site+str(score)
    else:
        return keywords+"No matching results!"