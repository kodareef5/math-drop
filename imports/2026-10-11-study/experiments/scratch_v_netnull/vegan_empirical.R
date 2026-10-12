# Empirical check of vegan null models on a 3x4 0/1 matrix with rs=(2,2,2), cs=(2,2,1,1)
suppressMessages(library(vegan))
set.seed(20261011)
x <- matrix(c(1,1,0,0,
              1,0,1,0,
              0,1,0,1), nrow=3, byrow=TRUE)
stopifnot(all(rowSums(x)==c(2,2,2)), all(colSums(x)==c(2,2,1,1)))
key <- function(a) apply(a, 3, function(m) paste(t(m), collapse=""))
out <- list()
nsim <- 60000
# non-sequential quasiswap with default thin=1 and with thin=100
out$quasiswap_thin1   <- table(key(simulate(nullmodel(x, "quasiswap"), nsim=nsim)))
out$quasiswap_thin100 <- table(key(simulate(nullmodel(x, "quasiswap"), nsim=nsim, thin=100)))
# sequential: many independent short chains are slow; use one long chain heavily thinned
out$swap      <- table(key(simulate(nullmodel(x, "swap"), nsim=nsim, thin=25, burnin=1000)))
out$curveball <- table(key(simulate(nullmodel(x, "curveball"), nsim=nsim, thin=25, burnin=1000)))
out$tswap     <- table(key(simulate(nullmodel(x, "tswap"), nsim=nsim, thin=100, burnin=1000)))
for (nm in names(out)) cat(nm, paste(names(out[[nm]]), as.integer(out[[nm]]), sep=":", collapse=" "), "\n")
cat("vegan", as.character(packageVersion("vegan")), "\n")
