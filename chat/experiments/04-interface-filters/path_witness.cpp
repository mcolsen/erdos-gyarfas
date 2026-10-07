#include <iostream>
#include <fstream>
#include <vector>
#include <cstdint>
using U=uint64_t;U adj[64];int n,goal,dist[64];std::vector<int> stack,result;
bool dfs(int u,int left,U seen){
 if(left==1){if(adj[u]>>goal&1){result=stack;result.push_back(goal);return true;}return false;}
 U b=adj[u]&~seen&~(U(1)<<goal);
 while(b){int v=__builtin_ctzll(b);b&=b-1;if(dist[v]>left-1)continue;stack.push_back(v);if(dfs(v,left-1,seen|(U(1)<<v)))return true;stack.pop_back();}return false;
}
int main(int argc,char**argv){if(argc!=3)return 2;std::ifstream f(argv[1]);std::string s;int m;f>>s>>s>>n>>m;int u,v;for(int i=0;i<m;i++){f>>s>>u>>v;--u;--v;adj[u]|=U(1)<<v;adj[v]|=U(1)<<u;}
 std::ifstream queries(argv[2]);int id,k;
 while(queries>>id>>k){std::vector<std::pair<int,int>> added;for(int i=0;i<k;i++){queries>>u>>v;added.emplace_back(u,v);}
  for(int i=0;i<k-1;i++){auto [a,b]=added[i];adj[a]|=U(1)<<b;adj[b]|=U(1)<<a;}
  auto [a,b]=added.back();goal=b;int q[64],l=0,r=0;for(int i=0;i<n;i++)dist[i]=999;dist[b]=0;q[r++]=b;
  while(l<r){int x=q[l++];U z=adj[x];while(z){int y=__builtin_ctzll(z);z&=z-1;if(dist[y]==999){dist[y]=dist[x]+1;q[r++]=y;}}}
  bool found=false;for(int L=4;L<=n;L*=2){stack={a};if(dfs(a,L-1,U(1)<<a)){std::cout<<id<<" "<<L;for(int x:result)std::cout<<" "<<x;std::cout<<"\n";found=true;break;}}
  if(!found)std::cout<<id<<" 0\n";
  for(int i=0;i<k-1;i++){auto [a,b]=added[i];adj[a]&=~(U(1)<<b);adj[b]&=~(U(1)<<a);}
 }
}
