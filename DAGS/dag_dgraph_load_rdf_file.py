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

url ="http://34.170.231.213:8080/mutate?commitNow=true"
headers={
    'Accept':'*/*',
    'Content-Encoding':'gzip',
    'Content-Type':'application/rdf',
    'Accept-Encoding':'gzip, deflate'
}

def load_rdf_file_a(ti):
    global url, headers
    fileId = "1_1"

    fileName = "accountRelations_"+fileId+".rdf.gz"
    ti.xcom_push(key='name', value=fileName)

    dataFileName = os.path.join(conf.get('core', 'DAGS_FOLDER'), 'data/accountRelations_'+fileId+'.rdf.gz')
    with open(dataFileName, 'rb') as dataRaw:
        resp = requests.post(url,headers=headers, data=dataRaw)
        ti.xcom_push(key='status', value=str(resp.status_code))
    
def load_rdf_file_b(ti):
    global url, headers
    fileId = "1_2"

    fileName = "accountRelations_"+fileId+".rdf.gz"
    ti.xcom_push(key='name', value=fileName)

    dataFileName = os.path.join(conf.get('core', 'DAGS_FOLDER'), 'data/accountRelations_'+fileId+'.rdf.gz')
    with open(dataFileName, 'rb') as dataRaw:
        resp = requests.post(url,headers=headers, data=dataRaw)
        ti.xcom_push(key='status', value=str(resp.status_code))
        
def load_rdf_file_c(ti):
    global url, headers
    fileId = "1_3"

    fileName = "accountRelations_"+fileId+".rdf.gz"
    ti.xcom_push(key='name', value=fileName)

    dataFileName = os.path.join(conf.get('core', 'DAGS_FOLDER'), 'data/accountRelations_'+fileId+'.rdf.gz')
    with open(dataFileName, 'rb') as dataRaw:
        resp = requests.post(url,headers=headers, data=dataRaw)
        ti.xcom_push(key='status', value=str(resp.status_code))
        
def load_rdf_file_d(ti):
    global url, headers
    fileId = "1_4"

    fileName = "accountRelations_"+fileId+".rdf.gz"
    ti.xcom_push(key='name', value=fileName)

    dataFileName = os.path.join(conf.get('core', 'DAGS_FOLDER'), 'data/accountRelations_'+fileId+'.rdf.gz')
    with open(dataFileName, 'rb') as dataRaw:
        resp = requests.post(url,headers=headers, data=dataRaw)
        ti.xcom_push(key='status', value=str(resp.status_code))
        
def load_rdf_file_e(ti):
    global url, headers
    fileId = "1_5"

    fileName = "accountRelations_"+fileId+".rdf.gz"
    ti.xcom_push(key='name', value=fileName)

    dataFileName = os.path.join(conf.get('core', 'DAGS_FOLDER'), 'data/accountRelations_'+fileId+'.rdf.gz')
    with open(dataFileName, 'rb') as dataRaw:
        resp = requests.post(url,headers=headers, data=dataRaw)
        ti.xcom_push(key='status', value=str(resp.status_code))
        
def log_print_py(ti):
    name = ti.xcom_pull(task_ids = 'load_rdf_gz_a', key='name')
    ti.xcom_push(key='status', value=name)
    print(f'hello world {name}')

with DAG(
    dag_id= 'dgraph_load_rdf_file_five',
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
        python_callable=load_rdf_file_b
    )

    task3 = PythonOperator(
        task_id='load_rdf_gz_c',
        python_callable=load_rdf_file_c
    )

    task4 = PythonOperator(
        task_id='load_rdf_gz_d',
        python_callable=load_rdf_file_d
    )

    task5 = PythonOperator(
        task_id='load_rdf_gz_e',
        python_callable=load_rdf_file_e
    )

    task6 = PythonOperator(
        task_id='print_log',
        python_callable=log_print_py
    )

    task1 >> task6