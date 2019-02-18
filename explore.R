library(here)
# You can download results from WoS queries in a delimited text file.
# Beware the file encoding! You must specify "UTF-16LE" lest R gets confused.
# There are a lot of variables that are missing for all observations. That seems
# to be a feature. You may want to tell R to only read the columns that are not
# missing. More importantly, this results in line 2 having fewer 'columns' than
# line 1 and R gets tricked into thinking that column 1 indicates row names. If
# we want to get the column names from the first line, we have to first specify
# a file connection to get around the encoding issue, or readLines complains.
fileconnection <- file(description = "examples/savedrecs (1).txt", open = "r",
                       encoding = "UTF-16LE")
columns <- readLines(fileconnection, n = 1, skipNul = TRUE)
columns <- unlist(strsplit(columns, "\t"))
columns <- c(columns, "")
recs <- read.delim("examples/savedrecs (1).txt", header = FALSE, skip = 1,
                   fileEncoding = "UTF-16LE", stringsAsFactors = FALSE,
                   row.names = NULL, col.names = columns)
