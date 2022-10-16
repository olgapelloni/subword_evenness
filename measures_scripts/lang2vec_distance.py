import lang2vec.lang2vec as l2v
from scipy import spatial

transfer_langs = ["eus", "eng", "fin", "fra", "deu", "ell", "heb", "hin",
                  "ind", "jpn", "kor", "cmn", "pes", "rus", "spa", "tgl",
                  "tha", "tur", "vie"]

target_langs = ["amp", "aey", "apu", "arz", "ape", "bsn", "mya", "cha",
                "dgz", "fij", "kat", "gug", "hau", "jac", "kew", "khk",
                "naq", "laj", "plt", "arn", "mig", "hae", "qvi", "sag",
                "xsu", "swh", "mzh", "yad", "yaq", "yor"]

features_transfer1 = l2v.get_features(transfer_langs, "inventory_knn")
features_target1 = l2v.get_features(target_langs, "inventory_knn")

features_transfer2 = l2v.get_features(transfer_langs, "inventory_knn")
features_target2 = l2v.get_features(target_langs, "inventory_knn")

features_transfer3 = l2v.get_features(transfer_langs, "inventory_knn")
features_target3 = l2v.get_features(target_langs, "inventory_knn")


sum_transfer = ''
sum_target = ''

target_res = {}

with open('lang2vec_phon.csv', 'r') as f:

    for lang1 in features_transfer:
        for lang2 in features_target:
            result = spatial.distance.cosine(features_transfer[lang1],
                                                 features_target[lang2])
            if lang2 not in target_res:
                target_res[lang2] = {}
            target_res[lang2][lang1] = result

    for target in target_res:

            min = 1000
            min_lang = ''
            for lang in target_res[target]:
                if target_res[target][lang] < min:
                    min = target_res[target][lang]
                    min_lang = lang

            print(min, target, min_lang)
