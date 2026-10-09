#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <unordered_map>
#include <vector>
using namespace std;
struct Hash {
  size_t operator()(const array<long long,5>& a) const noexcept {
    uint64_t h=0x9e3779b97f4a7c15ULL;
    for (auto x:a) { uint64_t z=(uint64_t)x+0x9e3779b97f4a7c15ULL; z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL; z=(z^(z>>27))*0x94d049bb133111ebULL; z^=z>>31; h^=z+(h<<6)+(h>>2); }
    return (size_t)h;
  }
};
long long choose(int n,int r) { static int c[5][5]={{1}}; if(n<0||r<0||r>n)return 0; long long z=1; for(int i=1;i<=r;i++) z=z*(n-r+i)/i; return z; }
long long powi(long long x,int r){long long z=1;while(r--)z*=x;return z;}
int main(int argc,char**argv){
  if(argc!=2){cerr<<"usage: search n\n";return 2;}
  int n=atoi(argv[1]), k=2, m=n-k; if(n<3||n>60){cerr<<"n must be 3..60\n";return 2;}
  for(uint64_t y=0;y<(1ULL<<m);y++){
    long long pref[5][61]{};
    for(int j=0;j<m;j++) for(int r=0;r<=4;r++) pref[r][j+1]=pref[r][j]+(((y>>j)&1)?powi(j+1,r):0);
    unordered_map<array<long long,5>,uint64_t,Hash> seen; seen.reserve((m+1)*(m+2)*2);
    for(int i=0;i<=m;i++) for(int j=i;j<=m;j++) for(int b1=0;b1<2;b1++) for(int b2=0;b2<2;b2++){
      array<long long,5> sig{};
      for(int r=0;r<=4;r++){
        long long v=pref[r][i];
        for(int a=0;a<=r;a++) v+=choose(r,a)*(pref[a][j]-pref[a][i]);
        for(int a=0;a<=r;a++) v+=choose(r,a)*powi(2,r-a)*(pref[a][m]-pref[a][j]);
        v+=b1*powi(i+1,r)+b2*powi(j+2,r);
        sig[r]=v;
      }
      uint64_t x=0;int pos=0;
      for(int cut=0;cut<=m;cut++){
        if(cut==i){if(b1)x|=1ULL<<pos;pos++;}
        if(cut==j){if(b2)x|=1ULL<<pos;pos++;}
        if(cut<m){if((y>>cut)&1)x|=1ULL<<pos;pos++;}
      }
      auto it=seen.find(sig);
      if(it!=seen.end()&&it->second!=x){
        auto print=[&](uint64_t z,int len){for(int t=len-1;t>=0;t--)cout<<((z>>t)&1);cout<<"\n";};
        cout<<"collision n="<<n<<" k=2 moments=0..4\nx=";print(x,n);cout<<"x'=";print(it->second,n);cout<<"y=";print(y,m);cout<<"moments=";for(auto q:sig)cout<<q<<",";cout<<"\n";return 0;
      }
      seen.emplace(sig,x);
    }
  }
  cout<<"no collision n="<<n<<" k=2 moments=0..4\n";
}
