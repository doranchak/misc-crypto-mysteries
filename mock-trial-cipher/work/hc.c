// Hill-climb injective substitution solver with 5-gram scoring.
// usage: hc cipher.txt restarts iters seed  ; cipher.txt = space-separated ints (0..K-1), K<=26
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static float *T;
static int n, K, seq[4000];
static int map[26]; // symbol -> letter (0..25), symbols >=K unused
static inline double score(const int *m){
  double s=0; int idx;
  for(int i=0;i+4<n;i++){
    idx=(((m[seq[i]]*26+m[seq[i+1]])*26+m[seq[i+2]])*26+m[seq[i+3]])*26+m[seq[i+4]];
    s+=T[idx];
  }
  return s;
}
static unsigned long long rs;
static inline unsigned rnd(){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return (unsigned)(rs>>11); }
int main(int argc,char**argv){
  FILE*f=fopen("five.bin","rb"); T=malloc(26*26*26*26*26*sizeof(float)); fread(T,4,11881376,f); fclose(f);
  f=fopen(argv[1],"r"); n=0; K=0; int v; while(fscanf(f,"%d",&v)==1){seq[n++]=v; if(v+1>K)K=v+1;} fclose(f);
  int restarts=atoi(argv[2]); long iters=atol(argv[3]); rs=atoll(argv[4])*2654435761ULL+88172645463325252ULL;
  double best=-1e18; int bestmap[26];
  for(int r=0;r<restarts;r++){
    int perm[26]; for(int i=0;i<26;i++)perm[i]=i;
    for(int i=25;i>0;i--){int j=rnd()%(i+1);int t=perm[i];perm[i]=perm[j];perm[j]=t;}
    for(int i=0;i<26;i++)map[i]=perm[i];
    double cur=score(map);
    // simulated annealing
    double T0=60.0,T1=1.0;
    for(long it=0;it<iters;it++){
      double temp=T0*pow(T1/T0,(double)it/iters);
      int a=rnd()%K, b=rnd()%26;
      // swap map[a] with letter b: find symbol holding b
      int c=-1; for(int i=0;i<26;i++) if(map[i]==b){c=i;break;}
      int old=map[a];
      if(b==old) continue;
      map[a]=b; if(c>=0) map[c]=old;
      double ns=score(map);
      if(ns>=cur || exp((ns-cur)/temp)>(rnd()%1000000)/1e6){cur=ns;}
      else {map[a]=old; if(c>=0)map[c]=b;}
    }
    if(cur>best){best=cur;memcpy(bestmap,map,sizeof(map));}
  }
  printf("%.1f %.2f\n",best,best/(n-4));
  for(int i=0;i<K;i++)printf("%d:%c ",i,'A'+bestmap[i]); printf("\n");
  for(int i=0;i<n;i++)putchar('A'+bestmap[seq[i]]); putchar('\n');
  return 0;
}
