FROM bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8

RUN mkdir -p /data/csv /scripts /data/output

COPY ./data/csv /data/csv
COPY ./scripts/load_hdfs.sh /scripts/load_hdfs.sh

RUN chmod +x /scripts/load_hdfs.sh
