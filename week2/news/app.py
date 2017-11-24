from flask import Flask, render_template, redirect, url_for
import os, json

app = Flask(__name__)

@app.errorhandler(404)
def not_fount(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    json_list=[]
    files_list = os.listdir('../files')
    for filename in files_list:
        with open(os.path.join('../files', filename), 'r') as f:
            article_dict = json.loads(f.read())
            json_list.append(article_dict)
    return render_template('index.html', json_list=json_list)            


@app.route('/files/<filename>')
def file(filename):
    absr_path = os.path.join('../files', filename+'.json')
    if os.path.exists(absr_path):        
        with open(absr_path, 'r') as f:
            article_dict = json.loads(f.read())        
        return render_template('file.html', article_dict=article_dict)
    else:
        return render_template('404.html')