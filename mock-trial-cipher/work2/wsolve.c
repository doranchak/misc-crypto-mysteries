// Word-aware cell/step-model substitution solver.
// Glyph stream g[i] (0..K-1) with reset[i] (cursor returns to HOME before this glyph) and ws[i] (word starts here).
// token_i = STEP[token_{i-1}][d[g_i]]  (mode 1)   -- grid-walk with displacement class d[g] in [0,D)
// token_i = g_i                         (mode 0)   -- plain monoalphabetic
// token_i = ADD[A[g_i]][B[g_{i-1}]]     (mode 4)   -- previous-glyph modifier (B index K = 'start of word')
// letters = Lmap[token] (injective into 26 letters). Score = word-aware 4-gram log-prob (space = symbol 26).
// usage: wsolve data.txt step.txt mode restarts iters seed [T0 T1]
// data.txt: first line n K ; then n lines "g reset ws"
// step.txt: first line M D HOME ; then M lines of D ints (STEP[token][d])   (for mode 4: ADD table, D==M)
// env DFIX="file": D-assignment fixed (K ints) -> only Lmap searched (modes 1,4A)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define MAXN 6000
static float *LM; static int n,K,M,D,HOME,mode;
static int g[MAXN],rs_[MAXN],ws_[MAXN];
static int STEP[64][64];
static int dd[40]; static int Bm[41]; static int perm[26];
static int tok[MAXN];
static unsigned long long rs;
static inline unsigned rnd(){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return (unsigned)(rs>>11); }
static int fixd=0; static int dfix[40]; static int lfix=0; static int lfixv[64];
static inline void tokens(){
  int cur=HOME;
  if(mode==0){ for(int i=0;i<n;i++)tok[i]=g[i]; return; }
  if(mode==1){ for(int i=0;i<n;i++){ if(rs_[i])cur=HOME; cur=STEP[cur][dd[g[i]]]; tok[i]=cur; } return; }
  if(mode==4){ int prev=K; for(int i=0;i<n;i++){ if(ws_[i])prev=K; tok[i]=STEP[dd[g[i]]][Bm[prev]]; prev=g[i]; } return; }
}
static char buf[MAXN*2];
static double score(){
  tokens();
  int L=0; buf[L++]=26;
  for(int i=0;i<n;i++){ if(ws_[i]&&i>0)buf[L++]=26; buf[L++]=perm[tok[i]]; }
  buf[L++]=26;
  double s=0;
  for(int i=0;i+3<L;i++) s+=LM[(((buf[i]*27)+buf[i+1])*27+buf[i+2])*27+buf[i+3]];
  return s;
}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); fscanf(f,"%d %d",&n,&K); for(int i=0;i<n;i++)fscanf(f,"%d %d %d",&g[i],&rs_[i],&ws_[i]); fclose(f);
  f=fopen(argv[2],"r"); fscanf(f,"%d %d %d",&M,&D,&HOME); for(int i=0;i<M;i++)for(int j=0;j<D;j++)fscanf(f,"%d",&STEP[i][j]); fclose(f);
  mode=atoi(argv[3]); int restarts=atoi(argv[4]); long iters=atol(argv[5]); rs=atoll(argv[6])*2654435761ULL+88172645463325252ULL;
  double T0=argc>7?atof(argv[7]):4.0, T1=argc>8?atof(argv[8]):0.15;
  char*df=getenv("DFIX"); if(df){ f=fopen(df,"r"); for(int i=0;i<K;i++)fscanf(f,"%d",&dfix[i]); fclose(f); fixd=1; }
  char*lf=getenv("LFIX"); if(lf){ f=fopen(lf,"r"); for(int i=0;i<M;i++)fscanf(f,"%d",&lfixv[i]); fclose(f); lfix=1; }
  int cdmode=getenv("CD")?atoi(getenv("CD")):0; int nz=getenv("NOZERO")?1:0;
  f=fopen("lm4.bin","rb"); LM=malloc(27*27*27*27*sizeof(float)); fread(LM,4,27*27*27*27,f); fclose(f);
  if(mode==0) M=K;
  double best=-1e18; int bd[40],bB[41],bp[26];
  for(int r=0;r<restarts;r++){
    for(int i=0;i<26;i++)perm[i]=i; for(int i=25;i>0;i--){int j=rnd()%(i+1);int t=perm[i];perm[i]=perm[j];perm[j]=t;}
    for(int i=0;i<K;i++) dd[i]= fixd? dfix[i] : (nz? 1+(int)(rnd()%(D-1)) : (int)(rnd()%D));
    for(int i=0;i<=K;i++) Bm[i]=rnd()%D;
    if(lfix){ int used[26]={0}; for(int i=0;i<M;i++){perm[i]=lfixv[i];used[lfixv[i]]=1;} int k=M; for(int c=0;c<26;c++)if(!used[c])perm[k++]=c; }
    double cur=score();
    if(cdmode){
      int improved=1; int ord[40];
      while(improved){ improved=0;
        for(int i=0;i<K;i++)ord[i]=i; for(int i=K-1;i>0;i--){int j=rnd()%(i+1);int t=ord[i];ord[i]=ord[j];ord[j]=t;}
        for(int q=0;q<K;q++){ int gg=ord[q]; if(fixd)break; int bv=dd[gg]; double bs=cur; int ov=dd[gg];
          for(int v=0;v<D;v++){ if(v==ov||(nz&&v==0))continue; dd[gg]=v; double s=score(); if(s>bs+1e-9){bs=s;bv=v;} }
          dd[gg]=bv; if(bv!=ov){cur=bs;improved=1;} }
        if(!lfix){ for(int a=0;a<M;a++)for(int b=0;b<26;b++){ if(a==b)continue; int t=perm[a];perm[a]=perm[b];perm[b]=t; double s=score(); if(s>cur+1e-9){cur=s;improved=1;} else {t=perm[a];perm[a]=perm[b];perm[b]=t;} } }
      }
      if(cur>best){best=cur;memcpy(bd,dd,sizeof(dd));memcpy(bB,Bm,sizeof(Bm));memcpy(bp,perm,sizeof(perm));}
      continue;
    }
    for(long it=0;it<iters;it++){
      double temp=T0*pow(T1/T0,(double)it/iters);
      int mv=rnd()%100; double ns;
      int a,b,old,old2;
      if(!lfix && (mode==0 || mv<45 || (fixd&&mode==1))){ // swap letters among tokens
        a=rnd()%M; b=rnd()%26; if(a==b)continue; int t=perm[a];perm[a]=perm[b];perm[b]=t; ns=score();
        if(ns>=cur || exp((ns-cur)/temp)>(rnd()%1000000)/1e6) cur=ns; else {t=perm[a];perm[a]=perm[b];perm[b]=t;}
      } else if(mode==1 || (mode==4 && mv<75)){ if(fixd)continue; // change a displacement
        a=rnd()%K; old=dd[a]; dd[a]=rnd()%D; if(dd[a]==old)continue; ns=score();
        if(ns>=cur || exp((ns-cur)/temp)>(rnd()%1000000)/1e6) cur=ns; else dd[a]=old;
      } else { // mode 4: change B
        a=rnd()%(K+1); old=Bm[a]; Bm[a]=rnd()%D; if(Bm[a]==old)continue; ns=score();
        if(ns>=cur || exp((ns-cur)/temp)>(rnd()%1000000)/1e6) cur=ns; else Bm[a]=old;
      }
    }
    if(cur>best){best=cur;memcpy(bd,dd,sizeof(dd));memcpy(bB,Bm,sizeof(Bm));memcpy(bp,perm,sizeof(perm));}
  }
  memcpy(dd,bd,sizeof(dd));memcpy(Bm,bB,sizeof(Bm));memcpy(perm,bp,sizeof(perm));
  double sc=score();
  printf("SCORE %.2f\n",sc);
  printf("D"); for(int i=0;i<K;i++)printf(" %d",dd[i]); printf("\n");
  printf("B"); for(int i=0;i<=K;i++)printf(" %d",Bm[i]); printf("\n");
  printf("L"); for(int i=0;i<M;i++)printf(" %c",'A'+perm[i]); printf("\n");
  printf("T "); for(int i=0;i<n;i++){ if(ws_[i]&&i>0)putchar(' '); putchar('A'+perm[tok[i]]); } printf("\n");
  return 0;
}
