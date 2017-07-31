import numpy as np
import pandas as pd
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import sys
import time
import testlib
import time
import graph

base_url = 'http://localhost:5000/'

data_fn = "data/random.csv"
data_df = testlib.getRandomTimeseries()
data_df = testlib.getRandomTimeseries()
data_df.to_csv(data_fn, header=None)

test_dates_fn = "data/test_dates.csv"
test_dates_df = testlib.getDatesDF(data_df)
test_dates_df.to_csv(test_dates_fn, header=None, date_format='%Y-%m-%d')


(success, request_id) = testlib.submitTrainingRequest(base_url, data_fn)

print ("Submit Success = ", success)
print ("Submit Request Id = ", request_id)

while True:

    (done, message) = testlib.getTrainingRequestStatus(base_url, request_id)
    print ("Reuest Done = ", done)
    print ("Request Msg = ", message)

    if done:
        break
    else:
        time.sleep(3)

sys.exit()



request_id = "1071338945f6f0f4aa20860939ba46de"

results_df = testlib.getTrainingResults(base_url, request_id)
print(results_df)

#for idx, row in results_df.iterrows():

#model_id = row["model"]
model_id = 0
predictions_df = testlib.submitPredictRequest(base_url, request_id, model_id, test_dates_fn)
if len(predictions_df.index) == 0:
    print("Predictions are empty")
else:
    #print(predictions_df)
    g = graph.Graph("Prediction Results (r-Data, g-Preds)")
    g.addLine(data_df, "y", "r")
    g.addLine(predictions_df, "yhat", "g")
    g.show()


sys.exit()
