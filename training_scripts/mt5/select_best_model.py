from collections import defaultdict
from email.policy import default
from genericpath import exists
import json 
import os
import re

path = "../mt5_models"
output = "../mt5_model_summary.json"

results = defaultdict(dict)

filelist = []

for root, dirs, files in os.walk(path):
    for file in files:
        filelist.append(os.path.join(root,file))

for f in filelist:
    if "eval_results" in f:
        _, _, language, name, file = f.split(os.sep)
        # print(language, name, file)
        with open(f, "r") as fp:
            results[language][name] = json.loads(fp.read())


for language, models in results.items():
    best_model = min(({"key": k, "model": m} for k, m in models.items()), 
    key=lambda m: m["model"]["eval_loss"])

    models["best"] = best_model["key"]

if exists(output):
    with open(output,"r") as fp:
        old_dict = json.loads(fp.read())
        results.update(old_dict)

with open(output, "w") as f:
    json.dump(results, f, indent=4, sort_keys=True)

print(json.dumps(results, indent=2))
