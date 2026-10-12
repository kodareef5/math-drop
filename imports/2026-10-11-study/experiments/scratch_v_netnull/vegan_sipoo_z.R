# Run-to-run SD of oecosimu NODF z-score on sipoo, curveball, default vs long burnin/thin
suppressMessages(library(vegan)); data(sipoo)
z <- function(...) { r <- oecosimu(sipoo, nestednodf, "curveball", nsimul=99, ...); unname(r$oecosimu$z["NODF"]) }
set.seed(1)
zd <- replicate(30, z())
zc <- replicate(30, z(burnin=20000, thin=500))
cat("dim", dim(sipoo), " C(r,2)=", choose(nrow(sipoo),2), "\n")
cat("default burnin=0 thin=1: mean z", round(mean(zd),2), "SD", round(sd(zd),3), "\n")
cat("burnin=20000 thin=500:   mean z", round(mean(zc),2), "SD", round(sd(zc),3), "\n")
