# libraries.py

import kagglehub
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.functions import udf
from pyspark.sql.types import *

from pyspark.ml.feature import MinMaxScaler, VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.linalg import Vectors
from pyspark.ml.classification import *
from pyspark.ml.regression import *


from airflow import DAG
from airflow.operators.empty import EmptyOperator as DummyOperator
from airflow.operators.python import PythonOperator    
from airflow.utils.task_group import  TaskGroup
from datetime import datetime, timedelta 


def_args={
    "owner": "airflow",
    "start_date": datetime(2025, 10, 9),
}