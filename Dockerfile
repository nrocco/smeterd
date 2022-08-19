# syntax = docker/dockerfile:1-experimental
FROM --platform=linux/amd64 alpine:edge AS pybase
RUN apk add --no-cache \
        ca-certificates \
        git \
        python3 \
        py3-pip \
        py3-wheel \
        py3-twine \
    && true
RUN python3 -m pip install \
        build \
        flake8 \
        pytest \
        pytest-cov \
    && true
WORKDIR /src
