from collections import defaultdict
import json
import re
import os

path = "../mt5_test_results"

new_dict = defaultdict(dict)
counter = 0
test_lang = re.compile(r"eval_test_results_on_(.+).json")

for root, dirs, files in os.walk(path):
    for file in files:
        file = os.path.join(root,file)

        with open(file,"r") as fp:
            _, _, language, file = file.split(os.sep)
            if os.path.isdir(path + "/" + language + "2/") == False:
                os.mkdir(path + "/" + language + "2/")

            outfile = path + "/" + language + "2/" + file
            print(outfile)
            data = fp.read()

            data = data.replace("}{", "}\n{")

            with open(outfile, "w") as outf:
                outf.write(data + "\n")