import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_PATH = os.path.join(BASE_DIR, 'logs')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_PATH, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

CONFIG = {
    "loaded_data_path": os.path.join(DATA_DIR, "loaded_data.csv"),
    "preprocessed_data_path": os.path.join(DATA_DIR, "preprocessed_data.csv"),
    "model_path": os.path.join(RESULTS_DIR, "model.pkl"),
    "metrics_path": os.path.join(RESULTS_DIR, "metrics.json"),
    "target_column": "diagnosis"
}
