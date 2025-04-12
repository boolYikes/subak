FROM python:3.12-bullseye

# Seperation of concerns even if it involves more layers.
# Which leads to better caching... apparently...
RUN apt update && \
    apt install -y --no-install-recommends openjdk-17-jdk gcc make git nano python3-pip && \
    apt clean && \
    rm -rf /var/lib/lists/*
RUN pip3 install psycopg2-binary clickhouse-connect --no-cache

# Databricks dbgen
RUN mkdir -p /usr/local/app/workspace
WORKDIR /usr/local/app/workspace
RUN git clone https://github.com/databricks/tpch-dbgen
WORKDIR /usr/local/app/workspace/tpch-dbgen
RUN make
RUN echo 'echo -e "\033[33mdbgen is in /usr/local/app/workspace/tpch-dbgen\033[0m, \033[34mmove data to /data\033[0m, \033[35mscripts are in /scripts\033[0m"' >> /etc/bash.bashrc

# Spark related
ENV SPARK_HOME="/opt/spark"
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
ENV PATH="${JAVA_HOME}:${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}"
RUN mkdir -p ${SPARK_HOME}
WORKDIR ${SPARK_HOME}
RUN curl https://dlcdn.apache.org/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz -o spark-3.5.5-bin-hadoop3.tgz \
    && tar xvzf spark-3.5.5-bin-hadoop3.tgz --directory ${SPARK_HOME} --strip-components 1 \
    && rm -rf spark-3.5.5-bin-hadoop3.tgz

ENV SPARK_MASTER_PORT="7077"
# Hostname DNS
ENV SPARK_MASTER_HOST="spark-master" 
# -> spark://spark-master:7077

COPY ./spark-defaults.conf "${SPARK_HOME}/conf"
# start commands -> this only is a suggestion
ENTRYPOINT [ "/bin/bash" ] 
# -> to be used in docker ocmpose