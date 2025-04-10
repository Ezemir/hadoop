#!/bin/bash

# Caminhos fixos
INPUT_DIR=/data/input
OUTPUT_DIR=/data/output
SCRIPT_DIR=/scripts

# Remover saída anterior se existir
hdfs dfs -rm -r $OUTPUT_DIR

# Enviar arquivos .csv para o HDFS
hdfs dfs -mkdir -p $INPUT_DIR
hdfs dfs -put -f $SCRIPT_DIR/dados.csv $INPUT_DIR/

# Executar o MapReduce com Python
hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming*.jar \
  -input $INPUT_DIR \
  -output $OUTPUT_DIR \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -file $SCRIPT_DIR/mapper.py \
  -file $SCRIPT_DIR/reducer.py

# Mostrar resultado
hdfs dfs -cat $OUTPUT_DIR/part-*
