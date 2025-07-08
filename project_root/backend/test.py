import json
import streamlit as st
import os

path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","encodings", f'manufacturer_encoding_dict.json'))
# Open and load a JSON file
with open(path, "r") as f:
    data = json.load(f)

# Display the loaded data
st.write(data)