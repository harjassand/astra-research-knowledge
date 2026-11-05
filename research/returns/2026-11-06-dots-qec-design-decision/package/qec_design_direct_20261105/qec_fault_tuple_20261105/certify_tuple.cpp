#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using u64=uint64_t;using u128=__uint128_t;
template<class T>void rd(std::ifstream&f,std::vector<T>&v){f.read((char*)v.data(),v.size()*sizeof(T));if(!f)std::abort();}
int bits(u128 a){int k=0;while(a){a>>=1;k++;}return k;}
u128 upshift(u128 a,int s){if(!a)return 0;if(s<=0)return a<<(-s);if(s>=128)return 1;return (a>>s)+((a&((u128(1)<<s)-1))!=0);}
int main(int argc,char**argv){
 if(argc!=3)return 2;std::ifstream f(argv[1],std::ios::binary);u64 nv,nd,m,N,D,Q,b;u64* hh[]={&nv,&nd,&m,&N,&D,&Q,&b};for(auto p:hh)f.read((char*)p,8);
 if(N!=64||nd>=(u64(1)<<b)||D>64||Q>=63)return 3;
 std::vector<uint32_t>eu(m),ev(m);std::vector<uint8_t>cost(m),side(nv),dist(nd*nd);std::vector<u64>q(m),W(nv),U(nv*N);std::vector<uint16_t>dl(nv),dr(nv);
 rd(f,eu);rd(f,ev);rd(f,cost);rd(f,q);rd(f,dl);rd(f,dr);rd(f,side);rd(f,dist);rd(f,W);rd(f,U);
 std::vector<std::vector<std::pair<uint32_t,u64>>> adj(nd);
 for(u64 e=0;e<m;e++){u128 wn=u128(q[e])<<cost[e];if(wn>UINT64_MAX)return 4;auto add=[&](u64 x,u64 y){if(x<nd&&side[y]!=1)adj[x].push_back({uint32_t(y),u64(wn)});};add(eu[e],ev[e]);add(ev[e],eu[e]);}
 std::vector<u128>JW(nd),J(nd*N);int maxprod=0,maxj=0,maxacc=0;
 for(u64 x=0;x<nd;x++)for(auto [y,w]:adj[x])JW[x]+=u128(w)*W[y];
 for(u64 v=0;v<nv;v++){
  u128 a=0;if(v<nd)for(u64 x=0;x<nd;x++)a+=upshift(JW[x],64+dist[v*nd+x]-int(b));
  u128 rhs=upshift(a,b)+1;if(W[v]<rhs){std::cerr<<"Scalar W failure "<<v<<"\n";return 5;}
 }
 // Explicit edge-cost adjacency for residue shifts.
 struct E{uint32_t y;u64 w;uint8_t c;};std::vector<std::vector<E>> aa(nd);
 for(u64 e=0;e<m;e++){u64 wn=u64(u128(q[e])<<cost[e]);auto add=[&](u64 x,u64 y){if(x<nd&&side[y]!=1)aa[x].push_back({uint32_t(y),wn,cost[e]});};add(eu[e],ev[e]);add(ev[e],eu[e]);}
 auto cj=[&](){std::fill(J.begin(),J.end(),0);for(u64 x=0;x<nd;x++)for(u64 r=0;r<N;r++){
  u128 a=0;for(auto e:aa[x]){u128 z=u128(e.w)*U[u64(e.y)*N+((r+e.c)&63)];if(~u128(0)-a<z)std::abort();a+=z;maxprod=std::max(maxprod,bits(z));}J[x*N+r]=a;maxj=std::max(maxj,bits(a));
 }};
 auto rhs=[&](u64 v,u64 r){
  u128 a=0;if(v<nd)for(u64 x=0;x<nd;x++){u64 d=dist[v*nd+x];u128 z=upshift(J[x*N+((r+N-(d%N))&63)],64+int(d)-int(b));if(~u128(0)-a<z)std::abort();a+=z;}
  maxacc=std::max(maxacc,bits(a));u128 ans=upshift(a,b);
  if(side[v]!=1){u64 rend=(r+N-(dr[v]%N))&63;int ex=int(Q)-int(dr[v])-int(rend);ans+=(ex>=0?u128(1)<<ex:1);}
  if(ans>UINT64_MAX)std::abort();return u64(ans);
 };
 cj();u64 defect=0;
 for(u64 v=0;v<nv;v++)for(u64 r=0;r<N;r++){u64 z=rhs(v,r);if(z>U[v*N+r])defect=std::max(defect,z-U[v*N+r]);}
 u64 repair=defect+4;
 for(u64 v=0;v<nv;v++)for(u64 r=0;r<N;r++){u128 z=u128(U[v*N+r])+u128(repair)*W[v];if(z>UINT64_MAX)std::abort();U[v*N+r]=u64(z);}
 cj();
 for(u64 v=0;v<nv;v++)for(u64 r=0;r<N;r++)if(rhs(v,r)>U[v*N+r]){std::cerr<<"H failure "<<v<<","<<r<<"\n";return 6;}
 std::string pre=argv[2];std::ofstream ou(pre+"_U.bin",std::ios::binary);ou.write((char*)U.data(),U.size()*8);ou.close();
 std::vector<u64>lo(J.size()),hi(J.size());for(u64 i=0;i<J.size();i++){lo[i]=u64(J[i]);hi[i]=u64(J[i]>>64);}std::ofstream ol(pre+"_Jlo.bin",std::ios::binary);ol.write((char*)lo.data(),lo.size()*8);std::ofstream oh(pre+"_Jhi.bin",std::ios::binary);oh.write((char*)hi.data(),hi.size()*8);
 std::cout<<"{\"integer_certificate_pass\":true,\"vertices\":"<<nv<<",\"internal_vertices\":"<<nd<<",\"folded_states\":"<<nv*N<<",\"kernel_pair_checks_per_pass\":"<<nd*nd*N<<",\"maximum_scalar_W\":"<<*std::max_element(W.begin(),W.end())<<",\"maximum_initial_grid_defect\":"<<defect<<",\"repair_multiplier\":"<<repair<<",\"intermediate_fraction_bits\":"<<b<<",\"maximum_product_bits\":"<<maxprod<<",\"maximum_J_bits\":"<<maxj<<",\"maximum_rounded_accumulator_bits\":"<<maxacc<<"}\n";
}
