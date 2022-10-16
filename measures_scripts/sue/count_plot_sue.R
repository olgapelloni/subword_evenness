library(ggplot2)
library(tidyverse)
library(gridExtra)
library(RColorBrewer)
library(reshape)
library(plyr)
library(FunChisq)
library(REdaS)
library(Morpho)
library(scales)

langs_short <- c('basque', 'eng', 'finnish', 'french', 'german', 'greek_modern', 'hebrew_modern', 'hindi', 'indonesian', 'japanese', 'korean', 'mandarin', 'persian', 'russian', 'spanish', 'tagalog', 'thai', 'turkish', 'vietnamese')
langs_full <- c('Basque', 'English', 'Finnish', 'French', 'German', 'Greek', 'Hebrew', 'Hindi', 'Indonesian', 'Japanese', 'Korean', 'Mandarin', 'Persian', 'Russian', 'Spanish', 'Tagalog', 'Thai', 'Turkish', 'Vietnamese')

Language <- c(NA)
Angle <- c(NA)
Mode <- c(NA)
new_results <- data.frame(Language, Angle, Mode)

language <- c(NA)
k <- c(NA)
b <- c(NA)
rad_angle <- c(NA)
deg_angle <- c(NA)
results <- data.frame(language, k, b, rad_angle, deg_angle)

Var1 <- c(NA)
Var2 <- c(NA)
Freq <- c(NA)
lang <- c(NA)
new_angle <- data.frame(Var1, Var2, Freq, lang)

x <- c(NA)
values <- c(NA)
diagonals <- c(NA)
lang <- c(NA)
new_data_fun <- data.frame(x, values, diagonals, lang)

angles <- rep(c(0),times=100)

for (l in 1:length(langs_short)) {
  print(langs_short[l])
  df <- read.csv(paste('../bpe-min-r/', langs_short[l], '_results.csv', sep=''), sep = '\t')
  
  df <- df[grepl(',', df$segments_lengths),]
  
  lang_short <- langs_short[l]
  lang_full <- langs_full[l]
  
  for (iter in 1:100) {
    # print(iter)
    df1 <- df[df$language == lang_short,]
    freqs <- data.frame(table(df1$index, df1$word_length))
    freqs <- freqs[!(freqs$Freq == 0),]
    freqs$lang <- lang_short
    
    freqs$Var1 <- as.integer(as.character(freqs$Var1))
    freqs$Var2 <- as.integer(as.character(freqs$Var2))
    
    freqs <- subset(freqs, select = c(1,2,3))
    freqs <- add.noise(freqs, 0.0001, "house", 2)
    freqs <- as.data.frame(freqs)
    names(freqs)[names(freqs)=="V1"] <- "Var1"
    names(freqs)[names(freqs)=="V2"] <- "Var2"
    names(freqs)[names(freqs)=="V3"] <- "Freq"
    
    p <- ggplot(freqs,
                aes(x = Var2,
                    y = Var1)) +
      labs(title = paste(lang_full, ', ', lang_short, sep = ''),
           x = 'word length in characters',
           y = 'unevenness index',
           size = 'frequency of\nthe unevenness index\nfor the given word length') +
      geom_point(aes(size = Freq)) +
      scale_size(labels = comma) +
      scale_x_continuous(limits = c(0, 50)) +
      scale_y_continuous(limits = c(0, 50)) + 
      geom_density_2d_filled(alpha=.5, bins=3, color='blue') +
      guides(size = guide_legend(order=1),
             levels = guide_legend(order=2))
    
    ggbld <- ggplot_build(p)
    gdata <- ggbld$data[[2]]
    sub <- gdata[gdata$fill == '#21908CFF',]
    
    sub %>%
      ggplot() +
      geom_point(aes(x, y)) +
      geom_polygon(aes(x, y))
    
    # find 2 data points
    # find x, where y is max
    max_y <- max(sub$y)
    max_x <- sub[sub$y == max_y,]$x[[1]]
    
    # find starting point for y
    #mid_y <- (max_y - 2) / 2
    
    max_right_x <- max(sub$x)
    max_right_y <- sub[sub$x == max_right_x,]$y[[1]]
    
    x1 <- max_x
    y1 <- max_y
    
    x2 <- max_right_x
    y2 <- max_right_y
    
    df_line <- data.frame(x1, y1)
    df_line <- rbind(df_line, c(x2, y2))
    
    X <- matrix(c(x1, 1,
                  x2, 1), 2, 2, byrow=TRUE)
    y <- c(y1, y2)
    coef <- solve(X, y)
    
    # extract k, b
    k <- coef[1]
    b <- coef[2]
    
    theta1 <- atan(1)
    theta2 <- atan(k)
    rad_angle <- pi - abs(theta1 - theta2)
    
    # radians to degrees
    deg_angle <- rad2deg(rad_angle)
    
    # print(deg_angle)
    
    # plot angle
    y <- function(x) { x - 2 }           # Create own functions
    right_diagonal <- function(x) { k*x + b}
    
    curve(y, from = 0, to = 100, col = 2)  # Draw Base R plot
    curve(right_diagonal, from = 0, to = 100, col = 3, add = TRUE)
    
    data_fun <- data.frame(x = - 100:100,            # Create data for ggplot2
                           values = c(y(- 100:100),
                                      right_diagonal(- 100:100)),
                           diagonals = rep(c("left diagonal", "right diagonal"), each = 201))
    
    data_fun$lang <- lang_short
    
    p2 <- ggplot(freqs,
                 aes(x = Var2,
                     y = Var1)) +
      ggtitle(paste(lang_full, '\nBPE-Min-R', sep = '')) +
      labs(x = 'word length in characters',
           size = 'frequency of\nthe unevenness index\nfor the given word length',
           colour = 'angle',
           levels = 'density level') +
      geom_point(aes(size = Freq)) +
      scale_size(labels = comma) +
      scale_x_continuous(limits = c(0, 30)) +
      scale_y_continuous(limits = c(0, 30)) +
      geom_density_2d_filled(alpha=.5, bins=3, color='blue') +
      geom_line(data = data_fun, aes(x, values, col = diagonals)) +
      scale_color_manual(values=c("bisque", "bisque")) +
      theme(
        axis.title.y = element_blank(),
        legend.position = 'none',
        plot.title=element_text(face='bold', color='white', size=18, hjust=0.08, vjust=-15, margin = margin(t=-30,b=0)))
    
    ggsave(paste('../plots/bpe-min-r/', lang_full, '_', iter, '.png', sep = ''),
           plot = p2,
           width = 9, height = 5)
    
    results <- rbind(results, c(lang_full, k, b, rad_angle, deg_angle))
    
    freqs$lang <- paste(lang_full, ', ', lang_short, sep = '')
    new_angle <- rbind(new_angle, freqs)
    
    data_fun$lang <- paste(lang_full, ', ', lang_short, sep = '')
    new_data_fun <- rbind(new_data_fun, data_fun)
    
    angles[iter] <- deg_angle
    
  }
  
  closest<-function(xv,sv){
    xv[which(abs(xv-sv)==min(abs(xv-sv)))] }
  
  closest(angles, mean(angles))
  
  index <- which(abs(angles-mean(angles))==min(abs(angles-mean(angles))))
  
  print(lang_full)
  print(index)
  print(mean(angles))
  
  new_results[nrow(new_results) + 1,] <- c(lang_full, mean(angles), 'BPE-Min-R')
}

na.omit(new_results)
new_results
