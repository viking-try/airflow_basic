from airflow import DAG
from datetime import datetime, timedelta, timedelta
from airflow.operators.python import PythonOperator
from airflow.decorators  import task, dag

#How to pass multiple xcom values to next task 
#we are not going to use multple xcom push and pull
@task.python (multiple_outputs=True)
#@task.python (task_id="extrat_dag", multiple_outputs=True)
#you can pass values to @task like task_id="extrat_dag" so it will appear as this on UI 
# to pass multiple values use  
def extract():  # if you donot want to use multiple vaule on top , then you can mention what kind of out put is expected fron this funtion
     #def extract() -> dict[str, str]:
     #like this it will return multiple val since we are returning dictionary we mention dict
     partner= "gucky"
     path= "/tmp/gucky"
     return {"partner_id": partner, "location": path}
     # we used same before to pass values and they were sent in return_values xcom
     # but here by using  multiple_outputs a diffrent xcom will be created by key name partner_id, location
     # but return_values will also be created by default  to stop thats use below 
     #@task.python (task_id="extrat_dag", do_xcom_push=False, multiple_outputs=True)

@task.python  # now how to use multiple xcom here? 
def process(makeit, takeit):  #add required vars here and make changes in dag dependancy line 32 
     print (makeit)
     print(takeit)

@dag(description= "taskflow api dag doco", start_date=datetime(2021, 1, 1),
         schedule_interval="@daily", dagrun_timeout=timedelta(minutes=10),
         catchup=False, tags=["taskflow_api", "xcom", "test"] )

def dag9_taskflow_api_xcom_2(): #to pass xom 
    partner_details = extract() #so we are taking xcom in this var by running the task 
    #process(extract()) before it looked like this
    process(partner_details['partner_id'],partner_details['location'] )  #both are key names and will be passed to process task 

rundag = dag9_taskflow_api_xcom_2()