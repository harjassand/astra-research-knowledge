#include <gmpxx.h>
#include <vector>
#include <iostream>
#include <fstream>
#include <chrono>
using Poly=std::vector<mpq_class>;
void trim(Poly &a){while(!a.empty() && a.back()==0)a.pop_back();}
Poly add(Poly a,const Poly&b,int sign=1){if(a.size()<b.size())a.resize(b.size());for(size_t i=0;i<b.size();i++)a[i]+=sign*b[i];trim(a);return a;}
Poly mulraw(const Poly&a,const Poly&b){if(a.empty()||b.empty())return {};Poly c(a.size()+b.size()-1);for(size_t i=0;i<a.size();i++)for(size_t j=0;j<b.size();j++)c[i+j]+=a[i]*b[j];trim(c);return c;}
std::pair<Poly,Poly> divide(Poly a,const Poly&b){Poly q(a.size()>=b.size()?a.size()-b.size()+1:0);while(a.size()>=b.size()&&!a.empty()){size_t k=a.size()-b.size();mpq_class c=a.back()/b.back();q[k]=c;for(size_t j=0;j<b.size();j++)a[k+j]-=c*b[j];trim(a);}trim(q);return {q,a};}
Poly modmul(const Poly&a,const Poly&b,const Poly&u){return divide(mulraw(a,b),u).second;}
Poly invert(Poly a,const Poly&u){Poly r0=u,r1=a,t0={},t1={1};while(!r1.empty()){auto qr=divide(r0,r1);r0=r1;r1=qr.second;auto t=add(t0,mulraw(qr.first,t1),-1);t0=t1;t1=t;}if(r0.size()!=1)throw std::runtime_error("norm not invertible");for(auto &x:t0)x/=r0[0];return divide(t0,u).second;}
mpq_class rat(mpz_class a,mpz_class b){mpq_class q(a,b);q.canonicalize();return q;}
int main(int argc,char**argv){auto st=std::chrono::steady_clock::now();std::ifstream in(argv[1]);int n;in>>n;Poly u(n+1),x(n),y(n);mpz_class a,b;for(auto &q:u){in>>a;q=a;}in>>b;for(auto&q:x){in>>a;q=rat(a,b);}in>>b;for(auto&q:y){in>>a;q=rat(a,b);}Poly z={0,1};int nt;in>>nt;struct Term{int e[3];mpq_class c;};std::vector<Term> terms(nt);for(auto&t:terms){in>>t.e[0]>>t.e[1]>>t.e[2]>>a>>b;t.c=rat(a,b);}if(!in)throw std::runtime_error("input parse");trim(x);trim(y);std::cerr<<"parsed\n";
Poly norm=add(add(add({1},modmul(x,x,u)),modmul(y,y,u)),{0,0,1});std::cerr<<"norm\n";std::cerr<<"using independently verified modular norm-invertibility witness\n";
std::vector<std::vector<Poly>> powers;for(auto &v:std::vector<Poly>{x,y,z})powers.push_back({{1},v,modmul(v,v,u),modmul(modmul(v,v,u),v,u)});Poly num;
for(auto&t:terms){Poly v={t.c};for(int j=0;j<3;j++)v=modmul(v,powers[j][t.e[j]],u);num=add(num,v);}Poly den=norm;for(auto&q:den)q*=4;std::cerr<<"exact numerator and denominator\n";
std::ifstream pin(argv[2]);int degree;pin>>degree;std::vector<mpz_class> cs(degree+1);for(auto&c:cs)pin>>c;if(!pin||degree!=n)throw std::runtime_error("polynomial parse");Poly val={mpq_class(cs[degree])},dp={1};
for(int i=degree-1;i>=0;i--){dp=modmul(dp,den,u);val=modmul(val,num,u);Poly term=dp;for(auto&q:term)q*=cs[i];val=add(val,term);std::cerr<<"horner "<<i<<" degree "<<int(val.size())-1<<"\n";}
if(!val.empty())throw std::runtime_error("EXACT VERIFICATION FAILED");double secs=std::chrono::duration<double>(std::chrono::steady_clock::now()-st).count();std::ofstream out(argv[3]);out<<"{\"exact_p_lambda_mod_U_zero\":true,\"degree\":"<<degree<<",\"norm_invertibility_via_modular_witness\":true,\"seconds\":"<<secs<<"}\n";std::cout<<"EXACT VERIFIED "<<secs<<"\n";
}
