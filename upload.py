
from roboflow import Roboflow
import argparse
import os
from threading import Thread
import time
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("--api_key", type=str, required=True)
parser.add_argument("--project", type=str, required=True)
parser.add_argument("--sleep", type=float, required=True)

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


def upload(file):
    bar.set_description(f"Uploading {file}")
    bar.refresh()
    project.upload(file)
    bar.update()
    bar.refresh()
    bar.set_description(f"Finished uploading file {file}")


for index, file in enumerate(files):
    Thread(target=upload, args=[file]).start()
    bar.refresh()
    time.sleep(args.sleep)
