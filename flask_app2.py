from flask import Flask
from flask import make_response, url_for, redirect
from flask import render_template

import json

import os


PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
data_path    = os.path.join(PROJECT_ROOT, 'data', 'data.json')
img_dir_path = 'static/img/'

data = json.loads( open(data_path,'r').read() )
my_info   = data["my_info"]
page_data = data["page_data"]
projects  = data["projects"]

app = Flask(__name__)


# ------------------------------------------------------------------------------
@app.context_processor
def override_url_for():
    '''Redirects ``url_for(..)`` to ``dated_url_for(..)`` in this app'''
    return dict(url_for=dated_url_for)
def dated_url_for(endpoint, **values):
    '''Appends static endpoints with last modified time - to make them
    dynamic'''
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


# ==============================================================================
@app.route('/', methods=['GET'])
def index():
    '''Home Page'''

    my_img     = img_dir_path + my_info['img']
    cover_img  = img_dir_path + page_data['cover_img']
    github_img = img_dir_path + page_data['github_img']

    return render_template(
            'index.html',
            my_img       = my_img           ,
            my_links     = my_info['links'] ,
            cover_img    = cover_img        ,
            github_img   = github_img       ,
            projects     = projects         ,
            img_dir_path = img_dir_path
        )


# ******************************************************************************
if __name__ == '__main__':
    app.secret_key = 'very_secure_password'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
