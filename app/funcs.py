import datetime
import pandas as pd
import numpy as np
import os
import hashlib
import sys
import glob
import funcs


ALLOWED_EXTENSIONS = set(['csv'])

# Right now only checks extension but can be edited to check any number of things abour the file to validate it
def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def writeLogMsg(msg):
    dt = datetime.datetime.now()
    with open("request.log", "a") as myfile:
        myfile.write("%s\t%s\n" % (dt, msg))

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def getResultsDir(rid=None):
    if rid is not None:
        return "/app/data/results/" + rid + "/"
    else:
        return "/app/data/results/"


def getRequestsDir():
    REQUESTS_FOLDER = "/app/data/requests/"
    return REQUESTS_FOLDER

def getRequestFn(rid):
    return getRequestsDir() + rid + ".txt"

def deleteRequest(rid):
    fn = getRequestFn(rid)
    os.remove(fn)

def deleteResult(rid):
    if(rid!= None):
        fn = getResultsDir(rid)
        os.remove(fn)

def getModelsDir(rid):
    dir = getResultsDir(rid) + "models/"
    ensure_dir(dir)
    return dir

def getResultsFn(rid):
    return getResultsDir(rid) + "results.csv"

def getImagesDir(rid):
    dir = getResultsDir(rid) + "images/"
    ensure_dir(dir)
    return dir

def getImageFn(rid,modelId):
    dir = getImagesDir(rid) + str(modelId) + '.png'
    if os.path.isfile(dir):
        return dir
    else:
        writeLogMsg('The requested model image does not exist.')
        return None

def getRequestTrainingDataFn(rid):
    return getResultsDir(rid) + "train.csv"

def getPendingRequestIds():
    dir = getRequestsDir()
    files = glob.glob(dir + '*.txt')
    files1 = [file.replace('.txt', '') for file in files]
    rids = [file.replace(dir, '') for file in files1]
    return rids

def getDoneRequestIds():
    dir = getResultsDir()[:-1]
    rids =[name for name in os.listdir(dir) if os.path.isdir(dir+'/'+name) and os.path.isfile(dir+'/'+name+'/results.csv')]
    return rids


def getNextRequestId():
    rids = getPendingRequestIds()
    print("Pending Requests")
    print(rids)
    if len(rids)==0:
        return None
    else:
        rid = rids[0]
        print("Next Req Id = ", rid)
        return rid

def dequeueJob():
    print("Dqing job")
    rid = getNextRequestId()
    if rid is not None:
        data_df = getRequestTrainingData(rid)
        print("Got Data ")
        print(data_df.head())
        return (data_df, rid)
    else:
        return (None, "")

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

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)

# Saves job file to specified location
def enqueueJob(df):
    writeLogMsg("Enqueue ")
    writeLogMsg(df.head())
    dfs = str(df)
    rid = hashlib.md5(dfs.encode()).hexdigest()
    writeLogMsg("\tenqueueJob() rid " + rid)
    ensure_dir(getResultsDir(rid))
    dest_fn = getRequestTrainingDataFn(rid)
    if os.path.isfile(dest_fn) == False:
        df.to_csv(dest_fn, header=False)

    touch(getRequestFn(rid))
    return rid

def getModels(rid):
    results_fn = funcs.getResultsFn(rid)
    if os.path.isfile(results_fn):
       writeLogMsg("Loading results file " + results_fn)
       df = pd.read_csv(results_fn, header=0)
       return df
    else:
        return None


def list2Dataframe(lst):
    df = pd.DataFrame({'date':lst})
    df['date']=pd.to_datetime(df['date'])
    return df


def getRequestResults(req_id):
    fn = funcs.getResultsFn(req_id)
    writeLogMsg("Loading file " + fn)
    if os.path.isfile(fn):
        df = pd.read_csv(fn, index_col=0, header=None, parse_dates=True)
        writeLogMsg("Done")
        return df
    else:
        writeLogMsg("ERROR: File does not exist\n"+fn)
        return None

def cleanDFHeaders(df):
    if df is not None and df.shape[0]>0 and df.shape[1]>0:
            #first_cell = df.iloc[0][1]
            #funcs.writeLogMsg(str(df.iloc[0]))
            #if type(first_cell) == 'str':
            df = df.iloc[1:][:]
    return df


'''

 Input:
  index = a 0 to n based index numbering the samples
  Col 1 = A timestamp or date (2017-07-0)
  Col 2 = The y floating point values
 Output:
  index = a 0 to n based index numbering the samples
  date = A Datetime (2017-07-0)
  y = The y floating point values
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


'''