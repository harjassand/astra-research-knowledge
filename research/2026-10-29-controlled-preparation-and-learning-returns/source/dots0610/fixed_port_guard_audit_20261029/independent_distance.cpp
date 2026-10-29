#include <iostream>
#include <vector>
#include <cstdint>
int main(){int n,d;std::cin>>n>>d;using U=__uint128_t;std::vector<U> v(3*n);for(auto &x:v){uint64_t l,h;std::cin>>l>>h;x=U(l)|(U(h)<<64);}uint64_t count=0,zeros=0;for(int w=1;w<d;w++){std::vector<int> p(w);for(int i=0;i<w;i++)p[i]=i;int power=1;for(int i=0;i<w;i++)power*=3;while(true){for(int labels=0;labels<power;labels++){int z=labels;U s=0;for(int i=0;i<w;i++){s^=v[3*p[i]+z%3];z/=3;}count++;zeros+=s==0;}int j=w-1;while(j>=0&&p[j]==n-w+j)j--;if(j<0)break;p[j]++;for(int i=j+1;i<w;i++)p[i]=p[i-1]+1;}}std::cout<<count<<" "<<zeros<<"\n";}
