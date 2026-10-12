suppressMessages(library(vegan)); data(sipoo); x <- (as.matrix(sipoo)>0)*1L
cert <- function(x, eps=0.25) { r <- rowSums(x); nc <- ncol(x); nr <- nrow(x)
  logOmega <- min(sum(lchoose(nc, r)), sum(lchoose(nr, colSums(x))))
  c(nrow=nr, ncol=nc, logOmega_bound=logOmega,
    curveball_burnin=ceiling(choose(nr,2)*(0.5*logOmega+log(1/(2*eps)))),
    curveball_thin_rho0.01=ceiling(choose(nr,2)*log(100))) }
print(cert(x))
t0 <- Sys.time(); s <- simulate(nullmodel(x,"curveball"), nsim=1, burnin=ceiling(cert(x)["curveball_burnin"])); print(Sys.time()-t0)
