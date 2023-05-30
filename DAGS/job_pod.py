


from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner' : 'angel',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='dag_cluster_gcp_v5',
    default_args = default_args,
    description='this is my first dag',
    start_date=datetime(2023,5,30),
    schedule_interval='@daily'
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command= "sudo apt-get update"
    )

    task2 = BashOperator(
        task_id = 'second_task',
        bash_command= "sudo apt-get install -y wget file"
    )

    task3 = BashOperator(
        task_id = 'third_task',
        bash_command= "wget -q -O 21million.rdf.gz  'https://github.com/dgraph-io/benchmarks/raw/release/v1.0/data/release/21million.rdf.gz'"
    )

    task4 = BashOperator(
        task_id = 'four_task',
        bash_command= "wget -q -O facets.rdf.gz -q  'https://github.com/dgraph-io/benchmarks/raw/release/v1.0/data/release/facets.rdf.gz'"
    )

    task5 = BashOperator(
        task_id = 'five_task',
        bash_command= "wget -q -O sf-tourism.rdf.gz 'https://github.com/dgraph-io/benchmarks/raw/release/v1.0/data/release/sf-tourism.rdf.gz'"
    )

    

    task1>>task2>>task3>>task4>>task5
    




            
            
            
            