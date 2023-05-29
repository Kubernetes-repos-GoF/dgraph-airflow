
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from pydgraph import DgraphClient, DgraphClientStub


def insert_data_to_dgraph():
    # Connect to Dgraph
    stub = DgraphClientStub('localhost:9080')  # Replace with your Dgraph connection details
    client = DgraphClient(stub)

    # Define your data to be inserted
    data = [
        {
            'uid': '_:alice',
            'name': 'Alice',
            'age': 30,
        },
        {
            'uid': '_:bob',
            'name': 'Bob',
            'age': 35,
        },
        # Add more data objects as needed
    ]

    # Perform mutation to insert data
    txn = client.txn()
    try:
        mutation = txn.create_mutation(set_obj=data)
        response = txn.mutate(mutation)
        txn.commit()

        print("Data inserted successfully:", response)

    finally:
        txn.discard()
        stub.close()


# Define the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 26),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'insert_data_to_dgraph',
    default_args=default_args,
    description='DAG to insert data into Dgraph',
    schedule_interval=None,
)

# Define the task
insert_task = PythonOperator(
    task_id='insert_data_task',
    python_callable=insert_data_to_dgraph,
    dag=dag,
)

# Set the task dependencies
insert_task



# In this script:

# 1. The `insert_data_to_dgraph()` function connects to Dgraph using the Dgraph Python client. Replace `'localhost:9080'` with your actual Dgraph connection details.

# 2. Inside the function, a list of data objects is defined. Each object represents a data entry to be inserted into Dgraph.

# 3. The `insert_data_to_dgraph()` function performs a mutation using the `create_mutation()` and `mutate()` methods of the Dgraph Python client to insert the data into Dgraph.

# 4. The `insert_data_task` is defined as a `PythonOperator` task in the Airflow DAG. It calls the `insert_data_to_dgraph()` function when executed.

# 5. The Airflow DAG is created with the `DAG` class, specifying the DAG's name, description, start date, and other parameters.

# 6. The task dependencies are set by using the `set_downstream()` method on the tasks.

# Remember to update the Dgraph connection details and customize the data to be inserted according to your requirements.