// Exact integer tensor contractions. Uses GMP; does not enumerate spin configurations.
// Input: n k eps_num eps_den; then n cores as dl dr p followed by dl*2*dr signed integers.
// Outputs integer contractions with shared dyadic scale handled by Python.
#include <gmpxx.h>
#include <vector>
#include <array>
#include <iostream>
#include <fstream>
#include <stdexcept>
using Z=mpz_class;
using Mat=std::vector<Z>;
struct Core {int l,r,p; std::vector<long> a; long at(int i,int s,int j)const{return a[(i*2+s)*r+j];}};
using Op=std::array<Z,4>;
using MPO=std::vector<std::vector<Op>>;
void addmul_si(Z& dst,const Z& x,long a){if(a>=0)mpz_addmul_ui(dst.get_mpz_t(),x.get_mpz_t(),(unsigned long)a);else mpz_submul_ui(dst.get_mpz_t(),x.get_mpz_t(),(unsigned long)(-a));}
Mat sand(const Mat&E,const Core&A,int s,int t){
    Mat tmp(A.l*A.r), out(A.r*A.r);
    for(int i=0;i<A.l;i++)for(int j=0;j<A.r;j++)for(int k=0;k<A.l;k++) addmul_si(tmp[i*A.r+j],E[i*A.l+k],A.at(k,t,j));
    for(int i=0;i<A.r;i++)for(int j=0;j<A.r;j++)for(int k=0;k<A.l;k++) addmul_si(out[i*A.r+j],tmp[k*A.r+j],A.at(k,s,i));
    return out;
}
bool nz(const Mat&m){for(auto &x:m)if(x!=0)return true;return false;}
void addscaled(Mat&out,const Mat&x,const Z&c){if(c==0)return; if(c==1){for(size_t i=0;i<x.size();i++)out[i]+=x[i];} else if(c==-1){for(size_t i=0;i<x.size();i++)out[i]-=x[i];}else for(size_t i=0;i<x.size();i++)mpz_addmul(out[i].get_mpz_t(),x[i].get_mpz_t(),c.get_mpz_t());}
MPO local(int i,int n,long k,long en,long ed){
    Z den=Z(k)*k+1,D=Z(ed)*den*den;
    MPO W(3,std::vector<Op>(3));
    W[0][0]={1,0,0,1}; W[1][0]={0,0,0,1}; W[2][2]={1,0,0,1};
    Z c=Z(ed-en)*den;
    W[2][1]={c,-c*k,-c*k,c*k*k};
    W[2][0]={0,0,0,i==0?D:Z(en)*den*den};
    if(i==0){Z bg=Z(en)*den;W[2][0][0]+=bg;W[2][0][3]+=bg;}
    if(i==n-1){Z s=ed-en; W[2][0][0]+=s;W[2][0][1]-=s*k;W[2][0][2]-=s*k;W[2][0][3]+=s*k*k;}
    return W;
}
// <v, H_D v>, and <v,H_D^2 v>. Both numerator integers.
Z quadratic(const std::vector<Core>&A,long k,long en,long ed,int power){
    int ch=power==1?3:9;
    std::vector<Mat>E(ch,Mat(1));E[ch-1][0]=1;
    for(size_t i=0;i<A.size();i++){
        const auto&a=A[i];auto W=local(i,A.size(),k,en,ed);
        std::vector<Mat>N(ch,Mat(a.r*a.r));
        for(int l=0;l<ch;l++)if(nz(E[l]))for(int s=0;s<2;s++)for(int t=0;t<2;t++){
            std::vector<Z>coeff(ch);
            if(power==1) for(int r=0;r<3;r++)coeff[r]=W[l][r][s*2+t];
            else for(int r=0;r<9;r++)for(int z=0;z<2;z++)coeff[r]+=W[l/3][r/3][z*2+s]*W[l%3][r%3][z*2+t];
            bool any=false;for(auto &c:coeff)if(c!=0)any=true;if(!any)continue;
            Mat T=sand(E[l],a,s,t);
            for(int r=0;r<ch;r++)addscaled(N[r],T,coeff[r]);
        }
        E.swap(N);
    }
    return E[0][0];
}
Z source(const std::vector<Core>&A,long k,long en,long ed,bool op){
    int ch=op?3:1;std::vector<Mat>E(ch,Mat(1));E[ch-1][0]=1;
    for(size_t i=0;i<A.size();i++){
        const auto&a=A[i];auto W=local(i,A.size(),k,en,ed);
        std::vector<Mat>N(ch,Mat(a.r));
        for(int l=0;l<ch;l++)for(int t=0;t<2;t++){
            Mat v(a.r);for(int j=0;j<a.r;j++)for(int h=0;h<a.l;h++)addmul_si(v[j],E[l][h],a.at(h,t,j));
            for(int r=0;r<ch;r++){Z c=op?W[l][r][t]:(t==0?1:0);addscaled(N[r],v,c);}
        }E.swap(N);
    }return E[0][0];
}
// Weights up to maxdegree for H_D v in the independent-site excitation basis.
std::vector<Z> sectors(const std::vector<Core>&A,long k,long en,long ed,int maxdegree){
    int ch=9;std::vector<std::vector<Mat>>E(maxdegree+1,std::vector<Mat>(ch,Mat(1)));E[0][8][0]=1;
    for(size_t i=0;i<A.size();i++){
        auto&a=A[i];auto W=local(i,A.size(),k,en,ed);
        std::vector<std::vector<Mat>>N(maxdegree+1,std::vector<Mat>(ch,Mat(a.r*a.r)));
        for(int h=0;h<=std::min((int)i,maxdegree);h++)for(int l=0;l<ch;l++)if(nz(E[h][l]))for(int s=0;s<2;s++)for(int t=0;t<2;t++){
            std::array<std::vector<Z>,2>cc={std::vector<Z>(9),std::vector<Z>(9)};
            bool any=false;
            for(int z=0;z<2;z++)if(h+z<=maxdegree)for(int r=0;r<9;r++){
                cc[z][r]=W[l/3][r/3][z*2+s]*W[l%3][r%3][z*2+t];if(cc[z][r]!=0)any=true;
            }
            if(!any)continue;Mat T=sand(E[h][l],a,s,t);
            for(int z=0;z<2;z++)if(h+z<=maxdegree)for(int r=0;r<9;r++)addscaled(N[h+z][r],T,cc[z][r]);
        }E.swap(N);
    }
    std::vector<Z>out;for(auto&e:E)out.push_back(e[0][0]);return out;
}
int main(int argc,char**argv){
    if(argc<2){std::cerr<<"input file required\n";return 1;}
    std::ifstream f(argv[1]);int n;long k,en,ed;f>>n>>k>>en>>ed;if(!f||n<2||ed<=0||en<=0||en>ed){std::cerr<<"invalid model\n";return 2;}
    std::vector<Core>A(n);long ptotal=0;
    for(auto&a:A){f>>a.l>>a.r>>a.p;a.a.resize(a.l*2*a.r);for(auto&x:a.a)f>>x;ptotal+=a.p;}
    if(!f){std::cerr<<"invalid core data\n";return 3;}
    Z den=Z(k)*k+1,D=Z(ed)*den*den;
    std::cout<<"p "<<ptotal<<"\nD "<<D<<"\n";
    std::cout<<"source "<<source(A,k,en,ed,false)<<"\n"<<std::flush;
    std::cout<<"Hsource "<<source(A,k,en,ed,true)<<"\n"<<std::flush;
    std::cout<<"energy "<<quadratic(A,k,en,ed,1)<<"\n"<<std::flush;
    std::cout<<"Hnorm "<<quadratic(A,k,en,ed,2)<<"\n"<<std::flush;
    int degree=argc>2?std::stoi(argv[2]):-1;
    if(degree>=0){auto w=sectors(A,k,en,ed,degree);for(int i=0;i<=degree;i++)std::cout<<"sector"<<i<<" "<<w[i]<<"\n";}
    return 0;
}
