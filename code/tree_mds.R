library(cmdscale)
bins <- read.table(file = "2bins_out.txt", header = T) # will need to do this with the 2 bins output, 3 bins output, etc.
# need a dist class 
n <- max(table(bins$Tree1)) + 1
res <- lapply(with(bins, split(Triples, bins$Tree1)), function(x) c(rep(NA, n - length(x)), x))
res <- do.call("rbind", res)
res <- rbind(res, rep(NA, n))
res <- as.dist(t(res))

# set up mds
mds <- cmdscale(res, k = 2)
plot(mds[,1], mds[,2], xlab = "", ylab = "", axes = TRUE,
     main = "cmdscale (stats)")
text(mds[,1], mds[,2], labels(res), cex = 0.9, xpd = TRUE) 

# calculate euclidean distance from origin
# add origin to mds data
mds_origin <- rbind(c(0,0), mds)
# calculate euclidean distance of each point from the origin
bins_eucl <- as.matrix(dist(mds_origin, method = "euclidean"))[1,]
# then write that, add the gene names and use that for your rankings
write.csv(bins_eucl, file = "2bins_euclidean_dist.csv")
