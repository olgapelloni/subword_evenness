langs=("basque" "english" "finnish" "hebrew_modern" "hindi" "indonesian" "japanese" "korean" "mandarin" "persian" "russian" "spanish" "tagalog" "thai" "turkish" "vietnamese" "french" "german" "greek_modern")

for j in 1
do

echo ${j}

for i in ../data/train/*train.txt

do
#  extract language variable from file name in two steps
one=${i#*/train/}
lang=${one%*_*}

if [[ ${langs[*]} =~ ${lang} ]];

then

echo ${lang}

export TRAIN_FILE=../data/train/${lang}_train.txt
export VALID_FILE=../data/valid/${lang}_valid.txt
export NUM_GPUS=1

python3 t5_run_mlm_flax.py \
    --model_type=t5 \
    --model_name_or_path=google/mt5-base \
    --tokenizer_name=google/mt5-base \
    --train_file=$TRAIN_FILE \
    --validation_file=$VALID_FILE \
    --learning_rate=3e-5 \
    --output_dir=../mt5_models/${lang}/${j} \
    --max_seq_length=256 \
    --do_train \
    --do_eval \
    --overwrite_output_dir \
    --eval_steps=200 \
    --total_steps=2000 \
    --per_device_train_batch_size="8" \
    --per_device_eval_batch_size="8" \
    --trial=${j} \
    --seed=${j}${j}

fi

done
done
