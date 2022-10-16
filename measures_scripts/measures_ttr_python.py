###Input: A textfile and size of the sample (if 0 it will take de whole text)
###Output: It prints a line containing the following measures for the input text: mean word length, median word length, char types, word types, word tokens, TTR, H
##To run this over a whole corpus (many files in a folder) use the *.sh scripts
#######################################################################################################################33


from __future__ import division
from collections import defaultdict, Counter
from itertools import chain
from re import escape, compile
# import matplotlib.pyplot as plt
import numpy as np
import sys
from re import sub
import random
import statistics
from polyglot.text import Text
from segments import Profile, Tokenizer

def get_chunks(s, maxlength):
    start = 0
    end = 0
    while start + maxlength  < len(s) and end != -1:
        end = s.rfind(" ", start, start + maxlength + 1)
        yield s[start:end]
        start = end +1
    yield s[start:]

inputcorpus = sys.argv[1]
samplesize = int(sys.argv[2])
myfile = open(inputcorpus, 'r', encoding="utf-8")
sample_text = myfile.read()  # tokens (orderes is preserved)
punctuation = ["!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?",
               "@", "[", "]", "^", "_", "`", "{", "}", "~", "]", "¿", "»", "«", "“", "”", "¡", "،"]
strings_clean_aux = []
strings_clean = []
t = Tokenizer()

for p in punctuation:  # Filter some common punctuation marks.
    sample_text = sample_text.replace(p, "")

# Make bigger chunks
chunks = get_chunks(sample_text, 1000)

for chunk in chunks:
    text = Text(chunk)  ##Polyglot object
    # if len(text)>0: #Otherwise Polyglot shows an error in empty strings
    try:
        tokenized_words = text.words  # Polyglot (orthograahic word boundaries)
    except:
        # tokenized_words = []
        tokenized_words = chunk.split()  # In case buggy polyglot finds something non utf-8 and it breaks the whole pipeline

    for s in tokenized_words:
        # print(s)
        if (len(s) == 1) and (
                s.isalnum() == False):  # UPDATE: For punctuation not detected in the predefined list. In cases we have a word (size 1) and it's not alphanumeric.
            continue  # we skip this token
        strings_clean_aux.append(s.lower())

textsize = len(strings_clean_aux)
if (textsize <= samplesize):  # very few text not enough for the sample, we take everything
    samplesize = textsize

max_number = textsize - samplesize  # upper bound of random number from which the windows of words will start (sampling)
if (samplesize == 0):  # No sampling
    strings_clean = strings_clean_aux
else:

    # For contiguous text:
    n = random.randint(0, max_number)
    strings_clean = strings_clean_aux[n:(n + samplesize)]

# strings_clean=random.sample(strings_clean_aux, samplesize)

# print(strings_clean)
# strings_clean = [sub(r'[^\w\s]','',w) for w in strings]
words = Counter(strings_clean)

types = len(set(strings_clean))
tokens = len(strings_clean)
ttr = types / tokens
total = 0;
char_freq = {}
sizes = []
for w in strings_clean:  ###Avg. word length of word Tokens###
    char_tokenized = t(w).split()  # Steve's library returns a string not a list so we do split()
    size = len(char_tokenized)
    total = total + size
    sizes.append(size)
    # print(w, 	char_tokenized, size)			#print (size)
    for i in char_tokenized:
        if i in char_freq:
            char_freq[i] += 1
        else:
            char_freq[i] = 1

avg = total / tokens  # Avg. word length
char_types = len(char_freq)
median = statistics.median(sizes)


def get_measures(voc,
                 filename):  # Just for getting the entropy  ---- update: (added frequencies printing in this function due to Chris's request)
    freq = defaultdict(int)
    myfile = open(filename, 'w', encoding="utf-8")
    ordered_voc = voc.most_common()
    for key, value in sorted(voc.items(), key=lambda item: item[1], reverse=True):
        if (key != ""):
            freq[key] += value
            freqpair = str(key) + "\t" + str(value) + "\n"
            myfile.write(freqpair)
    # print(freq)
    freq = np.array(list(freq.values()))
    # Probabilidad de los símbolos
    p = freq / freq.sum()
    # print (p)
    len_p = len(p)

    H = -(p * np.log2(p)).sum()  # entropy

    return H


# For Printing frequency file:
fileparts = inputcorpus.split("/")
# fileparts=fileparts[-2].split("/")

results = get_measures(words, (fileparts[-1] + ".freqs.tsv"))  # We extract entropy and also generates a frequency file:

# print(words)

print(str(avg) + "\t" + str(median) + "\t" + str(char_types) + "\t" + str(types) + "\t" + str(tokens) + "\t" + str(
    ttr) + "\t" + str(results))





