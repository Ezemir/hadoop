#!/bin/bash

export HDFS_URI=hdfs://namenode:9000

echo "Aguardando o fim do modo de segurança do NameNode..."
until hdfs dfsadmin -fs $HDFS_URI -safemode get | grep -q "OFF"; do
  echo "Ainda em modo seguro... aguardando..."
  sleep 5
done

echo "Criando diretório no HDFS..."
hdfs dfs -fs $HDFS_URI -mkdir -p /data/input

echo "Enviando arquivos CSV para o HDFS..."
hdfs dfs -fs $HDFS_URI -put -f /data/csv/*.csv /data/input/

echo "Executando Job Hadoop..."
hadoop jar /hadoop-config/job.jar br.com.vpsic.DieselJob $HDFS_URI/data/input $HDFS_URI/data/output

echo "Job executado com sucesso. Verifique o output no HDFS:"
hdfs dfs -ls $HDFS_URI/data/output
