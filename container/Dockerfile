#miniconda based python 3.9 image
FROM python:3-alpine

RUN apk update && apk add git glab github-cli

ARG CIAPI=/opt/ciapi
RUN git clone https://github.com/dingp/ciapi ${CIAPI}

RUN python3 -m venv /opt/litestar
RUN . /opt/litestar/bin/activate && pip install -r ${CIAPI}/requirements.txt
