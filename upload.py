
import base64
from roboflow import Roboflow
import argparse
import os
from threading import Thread
import time
from tqdm import tqdm
import requests

parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("--api_key", type=str, required=True)
parser.add_argument("--project", type=str, required=True)
parser.add_argument("--lock", type=int, default=10)
parser.add_argument("--wait", type=float, default=1.0)

args = parser.parse_args()

if not os.path.exists(args.file):
    parser.error(f"The file {args.file} does not exist!")

files = [os.path.join(args.file) + file for file in os.listdir(args.file)] if os.path.isdir(args.file) else [
    args.file, ]
files = [file for file in files if file.split(".")[-1].lower() in ("jpg", "jpeg", "png", "bmp", "mov", "mp4")]

rf = Roboflow(api_key=args.api_key)
workspace = rf.workspace()
project = workspace.project(args.project)

bar = tqdm(files, unit="images", desc="Starting Upload")

url = lambda project, api_key, name: f"https://api.roboflow.com/dataset/{project}/upload?api_key={api_key}&name={name}"

# add a prevention mechanism that prevents more than ten images at a time from being uploaded and waits for one to finish before starting another


def upload(file):
    bar.set_description(f"Uploading {file}")
    bar.refresh()
    lock.append(file)
    requests.post(url(args.project, args.api_key, os.path.basename(file)),
                             data=base64.b64encode(open(file, "rb").read()), headers={"content-type": "text/plain"})
    bar.update()
    bar.refresh()
    lock.remove(file)
    bar.set_description(f"Finished uploading file {file}")


lock = []

for index, file in enumerate(files):
    Thread(target=upload, args=[file]).start()
    bar.refresh()
    while len(lock) > args.lock:
        time.sleep(args.wait)
