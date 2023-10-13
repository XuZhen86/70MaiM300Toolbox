FROM python:3.11.6

WORKDIR /app
ADD . /app
RUN pip3 install .

ENTRYPOINT ["70mai-m300-toolbox"]
