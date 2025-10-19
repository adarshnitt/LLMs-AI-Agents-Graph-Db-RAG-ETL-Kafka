# task group

#python dag.py
from libraries import *


def_args={
    "owner": "airflow",
    "start_date": datetime(2025, 10, 9),
}


with DAG(
    dag_id="subtask2_id",
    default_args=def_args,
    catchup=False,
    dagrun_timeout=timedelta(minutes=10),
    tags=["example"]) as dag:
  
  with DAG(dag_id="subtask2a_id",) as dag:
    start=DummyOperator(task_id="start")
    mid=DummyOperator(task_id="mid")
    end=DummyOperator(task_id="end")
    with TaskGroup("a-z", tooltip="task group from ato z") as tg1:
      c=DummyOperator(task_id="c")
      e=DummyOperator(task_id="e")
      
  
        
        
      
      start>>tg1>>mid>>end
