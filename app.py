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
            #print(data)
            return data
    return None

@server.route('/savedescription/<file>')
def savedescription(file):
    with open(getjsonfile(file), "w") as f:
        json.dump(request.args.to_dict(), f)

    return redirect("/")



@server.route('/updatesummary/<file>', methods=["POST"])
def updatesummary(file):
    
    print(request.form.to_dict())
    filename = getjsonfile(file)
    if os.path.exists(filename) is False:
        with open(filename, "w") as f:
            json.dump({"sumary":request.data}, f)
    else:
        data = getdatajsonfile(file)
        with open(filename, "w") as f:
            data["sumary"] = request.data
            json.dump(data, f)
    return ""
       
    
    
@server.route('/editdescription/<file>')
def editdescription(file):
    ar = request.args
    if len(ar)!=0:
        print(ar)
    #data = json.loads(request.args['data'])
    data = getdatajsonfile(file)    
    return render_template('editdescription.html', file=file,data=data)

#
# Read/ Write CSV File.
# 
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
 
#
# Home page list of CSV files/
# 
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
