from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy import DummyOperator
from airflow.models import Variable
from airflow.operators.python import BranchPythonOperator, PythonOperator
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




def _partner_of_day(execution_date): #to choose partner based on day we need pass current exicution day 
     day = execution_date.day_of_week
     if day == 1:
         return 'extract_partner_facebook' # return next task in ''.  
     if day == 2:
         return 'extract_partner_facebook'
     if day == 3:
         return 'extract_partner_linkd'
     if day == 5:
         return 'extract_partner_google'
     return 'stop'


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

def dag13_branching():
    start= DummyOperator (task_id= "start")
    stop = DummyOperator (task_id= "stop")
    storing = DummyOperator (task_id= "storing", trigger_rule='none_failed_or_skipped')
    #by defaul is some of the parents tasks are skiped this tasks will be skiped
# we want to run this task at very end 
# but we want to run after extact data for parter of day is done 
# to solve this use trigur rule , we will see them in next dag  
    
    choosing_partner_based_on_day = BranchPythonOperator(
        task_id= "choosing_partner_based_on_day",
        python_callable= _partner_of_day #we need to create this funtion 
        #it should have logic to return task id of next task 
        #it should always runturn a task id for every situation 
        #in this case for every day we should get a task id, if thats not the case then we will get a error 

    )
    choosing_partner_based_on_day >> stop
    #below for loop will create dynamic tasks 
    for partner, details in partners.items():
        
        @task.python (multiple_outputs=True, do_xcom_push=False, task_id= f"extract_{partner}")
        def extract(partner, path):
          return {"partner_id": partner, "location": path}
        
        ex_values= extract(details['name'], details['location'])
        start >> choosing_partner_based_on_day>> ex_values
        dynamic_task(ex_values) >> storing
    
dag_start_here = dag13_branching()