suppressMessages(library(vegan)); data(sipoo); x <- (as.matrix(sipoo)>0)*1L
set.seed(3)
nodf <- function(m) nestednodf(m)$statistic["NODF"]
f <- function(...) { o <- oecosimu(x, function(m) nestednodf(m)$statistic["NODF"], ...); s <- as.numeric(o$oecosimu$simulated); c(mean=mean(s), sd=sd(s), z=unname(o$oecosimu$z)) }
r <- rbind(
  curveball_defaults = f(method="curveball", nsimul=99),
  swap_defaults      = f(method="swap", nsimul=99),
  tswap_defaults     = f(method="tswap", nsimul=99),
  curveball_certified= f(method="curveball", nsimul=99, burnin=22394, thin=705),
  quasiswap_default  = f(method="quasiswap", nsimul=99))
print(round(r,3))
# repeat defaults 20 times to see spread of z
zs <- replicate(20, f(method="curveball", nsimul=99)[3]); zc <- replicate(20, f(method="curveball", nsimul=99, burnin=22394, thin=705)[3])
cat("curveball defaults: z mean", round(mean(zs),2), "sd", round(sd(zs),2), " | certified: z mean", round(mean(zc),2), "sd", round(sd(zc),2), "\n")
cat("observed NODF", nodf(x), "\n")
