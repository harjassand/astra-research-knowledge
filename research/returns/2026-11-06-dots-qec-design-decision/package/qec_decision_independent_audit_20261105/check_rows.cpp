// Independent full-denominator checker. Unlike the producer, there are no
// intermediate 16-bit upward roundings. Bounds below keep all sums <2^208.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
#include <string>
using U64=uint64_t;
// Minimal checked four-limb arithmetic. No multiplication wider than the
// native exact 64x64->128 product is needed by this checker.
struct uint256_t {
  std::array<U64,4> limb{};
  uint256_t(U64 a=0) { limb[0]=a; }
  static uint256_t product(U64 a,U64 b) {
    __uint128_t z=__uint128_t(a)*b; uint256_t t;
    t.limb[0]=U64(z);t.limb[1]=U64(z>>64);return t;
  }
  uint256_t& operator+=(const uint256_t& b) {
    __uint128_t carry=0;
    for(int i=0;i<4;i++) {__uint128_t z=__uint128_t(limb[i])+b.limb[i]+carry;limb[i]=U64(z);carry=z>>64;}
    if(carry)throw std::runtime_error("256-bit addition overflow");return *this;
  }
  friend uint256_t operator+(uint256_t a,const uint256_t& b) {a+=b;return a;}
  uint256_t operator<<(unsigned k) const {
    uint256_t z;
    for(unsigned i=0;i<4;i++) if(limb[i]) {
      unsigned j=i+k/64,r=k%64;
      if(j>=4)throw std::runtime_error("256-bit shift overflow");
      z.limb[j]|=limb[i]<<r;
      if(r && limb[i]>>(64-r)) {
        if(j+1>=4)throw std::runtime_error("256-bit shift overflow");
        z.limb[j+1]|=limb[i]>>(64-r);
      }
    }return z;
  }
  bool operator==(const uint256_t& b) const {return limb==b.limb;}
  bool operator!=(const uint256_t& b) const {return !(*this==b);}
  bool operator>(const uint256_t& b) const {for(int i=3;i>=0;i--)if(limb[i]!=b.limb[i])return limb[i]>b.limb[i];return false;}
};
template<class T> std::vector<T> read(std::ifstream& in, size_t n) {
  std::vector<T> a(n); in.read(reinterpret_cast<char*>(a.data()),n*sizeof(T));
  if (!in) throw std::runtime_error("truncated input"); return a;
}
unsigned bits(const uint256_t& a) { for(int i=3;i>=0;i--)if(a.limb[i])return 64*i+64-__builtin_clzll(a.limb[i]);return 0; }
int main(int argc,char**argv) {
  if(argc!=2) return 2;
  std::ifstream in(argv[1],std::ios::binary);
  auto head=read<U64>(in,7);
  const U64 nv=head[0],nd=head[1],m=head[2],N=head[3],D=head[4],Q=head[5],qden=head[6];
  if(!(nv<1000000 && nd<65536 && m<1000000 && N==64 && D<=64 && Q<=63 && qden==64)) return 3;
  auto eu=read<uint32_t>(in,m),ev=read<uint32_t>(in,m);
  auto cost=read<uint8_t>(in,m); auto q=read<U64>(in,m);
  auto dl=read<uint16_t>(in,nv),dr=read<uint16_t>(in,nv);
  auto side=read<uint8_t>(in,nv),distance=read<uint8_t>(in,nd*nd);
  auto U=read<U64>(in,nv*N),Jlo=read<U64>(in,nd*N),Jhi=read<U64>(in,nd*N);
  char extra; if(in.read(&extra,1)) return 4;
  std::vector<uint256_t> J(nd*N,0);
  unsigned max_j_bits=0,max_row_bits=0,max_lhs_bits=0;
  for(U64 e=0;e<m;e++) {
    if(eu[e]>=nv || ev[e]>=nv || cost[e]>15) return 5;
    for(int flip=0;flip<2;flip++) {
      U64 x=flip?ev[e]:eu[e],y=flip?eu[e]:ev[e];
      if(x>=nd || side[y]==1) continue;
      for(U64 r=0;r<N;r++)
        J[x*N+r]+=uint256_t::product(q[e],U[y*N+((r+cost[e])%N)])<<cost[e];
    }
  }
  for(U64 x=0;x<nd*N;x++) {
    max_j_bits=std::max(max_j_bits,bits(J[x]));
    if(bits(J[x])>128 || J[x] != uint256_t(Jlo[x])+(uint256_t(Jhi[x])<<64)) return 6;
  }
  U64 terminal_fractional_rows=0;
  for(U64 v=0;v<nv;v++) for(U64 r=0;r<N;r++) {
    uint256_t rhs=0;
    if(v<nd) for(U64 x=0;x<nd;x++) {
      U64 d=distance[v*nd+x]; if(d>D) return 7;
      rhs+=J[x*N+((r+N-d%N)%N)]<<(D-d);
    }
    if(side[v]!=1) {
      U64 residue=(r+N-dr[v]%N)%N;
      int exponent=int(Q+qden+D)-int(dr[v])-int(residue);
      // If tiny terminal mass is not representable, one integer unit is an
      // explicit conservative upper bound, never a downward truncation.
      if(exponent>=0) rhs+=uint256_t(1)<<exponent;
      else { rhs+=1; terminal_fractional_rows++; }
    }
    uint256_t lhs=uint256_t(U[v*N+r])<<(qden+D);
    max_row_bits=std::max(max_row_bits,bits(rhs));
    max_lhs_bits=std::max(max_lhs_bits,bits(lhs));
    if(rhs>lhs) {std::cerr<<"invalid row "<<v<<","<<r<<"\n";return 8;}
  }
  std::cout<<"{\"all_full_denominator_rows_pass\":true,\"rows\":"<<nv*N
           <<",\"gap_terms\":"<<nd*nd*N<<",\"J_entries_rebuilt\":"<<nd*N
           <<",\"maximum_J_bits\":"<<max_j_bits<<",\"maximum_row_bits\":"<<max_row_bits
           <<",\"maximum_LHS_bits\":"<<max_lhs_bits
           <<",\"fractional_terminal_rows_rounded_up\":"<<terminal_fractional_rows<<"}\n";
  return 0;
}
