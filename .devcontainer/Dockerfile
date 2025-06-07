FROM ubuntu:24.04
ARG PLANTUML_VERSION=1.2024.6
ARG DRAWIO_VERSION=26.2.15
ARG POETRY_VERSION=2.1.1
ARG PYTHON_VERSION=3.12
ENV PLANTUML_PATH=/usr/share/plantuml/plantuml.jar

SHELL ["/bin/bash","-c"]

RUN apt-get update && apt-get upgrade -y
RUN DEBIAN_FRONTEND=noninteractive  apt install -y \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libssl-dev \
    git \
    curl \
    make \
    graphviz \
    locales \
    locales-all \
    openjdk-17-jdk \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-venv \
    python3-pip-whl \
    python3-pip \
    xvfb \
    libgbm1 \
    libxss1 \
    libgtk-3-0 \
    libnotify4 \
    xdg-utils \
    libsecret-1-0 \
    --fix-broken --assume-yes

RUN apt install -y pipx rsync

RUN mkdir -p $(dirname "${PLANTUML_PATH}")

RUN curl -o ${PLANTUML_PATH} -L \
    https://github.com/plantuml/plantuml/releases/download/v${PLANTUML_VERSION}/plantuml-mit-${PLANTUML_VERSION}.jar

RUN TARGETARCH=$(arch | sed s/aarch64/arm64/ | sed s/x86_64/amd64/) && \
    curl -o /tmp/drawio.deb -L \
        https://github.com/jgraph/drawio-desktop/releases/download/v$DRAWIO_VERSION/drawio-$TARGETARCH-$DRAWIO_VERSION.deb \
    && dpkg -i /tmp/drawio.deb \
    && rm /tmp/drawio.deb

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 311
RUN ln -s /usr/bin/python3 /usr/bin/python

ENV PIPX_HOME=/opt/pipx \
    PIPX_BIN_DIR=/usr/local/bin

RUN pipx ensurepath
RUN pipx install poetry==${POETRY_VERSION}

USER ubuntu
RUN poetry config virtualenvs.in-project true
