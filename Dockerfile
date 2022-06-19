FROM python:3.10-alpine

WORKDIR /app
ADD . /app
RUN pip3 install .

ENTRYPOINT ["70mai-m300-toolbox"]
