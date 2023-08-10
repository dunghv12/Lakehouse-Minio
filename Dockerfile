# FROM apache/airflow:2.6.2-python3.9
# FROM apache/airflow:slim-2.6.2-python3.9
# FROM apache/airflow:slim-2.7.0b1-python3.9
FROM apache/airflow:2.6.2-python3.9
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         openjdk-11-jre-headless \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && apt-get install -y procps \
  && rm -rf /var/lib/apt/lists/*
USER airflow
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" apache-airflow-providers-apache-spark
RUN pip install psycopg2-binary
# RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" pyarrow==10.0.1