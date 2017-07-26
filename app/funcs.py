import datetime
import pandas as pd
import numpy as np
import os
import hashlib
import sys
import glob
import funcs

REQUESTS_FOLDER = "/app/data/requests/"
ALLOWED_EXTENSIONS = set(['csv'])

# Right now only checks extension but can be edited to check any number of things abour the file to validate it
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def writeLogMsg(msg):
    dt = datetime.datetime.now()
    with open("request.log", "a") as myfile:
        myfile.write("%s\t%s\n" % (dt, msg))

def dequeueJob():
    #print("Dqing job")
    listFiles = glob.glob(REQUESTS_FOLDER + '*.csv')
    if len(listFiles) > 0:
        firstJobPath = min(listFiles, key=os.path.getctime)
        rid = os.path.basename(firstJobPath).split('.')[0]
        #print("Found job with path ", firstJobPath)
        #df = pd.read_csv(firstJobPath, index_col=0, header=0, parse_dates=True)
        df = getRequestByID(req_id)
        #print("Request Id ", rid)
        #os.system('mv '+firstJobPath+' '+TRAINING_FOLDER+os.path.basename(firstJobPath)) # moves job
        return (df, rid)
    else:
        return (None, "")

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def getRequestDir(rid):
    return REQUESTS_FOLDER + rid + "/"

def getModelsDir(rid):
    dir = getRequestDir(rid) + "models/"
    ensure_dir(dir)
    return dir

def getResultsDir(rid):
    return getRequestDir(rid)

def getResultsFn(rid):
    return getResultsDir(rid) + "results.csv"

def getRequestTrainingDataFn(rid):
    return getRequestDir(rid) + "train.csv"

def getRequestTrainingData(req_id):
    fn = getRequestTrainingDataFn(req_id)
    writeLogMsg("Loading file " + fn)
    if os.path.isfile(fn):
        df = pd.read_csv(fn, index_col=0, header=None, parse_dates=True)
        df.index.name = "date"
        df.columns = ["y"]
        writeLogMsg("Done")
        return df
    else:
        writeLogMsg("ERROR: File does not exist\n"+fn)
        return None

def saveResultsDF(rid, results_df):
    fn = getResultsFn(rid)
    writeLogMsg("Saving Result To '%s'" % fn)
    results_df.to_csv(fn)

# Saves job file to specified location
def enqueueJob(df):
    writeLogMsg("Enqueue ")
    writeLogMsg(df.head())
    dfs = str(df)
    rid = hashlib.md5(dfs.encode()).hexdigest()
    writeLogMsg("\tenqueueJob() rid " + rid)
    ensure_dir(getRequestDir(rid))
    dest_fn = getRequestTrainingDataFn(rid)
    if os.path.isfile(dest_fn) == False:
        df.to_csv(dest_fn, header=False)
    return rid

def getModels(rid):
#   (done, msg) = getReqStatus(rid)
#   if done:
    results_fn = funcs.getResultsFn(rid)
    if os.path.isfile(results_fn):
       writeLogMsg("Loading results file " + results_fn)
       df = pd.read_csv(results_fn, header=0)
       return df
    else:
        return None

"""
 Input:
  index = a 0 to n based index numbering the samples
  Col 1 = A timestamp or date (2017-07-0)
  Col 2 = The y floating point values
 Output:
  index = a 0 to n based index numbering the samples
  date = A Datetime (2017-07-0)
  y = The y floating point values
"""
def cleanUpDf(df):
    writeLogMsg("Before Cleaning")
    writeLogMsg(df.head())
    writeLogMsg(df.dtypes)
    a = [isinstance(x, np.int64) for x in df[1].values]
    if a.count(False):
        # Index is all timestamps
        df[1] = df[1].map(datetime.datetime.fromtimestamp)

    df.columns = ["date", "y"]

    writeLogMsg("After Cleaning")
    writeLogMsg(df.head())

    return df