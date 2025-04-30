import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
logging.basicConfig(level=logging.DEBUG)

from flask import Flask, request, jsonify, render_template
from utils import utils
from config import config
from data_transformation import data_transformation
from models import model
import json

# --- Flask App Setup ---
app = Flask(__name__, template_folder="templates")


# -------------------- UI ROUTES -------------------- #
@app.route('/')
def home():
    """Render main form for car price prediction."""
    return render_template('form.html', fields=config.FEATURE_ORDER)

@app.route('/get-options/<feature>')
def get_options(feature):
    try:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'encodings', f'{feature}_encoding_dict.json'))
        print(f"Looking for encoding file: {path}")
        with open(path, 'r') as f:
            options = json.load(f)
        return jsonify(list(options.keys()))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/autocomplete/model')
def autocomplete_model():
    try:
        term = request.args.get('q', '').lower()
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'encodings', 'model_encoding_dict.json'))
        with open(path, 'r') as f:
            model_dict = json.load(f)
        suggestions = [k for k in model_dict.keys() if term in k.lower()]
        return jsonify(suggestions[:20])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predict', methods=['POST'])
def predict():
    """Process user input and return predicted car price."""
    try:
        input_data = request.get_json() if request.is_json else request.form.to_dict()
        input_data = utils.prepare_input(input_data)
        X = data_transformation.process_input(input_data)
        prediction = model.predict(X, config.MODEL)
        return render_template('result.html', price=float(prediction[0]))
    except Exception as e:
        return render_template('error.html', error=str(e)), 500


# -------------------- Main -------------------- #
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
