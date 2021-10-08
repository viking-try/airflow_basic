from airflow.decorators  import task, dag
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


def grouped_tasks(Partner_details):
    with TaskGroup (group_id= "tasks_in_groups") as tasks_in_groups:
    #only thing you need to do is put your tasks below this 
    #like this they virtually grouped 
    #we can also put them in other files to make it look cleaner will do that in next dag   
      process_a(Partner_details['partner_id'], Partner_details['location'] )
      process_b(Partner_details['partner_id'], Partner_details['location'] )
      process_c(Partner_details['partner_id'], Partner_details['location'] )
      #what if you want to create a task group with in a task group
      #see in next dag 
    return tasks_in_groups # return group id