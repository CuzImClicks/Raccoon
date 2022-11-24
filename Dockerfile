FROM "tensorflow/tensorflow"

WORKDIR /home

RUN mkdir models

WORKDIR ./models

RUN mkdir input
RUN mkdir output
RUN mkdir object_detection

RUN apt-get -y update

RUN apt-get install -y protobuf-compiler python-pil python-lxml

RUN pip install matplotlib

# Copy resources
COPY repo/centernet_hg104_1024x1024_coco17_tpu-32 ./centernet_hg104_1024x1024_coco17_tpu-32
COPY repo/mscoco_label_map.pbtxt .
COPY repo/object_detection ./object_detection
COPY plot_object_detection_saved_model.py .
COPY repo/tensorflow-2.12.0-cp38-cp38-linux_x86_64.whl .

# Run protobuf compiler
RUN protoc ./object_detection/protos/*.proto --python_out=.
RUN export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

# Install custom tensorflow (no-avx, no-gpu)
RUN python -m pip install tensorflow-2.12.0-cp38-cp38-linux_x86_64.whl
RUN python -c 'import tensorflow as tf; msg = tf.constant("TensorFlow 2.0 Hello World"); tf.print(msg)' # validate installation