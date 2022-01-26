dat <- within(dat, loci <- factor(loci, levels = c("50", "100", "175",
                                                	  "225", "300", "375", "475"))) # or whatever other levels you use
dat <- within(datn, bins <- factor(bins, levels = c("2", "3", "4",
                                                         "5", "6", "7", "8"))) # or whatever other levels you use
node1 <- dat[which(dat$nodes==1),] # make a figure for each individual node
pdf("node1.pdf")
ggplot(node1, aes(loci, bins)) + geom_tile(aes(fill = bs)) + 
  scale_fill_gradientn(colours = c("white", "khaki1", "cyan", "mediumblue", "black"),
                       values = c(0, .70,.80,.90,1.00), limits =c(0,100)) + 
  coord_equal() +  theme(plot.background=element_blank(), 
                         panel.border=element_rect(fill = NA, colour='black',size=3), 
                         axis.title.x=element_blank(),
                         axis.text.x=element_blank(), axis.ticks.x=element_blank(), axis.text.y = element_blank(), 
                         axis.ticks.y = element_blank(), axis.title.y = element_blank()) +
  guides(fill = F)

dev.off()
