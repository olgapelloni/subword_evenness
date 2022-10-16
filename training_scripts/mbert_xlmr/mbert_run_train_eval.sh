for j in 2 3 4 5
do

for i in ../lang_transfer_sets/train/*train.txt

do

#  extract language variable from file name in two steps
one=${i#*/train/}
two=${one%*_*}

export TRAIN_FILE=../lang_transfer_sets/train/${two}_train.txt
export TEST_FILE=../lang_transfer_sets/valid/${two}_valid.txt
export EVAL_RESULTS=../results/seed${j}/${two}.csv
export TEST_FOLDER=../lang_transfer_sets/test

echo $TRAIN_FILE
echo $TEST_FILE
echo $EVAL_RESULTS

python3 run_mlm_no_trainer.py \
    --output_dir=output \
    --eval_results_path=$EVAL_RESULTS \
    --model_type=bert \
    --model_name_or_path=bert-base-multilingual-cased \
    --tokenizer_name=bert-base-multilingual-cased \
    --train_file=$TRAIN_FILE \
    --validation_file=$TEST_FILE \
    --test_folder_path=$TEST_FOLDER \
    --num_train_epochs=5 \
    --learning_rate=3e-5 \
    --per_device_train_batch_size=4 \
    --gradient_accumulation_steps=32

done

done
