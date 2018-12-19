library(ggplot2)
library(dplyr)

emo <- read.csv2("C:/Users/arnau/Desktop/emo.txt", header = T, sep = "\t")[,-1]
emo <- emo %>%
  mutate(pair = as.character(pair),
         emotion = factor(emo$emotion,
                          levels = c("positive", "negative", " ", "joy", "trust", "anger", "disgust", "fear", "sadness")),
         group = ifelse(emo$emotion %in% c("negative","positive"), "pol", "det"),
         col = ifelse(emo$emotion %in% c("positive", "anticipation", "joy", "trust"), "+", "-"))

df <- emo %>%
  filter(cooc >= 150)

df1 <- df %>%
  filter(pair == "lady_jessica&paul_atreides") %>%
  as.data.frame()
df2 <- df %>%
  filter(pair == "gurney_halleck&paul_atreides") %>%
  as.data.frame()
df3 <- df %>%
  filter(pair == "paul_atreides&stilgar") %>%
  as.data.frame()
df4 <- df %>%
  filter(pair == "baron_vladimir_harkonnen&feyd-rautha_rabban") %>%
  as.data.frame()

temp <- df[1,]
val <- list(0, " ", " ", 0, "det", "n")
for (i in 1:6){
  temp[1,i] <- val[[i]]
}

df1 <- rbind(df1, temp)
df2 <- rbind(df2, temp)
df3 <- rbind(df3, temp)
df4 <- rbind(df4, temp)

ggplot(df1) +
  geom_bar(aes(x = emotion, y = value, fill = col, color = group), stat = "identity") +
  scale_fill_manual(values = c("-" = "darkorange1", "+" ="lightskyblue", "n"="white"))+
  scale_color_manual(values = c("white", "black"))+
  theme_bw() +
  labs(x = "Emotions",
       y = "Score",
       title = "Relation entre lady Jessica et Paul Atreides") +
  theme(legend.position="none")

ggplot(df2) +
  geom_bar(aes(x = emotion, y = value, fill = col, color = group), stat = "identity") +
  scale_fill_manual(values = c("-" = "darkorange1", "+" ="lightskyblue", "n"="white"))+
  scale_color_manual(values = c("white", "black"))+
  theme_bw() +
  labs(x = "Emotions",
       y = "Score",
       title = "Relation entre Gurney Halleck et Paul Atreides") +
  theme(legend.position="none")

ggplot(df3) +
  geom_bar(aes(x = emotion, y = value, fill = col, color = group), stat = "identity") +
  scale_fill_manual(values = c("-" = "darkorange1", "+" ="lightskyblue", "n"="white"))+
  scale_color_manual(values = c("white", "black"))+
  theme_bw() +
  labs(x = "Emotions",
       y = "Score",
       title = "Relation entre Stilgar et Paul Atreides") +
  theme(legend.position="none")

ggplot(df4) +
  geom_bar(aes(x = emotion, y = value, fill = col, color = group), stat = "identity") +
  scale_fill_manual(values = c("-" = "darkorange1", "+" ="lightskyblue", "n"="white"))+
  scale_color_manual(values = c("white", "black"))+
  theme_bw() +
  labs(x = "Emotions",
       y = "Score",
       title = "Relation entre le Baron Vladimir Harkonnen et Feyd-Rautha Rabban") +
  theme(legend.position="none")


max <- emo %>%
  filter(emotion %in% c('positive', 'negative')) %>%
  group_by(pair) %>%
  summarise(col2 = emotion[which.max(value)]) %>%
  ungroup %>%
  mutate(col2 = ifelse(col2 == "positive", "+", "-"))
  
emo <- emo %>%
  left_join(max, by = 'pair')

data <- emo %>%
  filter(!(emotion %in% c('positive', 'negative'))) %>%
  group_by(pair) %>%
  filter(col == col2) %>%
  filter(value == max(value)) %>%
  filter(cooc > 50)

names <- as.character(read.csv2("C:/Users/arnau/Desktop/names.txt", header = T, sep = "\t")[,-1])
corpus <- as.character(read.csv2("C:/Users/arnau/Desktop/corpus.txt", header = T, sep = "\t")[,-1])

df <- data.frame(name = names, occ = NA) %>%
  group_by(name) %>%
  mutate(occ = sum(corpus == name)) %>%
  ungroup %>%
  filter(occ > 500)

lady <- which(corpus == "lady_jessica")
duke <- which(corpus == "duke_leto_i_atreides")
paul <- which(corpus == "paul_atreides")
gurney <- which(corpus == "gurney_halleck")
baron <- which(corpus == "baron_vladimir_harkonnen")

n <- length(corpus)

breaks <- seq(0,n,7500)
k <- length(breaks)-1

data <- data.frame(character = c(rep("Lady Jessica", k),
                                 rep("Duke Atreides", k),
                                 rep("Paul Atreides", k),
                                 rep("Gurney Halleck", k),
                                 rep("Baron Harkonnen", k)),
                   counts = c(hist(lady, breaks = breaks)$counts,
                              hist(duke, breaks = breaks)$counts,
                              hist(paul, breaks = breaks)$counts,
                              hist(gurney, breaks = breaks)$counts,
                              hist(baron, breaks = breaks)$counts))


g1 <- ggplot(data)+
  geom_bar(aes(x = rep(breaks[-(k+1)],5), y = counts), stat = "identity")+
  theme_bw() +
  labs(x = "Index dans le corpus",
       y = "Occurences")
g1 + facet_wrap( ~ character, ncol = 1) + theme(legend.position = "none") +
  ggtitle("Fréquence d'apparition des 5 personnages principaux au fil de Dune")
