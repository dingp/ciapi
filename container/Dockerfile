FROM python:3.12-slim-bookworm

RUN apt update && \
    apt install -y curl git wget

RUN curl -sSL "https://raw.githubusercontent.com/upciti/wakemeops/main/assets/install_repository" | bash && \
    apt install -y glab

RUN mkdir -p -m 755 /etc/apt/keyrings && \
    wget -qO- https://cli.github.com/packages/githubcli-archive-keyring.gpg | tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null && \
    chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt update && \
    apt install -y gh

RUN apt-get clean all

ARG CIAPI=/opt/ciapi
RUN git clone https://github.com/dingp/ciapi ${CIAPI}

RUN python3 -m venv /opt/litestar
RUN . /opt/litestar/bin/activate && pip install -r ${CIAPI}/requirements.txt
