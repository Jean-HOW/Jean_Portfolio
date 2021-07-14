library(dplyr);library(tidyr);library(ggplot2)

df <- read.csv("timestamp.txt",
               header = TRUE)

df$posted_at <- trimws(df$posted_at, "l")

df$posted_at <- sort(strptime(df$posted_at, "%d/%m/%y %H:%M"))

hist(df$posted_at, breaks = "months",
     col="cyan", 
     main = "Histogram of Barack Obama's timestamp for posts",
     xlab = "timestamp",
     ylab = "frequency",
     freq = TRUE)

#_________________________________________________________________

df2 <- read.delim("abc.txt",
                  header = TRUE,
                  sep = " ")


abc <- df2 %>% 
        select(-page_name) %>% 
        group_by(post_type)

boxplot <- abc %>% 
        ggplot(aes(x=post_type,
                   y=comments_count,
                   fill=post_type)) +
        geom_boxplot() +
        scale_y_continuous(trans='log10') + 
        labs(x = "Post Type",
             y = "Comments Count(Log10)") + 
        theme_minimal()

vid <- abc %>% filter(post_type == 'video') %>% 
        arrange(comments_count)

eve <- abc %>% filter(post_type == 'event') %>% arrange(comments_count)
eve

abc_filt <- abc %>% filter(comments_count < 1000)

boxplot2 <- abc_filt %>% 
        ggplot(aes(x=post_type,
                   y=comments_count,
                   fill=post_type)) +
        geom_boxplot() +
        labs(x = "Post Type",
             y = "Comments Count") + 
        theme_minimal()
boxplot2

stat <- abc_filt %>% filter(post_type == 'status')
summary(stat)
