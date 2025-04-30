# data_transformation/data_transformation.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
import sklearn

from utils import utils
from config import config

categorical_columns = config.CATEGORICAL_COLUMNS
numerical_columns = config.NUMERICAL_COLUMNS
encoding_dir_paths = config.ENCODING_PATHS
nominal_columns = config.NOMINAL_COLUMNS

user_input = {
    "year": 2013,
    "manufacturer": "ford",
    "model": "f-150 xlt",
    "condition": "excellent",
    "cylinders": "6 cylinders",
    "fuel": "gas",
    "odometer": 128000.0,
    "transmission": "automatic",
    "drive": "rwd",
    "size": "full-size",
    "type": "truck",
    "paint_color": "black",
    
}

def process_input(input_data):
    """
    Transforms a raw input dictionary into a processed NumPy array for inference.

    :param input_data: Dictionary with raw input values.
    :return: NumPy array ready for inference.
    """
    
    # Convert input dictionary to DataFrame
    data = pd.DataFrame([input_data])
    
    # Avoiding int interpreted as str 
    data['year'] = pd.to_numeric(data['year'], errors='coerce')
    data['odometer'] = pd.to_numeric(data['odometer'], errors='coerce')

    # Step 1: Encode categorical variables using predefined JSON encoding dictionaries
    for col in categorical_columns:
        utils.encode(data, col, encoding_dir_paths[col])  # Uses encode() from utils

    # Step 2: Apply One-Hot Encoding (OHE)
    for col in nominal_columns:
        ohe_dfs = utils.convert_to_ohe_input(data[col][0], col, encoding_dir_paths[col])
        data = pd.concat([data, ohe_dfs], axis=1)
    
    data.drop(columns = nominal_columns, inplace=True)
    
    # Step 3: Normalize numerical features
    data["year"] -= 1886  # Normalize year
  
    # Step 4: Keep relevant columns
    processed_data = utils.keep_relevant_columns(data,config.RELEVENT_COLUMNS_IDX)  
    
    # Step 5: Remove highly skewed columns by using log transform
    processed_data = utils.apply_log1p(processed_data,config.SKEW_VALUES_INDICES)
    
    # Step 6: Scale input data
    processed_data = utils.scale(config.X_SCALER, processed_data)

    # Step 5: Apply PCA transformation
    processed_data = utils.apply_pca_by_Q_mat(config.Q_MATRIX, processed_data)

    

    return processed_data
    # return data.shape
    

# if __name__ == "__main__":
#     print(process_input(user_input))  
    
   

    




    



    

