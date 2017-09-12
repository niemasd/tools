#!/usr/bin/env Rscript
# Randomly resolve tree passed in via standard input
args = commandArgs(trailingOnly=TRUE)
if (length(args)!=0) {
  stop("USAGE: ./resolve_random.R < UNRESOLVED.tre > RESOLVED.tre\n", call.=FALSE)
}
library(ape);
unresolved <- read.tree(file=file('stdin', 'r'))
resolved <- multi2di(unresolved)
write.tree(resolved)
