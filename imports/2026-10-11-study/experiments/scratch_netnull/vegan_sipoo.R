suppressMessages(library(vegan))
data(sipoo)
x <- (as.matrix(sipoo) > 0) * 1L
cat("sipoo dims", dim(x), "fill", sum(x), "\n")
stats <- function(s) {
  nodf <- apply(s, 3, function(m) nestednodf(m)$statistic["NODF"])
  cs <- apply(s, 3, function(m) nestedchecker(m)$C.score)
  cbind(nodf=nodf, cscore=cs)
}
set.seed(1)
N <- 1000
res <- list()
res$quasiswap_thin1   <- stats(simulate(nullmodel(x, "quasiswap"), nsim=N, thin=1))
res$quasiswap_thin100 <- stats(simulate(nullmodel(x, "quasiswap"), nsim=N, thin=100))
res$curveball_long    <- stats(simulate(nullmodel(x, "curveball"), nsim=N, burnin=20000, thin=200))
res$tswap_long        <- stats(simulate(nullmodel(x, "tswap"), nsim=N, burnin=200000, thin=5000))
res$swap_long         <- stats(simulate(nullmodel(x, "swap"), nsim=N, burnin=20000, thin=500))
ref <- res$curveball_long
obs <- c(nodf=nestednodf(x)$statistic["NODF"], cscore=nestedchecker(x)$C.score)
for (nm in names(res)) {
  r <- res[[nm]]
  cat(sprintf('{"model":"%s","NODF_mean":%.3f,"NODF_sd":%.3f,"NODF_shift_vs_curveball_in_sd":%.3f,"Cscore_mean":%.4f,"Cscore_sd":%.4f,"Cscore_shift_in_sd":%.3f,"z_NODF_obs":%.2f}\n',
      nm, mean(r[,1]), sd(r[,1]), (mean(r[,1])-mean(ref[,1]))/sd(ref[,1]),
      mean(r[,2]), sd(r[,2]), (mean(r[,2])-mean(ref[,2]))/sd(ref[,2]), (obs[1]-mean(r[,1]))/sd(r[,1])))
}
