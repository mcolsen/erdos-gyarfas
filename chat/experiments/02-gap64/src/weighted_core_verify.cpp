// Exhaustive low-cost simple-cycle verifier on the expanded lift CORE.
// Independent of voltage equations and base-cycle enumeration.
#include <bits/stdc++.h>
using namespace std;
vector<vector<int>> adj;vector<int> kind,special,used;int root,firstv;long long calls=0,cycles=0,bad=0;map<int,long long> weights;
int mincost(int v){return kind[v]==7?3:4;}
int turn(int v,int a,int b){int q=(special[v]!=a&&special[v]!=b);return kind[v]==7?3+q:4+2*q;}
void dfs(int prev,int u,int len,int acc){
 ++calls;
 if(len>=3 && firstv<u && find(adj[u].begin(),adj[u].end(),root)!=adj[u].end()){
  int w=acc+turn(u,prev,root)+turn(root,u,firstv);
  if(w<=65){weights[w]++;cycles++;if(w<65)bad++;}
 }
 for(int v:adj[u])if(v>root&&!used[v]){
  int next=acc+turn(u,prev,v);
  if(next+mincost(root)+mincost(v)>65)continue;
  used[v]=1;dfs(u,v,len+1,next);used[v]=0;
 }
}
int main(int argc,char**argv){if(argc<3)return 2;ifstream f(argv[1]);string line;int n=0,m=0;while(getline(f,line)){istringstream s(line);char c;s>>c;if(c=='p'){string z;s>>z>>n>>m;adj.resize(n);}else if(c=='e'){int u,v;s>>u>>v;--u;--v;adj[u].push_back(v);adj[v].push_back(u);}}
kind.resize(n);special.resize(n);used.resize(n);ifstream g(argv[2]);for(int v=0;v<n;v++){int u;g>>u>>kind[v]>>special[v];if(u!=v+1)return 3;--special[v];if(find(adj[v].begin(),adj[v].end(),special[v])==adj[v].end())return 4;}
for(root=0;root<n;root++){used[root]=1;for(int v:adj[root])if(v>root){firstv=v;used[v]=1;dfs(root,v,2,0);used[v]=0;}used[root]=0;}
cout<<"DFS calls "<<calls<<"\n";for(auto[w,c]:weights)cout<<"minimum_weight "<<w<<" core_cycles "<<c<<"\n";cout<<(bad?"FAIL":"PASS")<<" no core cycle of minimum expansion weight below65\n";return bad?1:0;}
