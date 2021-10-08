from airflow.models import DAG 
from airflow.decorators  import task, dag
from airflow.operators.python import get_current_context # it will be used to pull xcom crreated by master dag dag 10

#in last dag we used taskflow api to to variable and use it like that line 3 to 6 and line 10 11
#but due to sub dag operator limitations we cannot pass xcom from one dag master to another 
@task.python
def process_a ():
    # def process_a (partner_name, partner_path): # before it was this
    ti = get_current_context()['ti']
    partner_name = ti.xcom_pull(key='partner_id', task_ids='extract', dag_id='dag10_subdag')
    partner_path = ti.xcom_pull(key='location', task_ids='extract', dag_id='dag10_subdag')
    print(partner_name)
    print(partner_path)

def subdag_factory( parent_dag_id, subdag_dag_id, default_args):
    with DAG(f"{parent_dag_id}.{subdag_dag_id}", default_args=default_args) as dag:
        process_a()
        #process_b(partner_settings['partner_name'], partner_settings["partner_path"] )
    return dag