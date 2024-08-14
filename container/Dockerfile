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

RUN python3 -m venv /opt/litestar
RUN . /opt/litestar/bin/activate && pip install -r ${CIAPI}/requirements.txt
