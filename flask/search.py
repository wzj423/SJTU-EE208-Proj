import functools
import json
from multiprocessing import log_to_stderr
import os
import sys
from os import ttyname
from cv2 import imread
from werkzeug.utils import secure_filename

from backend.SearchPages import (get_search_handler, init_lucene,
                                 init_search_handler, lucene)
from database.itemQuery import filterItems, queryItems, sortItems
from database.resultsCounter import resultsCounter
from flask import (Blueprint, Flask, current_app, flash, g, redirect,
                   render_template, request, send_from_directory, session,
                   url_for)
from querybackend.queryWrapper import keywordQueryWrapped,logoQueryWrapped,imageQueryWrapped

print(__name__)
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
bp = Blueprint('search', __name__, url_prefix='/search')


@bp.before_app_first_request
def init_websearch_handler():
    init_search_handler()
    global handler
    handler = get_search_handler()


@bp.route('/', methods=('GET', 'POST'))
def search_webpages():
    if request.method == 'GET':
        return render_template('search/search_box.html')
    else:
        print(request)
        return redirect(url_for("search.search_results", keywords=request.form['keywords']))


@bp.route('/results', methods=('GET',))
def search_results():
    global handler
    vm_env = lucene.getVMEnv()
    # https://stackoverflow.com/questions/6536179/where-is-the-best-place-to-do-initvm-and-attachcurrentthread-when-using-pylucene/6543987#6543987
    vm_env.attachCurrentThread()
    keywords = request.args.get('keywords')

    imageFilename=request.args.get('imageFilename')
    logoFilename=request.args.get('logoFilename')

    brands = request.args.get('brands', default=None)
    brands = brands.split(',') if brands else None
    cate = request.args.get('cate', default=None)
    cate = cate.split(',') if cate else None
    attr = json.loads('{'+request.args.get('attr') +
                      '}') if request.args.get('attr') else None
    sortway = request.args.get('sortway', default=None)
    # results=handler(keywords)
    # lucene_results=results

    if  imageFilename:
        image=imread(os.path.join(current_app.config['UPLOAD_FOLDER'], imageFilename))
        resultIndex = imageQueryWrapped(image)
    elif logoFilename:
        logo=imread(os.path.join(current_app.config['UPLOAD_FOLDER'], logoFilename))
        resultIndex = logoQueryWrapped(logo)
    else:

        resultIndex = keywordQueryWrapped("123")

    print(resultIndex)
    results = queryItems(resultIndex)
    statis = resultsCounter(results)  # 做一点微小的统计工作
    filtered_results = filterItems(results, brands, cate, attr)  # 做一点微小的过滤工作
    sorted_filtered_results = sortItems(filtered_results, sortway)
    return render_template('search/search_results.html', results=sorted_filtered_results, statis=statis, title=keywords)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/imageUploader', methods=('POST',))
def image_upload():
    if 'imgFile' not in request.files:
        flash('No file part')
        return redirect('/')
    file = request.files['imgFile']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect('/')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('search.search_results',imageFilename=filename))
        #return redirect(url_for('search.download_file', name=filename))
        
@bp.route('/logoUploader', methods=('POST',))
def logo_upload():
    if 'logoFile' not in request.files:
        flash('No file part')
        return redirect('/')
    file = request.files['logoFile']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect('/')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('search.search_results',logoFilename=filename))
        return redirect(url_for('search.download_file', name=filename))

@bp.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], name)