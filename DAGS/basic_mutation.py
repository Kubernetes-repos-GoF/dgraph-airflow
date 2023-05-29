from airflow import DAG
from airflow.operators.python_operator import PythonOperator 
from datetime import datetime
from pydgraph import DgraphClient, DgraphClientStub

# Dgraph connection details
dgraph_host = 'http://44.211.75.97/'
dgraph_port = '8000'
# dgraph_username = '<DGRAPH_USERNAME>'
# dgraph_password = '<DGRAPH_PASSWORD>'

# DAG configuration
dag = DAG(
    'dgraph_insertion',
    start_date=datetime(2023, 5, 26),
    schedule_interval='@daily',
)

# Function to perform data insertion
def insert_data_to_dgraph():
    # Create a Dgraph client
    client_stub = DgraphClientStub(f'{dgraph_host}:{dgraph_port}')
    client = DgraphClient(client_stub)

    # Define your data to be inserted
    data = {
        'person': [
            {
                'name': 'John',
                'age': 30,
            },
            {
                'name': 'Jane',
                'age': 28,
            },
        ],
    }

    # Perform the data insertion
    txn = client.txn()
    try:
        response = txn.mutate(set_obj=data)
        txn.commit()
        print('Data inserted successfully:', response)
    finally:
        txn.discard()
        client_stub.close()

# Define the Airflow task
insert_data_task = PythonOperator(
    task_id='insert_data_to_dgraph',
    python_callable=insert_data_to_dgraph,
    dag=dag,
)

# Set the task dependency
insert_data_task
