from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta, timedelta
with DAG(dag_id="1dag_dummy", description= "dummy dag", start_date=datetime(2021, 1, 1),
         schedule_interval="@daily", dagrun_timeout=timedelta(minutes=10), tags=["dummy", "test"],
         catchup=False ) as dag:
    #you can remove dag_id and just write "1dag_dummy" because dag is by default first. 
    #schedule_interval @daily @weekly or a cron */10 * * * * or a timme delta timedelta(minutes=5)
    None