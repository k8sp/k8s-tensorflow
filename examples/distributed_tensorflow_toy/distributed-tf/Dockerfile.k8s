FROM bootstrapper:5000/liuqs_public/tensorflow:1.1.0-gpu

RUN mkdir /examples
COPY train.py run-gpu.sh /examples/
WORKDIR /examples

CMD ["./run-gpu.sh"]
