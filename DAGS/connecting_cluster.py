from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import GKEStartPodOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 29),
}

dag = DAG('gke_kubectl_example', default_args=default_args, schedule_interval=None)

command = """
    kubectl get pods
"""

run_kubectl_task = GKEStartPodOperator(
    task_id='run_kubectl',
    project_id='tf-my-gcp',
    location='us-west1-c',
    cluster_name='cluster-dgraph-air',
    name='run-kubectl-task',
    namespace='airflow',
    image='gcr.io/google-containers/kubectl',
    cmds=['sh', '-c'],
    arguments=[command],
    service_account_key='/home/angel/Descargas/tf-my-gcp-630622c99398.json',
    get_logs=True,
    dag=dag
)

run_kubectl_task
