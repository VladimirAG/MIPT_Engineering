import pandas as pd
import argparse
import os
import sys
from sklearn.preprocessing import StandardScaler
from etl.config import CONFIG, LOGS_PATH
from etl.logger import set_logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if not os.path.exists(LOGS_PATH):
    os.makedirs(LOGS_PATH, exist_ok=True)

log_file = os.path.join(LOGS_PATH, "preprocess_data.log")

logger = set_logger(
    name="preprocess_data_logger",
    log_file=log_file, 
    level=logging.INFO
)

def preprocess_data(input_path, output_path):
    try:
        if not os.path.exists(input_path):
            logger.error(f"Файл с данными не найден: {input_path}")
            sys.exit(1)
            
        df = pd.read_csv(input_path)
        
        X = df.drop(columns=[CONFIG["target_column"]])
        y = df[columns=[CONFIG["target_column"]]]
        
        # Масштабирование признаков
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        df_scaled = pd.DataFrame(X_scaled, columns=X.columns)
        df_scaled[CONFIG["target_column"]] = y.values
        df_scaled.to_csv(output_path, index=False)
        logger.info(f"Данные успешно сохранены в {output_path}")

    except Exception as e:
        logger.exception(f"Произошла ошибка при обработке данных: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обработка датасета")
    parser.add_argument("--input-path", type=str, default=CONFIG["loaded_data_path"])
    parser.add_argument("--output-path", type=str, default=CONFIG["preprocessed_data_path"])
    args = parser.parse_args()

    preprocess_data(args.input_path, args.output_path)
