// Cyclic-group nonzero-cycle-voltage search; every reported solution is checked exactly.
#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){
 if(argc<6){cerr<<"usage: forms modulus seconds seed output\n";return 2;}
 ifstream in(argv[1]); int n,m;in>>n>>m; if(!in)return 2;
 int p=stoi(argv[2]); double sec=stod(argv[3]); mt19937_64 rng(stoull(argv[4]));
 vector<vector<pair<int,int>>> forms(m),inc(n);for(int i=0;i<m;i++){int k;in>>k;for(int j=0;j<k;j++){int v,s;in>>v>>s;forms[i].push_back({v,s});inc[v].push_back({i,s});}}
 vector<int>x(n),sum(m),bad,pos(m),wt(m,1),hist(p),bestx;int best=m;uint64_t it=0;auto start=chrono::steady_clock::now();
 auto mod=[&](int v){v%=p;return v<0?v+p:v;};
 auto setbad=[&](int i,bool yes){if(yes&&pos[i]<0){pos[i]=bad.size();bad.push_back(i);}else if(!yes&&pos[i]>=0){int j=pos[i];pos[bad.back()]=j;bad[j]=bad.back();bad.pop_back();pos[i]=-1;}};
 auto init=[&](){for(int&v:x)v=rng()%p;bad.clear();fill(pos.begin(),pos.end(),-1);fill(wt.begin(),wt.end(),1);for(int i=0;i<m;i++){int z=0;for(auto[v,s]:forms[i])z+=s*x[v];sum[i]=mod(z);setbad(i,sum[i]==0);}};
 init();uint64_t stall=0;
 while(chrono::duration<double>(chrono::steady_clock::now()-start).count()<sec){
  if((int)bad.size()<best){best=bad.size();bestx=x;cerr<<"p="<<p<<" best="<<best<<" it="<<it<<" sec="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"\n";stall=0;}
  if(bad.empty()){
   for(auto&f:forms){int z=0;for(auto[v,s]:f)z+=s*x[v];if(mod(z)==0)abort();}
   ofstream out(argv[5]);out<<p<<" "<<n<<"\n";for(int v:x)out<<v<<" ";out<<"\n";cerr<<"SOLVED\n";return 0;
  }
  int c=bad[rng()%bad.size()];int v=forms[c][rng()%forms[c].size()].first;
  fill(hist.begin(),hist.end(),0);for(auto[i,s]:inc[v]){int forbidden=mod(x[v]-s*sum[i]);hist[forbidden]+=wt[i];}
  int t=x[v];if(rng()%100<3)t=rng()%p;else{int low=INT_MAX,nt=0;for(int j=0;j<p;j++)if(j!=x[v]){if(hist[j]<low){low=hist[j];t=j;nt=1;}else if(hist[j]==low&&rng()%++nt==0)t=j;}}
  int d=t-x[v]; x[v]=t;for(auto[i,s]:inc[v]){sum[i]=mod(sum[i]+s*d);setbad(i,sum[i]==0);}
  ++it;++stall;
  if(it%500==0){for(int i:bad)++wt[i];}
  if(stall>200000){init();stall=0;}
 }
 cerr<<"UNRESOLVED best="<<best<<" iterations="<<it<<"\n";return 1;
}
