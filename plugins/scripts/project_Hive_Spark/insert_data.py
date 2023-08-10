# from ..common import utils 

# from datetime import date,timedelta
# import pyspark.sql.functions as F
# import argparse
# import sys
# sys.path.append("/opt/airflow")
# # from plugins.scripts.common.utils import create_spark_session 

# #
# parser=argparse.ArgumentParser()
# parser.add_argument('--start_date',required=True,help='Ngay bat dau ingestion')
# parser.add_argument('--end_date',required=True,help='Ngay ket thuc ingestion')
# # parser.add_argument('--schema',type=str,required=True,help='Database cua hive hadoop')
# # parser.add_argument('--table_name',type=str,required=True,help='Table cua hive-hadoop')
# parser.add_argument('--data_path',required=True,help='Duong dan data de extract file')

# arg=parser.parse_args()
# start_date=arg.start_date
# end_date=arg.end_date
# # schema=arg.schema
# # table_name=arg.table_name
# data_path=arg.data_path

# print('Duong dan ne',start_date,end_date,data_path)
# from pyspark.sql import SparkSession
# def create_spark_session():
#     spark=SparkSession \
#         .builder \
#         .getOrCreate()
#     sc=spark.sparkContext
#     return spark,sc
# def Insert_data(start_date,end_date,data_path):
#     spark,sc=create_spark_session()
#     print(sc.parallelize([1,2,4,5,6]).count())
#     data=spark.read.format('csv')\
#             .option('header',True)\
#             .load(f'{data_path}')\
#             .filter(F.col('DATE')>=start_date)\
#             .filter(F.col('DATE')<=end_date)
#     print(data.show())
# Insert_data(start_date,end_date,data_path)
# #     print(data.show())
# #     data.repartition(1).\
# #         write.mode('append').\
# #         format('parquet').\
# #         partitionBy('YEAR','MONTH').\
# #         saveAsTable('Transaction_History')   
# # Insert_data(start_date,end_date,data_path)

# # spark,sc=create_spark_session()
# # print(sc.parallelize([1,2,4,5,6]).count())

# # templates_dict=
# #         'start_date':date(2015,2,1) ,
# #         'end_date':date(2015,2,2),
# #         'schema':'transaction',
# #         'table_name':'Transaction_History'
# # }
# # Insert_data(templates_dict)
# # spark,sc=create_spark_session()
# # data=spark.read.format('csv')\
# #         .option('header',True)\
# #         .load('../../data/archive/transactions.csv')\
# #         .filter(F.col('DATE')<'2015-01-02')
# # print(data.printSchema())
# # print(data.show(5))