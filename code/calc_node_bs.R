#Place all the bootstrapped trees into a single nexus file. Make sure to include their names. Read into R.

library(ape)
library(ggtree)
library(dplyr)
library(tidyr)
library(ggplot2)

tree <- read.nexus("tree.nex")
# reroot trees if necessary, it's essential that they all have the same node labels
	
# Grab BS node values for from each tree
dat <- lapply(trees, '[[', "node.label")
dat <- data.frame(dat)
dat <- tbl_df(dat)
# add a column with your nodes. Make sure this lines up the node numbers of your phylogeny. In R, the node number starts after
# the number of tips.
node <- c(142:182) # however many nodes you have
dat <- cbind(nodes, dat)
dat<- tbl_df(dat)
# reorganize the data into the proper format.
dat <- gather(dat, key = "set", value = "bs", first_tree:last_tree)
dat <- separate(dat, set, sep = "_", into = c("bins", "loci")) # splits NUMbin_NUMloci column into two based on the underscore
dat$bins <- gsub(pattern = "\\D", replacement = "", dat$bins) # gets rid of text in column
dat$loci <- gsub(pattern = "\\D", replacement = "", dat$loci) # gets rid of text in column

# You can make a figure with the node values and bs values to double check the correct BS value is placed with the correct node
ggtree(trees) +geom_text2(aes(subset=!isTip, label=label)) # to get the bs Values
ggtree(tress) +geom_text2(aes(subset=!isTip, label=node)) # to get the node labels
