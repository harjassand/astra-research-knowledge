#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <vector>

struct Record { uint64_t key; uint32_t a,b; };

int main(int argc,char**argv){
  if(argc!=5) return 2;
  std::ifstream in(argv[1],std::ios::binary);
  uint32_t m,n,w,r;in.read((char*)&m,4);in.read((char*)&n,4);in.read((char*)&w,4);in.read((char*)&r,4);
  const uint32_t t=std::strtoul(argv[2],nullptr,10);
  const uint64_t cap=std::strtoull(argv[3],nullptr,10);
  if(n>64 || w!=4 || t==0 || t>=64 || t>=r) return 2;
  const uint64_t mask=(1ULL<<t)-1;
  const uint32_t held=r-t;
  std::vector<uint8_t> base(n);std::vector<std::array<uint64_t,4>> col(n);
  std::set<std::pair<uint64_t,uint64_t>> checks;
  std::map<std::pair<uint64_t,uint64_t>,int> signs;
  uint64_t pair_records=0,collisions=0,overlap=0,proposals=0,accepted=0;
  for(uint32_t round=0;round<m;++round){
    in.read((char*)base.data(),n);in.read((char*)col.data(),n*32);
    std::vector<Record> pairs;pairs.reserve(n*(n-1)/2);
    for(uint32_t a=0;a<n;++a)for(uint32_t b=a+1;b<n;++b){
      uint64_t key=(col[a][0]^col[b][0])&mask;
      key=std::min(key,key^mask); // collision or complement: either check sign
      pairs.push_back({key,a,b});++pair_records;
    }
    std::sort(pairs.begin(),pairs.end(),[](const Record&a,const Record&b){
      if(a.key!=b.key)return a.key<b.key;
      if(a.a!=b.a)return a.a<b.a;
      return a.b<b.b;
    });
    std::set<uint64_t> supports;
    for(size_t begin=0;begin<pairs.size();){
      size_t end=begin+1;while(end<pairs.size() && pairs[end].key==pairs[begin].key)++end;
      for(size_t i=begin;i<end;++i)for(size_t j=i+1;j<end;++j){
        if(++collisions>cap){std::cerr<<"collision cap exceeded\n";return 3;}
        const auto &p=pairs[i],&q=pairs[j];
        if(p.a==q.a || p.a==q.b || p.b==q.a || p.b==q.b){++overlap;continue;}
        supports.insert((1ULL<<p.a)|(1ULL<<p.b)|(1ULL<<q.a)|(1ULL<<q.b));
      }
      begin=end;
    }
    for(uint64_t support:supports){
      ++proposals;
      uint64_t x=0,z=0;std::array<uint64_t,4> parity={0,0,0,0};
      for(uint64_t bits=support;bits;bits&=bits-1){
        unsigned e=__builtin_ctzll(bits);
        if(base[e]&1)x|=1ULL<<e;if(base[e]&2)z|=1ULL<<e;
        for(int j=0;j<4;++j)parity[j]^=col[e][j];
      }
      parity[0]&=~mask; // discovery bits are never reused for verification
      unsigned ones=0;for(auto word:parity)ones+=__builtin_popcountll(word);
      const int64_t signed_sum=int64_t(held)-2*int64_t(ones);
      if(2*std::llabs(signed_sum)>held){
        const int sign=signed_sum>0?1:-1;
        auto found=signs.find({x,z});
        if(found!=signs.end() && found->second!=sign){std::cerr<<"inconsistent accepted check sign\n";return 4;}
        signs[{x,z}]=sign;checks.insert({x,z});++accepted;
      }
    }
  }
  std::cout<<"# {\"pair_records\":"<<pair_records<<",\"collision_comparisons\":"<<collisions
           <<",\"overlapping_comparisons_discarded\":"<<overlap<<",\"held_out_verification_proposals\":"<<proposals
           <<",\"accepted_pattern_checks\":"<<accepted<<",\"unique_checks\":"<<checks.size()
           <<",\"discovery_rows_per_pattern\":"<<t<<",\"fresh_verification_rows_per_pattern\":"<<held
           <<",\"collision_cap\":"<<cap<<",\"cap_exceeded\":false,\"verification_threshold\":0.5}\n";
  for(auto p:checks)std::cout<<p.first<<" "<<p.second<<"\n";
  std::ofstream signout(argv[4]);signout<<"[\n";bool first=true;
  for(auto entry:signs){
    if(!first)signout<<",\n";first=false;
    signout<<"  {\"x\":"<<entry.first.first<<",\"z\":"<<entry.first.second<<",\"sign\":"<<entry.second<<"}";
  }
  signout<<"\n]\n";
}
