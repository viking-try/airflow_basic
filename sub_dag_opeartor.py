from airflow import DAG
from datetime import datetime, timedelta
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.operators.subdag import SubDagOperator
from airflow.decorators  import task, dag

from subdag.subdag_factory import subdag_factory # import this and use it in subdag task 
#this is the subdag you created in sub dag folder sub dag fectory is funtion in that dag 


@task.python (multiple_outputs=True, do_xcom_push=False)
def extract():
     partner= "gucky"
     path= "/tmp/gucky"
     return {"partner_id": partner, "location": path}

default_args = {
     "start_date": datetime(2021, 1, 1)
} #we are making this to pass start date to subdag so use defaul _args in @dag too

@dag(description= "subdag dag", default_args=default_args ,
         schedule_interval="@daily", dagrun_timeout=timedelta(minutes=10), tags=["subdag", "test"],
         catchup=False )

def dag10_subdag():
     #partner_setting = extract()
     process_task= SubDagOperator(
          task_id= "process_tasks",
          #subdag=subdag_factory("dag10_subdag", "process_tasks", default_args, partner_setting) #now we need to created subdag factory in subdag in subdag folder
          #subdag=subdag_factory("<dag_name>", "<taskid for subdag>", default_args, <xcom values for extract>)
          # create default argumnet with start date so start date for sub dag and taks is same
          #airflow.exceptions.AirflowException: Tried to set relationships between tasks in more than one DAG: dict_values([<DAG: dag10_subdag.process_tasks>, <DAG: dag10_subdag>]
          # We will get abbove error if we try to run it like that because "partner_setting" line 27 is using task flow api amd is = xcom arg 
          #and as we try to pass partner_setting to sub dag operator task flowapi  tries to create depency which is not possible 
          # beacuse partner_setting will be used in another dag 
          #so you use like below without xcom and pull xcom in sub dag.  
          subdag=subdag_factory("dag10_subdag", "process_tasks", default_args)
     )
     extract() >> process_task
dag = dag10_subdag()