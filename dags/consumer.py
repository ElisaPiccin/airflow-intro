from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime

my_file = Dataset("/tmp/my_file.txt") # dataset URI (same as in the producer)
my_file_2 = Dataset("/tmp/my_file_2.txt") 

with DAG(
    dag_id = "consumer",
    #schedule = [my_file], # as soon as this dataset is updated 
    schedule = [my_file, my_file_2], # as soon as both datasets are updated 
    start_date = datetime(2023, 1, 1),
    catchup = False
):
    
    @task
    def read_dataset():
        with open(my_file.uri, "r") as f:
            print(f.read())

    read_dataset()