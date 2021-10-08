from airflow import DAG
from datetime import datetime, timedelta, timedelta
from airflow.operators.python import PythonOperator
from airflow.decorators import task, dag    
#this is how me import task and dag decorator

@task.python
def extract():
     partner= "gucky"
     path= "/tmp/gucky"
     return partner

@task.python
def process(makeit):   # just mnetion a variable here any name 
     print (makeit)  #  xcom val will be passed by line 21

with DAG(dag_id="8dag_api_taskflow_xcom",description= "taskflow api dag doco", start_date=datetime(2021, 1, 1),
         schedule_interval="@daily", dagrun_timeout=timedelta(minutes=10),
         catchup=False, tags=["taskflow_api","xcom","test"] ) as dag:

    process(extract())    #this how we take xcom dependancy using task flow api 
#we donot need to add dag aanme in above
# you can create a funtion like below and name to funtion will be name of dag:          
#decorator must be on top funtion 
#put your dag dependies like below 

#finally call your dag funtion 