from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta, timedelta

def _get_user():
     #python_varibale = Variable.get("Key_of_airflow_variable")
     #Secret variables: values of these varibale is not shown nigher is task logs nor on airflow UI eg add password at end of key
     #my_user = Variable.get("user")
     partner_deatails = Variable.get("partner", deserialize_json=True)
     name = partner_deatails['name']
     passwordkey = partner_deatails['passowrd']
     pathname = partner_deatails['path']
     my_pass = Variable.get("password")
     print(name)
     print(passwordkey)
     print(pathname)
     #print(my_user)
     print(my_pass)
def _my_user(name):
     #passing variable to this funtion ussing op in python callable  
     print (name)

with DAG(dag_id="3dag_variable", description= "dummy dag", start_date=datetime(2021, 1, 1),
         schedule_interval="@daily", dagrun_timeout=timedelta(minutes=10), tags=["variables", "test"],
         catchup=False ) as dag:
    #you can remove dag_id and just write "1dag_dummy" because dag is by default first. 
    #schedule_interval @daily @weekly or a cron */10 * * * * or a timme delta timedelta(minutes=5)
     extract = PythonOperator(
          task_id="extract",
          python_callable=_get_user
     )
     myuser = PythonOperator(
          task_id="jinjatmppasingvalues",
          python_callable=_my_user,
          op_args=[Variable.get("partner", deserialize_json=True)['name']]
          #Variable.get("partner", deserialize_json=True)<key in json>
          #still it will  make connection to db to aviod that use jinja templeting 
     )
     jijja = PythonOperator(
          task_id="jinja",
          python_callable=_my_user,
          op_args=["{{var.json.partner.name}}"]
          #now connection will be made at runtime only
          #["{{var.json.<UI_json_variable_name>.<jsonkey>}}"]
     )
     env_var_jijja = PythonOperator(
          task_id="jinja_env_var",
          python_callable=_my_user,
          op_args=["{{var.json.FOO_BAZ.hello}}"]
          #carete a env variable by 
          # env AIRFLOW_VAR_partner2='{ "name": "user1", "passowrd": "passwd1", "path": "/tmp/user1" }'
          #  --> airflow variable named partner2 will be created 
          # this VAR will not be visible on UI or in aiflow command but be used in task by jinja 
          #now no connection will made to db
          #["{{var.json.<UI_json_variable_name>.<jsonkey>}}"]
     )
     