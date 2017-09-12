#!/usr/bin/env Rscript
# Randomly resolve tree passed in via standard input
args = commandArgs(trailingOnly=TRUE)
if (length(args)!=0) {
  stop("USAGE: ./resolve_random.R < UNRESOLVED.tre > RESOLVED.tre\n", call.=FALSE)
}
library(ape);
stdin <- file('stdin','r')
unresolved <- read.tree(file=stdin)
close(stdin)
resolved <- multi2di(unresolved)
cat(write.tree(resolved),'\n')
