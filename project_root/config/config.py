import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # This points to project_root/config

CATEGORICAL_COLUMNS = ['manufacturer', 'model', 'condition', 'cylinders', 'fuel', 
                       'transmission', 'drive', 'size', 'type', 'paint_color']

NUMERICAL_COLUMNS = ['year', 'odometer']

ENCODING_PATHS = {col: f'encodings/{col}_encoding_dict.json' for col in CATEGORICAL_COLUMNS}

NOMINAL_COLUMNS = ["manufacturer","model","fuel","type","paint_color"]

ORDINAL_COLUMNS = ["condition","cylinders","transmission","drive","size"]

TARGET_COLUMN = "Price"

Q_MATRIX = os.path.join(BASE_DIR, "../encodings/Q_matrix.npy")
Q_MATRIX = os.path.abspath(Q_MATRIX)

X_SCALER = os.path.join(BASE_DIR, "../encodings/X_scaler.pkl")
X_SCALER = os.path.abspath(X_SCALER)

Y_SCALER = os.path.join(BASE_DIR, "../encodings/y_scaler.pkl")
Y_SCALER = os.path.abspath(Y_SCALER)

RELEVENT_COLUMNS_IDX = os.path.join(BASE_DIR, "../encodings/relevant_columns_idx.npy")
RELEVENT_COLUMNS_IDX = os.path.abspath(RELEVENT_COLUMNS_IDX)  # Converts it to absolute path

SKEW_VALUES_INDICES = os.path.join(BASE_DIR, "../encodings/to_remove_skew_values_indices.npy")
SKEW_VALUES_INDICES = os.path.abspath(SKEW_VALUES_INDICES)  # Converts it to absolute path

MODEL = os.path.join(BASE_DIR, "../encodings/random_forest_model.pkl")
MODEL = os.path.abspath(MODEL)

FEATURE_ORDER = [
    "year",
    "manufacturer",
    "model",
    "condition",
    "cylinders",
    "fuel",
    "odometer",
    "transmission",
    "drive",
    "size",
    "type",
    "paint_color"
    # ... (add all your features here, exactly as you trained)
]
