from airflow import DAG
from airflow.operators.python_operator import PythonOperator 
from datetime import datetime
from pydgraph import DgraphClient, DgraphClientStub

# Dgraph connection details
dgraph_host = '<DGRAPH_HOST>'
dgraph_port = '<DGRAPH_PORT>'
dgraph_username = '<DGRAPH_USERNAME>'
dgraph_password = '<DGRAPH_PASSWORD>'

# DAG configuration
dag = DAG(
    'dgraph_insertion',
    start_date=datetime(2023, 1, 1),
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


# In this script:

# Replace <DGRAPH_HOST>, <DGRAPH_PORT>, <DGRAPH_USERNAME>, and <DGRAPH_PASSWORD> with the actual connection details for your Dgraph database.

# The DAG is scheduled to run daily (schedule_interval='@daily') starting from January 1, 2023 (start_date=datetime(2023, 1, 1)). Adjust these parameters according to your requirements.

# The insert_data_to_dgraph function establishes a connection to Dgraph, defines the data to be inserted, and performs the mutation using the Dgraph Python client.

# The PythonOperator is used to create a task named insert_data_to_dgraph that executes the insert_data_to_dgraph function.

# The task dependency is set by specifying insert_data_task as the last line.

# You can save this script as a Python file, such as dgraph_insertion_dag.py, and place it in the Airflow DAGs directory. Airflow will automatically detect and schedule the DAG according to the provided configuration.

