from flask import Flask, render_template, redirect, url_for
import os, json
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/web_app'
db = SQLAlchemy(app)

client = MongoClient('127.0.0.1', 27017)
db_mongo = client.shiyanlou


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %s>' % self.name


class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category')

    def add_tag(self, tag_name):
        file_item = db_mongo.files.find_one({'file_id': self.id})
        files = db_mongo.files
        if file_item:
            tags = file_item['tags']
            tags.append(tag_name)
            files.update_one({'file_id': self.id}, {'$set':{'tags':tags}})    
        else:
            tags = [tag_name]
            files.insert_one({'file_id': self.id, 'tags': tags})
                   

    def remove_tag(self, tag_name):
        file_item = db_mongo.files.find_one({'file_id': self.id})
        files = db_mongo.files
        if file_item:
            try:
                tags = file_item['tags']
                tags.remove(tag_name)
            except ValueError:
                return
            files.update_one({'file_id': self.id}, {'$set':{'tags':tags}})       
        else:
            return


    @property
    def tags(self):
        file_item = db_mongo.files.find_one({'file_id': self.id})
        files = db_mongo.files
        if file_item:
            return file_item['tags']
        else:
            return []

    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content
        
    def __repr__(self):
        return '<File %s>' % self.title
 
def insert_data():
    db.create_all()

    java = Category('Java')
    python = Category('Python')
    file1 = File('Hello Java', datetime.utcnow(), java, 'File Content - Java is cool!')
    file2 = File('Hello Python', datetime.utcnow(), python, 'File Content - Python is cool!')
    db.session.add(java)
    db.session.add(python)
    db.session.add(file1)
    db.session.add(file2)
    db.session.commit()

    file1.add_tag('tech')
    file1.add_tag('java')
    file1.add_tag('linux')
    file2.add_tag('tech')
    file2.add_tag('python')

@app.errorhandler(404)
def not_fount(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html', files=File.query.all())            


@app.route('/files/<file_id>')
def file(file_id):
    f = File.query.filter_by(id=file_id).first()
    if f is None:
        return render_template('404.html')
    else:
        return render_template('file.html', file = f)
