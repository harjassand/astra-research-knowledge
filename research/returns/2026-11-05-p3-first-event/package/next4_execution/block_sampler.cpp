#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>
// Diagnostic continuous block implementation.
// Rational kernel/rare-state choices use integer sampling.
// Standard-library Poisson, gamma, binomial and floating timestamps are
// diagnostic conveniences, not the report's finite clock implementation.
using u128=__uint128_t;
struct Engine {
  using result_type=uint64_t;
  std::mt19937_64 core;uint64_t calls=0;
  explicit Engine(uint64_t s):core(s){}
  static constexpr uint64_t min(){return 0;}
  static constexpr uint64_t max(){return UINT64_MAX;}
  uint64_t operator()(){++calls;return core();}
};
struct Model {
  Engine rng;
  const u128 D=(u128(1)<<100);
  uint64_t updates=0,integer_draws=0,rejection_retries=0;
  uint64_t poisson_draws=0,gamma_draws=0,binomial_draws=0;
  uint64_t block_proposals=0,prefix_updates=0;
  Model(uint64_t s):rng(s){}
  u128 bits(unsigned k){
    if(k<=64)return u128(rng()>>(64-k));
    return ((u128(rng())<<64)|u128(rng()))>>(128-k);
  }
  u128 below(u128 n){
    ++integer_draws;if(n==1)return 0;
    unsigned k=0;u128 t=n-1;while(t){++k;t>>=1;}
    for(unsigned a=0;a<128;++a){
      u128 z=bits(k);if(z<n)return z;++rejection_retries;
    }
    throw std::runtime_error("integer rejection cap");
  }
  int stationary(){
    // pi=(2(1-3d)/3,(1-3d)/3,d,2d), d=2^-100.
    if(bits(100)<3)return below(3)==0?2:3;
    return below(3)<2?0:1;
  }
  int rare(){return below(3)==0?2:3;}
  int step(int x,bool reverse){
    ++updates;unsigned c=unsigned(rng()&3u);
    if(c==0)return stationary();
    if(c>=2)return x;
    bool fire=false;
    if(x==0)fire=below(2*(D-3))<3;
    if(x==1)fire=below(D-3)<3;
    if(x==2)fire=true;
    if(x==3)fire=(rng()&1u)==0;
    if(!fire)return x;
    static const int next[4]={2,3,1,0};
    static const int prev[4]={3,2,0,1};
    return reverse?prev[x]:next[x];
  }
  int poisson(double mean){
    ++poisson_draws;
    int n=std::poisson_distribution<int>(mean)(rng);
    if(n>int(2*mean+256))throw std::runtime_error("Poisson diagnostic cap");
    return n;
  }
  double uniform(){return std::generate_canonical<double,53>(rng);}
  double order_time(int k,int n,double L){
    if(k==0)return 0.;
    gamma_draws+=2;
    double a=std::gamma_distribution<double>(k,1.)(rng);
    double b=std::gamma_distribution<double>(n+1-k,1.)(rng);
    return L*(a/(a+b));
  }
};
struct Block {
  bool good=false;
  int n=0,first=0,countB=0,terminal=-1,preceding=-1;
  double time=0.;std::vector<int> x;
};
Block proposal(Model& m,int L,double H,bool wrong_reverse=false){
  ++m.block_proposals;Block b;
  if(m.below(L+1)==0){
    // Initial-B branch cannot satisfy G; its rest need not be drawn.
    b.countB=1;return b;
  }
  b.n=m.poisson(L)+1;
  int mark=1+int(m.below(b.n));
  b.x.resize(b.n+1);b.x[mark]=m.rare();
  for(int i=mark;i>0;--i)b.x[i-1]=m.step(b.x[i],!wrong_reverse);
  for(int i=mark;i<b.n;++i)b.x[i+1]=m.step(b.x[i],false);
  b.first=-1;
  for(int i=0;i<=b.n;++i)if(b.x[i]>=2){
    ++b.countB;if(b.first<0)b.first=i;
  }
  if(b.first<0)throw std::runtime_error("missing Palm witness");
  b.time=m.order_time(b.first,b.n,L);
  b.good=b.first>0&&b.time>H;
  if(b.good){b.terminal=b.x[b.first];b.preceding=b.x[b.first-1];}
  return b;
}
struct Record {
  bool early=false;
  int terminal=0,preceding=0,initial_window=0;
  double block_time=0.;uint64_t block_bin=0;
  std::vector<std::array<int64_t,3>> jumps;
};
Record record_from(Model& m,const Block& b,double H,unsigned digits){
  Record r;
  r.terminal=b.terminal;r.preceding=b.preceding;r.block_time=b.time;
  r.block_bin=uint64_t(std::floor(std::ldexp(b.time,digits)));
  double span=std::min(H,b.time);int previous=b.first-1,inside=0;
  if(previous>0&&span>0.){
    ++m.binomial_draws;
    inside=std::binomial_distribution<int>(previous,span/b.time)(m.rng);
  }
  int start=b.first-inside-1;r.initial_window=b.x[start];
  std::vector<double> local(inside);
  for(double& z:local)z=span*m.uniform();
  std::sort(local.begin(),local.end());
  for(int j=0;j<inside;++j){
    int idx=start+j+1;
    if(b.x[idx]!=b.x[idx-1]){
      int64_t age=int64_t(std::floor(std::ldexp(span-local[j],digits)));
      r.jumps.push_back({age,b.x[idx-1],b.x[idx]});
    }
  }
  r.jumps.push_back({0,b.x[b.first-1],b.x[b.first]});return r;
}
bool observed_prefix(Model& m,int b,double H,unsigned digits,Record& out){
  int n=m.poisson(b);Block p;p.n=n;p.x.resize(n+1);p.x[0]=0;p.first=-1;
  for(int j=1;j<=n;++j){
    p.x[j]=m.step(p.x[j-1],false);++m.prefix_updates;
    if(p.first<0&&p.x[j]>=2)p.first=j;
  }
  if(p.first<0)return false;
  p.time=m.order_time(p.first,n,b);
  p.terminal=p.x[p.first];p.preceding=p.x[p.first-1];
  out=record_from(m,p,H,digits);out.early=true;return true;
}
void write_record(std::ostream& out,const Record& r){
  out<<"{\"early\":"<<(r.early?"true":"false")
     <<",\"terminal\":"<<r.terminal<<",\"preceding\":"<<r.preceding
     <<",\"window_initial\":"<<r.initial_window
     <<",\"block_time\":"<<std::setprecision(17)<<r.block_time
     <<",\"block_bin\":"<<r.block_bin<<",\"jumps\":[";
  for(size_t j=0;j<r.jumps.size();++j){
    if(j)out<<",";
    out<<"["<<r.jumps[j][0]<<","<<r.jumps[j][1]<<","<<r.jumps[j][2]<<"]";
  }
  out<<"]}";
}
int main(int argc,char** argv){
  int Ncal=argc>1?std::stoi(argv[1]):4096;
  int Nout=argc>2?std::stoi(argv[2]):1024;
  std::string path=argc>3?argv[3]:"block_results.json";
  const int L=65536,b=320;const double H=5.;const unsigned digits=10;
  Model m(2026110504ULL);auto begin=std::chrono::steady_clock::now();
  std::map<int,uint64_t> hist;uint64_t cal_bad=0;
  for(int k=0;k<Ncal;++k){
    Block z=proposal(m,L,H);
    if(z.good)++hist[z.countB];else++cal_bad;
  }
  uint64_t after_cal_updates=m.updates,after_cal_calls=m.rng.calls;
  auto cal_end=std::chrono::steady_clock::now();
  std::vector<Record> records;int early_count=0;
  for(int k=0;k<Nout;++k){
    Record r;
    if(observed_prefix(m,b,H,digits,r)){
      ++early_count;records.push_back(std::move(r));continue;
    }
    bool accepted=false;
    for(int tries=0;tries<4096;++tries){
      Block z=proposal(m,L,H);
      if(z.good&&m.below(z.countB)==0){
        records.push_back(record_from(m,z,H,digits));accepted=true;break;
      }
    }
    if(!accepted)throw std::runtime_error("conditional rejection cap");
  }
  auto end=std::chrono::steady_clock::now();std::ofstream out(path);
  out<<std::setprecision(17)
     <<"{\"rare_bits\":100,\"R\":4,\"g_lower\":0.25,\"L\":"<<L
     <<",\"buffer\":"<<b<<",\"H\":"<<H<<",\"digits\":"<<digits
     <<",\"calibration_proposals\":"<<Ncal<<",\"output_count\":"<<Nout
     <<",\"calibration_bad\":"<<cal_bad<<",\"calibration_histogram\":{";
  bool first=true;for(auto [n,c]:hist){
    if(!first)out<<",";
    first=false;out<<"\""<<n<<"\":"<<c;
  }
  out<<"},\"counts\":{\"updates\":"<<m.updates
     <<",\"calibration_updates\":"<<after_cal_updates
     <<",\"rng_words\":"<<m.rng.calls<<",\"calibration_rng_words\":"<<after_cal_calls
     <<",\"integer_draws\":"<<m.integer_draws
     <<",\"integer_rejection_retries\":"<<m.rejection_retries
     <<",\"poisson_draws\":"<<m.poisson_draws
     <<",\"gamma_draws\":"<<m.gamma_draws
     <<",\"binomial_draws\":"<<m.binomial_draws
     <<",\"proposals\":"<<m.block_proposals
     <<",\"prefix_updates\":"<<m.prefix_updates<<",\"early_events\":"<<early_count
     <<"},\"seconds\":{\"calibration\":"
     <<std::chrono::duration<double>(cal_end-begin).count()
     <<",\"total\":"<<std::chrono::duration<double>(end-begin).count()
     <<"},\"records\":[";
  for(size_t j=0;j<records.size();++j){
    if(j)out<<",";
    write_record(out,records[j]);
  }
  out<<"]}\n";
  std::cout<<"completed "<<Ncal<<" calibration proposals and "<<Nout
           <<" conditional records; "<<m.updates<<" kernel updates\n";
}
