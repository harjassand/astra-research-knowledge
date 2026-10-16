#define main frozen_simulator_main
#include "simulator_readouts.cpp"
#undef main
int main(){try{Geo g(16);uint64_t count=0;for(int f=0;f<6*g.N;f++){set<int>E{f};auto s=g.boundary(E);auto d0=decode(g,s,0);for(int p=1;p<=2;p++){auto d=decode(g,s,p);check(d.D==d0.D,"strict recovery exact equality");check(!d.fallback&&g.boundary(d.D)==s,"alternative singleface recovery");auto residual=E;for(int x:d.D)tog(residual,x);check(g.hom(residual)==0,"alternative singleface logical");count++;}}cout<<"{\"status\":\"PASS\",\"L\":16,\"D1_D2_singleface_cases\":"<<count<<",\"includes_all_seams\":true,\"exact_D0_equality\":true}"<<endl;}catch(exception&e){cerr<<e.what()<<endl;return 1;}}
