# task group

#python dag.py
from libraries import *


def_args={
    "owner": "airflow",
    "start_date": datetime(2025, 10, 9),
}


with DAG(
    dag_id="subtask1_id",
    default_args=def_args,
    catchup=False,
    dagrun_timeout=timedelta(minutes=10),
    tags=["example"]) as dag:
  
  
  start=DummyOperator(task_id="start")
  mid=DummyOperator(task_id="mid")
  end=DummyOperator(task_id="end")
  with TaskGroup("a-z", tooltip="task group from ato z") as tg1:
    a=DummyOperator(task_id="a")
    b=DummyOperator(task_id="b")
    c=DummyOperator(task_id="c")
    d=DummyOperator(task_id="d")
    e=DummyOperator(task_id="e")
    a>>b
    c>>d
    

start>>tg1>>mid>>end
