#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>
using U=uint64_t;
int n,adjlist[64][3],deg[64],dist[64],target,len;U adj[64];
uint64_t pathnodes,cap=200000,attempts=0,unknown=0;
bool cut=false;
bool path(int v,int remain,U seen){
 if(++pathnodes>cap){cut=true;return false;}
 if(remain==1)return adj[v]>>target&1;
 U bits=adj[v]&~seen&~(U(1)<<target);
 while(bits){int w=__builtin_ctzll(bits);bits&=bits-1;
  if(dist[w]>remain-1)continue;
  if(path(w,remain-1,seen|(U(1)<<w)))return true;
  if(cut)return false;
 }return false;
}
bool safe(int u,int v){
 ++attempts;int q[64],l=0,r=0;for(int i=0;i<n;i++)dist[i]=99;dist[v]=0;q[r++]=v;
 while(l<r){int x=q[l++];U b=adj[x];while(b){int w=__builtin_ctzll(b);b&=b-1;if(dist[w]==99){dist[w]=dist[x]+1;q[r++]=w;}}}
 target=v;
 for(int L=4;L<=n;L*=2){
  if(dist[u]>L-1)continue;pathnodes=0;cut=false;
  if(path(u,L-1,U(1)<<u))return false;
  if(cut){unknown++;return false;}
 }return true;
}
void add(int u,int v){adj[u]|=U(1)<<v;adj[v]|=U(1)<<u;deg[u]++;deg[v]++;}
void del(int u,int v){adj[u]&=~(U(1)<<v);adj[v]&=~(U(1)<<u);deg[u]--;deg[v]--;}
void save(const std::string &s){std::ofstream o(s);int e=0;for(int i=0;i<n;i++)e+=deg[i];o<<"p edge "<<n<<" "<<e/2<<"\n";for(int u=0;u<n;u++)for(int v=u+1;v<n;v++)if(adj[u]>>v&1)o<<"e "<<u+1<<" "<<v+1<<"\n";}
int main(int argc,char**argv){if(argc!=6)return 2;int m=atoi(argv[1]),r=atoi(argv[2]),seed=atoi(argv[3]);double seconds=atof(argv[4]);std::string prefix=argv[5];n=m*r;if(n>62||m<3||r<3)return 2;std::mt19937 rng(seed);
 for(int i=0;i<r;i++)for(int j=0;j<m;j++)add(i*m+j,i*m+(j+1)%m);
 for(int i=0;i<r;i++){int out=m==7?2:(i==0?2:3);add(i*m+out,((i+1)%r)*m);}
 int best=-1;auto start=std::chrono::steady_clock::now();std::vector<std::pair<int,int>> extra,bestextra;
 uint64_t rounds=0;
 while(std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<seconds){
  rounds++;
  std::vector<std::pair<int,int>> pairs;
  for(int u=0;u<n;u++)if(deg[u]==2)for(int v=u+1;v<n;v++)if(deg[v]==2 && !(adj[u]>>v&1))pairs.emplace_back(u,v);
  std::shuffle(pairs.begin(),pairs.end(),rng);
  for(auto [u,v]:pairs){
   if(deg[u]!=2||deg[v]!=2)continue;
   if(safe(u,v)){add(u,v);extra.emplace_back(u,v);}
  }
  if((int)extra.size()>best){best=extra.size();bestextra=extra;save(prefix+".edge");std::cerr<<"BEST extra="<<best<<" degree2="<<n-2*r-2*best<<" attempts="<<attempts<<" unknown="<<unknown<<"\n";if(n-2*r-2*best==0)break;}
  int remove=1+rng()%5;if(rounds%100==0)remove=extra.size();
  std::shuffle(extra.begin(),extra.end(),rng);
  while(remove--&&!extra.empty()){auto [u,v]=extra.back();extra.pop_back();del(u,v);}
  if(rounds%7==0){for(auto [u,v]:extra)del(u,v);extra=bestextra;for(auto [u,v]:extra)add(u,v);
   std::shuffle(extra.begin(),extra.end(),rng);int k=2+rng()%5;while(k--&&!extra.empty()){auto [u,v]=extra.back();extra.pop_back();del(u,v);}}
 }
 std::cerr<<"SUMMARY n="<<n<<" rounds="<<rounds<<" best_added="<<best<<" degree2="<<n-2*r-2*best<<" attempts="<<attempts<<" unknown="<<unknown<<" elapsed="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"\n";
}
