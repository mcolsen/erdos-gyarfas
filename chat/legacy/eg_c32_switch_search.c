#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <limits.h>
#define MAXN 512
#define MW 8
#define MAXPATH 4096
static int N,deg_[MAXN],nb_[MAXN][4];static unsigned char A[MAXN][MAXN];
static uint64_t rs[2]; static uint64_t xr(void){uint64_t a=rs[0],b=rs[1],r=a+b;b^=a;rs[0]=((a<<55)|(a>>9))^b^(b<<14);rs[1]=(b<<36)|(b>>28);return r;}static int rnd(int n){return xr()%(uint64_t)n;}
static void rebuild_nb(void){memset(deg_,0,sizeof(deg_));for(int i=0;i<N;i++)for(int j=0;j<N;j++)if(A[i][j])nb_[i][deg_[i]++]=j;}
static void del(int a,int b){A[a][b]=A[b][a]=0;}static void add(int a,int b){A[a][b]=A[b][a]=1;}
typedef struct{uint64_t m[MW];int end;} Path;
static Path P1[MAXPATH],P2[MAXPATH];static int pc1,pc2,skipu,skipv,targetDepth;static unsigned char pused[MAXN];static int pverts[32];static int head2[MAXN],next2[MAXPATH],whichset;
static void enumdfs(int u,int d,Path *P,int *pc){pverts[d]=u;if(d==targetDepth){int ix=(*pc)++;Path *q=&P[ix];memset(q->m,0,sizeof(q->m));for(int i=0;i<=d;i++)q->m[pverts[i]>>6]|=1ULL<<(pverts[i]&63);q->end=u;if(whichset==2){next2[ix]=head2[u];head2[u]=ix;}return;}for(int k=0;k<deg_[u];k++){int v=nb_[u][k];if((u==skipu&&v==skipv)||(u==skipv&&v==skipu)||pused[v])continue;pused[v]=1;enumdfs(v,d+1,P,pc);pused[v]=0;}}
static int edge_closes(int s,int t,int L){int k=L-1,h1=k/2,h2=k-h1;skipu=s;skipv=t;pc1=pc2=0;for(int i=0;i<N;i++)head2[i]=-1;whichset=1;memset(pused,0,N);pused[s]=1;pverts[0]=s;targetDepth=h1;enumdfs(s,0,P1,&pc1);whichset=2;memset(pused,0,N);pused[t]=1;pverts[0]=t;targetDepth=h2;enumdfs(t,0,P2,&pc2);for(int i=0;i<pc1;i++){int e=P1[i].end;for(int j=head2[e];j>=0;j=next2[j]){int ok=1;for(int w=0;w<MW;w++){uint64_t inter=P1[i].m[w]&P2[j].m[w];uint64_t want=(w==(e>>6))?(1ULL<<(e&63)):0;if(inter!=want){ok=0;break;}}if(ok)return 1;}}return 0;}
static int new_short_cycle(int a,int c,int b,int d){return edge_closes(a,c,4)||edge_closes(b,d,4)||edge_closes(a,c,8)||edge_closes(b,d,8)||edge_closes(a,c,16)||edge_closes(b,d,16);}
/* exact canonical cycle counter */
static int Lt,used[MAXN],secondv,distv[MAXN];static long cnt,capcnt;
static void bfs(int s){int q[MAXN],h=0,t=0;for(int i=0;i<N;i++)distv[i]=INT_MAX/4;distv[s]=0;q[t++]=s;while(h<t){int u=q[h++];for(int k=0;k<deg_[u];k++){int v=nb_[u][k];if(v<s||distv[v]<INT_MAX/4)continue;distv[v]=distv[u]+1;q[t++]=v;}}}
static void dfs(int u,int d,int s){if(cnt>=capcnt)return;if(d==Lt-1){if(A[u][s]&&secondv<u)cnt++;return;}int rem=Lt-d-1;for(int k=0;k<deg_[u];k++){int v=nb_[u][k];if(v<=s||used[v]||distv[v]>rem)continue;used[v]=1;dfs(v,d+1,s);used[v]=0;if(cnt>=capcnt)return;}}
static long countc(int L,long cap){Lt=L;cnt=0;capcnt=cap;memset(used,0,sizeof(used));for(int s=0;s<N&&cnt<cap;s++){bfs(s);used[s]=1;for(int k=0;k<deg_[s];k++){int v=nb_[s][k];if(v<=s||distv[v]>L-1)continue;secondv=v;used[v]=1;dfs(v,1,s);used[v]=0;if(cnt>=cap)break;}used[s]=0;}return cnt;}
static int shortzero(void){return countc(4,1)==0&&countc(8,1)==0&&countc(16,1)==0;}
static void save(const char*p){FILE*f=fopen(p,"w");int m=0;for(int i=0;i<N;i++)for(int j=i+1;j<N;j++)m+=A[i][j];fprintf(f,"p edge %d %d\n",N,m);for(int i=0;i<N;i++)for(int j=i+1;j<N;j++)if(A[i][j])fprintf(f,"e %d %d\n",i+1,j+1);fclose(f);}
static void load(const char*p){FILE*f=fopen(p,"r");if(!f){perror(p);exit(2);}char t;int a,b,m;while(fscanf(f," %c",&t)==1){if(t=='p'){char w[16];fscanf(f,"%15s%d%d",w,&N,&m);}else if(t=='e'){fscanf(f,"%d%d",&a,&b);a--;b--;A[a][b]=A[b][a]=1;}else{char line[1024];fgets(line,sizeof(line),f);}}fclose(f);rebuild_nb();}
int main(int ac,char**av){if(ac<5)return 2;load(av[1]);uint64_t seed=strtoull(av[2],0,10);long moves=atol(av[3]);rs[0]=seed^0x9e3779b97f4a7c15ULL;rs[1]=seed*0xbf58476d1ce4e5b9ULL+1;long cur=countc(32,LONG_MAX),valid=0,simple=0;fprintf(stderr,"start n=%d c32=%ld short=%d\n",N,cur,shortzero());for(long mv=1;mv<=moves;mv++){int a=rnd(N),b=nb_[a][rnd(3)],c=rnd(N),d=nb_[c][rnd(3)];if(a==c||a==d||b==c||b==d)continue;if(rnd(2)){int t=c;c=d;d=t;}if(A[a][c]||A[b][d])continue;simple++;del(a,b);del(c,d);add(a,c);add(b,d);rebuild_nb();if(new_short_cycle(a,c,b,d)){del(a,c);del(b,d);add(a,b);add(c,d);rebuild_nb();continue;}valid++;long nc=countc(32,LONG_MAX);if(nc<cur){cur=nc;fprintf(stderr,"NEW best=%ld mv=%ld valid=%ld swap %d-%d %d-%d\n",cur,mv,valid,a,b,c,d);save(av[4]);if(!shortzero()){fprintf(stderr,"BUG\n");return 3;}}else{del(a,c);del(b,d);add(a,b);add(c,d);rebuild_nb();}if(mv%10000==0){fprintf(stderr,"mv=%ld simple=%ld valid=%ld cur=%ld\n",mv,simple,valid,cur);fflush(stderr);}}fprintf(stderr,"DONE simple=%ld valid=%ld best=%ld audit=%d\n",simple,valid,cur,shortzero());return 0;}
