import re
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("metrics", nargs="+", type=str, choices=["learning_rate", "loss", "time_per_step", "det_loss", "cls_loss", "box_loss", "reg_l2_loss", "gradient_norm", "val_loss", "val_det_loss", "val_cls_loss", "val_reg_l2_loss", "val_box_loss"])
parser.add_argument("--input", "-i", nargs="+", type=str, default="data.txt", required=False)
parser.add_argument("--output", "-o", type=str, default="graph.png", required=False)
parser.add_argument("--end", action="store_true", required=False)
parser.add_argument("--lowest", action="store_true", required=False)

args = parser.parse_args()

line_regex = r"Epoch (?P<epoch>\d+)\/\d+\n\d+\/\d+ \[=+\] - (?P<time>\d+)s (?P<time_per_step>\d+)ms\/step - det_loss: (?P<det_loss>\d+\.\d+) - cls_loss: (?P<cls_loss>\d+\.\d+) - box_loss: (?P<box_loss>\d+\.\d+) - reg_l2_loss: (?P<reg_l2_loss>\d+\.\d+) - loss: (?P<loss>\d+\.\d+) - learning_rate: (?P<learning_rate>\d+\.\d+(e-\d+)?) - gradient_norm: (?P<gradient_norm>\d+\.\d+)"

line_regex_val = r"Epoch (?P<epoch>\d+)\/\d+\n\d+\/\d+ \[=+\] - (?P<time>\d+)m?s? (?P<time_per_step>\d+)m?s?\/step - det_loss: (?P<det_loss>\d+.\d+) - cls_loss: (?P<cls_loss>\d+.\d+) - box_loss: (?P<box_loss>\d+.\d+) - reg_l2_loss: (?P<reg_l2_loss>\d+.\d+) - loss: (?P<loss>\d+.\d+) - learning_rate: (?P<learning_rate>\d+.\d+(e-\d+)?) - gradient_norm: (?P<gradient_norm>\d+.\d+) - val_det_loss: (?P<val_det_loss>\d+.\d+) - val_cls_loss: (?P<val_cls_loss>\d+.\d+) - val_box_loss: (?P<val_box_loss>\d+.\d+) - val_reg_l2_loss: (?P<val_reg_l2_loss>\d+.\d+) - val_loss: (?P<val_loss>\d+.\d+)\n"

def generate_data(data: str):
    return [{ "epoch": int(match[0]), "time": int(match[1]), "time_per_step": int(match[2]), "det_loss": float(match[3]), "cls_loss": float(match[4]), "box_loss": float(match[5]), "reg_l2_loss": float(match[6]), "loss": float(match[7]), "learning_rate": float(match[8]), "gradient_norm": float(match[10]) } for match in  re.findall(line_regex_val, data)]


def generate_data_val(data: str):
    return [{ "epoch": int(match[0]), "time": int(match[1]), "time_per_step": int(match[2]), "det_loss": float(match[3]), "cls_loss": float(match[4]), "box_loss": float(match[5]), "reg_l2_loss": float(match[6]), "loss": float(match[7]), "learning_rate": float(match[8]), "gradient_norm": float(match[10]), "val_det_loss": float(match[11]), "val_cls_loss": float(match[12]), "val_box_loss": float(match[13]), "val_reg_l2_loss": float(match[14]), "val_loss": float(match[15]) } for match in re.findall(line_regex_val, data)]


files = [open(file, "r").read() for file in args.input]
files = [generate_data(file) if not "val_loss" in file else generate_data_val(file) for file in files]

import matplotlib.pyplot as plt

def add_graph(plt, data: dict, name: str, draw_end=False, draw_lowest=False):
    values = [float(match[name]) for match in data]
    plt.plot(range(1,  int(data[-1]["epoch"]) + 1), values, label = name)
    if draw_end:
        last = values[-1]
        plt.axhline(y=last)
        plt.annotate(text=str(last), xy=(values.index(last), last) )
    
    if draw_lowest:
        lowest = min(values)
        lowest_x = values.index(lowest)
        plt.axhline(y=lowest)
        plt.annotate(text=f"{lowest} | {lowest_x}", xy=(lowest_x, lowest))

for metric in args.metrics:
    for file in files:
        add_graph(plt, file, metric, args.end, args.lowest)

plt.legend(loc="upper right")
plt.xlabel("Epoch")
if any(["loss" in metric for metric in args.metrics]):
    plt.ylabel("Loss")
plt.savefig(args.output)
 
