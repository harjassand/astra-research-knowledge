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
struct Core {int l,r,p,d; std::vector<long> a; long at(int i,int s,int j)const{return a[(i*d+s)*r+j];}};
using Op=std::vector<Z>;
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
int physdim; Z gramden,opden;std::vector<Z>grams;std::vector<MPO>allW;
MPO local(int i,int n,long k,long en,long ed){return allW[i];}
// <v, H_D v>, and <v,H_D^2 v>. Both numerator integers.
Z quadratic(const std::vector<Core>&A,long k,long en,long ed,int power,int cap=-1){
    int ch=power==1?3:9;
    std::vector<Mat>E(ch,Mat(1));E[ch-1][0]=1;
    for(size_t i=0;i<A.size();i++){
        const auto&a=A[i];auto W=local(i,A.size(),k,en,ed);
        std::vector<Mat>N(ch,Mat(a.r*a.r));
        for(int l=0;l<ch;l++)if(nz(E[l]))for(int s=0;s<physdim;s++)for(int t=0;t<physdim;t++){
            std::vector<Z>coeff(ch);
            if(power==1) for(int r=0;r<3;r++)coeff[r]=grams[s]*W[l][r][s*physdim+t];
            else for(int r=0;r<9;r++)for(int z=0;z<(cap>=0?cap+1:(power==3?2:physdim));z++)coeff[r]+=grams[z]*W[l/3][r/3][z*physdim+s]*W[l%3][r%3][z*physdim+t];
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
        for(int l=0;l<ch;l++)for(int t=0;t<physdim;t++){
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
        for(int h=0;h<=std::min((int)i,maxdegree);h++)for(int l=0;l<ch;l++)if(nz(E[h][l]))for(int s=0;s<physdim;s++)for(int t=0;t<physdim;t++){
            std::array<std::vector<Z>,2>cc={std::vector<Z>(9),std::vector<Z>(9)};
            bool any=false;
            for(int z=0;z<2;z++)if(h+z<=maxdegree)for(int r=0;r<9;r++){
                cc[z][r]=grams[z]*W[l/3][r/3][z*physdim+s]*W[l%3][r%3][z*physdim+t];if(cc[z][r]!=0)any=true;
            }
            if(!any)continue;Mat T=sand(E[h][l],a,s,t);
            for(int z=0;z<2;z++)if(h+z<=maxdegree)for(int r=0;r<9;r++)addscaled(N[h+z][r],T,cc[z][r]);
        }E.swap(N);
    }
    std::vector<Z>out;for(auto&e:E)out.push_back(e[0][0]);return out;
}
int main(int argc,char**argv){
    if(argc<2){std::cerr<<"input file required\n";return 1;}
    std::ifstream f(argv[1]);int n;f>>n>>physdim>>opden>>gramden;
    if(!f||n<2||physdim<2){std::cerr<<"invalid model\n";return 2;}
    grams.resize(physdim);for(auto&x:grams)f>>x;
    allW.resize(n);
    for(auto&w:allW){w=MPO(3,std::vector<Op>(3,Op(physdim*physdim)));for(auto&row:w)for(auto&op:row)for(auto&x:op)f>>x;}
    std::vector<Core>A(n);long ptotal=0;
    for(auto&a:A){a.d=physdim;f>>a.l>>a.r>>a.p;a.a.resize(a.l*physdim*a.r);for(auto&x:a.a)f>>x;ptotal+=a.p;}
    if(!f){std::cerr<<"invalid core data\n";return 3;}
    std::cout<<"p "<<ptotal<<"\nD "<<opden<<"\nG "<<gramden<<"\n";
    std::cout<<"source "<<source(A,0,0,0,false)<<"\n"<<std::flush;
    std::cout<<"Hsource "<<source(A,0,0,0,true)<<"\n"<<std::flush;
    std::cout<<"energy "<<quadratic(A,0,0,0,1)<<"\n"<<std::flush;
    std::cout<<"Hnorm "<<quadratic(A,0,0,0,2)<<"\n"<<std::flush;
    std::cout<<"Hnorm_low "<<quadratic(A,0,0,0,3)<<"\n"<<std::flush;
    for(int cap=2;cap<physdim-1;cap++)std::cout<<"Hnorm_cap"<<cap<<" "<<quadratic(A,0,0,0,2,cap)<<"\n"<<std::flush;
    int degree=argc>2?std::stoi(argv[2]):-1;
    if(degree>=0){auto w=sectors(A,0,0,0,degree);for(int i=0;i<=degree;i++)std::cout<<"sector"<<i<<" "<<w[i]<<"\n";}
    return 0;
}
