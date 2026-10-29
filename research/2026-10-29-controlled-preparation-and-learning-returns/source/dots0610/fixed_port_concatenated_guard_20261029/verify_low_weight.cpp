#include <iostream>
#include <vector>
#include <cstdint>
using U=__uint128_t;
int n,d; std::vector<std::vector<U>> syn; unsigned long long checked=0; bool failed=false;
void walk(int start,int left,U s){
 if(!left){++checked;if(s==0)failed=true;return;}
 for(int j=start;j<=n-left && !failed;++j)for(int p=0;p<3 && !failed;++p)walk(j+1,left-1,s^syn[j][p]);
}
int main(){std::cin>>n>>d;syn.assign(n,std::vector<U>(3));for(int j=0;j<n;++j)for(int p=0;p<3;++p){unsigned long long lo,hi;std::cin>>lo>>hi;syn[j][p]=U(lo)|(U(hi)<<64);}for(int w=1;w<d && !failed;++w)walk(0,w,0);std::cout<<checked<<" "<<failed<<"\n";return failed?2:0;}
