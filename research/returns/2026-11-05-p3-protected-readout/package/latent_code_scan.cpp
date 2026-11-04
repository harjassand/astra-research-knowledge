#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <vector>
int main(int argc,char**argv){
  if(argc!=3)return 2;
  std::ifstream in(argv[1],std::ios::binary);
  uint32_t m,n,w,r;in.read((char*)&m,4);in.read((char*)&n,4);in.read((char*)&w,4);in.read((char*)&r,4);
  if(n>64 || w!=4) return 2;
  std::vector<uint8_t> base(n);std::vector<std::array<uint64_t,4>> col(n);
  std::set<std::pair<uint64_t,uint64_t>> checks;uint64_t tested=0,accepted=0;
  std::map<std::pair<uint64_t,uint64_t>,int> signs;
  for(uint32_t t=0;t<m;++t){
    in.read((char*)base.data(),n);in.read((char*)col.data(),n*32);
    for(uint32_t a=0;a<n;++a)for(uint32_t b=a+1;b<n;++b)for(uint32_t c=b+1;c<n;++c)for(uint32_t d=c+1;d<n;++d){
      unsigned count=0;
      for(int j=0;j<4;++j)count+=__builtin_popcountll(col[a][j]^col[b][j]^col[c][j]^col[d][j]);
      ++tested;
      if(count<=r/8 || count>=7*r/8){
        uint64_t x=0,z=0;
        for(auto e:{a,b,c,d}){if(base[e]&1)x|=1ULL<<e;if(base[e]&2)z|=1ULL<<e;}
        const int sign=2*count<r?1:-1;
        auto found=signs.find({x,z});
        if(found!=signs.end() && found->second!=sign){std::cerr<<"inconsistent accepted check sign\n";return 4;}
        signs[{x,z}]=sign;checks.insert({x,z});++accepted;
      }
    }
  }
  std::cout<<"# tested="<<tested<<" accepted_pattern_checks="<<accepted<<" unique="<<checks.size()<<"\n";
  for(auto p:checks)std::cout<<p.first<<" "<<p.second<<"\n";
  std::ofstream signout(argv[2]);signout<<"[\n";bool first=true;
  for(auto entry:signs){
    if(!first)signout<<",\n";first=false;
    signout<<"  {\"x\":"<<entry.first.first<<",\"z\":"<<entry.first.second<<",\"sign\":"<<entry.second<<"}";
  }
  signout<<"\n]\n";
}
