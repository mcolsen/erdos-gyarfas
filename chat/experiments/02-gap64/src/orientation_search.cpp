// Exact finite constraint checker with stochastic local search for its witness.
#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){if(argc<5)return 2;ifstream f(argv[1]);int n,m;f>>n>>m;vector<int>need(m);vector<vector<pair<int,int>>> row(m),inc(n);for(int i=0;i<m;i++){int k;f>>need[i]>>k;for(int j=0;j<k;j++){int v,s;f>>v>>s;row[i].push_back({v,s});inc[v].push_back({i,s});}}
mt19937_64 rng(stoull(argv[3]));double sec=stod(argv[2]);vector<int>x(n),counts(m),weights(m,1),bad,pos(m,-1);auto start=chrono::steady_clock::now();int best=INT_MAX;long long it=0,stall=0;
auto deficit=[&](int i,int c){int d=max(0,need[i]-c);return d*d;};
auto setbad=[&](int i,bool yes){if(yes&&pos[i]<0){pos[i]=bad.size();bad.push_back(i);}else if(!yes&&pos[i]>=0){int j=pos[i];pos[bad.back()]=j;bad[j]=bad.back();bad.pop_back();pos[i]=-1;}};
auto init=[&](){for(int&v:x)v=rng()%3;fill(weights.begin(),weights.end(),1);fill(pos.begin(),pos.end(),-1);bad.clear();for(int i=0;i<m;i++){counts[i]=0;for(auto[v,s]:row[i])counts[i]+=x[v]==s;setbad(i,counts[i]<need[i]);}};
init();
while(chrono::duration<double>(chrono::steady_clock::now()-start).count()<sec){
 if((int)bad.size()<best){best=bad.size();stall=0;cerr<<"best violated="<<best<<" it="<<it<<"\n";}
 if(bad.empty()){ofstream out(argv[4]);for(int a:x)out<<a<<" ";out<<"\n";return 0;}
 int r=bad[rng()%bad.size()];int v=row[r][rng()%row[r].size()].first;int t=x[v],cost=INT_MAX,nt=0;
 if(rng()%100<3)t=rng()%3;
 else for(int s=0;s<3;s++)if(s!=x[v]){int z=0;for(auto[i,j]:inc[v])z+=weights[i]*(deficit(i,counts[i]-(x[v]==j)+(s==j))-deficit(i,counts[i]));if(z<cost){cost=z;t=s;nt=1;}else if(z==cost&&rng()%++nt==0)t=s;}
 for(auto[i,s]:inc[v]){counts[i]+=(t==s)-(x[v]==s);setbad(i,counts[i]<need[i]);}x[v]=t;
 ++it;++stall;if(it%500==0)for(int i:bad)weights[i]++;
 if(stall>100000){init();stall=0;}
}
cerr<<"UNRESOLVED "<<best<<" iterations "<<it<<"\n";return 1;}
