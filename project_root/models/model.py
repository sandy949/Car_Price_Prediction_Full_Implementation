# models/model.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
import pandas as pd
import json
import joblib
from numpy import expm1

from utils import utils
from config import config

p = np.array([
    0.19849544, -0.16784018,  0.03859737,  0.0713949,  0.07724317, -0.03871399,
   -0.02593844,  0.18330161, -0.03562233,  0.47344241, -0.0219909, -0.34953354,
   -0.13865566,  0.16082946, -0.02754872,  0.0224978,  0.118096,   0.11671947,
    0.04061382,  0.02303464,  0.08262756, -0.00765489, 0.00206216, 0.00167276,
    0.00086565,  0.00480422, -0.00478028, 0.00047516
])

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
    
    # Load the model
    model = joblib.load(file_path)

    # Predict in transformed space
    if data.ndim == 1:
        data = data.reshape(1,-1)

    y_pred = model.predict(data)
    
    # Ensure y_pred is 2D
    if y_pred.ndim == 1:
        y_pred = y_pred.reshape(-1, 1)

    # Reverse scaling
    y_unscaled = utils.un_scale(config.Y_SCALER, y_pred)

    # Reverse log1p transformation
    y_real = expm1(y_unscaled)

    return y_real


# if __name__ == "__main__":
#     print(predict(p,config.MODEL))  