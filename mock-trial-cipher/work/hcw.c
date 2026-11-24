// word-aware hill-climb: seq of ints, -1 = word boundary. 27-symbol 4-gram log-prob table (0=space,1..26)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static float *T; static int n, K, seq[6000];
static int map[26];
static unsigned long long rs;
static inline unsigned rnd(){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return (unsigned)(rs>>11); }
static inline double score(const int*m){
  double s=0; int a=0,b=0,c=0;
  for(int i=0;i<n;i++){
    int d = seq[i]<0 ? 0 : m[seq[i]]+1;
    s+=T[((a*27+b)*27+c)*27+d]; a=b;b=c;c=d;
  }
  return s;
}
int main(int argc,char**argv){
  FILE*f=fopen("quad_sp.bin","rb"); T=malloc(27*27*27*27*4); fread(T,4,27*27*27*27,f); fclose(f);
  f=fopen(argv[1],"r"); n=0;K=0;int v; while(fscanf(f,"%d",&v)==1){seq[n++]=v; if(v+1>K)K=v+1;} fclose(f);
  int restarts=atoi(argv[2]); long iters=atol(argv[3]); rs=atoll(argv[4])*2654435761ULL+88172645463325252ULL;
  double best=-1e18; int bestmap[26];
  for(int r=0;r<restarts;r++){
    int perm[26]; for(int i=0;i<26;i++)perm[i]=i;
    for(int i=25;i>0;i--){int j=rnd()%(i+1);int t=perm[i];perm[i]=perm[j];perm[j]=t;}
    memcpy(map,perm,sizeof(map));
    double cur=score(map);
    double T0=3.0,T1=0.05;
    for(long it=0;it<iters;it++){
      double temp=T0*pow(T1/T0,(double)it/iters);
      int a=rnd()%K,b=rnd()%26; int c=-1; for(int i=0;i<26;i++) if(map[i]==b){c=i;break;}
      int old=map[a]; if(b==old) continue;
      map[a]=b; if(c>=0)map[c]=old;
      double ns=score(map);
      if(ns>=cur || exp((ns-cur)/temp)>(rnd()%1000000)/1e6) cur=ns;
      else {map[a]=old; if(c>=0)map[c]=b;}
    }
    if(cur>best){best=cur;memcpy(bestmap,map,sizeof(map));}
  }
  int nl=0; for(int i=0;i<n;i++) if(seq[i]>=0) nl++;
  printf("%.2f %.4f\n",best,best/nl);
  for(int i=0;i<K;i++)printf("%d:%c ",i,'A'+bestmap[i]); printf("\n");
  for(int i=0;i<n;i++) putchar(seq[i]<0?' ':'A'+bestmap[seq[i]]); putchar('\n');
  return 0;
}
