/* Z3-lift annealer over a one-degree-2 alpha-block base.
 * The three lifted degree-2 vertices are joined to a new hub, yielding a cubic graph.
 * Phase 1 minimizes exact C8 count; phase 2 (when C8=0) minimizes exact C16.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#define MAXB 64
#define MAXE 128
#define MAXN 256
static int BN, BM, rootv, eu[MAXE], ev[MAXE], eid[MAXB][MAXB];
static int volt[MAXE], chord[MAXE], nchord;
static int LN, deg_[MAXN], nb_[MAXN][4];
static uint64_t rs[2];
static uint64_t xr(void){uint64_t s0=rs[0],s1=rs[1],r=s0+s1;s1^=s0;rs[0]=((s0<<55)|(s0>>9))^s1^(s1<<14);rs[1]=(s1<<36)|(s1>>28);return r;}
static int rnd(int n){return (int)(xr()%(uint64_t)n);}
static void add(int a,int b){nb_[a][deg_[a]++]=b;nb_[b][deg_[b]++]=a;}
static void build(void){
 LN=3*BN+1; memset(deg_,0,sizeof(deg_));
 for(int e=0;e<BM;e++){int u=eu[e],v=ev[e],z=volt[e];for(int s=0;s<3;s++)add(3*u+s,3*v+(s+z)%3);}
 int hub=3*BN;for(int s=0;s<3;s++)add(hub,3*rootv+s);
}
static int Lt, used[MAXN], pathv[32], secondv; static long cnt; static long capcnt;
static int adjacent(int a,int b){for(int k=0;k<deg_[a];k++)if(nb_[a][k]==b)return 1;return 0;}
static void dfs_cycle(int u,int depth,int s){
 if(cnt>=capcnt)return;
 pathv[depth]=u;
 if(depth==Lt-1){if(adjacent(u,s)&&secondv<u)cnt++;return;}
 for(int k=0;k<deg_[u];k++){int w=nb_[u][k];if(w<=s||used[w])continue;used[w]=1;dfs_cycle(w,depth+1,s);used[w]=0;if(cnt>=capcnt)return;}
}
static long countc(int L,long cap){
 Lt=L;cnt=0;capcnt=cap;memset(used,0,sizeof(used));
 for(int s=0;s<LN;s++){used[s]=1;pathv[0]=s;for(int k=0;k<deg_[s];k++){int w=nb_[s][k];if(w<=s)continue;secondv=w;used[w]=1;dfs_cycle(w,1,s);used[w]=0;if(cnt>=capcnt){used[s]=0;return cnt;}}used[s]=0;}
 return cnt;
}
static void print_edge(FILE*f){fprintf(f,"p edge %d %d\n",LN,3*BM+3);for(int u=0;u<LN;u++)for(int k=0;k<deg_[u];k++)if(u<nb_[u][k])fprintf(f,"e %d %d\n",u+1,nb_[u][k]+1);}
static void readg6(const char *p){
 FILE*f=fopen(p,"r");if(!f){perror(p);exit(2);}int c=fgetc(f);if(c=='~'||c==EOF){fprintf(stderr,"short graph6 required\n");exit(2);}BN=c-63;uint64_t adj[MAXB]={0};int val=0,bits=0;
 for(int j=1;j<BN;j++)for(int i=0;i<j;i++){if(!bits){val=fgetc(f)-63;bits=6;}int b=(val>>(--bits))&1;if(b){adj[i]|=1ULL<<j;adj[j]|=1ULL<<i;}}fclose(f);
 BM=0;memset(eid,-1,sizeof(eid));rootv=-1;for(int i=0;i<BN;i++)if(__builtin_popcountll(adj[i])==2)rootv=i;
 for(int i=0;i<BN;i++){uint64_t x=adj[i];while(x){int j=__builtin_ctzll(x);x&=x-1;if(i<j){eu[BM]=i;ev[BM]=j;eid[i][j]=eid[j][i]=BM++;}}}
 if(rootv<0){fprintf(stderr,"no degree2 root\n");exit(2);}
 /* DFS spanning tree; mutate only cotree voltages (gauge-fixed). */
 int seen[MAXB]={0},stack[MAXB],top=0,tree[MAXE]={0};seen[0]=1;stack[top++]=0;
 while(top){int u=stack[--top];for(int e=0;e<BM;e++){int v=-1;if(eu[e]==u)v=ev[e];else if(ev[e]==u)v=eu[e];if(v>=0&&!seen[v]){seen[v]=1;tree[e]=1;stack[top++]=v;}}}
 nchord=0;for(int e=0;e<BM;e++)if(!tree[e])chord[nchord++]=e;
 fprintf(stderr,"base n=%d m=%d root=%d cycle_rank=%d lift_n=%d\n",BN,BM,rootv,nchord,3*BN+1);
}
int main(int ac,char**av){if(ac<4){fprintf(stderr,"usage: %s base.g6 seed moves\n",av[0]);return 2;}readg6(av[1]);uint64_t seed=strtoull(av[2],0,10);long moves=atol(av[3]);rs[0]=seed^0x9e3779b97f4a7c15ULL;rs[1]=seed*0xbf58476d1ce4e5b9ULL+1;
 for(int e=0;e<BM;e++)volt[e]=0;for(int i=0;i<nchord;i++)volt[chord[i]]=rnd(3);build();long c8=countc(8,1L<<60),best8=c8,best16=1L<<60;double T=3.0;int phase=1;long stall=0;
 fprintf(stderr,"init c8=%ld\n",c8);
 for(long mv=1;mv<=moves;mv++){
   int ii=rnd(nchord),e=chord[ii],old=volt[e],nv=(old+1+rnd(2))%3;volt[e]=nv;build();long n8=countc(8,1L<<60);int accept=0;
   if(phase==1){long d=n8-c8;if(d<=0||exp(-(double)d/T)*4294967296.0>(double)(xr()&0xffffffffu))accept=1;}
   else {if(n8==0){long n16=countc(16,1L<<60);long d=n16-best16;if(d<=0||exp(-(double)d/(T<.2?.2:T))*4294967296.0>(double)(xr()&0xffffffffu)){accept=1;if(n16<best16){best16=n16;fprintf(stderr,"NEW phase2 c16=%ld mv=%ld\n",n16,mv);FILE*f=fopen("lift3_best.edge","w");print_edge(f);fclose(f);if(n16==0){fprintf(stderr,"*** SHORT ZERO ***\n");print_edge(stdout);return 42;}}}}}
   if(accept){c8=n8;stall=0;}else{volt[e]=old;build();stall++;}
   if(n8<best8){best8=n8;fprintf(stderr,"NEW c8=%ld mv=%ld\n",best8,mv);if(best8==0){long c16=countc(16,1L<<60);best16=c16;phase=2;T=2.0;fprintf(stderr,"ENTER phase2 c16=%ld\n",c16);FILE*f=fopen("lift3_best.edge","w");print_edge(f);fclose(f);if(c16==0){print_edge(stdout);return 42;}}}
   if(mv%2000==0){if(phase==1){T*=.995;if(T<.25)T=.25;}else{T*=.997;if(T<.15)T=.15;}fprintf(stderr,"mv=%ld phase=%d cur8=%ld best8=%ld best16=%ld T=%.3f\n",mv,phase,c8,best8,best16,T);fflush(stderr);}
   if(stall>200000&&phase==1){for(int i=0;i<nchord;i++)volt[chord[i]]=rnd(3);build();c8=countc(8,1L<<60);T=2.0;stall=0;}
 }
 fprintf(stderr,"DONE best8=%ld best16=%ld\n",best8,best16);return 0;}
