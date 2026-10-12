suppressMessages(library(vegan))
set.seed(42)
# margins r=(2,2,2,2), c=(2,2,2,2): 90 binary matrices (exact results in vegan_exact.py)
x <- matrix(c(1,1,0,0, 0,1,1,0, 0,0,1,1, 1,0,0,1), 4, 4, byrow=TRUE)
key <- function(m) paste(as.integer(m), collapse="")
run <- function(method, nsim, thin) {
  nm <- nullmodel(x, method)
  s <- simulate(nm, nsim=nsim, thin=thin, burnin=if (method %in% c("swap","tswap","curveball")) 1000 else 0)
  k <- apply(s, 3, key)
  tab <- table(k)
  N <- 90
  cnt <- c(as.numeric(tab), rep(0, N - length(tab)))
  p <- cnt / sum(cnt)
  tv <- 0.5 * sum(abs(p - 1/N))
  pv <- chisq.test(cnt, p=rep(1/N, N))$p.value
  cat(sprintf('{"method":"%s","thin":%d,"nsim":%d,"distinct":%d,"TV_uniform":%.4f,"chisq_p_uniform":%.3g}\n', method, thin, nsim, length(tab), tv, pv))
}
run("swap", 60000, 20)
run("tswap", 60000, 50)
run("curveball", 60000, 10)
run("quasiswap", 60000, 1)
run("quasiswap", 60000, 100)
