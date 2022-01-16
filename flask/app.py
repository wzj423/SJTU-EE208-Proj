# SJTU EE208
import os
import sys

from werkzeug.utils import secure_filename

from backend.SearchPages import init_lucene
from flask import Flask, flash, redirect, render_template, request, url_for

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config.from_mapping(
        ENV='development',
        SECRET_KEY='dev',
        #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_lucene()

    # a simple page that says hello
    @app.route('/')
    def redirect_to_search():
        #return redirect(url_for('search.search_results',keywords='中国'))
        return redirect(url_for('search.search_webpages'))
    import search
    app.register_blueprint(search.bp)
    return app


app=create_app()
app.run(debug=True,port=8080)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#https://stackoverflow.com/questions/34066804/disabling-caching-in-flask
#@app.before_first_request


'''
@app.route('/form', methods=['POST', 'GET'])
def bio_data_form():
    if request.method == "POST":
        username = request.form['username']
        age = request.form['age']
        email = request.form['email']
        hobbies = request.form['hobbies']
        return redirect(url_for('showbio', username=username, age=age, email=email, hobbies=hobbies))
    return render_template("bio_form.html")


@app.route('/showbio', methods=['GET'])
def showbio():
    username = request.args.get('username')
    age = request.args.get('age')
    email = request.args.get('email')
    hobbies = request.args.get('hobbies')
    return render_template("show_bio.html", username=username, age=age, email=email, hobbies=hobbies)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
'''
