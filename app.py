import sqlite3
import json
import glob
from flask import Flask, request
from flask import render_template
import csv

server = Flask(__name__)


@server.route('/save/<file>', methods=["POST"])
def save(file):
    data = request.form['data']
    print(data)
    return file

@server.route('/edit/<file>')
def edit(file):
    result = []
    with open(file, 'rb') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for r in data:
            result.append(r)
    return render_template('edit.html',file=file,data=result)
    
@server.route('/')
def hello():
    dirs = glob.glob("*.csv")
    return render_template('index.html',dirs=dirs)
    #return "Hello World!"

       
if __name__ == '__main__':
    server.run(debug=True)