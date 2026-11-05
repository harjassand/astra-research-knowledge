"""Check the audit's four-limb arithmetic against Python arbitrary integers."""
from pathlib import Path
import random,subprocess,json
P=Path(__file__).resolve().parent
source=P/'wide_arithmetic_test.cpp'
source.write_text('''#define main certificate_main
#include "check_rows.cpp"
#undef main
int main(){int op;while(std::cin>>op){uint256_t a,b,z;unsigned k;
for(auto &x:a.limb)std::cin>>x;for(auto &x:b.limb)std::cin>>x;std::cin>>k;
try{if(op==0)z=a+b;else if(op==1)z=a<<k;else z=uint256_t::product(a.limb[0],b.limb[0]);
for(auto x:z.limb)std::cout<<x<<" ";std::cout<<bits(z)<<" "<<(a>b)<<"\\n";}
catch(const std::runtime_error&){std::cout<<"OVERFLOW\\n";}}}
''')
exe=P/'wide_arithmetic_test';subprocess.run(['g++','-O2','-std=c++17',str(source),'-o',str(exe)],check=True)
rng=random.Random(721163);mask=(1<<64)-1;cases=[];rows=[]
for i in range(12000):
    op=i%3;a=rng.getrandbits(rng.choice([0,1,63,64,65,127,128,129,191,192,255,256]));b=rng.getrandbits(rng.randrange(257));k=rng.choice([0,1,63,64,65,127,128,129,191,192,255,256,300])
    result=a+b if op==0 else a<<k if op==1 else (a&mask)*(b&mask)
    cases.append((result,a>b));rows.append(' '.join(map(str,[op]+[(a>>(64*j))&mask for j in range(4)]+[(b>>(64*j))&mask for j in range(4)]+[k])))
run=subprocess.run([str(exe)],input='\n'.join(rows)+'\n',capture_output=True,text=True,check=True)
output=run.stdout.splitlines();assert len(output)==len(cases);overflows=0
for line,(expected,gt) in zip(output,cases):
    if expected>=1<<256:assert line=='OVERFLOW';overflows+=1;continue
    vals=list(map(int,line.split()));assert len(vals)==6
    actual=sum(vals[j]<<(64*j) for j in range(4))
    assert actual==expected and vals[4]==expected.bit_length() and vals[5]==gt
out={'status':'PASS','cases':len(cases),'correctly_detected_overflows':overflows}
(P/'wide_arithmetic_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
