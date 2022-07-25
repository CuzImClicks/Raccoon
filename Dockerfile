FROM "tensorflow/tensorflow"

WORKDIR /home

RUN apt-get -y update
RUN apt-get -y install git

RUN apt-get install -y protobuf-compiler python-pil python-lxml

RUN pip install matplotlib

RUN git clone https://github.com/tensorflow/models/

WORKDIR ./models/research/

RUN protoc object_detection/protos/*.proto --python_out=.
RUN export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

COPY . .