import numpy as np
import pandas as pd
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import sys
import requests
import datetime
import random
import json
import time


def getAirlinePassengerData():
    input_data_fn = "data/intl_airline_passengers.csv"
    ts = pd.read_csv(input_data_fn, header=None, delimiter=",", parse_dates=True)
    ts.columns = ["date", "y"]
    return ts

def getRandomTimeseries():
    df = pd.DataFrame()
    dt = datetime.datetime.now()
    for i in range(0,100):
        dtstr = dt.strftime("%Y-%m-%d")
        v = int(random.random() * 100)
        df.set_value(dt, "y", v)
        dt = dt + datetime.timedelta(1)

    df.index.name = "date"
    return df

# Given a training or test dataframe, return a df with just the dates
def getDatesDF(df):
    dfc = df.copy()
    dfc.reset_index(inplace=True)
    dfc.drop("y", axis=1, inplace=True)
    return dfc

def submitTrainingRequest(base_url, fn):
    url = "%strain" % (base_url)
    files = {'file': open(fn, 'rb')}
    r = requests.post(url, files=files)
    request_id = r.content.decode()

    if len(request_id) > 10:
        success = True
    else:
        success = False
        request_id = ""

    return (success, request_id)


def submitPredictRequest(base_url, rid, model_id, fn):
    url = "%spredict/%s/%s" % (base_url, rid, model_id)
    files = {'file': open(fn, 'rb')}
    r = requests.post(url, files=files)
    jsonstr = r.content.decode()
    #print(jsonstr)
    df = pd.read_json(jsonstr, orient='split')
    return df


def getTrainingRequestStatus(base_url, request_id):
    url = "%sstatus/%s" % (base_url, request_id)
    request = Request(url)
    jsonstr = urlopen(request).read().decode()
    response = json.loads(jsonstr)
    return (response["done"], response["message"])


def executeTrainingRequest(base_url, request_id):
    url = "%sruntraining/%s" % (base_url, request_id)
    print("Calling Url ", url)
    request = Request(url)
    jsonstr = urlopen(request).read().decode()
    response = json.loads(jsonstr)
    return response

def getTrainingResults(base_url, request_id):
    url = "%sgetmodels/%s" % (base_url, request_id)
    request = Request(url)
    jsonstr = urlopen(request).read().decode()
    #response = json.loads(jsonstr)
    df = pd.read_json(jsonstr, orient='split')
    return df
