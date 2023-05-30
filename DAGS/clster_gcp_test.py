

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner' : 'angel',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='query_simpson',
    default_args = default_args,
    description='dag_cluster_gcp',
    start_date=datetime(2023,5,12,2),
    schedule_interval='@daily'
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command= "echo hello Angel, this is task 1"
    )

    task2 = BashOperator(
        task_id = 'second_task',
        bash_command= "echo second task completed"
    )

    task3 = BashOperator(
        task_id = 'third_task',
        
        bash_command = "curl -H 'Content-Type: application/dql' -X POST http://34.73.100.176:8080/query -d $' { movie(func:eq(name, 'Homer')) {name  ,parent_to{ name }  } } '"
    )

    task1.set_downstream(task2)
    task1.set_downstream(task3)

    