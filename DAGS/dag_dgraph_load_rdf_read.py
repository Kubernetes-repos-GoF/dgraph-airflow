from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.configuration import conf

from datetime import timedelta, datetime
import requests
import os

default_args = {
    'owner': 'mycelium',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

conf.get('core', 'DAGS_FOLDER')

def load_rdf_file(ti):
    ti.xcom_push(key='stepIni', value="OK")
    dataFileName = os.path.join(conf.get('core', 'DAGS_FOLDER'), 'data/accountRelations_1.rdf')

    minBound = 10
    maxBound = 51

    fp = open(dataFileName)
    queryUser = "g.V("
    for i, line in enumerate(fp):
        if i == 10:
            ti.xcom_push(key='stepLine', value=str.strip(line))
        
        if i >= minBound and i < maxBound:
            user_i = str.strip(line)
            queryUser += f"'user-{user_i}',"
        elif i > maxBound:
            break
    fp.close()
    ti.xcom_push(key='stepFin', value="OK")

def log_print_py(ti):
    name = ti.xcom_pull(task_ids = 'load_rdf_file_1_c', key='stepName')
    print(f'File rdf: {name}')

with DAG(
    dag_id= 'dgraph_load_rdf_read',
    default_args=default_args,
    description='dgraph load read rdf data',
    start_date=datetime(2023,6,16),
    schedule_interval=None
) as dag:
    task1 = PythonOperator(
        task_id='print_log',
        python_callable=log_print_py
    )

    task2 = PythonOperator(
        task_id='load_rdf_file_1_c',
        python_callable=load_rdf_file
    )

    task2 >> task1