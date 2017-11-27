from flask import Flask, render_template, redirect, url_for
import os, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/web_app'
db = SQLAlchemy(app)

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

    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content
        
    def __repr__(self):
        return '<File %s>' % self.title
 
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
