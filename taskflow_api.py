from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta, timedelta
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.decorators import task    #this is how me import task decorator

@task.python
#def _extract(ti): #we need to remove _ from fuction name. 
def extract():   # now task name will be extract
     partner= "gucky"
     path= "/tmp/gucky"
     #xcom push for multiple values, we use json to send multiple values
     return {"partner_name": partner, "partner_path": path}
@task.python
def process():
     print ("process")

with DAG(dag_id="6dag_taskflow_api_Task_decorator", description= "dummy dag", start_date=datetime(2021, 1, 1),
         schedule_interval="@daily", dagrun_timeout=timedelta(minutes=10), tags=["task_flow_api", "task deco", "tast"],
         catchup=False ) as dag:
    # Now we donot need start pythoneoperator here it will created by defaut
    #      
    #extract= PythonOperator(
    #     task_id= "extract",
    #     python_callable= _extract
    #)

    extract() >> process()
    #to instantiate pythonoperator you need run it like python funtion eg extract()