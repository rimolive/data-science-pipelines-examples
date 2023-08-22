# from registry.access.redhat.com/ubi9/python-39
from quay.io/rmartine/python:3.9-alpine

USER root

RUN apk update && \
    apk add make automake gcc g++ subversion python3-dev gfortran openblas-dev && \
    pip install pandas && \
    pip install scikit-learn
