# utils/utils.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
import pandas as pd
import json
import joblib
from config import config

def encode(data, column_name, json_file_path):
    """
    Encodes nominal categorical values using a predefined mapping from a JSON file.

    :param data: DataFrame containing the column to encode.
    :param column_name: The column to encode.
    :param json_file_path: Path to the JSON file containing encoding mappings.
    :return: DataFrame with the encoded column.
    """
    
    # Load encoding dictionary from JSON
    with open(json_file_path, "r") as file:
        encoding_dict = json.load(file)

    data[column_name].replace(to_replace=list(encoding_dict.keys()),
                          value=list(encoding_dict.values()),inplace=True)
    
    

def convert_to_ohe_input(value, column_name, json_file_path):
    """
    Converts a single categorical value into one-hot encoded DataFrame using a mapping from a JSON file.

    :param value: The input value to be one-hot encoded.
    :param json_file_path: Path to the JSON file containing encoding mappings.
    :param column_name: The name of the feature (used for naming OHE columns).
    :return: One-hot encoded DataFrame for the input value.
    """
    # Load encoding dictionary
    with open(json_file_path, 'r') as f:
        encoding_dict = json.load(f)

    value = int(value)
    num_categories = len(encoding_dict)
    if column_name == "model": # as we have a many to one dict
        num_categories = 774
    ohe_vector = np.eye(num_categories)[value]

    column_names = [f"{column_name}{i}" for i in range(num_categories)]
    ohe_df = pd.DataFrame([ohe_vector], columns=column_names)

    return ohe_df

def keep_relevant_columns(data, file_path):
   """
   Removes Predefined columns which have less than 0.07 pearson coorelation with the target variable.
   
   :param data: pd dataframe on which the columns are to be reduced.
   :param file_path: path to file containing the array which has the indexes of column which to keep.
   :return: dataframe with only relevant columns present.
   """

   loaded_file = np.load(file_path,allow_pickle=True)
   
   data = data.iloc[:,loaded_file]
   return data

def apply_pca_by_Q_mat(file_path,data):
    """
    Applies PCA on input data by using a already calculated Q matrix.
    
    :param file_path: path to the file containing the Q_matrix.
    :param data: pd dataframe on which the PCA will be applied.
    :return: A numpy array with PCA applied on it
    """

    Q_mat = np.load(file_path,allow_pickle=True)
    unprojected_X = np.array(data)
    projected_X = np.matmul(unprojected_X,Q_mat)
    return projected_X




def scale(file_path,data):
    """
    Loads a given scaler and scales the data using it.

    :param file_path: str, path to the scaler `.pkl` file.
    :param data: array-like, data to be scaled.
    :return: array-like, scaled data.
    """

    scaler = joblib.load(file_path)
    scaled_data = scaler.transform(data)
    return scaled_data

def un_scale(file_path,data):
    """
    loads a given scaler and unscales the data using it.
    
    :param file_path: str, path to the scaler `.pkl` file.
    :param data: array-like, data to be unscaled.
    :return: array-like, unscaled data.
    """
    
    scaler = joblib.load(file_path)
    unscaled_data = scaler.inverse_transform(data)
    return unscaled_data

def apply_log1p(data,file_path):

    loaded_file = np.load(file_path,allow_pickle=True)
    columns_to_log = data.columns[loaded_file]

    for col in columns_to_log:
        if (data[col] < 0).any():
            raise ValueError(f"Column {col} contains negative values — log1p not safe.")
        data[col] = np.log1p(data[col])

    return data 

def apply_expm1(result):
    return np.expm1(result)   

def prepare_input(data_dict):
    """
    Reorders incoming data_dict according to training feature order.
    """
    reordered = {feature: data_dict[feature] for feature in config.FEATURE_ORDER}
    return reordered