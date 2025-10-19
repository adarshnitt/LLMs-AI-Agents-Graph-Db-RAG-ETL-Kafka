#python dag.py
from airflow import DAG
from airflow.operators.empty import EmptyOperator as DummyOperator
from airflow.operators.python import PythonOperator    
from datetime import datetime, timedelta    



def_args={
    "owner": "airflow",
    "start_date": datetime(2025, 10, 9),
}

def extract_function(**kwargs):
import logging
    logging.info("extracting")
    print("extracting")
    return "extracted"

def transform_function(**kwargs):
    print("transformed_value")
    return "transformed_value"

def load_function(**kwargs):
    print("loaded_value")
    return "loaded_value"



with DAG(dag_id="apython_dag_id",default_args=def_args,catchup=False,dagrun_timeout=timedelta(minutes=10),tags=["example"]) as dag:
    print("basic dag testing")
    start = DummyOperator(task_id="start")
    extract= PythonOperator(task_id="extract",python_callable=extract_function,)
    
    transform= PythonOperator(task_id="transform_b",python_callable=transform_function, op_args=["transform"])
    load= PythonOperator(task_id="load",python_callable=load_function,op_kwargs={"li":"load"})
    end = DummyOperator(task_id="end")

    start >> extract >> transform >> load >> end