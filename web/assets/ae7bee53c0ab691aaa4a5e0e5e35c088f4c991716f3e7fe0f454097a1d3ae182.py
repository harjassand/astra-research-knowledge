"""Exact p=1,t=2 fixture for Lin2510.07162v1 Definitions 5.8/5.10.
Original type graph has all pairs including self-loops; both old CL maps are zero.
Binary original answer is the type label, so original game is perfect classical.
"""
from itertools import product
from collections import Counter
from fractions import Fraction
import json, math
from pathlib import Path

N=(1,1)
Z=(0,0)
def sample(seed):
    s0,s1,s2,s3,s4,s5=seed
    def local(v,mask,own,other):
        if mask==N:
            first=own
            second=tuple(other[j] if j==v else 0 for j in range(2))
        else:
            first=second=Z
        # The last one-bit register is old L_v(s)=0 in both cases.
        return (v,mask,0,Z,first,second,0)
    x=local(s0,s1,s4,s5)
    y=local(s2,s3,s5,s4)
    nt=(s1==s4==N and s3==s5==N)
    parity=(s0^s2) if nt else 0 # Definition5.10's dummy equality.
    return x,y,parity,nt

pairs=Counter()
for s0,s2 in product(range(2),repeat=2):
    for s1,s3,s4,s5 in product(list(product(range(2),repeat=2)),repeat=4):
        x,y,parity,nt=sample((s0,s1,s2,s3,s4,s5))
        pairs[(x,y,parity,nt)]+=1
assert sum(pairs.values())==1024
by_pair={}
for (x,y,parity,nt) in pairs:
    assert (x,y) not in by_pair or by_pair[(x,y)]==(parity,nt)
    by_pair[(x,y)]=(parity,nt)
z=(0,Z,0,Z,Z,Z,0)
x=(0,N,0,Z,N,(1,0),0)
y=(1,N,0,Z,N,(0,1),0)
cycle=[(x,z,0,False),(z,z,0,False),(z,y,0,False),(x,y,1,True)]
counts=[pairs[c] for c in cycle]
assert counts==[2,16,2,1],counts
witness_seeds=[
 (0,N,0,Z,N,N),
 (0,Z,0,Z,Z,Z),
 (0,Z,1,N,N,N),
 (0,N,1,N,N,N),
]
assert [sample(s) for s in witness_seeds]==cycle

# The paper's local honest extension (active question->type, otherwise->default0).
def active(q):
    v,mask,_,_,first,second,_=q
    return mask==N and first==N and second==tuple(1 if j==v else 0 for j in range(2))
def honest(q):return q[0] if active(q) else 0
published_loss=sum(c for (a,b,parity,nt),c in pairs.items() if (honest(a)^honest(b))!=parity)
# Proposed repair: nontrivial original test; dummy x!=y accepts automatically;
# full diagonal uses equality, exactly as required for strict synchronicity.
repaired_loss=sum(c for (a,b,parity,nt),c in pairs.items()
  if ((nt and (honest(a)^honest(b))!=parity)
      or (not nt and a==b and honest(a)!=honest(b))))
assert repaired_loss==0

out={
 'source':'https://arxiv.org/src/2510.07162v1',
 'seed_bits_effective':10,
 'old_body_register_bits':1,
 'old_body_map':'constant zero; extra body seed cancels in pair masses',
 'original_value':'1; deterministic answer is local type',
 'num_question_pairs':len(pairs),
 'cycle':[{'x':a,'y':b,'parity':p,'nontrivial':nt,
           'mass':str(Fraction(pairs[(a,b,p,nt)],1024))}
          for a,b,p,nt in cycle],
 'cycle_witness_seeds':witness_seeds,
 'quantum_upper_bound':'1-(2-sqrt(2))/1024',
 'quantum_upper_bound_decimal':1-(2-math.sqrt(2))/1024,
 'published_honest_extension_loss':str(Fraction(published_loss,1024)),
 'proposed_repair_honest_loss':str(Fraction(repaired_loss,1024)),
 'first_prefix_active_probability':'1/4',
 'proved_universal_resampling_gap_lower_bound_fixture':'3/8'
}
Path('work/agents/repetition_application/results/detyping_counterexample.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('cycle','cycle_witness_seeds')},indent=2))
