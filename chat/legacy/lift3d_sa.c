
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <limits.h>
#define MAXB 64
#define MAXE 128
#define MAXN 4096
#define MAXQ 81
static int D,Q,BN,BM,rootv,eu[MAXE],ev[MAXE],volt[MAXE],chord[MAXE],nchord;
static int LN,deg_[MAXN],nb_[MAXN][4],addtab[MAXQ][MAXQ];
static uint64_t rs[2];
static uint64_t xr(void){uint64_t a=rs[0],b=rs[1],r=a+b;b^=a;rs[0]=((a<<55)|(a>>9))^b^(b<<14);rs[1]=(b<<36)|(b>>28);return r;}
static int rnd(int n){return xr()%(uint64_t)n;}
static int vadd(int a,int b){int r=0,p=1;for(int k=0;k<D;k++){int x=(a%3+b%3)%3;r+=p*x;p*=3;a/=3;b/=3;}return r;}
static void initadd(void){for(int a=0;a<Q;a++)for(int b=0;b<Q;b++)addtab[a][b]=vadd(a,b);}
static void add(int a,int b){nb_[a][deg_[a]++]=b;nb_[b][deg_[b]++]=a;}
static void build(void){
 LN=Q*BN+Q/3;memset(deg_,0,sizeof(deg_));
 for(int e=0;e<BM;e++){int u=eu[e],v=ev[e],z=volt[e];for(int s=0;s<Q;s++)add(Q*u+s,Q*v+addtab[s][z]);}
 int cap=Q*BN;for(int p=0;p<Q/3;p++)for(int t=0;t<3;t++)add(cap+p,Q*rootv+(3*p+t));
}
static int Lt,used[MAXN],secondv,distv[MAXN];static long cnt,capcnt;
static int adjp(int a,int b){for(int k=0;k<deg_[a];k++)if(nb_[a][k]==b)return 1;return 0;}
static void bfs(int s){int q[MAXN],h=0,t=0;for(int i=0;i<LN;i++)distv[i]=INT_MAX/4;distv[s]=0;q[t++]=s;while(h<t){int u=q[h++];for(int k=0;k<deg_[u];k++){int v=nb_[u][k];if(v<s||distv[v]<INT_MAX/4)continue;distv[v]=distv[u]+1;q[t++]=v;}}}
static void dfs(int u,int d,int s){if(cnt>=capcnt)return;if(d==Lt-1){if(adjp(u,s)&&secondv<u)cnt++;return;}int rem=Lt-d-1;for(int k=0;k<deg_[u];k++){int w=nb_[u][k];if(w<=s||used[w]||distv[w]>rem)continue;used[w]=1;dfs(w,d+1,s);used[w]=0;if(cnt>=capcnt)return;}}
static long countc(int L,long cap){Lt=L;cnt=0;capcnt=cap;memset(used,0,sizeof(used));for(int s=0;s<LN&&cnt<cap;s++){bfs(s);used[s]=1;for(int k=0;k<deg_[s];k++){int w=nb_[s][k];if(w<=s||distv[w]>L-1)continue;secondv=w;used[w]=1;dfs(w,1,s);used[w]=0;if(cnt>=cap)break;}used[s]=0;}return cnt;}
static void printedge(FILE*f){fprintf(f,"p edge %d %d\n",LN,3*LN/2);for(int u=0;u<LN;u++)for(int k=0;k<deg_[u];k++)if(u<nb_[u][k])fprintf(f,"e %d %d\n",u+1,nb_[u][k]+1);}
static void readg6(const char*p){FILE*f=fopen(p,"r");if(!f){perror(p);exit(2);}int c=fgetc(f);if(c=='~'||c==EOF){fprintf(stderr,"short g6 only\n");exit(2);}BN=c-63;uint64_t ad[MAXB]={0};int val=0,bits=0;for(int j=1;j<BN;j++)for(int i=0;i<j;i++){if(!bits){val=fgetc(f)-63;bits=6;}if((val>>(--bits))&1){ad[i]|=1ULL<<j;ad[j]|=1ULL<<i;}}fclose(f);BM=0;rootv=-1;for(int i=0;i<BN;i++)if(__builtin_popcountll(ad[i])==2)rootv=i;for(int i=0;i<BN;i++){uint64_t x=ad[i];while(x){int j=__builtin_ctzll(x);x&=x-1;if(i<j){eu[BM]=i;ev[BM]=j;BM++;}}}int seen[MAXB]={0},st[MAXB],top=0,tree[MAXE]={0};seen[0]=1;st[top++]=0;while(top){int u=st[--top];for(int e=0;e<BM;e++){int v=eu[e]==u?ev[e]:ev[e]==u?eu[e]:-1;if(v>=0&&!seen[v]){seen[v]=1;tree[e]=1;st[top++]=v;}}}nchord=0;for(int e=0;e<BM;e++)if(!tree[e])chord[nchord++]=e;}
int main(int ac,char**av){if(ac<5){fprintf(stderr,"usage: base D seed moves\n");return 2;}readg6(av[1]);D=atoi(av[2]);Q=1;for(int i=0;i<D;i++)Q*=3;if(D<1||Q>MAXQ||Q*BN+Q/3>MAXN)return 2;initadd();uint64_t seed=strtoull(av[3],0,10);long moves=atol(av[4]);rs[0]=seed^0x9e3779b97f4a7c15ULL;rs[1]=seed*0xbf58476d1ce4e5b9ULL+1;for(int e=0;e<BM;e++)volt[e]=0;for(int i=0;i<nchord;i++)volt[chord[i]]=rnd(Q);build();long c8=countc(8,LONG_MAX),c16=-1,b8=c8,b16=LONG_MAX;int phase=1;double T=3;long stall=0;fprintf(stderr,"D=%d Q=%d n=%d rank=%d init8=%ld\n",D,Q,LN,nchord,c8);
for(long mv=1;mv<=moves;mv++){int e=chord[rnd(nchord)],old=volt[e];int coord=rnd(D),p=1;for(int k=0;k<coord;k++)p*=3;int digit=(old/p)%3,nd=(digit+1+rnd(2))%3,nw=old+(nd-digit)*p;volt[e]=nw;build();long n8=countc(8,LONG_MAX);int acc=0;long n16=-1;if(phase==1){long d=n8-c8;if(d<=0||exp(-(double)d/T)*4294967296.0>(double)(xr()&0xffffffffu))acc=1;}else if(n8==0){n16=countc(16,LONG_MAX);long d=n16-c16;if(d<=0||exp(-(double)d/(T<.2?.2:T))*4294967296.0>(double)(xr()&0xffffffffu))acc=1;}if(acc){c8=n8;if(phase==2&&n16>=0)c16=n16;stall=0;}else{volt[e]=old;build();stall++;}if(c8<b8){b8=c8;fprintf(stderr,"NEW8=%ld mv=%ld\n",b8,mv);}if(phase==1&&c8==0){c16=countc(16,LONG_MAX);b16=c16;phase=2;T=3;fprintf(stderr,"ENTER16=%ld mv=%ld\n",c16,mv);}if(phase==2&&c16<b16){b16=c16;fprintf(stderr,"NEW16=%ld mv=%ld\n",b16,mv);if(b16==0){fprintf(stderr,"*** SHORT ZERO ***\n");printedge(stdout);return 42;}}if(stall>100000){for(int e2=0;e2<BM;e2++)volt[e2]=0;for(int i=0;i<nchord;i++)volt[chord[i]]=rnd(Q);build();c8=countc(8,LONG_MAX);phase=1;T=3;stall=0;}if(mv%2000==0){T*=.995;if(T<.25)T=.25;fprintf(stderr,"mv=%ld p=%d c8=%ld c16=%ld b8=%ld b16=%ld\n",mv,phase,c8,c16,b8,b16);fflush(stderr);}}
fprintf(stderr,"DONE b8=%ld b16=%ld\n",b8,b16);return 0;}
