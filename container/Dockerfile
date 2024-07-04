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


RUN cd /opt && python3 -m venv litestar
RUN ["/bin/bash", "-c", "source /opt/litestar/bin/activate && pip install litestar uvicorn"]


ARG CIAPI=/opt/ciapi
RUN mkdir -p ${CIAPI} && \
    cd ${CIAPI} && \
    git clone https://github.com/dingp/ciapi
