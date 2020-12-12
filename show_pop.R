# Set local user library repo
.libPaths("C:/Users/millionc/Documents/R/win-library/3.5")

library(ggplot2)
data <- read.csv('pop.csv', col.names = c('day', 'agents'), stringsAsFactors = F)

p <- ggplot(data, aes(x=day, y=agents)) +
  geom_bar(stat = 'identity')

ggsave("model_results.png", p, path="images", width=5, height=3, units="in")
