#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <iostream>
#include <fstream>
#include <algorithm>
#include <string>
using u64=uint64_t;using u128=__uint128_t;
template<class T> void readv(std::ifstream& f,std::vector<T>& v){f.read((char*)v.data(),v.size()*sizeof(T));if(!f)std::abort();}
std::string str(u128 x){if(!x)return "0";std::string s;while(x){s.push_back('0'+x%10);x/=10;}std::reverse(s.begin(),s.end());return s;}
int main(int argc,char**argv){
 if(argc!=3)return 2;std::ifstream f(argv[1],std::ios::binary);u64 n,m,N,wb,qb;f.read((char*)&n,8);f.read((char*)&m,8);f.read((char*)&N,8);f.read((char*)&wb,8);f.read((char*)&qb,8);
 std::vector<u64> row(n+1),lo(n),hi(n),W(n),U(n*N);std::vector<uint32_t> col(m);std::vector<int8_t> delta(n);std::vector<uint8_t>end(n);readv(f,row);readv(f,col);readv(f,lo);readv(f,hi);readv(f,delta);readv(f,end);readv(f,W);readv(f,U);
 std::vector<u128>w(n);for(u64 i=0;i<n;i++)w[i]=(u128(hi[i])<<64)|lo[i];u128 D=u128(1)<<wb;
 u128 maxsum=0;u64 maxW=0,maxdefect=0;
 for(u64 i=0;i<n;i++){
  u128 s=0;for(u64 k=row[i];k<row[i+1];k++){u128 p=w[col[k]]*W[col[k]];if(~u128(0)-s<p)std::abort();s+=p;}
  if(W[i]==0 || u128(W[i]-1)*D<s){std::cerr<<"Scalar supersolution failed "<<i<<"\n";return 3;}
  maxW=std::max(maxW,W[i]);
  for(u64 r=0;r<N;r++){
   u128 a=0;for(u64 k=row[i];k<row[i+1];k++){u64 j=col[k],rr=(int64_t(r)+delta[j]+N)%N;u128 p=w[j]*U[j*N+rr];if(~u128(0)-a<p)std::abort();a+=p;}
   maxsum=std::max(maxsum,a);u64 rhs=u64((a+D-1)>>wb);if(end[i])rhs+=(r<=qb?u64(1)<<(qb-r):1);
   u64 own=U[i*N+r];if(rhs>own)maxdefect=std::max(maxdefect,rhs-own);
  }
 }
 for(u64 i=0;i<n;i++)for(u64 r=0;r<N;r++){u128 v=u128(U[i*N+r])+u128(maxdefect)*W[i];if(v>UINT64_MAX)std::abort();U[i*N+r]=u64(v);}
 u64 maxU=0;
 for(u64 i=0;i<n;i++)for(u64 r=0;r<N;r++){
  u128 a=0;for(u64 k=row[i];k<row[i+1];k++){u64 j=col[k],rr=(int64_t(r)+delta[j]+N)%N;u128 p=w[j]*U[j*N+rr];if(~u128(0)-a<p)std::abort();a+=p;}
  if(end[i]){u64 term=(r<=qb?u64(1)<<(qb-r):1);a+=u128(term)*D;}
  if(u128(U[i*N+r])*D<a){std::cerr<<"Folded supersolution failed "<<i<<","<<r<<"\n";return 4;}
  maxU=std::max(maxU,U[i*N+r]);
 }
 std::ofstream out(argv[2],std::ios::binary);out.write((char*)U.data(),U.size()*8);out.close();
 std::cout<<"{\"all_integer_inequalities_pass\":true,\"states\":"<<n<<",\"modulus\":"<<N<<",\"transitions\":"<<m<<",\"weight_denominator_exponent\":"<<wb<<",\"table_denominator_exponent\":"<<qb<<",\"maximum_grid_defect_before_repair\":"<<maxdefect<<",\"maximum_scalar_witness\":"<<maxW<<",\"maximum_table_integer\":"<<maxU<<",\"maximum_accumulator_before_repair\":\""<<str(maxsum)<<"\"}\n";
}
