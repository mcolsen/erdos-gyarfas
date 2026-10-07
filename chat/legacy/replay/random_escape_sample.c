#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <limits.h>
#include <omp.h>
#define MAXN 256
#define MAXE 512

typedef struct{int n,m;unsigned char A[MAXN][MAXN];uint16_t nb[MAXN][4];unsigned char deg[MAXN];}Graph;
typedef struct{int L,second;long cap,cnt;unsigned char used[MAXN];uint16_t dist[MAXN];}Ctx;
typedef struct{uint16_t a,b,c,d;unsigned char o;}Cand;
#define MAXPATH 1024
#define MAXW 4
typedef struct{uint64_t mask[MAXW];uint16_t end;}Path;
typedef struct{Path p1[MAXPATH],p2[MAXPATH];int pc1,pc2,head2[MAXN],next2[MAXPATH];int target,which,skipu,skipv,words;unsigned char used[MAXN];uint16_t verts[32];}ShortCtx;
static void enumhalf(const Graph*g,ShortCtx*c,int u,int depth,Path*P,int*pc){c->verts[depth]=u;if(depth==c->target){if(*pc>=MAXPATH)exit(5);int ix=(*pc)++;memset(P[ix].mask,0,sizeof(P[ix].mask));for(int i=0;i<=depth;i++){int v=c->verts[i];P[ix].mask[v>>6]|=1ULL<<(v&63);}P[ix].end=u;if(c->which==2){c->next2[ix]=c->head2[u];c->head2[u]=ix;}return;}for(int k=0;k<g->deg[u];k++){int v=g->nb[u][k];if((u==c->skipu&&v==c->skipv)||(u==c->skipv&&v==c->skipu)||c->used[v])continue;c->used[v]=1;enumhalf(g,c,v,depth+1,P,pc);c->used[v]=0;}}
static int edgecloses(const Graph*g,ShortCtx*c,int s,int t,int L){int k=L-1,h1=k/2,h2=k-h1;c->skipu=s;c->skipv=t;c->pc1=c->pc2=0;c->words=(g->n+63)/64;for(int i=0;i<g->n;i++)c->head2[i]=-1;c->which=1;memset(c->used,0,sizeof(c->used));c->used[s]=1;c->verts[0]=s;c->target=h1;enumhalf(g,c,s,0,c->p1,&c->pc1);c->which=2;memset(c->used,0,sizeof(c->used));c->used[t]=1;c->verts[0]=t;c->target=h2;enumhalf(g,c,t,0,c->p2,&c->pc2);for(int i=0;i<c->pc1;i++){int e=c->p1[i].end;for(int j=c->head2[e];j>=0;j=c->next2[j]){int ok=1;for(int w=0;w<c->words;w++){uint64_t inter=c->p1[i].mask[w]&c->p2[j].mask[w],want=(w==(e>>6))?(1ULL<<(e&63)):0;if(inter!=want){ok=0;break;}}if(ok)return 1;}}return 0;}
static int newshort(const Graph*g,ShortCtx*c,int a,int x,int b,int y){return edgecloses(g,c,a,x,4)||edgecloses(g,c,b,y,4)||edgecloses(g,c,a,x,8)||edgecloses(g,c,b,y,8)||edgecloses(g,c,a,x,16)||edgecloses(g,c,b,y,16);}
static int load(const char*p,Graph*g){memset(g,0,sizeof(*g));FILE*f=fopen(p,"r");if(!f){perror(p);return 0;}char t;int a,b,m;while(fscanf(f," %c",&t)==1){if(t=='p'){char w[16];fscanf(f,"%15s%d%d",w,&g->n,&m);}else if(t=='e'){fscanf(f,"%d%d",&a,&b);--a;--b;g->A[a][b]=g->A[b][a]=1;}else{char z[1024];fgets(z,sizeof(z),f);}}fclose(f);memset(g->deg,0,sizeof(g->deg));for(int i=0;i<g->n;i++)for(int j=0;j<g->n;j++)if(g->A[i][j])g->nb[i][g->deg[i]++]=j;g->m=0;for(int i=0;i<g->n;i++)g->m+=g->deg[i];g->m/=2;return 1;}
static void rebuild(Graph*g){memset(g->deg,0,sizeof(g->deg));for(int i=0;i<g->n;i++)for(int j=0;j<g->n;j++)if(g->A[i][j])g->nb[i][g->deg[i]++]=j;}
static void save(const char*p,const Graph*g){FILE*f=fopen(p,"w");fprintf(f,"p edge %d %d\n",g->n,g->m);for(int i=0;i<g->n;i++)for(int j=i+1;j<g->n;j++)if(g->A[i][j])fprintf(f,"e %d %d\n",i+1,j+1);fclose(f);}
static void bfs(const Graph*g,Ctx*c,int s){uint16_t q[MAXN];int h=0,t=0;for(int i=0;i<g->n;i++)c->dist[i]=UINT16_MAX;c->dist[s]=0;q[t++]=s;while(h<t){int u=q[h++];for(int k=0;k<g->deg[u];k++){int v=g->nb[u][k];if(v<s||c->dist[v]!=UINT16_MAX)continue;c->dist[v]=c->dist[u]+1;q[t++]=v;}}}
static void dfs(const Graph*g,Ctx*c,int u,int d,int s){if(c->cnt>=c->cap)return;if(d==c->L-1){if(g->A[u][s]&&c->second<u)c->cnt++;return;}int rem=c->L-d-1;for(int k=0;k<g->deg[u];k++){int v=g->nb[u][k];if(v<=s||c->used[v]||c->dist[v]>rem)continue;c->used[v]=1;dfs(g,c,v,d+1,s);c->used[v]=0;if(c->cnt>=c->cap)return;}}
static long countc(const Graph*g,int L,long cap){Ctx c;memset(&c,0,sizeof(c));c.L=L;c.cap=cap;for(int s=0;s<g->n&&c.cnt<cap;s++){bfs(g,&c,s);c.used[s]=1;for(int k=0;k<g->deg[s];k++){int v=g->nb[s][k];if(v<=s||c.dist[v]>L-1)continue;c.second=v;c.used[v]=1;dfs(g,&c,v,1,s);c.used[v]=0;if(c.cnt>=cap)break;}c.used[s]=0;}return c.cnt;}
static uint64_t R[2];static uint64_t xr(void){uint64_t a=R[0],b=R[1],r=a+b;b^=a;R[0]=((a<<55)|(a>>9))^b^(b<<14);R[1]=(b<<36)|(b>>28);return r;}
int main(int ac,char**av){if(ac<8){fprintf(stderr,"usage in out seed threads samples target report\n");return 2;}Graph base;if(!load(av[1],&base))return 2;uint64_t seed=strtoull(av[3],0,10);int th=atoi(av[4]);long samples=atol(av[5]),target=atol(av[6]);const char*report=av[7];R[0]=seed^0x9e3779b97f4a7c15ULL;R[1]=seed*0xbf58476d1ce4e5b9ULL+1;int eu[MAXE],ev[MAXE],M=0;for(int i=0;i<base.n;i++)for(int j=i+1;j<base.n;j++)if(base.A[i][j]){eu[M]=i;ev[M]=j;M++;}Cand*cs=malloc((long)M*(M-1)*sizeof(Cand));long nc=0;for(int i=0;i<M;i++)for(int j=i+1;j<M;j++){int a=eu[i],b=ev[i],c=eu[j],d=ev[j];if(a==c||a==d||b==c||b==d)continue;if(!base.A[a][c]&&!base.A[b][d])cs[nc++]=(Cand){a,b,c,d,0};if(!base.A[a][d]&&!base.A[b][c])cs[nc++]=(Cand){a,b,c,d,1};}for(long i=nc-1;i>0;i--){long j=xr()%(i+1);Cand q=cs[i];cs[i]=cs[j];cs[j]=q;}if(samples>nc)samples=nc;long best=target,valid=0;Graph bg=base;Cand bq={0};double t0=omp_get_wtime();omp_set_num_threads(th);
#pragma omp parallel
 {Graph g;ShortCtx sc;
#pragma omp for schedule(dynamic,8) reduction(+:valid)
  for(long z=0;z<samples;z++){g=base;Cand q=cs[z];int a=q.a,b=q.b,c=q.c,d=q.d,x=q.o?d:c,y=q.o?c:d;g.A[a][b]=g.A[b][a]=0;g.A[c][d]=g.A[d][c]=0;g.A[a][x]=g.A[x][a]=1;g.A[b][y]=g.A[y][b]=1;rebuild(&g);if(newshort(&g,&sc,a,x,b,y))continue;valid++;long v=countc(&g,32,target);if(v<target){
#pragma omp critical
   {if(v<best){best=v;bg=g;bq=q;}}
  }}
 }
 FILE*f=fopen(report,"a");fprintf(f,"%llu\t%ld\t%ld\t%ld\t%.3f\t%d\t%d\t%d\t%d\t%d\n",(unsigned long long)seed,samples,valid,best,omp_get_wtime()-t0,bq.a+1,bq.b+1,bq.c+1,bq.d+1,bq.o);fclose(f);if(best<target)save(av[2],&bg);fprintf(stderr,"seed=%llu sampled=%ld valid=%ld best=%ld elapsed=%.2f\n",(unsigned long long)seed,samples,valid,best,omp_get_wtime()-t0);free(cs);return best<target?42:0;}
