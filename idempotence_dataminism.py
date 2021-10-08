from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta, timedelta
with DAG(dag_id="2dag_IDEM_DATAMINISM", description= "dummy dag", start_date=datetime(2021, 1, 1),
         schedule_interval="@daily", dagrun_timeout=timedelta(minutes=10), tags=["IDEM_DATAMINISM", "test"],
         catchup=False, max_active_runs=1 ) as dag:
    #you can remove dag_id and just write "1dag_dummy" because dag is by default first. 
    #schedule_interval @daily @weekly or a cron */10 * * * * or a timme delta timedelta(minutes=5)
    
    # your dag should have same side effects on ech run and should give same out put of same input
    #if we didnot add "if not in below sql then it will fail on next run so it would not be idempotent"
    #max_active_runs: set how many run of this dag can go at the same time 
    PostgresOperator (task_id="ID_DATA", sql= "CREATE TABLE IF NOT EXISTS accounts ( user_id serial PRIMARY KEY, username VARCHAR ( 50 ) UNIQUE NOT NULL);")