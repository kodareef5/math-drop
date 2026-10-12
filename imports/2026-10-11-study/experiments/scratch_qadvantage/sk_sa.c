/* Simulated annealing + greedy descent on SK: H(s) = (1/sqrt n) sum_{i<j} J_ij s_i s_j, maximize.
   Reports energy per spin H/n (same normalization as QOKit best_SK_QAOA_parameters.json energies
   and the Parisi constant P* = 0.763166).  Usage: sk_sa n sweeps seed */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
static unsigned long long st;
static double urand(void){ st ^= st<<13; st ^= st>>7; st ^= st<<17; return (st>>11)*(1.0/9007199254740992.0);}
static double gauss(void){ double u=urand(),v=urand(); if(u<1e-300)u=1e-300; return sqrt(-2*log(u))*cos(2*M_PI*v);}
int main(int argc,char**argv){
  int n=atoi(argv[1]); long sweeps=atol(argv[2]); st=0x9E3779B97F4A7C15ULL*(unsigned long long)(atoi(argv[3])+1);
  double *J=malloc(sizeof(double)*n*n), *h=calloc(n,sizeof(double)); int *s=malloc(sizeof(int)*n);
  double sc=1.0/sqrt((double)n);
  for(int i=0;i<n;i++){J[i*n+i]=0; for(int j=i+1;j<n;j++){double g=gauss()*sc; J[i*n+j]=g; J[j*n+i]=g;}}
  for(int i=0;i<n;i++) s[i]= urand()<0.5?1:-1;
  for(int i=0;i<n;i++){double a=0; for(int j=0;j<n;j++) a+=J[i*n+j]*s[j]; h[i]=a;}
  clock_t t0=clock();
  /* maximize H: flipping i changes H by -2 s_i h_i */
  double b0=0.1,b1=10.0;
  for(long sw=0;sw<sweeps;sw++){
    double beta=b0*pow(b1/b0,(double)sw/(sweeps>1?sweeps-1:1));
    for(int k=0;k<n;k++){ int i=(int)(urand()*n); double dE=-2.0*s[i]*h[i];
      if(dE>=0 || urand()<exp(beta*dE)){ s[i]=-s[i]; double d=2.0*s[i]; double*Ji=J+(long)i*n; for(int j=0;j<n;j++) h[j]+=d*Ji[j]; } }
  }
  /* greedy descent to a local optimum */
  int improved=1; while(improved){improved=0; for(int i=0;i<n;i++){ if(s[i]*h[i]<0){ s[i]=-s[i]; double d=2.0*s[i]; double*Ji=J+(long)i*n; for(int j=0;j<n;j++) h[j]+=d*Ji[j]; improved=1;}}}
  double E=0; for(int i=0;i<n;i++) E+=s[i]*h[i]; E*=0.5;
  printf("%d %ld %.5f %.2f\n", n, sweeps, E/n, (double)(clock()-t0)/CLOCKS_PER_SEC);
  return 0;}
