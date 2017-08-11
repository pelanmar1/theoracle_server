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
    images_dir = funcs.getImagesDir(rid)
    funcs.writeLogMsg("Models " + models_dir)
    results_df = predictionAPI.doTrainRequest(models_dir, results_fn, df, funcs.writeLogMsg,images_dir)
    funcs.saveResultsDF(rid, results_df)
    funcs.writeLogMsg("Trained, saved, and deleted job")
    funcs.deleteRequest(rid)
else:
    print("No job to remove from queue")


