from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime


with DAG(
    dag_id='test_spark_job_dag',
    description='DAG to trigger a Spark job',
    schedule_interval="@daily",
    start_date=datetime(2023, 7, 11)
) as dag:
    spark_job_task = SparkSubmitOperator(
    task_id='run_spark_job',
    application='dags/Spark/test_docker_spark.py',
    conn_id='Cluster_spark',
    total_executor_cores='1',# Tổng số core in 1 worker
    application_args=['--execution_date','{{ ds }}','--name','Dung'],
    executor_cores='1',
    executor_memory='512m',
    num_executors=3,
    driver_memory='1g',
    dag=dag
)
    
