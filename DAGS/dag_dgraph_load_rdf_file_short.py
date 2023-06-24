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

def load_rdf(ti, **kwargs):
    global url, headers
    fileId = "1_"+str(kwargs['fileid'])

    fileName = "accountRelations_"+fileId+".rdf.gz"
    ti.xcom_push(key='name', value=fileName)

    dataFileName = os.path.join(conf.get('core', 'DAGS_FOLDER'), 'data/accountRelations_'+fileId+'.rdf.gz')
    with open(dataFileName, 'rb') as dataRaw:
        resp = requests.post(url,headers=headers, data=dataRaw)
        ti.xcom_push(key='status', value=str(resp.status_code))
        
with DAG(
    dag_id= 'dgraph_load_rdf',
    default_args=default_args,
    description='dgraph load data',
    start_date=datetime(2023,6,23),
    schedule_interval=None
) as dag:
    task1 = PythonOperator(
        task_id='load_rdf_a',
        provide_context=True,
        python_callable=load_rdf,
        op_kwargs={'fileid': '1'}
    )

    task2 = PythonOperator(
        task_id='load_rdf_b',
        provide_context=True,
        python_callable=load_rdf,
        op_kwargs={'fileid': '2'}
    )
