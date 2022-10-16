import os

langs = ['xlmr_nofinetune']

#langs = ['basque', 'eng', 'finnish', 'french', 'german','greek_modern', 'hebrew_modern',
 #         'hindi', 'indonesian', 'japanese', 'korean', 'mandarin', 'persian', 'russian',
  #        'spanish', 'tagalog', 'thai', 'turkish', 'vietnamese']

#langs = ['greek_modern', 'hebrew_modern', 'hindi', 'indonesian', 'korean', 'mandarin']

all = {}

folder = 'results_xlmr'

if not os.path.exists('../' + folder + '/avg/'):
    os.mkdir('../' + folder + '/avg/')

for lang in langs:
    avg_file = '../' + folder + '/avg/' + lang + '.csv'
    with open(avg_file, 'w') as f_avg:
        with open('../' + folder + '/seed1/' + lang + '.csv', 'r') as f_seed1:
            seed1 = f_seed1.readlines()
            print(len(seed1))
        with open('../' + folder + '/seed2/' + lang + '.csv', 'r') as f_seed2:
            seed2 = f_seed2.readlines()
        with open('../' + folder + '/seed3/' + lang + '.csv', 'r') as f_seed3:
            seed3 = f_seed3.readlines()
        with open('../' + folder + '/seed4/' + lang + '.csv', 'r') as f_seed4:
            seed4 = f_seed4.readlines()
        with open('../' + folder + '/seed5/' + lang + '.csv', 'r') as f_seed5:
            seed5 = f_seed5.readlines()

        for i in range(len(seed1)):
            print(lang)
            print(i, seed1[i], seed2[i], seed3[i], seed4[i], seed5[i])
            avg = (float(seed1[i].strip()) + float(seed2[i].strip()) + float(seed3[i].strip()) +
                   float(seed4[i].strip()) + float(seed5[i].strip())) / 5
            f_avg.write(str(avg) + '\n')

