// Independently authored one-sector simulator. C++17, no external dependencies.
#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <random>
#include <set>
#include <sstream>
#include <stdexcept>
#include <vector>
using namespace std;
using B=vector<uint8_t>; using Q=array<int,4>; using K=array<int,5>;
const int pairs[6][2]={{0,1},{0,2},{0,3},{1,2},{1,3},{2,3}};
void check(bool b,string s){if(!b)throw runtime_error(s);}
template<class T> void tog(set<T>&s,T x){if(!s.erase(x))s.insert(x);}
struct Geo{
 static int size(int l){check(l>=2 && l<=64,"L must be 2..64");return l*l*l*l;}
 int L,N; array<int,4> st; vector<Q> up,dn,coord;
 Geo(int l):L(l),N(size(l)),up(N),dn(N),coord(N){st={l*l*l,l*l,l,1};for(int x=0;x<N;x++)for(int a=0;a<4;a++){int c=x/st[a]%L;coord[x][a]=c;up[x][a]=x+(c==L-1?-(L-1):1)*st[a];dn[x][a]=x+(c==0?L-1:-1)*st[a];}}
 int pos(Q q)const{int x=0;for(int a=0;a<4;a++)x+=((q[a]%L+L)%L)*st[a];return x;}
 int ori(int i,int j)const{if(i>j)swap(i,j);for(int o=0;o<6;o++)if(pairs[o][0]==i&&pairs[o][1]==j)return o;throw runtime_error("orientation");}
 array<int,4> bd(int f)const{int o=f/N,x=f%N,i=pairs[o][0],j=pairs[o][1];return {i*N+x,i*N+up[x][j],j*N+x,j*N+up[x][i]};}
 set<int> boundary(const set<int>&F)const{set<int>s;for(int f:F)for(int e:bd(f))tog(s,e);return s;}
 B gather(const B&E)const{B s(4*N);for(int i=0;i<4;i++)for(int x=0;x<N;x++)for(int j=0;j<4;j++)if(i!=j){int o=ori(i,j);s[i*N+x]^=E[o*N+x]^E[o*N+dn[x][j]];}return s;}
 int hom(const set<int>&F,int cut=0)const{int h=0;for(int f:F){int o=f/N,x=f%N;if(coord[x][pairs[o][0]]==cut&&coord[x][pairs[o][1]]==cut)h^=1<<o;}return h;}
};
struct Readout{set<int>D;bool fallback=false;int components=0,eligible=0;};
B axis(const Geo&g,const B&a,int d,int kind){B b(g.N);int st=g.st[d];for(int base=0;base<g.N;base++)if(g.coord[base][d]==0){int v=0;if(kind==0){for(int t=0;t<g.L;t++)v^=a[base+t*st];b[base]=v;}else if(kind==1){v=a[base+(g.L-1)*st];for(int t=0;t<g.L;t++)b[base+t*st]=v;}else{for(int t=g.L-1;t>=0;t--){b[base+t*st]=v;v^=a[base+t*st];}}}return b;}
set<int> globalH(const Geo&g,const set<int>&s){array<B,4> in;array<B,6> out;for(auto&a:in)a.resize(g.N);for(auto&a:out)a.resize(g.N);for(int e:s)in[e/g.N][e%g.N]=1;for(int k=0;k<4;k++)for(int j=0;j<4;j++)if(k!=j){B a=in[k];for(int ell=0;ell<j;ell++)a=axis(g,a,ell,ell==k?1:0);a=axis(g,a,j,2);int o=g.ori(k,j);for(int x=0;x<g.N;x++)out[o][x]^=a[x];}set<int>D;for(int o=0;o<6;o++)for(int x=0;x<g.N;x++)if(out[o][x])D.insert(o*g.N+x);return D;}
Readout decode(const Geo&g,const set<int>&s){Readout r;set<int> unseen=s;bool all=true;while(!unseen.empty()){
 int anchor=*unseen.begin()%g.N;map<int,Q> lift;lift[anchor]=g.coord[anchor];vector<int> queue{anchor};set<int> component;bool consistent=true;
 for(size_t h=0;h<queue.size();h++){int v=queue[h];Q q=lift[v];for(int a=0;a<4;a++)for(int sign:{-1,1}){int base=sign==1?v:g.dn[v][a],e=a*g.N+base;if(!s.count(e))continue;component.insert(e);unseen.erase(e);int w=sign==1?g.up[v][a]:g.dn[v][a];Q z=q;z[a]+=sign;auto it=lift.find(w);if(it==lift.end()){lift[w]=z;queue.push_back(w);}else if(it->second!=z)consistent=false;}}
 r.components++;Q lo=lift.begin()->second;array<set<int>,4> coords;for(auto &[v,q]:lift)for(int a=0;a<4;a++){lo[a]=min(lo[a],q[a]);coords[a].insert(g.coord[v][a]);}
 bool small=consistent;for(int a=0;a<4;a++)for(int x:coords[a])for(int y:coords[a]){int d=abs(x-y);d=min(d,g.L-d);if(8*d>=g.L)small=false;}
 if(!small){all=false;continue;}r.eligible++;
 set<K> cur;for(int e:component){Q q=lift.at(e%g.N);cur.insert({q[0],q[1],q[2],q[3],e/g.N});}
 for(int d=0;d<4;d++){set<K> next;for(K e:cur){int i=e[4];if(i==d)continue;Q q={e[0],e[1],e[2],e[3]};for(int t=lo[d];t<e[d];t++){q[d]=t;tog(r.D,g.ori(i,d)*g.N+g.pos(q));}e[d]=lo[d];tog(next,e);}cur=move(next);}check(cur.empty(),"local prism residual");
 }if(!all){r.fallback=true;r.D=globalH(g,s);}return r;}
