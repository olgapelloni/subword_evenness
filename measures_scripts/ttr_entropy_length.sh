########################################################################################################
#Script for simply calculating unigram word entropy TTR, Hrcross, redundancy of a text (each word separated by space)
####################################################################################################

input_corpus=lang_transfer_sets/full_train
mode=tokens
output="$input_corpus"_"$mode"
echo "File	Avg_length	median_length	Char_types	Types	Tokens	TTR	H">../"$output".stats.tsv

for f in `ls ../"$input_corpus"/`;
do
	echo "Processing $f"

	echo -n "$f	">>../"$output".stats.tsv
	if [ "$mode" = tokens ]
	then
		python3 measures_ttr_python.py ../$input_corpus/"$f" 0  >>../"$output".stats.tsv

	fi
done

echo "DONE. See ../$input_corpus.stats.tsv"