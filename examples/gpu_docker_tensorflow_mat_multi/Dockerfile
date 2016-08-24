FROM b.gcr.io/tensorflow/tensorflow:latest-gpu

RUN mkdir /examples
COPY test.py /examples/
WORKDIR /examples

CMD ["python","./test.py"]
