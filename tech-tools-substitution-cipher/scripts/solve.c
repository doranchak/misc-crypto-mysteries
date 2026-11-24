// homophonic SA solver (4-gram model, one-sided cap on glyphs per letter). Build: clang -O3 -o solve solve.c -lm
// usage: solve cipher.txt K iters restarts lambda seed   (needs quad.bin: 26^4 float32 log-probs)
// cipher.txt = space-separated glyph class ids 0..K-1; vowels may use 4 glyphs, other letters 3
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <stdint.h>
static float Q[456976];
static int L,K; static int cip[2000]; static int fixed_[200];
static uint64_t s[2];
static inline uint64_t rotl(uint64_t x,int k){return (x<<k)|(x>>(64-k));}
static uint64_t nextr(void){uint64_t s0=s[0],s1=s[1],r=s0+s1;s1^=s0;s[0]=rotl(s0,55)^s1^(s1<<14);s[1]=rotl(s1,36);return r;}
static double rnd(void){return (nextr()>>11)*(1.0/9007199254740992.0);}
static int rint_(int n){return (int)(nextr()%n);}
static int m[200]; static int cnt[26]; static int target[26];
static double lambda_;
static double score_text(void){
  double sc=0; int p[2000];
  for(int i=0;i<L;i++)p[i]=m[cip[i]];
  for(int i=0;i+3<L;i++) sc+=Q[((p[i]*26+p[i+1])*26+p[i+2])*26+p[i+3]];
  return sc;
}
static double pen(void){double p=0;for(int l=0;l<26;l++){double d=cnt[l]-target[l]; if(d>0)p+=d*d;}return p*lambda_;}
int main(int argc,char**argv){
  // args: cipherfile K iters restarts lambda seed [targetsfile]
  FILE*f=fopen(argv[1],"r"); K=atoi(argv[2]); long iters=atol(argv[3]); int restarts=atoi(argv[4]); lambda_=atof(argv[5]);
  s[0]=atoll(argv[6])*2654435761ULL+12345; s[1]=0x9E3779B97F4A7C15ULL^atoll(argv[6]);
  for(int i=0;i<20;i++)nextr();
  L=0; while(fscanf(f,"%d",&cip[L])==1)L++; fclose(f);
  FILE*q=fopen("quad.bin","rb"); fread(Q,4,456976,q); fclose(q);
  // targets: vowels (a,e,i,o,u) 4, others 3 by default
  for(int l=0;l<26;l++)target[l]=3; target[0]=target[4]=target[8]=target[14]=target[20]=4;
  int tsum=0; for(int l=0;l<26;l++)tsum+=target[l];
  if(argc>7){FILE*t=fopen(argv[7],"r"); for(int l=0;l<26;l++)fscanf(t,"%d",&target[l]); fclose(t);} 
  double gbest=-1e18; int gm[200];
  for(int r=0;r<restarts;r++){
    // init: assign symbols to letters respecting target distribution cyclically
    int pool[400],np=0; for(int l=0;l<26;l++)for(int j=0;j<target[l];j++)pool[np++]=l;
    for(int i=np-1;i>0;i--){int j=rint_(i+1);int t=pool[i];pool[i]=pool[j];pool[j]=t;}
    memset(cnt,0,sizeof cnt);
    for(int k=0;k<K;k++){m[k]=pool[k%np];cnt[m[k]]++;}
    double cur=score_text()-pen(); double best=cur; int bm[200]; memcpy(bm,m,sizeof m);
    double T0=2.0,T1=0.05;
    for(long it=0;it<iters;it++){
      double T=T0*pow(T1/T0,(double)it/iters);
      int a=rint_(K); int old=m[a];
      if(rnd()<0.6){ // swap letters between two symbols
        int b=rint_(K); if(m[b]==old)continue; int ob=m[b];
        m[a]=ob;m[b]=old;
        double ns=score_text()-pen();
        if(ns>=cur||rnd()<exp((ns-cur)/T)){cur=ns;}else{m[a]=old;m[b]=ob;}
      } else { // reassign
        int nl=rint_(26); if(nl==old)continue;
        m[a]=nl;cnt[old]--;cnt[nl]++;
        double ns=score_text()-pen();
        if(ns>=cur||rnd()<exp((ns-cur)/T)){cur=ns;}else{m[a]=old;cnt[old]++;cnt[nl]--;}
      }
      if(cur>best){best=cur;memcpy(bm,m,sizeof m);}
    }
    if(best>gbest){gbest=best;memcpy(gm,bm,sizeof bm);
      printf("restart %d best %.2f\n",r,best); 
      for(int i=0;i<L;i++)putchar('a'+gm[cip[i]]);putchar('\n');
      fflush(stdout);
    }
  }
  printf("FINAL %.2f\nMAP",gbest); for(int k=0;k<K;k++)printf(" %d:%c",k,'a'+gm[k]); printf("\n");
  return 0;
}
