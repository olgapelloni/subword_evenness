for j in 1 2 3 4 5
do

for i in ../lang_transfer_sets/train/eng_train.txt
do

#  extract language variable from file name in two steps
one=${i#*/train/}
lang=${one%*_*}

export TRAIN_FILE=../lang_transfer_sets/train/${lang}_train.txt
export TEST_FILE=../lang_transfer_sets/valid/${lang}_valid.txt
export EVAL_RESULTS=../results_xlmr/seed${j}/${lang}.csv
export TEST_FOLDER=../lang_transfer_sets/test

echo $TRAIN_FILE
echo $TEST_FILE
echo $EVAL_RESULTS

python3 train_separately.py \
    --output_dir=../xlmr_models/seed${j}/${lang} \
    --eval_results_path=$EVAL_RESULTS \
    --model_type=xlm-roberta \
    --model_name_or_path=xlm-roberta-base \
    --tokenizer_name=xlm-roberta-base \
    --train_file=$TRAIN_FILE \
    --validation_file=$TEST_FILE \
    --test_folder_path=$TEST_FOLDER \
    --num_train_epochs=5 \
    --learning_rate=3e-5 \
    --per_device_train_batch_size=4 \
    --gradient_accumulation_steps=32 \
    --max_seq_length=256

done

done

echo 'training done'