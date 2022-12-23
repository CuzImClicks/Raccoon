# Raccoon Object Detector
Raccoon is a TensorFlow based application designed to recognize people on video feeds.
It uses the latest version of TensorFlow and is hosted on a custom Docker system 
consisting of multiple different Docker images. The object detector is trained on a 
custom dataset of approximately 1000 annotated images hosted at https://universe.roboflow.com/cuzimclicks/raccoon-qnjzn. 
The dataset contains three different classes and has been resized to 640x640.

## Dependencies
- Docker

## Installation
To use Raccoon, you will need to install TensorFlow. You can then clone the repository from GitHub using the following command:
```
git clone https://github.com/CuzImClicks/Raccoon.git
```

## Usage
To use Raccoon, you will need to provide it with an input image or video stream. The object detector will then return the bounding boxes and labels for any detected objects.

You can run the object detection script using the following command:

```
python plot_object_detection_saved_model.py
```
For more options, you can use the following command to view the available arguments:

```
python examples/detect_image.py --help
```

## Training
To train the object detector, you will need to use the custom dataset of annotated images hosted at https://universe.roboflow.com/cuzimclicks/raccoon-qnjzn. This can be done using the TensorFlow training API. Make sure to specify the three different classes and that the images have been resized to 640x640.

## Hosting
Raccoon can be hosted using a custom Docker system consisting of multiple different Docker images, which are hosted at Docker Hub:

> TensorFlow

The first version of this object detector, which is very accurate but slow on low-performance CPUs/GPUs
> Edge TPU

the Edge TPU version of this object detector, which is quick but has low accuracy
> Compiler
 
comes with the Edge TPU compiler preinstalled

<details>
<summary>Vanilla TensorFlow</summary>
Build the docker image

`docker build -t my-name/my-image .`

Run the docker image

`docker run --rm -i -t my-name/my-image bash`

In the bash command line run to start the program

`python plot_object_detection_saved_model.py`

To copy something(the final images) to or from a docker container

```bash
docker ps
docker cp <file path> <container id>:<destination path>
```
</details>

## TensorFlow (no-avx, no-gpu)
https://github.com/yaroslavvb/tensorflow-community-wheels/issues/217

[Download](https://doc-0s-a0-docs.googleusercontent.com/docs/securesc/5f65sii56chced822u4lor2pbohefi4i/dva7se5p115uie0jdv1es1sq2nkbucai/1670197125000/10382843425728757322/17942727790113938602/1T3WrRsiKBBqZn-LRaBQL6ulAQM-Unh3G?e=download&ax=AEKYgyStt5G864Wti50Rt5YGAAhdZ71dbTiVafx_QmB_LpttIVvxOsr8EBiN_nq49pZoHOSlhZlRLJ07uix14YCqnFR3gJ5aVoPcXolv_Lb0quTC7Gi9Ah-sqSlxc-dEVZ9AWTPGEp-X9n2Y8z9J0T-kjkQ4LzmbOvXYnzgtZVLjMW09EPUOcnVvL_P7zCv7GPi7kFnueyzu2nO_O5yszG5aqI2k3a8Sd9oCIQe9x8ojX-9cW8loPxWRc3xkn29-HEBIqr5qBUkOsFh2GQ4mHb3LWnBRKCfbdgnW4xLPRT88rr3SEL0cLjakX2F10_muHErek60jvFsAkylUTj5uwrhp1pQ0WnQWOEkMAlGLNgeNO5uC8EI1Y4fJJUyyaUQzY-2d_seiXwKxK5IbDsbGFnl1jxc8psC_WJhgBhynCsRrYSqNdDoXc0vXzwqvi2ED1BdL5FFwaITa405fIysYFRcAFcd7scL8vT1ekE0q5GT_J7K0duUL2k13y_7gLRJqhG8JS_xwreCY_AJRpAU8iRNyApYhnDXHDAkTdPHXgRBkaUODA33HKa3R32NpPAKZl5HuzN6GXHb-ERhLLIJF1rGFmXWko2uwkg8x2f5UErlA2Z6kRC10_ILsoEZnUVK2nmDVQRZrOxaWzRJIEa0HAKZJBc5NOdxtVDp1w_jOf-gN_1ZVJRTrzG9qKkY8GeNbYLBLnMFo0EBevT7ZtBCpqMFr2_tOCjXvhhRBepWHu4hanYymUOg8YVGri6kM7fTPMxb8h9eGedCLBplBd0vtZVJ-6twZVmYzKiUTWJqC5Y8B7NFsZbK8hF6obBTNDTQ1o5p_XZaUcnvXUOPL_EjoeOqTUnAQcDzA3at1R2okHOg85M8QEnnWfDu5GXV9BHVOrHZtDw&uuid=57e82a88-77a8-4b34-9c99-9c27b95c2048&authuser=0&nonce=uekp1hobqnm68&user=17942727790113938602&hash=hqbmb2jn1aal1v49ct94b73fqd3h61ag)


## Docker
Run the same container again

`docker container ps -a`

Find the container you want

` docker exec -it <CONTAINER_ID> bash`

## Locations
Input folder for copying with pull.sh
>/share/Henrik/input

Output folder for copying with push.sh 
>/share/Henrik/output

Location of the converted YOLOV7 model
>/share/Henrik/yolov7_model.tflite

Location of the security camera alarm images
>/share/Public/record_nvr_images

## Converting a model to tflite
```
tflite_convert --[keras_model_file|saved_model_dir]<input> --output_file=<file>
```




## TODO:
- [ ] train own dataset
- [x] dockerize for deployment
- [ ] code quality with codacy
- [x] tensorflow
- [ ] pr based contributing
- [ ] discord webhook for results

<details>
<summary>Links</summary>

### Problems

> '${\r' command not found
-> apt install dos2unix

### Links
<details>
<summary>usbipd</summary>

[usbipd docs](https://github.com/dorssel/usbipd-win)
[WSL support](https://github.com/dorssel/usbipd-win/wiki/WSL-support)
[Docker on wsl does not like having fun](https://github.com/dorssel/usbipd-win/issues/264)
</details>

<details>
<summary>YOLO V7</summary>

[Converting YOLO V7](https://medium.com/geekculture/converting-yolo-v7-to-tensorflow-lite-for-mobile-deployment-ebc1103e8d1e)

[Converting TensorFlow model to Edge TPU model](https://coral.ai/docs/edgetpu/models-intro)

[Converting TensorFlow models to Tflite](https://www.tensorflow.org/lite/models/convert)

[jveitchmichaelis/edgetpu-yolo](https://github.com/jveitchmichaelis/edgetpu-yolo)

[EdgeTPU Compiler](https://coral.ai/docs/edgetpu/compiler/)
</details>

<details>
<summary>Retraining models</summary>

[Retraining TensorFlow models](https://blog.tensorflow.org/2021/07/real-world-ml-with-coral-manufacturing.html)

[Retrain EdgeTPU model](https://coral.ai/docs/edgetpu/retrain-detection/)
</details>

<details>
<summary>List of Models</summary>

[List of EdgeTPU compatible models](https://coral.ai/models/object-detection/)

[TensorFlow Hub](https://tfhub.dev/s?module-type=image-object-detection)
</details>


</details>