vector<int> sweep(const Geo&g,const B&s,int v){bool incoming=false;vector<int>o;for(int a=0;a<4;a++){incoming|=s[a*g.N+g.dn[v][a]];if(s[a*g.N+v])o.push_back(a);}if(incoming)return {};check(o.size()%2==0,"odd outgoing physical syndrome");vector<int>f;for(size_t k=0;k<o.size();k+=2)f.push_back(g.ori(o[k],o[k+1])*g.N+v);return f;}
void flip(const Geo&g,B&E,B&s,int f){E[f]^=1;for(int e:g.bd(f))s[e]^=1;}
set<int> nonzero(const B&a){set<int>s;for(int i=0;i<(int)a.size();i++)if(a[i])s.insert(i);return s;}
struct RNG{mt19937_64 eng;uint64_t draws=0;RNG(uint64_t s):eng(s){}uint64_t raw(){draws++;return eng();}double unit(){return ((raw()>>11)+0.5)*0x1.0p-53;}uint64_t bounded(uint64_t n){uint64_t threshold=-n%n,x;do{x=raw();}while(x<threshold);return x%n;}};
uint64_t mix(uint64_t x){x+=0x9e3779b97f4a7c15ULL;x=(x^(x>>30))*0xbf58476d1ce4e5b9ULL;x=(x^(x>>27))*0x94d049bb133111ebULL;return x^(x>>31);}
void trial(int L,double alpha,double T,uint64_t seed,string method){check(L>=4 && L%2==0,"trial requires even L>=4");check(isfinite(alpha)&&alpha>=0&&isfinite(T)&&T>=0,"invalid alpha/T");check(method=="sweep"||method=="toom","unknown method");auto start=chrono::steady_clock::now();Geo g(L);B E(6*g.N),s(4*g.N);RNG clock(mix(seed^1)),kind(mix(seed^2)),noise(mix(seed^3)),correction(mix(seed^4));double R=g.N*(1+6*alpha),t=0;uint64_t na=0,ca=0,success=0,flips=0,two=0;while(true){t+=-log(clock.unit())/R;if(t>T)break;if(kind.unit()<6*alpha/(1+6*alpha)){int f=noise.bounded(6*g.N);flip(g,E,s,f);na++;}else{ca++;vector<int>fs;if(method=="sweep")fs=sweep(g,s,correction.bounded(g.N));else{int f=correction.bounded(6*g.N),o=f/g.N,x=f%g.N,i=pairs[o][0],j=pairs[o][1];if(s[i*g.N+g.up[x][j]] & s[j*g.N+g.up[x][i]])fs.push_back(f);}if(!fs.empty())success++;if(fs.size()==2)two++;for(int f:fs){flip(g,E,s,f);flips++;}}}
 check(g.gather(E)==s,"endpoint incremental syndrome");double dynamics=chrono::duration<double>(chrono::steady_clock::now()-start).count();auto rd=chrono::steady_clock::now();auto ss=nonzero(s);auto d=decode(g,ss);check(g.boundary(d.D)==ss,"recovery boundary");auto C=nonzero(E);for(int f:d.D)tog(C,f);check(g.boundary(C).empty(),"residual closed");int h=g.hom(C);double readout=chrono::duration<double>(chrono::steady_clock::now()-rd).count();
 cout<<setprecision(12)<<"{\"L\":"<<L<<",\"kappa\":1,\"T\":"<<T<<",\"alpha\":"<<alpha<<",\"lambda_over_face_attempt_rate\":"<<6*alpha<<",\"seed\":"<<seed<<",\"method\":\""<<method<<"\",\"failure\":"<<(h?1:0)<<",\"logical_bits\":"<<h<<",\"unresolved\":0,\"fallback\":"<<d.fallback<<",\"components\":"<<d.components<<",\"eligible_components\":"<<d.eligible<<",\"syndrome_weight\":"<<ss.size()<<",\"recovery_faces\":"<<d.D.size()<<",\"noise_attempts\":"<<na<<",\"correction_attempts\":"<<ca<<",\"successful_corrections\":"<<success<<",\"two_face_events\":"<<two<<",\"correction_face_flips\":"<<flips<<",\"check_reads\":"<<ca*(method=="sweep"?8:2)<<",\"rng_draws\":"<<clock.draws+kind.draws+noise.draws+correction.draws<<",\"dynamics_seconds\":"<<dynamics<<",\"readout_seconds\":"<<readout<<"}"<<endl;}
