# models/model.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
import pandas as pd
import json
import joblib

from utils import utils
from config import config

def predict(data,file_path):
    """
    Predicts the target variable using a pre-trained linear regression model.

    Parameters:
    ----------
    data : np.ndarray
        A NumPy array of transformed input features.
    file_path : str
        (Unused) Reserved for future use if model path is dynamic.

    Returns:
    -------
    float or np.ndarray
        The predicted car price(s) in real-world units, after inverse scaling.
    """

    with open(config.MODEL, "r") as f:
        loaded_weights = json.load(f)

    theta_0 = loaded_weights["theta_0"]
    theta = np.array(loaded_weights["theta"]) 


    y_pred = theta_0 + np.matmul(data, theta)
    y_real = utils.un_scale(config.Y_SCALER,y_pred)
    return y_real