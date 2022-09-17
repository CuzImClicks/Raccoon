#!/usr/bin/env python
# coding: utf-8
"""
Object Detection From TF2 Saved Model
=====================================
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # Suppress TensorFlow logging (1)
import pathlib
import tensorflow as tf

tf.get_logger().setLevel('ERROR')           # Suppress TensorFlow logging (2)

print("_"*20)
print(f"CuzImClicks/Raccoon Image Detection")
print("\n")
print(os.getcwd())
production = bool(os.environ.get("PRODUCTION"))
print(f"production set to: {production}")

# Enable GPU dynamic memory allocation
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

def download_images():
    base_url = 'https://garagenparkhalle.de/sites/default/files/Analyse/'
    filenames = ["image4.jpg", "image5.jpg", "image6.jpg", 'image7.jpg', 'image8.jpg', 'image9.jpg', 'image10.jpg']
    image_paths = []
    for filename in filenames:
        image_path = tf.keras.utils.get_file(fname=filename,
                                            origin=base_url + filename,
                                            untar=False)
        image_path = pathlib.Path(image_path)
        image_paths.append(str(image_path))
    return image_paths

#IMAGE_PATHS = download_images()
#print("Downloaded Images")

# Download and extract model
def download_model(model_name, model_date):
    base_url = 'http://download.tensorflow.org/models/object_detection/tf2/'
    model_file = model_name + '.tar.gz'
    model_dir = tf.keras.utils.get_file(fname=model_name,
                                        origin=base_url + model_date + '/' + model_file,
                                        untar=True)
    return str(model_dir)

MODEL_DATE = '20200711'
MODEL_NAME = 'centernet_hg104_1024x1024_coco17_tpu-32'
PATH_TO_MODEL_DIR = download_model(MODEL_NAME, MODEL_DATE)
print("Downloaded Model")

# Download labels file
def download_labels(filename):
    base_url = 'https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/'
    label_dir = tf.keras.utils.get_file(fname=filename,
                                        origin=base_url + filename,
                                        untar=False)
    label_dir = pathlib.Path(label_dir)
    return str(label_dir)

LABEL_FILENAME = 'mscoco_label_map.pbtxt'
PATH_TO_LABELS = download_labels(LABEL_FILENAME)
print("Downloaded Labels")

# Load the model
# Next we load the downloaded model
import time
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils

PATH_TO_SAVED_MODEL = PATH_TO_MODEL_DIR + "/saved_model"
print('Loading model...')
start_time = time.time()

detect_fn = tf.keras.models.load_model(PATH_TO_SAVED_MODEL)

# Load saved model and build the detection function
#detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)

end_time = time.time()
elapsed_time = end_time - start_time
print('Done! Took {} seconds'.format(elapsed_time))


# Load label map data (for plotting)
# Creates a dictionary of { "1": "person" }
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS,
                                                                    use_display_name=True)

print(f"Loaded category index")
print(category_index)

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')   # Suppress Matplotlib warnings

def load_image_into_numpy_array(path):
    """Load an image from file into a numpy array.

    Puts image into numpy array to feed into tensorflow graph.
    Note that by convention we put it into a numpy array with shape
    (height, width, channels), where channels=3 for RGB.

    Args:
      path: the file path to the image

    Returns:
      uint8 numpy array with shape (img_height, img_width, 3)
    """
    return np.array(Image.open(path))

def computeAndSaveImages(images: list) -> None:
    """Computes every image in a list of file paths, runs it through tensorflow and draws the boxes on them

    Args:
        images (list): A list of file paths to the images that are to be computed
    """

    for image_path in images:
        print(f'Running inference for {image_path}... ')

        image_np = load_image_into_numpy_array(image_path)

        input_tensor = tf.convert_to_tensor(image_np)
        input_tensor = input_tensor[tf.newaxis, ...]

        detections = detect_fn(input_tensor)

        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy()
                    for key, value in detections.items()}
        detections['num_detections'] = num_detections

        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
        contains_person = False
        for index, value in enumerate(detections["detection_classes"]):
            if value == 1 and detections["detection_scores"][index] > 0.3:
                contains_person = True

        if not contains_person and production:
            print(f"No person found in image")
            continue

        important = {f"{category_index[det]['name']}#{index}": detections["detection_scores"][index] for index, det in enumerate(detections["detection_classes"]) if detections["detection_scores"][index] > 0.3}
        print(f"Findings for {image_path}")
        print(important)
        
        image_np_with_detections = image_np.copy()

        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes'],
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=200,
            min_score_thresh=.30,
            agnostic_mode=False)

        plt.figure()
        plt.imshow(image_np_with_detections)
        
        (dirname, filename) = os.path.split(image_path)
        new_image_path = "./output"+'/new_'+filename
        print(new_image_path)
        plt.savefig(new_image_path)
        print("\n")

if __name__ == "__main__":
    print("Started the listener")
    while True:
        try:
            new_files = os.listdir("./input")
            if len(new_files) > 0:
                print("New files found")
                new_files = [f"./input/{f}" for f in new_files if f.endswith(".jpg")]
                print(new_files)
                computeAndSaveImages(new_files)
                for f in new_files:
                    print(f"Deleted the source file for {f}")
                    os.remove(f"{f}")

                print("\n"*2)
            
            else:
                print("Waiting for new files")

            time.sleep(10)

        except Exception as e:
            print(e)

print('Done')
plt.show()


# sphinx_gallery_thumbnail_number = 2