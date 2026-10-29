#include <gmpxx.h>
#include <vector>
#include <iostream>
#include <fstream>
#include <chrono>
using Z=mpz_class;struct P{std::vector<Z>a;Z d=1;};std::vector<Z> U;int n;
void trim(P&p){while(!p.a.empty()&&p.a.back()==0)p.a.pop_back();if(p.a.empty())p.d=1;}
void norm(P&p){trim(p);Z g=p.d;for(auto&x:p.a){mpz_gcd(g.get_mpz_t(),g.get_mpz_t(),x.get_mpz_t());if(g==1)break;}if(g!=1){p.d/=g;for(auto&x:p.a)x/=g;}if(p.d<0){p.d=-p.d;for(auto&x:p.a)x=-x;}}
P con(Z x){return {{x},1};}
P reduce(P p){trim(p);while(p.a.size()>size_t(n)){size_t k=p.a.size()-1,shift=k-n;Z lead=p.a.back();Z g;mpz_gcd(g.get_mpz_t(),lead.get_mpz_t(),U.back().get_mpz_t());Z fac=U.back()/g,c=lead/g;for(size_t i=0;i<k;i++)p.a[i]*=fac;for(int j=0;j<n;j++)p.a[shift+j]-=c*U[j];p.d*=fac;p.a.pop_back();trim(p);}norm(p);return p;}
P mul(const P&a,const P&b){if(a.a.empty()||b.a.empty())return {};P c;c.d=a.d*b.d;c.a.resize(a.a.size()+b.a.size()-1);for(size_t i=0;i<a.a.size();i++)for(size_t j=0;j<b.a.size();j++)c.a[i+j]+=a.a[i]*b.a[j];return reduce(c);}
P add(const P&a,const P&b){Z g;mpz_gcd(g.get_mpz_t(),a.d.get_mpz_t(),b.d.get_mpz_t());Z aa=b.d/g,bb=a.d/g;P c;c.d=a.d*aa;c.a.resize(std::max(a.a.size(),b.a.size()));for(size_t i=0;i<a.a.size();i++)c.a[i]+=a.a[i]*aa;for(size_t i=0;i<b.a.size();i++)c.a[i]+=b.a[i]*bb;norm(c);return c;}
P scale(P a,Z c,Z d=1){for(auto&v:a.a)v*=c;a.d*=d;norm(a);return a;}
int main(int argc,char**argv){auto st=std::chrono::steady_clock::now();std::ifstream in(argv[1]);in>>n;U.resize(n+1);for(auto&x:U)in>>x;P x,y,z={{0,1},1};x.a.resize(n);y.a.resize(n);in>>x.d;for(auto&a:x.a)in>>a;in>>y.d;for(auto&a:y.a)in>>a;norm(x);norm(y);int nt;in>>nt;struct T{int e[3];Z a,b;};std::vector<T>ts(nt);for(auto&t:ts)in>>t.e[0]>>t.e[1]>>t.e[2]>>t.a>>t.b;if(!in)throw std::runtime_error("input");
P den=scale(add(add(add(con(1),mul(x,x)),mul(y,y)),mul(z,z)),4);std::cerr<<"norm built\n";std::vector<std::vector<P>> powers;for(auto&v:std::vector<P>{x,y,z})powers.push_back({con(1),v,mul(v,v),mul(mul(v,v),v)});P num;for(auto&t:ts){P v=scale(con(1),t.a,t.b);for(int j=0;j<3;j++)v=mul(v,powers[j][t.e[j]]);num=add(num,v);}std::cerr<<"numerator built; denominator bits "<<mpz_sizeinbase(num.d.get_mpz_t(),2)<<"\n";
std::ifstream pin(argv[2]);int degree;pin>>degree;std::vector<Z>cs(degree+1);for(auto&c:cs)pin>>c;if(!pin||degree!=n)throw std::runtime_error("candidate");P val=con(cs[degree]),dp=con(1);for(int i=degree-1;i>=0;i--){dp=mul(dp,den);val=add(mul(val,num),scale(dp,cs[i]));std::cerr<<"horner "<<i<<" degree "<<int(val.a.size())-1<<" denom bits "<<mpz_sizeinbase(val.d.get_mpz_t(),2)<<"\n";}
if(!val.a.empty())throw std::runtime_error("EXACT HOMOGENEOUS IDENTITY FAILED");double secs=std::chrono::duration<double>(std::chrono::steady_clock::now()-st).count();std::ofstream out(argv[3]);out<<"{\"exact_homogeneous_p_num_den_mod_U_zero\":true,\"degree\":"<<degree<<",\"norm_invertibility_from_separate_modular_witness\":true,\"seconds\":"<<secs<<"}\n";std::cout<<"EXACT VERIFIED "<<secs<<"\n";}
