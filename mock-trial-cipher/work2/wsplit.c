// Latent-subclass substitution solver: some glyph classes are split into k hidden subclasses (per-occurrence labels).
// usage: wsplit data.txt restarts iters seed T0 T1   env SPLIT="cls:k,cls:k"
// data.txt: "n K" then n lines "g reset ws"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define MAXN 6000
static float *LM; static int n,K;
static int g[MAXN],ws_[MAXN],lab[MAXN],tok[MAXN];
static int ksplit[40], base[40]; // base token id for subclass 0 = class id; sub s>=1 -> extra[...]
static int extra0[40]; // first extra token id for class
static int M, perm[40]; static int NN=6; static double NP=3.0; static int homo=0; static double CHI=0.0;
static const double EF[26]={8.17,1.49,2.78,4.25,12.70,2.23,2.02,6.09,6.97,0.15,0.77,4.03,2.41,6.75,7.51,1.93,0.10,5.99,6.33,9.06,2.76,0.98,2.36,0.15,1.97,0.07};
static unsigned long long rs;
static inline unsigned rnd(){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return (unsigned)(rs>>11); }
static char buf[MAXN*2];
static inline void toks(){ for(int i=0;i<n;i++){ int c=g[i]; tok[i]= (ksplit[c]>1 && lab[i]>0)? extra0[c]+lab[i]-1 : c; } }
static double score(){
  toks(); int nn_=0;
  int L=0; buf[L++]=26;
  for(int i=0;i<n;i++){ if(ws_[i]&&i>0)buf[L++]=26; if(perm[tok[i]]<26) buf[L++]=perm[tok[i]]; else nn_++; }
  buf[L++]=26;
  double s=0;
  if(CHI>0){ int cnt[26]={0}; int nl=0; for(int i=0;i<L;i++) if(buf[i]<26){cnt[(int)buf[i]]++;nl++;} double ch=0; for(int c=0;c<26;c++){ double e=nl*EF[c]/100.0; double d=cnt[c]-e; ch+=d*d/(e>3?e:3);} s-=CHI*ch; }
  for(int i=0;i+3<L;i++) s+=LM[(((buf[i]*27)+buf[i+1])*27+buf[i+2])*27+buf[i+3]];
  return s-NP*nn_;
}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); int rr; fscanf(f,"%d %d",&n,&K); for(int i=0;i<n;i++)fscanf(f,"%d %d %d",&g[i],&rr,&ws_[i]); fclose(f);
  int restarts=atoi(argv[2]); long iters=atol(argv[3]); rs=atoll(argv[4])*2654435761ULL+88172645463325252ULL;
  double T0=atof(argv[5]),T1=atof(argv[6]);
  for(int i=0;i<K;i++)ksplit[i]=1;
  M=K; char*sp=getenv("SPLIT"); if(sp){ char*p=sp; int c,k; while(sscanf(p,"%d:%d",&c,&k)==2){ ksplit[c]=k; extra0[c]=M; M+=k-1; char*q=strchr(p,','); if(!q)break; p=q+1; } }
  if(getenv("HOMO"))homo=1; if(getenv("CHI"))CHI=atof(getenv("CHI")); if(getenv("NN"))NN=atoi(getenv("NN")); if(getenv("NP"))NP=atof(getenv("NP")); int NS=26+NN; if(M>NS && !homo){fprintf(stderr,"M=%d>%d\n",M,NS);return 1;}
  f=fopen("lm4.bin","rb"); LM=malloc(27*27*27*27*sizeof(float)); fread(LM,4,27*27*27*27,f); fclose(f);
  int idxs[MAXN],ni=0; for(int i=0;i<n;i++) if(ksplit[g[i]]>1) idxs[ni++]=i;
  double best=-1e18; int bl[MAXN],bp[40];
  for(int r=0;r<restarts;r++){
    for(int i=0;i<NS;i++)perm[i]=i; for(int i=NS-1;i>0;i--){int j=rnd()%(i+1);int t=perm[i];perm[i]=perm[j];perm[j]=t;}
    if(homo) for(int i=0;i<M;i++) perm[i]=rnd()%NS;
    for(int i=0;i<n;i++) lab[i]= ksplit[g[i]]>1 ? rnd()%ksplit[g[i]] : 0;
    double cur=score();
    for(long it=0;it<iters;it++){
      double temp=T0*pow(T1/T0,(double)it/iters);
      int mv=rnd()%100; double ns;
      if(mv<35 || ni==0){
        if(homo){ int a=rnd()%M,b=rnd()%NS; int old=perm[a]; if(old==b)continue; perm[a]=b; ns=score(); if(ns>=cur||exp((ns-cur)/temp)>(rnd()%1000000)/1e6)cur=ns; else perm[a]=old; } else {
        int a=rnd()%M,b=rnd()%NS; if(a==b)continue; int t=perm[a];perm[a]=perm[b];perm[b]=t; ns=score();
        if(ns>=cur||exp((ns-cur)/temp)>(rnd()%1000000)/1e6)cur=ns; else {t=perm[a];perm[a]=perm[b];perm[b]=t;} }
      } else {
        int i=idxs[rnd()%ni]; int old=lab[i]; lab[i]=rnd()%ksplit[g[i]]; if(lab[i]==old)continue; ns=score();
        if(ns>=cur||exp((ns-cur)/temp)>(rnd()%1000000)/1e6)cur=ns; else lab[i]=old;
      }
    }
    // greedy polish: sweep labels and swaps until stable
    int improved=1;
    while(improved){ improved=0;
      for(int q=0;q<ni;q++){ int i=idxs[q]; int ol=lab[i],bv=ol; double bs=cur; for(int v=0;v<ksplit[g[i]];v++){ if(v==ol)continue; lab[i]=v; double s=score(); if(s>bs+1e-9){bs=s;bv=v;} } lab[i]=bv; if(bv!=ol){cur=bs;improved=1;} }
      if(homo){ for(int a=0;a<M;a++)for(int b=0;b<NS;b++){ int old=perm[a]; if(old==b)continue; perm[a]=b; double s=score(); if(s>cur+1e-9){cur=s;improved=1;} else perm[a]=old; } } else for(int a=0;a<M;a++)for(int b=0;b<NS;b++){ if(a==b)continue; int t=perm[a];perm[a]=perm[b];perm[b]=t; double s=score(); if(s>cur+1e-9){cur=s;improved=1;} else {t=perm[a];perm[a]=perm[b];perm[b]=t;} }
    }
    if(cur>best){best=cur;memcpy(bl,lab,sizeof(int)*n);memcpy(bp,perm,sizeof(perm));}
  }
  memcpy(lab,bl,sizeof(int)*n);memcpy(perm,bp,sizeof(perm)); double sc=score();
  printf("SCORE %.2f\n",sc);
  printf("L"); for(int i=0;i<M;i++)printf(" %c",perm[i]<26?'A'+perm[i]:'_'); printf("\n");
  printf("LAB"); for(int i=0;i<n;i++)printf(" %d",lab[i]); printf("\n");
  printf("T "); for(int i=0;i<n;i++){ if(ws_[i]&&i>0)putchar(' '); if(perm[tok[i]]<26)putchar('A'+perm[tok[i]]); else putchar('_'); } printf("\n");
  return 0;
}
