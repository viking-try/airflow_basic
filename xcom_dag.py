from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta, timedelta
from airflow.models import Variable
from airflow.operators.python import PythonOperator

def _extract(ti):
     # ti is task instanace and used in xcom 
     partner= "netflix"
     ti.xcom_push (key="partner_name", value=partner)
     #by xcom push we push values to xcom which are stored in airflow db and  can be useed by other process 
     #in airflow 2.0 it is stored as json 
     print("extract")

def _extract2(ti):
     partner= "facebook"
     print("extract2")
     #insatred of using xcom push you can just return the values and it will be stored in xcom as "return_value"
     return partner
def _extract3(ti):
     partner= "gucky"
     path= "/tmp/gucky"
     print("extract3")
     #xcom push for multiple values, we use json to send multiple values
     return {"partner_name": partner, "partner_path": path} 

def _process(ti):
     partner_name= ti.xcom_pull (key="partner_name", task_ids="extract")
     print (partner_name)
     print("process")

def _process2(ti):
     #here we will use return_value as key from extract 1
     partner_name= ti.xcom_pull (key="return_value", task_ids="extract2")
     #or we can just remove key and write it like below 
     partner_name2= ti.xcom_pull (task_ids="extract2")
     print (partner_name)
     print (partner_name2)
     print("process2")

def _process3(ti):
     partner_name= ti.xcom_pull (key="return_value", task_ids="extract3")
     print (partner_name['partner_path'])
     print("process3")


with DAG(dag_id="5dag_xcom", description= "dummy dag", start_date=datetime(2021, 1, 1),
         schedule_interval="@daily", dagrun_timeout=timedelta(minutes=10), tags=["xcom", "test"],
         catchup=False ) as dag:
    extract= PythonOperator(
         task_id= "extract",
         python_callable= _extract
    )
    process= PythonOperator(
         task_id= "process",
         python_callable= _process
    )
    extract2= PythonOperator(
         task_id= "extract2",
         python_callable= _extract2
    )
    process2= PythonOperator(
         task_id= "process2",
         python_callable= _process2
    )
    extract3= PythonOperator(
         task_id= "extract3",
         python_callable= _extract3
    )
    process3= PythonOperator(
         task_id= "process3",
         python_callable= _process3
    )

    extract>>process
    extract2>>process2
    extract3>>process3
