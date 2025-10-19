
#python dag.py
from airflow import DAG
from airflow.operators.empty import EmptyOperator as DummyOperator
from airflow.operators.python import PythonOperator    
from datetime import datetime, timedelta    
import pandas as pd


def_args={
    "owner": "airflow",
    "start_date": datetime(2025, 10, 9),
}




def extract():
  print("extract task")
  data=[{"a":1,"b":1},{"a":11,"b":11}]
  df=pd.DataFrame([{"a":1,"b":1},{"a":11,"b":11}])
  return df
def transform(arg1):
  print("transform task")
  return arg1
def load(arg2):
  print("load task")
  return "extract"


def etl():
  df=extract()
  df1=transform(df)
  load(df1)


with DAG(
    dag_id="atldag_id",
    default_args=def_args,
    catchup=False,
    dagrun_timeout=timedelta(minutes=10),
    tags=["example"]) as dag:
  start=DummyOperator(task_id="start")

  extract_task=PythonOperator(task_id="extract", python_callable=extract)
  transform_task=PythonOperator(task_id="transform", python_callable=transform,op_kwargs={"arg1":"agr1"})
  load_task=PythonOperator(task_id="load", python_callable=load, op_kwargs={"arg2":"agr2"})
  end=DummyOperator(task_id="end")

  start>>extract_task>>transform_task>>load_task>>end