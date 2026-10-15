#include <algorithm>
#include <limits>
#include <cfloat>
static_assert(FLT_EVAL_METHOD == 0, "Binary64 evaluation required");
#include <cfenv>
#ifdef __FAST_MATH__
#error Fast math is not supported
#endif
static_assert(std::numeric_limits<double>::is_iec559 && std::numeric_limits<double>::digits==53 && std::numeric_limits<double>::radix==2);
#include <array>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include "coefficients.h"
// Compile without fast math and without FMA contraction.
static double plog(double x){int e;double m=std::frexp(x,&e)*2;--e;double z=(m-1)/(m+1),y=z*z,s=LC[19];for(int j=18;j>=0;--j)s=LC[j]+y*s;return z*s+e*0x1.62e42fefa39efp-1;}
static double pexp(double x){if(x < -64)return 0;double v=x/128,s=EC[32];for(int j=31;j>=0;--j)s=EC[j]+v*s;for(int j=0;j<7;++j)s=s*s;return s;}
int main(int argc,char**argv){if(std::fegetround()!=FE_TONEAREST)return 3;std::ifstream f(argv[1]);std::string st;auto rd=[&](){f>>st;return std::strtod(st.c_str(),nullptr);};double a=rd(),p=rd(),base=rd();std::array<double,400> rates;uint64_t cdfs[400][128];for(int i=0;i<400;++i){rates[i]=rd();for(auto &c:cdfs[i])f>>c;}
 uint64_t N=std::stoull(argv[2]);std::mt19937_64 rng(std::stoull(argv[3]));std::array<double,400> t,sorted;
 for(uint64_t begin=0;begin<N;begin+=5000){uint64_t sum=0,ss=0,events=0,badcount=0;for(uint64_t k=begin;k<std::min(N,begin+5000);++k){bool bad=false;for(int i=0;i<400;++i){uint64_t r=rng();int m=std::upper_bound(cdfs[i],cdfs[i]+128,r)-cdfs[i];uint64_t hi=rng();uint32_t low=uint32_t(rng());if(hi<(uint64_t(1)<<24))bad=true;double u=std::ldexp(double(hi),-64)+std::ldexp(double(low)+0.5,-96);if(!bad)t[i]=-plog(u)/(rates[i]+a*m);}
 uint64_t v=0;if(bad){++badcount;}else{sorted=t;std::sort(sorted.begin(),sorted.end());double tau=0;for(int j=0;j<400;++j)tau+=(799-2*j)*sorted[j];tau/=160000;if(tau<=0.2){++events;double ex=base;for(auto ti:t)ex+=2*plog(1-p*pexp(-a*ti));double w=std::min(1.0,std::max(0.0,pexp(std::min(0.0,ex))));v=uint64_t(std::ldexp(w,24));}}sum+=v;ss+=v*v;}std::cout<<sum<<' '<<ss<<' '<<events<<' '<<badcount<<'\n';}
}
