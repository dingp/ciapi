#miniconda based python 3.9 image
FROM docker.io/library/ubuntu:noble

#RUN sed -i~ -e 's,http://.*.ubuntu.com,http://linux.mirrors.es.net,' /etc/apt/sources.list

ARG DEBIAN_FRONTEND=noninteractive

RUN \
    apt-get update        && \
    apt-get upgrade --yes && \
    apt-get install --yes    \
        python3 python3-pip python3-venv &&  \
    apt-get clean all    &&  \
    rm -rf /var/lib/apt/lists/*

ARG CIAPI=/opt/ciapi
RUN  \
    mkdir -p $CIAPI && \
    cd $CIAPI && \
    git clone https://github.com/pding/ciapi

RUN \
    cd /opt && \
    python3 -m venv litestar && \
    source /opt/litestar/bin/activate && \
    pip install litestar uvicorn
