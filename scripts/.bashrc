# --- rest of the .bashrc file ---


export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin
export PATH=$PATH:$SPARK_HOME/sbin

export PYSPARK_DRIVER_PYTHON="jupyter"
export PYSPARK_DRIVER_PYTHON_OPTS="notebook --ip=* --NotebookApp.token=''"