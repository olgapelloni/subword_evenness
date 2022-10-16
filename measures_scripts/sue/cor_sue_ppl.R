library(ggplot2)

df <- read.csv('../results/sue_scores/sue_vs_ppl.csv', sep='\t')
df1 <- read.csv('../results/sue_scores/ttr_entropy_length.csv', sep='\t')

df$iso <- c('eus', 'eng', 'fin', 'fra',
            'deu', 'ell', 'heb', 'hin',
            'ind', 'jpn', 'kor', 'cmn',
            'pes', 'rus', 'spa', 'tgl',
            'tha', 'tur', 'vie')

df <- df[order(df$iso), ]

df1 <- df1[df$iso %in% df1$file,]

df1 <- df1[order(df1$file), ]

df <- cbind(df, df1)

ggplot(df, aes(x = sue_bpe_minr, y = ppl_mt5)) +
  geom_text(aes(label = iso,
                color = script), size = 6) +
  geom_smooth(method = "lm",
              formula = y ~ x) +
  labs(color = 'Script',
       x = 'TTR',
       y = 'Average PPL on all targets')


cor.test(df$sue_bpe_minr, df$ppl_mbert, method = "pearson")
cor.test(df$sue_bpe_minr, df$ppl_mbert, method = "spearman")

