import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, request, jsonify, render_template
from utils import utils
from config import config
from data_transformation import data_transformation
from models import model

# --- Flask App Setup ---
app = Flask(__name__, template_folder="templates")


# -------------------- UI ROUTES -------------------- #
@app.route('/')
def home():
    """Render main form for car price prediction."""
    return render_template('form.html')

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
        return jsonify({'error': str(e)}), 500

# -------------------- Main -------------------- #
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
