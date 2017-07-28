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
import testlib

# Must have the api server running at the following location
base_url = 'http://localhost:5000/'

request_id = "a6b8c27d44e7061e78c0de5ffc5f6604"

fn = "data/intl_airline_passengers.csv"
(success, request_id) = testlib.submitTrainingRequest(base_url, fn)

print ("Submit Success = ", success)
print ("Submit Request Id = ", request_id)

(done, message) = testlib.getTrainingRequestStatus(base_url, request_id)

print ("Reuest Done = ", done)
print ("Request Msg = ", message)

sys.exit()

#response = executeTrainingRequest(base_url, request_id)
#print(response)



# (done, message) = getTrainingRequestStatus(base_url, request_id)
# print ("Reuest Done = ", done)
# print ("Request Msg = ", message)


#response = testlib.getTrainingResults(base_url, request_id)
#print(response)


model_id = 1
fn = "data/intl_airline_passengers_pred.csv"
response = testlib.submitPredictRequest(base_url, request_id, model_id, fn)
print(response)

sys.exit()
