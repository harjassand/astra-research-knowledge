"""Independent ring and controller-latency checks for the receiving review."""
from fractions import Fraction as F
from pathlib import Path
import json
u=(F(1,10),F(3,10),F(1,4),F(7,20))
v=(F(1,20),F(-3,20),F(1,10),F(-1,10))
N=4
states=range(1<<N)
bit=lambda x,i:(x>>(i%N))&1
weights={x:F(3,5)**(sum(bit(x,i)!=bit(x,i+1) for i in range(N))//2) for x in states}
Z=sum(weights.values());pi={x:w/Z for x,w in weights.items()}
rows={x:{x:F(0)} for x in states};local_counts=set()
for x in states:
    for i in range(N):
        neighbours=bit(x,i-1)+bit(x,i+1)
        p=(F(3,8),F(1,2),F(5,8))[neighbours]
        alpha=F(9,20)*(p if bit(x,i)==0 else 1-p)
        nB=int(8*(alpha-F(3,20))/F(3,20));counts=[0,0,0,0]
        for key in range(32):
            selector=key&7;raw=key>>3
            if selector<nB:j=2+(raw>=2)
            else:j=(raw==3)
            counts[j]+=1
        counts=tuple(counts);local_counts.add(counts)
        assert sum(F(counts[j],32)*u[j] for j in range(4))==alpha
        assert sum(F(counts[j],32)*v[j] for j in range(4))==0
        y=x^(1<<i)
        rows[x][y]=rows[x].get(y,F(0))+alpha/N
        rows[x][x]+=(1-alpha)/N
        x0=x&~(1<<i);x1=x|(1<<i)
        assert weights[x1]/(weights[x0]+weights[x1])==p
for x in states:
    assert sum(rows[x].values())==1
    for y in states:
        assert pi[x]*rows[x].get(y,F(0))==pi[y]*rows[y].get(x,F(0))
latency=[]
for c in (F(3,20),F(3,10)):
    outputs=[c+(1-2*c)*(u[3]+v[3]*h) for h in (F(-1),F(1))]
    assert outputs[0]!=outputs[1]
    latency.append({'compiled_c':str(c),'unprotected_mode3_delay_at_hminus':str(outputs[0]),
                    'unprotected_mode3_delay_at_hplus':str(outputs[1])})
out={'scope':'Independent rational network algebra and latency-scope counterexample; not apparatus trials',
     'visible_states':16,'local_contexts':64,'fresh_bit_strings_per_context':32,
     'primitive_key_counts':sorted(local_counts),'all_hidden_slopes_cancel_symbolically':True,
     'full_random_scan_kernel_stochastic':True,'detailed_balance_entries':256,
     'relative_weight_normalization':str(Z),
     'Gibbs_probabilities_by_domain_wall_count':{'0':'25/248','2':'15/248','4':'9/248'},
     'unprotected_latency_counterexamples':latency}
Path(__file__).with_name('SIGNED_REVIEW_ADDITIONAL_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
