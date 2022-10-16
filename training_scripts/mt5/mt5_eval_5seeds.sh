#  loop through test files
for i in ../data/test/*.txt
do 
one=${i#*/test/}
test_lang=${one%*.*}
echo $test_lang

# loop through languages of trained models
for l in ../mt5_models/*
do 
train_lang=${l#*/mt5_models/}
echo $train_lang

# loop through trained models within each language
for m in ../mt5_models/$train_lang/*
do 
model=${m#*/$train_lang/}
echo ${model}

export NUM_GPUS=1
export TEST_FILE=../data/test/${test_lang}.txt

python3 mt5_eval.py \
    --model_type=t5 \
    --model_name_or_path=../mt5_models/${train_lang}/${model} \
    --tokenizer_name=google/mt5-base \
    --validation_file=$TEST_FILE \
    --learning_rate=3e-5 \
    --output_dir=../mt5_test_results/${train_lang} \
    --max_seq_length=256 \
    --do_eval \
    --per_device_train_batch_size="8" \
    --per_device_eval_batch_size="8" \
    --language=${test_lang}
    
done
done
done
