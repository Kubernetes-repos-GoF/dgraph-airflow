from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.configuration import conf
from airflow.models import Variable

from datetime import timedelta, datetime
import requests
import os

default_args = {
    'owner': 'mycelium',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


dgraph_endpoint = Variable.get("dgraph_endpoint")
url = f"http://{dgraph_endpoint}/mutate?commitNow=true"
headers={
    'Accept':'*/*',
    'Content-Encoding':'gzip',
    'Content-Type':'application/rdf',
    'Accept-Encoding':'gzip, deflate'
}

def load_rdf_file(ti, fileid):
    global url, headers
    fileId = str(fileid)

    fileName = f"data/accountRelations_{fileId}.rdf.gz"
    ti.xcom_push(key='name', value=fileName)

    dataFileName = os.path.join(conf.get('core', 'DAGS_FOLDER'), fileName)
    with open(dataFileName, 'rb') as dataRaw:
        resp = requests.post(url,headers=headers, data=dataRaw)
        ti.xcom_push(key='status', value=str(resp.status_code))
        
with DAG(
    dag_id= 'dgraph_import_rdf_queue',
    default_args=default_args,
    description='dgraph import rdf queue',
    start_date=datetime(2023,6,23),
    schedule_interval=None
) as dag:
    task1 = PythonOperator(
        task_id='load_rdf_a',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '1_1'}
    )

    task2 = PythonOperator(
        task_id='load_rdf_b',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '1_2'}
    )

    task3 = PythonOperator(
        task_id='load_rdf_c',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '1_3'}
    )

    task4 = PythonOperator(
        task_id='load_rdf_d',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '1_4'}
    )

    task5 = PythonOperator(
        task_id='load_rdf_e',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '1_5'}
    )

    task6 = PythonOperator(
        task_id='load_rdf_f',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '1_6'}
    )

    task7 = PythonOperator(
        task_id='load_rdf_g',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '1_7'}
    )

    task8 = PythonOperator(
        task_id='load_rdf_h',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '10_1'}
    )

    task9 = PythonOperator(
        task_id='load_rdf_i',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '10_2'}
    )

    task10 = PythonOperator(
        task_id='load_rdf_j',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '10_3'}
    )

    task11 = PythonOperator(
        task_id='load_rdf_aa',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '10_4'}
    )

    task12 = PythonOperator(
        task_id='load_rdf_ab',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '10_5'}
    )

    task13 = PythonOperator(
        task_id='load_rdf_ac',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '10_6'}
    )

    task14 = PythonOperator(
        task_id='load_rdf_ad',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '11_1'}
    )

    task15 = PythonOperator(
        task_id='load_rdf_ae',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '11_2'}
    )

    task16 = PythonOperator(
        task_id='load_rdf_af',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '11_3'}
    )

    task17 = PythonOperator(
        task_id='load_rdf_ag',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '11_4'}
    )

    task18 = PythonOperator(
        task_id='load_rdf_ah',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '11_5'}
    )

    task19 = PythonOperator(
        task_id='load_rdf_ai',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '11_6'}
    )

    task20 = PythonOperator(
        task_id='load_rdf_aj',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '11_7'}
    )

    task21 = PythonOperator(
        task_id='load_rdf_ba',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '12_1'}
    )

    task22 = PythonOperator(
        task_id='load_rdf_bb',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '12_2'}
    )

    task23 = PythonOperator(
        task_id='load_rdf_bc',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '12_3'}
    )

    task24 = PythonOperator(
        task_id='load_rdf_bd',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '12_4'}
    )

    task25 = PythonOperator(
        task_id='load_rdf_be',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '12_5'}
    )

    task26 = PythonOperator(
        task_id='load_rdf_bf',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '12_6'}
    )

    task27 = PythonOperator(
        task_id='load_rdf_bg',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '12_7'}
    )

    task28 = PythonOperator(
        task_id='load_rdf_bh',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '13_1'}
    )

    task29 = PythonOperator(
        task_id='load_rdf_bi',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '13_2'}
    )

    task30 = PythonOperator(
        task_id='load_rdf_bj',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '13_3'}
    )

    task31 = PythonOperator(
        task_id='load_rdf_ca',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '13_4'}
    )

    task32 = PythonOperator(
        task_id='load_rdf_cb',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '13_5'}
    )

    task33 = PythonOperator(
        task_id='load_rdf_cc',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '13_6'}
    )

    task34 = PythonOperator(
        task_id='load_rdf_cd',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '13_7'}
    )

    task35 = PythonOperator(
        task_id='load_rdf_ce',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '100_1'}
    )

    task36 = PythonOperator(
        task_id='load_rdf_cf',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '100_2'}
    )

    task37 = PythonOperator(
        task_id='load_rdf_cg',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '100_3'}
    )

    task38 = PythonOperator(
        task_id='load_rdf_ch',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '100_4'}
    )

    task39 = PythonOperator(
        task_id='load_rdf_ci',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '100_5'}
    )

    task40 = PythonOperator(
        task_id='load_rdf_cj',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '100_6'}
    )

    task41 = PythonOperator(
        task_id='load_rdf_da',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '101_1'}
    )

    task42 = PythonOperator(
        task_id='load_rdf_db',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '101_2'}
    )

    task43 = PythonOperator(
        task_id='load_rdf_dc',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '101_3'}
    )

    task44 = PythonOperator(
        task_id='load_rdf_dd',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '101_4'}
    )

    task45 = PythonOperator(
        task_id='load_rdf_de',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '101_5'}
    )

    task46 = PythonOperator(
        task_id='load_rdf_df',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '101_6'}
    )

    task47 = PythonOperator(
        task_id='load_rdf_dg',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '102_1'}
    )

    task48 = PythonOperator(
        task_id='load_rdf_dh',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '102_2'}
    )

    task49 = PythonOperator(
        task_id='load_rdf_di',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '102_3'}
    )

    task50 = PythonOperator(
        task_id='load_rdf_dj',
        python_callable=load_rdf_file,
        op_kwargs={'fileid': '102_4'}
    )

    task1 >> task6 >> task11 >> task16 >> task21 >> task26 >> task31 >> task36 >> task41 >> task46
    task2 >> task7 >> task12 >> task17 >> task22 >> task27 >> task32 >> task37 >> task42 >> task47
    task3 >> task8 >> task13 >> task18 >> task23 >> task28 >> task33 >> task38 >> task43 >> task48
    task4 >> task9 >> task14 >> task19 >> task24 >> task29 >> task34 >> task39 >> task44 >> task49
    task5 >> task10 >> task15 >> task20 >> task25 >> task30 >> task35 >> task40 >> task45 >> task50
