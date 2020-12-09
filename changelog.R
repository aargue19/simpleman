rm(list=ls())
setwd("C:/Users/gaoan/Desktop")

old = read.csv("step3_2020_12_04_TAV.csv")
new = read.csv("step3_2020_12_06_AJA.csv")

colnames(old)

vec1 = unique(old$std_word)
              
vec2 = unique(new$std_word)

length(vec1)

length(vec2)

setdiff(vec1, vec2)

added_words = vec2[!(vec2 %in% vec1)]

new_df = new[new$std_word != old$std_word, c("std_word", "changed_word")]

new_df = unique(new_df)

new_df = new_df[order(new_df$std_word),]

write.csv(new_df, "temp.csv")
