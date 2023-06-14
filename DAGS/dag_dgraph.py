from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'mycelium',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def get_name(ti):
    ti.xcom_push(key='name', value='Mycelium')
    

def greet(ti):
    name = ti.xcom_pull(task_ids = 'obtener_nombre', key='name')
    print(f'hello world {name}')

with DAG(
    dag_id= 'dgraph_data',
    default_args=default_args,
    description='first dag with dgraph',
    start_date=datetime(2023,6,13),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='saludo',
        python_callable=greet
    )

    task2 = PythonOperator(
        task_id='obtener_nombre',
        python_callable=get_name
    )

    task2 >> task1