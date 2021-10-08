from airflow import DAG
from datetime import datetime, timedelta
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.decorators  import task, dag
from airflow.utils.task_group import TaskGroup   
from Task_Group.grouped_tasks_nested import grouped_tasks_nested 
# line 6you need to do this to use task group
# you are importing taskgroup from adiffrent file here 
#in this dag we are calling task group within task group

@task.python (multiple_outputs=True, do_xcom_push=False)
def extract():
     partner= "gucky"
     path= "/tmp/gucky"
     return {"partner_id": partner, "location": path}

default_args = {
     "start_date": datetime(2021, 1, 1)
}

@dag(description= "subdag dag", default_args=default_args ,
         schedule_interval="@daily", dagrun_timeout=timedelta(minutes=10), tags=["task_group","nested" , "test"],
         catchup=False )

def dag11_task_group_nested_3():
    Partner_details= extract()
    grouped_tasks_nested(Partner_details)
    
dag = dag11_task_group_nested_3()