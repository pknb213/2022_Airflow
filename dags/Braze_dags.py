from datetime import datetime, timedelta
from textwrap import dedent
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from Braze import *

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def print_result(**kwargs):
    r = kwargs["task_instance"].xcom_pull(key='result_msg')
    print("message : ", r)


default_args = {
    'owner': 'Cheon YoungJo',
    'depends_on_past': True,
    'email': ['pknb213@naver.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=15),
}
with DAG(
    'Braze Update By External_Id API',
    **default_args,
    description='A simple Echo Test DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 8, 3),
    catchup=False,
    tags=['Braze_API'],
) as dag:
    t1 = BashOperator(
        task_id='start',
        bash_command='echo "Braze Workflow Start!!"',
    )

    t2 = PythonOperator(
        task_id='internal_db_loading',
        depends_on_past=True,
        python_callable={},
        retries=3,
    )

    t3 = PythonOperator(
        task_id='transforming',
        depends_on_past=True,
        python_callable={},
        retries=3,
    )

    t4 = PythonOperator(
        task_id='requesting',
        depends_on_past=True,
        python_callable={},
        retries=3,
    )

    t5 = PythonOperator(
        task_id='msg',
        depends_on_past=True,
        python_callable=print_result
    )

    t6 = BashOperator(
        task_id='complete',
        depends_on_past=True,
        bash_command='echo "Braze Workflow Complete!!"',
    )

    t1.doc_md = dedent(
        """\
    #### Task Documentation
    You can document your task using the attributes `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.
    ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)

    """
    )

    dag.doc_md = __doc__  # providing that you have a docstring at the beginning of the DAG
    dag.doc_md = """
    This is a documentation placed anywhere
    """  # otherwise, type it like this

    t1 >> t2 >> t3
