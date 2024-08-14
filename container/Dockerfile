#miniconda based python 3.9 image
FROM docker.io/library/ubuntu:noble

ARG DEBIAN_FRONTEND=noninteractive

RUN \
    apt-get update        && \
    apt-get upgrade --yes && \
    apt-get install --yes    \
        git python3 python3-pip python3-venv &&  \
    apt-get clean all    &&  \
    rm -rf /var/lib/apt/lists/*

ARG CIAPI=/opt/ciapi
RUN git clone https://github.com/dingp/ciapi ${CIAPI}

RUN cd /opt && python3 -m venv litestar
RUN source /opt/litestar/bin/activate && \
    pip install -r ${CIAPI}/requirements.txt
