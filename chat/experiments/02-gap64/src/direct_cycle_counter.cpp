// Independent full-graph simple-cycle counter. No gadget assumptions.
// Compile: c++ -O3 -std=c++17 direct_cycle_counter.cpp -o direct_cycle_counter
// Usage: ./direct_cycle_counter graph.edge length [count_cap]
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <queue>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

class Counter {
    std::vector<std::vector<int>> adj;
    std::vector<unsigned char> used;
    std::vector<int> distance;
    int length, root=0, first=0;
    uint64_t cap, total=0;
    void visit(int u, int depth) {
        if (total >= cap) return;
        if (depth == length-1) {
            if (first < u && std::binary_search(adj[u].begin(),adj[u].end(),root)) ++total;
            return;
        }
        const int remaining = length-depth-1;
        for (int v:adj[u]) {
            if (v<=root || used[v] || distance[v]>remaining) continue;
            used[v]=1; visit(v,depth+1); used[v]=0;
            if (total>=cap) return;
        }
    }
public:
    Counter(std::vector<std::vector<int>> g,int l,uint64_t c)
      :adj(std::move(g)),used(adj.size(),0),distance(adj.size()),length(l),cap(c) {}
    uint64_t count() {
        if (length>static_cast<int>(adj.size())) return 0;
        for (root=0;root<static_cast<int>(adj.size()) && total<cap;++root) {
            std::fill(distance.begin(),distance.end(),std::numeric_limits<int>::max());
            std::queue<int> q; q.push(root);distance[root]=0;
            while(!q.empty()) {int u=q.front();q.pop();for(int v:adj[u])
                if(v>=root && distance[v]==std::numeric_limits<int>::max()) {
                    distance[v]=distance[u]+1;q.push(v);
                }
            }
            used[root]=1;
            for(int v:adj[root]) {
                if(v<=root) continue;
                first=v;used[v]=1;visit(v,1);used[v]=0;
                if(total>=cap) break;
            }
            used[root]=0;
        }
        return total;
    }
};
int main(int argc,char**argv) {
    try {
        if(argc<3 || argc>4) throw std::runtime_error("usage: graph.edge length [count_cap]");
        int length=std::stoi(argv[2]);
        uint64_t cap=argc==4?std::stoull(argv[3]):std::numeric_limits<uint64_t>::max();
        if(length<3 || cap==0) throw std::runtime_error("length >=3 and cap >=1 required");
        std::ifstream input(argv[1]);if(!input) throw std::runtime_error("Cannot open graph");
        int n=0,m=0,read_edges=0;std::vector<std::vector<int>> adj;std::string line;
        while(std::getline(input,line)) {
            std::istringstream in(line);char type;if(!(in>>type)||type=='c') continue;
            if(type=='p') {
                std::string word;if(n || !(in>>word>>n>>m) || n<1 || n>10000 || m<0)
                    throw std::runtime_error("Invalid or repeated header");
                adj.resize(n);
            } else if(type=='e') {
                int a,b;if(!n || !(in>>a>>b)||a<1||b<1||a>n||b>n||a==b)
                    throw std::runtime_error("Invalid edge");
                --a;--b;
                if(std::find(adj[a].begin(),adj[a].end(),b)!=adj[a].end())
                    throw std::runtime_error("Duplicate edge");
                adj[a].push_back(b);adj[b].push_back(a);++read_edges;
            } else throw std::runtime_error("Unknown DIMACS record");
        }
        if(!n || read_edges!=m) throw std::runtime_error("Header/edge-count mismatch");
        for(auto& neighbours:adj)std::sort(neighbours.begin(),neighbours.end());
        Counter counter(std::move(adj),length,cap);uint64_t count=counter.count();
        std::cout<<"n="<<n<<" L="<<length<<" count"<<(count>=cap?">=":"=")<<count<<"\n";
        return 0;
    } catch(const std::exception& e) {std::cerr<<e.what()<<"\n";return 2;}
}
