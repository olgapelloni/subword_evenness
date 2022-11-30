# Subword Evenness (SuE)

Repository for the paper:

Olga Pelloni, Anastassia Shaitarova and Tanja Samardzic (2022). Subword Evenness (SuE) as a Predictor of Cross-lingual Transfer to Low-resource Languages, EMNLP 2022.


## Data

Data comes from the [TeDDi Sample corpus](https://github.com/MorphDiv/TeDDi_sample). We create 1M tokens balanced datasets for 19 training languages and 200K tokens datasets for 30 test languages.

Links to our datasets:
- [Train dataset](https://drive.switch.ch/index.php/s/rPCEnAHyTrXVAY1)
- [Valid dataset](https://drive.switch.ch/index.php/s/Lau2Y4vGgds8wtu)
- [Test dataset](https://drive.switch.ch/index.php/s/8HVSN2d2KIwffDR)

## Scripts

Most of the scripts are done by [Anastassia Shaitarova](https://github.com/shaitarAn) and me. Scripts for continuous training/fine-tuning are taken and adapted from [HuggingFace](https://github.com/huggingface). Scripts for measuring TTR and unigram entropy come from [Ximena Gutierrez-Vasques](https://github.com/ximenina). The number of BPE merges is calculated following the minimum redundancy approach [(Gutierrez-Vasques et al. 2021)](https://aclanthology.org/2021.eacl-main.302/) and using the scripts from the [paper repository](https://github.com/ximenina/theturningpoint). The resulting numbers of merges used for monolingual training on the 19 transfer languages are listed in the file ```measures_scripts/sue/num_bpe_merges.tsv```
