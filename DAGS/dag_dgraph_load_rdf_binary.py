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
    url ="http://34.170.231.213:8080/mutate?commitNow=true"
    headers={
        'Accept':'*/*',
        'Content-Encoding':'gzip',
        'Content-Type':'application/rdf',
        'Accept-Encoding':'gzip, deflate'
    }

    dataFileName = os.path.join(conf.get('core', 'DAGS_FOLDER'), 'data/accountRelations_1_1.rdf.gz')
    ti.xcom_push(key='stepName', value=dataFileName)

    with open(dataFileName, 'rb') as dataRaw:
        ti.xcom_push(key='stepRead', value="OK")
        resp = requests.post(url,headers=headers, data=dataRaw)
        ti.xcom_push(key='stepStatusCode', value=str(resp.status_code))
    ti.xcom_push(key='stepEnd', value="OK")

def log_print_py(ti):
    name = ti.xcom_pull(task_ids = 'load_rdf_file_1_c', key='stepName')
    print(f'File rdf: {name}')

with DAG(
    dag_id= 'dgraph_load_rdf_binary',
    default_args=default_args,
    description='dgraph load binary data',
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