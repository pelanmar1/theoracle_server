from flask import Flask, render_template, request, jsonify
import pandas
import os
import hashlib
import datetime
import sys
sys.path.insert(0, '/app/src')
#import predictionAPI

# UPLOAD_FOLDER = 'inputFiles'
ALLOWED_EXTENSIONS = set(['csv'])
REQUESTS_FOLDER = "/app/data/requests/"

inputFolder = 'inputFiles'
modelsFolder = 'models'

def writeLogMsg(msg):
    dt = datetime.datetime.now()
    with open("request.log", "a") as myfile:
        myfile.write("%s\t%s\n" % (dt, msg))

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# Right now only checks extension but can be edited to check any number of things abour the file to validate it
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Saves job file to specified location
def enqueueJob(df):
    dfs = str(df)
    rid = hashlib.md5(dfs.encode()).hexdigest()
    writeLogMsg("\tenqueueJob() rid " + rid)
    dest_fn = REQUESTS_FOLDER+rid+'.csv'
    if os.path.isfile(dest_fn) == False:
        df.to_csv(dest_fn)
    return rid

#@app.route('/')
#def dataForm():
#    return render_template("dataForm.html")

@app.route('/train', methods=['GET','POST'])
def handlePost():
    tmp_dir = "/app/data/tmp/"

    writeLogMsg("handlePost")
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            dt = datetime.datetime.now()
            dest_fn = "%s%s.csv" % (tmp_dir, dt.strftime("%s"))
            writeLogMsg("\tUploaded File "+ dest_fn)
            file.save(dest_fn)
            df = pandas.read_csv(dest_fn, header=0)
            writeLogMsg(df.describe())
            rid = enqueueJob(df)
            os.remove(dest_fn)
            return rid

    return "not ok"

def getReqStatus(rid):
    writeLogMsg("getReqStatus(%s)" % rid)
    done = False
    msg = ""
    if os.path.isfile(modelsFolder+'/'+rid+'.csv'):
        done = True
        msg = 'Job is complete'
    elif os.path.isfile(REQUESTS_FOLDER+rid+'.csv'):
        msg = 'Job is in queue'
    else:
        msg = 'Job does not exist'
    return (done, msg)

@app.route('/status/<string:rid>')
def handleRequest(rid):
    (done, msg) = getReqStatus(rid)
    jsonDict = {'done': done, 'message':msg}
    return jsonify(jsonDict)

def getModels(rid):
    (done, msg) = getReqStatus(rid)
    if done:
	    return pandas.read_csv(modelsFolder+'/'+rid+'.csv')
    else:
        return None

@app.route('/getmodels/<string:rid>')
def handleModelsRequest(rid):
    df = getModels(rid)
    if df:
        jsonDict = df.to_dict()
        return jsonify(jsonDict)
    else:
        return jsonify({'Message':'Models not ready or don\'t exist, check with /status/<rid>'})

def predict(rid, mid, df):
    return pandas.DataFrame()

@app.route('/predict/<string:rid>/<string:mid>', methods=['POST'])
def handlePredictRequest(rid, mid):
    file = request.files['file']
    file.save('tempFiles/'+file.filename)
    input_df = pandas.read_csv('tempFiles/'+file.filename)
    output_df = predict(rid, mid, input_df)
    jsonDict = output_df.to_dict()
    return jsonify(jsonDict)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

