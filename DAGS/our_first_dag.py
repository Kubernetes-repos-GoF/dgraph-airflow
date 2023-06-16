

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner' : 'mycelium',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='first_dag',
    default_args = default_args,
    description='this is my first dag',
    start_date=datetime(2023,5,12,2),
    schedule_interval='@daily'
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command= "echo hello mycelium, this is task 1"
    )

    task2 = BashOperator(
        task_id = 'second_task',
        bash_command= "echo second task completed"
    )

    task3 = BashOperator(
        task_id = 'third_task',
        bash_command = "echo third task running good"
    )

    task1.set_downstream(task2)
    task1.set_downstream(task3)