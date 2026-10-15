// Independent integer-only enclosure. Compile: g++ -O3 -std=c++17.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
#include <string>
using namespace std;using U=unsigned __int128;using S=__int128;using W=uint64_t;
const W M=W(1)<<60, D=1000000;
struct I {W l,h;};
W down(U a,W b){return a/b;} W up(U a,W b){return (a+b-1)/b;}
I mul(I a,I b){return {W(U(a.l)*b.l/M),up(U(a.h)*b.h,M)};}
// exp(-x) for exact x=X/M. Taylor on [0,1/2], then squaring.
I ex(U X){if(U(X)>=U(64)*M)return {0,1};int k=0;U den=1;while(U(X)>U(M)*den/2){den*=2;k++;}
 I y={W(X/den),W((X+den-1)/den)};
 // Interval recurrence bounds each term; degree 24 alternating remainder is < 1/M.
 I t={M,M};S lo=M,hi=M;
 for(int j=1;j<=24;j++){t={W(U(t.l)*y.l/(U(M)*j)),W((U(t.h)*y.h+U(M)*j-1)/(U(M)*j))};if(j%2){lo-=t.h;hi-=t.l;}else{lo+=t.l;hi+=t.h;}}
 I r={W(max(S(0),lo-1)),W(min(S(M),hi+1))};for(int j=0;j<k;j++)r=mul(r,r);return r;
}
// Input exponent interval can exceed uint64; cutoff is proved by e>2.
I exwide(U l,U h){auto at=[](U x)->I{if(x>=U(64)*M)return {0,1};return ex(x);};return {at(h).l,at(l).h};}
string str(U x){if(!x)return "0";string s;while(x){s+=char('0'+x%10);x/=10;}reverse(s.begin(),s.end());return s;}
U readU(){string s;cin>>s;U x=0;for(char c:s)x=x*10+c-'0';return x;}
int main(){int n;W limit;cin>>n>>limit; assert(n>=1 && n<=400 && limit>=1 && limit<=100000000000000000ULL); vector<I> lam(n),psi(n+1);vector<int>js(n+1);vector<vector<int>> buckets(n+1);vector<vector<bool>>ok(n,vector<bool>(n+1));
 for(int j=0;j<n;j++){U l=readU(),h=readU();lam[j]=exwide(l,h);}for(int m=1;m<=n;m++){U l=readU(),h=readU();psi[m]=exwide(l,h);}for(int m=0;m<=n;m++){cin>>js[m];if(js[m]>=m)buckets[js[m]].push_back(m);}for(int j=0;j<n;j++)for(int m=0;m<=n;m++){int a;cin>>a;ok[j][m]=a;}
 auto kernel=[&](const vector<W>&p,bool upper)->W{vector<W>pref(n+1),a(n+1),h(n+1,M),out(n+1);pref[0]=M;for(int m:buckets[0])a[m]=pref[m];for(int j=1;j<=n;j++){W v=p[j-1];for(int m=j;m>=0;m--)pref[m]=W((U(M-v)*pref[m]+(m?U(v)*pref[m-1]:0))/M);for(int m:buckets[j])a[m]=pref[m];}for(int m:buckets[n])out[m]=W(U(a[m])*h[m]/M);for(int j=n-1;j>=0;j--){W v=p[j];for(int m=0;m<=n;m++)h[m]=W((U(M-v)*(ok[j][m]?h[m]:0)+(m<n?U(v)*(ok[j][m+1]?h[m+1]:0):0))/M);for(int m:buckets[j])out[m]=W(U(a[m])*h[m]/M);}U ans=0;for(int m=1;m<=n;m++)ans+=U(out[m])*(upper?psi[m].h:psi[m].l)/M;if(upper)ans+=W(n)*(n+3);return min(U(M),ans);};
 auto value=[&](W ticks)->I{vector<W>pl(n),ph(n);for(int j=0;j<n;j++){I p=exwide(U(lam[j].l)*ticks/D,(U(lam[j].h)*ticks+D-1)/D);pl[j]=p.l;ph[j]=p.h;}return {kernel(pl,false),kernel(ph,true)};};
 W prev=0,t=1;I last=value(0);U lo=0,hi=0;int count=1;while(true){I now=value(t);lo+=U(t-prev)*now.l;hi+=U(t-prev)*last.h;count++;if(t==limit)break;prev=t;last=now;t=min(limit,W((U(t)*1005+999)/1000));}
 U tail=0;for(int j=0;j<n;j++){if(lam[j].l==0){cerr<<"Zero lower rate";return 1;}I p=exwide(U(lam[j].l)*limit/D,U(lam[j].l)*limit/D);assert(U(p.h)<=U(-1)/(U(M)*D));tail+=(U(p.h)*M*D+lam[j].l-1)/lam[j].l;}hi+=tail;
 cout<<"{\"lower_numerator\":\""<<str(lo)<<"\",\"upper_numerator\":\""<<str(hi)<<"\",\"denominator\":\""<<str(U(M)*D)<<"\",\"tail_numerator\":\""<<str(tail)<<"\",\"evaluations\":"<<count<<"}"<<endl;return 0;
}
