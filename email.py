from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
#from airflow.operators.email_operator import EmailOperator
from airflow.operators.email import EmailOperator

# Name of the Dag
DAG_NAME = "test_email"
FREQUENCY = "weekly"

# Set default dag properties
default_args = {
    "owner": "ZS Associates",
    "start_date": datetime(2021, 1, 1),
    "provide_context": True,
    "email_on_failure": True,
    "email": ['mohit.nadda@zs.com']
}

# Define the dag object
dag = DAG(
    DAG_NAME,
    default_args=default_args,
    catchup=False,
    schedule_interval=None,
)

start = DummyOperator(
    task_id="start",
    dag=dag)

email = EmailOperator(
        task_id='send_email',
        to='mohit.nadda@zs.com',
        subject='Airflow Alert',
        html_content=""" <h3>Email Test</h3> """,
        dag=dag
)

# Create a dummy operator task
end = DummyOperator(
    task_id="end",
    dag=dag)


# def test_email_fun(path, **kwargs):
#     print("----------")
#     print("inside function")
#     import smtplib
#
#     sender = 'allergan_insight_ops@zs.com'
#     receivers = ['saksham.agarwal@zs.com']
#
#     message = """
#     This is a test e-mail message.
#     """
#
#     try:
#         smtpObj = smtplib.SMTP('10.121.0.205')
#         smtpObj.sendmail(sender, receivers, message)
#         print("Successfully sent email")
#     except Exception as e:
#         print("Error: unable to send email", e)


# test_email = PythonOperator(
#     task_id="test_email",
#     python_callable=test_email_fun,
#     op_kwargs={'path': ''},
#     dag=dag)


email.set_upstream(start)
end.set_upstream(email)