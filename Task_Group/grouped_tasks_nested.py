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



def grouped_tasks_nested(Partner_details):
    #we are using task group decorator now @task_group
    #@task_group (group_id= "tasks_in_groups_nested") It didnot work
    # as it is decorator, is must be followed by a funtion  
    #def tasks_groups_nested():
    with TaskGroup (group_id="tasks_in_groups_nested") as tasks_in_groups_nested:
      #what if you want to create a task group with in a task group
        with TaskGroup (group_id= "tasks_in_nest") as tasks_in_nest:
          check_a()
          check_b()
          check_c()
        process_a(Partner_details['partner_id'], Partner_details['location'] ) >> tasks_in_nest
        process_b(Partner_details['partner_id'], Partner_details['location'] ) >> tasks_in_nest
        process_c(Partner_details['partner_id'], Partner_details['location'] ) >> tasks_in_nest  # we are mentioning tasks_in_nest
      # so subdag tasks_in_nest will be run after  process a/b/c
         
    return tasks_in_groups_nested # return group id