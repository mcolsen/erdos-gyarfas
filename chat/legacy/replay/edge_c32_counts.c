#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#define MAXN 512
static int N,deg[MAXN],nb[MAXN][8],L;static long cnt,ec[MAXN][MAXN];static unsigned char used[MAXN];static int secondv,distv[MAXN],pathv[512];
static int adjacent(int a,int b){for(int i=0;i<deg[a];i++)if(nb[a][i]==b)return 1;return 0;}
static void bfs_allowed(int s){int q[MAXN],h=0,t=0;for(int i=0;i<N;i++)distv[i]=INT_MAX/4;distv[s]=0;q[t++]=s;while(h<t){int u=q[h++];for(int k=0;k<deg[u];k++){int v=nb[u][k];if(v<s||distv[v]<INT_MAX/4)continue;distv[v]=distv[u]+1;q[t++]=v;}}}
static void record(int s){cnt++;for(int i=0;i<L-1;i++){int a=pathv[i],b=pathv[i+1];if(a>b){int t=a;a=b;b=t;}ec[a][b]++;}int a=pathv[L-1],b=s;if(a>b){int t=a;a=b;b=t;}ec[a][b]++;}
static void dfs(int u,int d,int s){pathv[d]=u;if(d==L-1){if(adjacent(u,s)&&secondv<u)record(s);return;}int rem=L-d-1;for(int k=0;k<deg[u];k++){int v=nb[u][k];if(v<=s||used[v]||distv[v]>rem)continue;used[v]=1;dfs(v,d+1,s);used[v]=0;}}
int main(int ac,char**av){if(ac<4){fprintf(stderr,"usage edgefile L out.tsv\n");return 2;}FILE*f=fopen(av[1],"r");if(!f){perror(av[1]);return 2;}char typ;int a,b,m;while(fscanf(f," %c",&typ)==1){if(typ=='p'){char word[16];fscanf(f,"%15s%d%d",word,&N,&m);}else if(typ=='e'){fscanf(f,"%d%d",&a,&b);--a;--b;nb[a][deg[a]++]=b;nb[b][deg[b]++]=a;}else{char line[1024];fgets(line,sizeof(line),f);}}fclose(f);L=atoi(av[2]);memset(used,0,sizeof(used));for(int s=0;s<N;s++){bfs_allowed(s);used[s]=1;pathv[0]=s;for(int k=0;k<deg[s];k++){int v=nb[s][k];if(v<=s||distv[v]>L-1)continue;secondv=v;used[v]=1;dfs(v,1,s);used[v]=0;}used[s]=0;}FILE*out=fopen(av[3],"w");fprintf(out,"a\tb\tcount\n");for(int i=0;i<N;i++)for(int j=i+1;j<N;j++)if(ec[i][j])fprintf(out,"%d\t%d\t%ld\n",i+1,j+1,ec[i][j]);fclose(out);fprintf(stderr,"n=%d L=%d cycles=%ld sum=%ld\n",N,L,cnt,cnt*L);return 0;}
