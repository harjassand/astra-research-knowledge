"""Final coupled-chain CDF check against a directly killed 3-state matrix."""
from chain_passage import *
from run_validation import serial
from itertools import product
from pathlib import Path
import time,json

ch=Chain([F(3,5)],[1,F(4,3)])
x=(-1,1);A=[(1,1)];T=F(5,4);eps=F(1,32)
t0=time.perf_counter()
def progress(data):
    print(data,'seconds',round(time.perf_counter()-t0,3),flush=True)
r=passage_cdf(ch,x,A,T,eps,progress=progress)
elapsed=time.perf_counter()-t0

# Independent explicitly constructed comparator: only the 3 non-target states.
states=[v for v in product((-1,1),repeat=2) if v not in A]
K=[[F(0) for _ in states] for _ in states]
for i,v in enumerate(states):
    for site in range(2):
        loc=ch.a[site]*v[site-1] if site else ch.b[site]*v[site+1]
        rate=ch.lam[site]*(1-v[site]*loc)/2
        K[i][i]+=rate
        w=list(v);w[site]*=-1;w=tuple(w)
        if w in states:
            K[i][states.index(w)]-=rate
N=len(states)
U,den,err=exp_fixed(([[-T*v for v in row] for row in K],[[F(0)]*N for _ in range(N)]),
                    F(1),F(1,1<<70))
survival=F(sum(int(v) for v in U[0][states.index(x)]),den)
truth=1-survival
discrepancy=abs(r['mid']-truth)
assert discrepancy+err <= r['error']
data={'bonds':ch.t,'clocks':ch.lam,'initial':x,'targets':A,'time':T,
      'requested_radius':eps,'result':r,'wall_seconds':elapsed,
      'direct_killed_states':N,'direct_midpoint':truth,'direct_error':err,
      'discrepancy':discrepancy,'enclosure_check':True}
Path(__file__).with_name('cdf_two_spin_record.json').write_text(json.dumps(serial(data),indent=2)+'\n')
print('coupled CDF passed','mid',float(r['mid']),'radius',float(r['error']),
      'direct',float(truth),'seconds',round(elapsed,3),flush=True)
