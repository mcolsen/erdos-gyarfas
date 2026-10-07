/* Exact cycle-polynomial search for cubic graphs assembled from 3- and 7-vertex cells.
 * Input: n then n rows: type(0=triangle,1=7-cell), special slot, three neighbours (zero-based).
 * Usage: core_search input out seconds seed [temperature] [objective_mode] [max_moves]
 * Every accepted state is exactly C4,C8,C16-free. C32 is counted, not sampled.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <assert.h>
#include <limits.h>
#define V 128
typedef __uint128_t Mask;
#define R 17
typedef struct{int n,nb[V][3],t[V],sp[V];}Graph;
static uint64_t W[R][R][R];
static uint64_t rng;
static int objective_mode=0;
static uint64_t rand64(void){rng^=rng<<13;rng^=rng>>7;rng^=rng<<17;return rng;}
static int ri(int n){return rand64()%n;}
static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return t.tv_sec+1e-9*t.tv_nsec;}
static void weights(void){for(int r=3;r<R;r++)for(int s=0;s<=r;s++)for(int q=0;q<=s;q++){
 int shift=2*r+s+q; if(shift>32)continue;
 uint64_t p[33]={1},z[33];
 for(int j=0;j<r+2*q;j++){memset(z,0,sizeof(z));for(int i=0;i<=32;i++){z[i]+=p[i];if(i+1<=32)z[i+1]+=p[i];}memcpy(p,z,sizeof(p));}
 for(int j=0;j<s-q;j++){memset(z,0,sizeof(z));for(int i=0;i<=32;i++){z[i]+=p[i];if(i+2<=32)z[i+2]+=p[i];if(i+3<=32)z[i+3]+=p[i];}memcpy(p,z,sizeof(p));}
 W[r][s][q]=p[32-shift];
}}
typedef struct{const Graph*g;int root,first,maxlen,dist[V];uint64_t total;int bad;}Ctx;
static int turn(const Graph*g,int u,int a,int b){int v=g->nb[u][g->sp[u]];return g->t[u]&&(v!=a&&v!=b);}
static void dfs(Ctx*c,int prev,int u,int r,int s,int q,Mask mask){
 const Graph*g=c->g;if(2*r+s+q+2*(c->dist[u]-1)>c->maxlen)return;
 for(int k=0;k<3;k++){int v=g->nb[u][k];
  if(v==c->root){if(r>=3&&c->first<u){int qq=q+turn(g,u,prev,v)+turn(g,v,u,c->first);int lo=2*r+s+qq,hi=3*r+4*s;
    if(c->maxlen==16){if((lo<=4&&hi>=4)||(lo<=8&&hi>=8)||(lo<=16&&hi>=16)){c->bad=1;return;}}
    else if(r<R)c->total += objective_mode ? (uint64_t)((lo<=32&&hi>=32)?(objective_mode==2 ? (1+(32-lo<hi-32 ? 32-lo:hi-32)):1):0) : W[r][s][qq];
   }continue;}
  if(v<c->root||(mask&(((Mask)1)<<v)))continue;
  int ss=s+g->t[v],qq=q+turn(g,u,prev,v);if(2*(r+1)+ss+qq>c->maxlen)continue;
  dfs(c,u,v,r+1,ss,qq,mask|(((Mask)1)<<v));if(c->bad)return;
 }
}
static uint64_t calc(const Graph*g,int maxlen){Ctx c;memset(&c,0,sizeof(c));c.g=g;c.maxlen=maxlen;
 for(int root=0;root<g->n;root++){c.root=root;int qu[V],a=0,b=0;for(int i=0;i<g->n;i++)c.dist[i]=100;c.dist[root]=0;qu[b++]=root;
  while(a<b){int u=qu[a++];for(int k=0;k<3;k++){int v=g->nb[u][k];if(v<root||c.dist[v]!=100)continue;c.dist[v]=c.dist[u]+1;qu[b++]=v;}}
  for(int k=0;k<3;k++){int v=g->nb[root][k];if(v<=root)continue;c.first=v;dfs(&c,root,v,2,g->t[root]+g->t[v],0,(((Mask)1)<<root)|(((Mask)1)<<v));if(c.bad)return 1;}
 }return c.total;
}
static void save(const Graph*g,const char*name){char tmp[1024];snprintf(tmp,sizeof(tmp),"%s.tmp",name);FILE*f=fopen(tmp,"w");if(!f){perror(tmp);exit(2);}fprintf(f,"%d\n",g->n);for(int i=0;i<g->n;i++)fprintf(f,"%d %d %d %d %d\n",g->t[i],g->sp[i],g->nb[i][0],g->nb[i][1],g->nb[i][2]);fclose(f);if(rename(tmp,name)){perror("rename");exit(2);}}
static int adjacent(const Graph*g,int u,int v){for(int k=0;k<3;k++)if(g->nb[u][k]==v)return k;return -1;}
static int sw(Graph*g){int a=ri(g->n),ia=ri(3),b=g->nb[a][ia],ib=adjacent(g,b,a);int c=ri(g->n),ic=ri(3),d=g->nb[c][ic],id=adjacent(g,d,c);
 if(a==c||a==d||b==c||b==d||adjacent(g,a,c)>=0||adjacent(g,b,d)>=0)return 0;
 g->nb[a][ia]=c;g->nb[c][ic]=a;g->nb[b][ib]=d;g->nb[d][id]=b;return 1;
}
int main(int ac,char**av){if(ac<5){fprintf(stderr,"usage input out seconds seed [temperature] [objective_mode] [max_moves]\n");return 2;}Graph g;FILE*f=fopen(av[1],"r");if(!f)return 2;if(fscanf(f,"%d",&g.n)!=1||g.n<4||g.n>127)return 2;
 for(int i=0;i<g.n;i++){if(fscanf(f,"%d%d%d%d%d",g.t+i,g.sp+i,g.nb[i],g.nb[i]+1,g.nb[i]+2)!=5)return 2;}
 fclose(f);
 for(int i=0;i<g.n;i++){if(g.t[i]<0||g.t[i]>1||g.sp[i]<0||g.sp[i]>2)return 2;for(int k=0;k<3;k++){if(g.nb[i][k]<0||g.nb[i][k]>=g.n||g.nb[i][k]==i)return 2;for(int j=0;j<k;j++)if(g.nb[i][j]==g.nb[i][k])return 2;}}
 for(int i=0;i<g.n;i++)for(int k=0;k<3;k++)assert(adjacent(&g,g.nb[i][k],i)>=0);
 objective_mode=ac>6?atoi(av[6]):0;weights();rng=strtoull(av[4],0,10)+1;double secs=atof(av[3]),temp=ac>5?atof(av[5]):2000.,start=now();
 if(calc(&g,16)){fprintf(stderr,"input not short-free\n");return 3;}uint64_t cur=calc(&g,32),best=cur;Graph bestg=g;save(&g,av[2]);fprintf(stderr,"initial=%llu\n",(unsigned long long)cur);fflush(stderr);
 long moves=0,valid=0,accepted=0,maxmoves=ac>7?strtol(av[7],0,10):LONG_MAX;for(;moves<maxmoves&&now()-start<secs;moves++){
 Graph h=g;int mode=ri(100),ok=1;
 if(mode<50)ok=sw(&h);
 else if(mode<70){int v=ri(g.n);if(!h.t[v])continue;h.sp[v]=(h.sp[v]+1+ri(2))%3;}
 else if(mode<90){int a=ri(g.n),b=ri(g.n);if(h.t[a]==h.t[b])continue;int t=h.t[a];h.t[a]=h.t[b];h.t[b]=t;h.sp[a]=ri(3);h.sp[b]=ri(3);}
 else{int n=2+ri(3);for(int i=0;i<n;i++)if(!sw(&h)){ok=0;break;}}
 if(!ok||calc(&h,16)){continue;}
 valid++;uint64_t val=calc(&h,32);
 double T=temp*pow(0.01,(double)(moves%10000)/10000.0);
 if(val<=cur||((double)(rand64()>>11)/9007199254740992.)<exp(((double)cur-(double)val)/T)){
  g=h;cur=val;accepted++;
  if(val<best){best=val;bestg=g;save(&g,av[2]);fprintf(stderr,"best=%llu moves=%ld valid=%ld accepted=%ld t=%.3f\n",(unsigned long long)best,moves,valid,accepted,now()-start);fflush(stderr);if(!best)break;}
 }
 if(moves%30000==29999){g=bestg;cur=best;}
 }
 fprintf(stderr,"DONE best=%llu moves=%ld valid=%ld accepted=%ld elapsed=%.3f\n",(unsigned long long)best,moves,valid,accepted,now()-start);return 0;
}
