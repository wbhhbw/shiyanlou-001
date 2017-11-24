from flask import Flask, render_template

app = Flask(__name__)

@app.errorhandler(404)
def not_fount(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    pass

@app.route('/files/<filename>')
def file(filename):
    pass

