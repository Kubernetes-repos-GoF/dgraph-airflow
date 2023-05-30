

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner' : 'angel',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='dgraph_testing_connection',
    default_args = default_args,
    description='this is my first dag',
    start_date=datetime(2023,5,12,2),
    schedule_interval='@daily'
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command= "gcloud container clusters get-credentials cluster-dgraph-air --zone us-west1-c --project tf-my-gcp"
    )

    task2 = BashOperator(
        task_id = 'second_task',
        bash_command= "kubectl get pod -n airflow "
        
    )

    task1.set_downstream(task2)
  