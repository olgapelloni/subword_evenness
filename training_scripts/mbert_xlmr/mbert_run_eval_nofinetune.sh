for i in ../lang_transfer_sets/test/*.txt

do

one=${i#*/test/}
lang=${one%*.*}

echo $lang

export TEST_FILE=../lang_transfer_sets/test/${lang}.txt
export EVAL_RESULTS=../results/mbert_nofinetune.csv

python3 eval_separately.py \
    --eval_results_path=$EVAL_RESULTS \
    --model_type=bert \
    --model_name_or_path=bert-base-multilingual-cased \
    --tokenizer_name=bert-base-multilingual-cased \
    --validation_file=$TEST_FILE \
    --learning_rate=3e-5 \
    --per_device_train_batch_size=4 \
    --gradient_accumulation_steps=32 \
    --language=$lang

done
