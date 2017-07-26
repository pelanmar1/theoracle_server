
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

def getTrainingRequestStatus(base_url, request_id):
    url = "%sstatus/%s" % (base_url, request_id)
    request = Request(url)
    jsonstr = urlopen(request).read().decode()
    response = json.loads(jsonstr)
    return (response["done"], response["message"])

def executeTrainingRequest(base_url, request_id):
    url = "%sruntraining/%s" % (base_url, request_id)
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
#
# (done, message) = getTrainingRequestStatus(base_url, request_id)
#
# print ("Reuest Done = ", done)
# print ("Request Msg = ", message)
#
# request_id = "aa89b2c6afa51346cd014948f96a4357"
# response = executeTrainingRequest(base_url, request_id)
# print(response)

request_id = "aa89b2c6afa51346cd014948f96a4357"
response = getTrainingResults(base_url, request_id)
print(response)


