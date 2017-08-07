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
import subprocess

tmp_dir = "/app/data/tmp/"

app = Flask(__name__)

@app.route('/')
def home():
    return 'Server is running.'

#------------------------------
@app.route('/runtraining/<string:rid>', methods=['GET'])
def runTraining(rid):
    funcs.writeLogMsg("Run Training " + rid)

    train_df = funcs.getRequestTrainingData(rid)
    if train_df is not None:
        models_dir = funcs.getModelsDir(rid)
        funcs.writeLogMsg("Models " + models_dir)
        results_df = predictionAPI.doTrainRequest(rid, models_dir, train_df, funcs.writeLogMsg)
        funcs.saveResultsDF(rid, results_df)
        funcs.writeLogMsg(results_df.head())
        jsonDict = {'done': True, 'message': ""}
    else:
        jsonDict = {'done': False, 'message': "Could not find training data"}

    return jsonify(jsonDict)


#------------------------------
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
       if file and funcs.allowedFile(file.filename):
           dt = datetime.datetime.now()
           dest_fn = "%s%s.csv" % (tmp_dir, dt.strftime("%s"))
           file.save(dest_fn)
           funcs.writeLogMsg("\tUploaded File " + dest_fn)
           df = pandas.read_csv(dest_fn, header=None, index_col=0, parse_dates=True)
           df.columns = ["y"]
           funcs.writeLogMsg("\tRead csv")
           #df = funcs.cleanUpDf(df)
           rid = funcs.enqueueJob(df)
           return rid

   return "not ok"

#------------------------------
def getReqStatus(rid):
   funcs.writeLogMsg("getReqStatus(%s)" % rid)
   done = False
   msg = ""
   rfn = funcs.getResultsFn(rid)
   funcs.writeLogMsg("Request Fn = %s" % rfn)
   if os.path.isfile(rfn):
       done = True
       msg = 'Job is complete'
   elif os.path.isfile(funcs.getRequestTrainingDataFn(rid)):
       msg = 'Job is in queue'
   else:
       msg = 'Job does not exist'

   return (done, msg)

#------------------------------
@app.route('/status/<string:rid>')
def handleRequest(rid):
   (done, msg) = getReqStatus(rid)
   jsonDict = {'done': done, 'message':msg}
   return jsonify(jsonDict)


#------------------------------
def cleanDictKeys(mydict):
   for key in mydict.keys():
       mydict[key] = str(mydict)

#------------------------------
@app.route('/getmodels/<string:rid>')
def handleModelsRequest(rid):
    funcs.writeLogMsg("handleModelsRequest")
    df = funcs.getModels(rid)
    if df is not None:
       jsonDict = df.to_json(orient='split')
       #funcs.writeLogMsg(jsonDict)
       return jsonDict
    else:
       return jsonify({'Message':'Models not ready or don\'t exist, check with /status/<rid>'})

#------------------------------
@app.route('/predict/<string:rid>/<string:mid>', methods=['POST'])
def handlePredictRequest(rid, mid):
    funcs.writeLogMsg("handlePredictRequest")
    file = request.files['file']
    fn = tmp_dir+file.filename
    file.save(fn)
    funcs.writeLogMsg("readin File " + fn)
    predict_dates_df = pandas.read_csv(tmp_dir+file.filename, index_col=0)
    predict_dates_df.columns = ["date"]
    funcs.writeLogMsg("Predict Dates")
    funcs.writeLogMsg(predict_dates_df.head())

    results_fn = funcs.getResultsFn(rid)
    models_dir = funcs.getModelsDir(rid)
    predictions_df = predictionAPI.doPredictionRequest(results_fn, models_dir,
                                                       rid, mid,
                                                      predict_dates_df,
                                                       funcs.writeLogMsg)
    funcs.writeLogMsg("Predictions")
    funcs.writeLogMsg(predictions_df.head())

    jsonStr = predictions_df.to_json(date_format='iso', orient='split')
    return jsonStr

#------------------------------
# @app.route('/run')
# def runJob():
#    #os.system("python train.py")
#    output = subprocess.check_output("python train.py", shell=True)
#    #funcs.writeLogMsg('ok')
#    return 'ok'
#
#    # dequeueJob
#    '''listFiles = glob.glob(REQUESTS_FOLDER + '*')
#    df = None
#    rid = ''
#    if len(listFiles) > 0:
#        firstJobName = min(listFiles, key=os.path.getctime)
#        df = pandas.read_csv(firstJobName)
#        rid = firstJobName.split('/')[-1].split('.')[0]
#
#    # save df as csv in models folder to test
#    if df is not None:
#        funcs.writeLogMsg('About to save to csv')
#        df.to_csv(MODELS_FOLDER+rid+'.csv')
#
#    return 'done'
#    '''

if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0')

