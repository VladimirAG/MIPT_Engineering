import os
import sys
import pandas as pd
import argparse
from sklearn.datasets import load_breast_cancer
from etl.config import CONFIG, LOGS_PATH
from etl.logger import set_logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
    
if not os.path.exists(LOGS_PATH):
    os.makedirs(LOGS_PATH, exist_ok=True)

log_file = os.path.join(LOGS_PATH, "load_data.log")

logger = set_logger(
    name="load__data_logger",
    log_file=log_file, 
    level=logging.INFO
)

def load_data(save_path):
    try:
        data = load_breast_cancer()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df[CONFIG["target_column"]] = data.target
        df.to_csv(save_path, index=False)
        logger.info(f"Датасет успешно сохранен в {save_path}.")
    except Exception as e:
        logger.exception(f"Не удалось загрузить датасет: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", 
        type=str, 
        required=True,
        default=CONFIG["loaded_data_path"],
        help="Путь к исходному датасету"
    )
    args = parser.parse_args()

    load_data(args.output_path)
