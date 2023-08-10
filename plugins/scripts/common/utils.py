from pyspark.sql import SparkSession
def create_spark_session():
    spark=SparkSession \
        .builder \
        .config("spark.hadoop.hive.metastore.uris","thrift://host.docker.internal:9083")\
        .config("spark.hadoop.hive.exec.dynamic.partition","true")\
        .config("spark.hadoop.hive.exec.dynamic.partition.mode","nonstrict")\
        .getOrCreate()
    sc=spark.sparkContext
    return spark,sc