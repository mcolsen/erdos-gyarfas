#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <limits.h>
#include <omp.h>
#define MAXN 256
#define MAXE 512
#define MAXK 100

typedef struct{int n,m;unsigned char A[MAXN][MAXN];uint16_t nb[MAXN][4];unsigned char deg[MAXN];}Graph;
typedef struct{int L,second;long cap,cnt;unsigned char used[MAXN];uint16_t dist[MAXN];}Ctx;
typedef struct{int u,v;long score;} Edge;
typedef struct{uint8_t p[6];} Matching;
static Matching mats[32];static int nmats=0;
static int load(const char*p,Graph*g){memset(g,0,sizeof(*g));FILE*f=fopen(p,"r");if(!f){perror(p);return 0;}char t;int a,b,m;while(fscanf(f," %c",&t)==1){if(t=='p'){char w[16];fscanf(f,"%15s%d%d",w,&g->n,&m);}else if(t=='e'){fscanf(f,"%d%d",&a,&b);--a;--b;g->A[a][b]=g->A[b][a]=1;}else{char z[1024];fgets(z,sizeof(z),f);}}fclose(f);for(int i=0;i<g->n;i++)for(int j=0;j<g->n;j++)if(g->A[i][j])g->nb[i][g->deg[i]++]=j;g->m=0;for(int i=0;i<g->n;i++)g->m+=g->deg[i];g->m/=2;return 1;}
static void save(const char*p,const Graph*g){FILE*f=fopen(p,"w");fprintf(f,"p edge %d %d\n",g->n,g->m);for(int i=0;i<g->n;i++)for(int j=i+1;j<g->n;j++)if(g->A[i][j])fprintf(f,"e %d %d\n",i+1,j+1);fclose(f);}
static inline void rep(Graph*g,int u,int oldv,int newv){for(int k=0;k<g->deg[u];k++)if(g->nb[u][k]==oldv){g->nb[u][k]=newv;return;}abort();}
static void bfs(const Graph*g,Ctx*c,int s){uint16_t q[MAXN];int h=0,t=0;for(int i=0;i<g->n;i++)c->dist[i]=UINT16_MAX;c->dist[s]=0;q[t++]=s;while(h<t){int u=q[h++];for(int k=0;k<g->deg[u];k++){int v=g->nb[u][k];if(v<s||c->dist[v]!=UINT16_MAX)continue;c->dist[v]=c->dist[u]+1;q[t++]=v;}}}
static void dfs(const Graph*g,Ctx*c,int u,int d,int s){if(c->cnt>=c->cap)return;if(d==c->L-1){if(g->A[u][s]&&c->second<u)c->cnt++;return;}int rem=c->L-d-1;for(int k=0;k<g->deg[u];k++){int v=g->nb[u][k];if(v<=s||c->used[v]||c->dist[v]>rem)continue;c->used[v]=1;dfs(g,c,v,d+1,s);c->used[v]=0;if(c->cnt>=c->cap)return;}}
static long countc(const Graph*g,int L,long cap){Ctx c;memset(&c,0,sizeof(c));c.L=L;c.cap=cap;for(int s=0;s<g->n&&c.cnt<cap;s++){bfs(g,&c,s);c.used[s]=1;for(int k=0;k<g->deg[s];k++){int v=g->nb[s][k];if(v<=s||c.dist[v]>L-1)continue;c.second=v;c.used[v]=1;dfs(g,&c,v,1,s);c.used[v]=0;if(c.cnt>=cap)break;}c.used[s]=0;}return c.cnt;}
static int cmpedge(const void*A,const void*B){const Edge*a=A,*b=B;return a->score<b->score?1:a->score>b->score?-1:0;}
static void gen_rec(uint8_t used[6],uint8_t p[6]){int i;for(i=0;i<6;i++)if(!used[i])break;if(i==6){mats[nmats++]=(Matching){{p[0],p[1],p[2],p[3],p[4],p[5]}};return;}used[i]=1;for(int j=i+1;j<6;j++)if(!used[j]){used[j]=1;p[i]=j;p[j]=i;gen_rec(used,p);used[j]=0;}used[i]=0;}
static int original_pair(int i,int j){return (i/2==j/2);}
int main(int ac,char**av){if(ac<6){fprintf(stderr,"usage graph edgecounts.tsv K out threads\n");return 2;}Graph base;if(!load(av[1],&base))return 2;FILE*f=fopen(av[2],"r");if(!f){perror(av[2]);return 2;}char line[256];fgets(line,sizeof(line),f);Edge es[MAXE];int ne=0,a,b;long sc;while(fscanf(f,"%d%d%ld",&a,&b,&sc)==3)es[ne++]=(Edge){a-1,b-1,sc};fclose(f);qsort(es,ne,sizeof(Edge),cmpedge);int K=atoi(av[3]);if(K>ne)K=ne;int th=atoi(av[5]);uint8_t used[6]={0},pp[6]={0};gen_rec(used,pp);long cur=countc(&base,32,LONG_MAX),best=cur,total=0,simple=0,shortok=0,eval=0;Graph bestg=base;double t0=omp_get_wtime();
 // count candidate upper bound and flatten triple/matching tasks
 typedef struct{uint8_t i,j,k,m;} Task; long cap=(long)K*K*K*nmats/6+1;Task*tasks=malloc(cap*sizeof(Task));long nt=0;
 for(int i=0;i<K;i++)for(int j=i+1;j<K;j++)for(int k=j+1;k<K;k++){
   int v[6]={es[i].u,es[i].v,es[j].u,es[j].v,es[k].u,es[k].v};int distinct=1;for(int x=0;x<6;x++)for(int y=x+1;y<6;y++)if(v[x]==v[y])distinct=0;if(!distinct)continue;
   for(int m=0;m<nmats;m++){int ok=1;for(int x=0;x<6;x++)if(x<mats[m].p[x]&&original_pair(x,mats[m].p[x]))ok=0;if(ok)tasks[nt++]=(Task){i,j,k,m};}
 }
 fprintf(stderr,"current=%ld K=%d matchings=%d tasks=%ld threads=%d\n",cur,K,nmats,nt,th);omp_set_num_threads(th);
#pragma omp parallel
 {Graph g=base;
#pragma omp for schedule(dynamic,8) reduction(+:total,simple,shortok,eval)
  for(long z=0;z<nt;z++){Task t=tasks[z];Edge rr[3]={es[t.i],es[t.j],es[t.k]};int v[6]={rr[0].u,rr[0].v,rr[1].u,rr[1].v,rr[2].u,rr[2].v};Matching M=mats[t.m];total++;int ok=1;for(int x=0;x<6;x++)if(x<M.p[x]){int u=v[x],w=v[M.p[x]];if(u==w||g.A[u][w]){ok=0;break;}}if(!ok)continue;simple++;
   for(int r=0;r<3;r++){int u=rr[r].u,w=rr[r].v;g.A[u][w]=g.A[w][u]=0;}
   for(int x=0;x<6;x++)if(x<M.p[x]){int u=v[x],w=v[M.p[x]];g.A[u][w]=g.A[w][u]=1;}
   for(int x=0;x<6;x++){int old=v[x^1],nw=v[M.p[x]];rep(&g,v[x],old,nw);}
   if(countc(&g,4,1)==0&&countc(&g,8,1)==0&&countc(&g,16,1)==0){shortok++;long lim;
#pragma omp atomic read
    lim=best;long val=countc(&g,32,lim);eval++;
#pragma omp critical
    {if(val<best){best=val;bestg=g;save(av[4],&bestg);fprintf(stderr,"BEST %ld delta=%ld task=%ld edges=(%d-%d,%d-%d,%d-%d) elapsed=%.2f\n",best,best-cur,z,v[0]+1,v[1]+1,v[2]+1,v[3]+1,v[4]+1,v[5]+1,omp_get_wtime()-t0);fflush(stderr);}}
   }
   for(int x=0;x<6;x++)if(x<M.p[x]){int u=v[x],w=v[M.p[x]];g.A[u][w]=g.A[w][u]=0;}
   for(int r=0;r<3;r++){int u=rr[r].u,w=rr[r].v;g.A[u][w]=g.A[w][u]=1;}
   for(int x=0;x<6;x++){int nw=v[M.p[x]],old=v[x^1];rep(&g,v[x],nw,old);}
  }
 }
 if(best==cur)save(av[4],&base);fprintf(stderr,"DONE best=%ld delta=%ld tasks=%ld simple=%ld shortok=%ld eval=%ld elapsed=%.2f\n",best,best-cur,total,simple,shortok,eval,omp_get_wtime()-t0);free(tasks);return 0;}
