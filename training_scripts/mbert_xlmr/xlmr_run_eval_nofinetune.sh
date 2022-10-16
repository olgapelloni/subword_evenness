for k in 1 2 3 4 5
do

for i in ../lang_transfer_sets/test/*.txt
do

one=${i#*/test/}
lang=${one%*.*}

echo $lang

export TEST_FILE=../lang_transfer_sets/test/${lang}.txt
export EVAL_RESULTS=../results_xlmr/seed${k}/xlmr_nofinetune.csv

python3 eval_separately.py \
    --eval_results_path=$EVAL_RESULTS \
    --model_type=xlm-roberta \
    --model_name_or_path=xlm-roberta-base \
    --tokenizer_name=xlm-roberta-base \
    --validation_file=$TEST_FILE \
    --learning_rate=3e-5 \
    --per_device_train_batch_size=4 \
    --gradient_accumulation_steps=32 \
    --max_seq_length=256 \
    --language=${lang}

done

done