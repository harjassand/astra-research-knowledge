import sys,json
sys.dont_write_bytecode=True
import numpy as np
from pathlib import Path
raw=json.loads((Path(__file__).parent/'free_third_char_aspect.json').read_text());groups={}
for m,c in raw:groups.setdefault(tuple(m[:2]),[]).append((m[2:],float(c)))
rng=np.random.default_rng(1234);p=rng.normal(size=20000);q=rng.normal(size=20000);e=np.exp(rng.uniform(-2.5,2.5,size=20000));p/=np.sqrt(p*p+q*q);q/=np.sqrt(p*p+q*q)
for key,terms in groups.items():
 vals=sum(co*p**m[0]*q**m[1]*e**m[2] for m,co in terms);ii=np.argmin(vals)
 if vals[ii]<-1e-4:print('NEG GROUP',key,vals[ii],p[ii],q[ii],e[ii])
print('done')
