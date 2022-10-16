# Process all 19 languages
# Tokenize, apply BPE, clump single characters, count lengths, UI, variance
# Store the whole table in each language folder

import csv
import os
import re, regex
import sys
import unicodedata
import statistics
from subprocess import call
from polyglot.text import Text


def tokenize(line):
    RE_BAD_CHARS = regex.compile(r"\p{Cc}|\p{Cs}")

    def remove_bad_chars(text):
        return RE_BAD_CHARS.sub("", text)

    new_line = remove_bad_chars(line)
    text = Text(new_line)

    try:
        tokens = text.words
    except ValueError:
        tokens = []
    return tokens


def remove_punctuation(text):
    tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                        if unicodedata.category(chr(i)).startswith('P'))
    return text.translate(tbl)


def clump_bpe(segmented, substituted):
    segments = []
    with open(segmented, 'r') as f_segments:
        for line in f_segments:
            segments.append(line.strip())

    result = []
    for word in segments:
        new_word = word

        start = re.search('^[^@]@@( [^@]@@)+', new_word)
        if start:
            new_start = start.group(0).replace('@@ ', '')
            new_word = new_word.replace(start.group(0), new_start)

        middle = re.findall(' ([^@]@@)(( [^@]@@)+)( [^@]$)?', new_word)
        if len(middle) > 0:
            for item in middle:
                new_item = (item[0] + item[1] + item[3]).replace('@@ ', '')
                new_word = new_word.replace(item[0] + item[1] + item[3], new_item)

        end = re.search('(^| )[^@]@@ [^@]$', new_word)
        if end:
            new_end = end.group(0).replace('@@ ', '')
            new_word = new_word.replace(end.group(0), new_end)

        result.append(new_word)

    # Replace all @@ symbols
    result = [segment.replace('@@ ', '|') for segment in result]

    with open(substituted, 'w') as f:
        for word in result:
            f.write(word + '\n')


def count_lengths_ui(segments):
    segments_lengths = []

    max_seg = -1
    min_seg = 1000
    for seg in segments:
        segments_lengths.append(len(seg))

    for seg_len in segments_lengths:
        if int(seg_len) > max_seg:
            max_seg = int(seg_len)
        if int(seg_len) < min_seg:
            min_seg = int(seg_len)

    index = max_seg - min_seg
    return segments_lengths, index


def count_variance(segments):
    int_seq = []
    for s in segments:
        int_seq.append(int(s))

    if len(int_seq) > 1:
        variance = statistics.variance(int_seq)
    else:
        variance = 'NA'
    return variance


def find_files(start, pattern):
    all_lang_results = []
    for root, dirs, files in os.walk(start):
        for file in files:
            if pattern in file:
                all_lang_results.append(os.path.join(root, file))
    return all_lang_results


def main():
    # generate sh files for BPE
    print('BPE-MIN-R')
    
    with open('../train/bpe-min-r/learn-bpe.sh', 'w') as f_learn_bpe:
        with open('../train/bpe-min-r/apply-bpe.sh', 'w') as f_apply_bpe:
            for root, dirs, files in os.walk('../train/'):
                for file in files:
                    if file.endswith('full.txt'):
                        print(file)
                        file_codes = '../train/bpe-min-r/' + file[:-9] + '_codes.txt'
                        file_segm = '../train/bpe-min-r/' + file[:-9] + '_segmented.txt'

                        # the number 200 has to be adjusted to different languages
                        learn_line = 'subword-nmt learn-bpe -s 200 < ' + \
                                     os.path.join(root, file) + ' > ' + file_codes
                        apply_line = 'subword-nmt apply-bpe -c ' + file_codes + \
                                     ' < ' + os.path.join(root, file) + ' > ' + file_segm
                        print(learn_line)
                        print(apply_line)
                        f_learn_bpe.write(learn_line + '\n')
                        f_apply_bpe.write(apply_line + '\n')
    
    # learn bpe 200 codes; this is recommended to be run separately in the terminal!
    call('../train/bpe-min-r/learn-bpe.sh', shell=True)
    
    # apply bpe 200; this is recommended to be run separately in the terminal!
    call('../train/bpe-min-r/apply-bpe.sh', shell=True)

    for mode in ['bpe-min-r']:
        for root, dirs, files in os.walk('../train/'):
            for file in files:
                if file.endswith('full.txt'):
                    print(file)
                    segmented_file = os.path.join('../train/' + mode + '/' + file[:-9] + '_segmented.txt')
                    print(segmented_file)

                    if mode == 'bpe-min-r':
                        clump_bpe(segmented_file, substituted_file)

                    with open(results_file, 'w', newline='') as sequences_results:
                        seq_writer = csv.writer(sequences_results, delimiter='\t')
                        seq_writer.writerow(['word_split', 'segments_lengths', 'word_length',
                                             'index', 'variance', 'word',
                                             'file', 'genre', 'language'])
                        lang = file[:-9]
                        genre = 'na'

                        with open(substituted_file, 'r') as f:
                            for line in f:
                                word_split = line.strip()
                                segments = line.strip().split('|')
                                word = ''.join(segments)
                                segments_lengths, index = count_lengths_ui(segments)
                                variance = count_variance(segments_lengths)

                                seq_writer.writerow([word_split, segments_lengths, len(word),
                                                     index, variance, word,
                                                     file, genre, lang])


if __name__ == '__main__':
    main()
