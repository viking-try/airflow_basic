from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta, timedelta
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

class PostgresOperatorCustom(PostgresOperator):
     template_fields = ('sql','parameters')
     
def _my_user(name):
     #passing variable to this funtion ussing oparg in python callable  
     print (name)
with DAG(dag_id="4dag_templating", description= "dummy dag", start_date=datetime(2021, 1, 1),
         schedule_interval="@daily", dagrun_timeout=timedelta(minutes=10), tags=["jijja", "test"],
         catchup=False ) as dag:

         jinjaT_python = PythonOperator(
              task_id= "python_with_jinja",
              python_callable=_my_user,
              op_args=['{{ var.json.partner.name }}']
         )
     # you vcannot use jinja every were fist make sure that filed can we tepmlated.
     #https://registry.astronomer.io/ user this site to see if filed in templated 
     #sql filed is templated so we can use jinja 
         JinjaT_Posgre = PostgresOperator(
              task_id= "jinja_with_posgre",
              #sql= "SELECT partnet FROM partner where date=2021-10-1 "
              #above satement  will alwyas return same output lets teplate date 
              #sql= "SELECT partnet FROM partner where date={{ ds }}",
              #we can able use sql file as it is best practice sparate dags from sql and other things 
              sql= "sql/templated_sql.sql"

         )
         #:param parameters: (optional) the parameters to render the SQL query with.
         #by default parameters in posgre operator are not templeated if you want to use parameters then 
         #make a custom posgre oprator 
         JinjaT_Posgre_Custom = PostgresOperatorCustom(
              task_id= "jinja_with_posgr_custom",
              sql= "sql/templated_sql.sql",
              parameters={
                   'next_exicution': '{{ next_ds }}',
                   'Prev_ds': '{{ prev_ds }}',
                   'partner_name2': '{{ var.json.partner.name }}'
              }
         )
