from flask import Flask, render_template, request, jsonify,send_file
import pandas
import numpy as np
import os
import hashlib
import datetime
import sys
import glob
import funcs
import pickle
import json
import ast

from flask_cors import CORS, cross_origin


sys.path.insert(0, '/app/src')
from predictionAPI import predictionAPI
from fbProphet import fbProphet
import subprocess

tmp_dir = "/app/data/tmp/"
RESULTS_DIR = "/app/data/results/"

app = Flask(__name__)
CORS(app)

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
        images_dir = funcs.getImagesDir(rid)
        results_dir = funcs.getResultsDir(rid)
        funcs.writeLogMsg("Models " + models_dir)
        funcs.writeLogMsg(train_df.iloc[0])
        funcs.writeLogMsg(str(rid))
        results_df = predictionAPI.doTrainRequest(models_dir,results_dir, train_df, funcs.writeLogMsg,images_dir=images_dir)
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
           df = funcs.cleanDFHeaders(df)
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
    futureVals = json.dumps(request.get_json(force=True)['values'])
    futureVals = ast.literal_eval(futureVals)
    predict_dates_df = funcs.list2Dataframe(futureVals)
    jsonStr = jsonify({'result':futureVals})
    funcs.writeLogMsg(str(predict_dates_df))
    results_fn = funcs.getResultsFn(rid)
    funcs.writeLogMsg("Loading training data" )
    df = funcs.getRequestTrainingData(rid)
    funcs.writeLogMsg("Starting prediction")
    image_fn = None
    result_df =predictionAPI.doPredictionRequest(df,results_fn, mid, predict_dates_df,image_fn, funcs.writeLogMsg)
    if result_df is not None:
        funcs.writeLogMsg(result_df)
        result_df.insert(0, 'date', result_df.index)
        html = result_df.to_html(header=True,index=False)
        html = html.replace('dataframe','table table-condensed')
        jsonDict = jsonify(resTable = html)
        return jsonDict
    else:
        return jsonify({'Message':'There was a problem. Please try again.'})                               
    
    return jsonStr

#------------------------------
@app.route('/getPending')
def handleGetPendingRequest():
    #funcs.writeLogMsg("handleGetPendingModels")
    rids = funcs.getPendingRequestIds()
    if rids is not None:
       jsonDict = jsonify(results = rids)
       #funcs.writeLogMsg(str(jsonDict))
       return jsonDict
    else:
       return jsonify({'Message':'There are no models pending.'})

@app.route('/getDone')
def handleGetDoneRequest():
    #funcs.writeLogMsg("handleGetDoneModels")
    rids = funcs.getDoneRequestIds()
    if rids is not None:
       jsonDict = jsonify(results = rids)
       #funcs.writeLogMsg(str(jsonDict))
       return jsonDict
    else:
       return jsonify({'Message':'There are no models finished yet.'})

#------------------------------
@app.route('/getTrainHTML/<string:rid>')
def handleGetTrainHTMLRequest(rid):
    if rid is not None:
        funcs.writeLogMsg("handleGetCSVRequest")
        train_df = funcs.getRequestTrainingData(rid)
        if train_df is not None:
            train_df.reset_index(inplace=True)
            train_df.columns = ['Date','Value']
            train_df = train_df.ix[1:]
            html = train_df.to_html(header=True,index=False)
            html = html.replace('dataframe','table table-condensed')
            jsonDict = jsonify(trainCSV = html)
            #funcs.writeLogMsg(jsonDict)
            return jsonDict
        else:
            return jsonify({'Message':'Models not ready or don\'t exist, check with /status/<rid>'})
@app.route('/getResultsHTML/<string:rid>')
def handleGetResultsHTMLRequest(rid):
    if rid is not None:
        funcs.writeLogMsg("handleGetCSVRequest")
        res_df = funcs.getRequestResults(rid)
        if res_df is not None:
            res_df.columns = res_df.iloc[0][:].values
            res_df = res_df.iloc[1:][:]
            html = res_df.to_html(header=True,index=False)
            html = html.replace('dataframe','table table-condensed')
            jsonDict = jsonify(resTable = html)
            #funcs.writeLogMsg(jsonDict)
            return jsonDict
        else:
            return jsonify({'Message':'Models not ready or don\'t exist, check with /status/<rid>'})

@app.route('/getModelImage/<string:rid>/<string:modelid>')
def handleGetModelImageRequest(rid,modelid):
    if rid is not None and modelid is not None:
        funcs.writeLogMsg("handleGetModelImageRequest")
        image_fn = funcs.getImageFn(rid,modelid)
        if image_fn is not None:
            return send_file(image_fn, mimetype='image/gif') 
        else:
            return jsonify({'Message':'The requested image does not exist.'})


#------------------------------

#------------------------------

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

