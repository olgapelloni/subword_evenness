import json
import os
from collections import defaultdict
import pandas as pd

path = "../mt5_test_results/"
output = "../mt5_test_summary.csv"

results = defaultdict(dict)

for root, dirs, files in sorted(os.walk(path)):
    for f in sorted(files):
        filepath = os.path.join(root,f)
        _, _, language, file = filepath.split(os.sep)
        # print(file)
        print(language)
        test_lang = ''
        losses = []
        if "eval" not in file:
            with open(filepath, "r") as fp:
                for line in fp.readlines():
                    data = json.loads(line)
                    losses. append(data["eval_loss"])
                    test_lang = data["eval_lang"]
        
        results[language][test_lang] = sum(losses)/len(losses)

print(json.dumps(results, indent=2))
df = pd.DataFrame.from_dict(results)
df.to_csv(output)