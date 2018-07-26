FROM ubuntu:17.10

RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  wget \
  unzip \
  git \
  cmake \
  pkg-config \
  gfortran \
  python3.6-dev \
  python3-pip \
  liblapacke-dev \
  libopenblas-base \
  libopenblas-dev \
  swig \
  libssl-dev \
  libffi-dev \
  curl \
  librdkafka-dev\
  freetds-bin \
  freetds-common \
  freetds-dev

# Openblas environment variables
ENV LD_LIBRARY_PATH /usr/lib/x86_64-linux-gnu/
ENV BLASLDFLAGS /usr/lib/x86_64-linux-gnu/libopenblas.so.0

# For librdkafka, we need to overwrite system-wide python with python3
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install Librdkafka for kafka dependencies 
RUN mkdir -p /root/librdkafka
RUN curl -Lk -o /root/librdkafka.tar.gz https://github.com/edenhill/librdkafka/archive/v0.11.3.tar.gz &&\
    tar -xzf /root/librdkafka.tar.gz -C /root &&\
    cd /root/librdkafka-0.11.3 && \
    ./configure && make && make install && make clean && ./configure --clean

ENV CPLUS_INCLUDE_PATH /usr/local/include
ENV LIBRARY_PATH /usr/local/lib
ENV LD_LIBRARY_PATH /usr/local/lib

COPY baybars /root/python/baybars
WORKDIR /root/python/baybars

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "sql.py"]