void tests(){uint64_t single=0,cubes=0;for(int L:{3,4,16}){Geo g(L);for(int o=0;o<6;o++){set<int>sheet;int i=pairs[o][0],j=pairs[o][1];for(int a=0;a<L;a++)for(int b=0;b<L;b++){Q q={0,0,0,0};q[i]=a;q[j]=b;sheet.insert(o*g.N+g.pos(q));}check(g.boundary(sheet).empty(),"sheet boundary");for(int cut=0;cut<L;cut++)check(g.hom(sheet,cut)==(1<<o),"sheet homology");}
 for(int f=0;f<6*g.N;f++){set<int>F{f};auto s=g.boundary(F);set<int>v;for(int e:s){int a=e/g.N,x=e%g.N;tog(v,x);tog(v,g.up[x][a]);}check(v.empty(),"d1d2");if(L==16){auto d=decode(g,s);check(!d.fallback&&g.boundary(d.D)==s,"single face local");for(int z:d.D)tog(F,z);check(g.hom(F)==0,"single face logical");single++;}}
 for(int x=0;x<g.N;x++)for(int a=0;a<4;a++)for(int b=a+1;b<4;b++)for(int c=b+1;c<4;c++){set<int>F;for(auto p:vector<array<int,3>>{{a,b,c},{a,c,b},{b,c,a}}){int o=g.ori(p[0],p[1]);F.insert(o*g.N+x);F.insert(o*g.N+g.up[x][p[2]]);}check(g.boundary(F).empty()&&g.hom(F)==0,"cube d2d3/hom");cubes++;}
 }
 Geo g(4);B E(6*g.N),s(4*g.N);mt19937_64 gen(20261015);for(int z=0;z<2000;z++){if(z%2==0)flip(g,E,s,gen()%(6*g.N));else for(int f:sweep(g,s,gen()%g.N))flip(g,E,s,f);check(g.gather(E)==s,"incremental random");}auto ss=nonzero(s);auto d=decode(g,ss);check(g.boundary(d.D)==ss,"global recovery");
 for(int mask=0;mask<16;mask++)if(__builtin_popcount((unsigned)mask)==2||mask==15){B a(4*g.N);for(int i=0;i<4;i++)a[i*g.N]=!!(mask&(1<<i));auto f=sweep(g,a,0);check(f.size()==size_t(__builtin_popcount((unsigned)mask)/2),"active pattern size");vector<int>o;for(int i=0;i<4;i++)if(mask&(1<<i))o.push_back(i);for(int k=0;k<(int)f.size();k++)check(f[k]==g.ori(o[2*k],o[2*k+1])*g.N,"fixed pairing");a[g.dn[0][0]]=1;check(sweep(g,a,0).empty(),"incoming veto");}
 cout<<"{\"status\":\"PASS\",\"all_L16_single_faces\":"<<single<<",\"cube_checks\":"<<cubes<<",\"incremental_steps\":2000,\"logical_sheets\":18,\"active_patterns\":7}"<<endl;
}
int main(int argc,char**argv){try{string mode=argc>1?argv[1]:"test";if(mode=="test")tests();else if(mode=="trial")trial(stoi(argv[2]),stod(argv[3]),stod(argv[4]),stoull(argv[5]),argv[6]);else if(mode=="kernel"){Geo g(stoi(argv[2]));B s(4*g.N);int e;while(cin>>e)s.at(e)=1;string method=argv[3];int site=stoi(argv[4]);vector<int> fs;if(method=="sweep")fs=sweep(g,s,site);else {int o=site/g.N,x=site%g.N,i=pairs[o][0],j=pairs[o][1];if(s[i*g.N+g.up[x][j]] & s[j*g.N+g.up[x][i]])fs.push_back(site);}for(int f:fs)cout<<f<<" ";cout<<"\n";}else if(mode=="decode"){Geo g(stoi(argv[2]));set<int>s;int e;while(cin>>e)s.insert(e);auto r=decode(g,s);cout<<r.fallback<<"\n";for(int f:r.D)cout<<f<<" ";cout<<"\n";}else throw runtime_error("mode");}catch(exception&e){cerr<<e.what()<<endl;return 1;}}
