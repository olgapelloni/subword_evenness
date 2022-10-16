# Subword Evenness (SuE)

Repository for the paper:

Olga Pelloni, Anastassia Shaitarova and Tanja Samardzic (2022). Subword Evenness (SuE) as a Predictor of Cross-lingual Transfer to Low-resource Languages, EMNLP 2022.


## Data

Data comes from the TeDDi Sample (link) corpus. We create 1M tokens balanced datasets for 19 training languages and 200K tokens datasets for 30 test languages.

Links:
- Train dataset
- Valid dataset
- Test dataset

## Scripts

Most of the scripts are done by me and Anastassia Shaitarova. Scripts for continuous training/fine-tuning are taken and adapted from HuggingFace. Script for measuring TTR and unigram entropy comes from Ximena Gutierrez.

## Results

Link:
- Files segmented by BPE (minimum redundancy approach)
- Tables with UI measured on each word