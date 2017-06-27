FROM  bootstrapper:5000/liuqs_public/tensorflow:1.1.0-gpu

COPY requirements.txt /tmp/
COPY sources.list /etc/apt
RUN apt-get update && apt-get install -y vim git

RUN pip install -r /tmp/requirements.txt

