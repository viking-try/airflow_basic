from airflow import DAG
from datetime import datetime, timedelta
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.decorators  import task, dag
from airflow.utils.task_group import TaskGroup  # you need to do this to use task group 
from Task_Group.grouped_tasks import grouped_tasks # you are importing taskgroup from adiffrent file here 



@task.python (multiple_outputs=True, do_xcom_push=False)
def extract():
     partner= "gucky"
     path= "/tmp/gucky"
     return {"partner_id": partner, "location": path}

default_args = {
     "start_date": datetime(2021, 1, 1)
}

@dag(description= "subdag dag", default_args=default_args ,
         schedule_interval="@daily", dagrun_timeout=timedelta(minutes=10), tags=["task_group", "test"],
         catchup=False )

def dag11_task_group_2():
    Partner_details= extract()
    #we are puting task group in other files to make it look cleaner
    grouped_tasks(Partner_details) #we are passing xcom to task group here 
    # task groups work well with taskflow apis 
    
dag = dag11_task_group_2()