from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
 
from datetime import datetime

# first way to share a value 
# def _t1():
#     return 42 # --> create a corresponding xcom with key equals to "return_value"

def _t1(ti):
    ti.xcom_push(key="my_key", value=42)
    ti.xcom_push(key="my_new_key", value={"foo": "bar"})
 
def _t2(ti):
    print(ti.xcom_pull(key="my_key", task_ids="t1"))
 
with DAG("xcom_dag", start_date=datetime(2022, 1, 1), 
    schedule_interval='@daily', catchup=False) as dag:
 
    t1 = PythonOperator(
        task_id='t1',
        python_callable=_t1
    )
 
    t2 = PythonOperator(
        task_id='t2',
        python_callable=_t2
    )
 
    t3 = BashOperator(
        task_id='t3',
        bash_command="echo ''"
    )
 
    t1 >> t2 >> t3