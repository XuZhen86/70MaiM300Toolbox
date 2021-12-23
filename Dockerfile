FROM python:slim
ARG DEBIAN_FRONTEND=noninteractive

RUN pip install absl_py requests

ADD 70maim300toolbox.py /
