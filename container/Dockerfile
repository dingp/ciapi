FROM python:3.12-alpine

RUN apk add --no-cache git glab github-cli


ARG CIAPI=/opt/ciapi
RUN git clone https://github.com/dingp/ciapi ${CIAPI}

RUN python3 -m venv /opt/litestar
RUN . /opt/litestar/bin/activate && pip install -r ${CIAPI}/requirements.txt && pip cache purge
