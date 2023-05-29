

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner' : 'angel',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='dgraph_insert_v4',
    default_args = default_args,
    description='this is my first dag',
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
        # bash_command = "curl -H 'Content-Type:application/json' http://44.211.75.97:8000/admin/schema -X POST -d \
        #     $' type City{ id:ID! , lat:Float! , lgn: Float! }'"
        bash_command = "curl 'localhost:8080/alter' --silent --request POST \
  --data $' name: string @index(term) . release_date: datetime @index(year) . revenue: float . running_time: int . starring: [uid] . director: [uid] . \
type Person { \
  name\
} \
type Film { \
  name \
  release_date \
  revenue  \
  running_time \
  starring  \
  director  \
}' | python -m json.tool "
    )

    task1.set_downstream(task2)
    task1.set_downstream(task3)