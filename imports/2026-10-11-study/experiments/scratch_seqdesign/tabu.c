// LABS tabu search (Gallardo-Cotta-Fernandez 2009 style TS component, as used in MTS).
// Usage: tabu N budget_steps rng_seed seeds_file
//   seeds_file: one sequence per line as a string of '+'/'-' (length N). Restarts cycle
//   through the file in order (each restart = one TS run of maxIters steps from the next seed).
// Output: best energy, best merit factor, number of restarts, best sequence.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static uint64_t rs;
static inline uint64_t xr(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }

static int64_t energy(const int *s, int N, int *C){
  int64_t E=0;
  for(int k=1;k<N;k++){ int c=0; for(int j=0;j+k<N;j++) c+=s[j]*s[j+k]; C[k]=c; E+=(int64_t)c*c; }
  return E;
}

int main(int argc, char **argv){
  if(argc<5){ fprintf(stderr,"usage\n"); return 1; }
  int N=atoi(argv[1]); long budget=atol(argv[2]); rs=strtoull(argv[3],0,10)*2654435761ULL+12345;
  FILE *f=fopen(argv[4],"r"); if(!f){perror("seeds");return 1;}
  // read seeds
  int cap=16, ns=0; char **seeds=malloc(cap*sizeof(char*));
  char *line=malloc(N+16);
  while(fgets(line,N+16,f)){ if((int)strlen(line)<N) continue; if(ns==cap){cap*=2;seeds=realloc(seeds,cap*sizeof(char*));} seeds[ns]=malloc(N); memcpy(seeds[ns],line,N); ns++; }
  fclose(f);
  if(ns==0){fprintf(stderr,"no seeds\n");return 1;}
  int *s=malloc(N*sizeof(int)), *C=malloc(N*sizeof(int)), *best=malloc(N*sizeof(int));
  long *tabu=malloc(N*sizeof(long));
  int64_t bestE=INT64_MAX; long steps=0; int restarts=0; double seedF_first=0, seedF_best=0;
  while(steps<budget){
    char *sd=seeds[restarts%ns];
    for(int i=0;i<N;i++) s[i]=(sd[i]=='+')?1:-1;
    int64_t E=energy(s,N,C);
    double sf=(double)N*N/(2.0*E); if(restarts==0) seedF_first=sf; if(sf>seedF_best) seedF_best=sf;
    if(E<bestE){bestE=E; memcpy(best,s,N*sizeof(int));}
    restarts++;
    // TS run
    long maxIters = N/2 + (long)(xr()%(N+1)); // uniform in [N/2, 3N/2]
    long minTabu = maxIters/10; long extraTabu = maxIters/50; if(extraTabu<1) extraTabu=1;
    for(int i=0;i<N;i++) tabu[i]=-1;
    int64_t runBest=E;
    for(long it=0; it<maxIters && steps<budget; it++, steps++){
      int bi=-1; int64_t bE=INT64_MAX; int nties=0;
      for(int i=0;i<N;i++){
        int si=s[i]; int64_t e=0;
        int lo=(i<N-1-i)?i:(N-1-i); // k<=lo: both neighbours exist
        int k=1;
        for(;k<=lo;k++){ int c=C[k]-2*si*(s[i+k]+s[i-k]); e+=(int64_t)c*c; }
        if(i< N-1-i){ for(;k<N-i;k++){ int c=C[k]-2*si*s[i+k]; e+=(int64_t)c*c; } for(;k<N;k++){ e+=(int64_t)C[k]*C[k]; } }
        else { for(;k<=i;k++){ int c=C[k]-2*si*s[i-k]; e+=(int64_t)c*c; } for(;k<N;k++){ e+=(int64_t)C[k]*C[k]; } }
        int allowed = (tabu[i] < it) || (e < bestE);
        if(!allowed) continue;
        if(e<bE){bE=e;bi=i;nties=1;}
        else if(e==bE){ nties++; if(xr()%nties==0) bi=i; }
      }
      if(bi<0) continue;
      // apply flip
      int si=s[bi];
      for(int k=1;k<N;k++){ int v=0; if(bi+k<N) v+=s[bi+k]; if(bi-k>=0) v+=s[bi-k]; C[k]-=2*si*v; }
      s[bi]=-si; E=bE;
      tabu[bi]=it+minTabu+(long)(xr()%(extraTabu+1));
      if(E<runBest) runBest=E;
      if(E<bestE){bestE=E; memcpy(best,s,N*sizeof(int));}
    }
  }
  printf("bestE %lld bestF %.4f restarts %d steps %ld seedF_first %.4f seedF_best %.4f\n",(long long)bestE,(double)N*N/(2.0*bestE),restarts,steps,seedF_first,seedF_best);
  for(int i=0;i<N;i++) putchar(best[i]>0?'+':'-'); putchar('\n');
  return 0;
}
