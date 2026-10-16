// Exhaustive finite falsification of s01's modulo-8 two-fault moat decoder.
// Scope: 4x4 torus, clean reachable counter heights <=3, arbitrary two
// distinct counter substitutions. This does not prove a size-uniform lemma.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <functional>
#include <iostream>
#include <set>
#include <vector>
using namespace std;

using State = array<int,16>;
struct Tile { int p; array<int,4> v; };
vector<Tile> tiles;
array<array<int,2>,16> inc{};
bool vm[2][256]{};

int mask(const State& s, const Tile& t) {
  int m=0; for(int v:t.v) m|=1<<s[v]; return m;
}
bool valid_tile(const State& s,int ti) { return vm[tiles[ti].p][mask(s,tiles[ti])]; }
bool valid(const State& s) { for(int i=0;i<8;i++) if(!valid_tile(s,i)) return false; return true; }
void init() {
  for(int p=0;p<2;p++) for(int x=p;x<4;x+=2) for(int y=p;y<4;y+=2) {
    Tile t{p,{x*4+y,x*4+(y+1)%4,((x+1)%4)*4+y,((x+1)%4)*4+(y+1)%4}};
    sort(t.v.begin(),t.v.end()); tiles.push_back(t);
  }
  array<int,16> n{};
  for(int j=0;j<8;j++) for(int v:tiles[j].v) inc[v][n[v]++]=j;
  for(int v=0;v<16;v++) if(n[v]!=2) abort();
  for(int p=0;p<2;p++) for(int a=0;a<8;a++) {
    vm[p][1<<a]=true;
    if((a&1)!=p) vm[p][(1<<a)|(1<<((a+1)%8))]=true;
  }
}
void print(const State& s) { for(int x=0;x<4;x++) { for(int y=0;y<4;y++) cout << s[x*4+y]; cout << (x==3?'\n':'/'); } }
int gate_delta(const State& h,const State& s) {
  array<int,16> ch{}; int n=0;
  for(int v=0;v<16;v++) if(h[v]!=s[v]) ch[v]=1,n++;
  if(n==0) return 0;
  if(n!=4) return -1;
  for(int j=0;j<8;j++) {
    auto &t=tiles[j]; bool same=true,up=true,down=true;
    for(int v=0;v<16;v++) if(ch[v] != (find(t.v.begin(),t.v.end(),v)!=t.v.end())) same=false;
    for(int v:t.v) {
      if(h[v]!=h[t.v[0]]) same=false;
      if(s[v]!=(h[v]+1)%8) up=false;
      if(s[v]!=(h[v]+7)%8) down=false;
    }
    if(same && ((h[t.v[0]]%2==t.p && up) || (h[t.v[0]]%2!=t.p && down))) return j+1;
  }
  return -1;
}
vector<pair<int,int>> repairs(const State& s) {
  vector<pair<int,int>> out;
  State t=s;
  for(int v=0;v<16;v++) {
    int n=0,zstar=-1;
    for(int z=0;z<8;z++) {
      t[v]=z;
      if(valid_tile(t,inc[v][0]) && valid_tile(t,inc[v][1])) n++,zstar=z;
    }
    t[v]=s[v];
    if(n==1 && zstar!=s[v]) out.push_back({v,zstar});
  }
  return out;
}
int main() {
  init();
  vector<State> clean; State h;
  while(true) {
    for(int i=0;i<16;i++) if(!(cin>>h[i])) goto loaded;
    clean.push_back(h);
  }
loaded:
  long long fault_cases=0, falseR=0, bcases=0, bcandidates=0, bnonlocal=0, bmissing=0;
  for(const auto &a:clean) {
    if(!valid(a)) {cerr<<"bad clean input\n";return 2;}
    for(int u=0;u<16;u++) for(int v=u+1;v<16;v++)
    for(int x=0;x<8;x++) if(x!=a[u]) for(int y=0;y<8;y++) if(y!=a[v]) {
      State s=a; s[u]=x;s[v]=y; fault_cases++;
      auto rr=repairs(s);
      for(auto [w,z]:rr) if(z!=a[w]) {
        falseR++;
        if(falseR==1) {cout<<"FALSE_R clean=";print(a);cout<<" faulty=";print(s);cout<<" faults="<<u<<","<<v<<" repair="<<w<<"->"<<z<<"\n";}
      }
      if(valid(s)) continue;
      bool anyB=false;
      // For L=4 every overlap-distance-two moat contains all eight tiles.
      for(int j=0;j<8;j++) if(!valid_tile(s,j)) {
        const auto &P=tiles[j];
        bool localR=false;
        for(int w:P.v) for(auto [rv,rz]:rr) if(rv==w) localR=true;
        if(localR) continue;
        for(int i=0;i<4;i++) for(int z=0;z<8;z++) if(z!=s[P.v[i]]) {
          State t=s;t[P.v[i]]=z;
          if(valid(t)) {
            anyB=true;bcandidates++;
            if(gate_delta(a,t)<0) { bnonlocal++; if(bnonlocal==1) {cout<<"NONLOCAL_B1 clean=";print(a);cout<<" faulty=";print(s);cout<<" Btile="<<j<<" site="<<P.v[i]<<"->"<<z<<" result=";print(t);} }
          }
        }
        for(int i=0;i<4;i++) for(int k=i+1;k<4;k++)
        for(int z=0;z<8;z++) if(z!=s[P.v[i]])
        for(int w=0;w<8;w++) if(w!=s[P.v[k]]) {
          State t=s;t[P.v[i]]=z;t[P.v[k]]=w;
          if(valid(t)) {
            anyB=true;bcandidates++;
            if(gate_delta(a,t)<0) { bnonlocal++; if(bnonlocal==1) {cout<<"NONLOCAL_B2 clean=";print(a);cout<<" faulty=";print(s);cout<<" Btile="<<j<<" sites="<<P.v[i]<<","<<P.v[k]<<"->"<<z<<","<<w<<" result=";print(t);} }
          }
        }
      }
      if(anyB) bcases++; else if(rr.empty()) {
        bmissing++;
        if(bmissing==1) {cout<<"NO_R_OR_B clean=";print(a);cout<<" faulty=";print(s);cout<<" faults="<<u<<","<<v<<"\n";}
      }
    }
  }
  cout<<"COUNTS clean="<<clean.size()<<" cases="<<fault_cases<<" falseR="<<falseR<<" Bcases="<<bcases<<" Bcandidates="<<bcandidates<<" Bnonlocal="<<bnonlocal<<" noRorB="<<bmissing<<"\n";
  long long examined=0, near_valid=0, near_nonlocal=0;
  for(const auto &a:clean) {
    State t=a;
    vector<int> support;
    function<void(int)> assign = [&](int k) {
      if(k==(int)support.size()) {
        examined++;
        if(valid(t)) {
          near_valid++;
          if(gate_delta(a,t)<0) {
            near_nonlocal++;
            if(near_nonlocal==1) {cout<<"NONLOCAL_NEAR clean=";print(a);cout<<" result=";print(t);}
          }
        }
        return;
      }
      int v=support[k];
      for(int z=0;z<8;z++) if(z!=a[v]) {t[v]=z;assign(k+1);}
      t[v]=a[v];
    };
    function<void(int,int)> choose = [&](int start,int left) {
      if(left==0) {assign(0);return;}
      for(int v=start;v<=16-left;v++) {support.push_back(v);choose(v+1,left-1);support.pop_back();}
    };
    for(int n=1;n<=4;n++) choose(0,n);
  }
  cout<<"CLASSIFY examined="<<examined<<" valid="<<near_valid<<" nonlocal="<<near_nonlocal<<"\n";
  return 0;
}
