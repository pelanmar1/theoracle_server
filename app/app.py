from flask import Flask, render_template, request, jsonify
import pandas
import numpy as np
import os
import hashlib
import datetime
import sys
import glob
import funcs

import pickle


sys.path.insert(0, '/app/src')
from predictionAPI import predictionAPI
from fbProphet import fbProphet
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



app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# Right now only checks extension but can be edited to check any number of things abour the file to validate it
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/runtraining/<string:rid>', methods=['GET'])
def runTraining(rid):
    funcs.writeLogMsg("Run Training " + rid)

    df = funcs.getRequestByID(rid)

    results_df = predictionAPI.doTrainRequest(rid, RESULTS_FOLDER, MODELS_FOLDER, df)

    #algo = fbProphet()
    #params = {'growth':'logistic', 'cap':200000000}
    #show_graph = False
    #(model, result_df, errors) = predictionAPI.trainAndEval(algo, params, training_data_df, test_data_df, show_graph)

    #funcs.writeLogMsg(str(results_df))
    #funcs.writeLogMsg(str(errors))

    jsonDict = {'done': 6, 'message': ""}
    return jsonify(jsonDict)



'''
Expecting something like

2017-07-25,92.0
2017-07-26,88.0
2017-07-27,84.0
2017-07-28,65.0
2017-07-29,94.0
2017-07-30,89.0
'''
@app.route('/train', methods=['GET','POST'])
def handlePost():
   funcs.writeLogMsg("handlePost")
   if request.method == 'POST':
       file = request.files['file']
       if file and allowed_file(file.filename):
           dt = datetime.datetime.now()
           dest_fn = "%s%s.csv" % (tmp_dir, dt.strftime("%s"))
           file.save(dest_fn)
           funcs.writeLogMsg("\tUploaded File " + dest_fn)
           df = pandas.read_csv(dest_fn, header=None, parse_dates=True)
           df.columns = ["date", "y"]
           funcs.writeLogMsg("\tRead csv")
           #df = funcs.cleanUpDf(df)
           rid = funcs.enqueueJob(df)
           return rid

   return "not ok"

def getReqStatus(rid):
   funcs.writeLogMsg("getReqStatus(%s)" % rid)
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
       jsonDict = df.to_json(orient='split')
       #funcs.writeLogMsg(jsonDict)
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
       funcs.writeLogMsg("WORKING -X-X-X-X-X-X-X-X-X-X-X-X--X-X-X-")
       jsonDict = output_df.to_json()
       return jsonDict

   return msg

@app.route('/run')
def runJob():
   #os.system("python train.py")
   output = subprocess.check_output("python train.py", shell=True)
   #funcs.writeLogMsg('ok')
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
       funcs.writeLogMsg('About to save to csv')
       df.to_csv(MODELS_FOLDER+rid+'.csv')

   return 'done'
   '''

if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0')

