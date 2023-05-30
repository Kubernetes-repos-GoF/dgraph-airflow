from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 29),
}

dag = DAG('kubectl_example', default_args=default_args, schedule_interval=None)

command = " kubectl get pods "

run_kubectl_task = KubernetesPodOperator(
    task_id='run_kubectl',
    name='run-kubectl-task',
    namespace='new_pod_task',
    image='google/cloud-sdk:latest',
    cmds=['sh', '-c'],
    arguments=[command],
    dag=dag
)

run_kubectl_task
