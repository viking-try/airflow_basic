from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy import DummyOperator
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.decorators  import task, dag
from airflow.utils.task_group import TaskGroup   
from Task_Group.dynamic_taskgroup import dynamic_task

from typing import Dict
# to create dynamic tasks airflow must know required values before hand
# we cannot create dynamic tasks based on output of anouthera tsks as of now 
# below dict containe informaion regarding all partners and based on it we will create tasks  
partners= {
    "partner_facebook":
    {
        "name": "facebook",
        "location": "/tmp/facebook"
    },
    "partner_linkd":
    {
        "name": "linkd",
        "location": "/tmp/linkd"
    },
    "partner_google":
    {
        "name": "google",
        "location": "/tmp/location"
    }
}

@task.python (multiple_outputs=True, do_xcom_push=False)
def extract(partner, path, partnerall):
    print (partnerall)
    return {"partner_id": partner, "location": path}

default_args = {
     "start_date": datetime(2021, 1, 1)
}

@dag(description= "subdag dag", default_args=default_args ,
         schedule_interval="@daily", dagrun_timeout=timedelta(minutes=10), tags=["task_group","dynamic_task" , "test"],
         catchup=False )

def dag12_dynamic_tasks():
    start= DummyOperator (task_id= "start")
    #below for loop will create dynamic tasks 
    for partner, details in partners.items():

        @task.python (multiple_outputs=True, do_xcom_push=False, task_id= f"extract_{partner}")
        def extract(partner, path):
          return {"partner_id": partner, "location": path}
        
        ex_values= extract(details['name'], details['location'])
        start >> ex_values
        dynamic_task(ex_values)

        # by default this will give a error, why? 
        #  because task groups retuens a tasks group and that task groups keeps the same id
        #you cannot have multiple task group with same idS
        #airflow.exceptions.DuplicateTaskIdFound: group_id 'tasks_in_groups_nested' has already been added to the DAG
        # to over come this add parameter in your task group file   add_suffix_on_collision=True
    
    #grouped_tasks_nested(Partner_details)
    
dag_start_here = dag12_dynamic_tasks()