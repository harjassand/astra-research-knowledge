// Exact integer sampling with an O(log n) dynamic potential.
// g++ -std=c++17 -O3 all_order_sampler.cpp -o producer-workspace/astra_all_order_sampler
// Run: sampler n samples seed output.json. 4<=n<=65536.
// Worst-case intermediate integers fit signed 128 bits in this range.
#include <algorithm>
#include <array>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <random>
#include <string>
#include <vector>
using I=__int128_t;using U=__uint128_t;
struct Agg{int count=0;std::array<I,4>p={0,0,0,0};I e2=0,e3=0;};
Agg one(int x){Agg a;a.count=1;a.p={1,x,I(x)*x,I(x)*x*x};return a;}
Agg cat(const Agg&a,const Agg&b){
 Agg z;z.count=a.count+b.count;I s=(a.count%2?-1:1);
 for(int k=0;k<4;k++)z.p[k]=a.p[k]+s*b.p[k];
 z.e2=a.e2+b.e2+s*(a.p[0]*b.p[2]-2*a.p[1]*b.p[1]+a.p[2]*b.p[0]);
 z.e3=a.e3+b.e3+s*(a.p[0]*b.p[3]-3*a.p[1]*b.p[2]+3*a.p[2]*b.p[1]-a.p[3]*b.p[0]);return z;
}
struct Node{int key,height=1;Node*left=nullptr,*right=nullptr;Agg a;explicit Node(int x):key(x),a(one(x)){};};
int ht(Node*t){return t?t->height:0;}int cnt(Node*t){return t?t->a.count:0;}Agg ag(Node*t){return t?t->a:Agg();}
void pull(Node*t){t->height=1+std::max(ht(t->left),ht(t->right));t->a=cat(cat(ag(t->left),one(t->key)),ag(t->right));}
Node*rr(Node*y){Node*x=y->left;Node*t=x->right;x->right=y;y->left=t;pull(y);pull(x);return x;}
Node*lr(Node*x){Node*y=x->right;Node*t=y->left;y->left=x;x->right=t;pull(x);pull(y);return y;}
Node*bal(Node*t){
 if(!t)return t;
 pull(t);int b=ht(t->left)-ht(t->right);
 if(b>1){if(ht(t->left->left)<ht(t->left->right))t->left=lr(t->left);return rr(t);}
 if(b< -1){if(ht(t->right->right)<ht(t->right->left))t->right=rr(t->right);return lr(t);}return t;
}
Node*ins(Node*t,int x){if(!t)return new Node(x);if(x<t->key)t->left=ins(t->left,x);else if(x>t->key)t->right=ins(t->right,x);else assert(false);return bal(t);}
Node*del(Node*t,int x){
 assert(t);if(x<t->key)t->left=del(t->left,x);else if(x>t->key)t->right=del(t->right,x);
 else{if(!t->left||!t->right){Node*q=t->left?t->left:t->right;delete t;return q;}
 Node*q=t->right;while(q->left)q=q->left;t->key=q->key;t->right=del(t->right,q->key);}return bal(t);
}
bool has(Node*t,int x){while(t){if(x==t->key)return true;t=x<t->key?t->left:t->right;}return false;}
Node*toggle(Node*t,int x){return has(t,x)?del(t,x):ins(t,x);}
int rankkey(Node*t,int k){assert(t&&k>=0&&k<cnt(t));int l=cnt(t->left);if(k<l)return rankkey(t->left,k);if(k==l)return t->key;return rankkey(t->right,k-l-1);}
void collect(Node*t,std::vector<int>&v){if(t){collect(t->left,v);v.push_back(t->key);collect(t->right,v);}}
void destroy(Node*t){if(t){destroy(t->left);destroy(t->right);delete t;}}
I hnum(Node*t,int n){I z=3*I(n)*t->a.e2-2*t->a.e3;assert(z>=0&&z%6==0);return z/6;}
I slow_h(const std::vector<int>&v,int n){
 int k=v.size();std::vector<int>g;for(int i=0;i+1<k;i++)g.push_back(v[i+1]-v[i]);g.push_back(n+v[0]-v.back());
 I p[2]={0,0},q[2][2]={{0,0},{0,0}},z=0;
 for(int i=0;i<k;i++){int t=i%2;z+=g[i]*q[t][1-t];for(int j=0;j<2;j++)q[j][t]+=p[j]*g[i];p[t]+=g[i];}return z;
}
U uniform(std::mt19937_64&rng,U limit){
 assert(limit>0);if(limit==1)return 0;U max=limit-1;int bits=0;while(max){++bits;max>>=1;}
 U mask=(U(1)<<bits)-1;for(;;){U x=U(rng());if(bits>64)x|=U(rng())<<64;x&=mask;if(x<limit)return x;}
}
int main(int argc,char**argv){
 if(argc!=5&&argc!=6){std::cerr<<"n samples seed output.json [--stream]\n";return 2;}
 int n=std::stoi(argv[1]),samples=std::stoi(argv[2]);assert(n>=4&&n<=65536&&samples>=2);
 bool streaming=(argc==6&&std::string(argv[5])=="--stream");
 std::ofstream streamfile;std::ostream*streamout=nullptr;
 if(streaming){if(std::string(argv[4])=="-")streamout=&std::cout;else{streamfile.open(argv[4]);streamout=&streamfile;}
 *streamout<<"{\"type\":\"header\",\"n\":"<<n<<",\"samples\":"<<samples<<",\"seed\":\""<<argv[3]<<"\"}\n";}
 std::mt19937_64 rng(std::stoull(argv[3]));I n2=I(n)*n,D=3*(n2+1),mass=D+4*(D-4);
 std::map<std::vector<int>,uint64_t>hist;uint64_t attempts=0,events=0,max_attempts=0,max_events=0;
 int max_particles=3,max_height=2;auto started=std::chrono::steady_clock::now();
 for(int sample=0;sample<samples;sample++){
  Node*t=nullptr;for(int x:{0,1,2})t=ins(t,x);uint64_t pa=0,pe=0;
  for(;;){
   ++pa;int N=cnt(t);I h=hnum(t,n);assert(h>0);
   if(uniform(rng,U(mass))<U(D)){
    I kill=((n2-1)*n+2*(n2+1))*N-2*n2*n+4*N*h;I den=I(N)*D*h;assert(kill>=0&&kill<=den);
    if(uniform(rng,U(den))<U(kill)){++pe;break;}
   }else{
    int i=rankkey(t,int(uniform(rng,U(N))));I typ=I(uniform(rng,U(D-4)));
    int l=(i+n-1)%n,r=(i+1)%n,u,v;
    if(typ<n2-1){u=i;v=l;}else if(typ<2*(n2-1)){u=i;v=r;}else{u=l;v=r;}
    t=toggle(toggle(t,u),v);I hn=hnum(t,n);assert(hn<=4*h);
    if(uniform(rng,U(4*h))<U(hn))++pe;else t=toggle(toggle(t,u),v);
   }
   max_particles=std::max(max_particles,cnt(t));max_height=std::max(max_height,ht(t));
  }
  std::vector<int>state;collect(t,state);assert(hnum(t,n)==slow_h(state,n));
  int offset=state.front();for(auto&x:state)x-=offset;
  if(streaming){*streamout<<"{\"type\":\"sample\",\"state\":[";for(size_t j=0;j<state.size();j++){if(j)*streamout<<",";*streamout<<state[j];}*streamout<<"]}\n";}
  else hist[state]++;
  destroy(t);
  attempts+=pa;events+=pe;max_attempts=std::max(max_attempts,pa);max_events=std::max(max_events,pe);
 }
 double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count();
 if(streaming){*streamout<<"{\"type\":\"footer\",\"total_proposals\":"<<attempts<<",\"total_events\":"<<events<<",\"max_proposals\":"<<max_attempts<<",\"max_events\":"<<max_events<<",\"max_active_particles\":"<<max_particles<<",\"max_tree_height\":"<<max_height<<",\"seconds\":"<<seconds<<"}\n";return 0;}
 std::ofstream out(argv[4]);
 out<<"{\n\"n\":"<<n<<",\"samples\":"<<samples<<",\"seed\":\""<<argv[3]<<"\",\n";
 out<<"\"total_proposals\":"<<attempts<<",\"total_events\":"<<events<<",\"max_proposals\":"<<max_attempts<<",\"max_events\":"<<max_events<<",\n";
 out<<"\"max_active_particles\":"<<max_particles<<",\"max_tree_height\":"<<max_height<<",\"seconds\":"<<seconds<<",\n\"terminal_histogram\":[\n";
 bool first=true;for(const auto&kv:hist){if(!first)out<<",\n";first=false;out<<"{\"state\":[";for(size_t i=0;i<kv.first.size();i++){if(i)out<<",";out<<kv.first[i];}out<<"],\"count\":"<<kv.second<<"}";}out<<"\n]}\n";
 std::cout<<"n="<<n<<" samples="<<samples<<" proposals="<<attempts<<" events="<<events<<" maxN="<<max_particles<<" height="<<max_height<<" seconds="<<seconds<<"\n";
}
