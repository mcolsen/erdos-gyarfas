#include <vector>
#include <algorithm>
#include <cstdint>
#include <queue>
using namespace std;
namespace {vector<vector<int>> a;vector<int>d,path;vector<char> used;int n,L,root,cap,found;long long budget,nodes;int *out;bool aborted;
void dfs(int u,int dep){
 if(++nodes>budget){aborted=true;return;}
 if(dep==L-1){if(path[1]<u && binary_search(a[u].begin(),a[u].end(),root)){copy(path.begin(),path.begin()+L,out+L*found);++found;}return;}
 for(int v:a[u])if(v>root&&!used[v]&&d[v]<=L-dep-1){used[v]=1;path[dep+1]=v;dfs(v,dep+1);used[v]=0;if(found>=cap||aborted)return;}
}
}
extern "C" int cycles(int N,int M,const int*edges,int len,int maxout,long long maxnodes,int* output,long long* visits){
 n=N;L=len;cap=maxout;out=output;nodes=0;budget=maxnodes;found=0;aborted=false;a.assign(n,{});used.assign(n,0);path.resize(n);d.resize(n);
 for(int i=0;i<M;i++){int u=edges[2*i],v=edges[2*i+1];a[u].push_back(v);a[v].push_back(u);}for(auto &v:a)sort(v.begin(),v.end());
 if(L<=n)for(root=0;root<n;root++){
  fill(d.begin(),d.end(),n+1);queue<int>q;q.push(root);d[root]=0;while(!q.empty()){int u=q.front();q.pop();for(int v:a[u])if(v>=root&&d[v]>d[u]+1){d[v]=d[u]+1;q.push(v);}}
  used[root]=1;path[0]=root;dfs(root,0);used[root]=0;if(found>=cap||aborted)break;
 }
 *visits=nodes;return aborted ? -found-1 : found;
}
