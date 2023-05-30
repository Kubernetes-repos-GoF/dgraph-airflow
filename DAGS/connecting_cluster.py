from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from kubernetes import client, config

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 29),
}

dag = DAG('kubectl_example', default_args=default_args, schedule_interval=None)

def run_kubectl_command():
    # Load the Kubernetes configuration
    config.load_kube_config()

    # Create a Kubernetes API client
    api_client = client.ApiClient()

    # Create a Kubernetes core API object
    core_api = client.CoreV1Api(api_client)

    # Example: Get the list of pods in the cluster
    pods = core_api.list_namespaced_pod(namespace='default')

    # Print the pod names
    for pod in pods.items:
        print(pod.metadata.name)

run_kubectl_task = PythonOperator(
    task_id='run_kubectl',
    python_callable=run_kubectl_command,
    dag=dag
)

run_kubectl_task
