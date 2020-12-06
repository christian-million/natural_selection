library(ggplot2)
library(dplyr)


data <- read.csv('natural_selection/tst.csv',
                col.names = c('agent','time', 'x', 'y'),
                stringsAsFactors = F)

path <- data %>%
  filter(stringr::str_starts(agent, 'Agent')) %>%
  arrange(agent, time)

food <- data %>%
  filter(stringr::str_starts(agent, 'Food')) %>%
  arrange(agent, time)

ggplot(path, aes(x=x, y=y, color=agent, group=agent))+
  geom_path(aes(alpha = time))+
  geom_point(data=food, aes(x=x, y=y), size=3)
