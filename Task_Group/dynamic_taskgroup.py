from airflow.decorators  import task, dag, task_group
from airflow.utils.task_group import TaskGroup

@task.python
def process_a (partner_name , partner_path):
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

@task.python
def check_a ():
    print ("check a")
@task.python
def check_b ():
    print ("check b")
@task.python
def check_c ():
    print ("check c")



def dynamic_task(Partner_details):
    with TaskGroup (group_id="dynamictask_task_group", add_suffix_on_collision=True) as dynamictask_task_group:
        with TaskGroup (group_id= "tasks_in_nest") as tasks_in_nest:
          check_a()
          check_b()
          check_c()
        process_a(Partner_details['partner_id'], Partner_details['location'] ) >> tasks_in_nest
        process_b(Partner_details['partner_id'], Partner_details['location'] ) >> tasks_in_nest
        process_c(Partner_details['partner_id'], Partner_details['location'] ) >> tasks_in_nest
         
    return dynamictask_task_group