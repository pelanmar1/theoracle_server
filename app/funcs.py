import datetime
import pandas as pd
import numpy as np
import os
import hashlib
import sys
import glob
import funcs

REQUESTS_FOLDER = "/app/data/requests/"


def writeLogMsg(msg):
    dt = datetime.datetime.now()
    with open("request.log", "a") as myfile:
        myfile.write("%s\t%s\n" % (dt, msg))

def getRequestByID(req_id):
    fn = REQUESTS_FOLDER + req_id + '.csv'
    df = pd.read_csv(fn, index_col=0, header=0, parse_dates=True)
    return df


def dequeueJob():
    print("Dqing job")
    listFiles = glob.glob(REQUESTS_FOLDER + '*.csv')
    if len(listFiles) > 0:
        firstJobPath = min(listFiles, key=os.path.getctime)
        rid = os.path.basename(firstJobPath).split('.')[0]
        print("Found job with path ", firstJobPath)
        #df = pd.read_csv(firstJobPath, index_col=0, header=0, parse_dates=True)
        df = getRequestByID(req_id)
        print("Request Id ", rid)
        #os.system('mv '+firstJobPath+' '+TRAINING_FOLDER+os.path.basename(firstJobPath)) # moves job
        return (df, rid)
    else:
        return (None, "")

# Saves job file to specified location
def enqueueJob(df):
    writeLogMsg("Enqueue ")
    writeLogMsg(df.head())
    dfs = str(df)
    rid = hashlib.md5(dfs.encode()).hexdigest()
    writeLogMsg("\tenqueueJob() rid " + rid)
    dest_fn = REQUESTS_FOLDER+rid+'.csv'
    if os.path.isfile(dest_fn) == False:
        df.to_csv(dest_fn, header=True)
    return rid


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