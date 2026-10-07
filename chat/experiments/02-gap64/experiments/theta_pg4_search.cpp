#include<bits/stdc++.h>
using namespace std;
struct E{int v,a,b;};
int main(int ac,char**av){if(ac<5)return 2;ifstream f(av[1]);int n,S,m;f>>n>>S>>m;vector<array<int,25>>states(S);for(auto&r:states)for(int&x:r)f>>x;array<int,4096>cost6;for(int&x:cost6)f>>x;int A;f>>A;vector<vector<E>>rows(m);vector<vector<int>>inc(n);for(int i=0;i<m;i++){int k;f>>k;for(int j=0;j<k;j++){E e;f>>e.v>>e.a>>e.b;rows[i].push_back(e);inc[e.v].push_back(i);}}
mt19937_64 rng(stoull(av[3]));double sec=stod(av[2]);vector<int>x(n),cost(m),bad,pos(m,-1);long long energy=0,best=LLONG_MAX,it=0;auto start=chrono::steady_clock::now();
auto val=[&](int i){int z=0;for(auto e:rows[i]){int t=states[x[e.v]][e.a*5+e.b];if(rows[i].size()==8&&t!=A)return 0;z=(z<<2)|t;}return rows[i].size()==8?1:cost6[z];};
auto setbad=[&](int i,bool yes){if(yes&&pos[i]<0){pos[i]=bad.size();bad.push_back(i);}else if(!yes&&pos[i]>=0){int j=pos[i];pos[bad.back()]=j;bad[j]=bad.back();bad.pop_back();pos[i]=-1;}};
for(int&v:x)v=rng()%S;for(int i=0;i<m;i++){cost[i]=val(i);energy+=cost[i];setbad(i,cost[i]>0);}
while(chrono::duration<double>(chrono::steady_clock::now()-start).count()<sec){
 if(energy<best){best=energy;cerr<<"best="<<best<<" bad_core="<<bad.size()<<" it="<<it<<"\n";ofstream out(av[4]);out<<best<<"\n";for(int a:x)out<<a<<" ";out<<"\n";}
 if(!energy)return 0;
 int r=bad[rng()%bad.size()];int v=rows[r][rng()%rows[r].size()].v,old=x[v];x[v]=rng()%S;vector<int>nc;long long delta=0;
 for(int i:inc[v]){int z=val(i);nc.push_back(z);delta+=z-cost[i];}
 double t=0.15+3.0*(1.0-(it%50000)/50000.0);
 if(delta<=0||generate_canonical<double,53>(rng)<exp(-delta/t)){
  energy+=delta;for(int j=0;j<(int)inc[v].size();j++){int i=inc[v][j];cost[i]=nc[j];setbad(i,cost[i]>0);}
 }else x[v]=old;
 ++it;
}
cerr<<"UNRESOLVED best="<<best<<" iterations="<<it<<"\n";return 1;}
