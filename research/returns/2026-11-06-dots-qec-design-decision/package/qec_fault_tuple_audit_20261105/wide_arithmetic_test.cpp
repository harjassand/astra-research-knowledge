#define main certificate_main
#include "check_rows.cpp"
#undef main
int main(){int op;while(std::cin>>op){uint256_t a,b,z;unsigned k;
for(auto &x:a.limb)std::cin>>x;for(auto &x:b.limb)std::cin>>x;std::cin>>k;
try{if(op==0)z=a+b;else if(op==1)z=a<<k;else z=uint256_t::product(a.limb[0],b.limb[0]);
for(auto x:z.limb)std::cout<<x<<" ";std::cout<<bits(z)<<" "<<(a>b)<<"\n";}
catch(const std::runtime_error&){std::cout<<"OVERFLOW\n";}}}
