import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,                  
    "retry_delay": timedelta(minutes=3),
    "execution_timeout": timedelta(minutes=15),  
    "start_date": datetime(2025, 6, 17),
    "on_failure_callback": notify_failure, 
}

with DAG(
    dag_id="breast_cancer_etl_pipeline",
    default_args=default_args,
    description="ETL pipeline for breast cancer diagnosis model",
    schedule_interval=None,
    catchup=False,
    tags=["breast_cancer"]
) as dag:

    load_data = BashOperator(
        task_id="load_data",
        bash_command=(f'PYTHONPATH={BASE_DIR} python -m etl.download'),
    )

    preprocess_data = BashOperator(
        task_id="preprocess_data",
        bash_command=(f'PYTHONPATH={BASE_DIR} python -m etl.preprocess'),
    )

    train_model = BashOperator(
        task_id="train_model",
        bash_command=(f'PYTHONPATH={BASE_DIR} python -m etl.train'),
    )

    evaluate_model = BashOperator(
        task_id="evaluate_model",
        bash_command=(f'PYTHONPATH={BASE_DIR} python -m etl.evaluate'),
    )


    load_data >> preprocess_data >> train_model >> evaluate_model
