from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,date
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
import subprocess
from Spark.operator import SparkSubmit


spark_config = {
    "spark.sql.extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
    "spark.sql.catalog.hive_prod": "org.apache.iceberg.spark.SparkCatalog",
    "spark.sql.catalog.hive_prod.type": "hive",
    "spark.sql.defaultCatalog": "hive_prod",
    "spark.sql.catalog.hive_prod.uri": "thrift://hive-metastore:9083",
    "spark.sql.catalog.hive_prod.warehouse": "s3a://warehouse/",
    "spark.sql.catalog.hive_prod.hadoop.fs.s3a.endpoint": "http://minio:9000",
    "spark.sql.catalog.hive_prod.hadoop.fs.s3a.path.style.access": "true",
    "spark.sql.catalog.hive_prod.hadoop.fs.s3a.access.key": "admin",
    "spark.sql.catalog.hive_prod.hadoop.fs.s3a.secret.key": "password",
    "spark.sql.catalog.hive_prod.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
    "spark.sql.catalog.hive_prod.hadoop.fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
    "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
    "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
    "spark.hadoop.fs.s3a.path.style.access": "true",
    "spark.hadoop.fs.s3a.access.key": "admin",
    "spark.hadoop.fs.s3a.secret.key": "password",
    "spark.hadoop.fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
    "spark.master": "spark://spark-master:7077",
    "spark.master.rest.enabled": "true"
}

with DAG(
    dag_id='A_Process_data_hive_spark',
    start_date=datetime(2015,2,1),
    end_date=datetime(2015,2,1),
    schedule='@daily'
) as dag:
    insert_data=SparkSubmit(
    task_id='Insert_data_hive', 
    application='plugins/scripts/project_Hive_Spark/untitled_2.12-0.1.0-SNAPSHOT.jar',
    conn_id='Cluster_spark',
    driver_memory='500m',
    status_poll_interval=1,
    conf=spark_config
    )

# templates_dict={
#         'start_date':date(2015,2,1) ,
#         'end_date':date(2015,2,2),
#         'schema':'transaction',
#         'table_name':'Transaction_History'
# }
# Insert_data(templates_dict)
    # application_args=['--start_date','{{ds}}','--end_date','{{next_ds}}','--data_path','data/archive/transactions.csv'],