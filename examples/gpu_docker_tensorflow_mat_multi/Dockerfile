FROM bootstrapper:5000/liuqs_public/tensorflow:1.1.0-gpu 

RUN mkdir /examples
COPY test.py /examples/

WORKDIR /examples

CMD ["python","./test.py"]
