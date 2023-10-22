FROM python:3.12.0

WORKDIR /app
ADD . /app
RUN pip3 install .

ENTRYPOINT ["70mai-m300-toolbox"]
