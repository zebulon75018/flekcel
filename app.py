import sqlite3
import json
import glob
from flask import Flask, request, Response, redirect
from flask import render_template
import csv
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

server = Flask(__name__)

def getjsonfile(file):
    return "%s.json" % (file)


def getdatajsonfile(file):
    filenamejson = getjsonfile(file)
    print(filenamejson)
    if os.path.isfile(filenamejson):
        with open(filenamejson, "r") as f:
            data = json.load(f)
            print(data)
            return data
    return None

@server.route('/savedescription/<file>')
def savedescription(file):
    with open(getjsonfile(file), "w") as f:
        json.dump(request.args.to_dict(), f)

    return redirect("/")


@server.route('/editdescription/<file>')
def editdescription(file):
    data = getdatajsonfile(file)    
    return render_template('editdescription.html', file=file,data=data)

@server.route('/save/<file>', methods=["POST"])
def save(file):
    data = json.loads(request.form['data'])    
    with open(file, 'wb') as f:  
        # Create Writer Object
        wr = csv.writer(f)
        # Write Data to File
        for item in data:
            wr.writerow(item)

    return Response(status=200)     

@server.route('/edit/<file>')
def edit(file):
    result = []
    description = getdatajsonfile(file)
    with open(file, 'rb') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for r in data:
            result.append(r)
    return render_template('edit.html', file=file, data=result, description=description)
    
@server.route('/')
def hello():
    datas = {}
    dirs = glob.glob("*.csv")
    for f in dirs:
        datas[f] = getdatajsonfile(f)                     
    return render_template('index.html',dirs=dirs,datas =datas)
    #return "Hello World!"

       
if __name__ == '__main__':
    server.run(debug=True)
