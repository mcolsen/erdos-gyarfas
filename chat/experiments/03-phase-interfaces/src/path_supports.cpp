#include <bits/stdc++.h>
using namespace std;using U=uint64_t;U a[64],S[64];int N;unsigned long long states=0;
void dfs(int v,U used,int d){states++;S[v]|=1ULL<<d;U m=a[v]&~used;while(m){int w=__builtin_ctzll(m);m&=m-1;dfs(w,used|1ULL<<w,d+1);}}
int main(int argc,char**argv){if(argc<2)return 2;ifstream f(argv[1]);string s;int m;while(f>>s){if(s=="p"){string z;f>>z>>N>>m;}else if(s=="e"){int u,v;f>>u>>v;--u;--v;a[u]|=1ULL<<v;a[v]|=1ULL<<u;}else{string z;getline(f,z);}}if(N>64)return 3;vector<int>ps;for(int v=0;v<N;v++)if(__builtin_popcountll(a[v])==2)ps.push_back(v);for(int s:ps){fill(S,S+64,0);dfs(s,1ULL<<s,0);for(int t:ps)if(t>s)cout<<s+1<<" "<<t+1<<" "<<S[t]<<"\n";}cerr<<"DFSstates "<<states<<"\n";}
