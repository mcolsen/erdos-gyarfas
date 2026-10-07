#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <vector>
using U=uint64_t;
int n,t; U adj[32]; std::vector<std::pair<int,int>> chords;
uint64_t nodes=0,leaves=0,kept=0; bool timedout=false; double budget;
std::chrono::steady_clock::time_point started;
bool path(int u,int target,int remain,U seen){
 if(remain==1) return (adj[u]>>target)&1;
 U a=adj[u]&~seen&~(U(1)<<target);
 while(a){int v=__builtin_ctzll(a);a&=a-1;if(path(v,target,remain-1,seen|(U(1)<<v)))return true;}
 return false;
}
bool bad(int u,int v){for(int L=4;L<=n;L*=2)if(path(u,v,L-1,U(1)<<u))return true;return false;}
bool canonical(){
 auto a=chords;for(auto &e:a)if(e.first>e.second)std::swap(e.first,e.second);std::sort(a.begin(),a.end());
 for(int sign:{-1,1})for(int shift=0;shift<n;shift++){
  std::vector<std::pair<int,int>> b;for(auto e:a){int x=(sign*e.first+shift+n)%n,y=(sign*e.second+shift+n)%n;if(x>y)std::swap(x,y);b.emplace_back(x,y);}std::sort(b.begin(),b.end());if(b<a)return false;
 }return true;
}
void visit(U free,int skips){
 if(timedout)return;
 if((++nodes&65535)==0 && std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()>budget){timedout=true;return;}
 int k=__builtin_popcountll(free);if(skips<0||skips>k||((k-skips)&1))return;
 if(k==skips){leaves++;if(canonical()){kept++;std::cout<<n<<" "<<t;for(auto [a,b]:chords)std::cout<<" "<<a<<" "<<b;std::cout<<"\n";}return;}
 int u=__builtin_ctzll(free);U rest=free&~(U(1)<<u);
 if(skips)visit(rest,skips-1);
 U poss=rest&~adj[u];
 while(poss){int v=__builtin_ctzll(poss);poss&=poss-1;if(bad(u,v))continue;
 adj[u]|=U(1)<<v;adj[v]|=U(1)<<u;chords.emplace_back(u,v);
 visit(rest&~(U(1)<<v),skips);
 chords.pop_back();adj[u]&=~(U(1)<<v);adj[v]&=~(U(1)<<u);
 }
}
int main(int argc,char**argv){if(argc!=4)return 2;n=atoi(argv[1]);t=atoi(argv[2]);budget=atof(argv[3]);if(n<3||n>30||t<0||t>n||((n-t)&1)||(n&(n-1))==0)return 2;
 for(int u=0;u<n;u++)adj[u]=(U(1)<<((u+1)%n))|(U(1)<<((u+n-1)%n));
 started=std::chrono::steady_clock::now();visit((U(1)<<n)-1,t);
 std::cerr<<"n="<<n<<" t="<<t<<" nodes="<<nodes<<" leaves="<<leaves<<" dihedral_representatives="<<kept<<" complete="<<!timedout<<" seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()<<"\n";
 return timedout?3:0;
}
