FROM ubuntu:16.04
LABEL maintainer="bugra@ymail.com"
RUN apt-get update --fix-missing
RUN apt-get install -y python3 python3-pip libssl-dev python3-dev build-essential librdkafka-dev curl wget libssl-dev libffi-dev
RUN apt-get install -y freetds-dev 
RUN ln -s /usr/bin/python3 /usr/bin/python

ENV LIBRDKAFKA_VERSION 0.11.6
RUN curl -Lk -o /root/librdkafka-${LIBRDKAFKA_VERSION}.tar.gz https://github.com/edenhill/librdkafka/archive/v${LIBRDKAFKA_VERSION}.tar.gz && \
    tar -xzf /root/librdkafka-${LIBRDKAFKA_VERSION}.tar.gz -C /root && \
    cd /root/librdkafka-${LIBRDKAFKA_VERSION} && \
    ./configure && make && make install && make clean && ./configure --clean

ENV CPLUS_INCLUDE_PATH /usr/local/include
ENV LIBRARY_PATH /usr/local/lib
ENV LD_LIBRARY_PATH /usr/local/lib
RUN pip3 install baybars==0.0.23
RUN pip3 install pytest

