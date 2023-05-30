from airflow import DAG
from airflow.providers.google.cloud.operators.kubernetes_engine import GKEStartPodOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 29),
}

svc_acc_key = '{ "type": "service_account", "project_id": "tf-my-gcp", "private_key_id": "630622c993988d8aef3ece9769d5f43de2956795", "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCscwiScX4Z5Dfm\n9jmX0ht0E6nC9mcX0F6psabZPSDdljBmDe2q20C5iLxySKx0SdGP50TM4HJ2qX9f\n5R4PuZ/icp1Tfftu4RFTHwYhq/keSGQVPVnIFgjEFTSfMOH7M5vWwbKqOsQH7cuC\nfYbU3Q0vOWeKk7aOkDZZ4TDZWg5Wr9MtJ8wV15kriU4zqcy3kk8OB68Y2jHQ+9Zg\nQzjePD6V2EYpXaVhGuj30DnfkVdDvxVw0v370vNooinBaJSKP6j3Dc8lxVo0N/Sr\nDuxOjns6wMP7F6NUSj5zBLT1TgI0Bwu7WsqLOCXx+kYVq9zgvgQkCDWZfivDisIs\n/avipl+zAgMBAAECggEAISr64he8FkTDz8NZ7m5140yI4Tu9NmJYYrENk0jjklr5\nshdJuAv1lfnLrPt3V+J+0Pu9St58hYAyRIJv1rxwGQDMa6uWeYwGZgNYjY9jGcT4\novEq3IYIZ5ZgiaHARS128sZMk9s7qv68nrt//F8L0yJqXMfuW9s26PCcEaH1kgxs\nQ5J6J8pQrJp8WWLX7rvdCDyFlGT66YxNkBpu3MjdBDFl+1VCsJiW/B+/IQmC9zVi\nP0ogaUWUZa+ufPczKKDUNo5QGHcsXvIWx+YleGzUUnqvm6l4r7oUKFslqjGPoMGa\nmnYNnoEHxuLYUG+eIsoulksjvOqLFV1ZLVT91RhewQKBgQDgk0KzEGzzc7z1S3Lh\ne86/f3o0hwlRjblUl2jhcUntyI8zn4oix1/ojtwMQyI5DjHHbcqiSr4S3nVhKj/m\nOu4b3eAoQIcQxyRx03S/4NKH4cDZMMD/RiNfaXqVdMziW4+F62W9XhYxrWAe9uHS\n11GL0TYpN9ElpIQOvA3x/KXj4QKBgQDElISnZ6n2bd5nP4VOg68DLR4BFJjbQYJB\nhHNvOUj1pvQDWjdPYhO4uT4Jz1tlw8/uPUW9P/+94vIbLPemx06HPc5JO6eDXctR\nFZu62MycAs5xEa8KY+xXhiwR3hCx9xvrhT70q/4FaSqw1SYR3jLnz/4uGBGi/i1W\ntwVPzOU2EwKBgBYZR5n5Rs9aF0EIEKDxnvGnKK5cj2UwDgmt8Ismq8CzWKwayewM\nNHrc+/hU7twwcmOOgT8hHb0bmO9byffs2ptxZOpxFxlmj0aIKVfsVqs6YtC8hHFa\nRIbSCVcFrFel7OSful49EPAIgInrf2NQ/txEVREPRgxvOPN+O90RIH3hAoGAS6aw\nSlBdm0V68pcCcU3CG2HQiy/nB3H1c8tKNUKBbnAatfORF46x8kPvuQzAqrAppBCW\ndxdbDzN4Yrbyc49+DBPgAFThyW9eIE1FiimGzH9T/TWF/GSp/qDW8uVX3XUwnHnB\n2Z0a+/AWCslshjHRu15S/mAq4WQaBKYYeDZs+1sCgYEAxZ4hAPm+ZN5Hh4LsW1kP\n448JEqoivBh4Xeaha8Q1Rw5AfIHkZOwgtYaO2Y2dxKr1Q7G1OV5POOTSC/m0VrI4\nxAKBXFpG4rjiKUPtCjN47uX7802A9RDjAf/wHExDQoLM46zU1P7n8EJO2joyMZMZ\norJnRKLOYiSaQzO0Xa1AmX4=\n-----END PRIVATE KEY-----\n", "client_email": "tf-my-gcp-sa@tf-my-gcp.iam.gserviceaccount.com",  "client_id": "100333622286468662887",  "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token",  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/tf-my-gcp-sa%40tf-my-gcp.iam.gserviceaccount.com",  "universe_domain": "googleapis.com"}'

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
    service_account_key=svc_acc_key,
    get_logs=True,
    dag=dag
)

run_kubectl_task
