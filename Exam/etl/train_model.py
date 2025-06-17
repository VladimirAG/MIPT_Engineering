import pandas as pd
import argparse
import joblib
import os
import sys
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from etl.config import CONFIG, LOGS_PATH
from etl.logger import set_logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if not os.path.exists(LOGS_PATH):
    os.makedirs(LOGS_PATH, exist_ok=True)

log_file = os.path.join(LOGS_PATH, "train_model.log")

logger = set_logger(
    name="train_model_logger",
    log_file=log_file,
    level=logging.INFO
)

def train_model(data_path, model_path):
    try:
        df = pd.read_csv(data_path)
        X = df.drop(columns=[CONFIG["target_column"]])
        y = df[CONFIG["target_column"]]
      
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
      
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        logger.info("Обучение модели завершено.")
        
        joblib.dump(model, model_path)
        logger.info(f"Модель сохранена в: {model_path}.")
        
    except Exception as e:
        logger.exception(f"Ошибка при обучении модели: {e}.")
        raise 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обучение модели логистической регрессии")
    parser.add_argument("--data-path", type=str, default=CONFIG["preprocessed_data_path"])
    parser.add_argument("--model-path", type=str, default=CONFIG["model_path"])
    args = parser.parse_args()

    train_model(args.data_path, args.model_path)
