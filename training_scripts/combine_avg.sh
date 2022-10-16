paste ../results/avg/*.csv | column -s $',' -t > ../results/all_avg.csv

paste ../results/gains/*.csv | column -s $',' -t > ../results/all_gains.csv