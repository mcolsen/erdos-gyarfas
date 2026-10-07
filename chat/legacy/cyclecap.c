#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#define MAXN 512
static int N,deg[MAXN],nb[MAXN][8],L;static long cap,cnt;static unsigned char used[MAXN];static int secondv,distv[MAXN];
static int adjacent(int a,int b){for(int i=0;i<deg[a];i++)if(nb[a][i]==b)return 1;return 0;}
static void bfs_allowed(int s){int q[MAXN],h=0,t=0;for(int i=0;i<N;i++)distv[i]=INT_MAX/4;distv[s]=0;q[t++]=s;while(h<t){int u=q[h++];for(int k=0;k<deg[u];k++){int v=nb[u][k];if(v<s||distv[v]<INT_MAX/4)continue;distv[v]=distv[u]+1;q[t++]=v;}}}
static void dfs(int u,int d,int s){if(cnt>=cap)return;if(d==L-1){if(adjacent(u,s)&&secondv<u)cnt++;return;}int rem=L-d-1;for(int k=0;k<deg[u];k++){int v=nb[u][k];if(v<=s||used[v]||distv[v]>rem)continue;used[v]=1;dfs(v,d+1,s);used[v]=0;if(cnt>=cap)return;}}
int main(int ac,char**av){if(ac<4){fprintf(stderr,"usage: edgefile L cap\n");return 2;}FILE*f=fopen(av[1],"r");if(!f){perror(av[1]);return 2;}char typ;int a,b,m;while(fscanf(f," %c",&typ)==1){if(typ=='p'){char word[16];fscanf(f,"%15s%d%d",word,&N,&m);}else if(typ=='e'){fscanf(f,"%d%d",&a,&b);--a;--b;nb[a][deg[a]++]=b;nb[b][deg[b]++]=a;}else{char line[1024];fgets(line,sizeof(line),f);}}fclose(f);L=atoi(av[2]);cap=atol(av[3]);memset(used,0,sizeof(used));for(int s=0;s<N&&cnt<cap;s++){bfs_allowed(s);used[s]=1;for(int k=0;k<deg[s];k++){int v=nb[s][k];if(v<=s||distv[v]>L-1)continue;secondv=v;used[v]=1;dfs(v,1,s);used[v]=0;if(cnt>=cap)break;}used[s]=0;}printf("n=%d L=%d count%s=%ld\n",N,L,cnt>=cap?">=":"",cnt);return 0;}
