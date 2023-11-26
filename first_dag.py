from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import pendulum

from extract import extract 
from app_db import dumb_db
from transform import transform
from google_sheet import send_data_to_google_sheet
import time

with DAG(dag_id="my_first_etlpipeline"
        ,default_args={"retries":2}
        ,schedule_interval="0 0 * * *"
        ,start_date=pendulum.datetime(2023,2,10,tz="UTC")
        ,catchup=False
        ,tags=["etl","custom tag"]) as dag:

         

        extract_task = PythonOperator(task_id="extract_data"
        ,python_callable=extract 
        ,op_kwargs={"name":"mohammad"})

        database_task = PythonOperator(task_id="database"
        ,python_callable=dumb_db
        ,op_kwargs={"name":"mohammad"})


        transform_task = PythonOperator(task_id="transform"
        ,python_callable=transform 
        ,op_kwargs={"name":"mohammad"})

        dumb_googlesheet = PythonOperator(task_id="google_sheet"
        ,python_callable=send_data_to_google_sheet 
        ,op_kwargs={"name":"mohammad"})


extract_task >> database_task >>transform_task >> dumb_googlesheet
