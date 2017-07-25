from flask import Flask, render_template, request, jsonify
import pandas
import os
import hashlib
import datetime
import sys
import glob
sys.path.insert(0, '/app/src')
from predictionAPI import predictionAPI
#import train
import subprocess

# UPLOAD_FOLDER = 'inputFiles'
ALLOWED_EXTENSIONS = set(['csv'])
REQUESTS_FOLDER = "/app/data/requests/"
TRAINING_FOLDER = "/app/data/training/"
MODELS_FOLDER = "/app/data/models/"
RESULTS_FOLDER = "/app/data/results/"

tmp_dir = "/app/data/tmp/"

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
        df.to_csv(dest_fn, header=False)
    return rid

#@app.route('/')
#def dataForm():
#    return render_template("dataForm.html")

@app.route('/train', methods=['GET','POST'])
def handlePost():
    writeLogMsg("handlePost")
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            dt = datetime.datetime.now()
            dest_fn = "%s%s.csv" % (tmp_dir, dt.strftime("%s"))
            file.save(dest_fn)
            writeLogMsg("\tUploaded File " + dest_fn)
            df = pandas.read_csv(dest_fn, index_col=0, header=None, parse_dates=True)
            writeLogMsg(df.describe())
            rid = enqueueJob(df)
            #os.remove(dest_fn)
            return rid

    return "not ok"

def getReqStatus(rid):
    writeLogMsg("getReqStatus(%s)" % rid)
    done = False
    msg = ""
    if os.path.isfile(RESULTS_FOLDER+rid+'.csv'):
        done = True
        msg = 'Job is complete'
    elif os.path.isfile(REQUESTS_FOLDER+rid+'.csv'):
        msg = 'Job is in queue'
    elif os.path.isfile(TRAINING_FOLDER+rid+'.csv'):
        msg = 'Job is being processed (model is being trained)'
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
        return pandas.read_csv(RESULTS_FOLDER+rid+'.csv')
    else:
        return None

def cleanDictKeys(mydict):
    for key in mydict.keys():
        mydict[key] = str(mydict)

@app.route('/getmodels/<string:rid>')
def handleModelsRequest(rid):
    df = getModels(rid)
    if df is not None:
        jsonDict = df.to_json()
        writeLogMsg(jsonDict)
        return jsonDict
    else:
        return jsonify({'Message':'Models not ready or don\'t exist, check with /status/<rid>'})

@app.route('/predict/<string:rid>/<string:mid>', methods=['POST'])
def handlePredictRequest(rid, mid):
    file = request.files['file']
    file.save(tmp_dir+file.filename)
    input_df = pandas.read_csv(tmp_dir+file.filename)

    (done,msg) = getReqStatus(rid)
    if done:
        output_df = predictionAPI.predict(futureDf=input_df, reqId=rid, modelId=mid)
        writeLogMsg("WORKING -X-X-X-X-X-X-X-X-X-X-X-X--X-X-X-")
        jsonDict = output_df.to_json()
        return jsonDict

    return msg

@app.route('/run')
def runJob():
    #os.system("python train.py")
    output = subprocess.check_output("python train.py", shell=True)
    #writeLogMsg('ok')
    return 'ok'

    # dequeueJob
    '''listFiles = glob.glob(REQUESTS_FOLDER + '*')
    df = None
    rid = ''
    if len(listFiles) > 0:
        firstJobName = min(listFiles, key=os.path.getctime)
        df = pandas.read_csv(firstJobName)
        rid = firstJobName.split('/')[-1].split('.')[0]

    # save df as csv in models folder to test
    if df is not None:
        writeLogMsg('About to save to csv')
        df.to_csv(MODELS_FOLDER+rid+'.csv')

    return 'done'
    '''

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

