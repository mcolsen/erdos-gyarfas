// Independent BFS girth computation, records a shortest-cycle witness.
#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){if(argc<3)return 2;ifstream f(argv[1]);string line;int n=0,m=0;vector<vector<int>>a;while(getline(f,line)){istringstream s(line);char c;s>>c;if(c=='p'){string z;s>>z>>n>>m;a.resize(n);}else if(c=='e'){int u,v;s>>u>>v;--u;--v;a[u].push_back(v);a[v].push_back(u);}}
int best=n+1;vector<int> witness,d(n),par(n),q(n);long long visits=0;
for(int r=0;r<n;r++){fill(d.begin(),d.end(),-1);fill(par.begin(),par.end(),-1);int lo=0,hi=0;q[hi++]=r;d[r]=0;
while(lo<hi){int u=q[lo++];visits++;if(2*d[u]+1>=best)continue;for(int v:a[u]){if(d[v]<0){d[v]=d[u]+1;par[v]=u;q[hi++]=v;}else if(par[u]!=v&&par[v]!=u){int bound=d[u]+d[v]+1;if(bound<best){vector<int>p1,p2;int x=u,y=v;while(d[x]>d[y]){p1.push_back(x);x=par[x];}while(d[y]>d[x]){p2.push_back(y);y=par[y];}while(x!=y){p1.push_back(x);p2.push_back(y);x=par[x];y=par[y];}p1.push_back(x);reverse(p2.begin(),p2.end());p1.insert(p1.end(),p2.begin(),p2.end());if((int)p1.size()<best){best=p1.size();witness=p1;}}}}}
}
cout<<"girth "<<best<<" bfs_visits "<<visits<<"\n";ofstream out(argv[2]);for(int x:witness)out<<x+1<<" ";out<<"\n";return 0;}
