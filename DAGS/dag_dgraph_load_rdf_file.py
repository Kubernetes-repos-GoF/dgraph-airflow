from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator
import requests

default_args = {
    'owner': 'mycelium',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def load_rdf_file(ti):
    ti.xcom_push(key='name', value='Mycelium')
    url ="http://34.170.231.213:8080/mutate?commitNow=true"
    headers={
        'Accept':'*/*',
        'Content-Type':'application/rdf',
        'Accept-Encoding':'gzip, deflate'
    }
    with open('./accountRelations_1_1.rdf.gz', 'rb') as dataRaw:
        resp = requests.post(url,headers=headers, data=dataRaw)
    

def log_print_py(ti):
    name = ti.xcom_pull(task_ids = 'load_rdf_file_1_c', key='name')
    print(f'hello world {name}')

with DAG(
    dag_id= 'dgraph_load_rdf_file_b',
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