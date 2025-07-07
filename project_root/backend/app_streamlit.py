import streamlit as st
import os
import json
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import utils
from config import config
from data_transformation import data_transformation
from models import model

# ---- Set page config ---- #
st.set_page_config(page_title="Car Price Predictor", layout="centered")

st.title("🚗 Car Price Prediction App")
st.markdown("Fill in the details below to estimate your car's price.")

# ---- Load encoding options ---- #
@st.cache_data
def load_options(feature):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'encodings', f'{feature}_encoding_dict.json'))
    with open(path, 'r') as f:
        return json.load(f)

# ---- Form UI ---- #
input_data = {}
with st.form("prediction_form"):
    for feature in config.FEATURE_ORDER:
        if feature == 'model':
            all_models = load_options("model").keys()
            input_data[feature] = st.text_input("Model", "")
        elif feature in ['year', 'odometer', 'cylinders']:
            input_data[feature] = st.number_input(f"{feature.capitalize()}", min_value=0)
        else:
            options = load_options(feature)
            input_data[feature] = st.selectbox(feature.capitalize(), options.keys())

    submitted = st.form_submit_button("Predict")

# ---- Prediction ---- #
if submitted:
    try:
        prepared_input = utils.prepare_input(input_data)
        X = data_transformation.process_input(prepared_input)
        prediction = model.predict(X, config.MODEL)
        st.success(f"💰 Estimated Car Price: ${float(prediction[0]):,.2f}")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
