#define main search_main
#include "complete_necklace.cpp"
#undef main
int main(int argc,char**argv){if(argc!=4)return 2;int m=atoi(argv[1]),r=atoi(argv[2]);std::string out=argv[3];n=m*r;if(n>62)return 2;
 for(int i=0;i<r;i++)for(int j=0;j<m;j++)add(i*m+j,i*m+(j+1)%m);
 for(int i=0;i<r;i++){int k=m==7?2:(i==0?2:3);add(i*m+k,((i+1)%r)*m);}
 cap=20000000;save(out+"_backbone.edge");std::ofstream f(out+"_compatible.txt");std::vector<std::pair<int,int>> edges;
 for(int u=0;u<n;u++)if(deg[u]==2)for(int v=u+1;v<n;v++)if(deg[v]==2&&!(adj[u]>>v&1)&&safe(u,v))edges.emplace_back(u,v);
 for(auto [u,v]:edges)f<<u<<" "<<v<<"\n";f.close();
 std::ofstream cf(out+"_conflicts.txt");uint64_t conflicts=0;
 for(int i=0;i<(int)edges.size();i++)for(int j=i+1;j<(int)edges.size();j++){
  auto [a,b]=edges[i];auto [c,d]=edges[j];bool clash=a==c||a==d||b==c||b==d;
  if(!clash){add(a,b);clash=!safe(c,d);del(a,b);}
  if(clash){cf<<i<<" "<<j<<"\n";conflicts++;}
 }
 std::cerr<<"n="<<n<<" candidateedges="<<edges.size()<<" conflicts="<<conflicts<<" tests="<<attempts<<" unknown="<<unknown<<"\n";
}
