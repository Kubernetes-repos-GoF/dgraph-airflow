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
    url ="http://34.170.231.213:8080/mutate?commitNow=true"
    headers={
        'Accept':'*/*',
        'Content-Encoding':'gzip',
        'Content-Type':'application/rdf',
        'Accept-Encoding':'gzip, deflate'
    }

    readFileName = os.path.join(conf.get('core', 'DAGS_FOLDER'), 'accountRelations_1c.rdf.gz')
    ti.xcom_push(key='name', value=readFileName)
    fp = open(readFileName)
    for i, line in enumerate(fp):
        if i == 3:
            user_i = str.strip(line)
            ti.xcom_push(key='line', value=user_i)
            break
    fp.close()

    with open(readFileName, 'rb') as dataRaw:
        resp = requests.post(url,headers=headers, data=dataRaw)
    

def log_print_py(ti):
    name = ti.xcom_pull(task_ids = 'load_rdf_file_1_c', key='name')
    print(f'hello world {name}')

with DAG(
    dag_id= 'dgraph_load_rdf_file_line',
    default_args=default_args,
    description='dgraph load data',
    start_date=datetime(2023,6,15),
    schedule_interval='@daily'
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