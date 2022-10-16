import random
import csv
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split

path = ".../lang_transfer_sets/"

train = path + "train/"
val = Path(path + "valid/")
meta = Path(path + "meta/train+valid_meta/")

val.mkdir(parents=True, exist_ok=True)
meta.mkdir(parents=True, exist_ok=True)

sentences = open(Path(train + "eng_full.txt"), 'r').readlines()
sentences_meta = open(str(meta) + "/eng_full_meta.csv", 'r').readlines()

tr_inputs, val_inputs, meta_train, meta_val = train_test_split(
    sentences, sentences_meta[1:], test_size=0.20, random_state=42)


with open(Path(train + "eng_train.txt"), "w") as out1, open(Path(str(val) + "/eng_valid.txt"), "w") as out2:
    for line1 in tr_inputs:
        out1.write(line1)

    for line2 in val_inputs:
        out2.write(line2)


with open(str(meta) + "/eng_train_meta.csv", "w", newline='') as out1, open(str(meta) + "/eng_valid_meta.csv", "w", newline='') as out2:
    writer1 = csv.writer(out1)
    writer2 = csv.writer(out2)

    writer1.writerow(["line", "file_name", "genre"])
    writer2.writerow(["line", "file_name", "genre"])

    for line1 in meta_train:
        writer1.writerow(line1)

    for line2 in meta_val:
        writer2.writerow(line2)
