FROM bootstrapper:5000/liuqs_public/tensorflow:1.1.0-gpu 

RUN mkdir /examples
COPY ["list_gpu.py", "test.sh",  "/examples/"]
WORKDIR /examples

CMD ["./test.sh"]
