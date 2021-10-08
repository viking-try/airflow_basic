from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

DEFAULT_ARGS = {
    "owner": "airflow",

}


@task
def some_other_task():
    pass


@dag(
    default_args=DEFAULT_ARGS,
    schedule_interval=None,
    start_date=days_ago(2),
    tags= ["dag_deco", "test"]
)
def dag_7_decorator():
    some_other_task()


DAG_2 = dag_7_decorator()