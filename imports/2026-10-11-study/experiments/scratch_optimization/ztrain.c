#define ZDICT_STATIC_LINKING_ONLY
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "zstd_instr/zdict.h"
int main(int argc, char** argv){
  /* argv[1]=mode(cover|fastcover) argv[2]=list file argv[3]=samples concat out */
  FILE* lf=fopen(argv[2],"r"); char path[4096]; size_t cap=1<<26, tot=0; char* buf=malloc(cap); size_t sizes[100000]; unsigned n=0;
  while(fgets(path,sizeof path,lf)){ path[strcspn(path,"\n")]=0; FILE* f=fopen(path,"rb"); if(!f) continue; size_t r=fread(buf+tot,1,cap-tot,f); fclose(f); if(!r) continue; sizes[n++]=r; tot+=r; }
  FILE* o=fopen(argv[3],"wb"); fwrite(buf,1,tot,o); fclose(o);
  size_t dcap=112640; void* dict=malloc(dcap); size_t r;
  if(!strcmp(argv[1],"cover")){ ZDICT_cover_params_t p; memset(&p,0,sizeof p); p.k=200; p.d=8; p.zParams.compressionLevel=3; r=ZDICT_trainFromBuffer_cover(dict,dcap,buf,sizes,n,p);}
  else { ZDICT_fastCover_params_t p; memset(&p,0,sizeof p); p.k=200; p.d=8; p.f=20; p.accel=1; p.zParams.compressionLevel=3; r=ZDICT_trainFromBuffer_fastCover(dict,dcap,buf,sizes,n,p);}
  fprintf(stderr,"dict size %zu (err=%d) samples %u bytes %zu\n", r, ZDICT_isError(r), n, tot);
  return 0;
}
