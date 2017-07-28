import sys

sys.path.insert(0, '/app/src')
sys.path.insert(0, '/app/app')

import pandas as pd
import numpy as np
from datetime import datetime as dt
from predictionAPI import predictionAPI
import glob
import math
import os
from regressions.scikit import Regression
import funcs


(df, rid) = funcs.dequeueJob()

if df is not None:

    models_dir = funcs.getModelsDir(rid)
    results_fn = funcs.getResultsFn(rid)
    results_df = predictionAPI.doTrainRequest(rid, models_dir, results_fn, df, funcs.writeLogMsg)
    print("Prediction Results")
    print(results_df)

    funcs.deleteRequest(rid)
    print("Trained, saved, and deleted job")

else:
    print("No job to remove from queue")


