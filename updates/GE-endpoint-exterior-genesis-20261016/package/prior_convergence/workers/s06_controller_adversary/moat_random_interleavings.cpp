// Random adversarial two-counter audit of s01's radius-two moat rule.
// Unlike the L4 exhaustive check, L6/L8 moats leave exterior tiles unseen.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <random>
#include <vector>
using namespace std;
struct Tile {int p;array<int,4> v;vector<int> moat;};
struct Move {char kind;int label;int z;vector<int> s;};
int L,N;
vector<Tile> tiles;
vector<array<int,2>> inc;
bool vm[2][256]{};
mt19937_64 rng(60620261016ULL);
bool overlap(int i,int j) {for(int v:tiles[i].v) for(int w:tiles[j].v) if(v==w) return true;return false;}
void init(int side) {
  L=side;N=L*L;inc.resize(N);
  for(int p=0;p<2;p++) for(int x=p;x<L;x+=2) for(int y=p;y<L;y+=2) {
    Tile t{p,{x*L+y,x*L+(y+1)%L,((x+1)%L)*L+y,((x+1)%L)*L+(y+1)%L},{}};
    sort(t.v.begin(),t.v.end());tiles.push_back(t);
  }
  vector<int> n(N);
  for(int j=0;j<(int)tiles.size();j++) for(int v:tiles[j].v) inc[v][n[v]++]=j;
  for(int v=0;v<N;v++) if(n[v]!=2) abort();
  for(int p=0;p<2;p++) for(int a=0;a<8;a++) {
    vm[p][1<<a]=true;
    if((a&1)!=p) vm[p][(1<<a)|(1<<((a+1)%8))]=true;
  }
  for(int i=0;i<(int)tiles.size();i++) {
    vector<int> first;
    for(int j=0;j<(int)tiles.size();j++) if(overlap(i,j)) first.push_back(j);
    for(int j=0;j<(int)tiles.size();j++)
      for(int k:first) if(overlap(k,j)) {tiles[i].moat.push_back(j);break;}
  }
}
bool valid_tile(const vector<int>& s,int j) {
  int m=0;for(int v:tiles[j].v)m|=1<<s[v];return vm[tiles[j].p][m];
}
bool valid(const vector<int>&s) {for(int j=0;j<(int)tiles.size();j++)if(!valid_tile(s,j))return false;return true;}
bool star(const vector<int>&s,int v) {return valid_tile(s,inc[v][0])&&valid_tile(s,inc[v][1]);}
bool ready(const vector<int>&s,int j) {
  const auto &P=tiles[j];int c=s[P.v[0]];
  if(c%2!=P.p) return false;
  for(int v:P.v) if(s[v]!=c||!star(s,v))return false;
  return true;
}
int delta(const vector<int>&h,const vector<int>&s) {
  vector<int> ch;for(int v=0;v<N;v++)if(h[v]!=s[v])ch.push_back(v);
  if(ch.empty())return 0;
  if(ch.size()!=4)return -1;
  for(int j=0;j<(int)tiles.size();j++) {
    const auto &P=tiles[j];
    if(!equal(ch.begin(),ch.end(),P.v.begin()))continue;
    bool eq=true,up=true,down=true;int c=h[P.v[0]];
    for(int v:P.v) {if(h[v]!=c)eq=false;if(s[v]!=(c+1)%8)up=false;if(s[v]!=(c+7)%8)down=false;}
    if(eq&&((c%2==P.p&&up)||(c%2!=P.p&&down)))return j+1;
  }
  return -1;
}
vector<Move> repairs(const vector<int>&s) {
  vector<Move> out;vector<int> t=s;
  vector<int> rvalue(N,-1);
  for(int v=0;v<N;v++) {
    int n=0,zstar=-1;
    for(int z=0;z<8;z++) {
      t[v]=z;if(star(t,v))n++,zstar=z;
    }
    t[v]=s[v];
    if(n==1&&zstar!=s[v]) {
      rvalue[v]=zstar;t[v]=zstar;out.push_back({'R',v,zstar,t});t[v]=s[v];
    }
  }
  for(int j=0;j<(int)tiles.size();j++) if(!valid_tile(s,j)) {
    auto &P=tiles[j];bool localR=false;
    for(int v:P.v) if(rvalue[v]>=0)localR=true;
    if(localR)continue;
    auto moated=[&](){for(int k:P.moat)if(!valid_tile(t,k))return false;return true;};
    bool found=false;vector<int> best;
    for(int v:P.v) {
      for(int z=0;z<8;z++) if(z!=s[v]) {
        t[v]=z;
        if(moated()&&(!found||t<best)) {best=t;found=true;}
        t[v]=s[v];
      }
    }
    if(!found) {
      for(int a=0;a<4;a++) for(int b=a+1;b<4;b++)
      for(int z=0;z<8;z++) if(z!=s[P.v[a]])
      for(int w=0;w<8;w++) if(w!=s[P.v[b]]) {
        t[P.v[a]]=z;t[P.v[b]]=w;
        if(moated()&&(!found||t<best)) {best=t;found=true;}
        t[P.v[a]]=s[P.v[a]];t[P.v[b]]=s[P.v[b]];
      }
    }
    if(found)out.push_back({'B',j,0,best});
  }
  return out;
}
void print(const vector<int>&s) {for(int x=0;x<L;x++){for(int y=0;y<L;y++)cout<<s[x*L+y];cout<<(x==L-1?'\n':'/');}}
int main(int argc,char**argv) {
  int side=argc>1?atoi(argv[1]):6;
  long long trials=argc>2?atoll(argv[2]):100000;
  init(side);
  vector<int> h(N,0);
  long long falseR=0,falseG=0,traps=0,more2=0,nonlocal=0, bFired=0, bNonGlobal=0;
  long long cleanMoves=0;
  for(long long n=0;n<trials;n++) {
    if(n%1000==0)fill(h.begin(),h.end(),0);
    int advance=(int)(rng()%9)+1;
    for(int k=0;k<advance;k++) {
      vector<int> g;for(int j=0;j<(int)tiles.size();j++)if(ready(h,j))g.push_back(j);
      if(g.empty()) {cerr<<"clean deadlock\n";return 2;}
      int j=g[rng()%g.size()];
      for(int v:tiles[j].v)h[v]=(h[v]+1)%8;
      cleanMoves++;
    }
    if(!valid(h)) {cerr<<"bad clean state\n";return 2;}
    int u=rng()%N,v=rng()%N;while(v==u)v=rng()%N;
    vector<int>s=h;
    s[u]=(s[u]+1+rng()%7)%8;s[v]=(s[v]+1+rng()%7)%8;
    auto report=[&](const char*tag,const vector<int>&a,const vector<int>&b) {
      cout<<tag<<" trial="<<n<<" L="<<L<<" faults="<<u<<","<<v<<" clean=";print(h);cout<<" faulty=";print(s);cout<<" state1=";print(a);cout<<" state2=";print(b);
    };
    auto m=repairs(s);
    for(auto &mv:m) if(mv.kind=='R'&&mv.z!=h[mv.label]) {falseR++;if(falseR==1)report("FALSE_R",mv.s,mv.s);}
    for(int j=0;j<(int)tiles.size();j++) if(ready(s,j)) {
      if(!ready(h,j)) {falseG++;if(falseG==1)report("FALSE_G",s,s);}
      if(find(tiles[j].v.begin(),tiles[j].v.end(),u)!=tiles[j].v.end()||find(tiles[j].v.begin(),tiles[j].v.end(),v)!=tiles[j].v.end()) {
        falseG++;if(falseG==1)report("DIRTY_SITE_G",s,s);
      }
    }
    if(!valid(s)&&m.empty()) {traps++;if(traps==1)report("NO_REPAIR",s,s);}
    for(auto &a:m) {
      if(a.kind=='B') {bFired++;if(!valid(a.s))bNonGlobal++;}
      if(valid(a.s)) {
        if(delta(h,a.s)<0){nonlocal++;if(nonlocal==1)report("NONLOCAL_1",a.s,a.s);}
      } else {
        auto m2=repairs(a.s);
        if(m2.empty()) {traps++;if(traps==1)report("TRAP_AFTER_1",a.s,a.s);}
        for(auto &b:m2) {
          if(b.kind=='B'){bFired++;if(!valid(b.s))bNonGlobal++;}
          if(!valid(b.s)) {more2++;if(more2==1)report("MORE_THAN_2",a.s,b.s);}
          else if(delta(h,b.s)<0){nonlocal++;if(nonlocal==1)report("NONLOCAL_2",a.s,b.s);}
        }
      }
    }
  }
  cout<<"COUNTS L="<<L<<" trials="<<trials<<" cleanMoves="<<cleanMoves<<" falseR="<<falseR<<" falseG="<<falseG<<" traps="<<traps<<" more2="<<more2<<" nonlocal="<<nonlocal<<" Bmoves="<<bFired<<" BnonGlobal="<<bNonGlobal<<"\n";
}
