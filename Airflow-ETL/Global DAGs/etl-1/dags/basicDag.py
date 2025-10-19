# basic dag
from airflow import DAG
from airflow.operators.empty import EmptyOperator as DummyOperator
from datetime import datetime, timedelta    



def_args={
    "owner": "airflow",
    "start_date": datetime(2023, 1, 1),
}


with DAG(
    dag_id="basics_dag_id",
    default_args=def_args,
    catchup=False,
    dagrun_timeout=timedelta(minutes=10),
    tags=["example"]
) as dag:
    print("basic dag testing")
    start = DummyOperator(task_id="start")
    extract= DummyOperator(task_id="extract")
    transform= DummyOperator(task_id="transform_b")
    load= DummyOperator(task_id="load")
    end = DummyOperator(task_id="end")

    start >> extract >> transform >> load >> end