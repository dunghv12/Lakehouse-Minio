from airflow.models import BaseOperator
class MyCustomOperator(BaseOperator):

    def __init__(self, *args, **kwargs):
        super(MyCustomOperator, self).__init__(*args, **kwargs)

    def execute(self, context):
        print("Hello World")
        print(context)