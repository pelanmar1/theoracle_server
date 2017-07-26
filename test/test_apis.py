
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

# Must have the api server running at the following location
base_url = 'http://localhost:5000/'

# fn = "data/intl_airline_passengers.csv"
# (success, request_id) = submitTrainingRequest(base_url, fn)
#
# print ("Submit Success = ", success)
# print ("Submit Request Id = ", request_id)

# (done, message) = getTrainingRequestStatus(base_url, request_id)

# print ("Reuest Done = ", done)
# print ("Request Msg = ", message)

request_id = "a6b8c27d44e7061e78c0de5ffc5f6604"
# response = executeTrainingRequest(base_url, request_id)
# print(response)


# (done, message) = getTrainingRequestStatus(base_url, request_id)
# print ("Reuest Done = ", done)
# print ("Request Msg = ", message)


# response = getTrainingResults(base_url, request_id)
# print(response)


model_id = 1
fn = "data/intl_airline_passengers_pred.csv"
response = submitPredictRequest(base_url, request_id, model_id, fn)
print(response)

