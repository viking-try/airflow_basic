from airflow import DAG
from datetime import datetime, timedelta
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.decorators  import task, dag
from airflow.utils.task_group import TaskGroup
# you need to do this to use task group 

#task groups a better way to do task grouping
#unlike subdag operator we donot need to to xcom pull, it can be passed by taskflow api like dag 8 and 9

@task.python (multiple_outputs=True, do_xcom_push=False)
def extract():
     partner= "gucky"
     path= "/tmp/gucky"
     return {"partner_id": partner, "location": path}

@task.python
def process_a (partner_name , partner_path):
    # def process_a (): # before it was this
    #ti = get_current_context()['ti']
    #partner_name = ti.xcom_pull(key='partner_id', task_ids='extract', dag_id='dag10_subdag')
    #partner_path = ti.xcom_pull(key='location', task_ids='extract', dag_id='dag10_subdag')
    print(partner_name)
    print(partner_path)

@task.python
def process_b (partner_name , partner_path):
    print(partner_name)
    print(partner_path)

@task.python
def process_c (partner_name , partner_path):
    print(partner_name)
    print(partner_path)


default_args = {
     "start_date": datetime(2021, 1, 1)
}

@dag(description= "subdag dag", default_args=default_args ,
         schedule_interval="@daily", dagrun_timeout=timedelta(minutes=10), tags=["task_group", "test"],
         catchup=False )

def dag11_task_group_1():
    Partner_details= extract()
    with TaskGroup (group_id= "tasks_in_groups") as tasks_in_groups:
    #only thing you need to do is put your tasks below this 
    #like this they virtually grouped 
    #we can also put them in other files to make it look cleaner will do that in next dag   
      process_a(Partner_details['partner_id'], Partner_details['location'] )
      process_b(Partner_details['partner_id'], Partner_details['location'] )
      process_c(Partner_details['partner_id'], Partner_details['location'] )
    
dag_2 = dag11_task_group_1()