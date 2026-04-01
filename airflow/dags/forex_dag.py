import sys
sys.path.insert(0, "/opt/airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


def ingest_rates():
    from ingestion.fetch_rates import fetch_kes_rates
    from ingestion.validate import validate_rates
    from ingestion.load_duckdb import init_db, insert_rates

    rates = fetch_kes_rates()

    if not validate_rates(rates):
        raise ValueError("Great Expectations validation failed — rates not written to DuckDB.")

    init_db()
    insert_rates(rates)


with DAG(
    dag_id="forex_ingestion",
    default_args=default_args,
    description="Hourly KES exchange rate ingestion from open.er-api.com into DuckDB",
    schedule_interval="@hourly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["forex", "kenya", "duckdb"],
) as dag:

    ingest_task = PythonOperator(
        task_id="ingest_rates",
        python_callable=ingest_rates,
    )
