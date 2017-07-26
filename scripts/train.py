import sys

sys.path.insert(0, '/app/src')


#import theoracle
import pandas as pd
import numpy as np
from datetime import datetime as dt
from predictionAPI import predictionAPI
import glob
import math
import os
from regressions.scikit import Regression
import funcs



REQUESTS_FOLDER = "/app/data/requests/"
RESULTS_FOLDER = "/app/data/results/"
MODELS_FOLDER = "/app/data/models/"


def convertTs(df):
    """
    Converts dataframe's dates to correct datetime format, and removes the original data file.

    Output:
    A time series with all dates in date time format
    """

    # Loads filename as time series adding date and y column headers
    # converted_ts = pd.read_csv(data_fn, header=0, index_col=0, delimiter=",", names = ['date', 'y'], parse_dates=True)

    # If the dates are floats or integers

    converted_ts = df
    if (isinstance(converted_ts.index.values.tolist()[0], int) or isinstance(converted_ts.index.values.tolist()[0],
                                                                             float)):
        converted_date_vals = []
    else:
        converted_date_vals = converted_ts.index.values

    for time in converted_ts.index.values.tolist():
        # Check if the time is a timestamp and don't try to convert NaNs to datetime.
        if ((isinstance(time, int) or isinstance(time, float)) and (math.isnan(time) is False)):
            time = dt.utcfromtimestamp(time)
            converted_date_vals.append(time)

    # Remove the y values corresponding to NaNs.
    yVals = converted_ts['y'].values.tolist()[0:len(converted_date_vals)]

    converted_ts = pd.DataFrame({'date': converted_date_vals, 'y': yVals}).dropna()

    # Remove original data file (Commented out to avoid accidentally deleting files when testing).
    # os.remove(data_fn)

    return converted_ts





'''
Expecting file to be in the format
,date,y
0,2017-07-25,57.0
1,2017-07-26,16.0
2,2017-07-27,14.0
'''




def deleteJob(rid):

    print("Deleting Job ", rid)
    """
    Deletes job from training folder.
    Input:
    Request Id of job to be deleted.
    """

    fn = REQUESTS_FOLDER + rid + '.csv'
    os.remove(fn)


# def trainAndSaveModel(req_id, data_df):
#     """
#     Trains and saves trained model to CSV.
#
#     Inputs:
#     reqId:request Id of
#     ts: time series
#     """
#
#     algorithmObjects = []
#     # lr = LinearReg()
#     # pfa = PyFluxARIMA()
#     # fbp = fbProphet()
#     reg = Regression()
#     algorithmObjects.append(reg)
#
#     #modelResults = predictionAPI.train(reqId, ts, algorithmObjects)
#
#     results_dir =
#     models_dir
#     results_df = predictionAPI.doTrainRequest(req_id, results_dir, models_dir, data_df)
#
#     # Store model results into a csv file, named with the reqId
#     modelResults.index.name = "modelId"
#     modelResults.to_csv(RESULTS_FOLDER + str(reqId) + '.csv')
#     return


def trainData():
    """
    Parses user's commands, and converts file to dataframe with correct
    date formats. Then it trains the model on the data.
    Inputs:
    file path of future dataframe.
    """

    # Dequeue job and get dataframe and request ID
    (df, rid) = dequeueJob()

    # If there is a dequeued job then do this.
    if df is not None:
        # Converts dataframe, and trains the model on dataframe

        # ts = convertTs(df)

        # algorithmObjects = []
        # # lr = LinearReg()
        # # pfa = PyFluxARIMA()
        # # fbp = fbProphet()
        # reg = Regression()
        # algorithmObjects.append(reg)

        # modelResults = predictionAPI.train(reqId, ts, algorithmObjects)
        #df.index = df.index.to_datetime(format="%s")


        # print(df)
        # Code to test and convert series

        # a = [isinstance(x, np.int64) for x in df.index.values]
        # if a.count(False):
        #     # Index is all timestamps
        #     df.index = df.index.map(dt.fromtimestamp)
        #
        # print("DF Types ", df.dtypes)
        #
        # df.index = df.index.map(dt.fromtimestamp)
        #
        # print(df)
        results_df = predictionAPI.doTrainRequest(rid, MODELS_FOLDER, df)

        # Store model results into a csv file, named with the reqId
        #modelResults.index.name = "modelId"
        #modelResults.to_csv(RESULTS_FOLDER + str(reqId) + '.csv')


        # Delete job
        #deleteJob(rid)
        return "Trained, saved, and deleted job"

    # If there is no job in the queue.
    else:
        print("Error: no job to remove from queue")
        return "Error: no job to remove from queue"



trainData()
