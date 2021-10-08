from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy import DummyOperator
from airflow.models.baseoperator import cross_downstream, chain

default_args={
    'start_date': datetime(2021, 1, 1)
}

with DAG ('dag14_DependencyAndModules',
           description= "dependency with chain and cross dependancy module" , 
           default_args=default_args, catchup=False, schedule_interval=None) as dag:
    t1= DummyOperator(task_id= 'start')
    t2= DummyOperator(task_id= 't2')
    t3= DummyOperator(task_id= 't3')
    t4= DummyOperator(task_id= 't4')
    t5= DummyOperator(task_id= 't5')
    t6= DummyOperator(task_id= 't6')
    t7= DummyOperator(task_id= 't7')
     #old way
     #t2.set_upstream(t1)   
    # t1.set_downstream(t2)
     #new way 
     #t2 << t1
     #t1 >> t2

    #basic dependancy with ount any module 
    #[t1, t2, t3] >> t5
    #yes this can we done now t5 will wait for all up stream tasks 
    #[t1, t2, t3] >> [t5,t6,t7]
    # this is not possible, airflow will get confused and will give a error list coonot be mapped to another list 
    #[t1, t2, t3] >> t4
    #[t1, t2, t3] >> t5
    #[t1, t2, t3] >> t6
    #[t4, t5, t6] >> t7 #t7 depends on 4,5,6 and t6 on 1,2,3 
    # above way gets complicated with time to make it easy we have a module cross_downstream
    #from airflow.models.baseoperator import cross_downstream
    #cross_downstream ([t1, t2, t3], [t4,t5,t6])  #list1, list2. It will work of line 32 to 34
    # but remember cross_downstream does not give an out pul so so cannot do below:
    #  cross_downstream ([t1, t2, t3], [t4,t5,t6]) >> t7 
    # to achhive this you need to add below 
    #[t4,t5,t6] >> t7
    #next is chain, with chain operator you can create more complex pipelines 
    # eg t2,3(t3 depends on t2) depends on t1. t4,5 depens on t1. t6 dpends on t5 and t3
    #chain(t1,[t2,t3],[t4,t5],t6)
    #chain (a,[b],[c],d)
    # remember b and c lists should be of same size
    cross_downstream([t2,t3], [t4,t5])
    chain(t1, t2, t5, t6)






  
