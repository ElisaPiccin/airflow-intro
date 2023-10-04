from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime

my_file = Dataset("/tmp/my_file.txt") #dataset URI
my_file_2 = Dataset("/tmp/my_file_2.txt") 

with DAG(
    dag_id = "producer",
    schedule = "@daily",
    start_date = datetime(2023, 1, 1),
    catchup = False
):
    @task(outlets = [my_file]) # as soon as this task succeeds, the DAG that depends on this Dataset my_file will be automatically triggered 
    def update_dataset():
        with open(my_file.uri, "a+") as f:
            f.write("producer update")
    
    @task(outlets = [my_file_2]) # as soon as this task succeeds, the DAG that depends on this Dataset my_file_2 will be automatically triggered 
    def update_dataset_2():
        with open(my_file_2.uri, "a+") as f:
            f.write("producer update")

    update_dataset()
    update_dataset_2()