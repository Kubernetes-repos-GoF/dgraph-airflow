from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.configuration import conf

from datetime import timedelta, datetime
import requests
import os

default_args = {
    'owner': 'mycelium',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def load_rdf_file_a(ti):
    ti.xcom_push(key='name', value='Mycelium')
    url ="http://34.170.231.213:8080/mutate?commitNow=true"
    headers={
        'Accept':'*/*',
        'Content-Encoding':'gzip',
        'Content-Type':'application/rdf',
        'Accept-Encoding':'gzip, deflate'
    }

    dataFileName = os.path.join(conf.get('core', 'DAGS_FOLDER'), 'data/accountRelations_1_1.rdf.gz')
    with open(dataFileName, 'rb') as dataRaw:
        resp = requests.post(url,headers=headers, data=dataRaw)
    
def load_rdf_file_b(ti):
    ti.xcom_push(key='name', value='Mycelium')
    url ="http://34.170.231.213:8080/mutate?commitNow=true"
    headers={
        'Accept':'*/*',
        'Content-Encoding':'gzip',
        'Content-Type':'application/rdf',
        'Accept-Encoding':'gzip, deflate'
    }

    dataFileName = os.path.join(conf.get('core', 'DAGS_FOLDER'), 'data/accountRelations_1_2.rdf.gz')
    with open(dataFileName, 'rb') as dataRaw:
        resp = requests.post(url,headers=headers, data=dataRaw)

def log_print_py(ti):
    name = ti.xcom_pull(task_ids = 'load_rdf_gz_a', key='name')
    print(f'hello world {name}')

with DAG(
    dag_id= 'dgraph_load_rdf_file_r',
    default_args=default_args,
    description='dgraph load data',
    start_date=datetime(2023,6,15),
    schedule_interval=None
) as dag:
    task1 = PythonOperator(
        task_id='load_rdf_gz_a',
        python_callable=load_rdf_file_a
    )

    task2 = PythonOperator(
        task_id='load_rdf_gz_b',
        python_callable=load_rdf_file_a
    )

    task3 = PythonOperator(
        task_id='print_log',
        python_callable=log_print_py
    )

    task1 >> task2 >> task3