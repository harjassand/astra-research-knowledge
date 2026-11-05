// Exact rational random-scan heat bath, accelerated for <=60 binary variables
// and transition denominators fitting in unsigned 128 bits. No floating point.
// mt19937_64 is a reproducible diagnostic bit source. The probability proof
// assumes independent fair words, not a theorem about this PRNG.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <limits>
#include <map>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>
using U = unsigned __int128;
using Q = std::pair<U,U>;
U parse_u(const std::string& s) {
    U out=0, mx=~U(0);
    if(s.empty()) throw std::runtime_error("empty integer");
    for(char c:s) { if(c<'0'||c>'9'||out>(mx-U(c-'0'))/10)
      throw std::runtime_error("integer exceeds unsigned 128-bit accelerator");
      out=10*out+U(c-'0'); }
    return out;
}
int bits(U n) {int b=0; while(n){++b;n>>=1;}return b;}
struct Bits {
    std::mt19937_64 prng;
    uint64_t calls=0, words=0, rejected=0, cap;
    unsigned retries;
    Bits(uint64_t seed, uint64_t cap_, unsigned r):prng(seed),cap(cap_),retries(r){}
    U get(unsigned b) {
        if(!b) return 0;
        U v=prng(); ++words;
        if(b>64){v|=U(prng())<<64;++words;}
        if(b<128) v&=(U(1)<<b)-1;
        return v;
    }
    U below(U n) {
        if(n==0) throw std::runtime_error("zero random denominator");
        if(++calls>cap) throw std::runtime_error("random operation cap exceeded");
        if(n==1)return 0;
        unsigned b=bits(n-1);
        for(unsigned k=0;k<retries;++k){U z=get(b);if(z<n)return z;++rejected;}
        throw std::runtime_error("rational randomness rejection cap exceeded");
    }
    bool bernoulli(Q q){return below(q.second)<q.first;}
};
int main(){
  try {
    unsigned m; if(!(std::cin>>m)||m>60)throw std::runtime_error("bad variable count");
    std::vector<std::vector<unsigned>> nb(m);
    std::vector<std::vector<Q>> q(m);
    for(unsigned i=0;i<m;++i){
      unsigned d;std::cin>>d;nb[i].resize(d);for(auto&j:nb[i])std::cin>>j;
      uint64_t cnt;std::cin>>cnt;if(d>=24||cnt!=(uint64_t(1)<<d))
        throw std::runtime_error("bad conditional table size");
      q[i].reserve(cnt);
      for(uint64_t j=0;j<cnt;++j){std::string a,b;std::cin>>a>>b;
        U aa=parse_u(a),bb=parse_u(b);if(!bb||aa>bb)throw std::runtime_error("bad probability");
        q[i].push_back({aa,bb});}
    }
    uint64_t pinmask,pinvals,steps,count,seed,cap;unsigned retries,keep;
    std::cin>>pinmask>>pinvals>>steps>>count>>seed>>cap>>retries>>keep;
    if(!std::cin||retries==0)throw std::runtime_error("bad run arguments");
    Bits rng(seed,cap,retries);
    std::vector<unsigned> active;
    for(unsigned i=0;i<m;++i)if(!(pinmask&(uint64_t(1)<<i)))active.push_back(i);
    std::map<uint64_t,uint64_t> hist;
    std::vector<uint64_t> states;if(keep)states.reserve(count);
    for(uint64_t k=0;k<count;++k){
      uint64_t x=pinvals;
      if(!active.empty())for(uint64_t t=0;t<steps;++t){
        unsigned i=active[(uint64_t)rng.below(active.size())];
        uint64_t z=0;for(unsigned j=0;j<nb[i].size();++j)
          z|=((x>>nb[i][j])&1)<<j;
        bool v=rng.bernoulli(q[i][z]);
        x=(x&~(uint64_t(1)<<i))|(uint64_t(v)<<i);
      }
      ++hist[x];if(keep)states.push_back(x);
    }
    std::cout<<"{\"hist\":[";bool first=true;
    for(auto [x,n]:hist){if(!first)std::cout<<',';first=false;std::cout<<'['<<x<<','<<n<<']';}
    std::cout<<"],\"calls\":"<<rng.calls<<",\"words64\":"<<rng.words
      <<",\"rejected_integer_trials\":"<<rng.rejected<<",\"states\":[";
    first=true;for(auto x:states){if(!first)std::cout<<',';first=false;std::cout<<x;}
    std::cout<<"]}\n";
  }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 2;}
}
