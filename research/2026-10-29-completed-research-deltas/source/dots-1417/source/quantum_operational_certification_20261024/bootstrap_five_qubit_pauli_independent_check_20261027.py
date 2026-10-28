"""Exact phase-free exhaustive stabilizer check; no external dependencies.
Tests all 4**5 errors, exact biased laws, mixtures, and concatenation.
"""
from itertools import product
from collections import Counter
from fractions import Fraction as F
import json
from pathlib import Path

P={'I':(0,0),'X':(1,0),'Y':(1,1),'Z':(0,1)}
def vec(s): return tuple(P[c][0] for c in s)+tuple(P[c][1] for c in s)
def add(a,b): return tuple(x^y for x,y in zip(a,b))
def sp(a,b): return sum(a[i]*b[i+5]+a[i+5]*b[i] for i in range(5))%2
G=list(map(vec,['XZZXI','IXZZX','XIXZZ','ZXIXZ']))
LX,LZ=vec('XXXXX'),vec('ZZZZZ')
assert all(sp(a,b)==0 for a in G for b in G)
assert sp(LX,LZ)==1
S={vec('IIIII')}
for g in G: S|={add(s,g) for s in list(S)}
assert len(S)==16
syn=lambda e:tuple(sp(e,g) for g in G)
cor={syn(vec('IIIII')):vec('IIIII')}
for i in range(5):
 for c in 'XYZ':
  s='I'*i+c+'I'*(4-i); e=vec(s)
  assert syn(e) not in cor
  cor[syn(e)]=e
assert len(cor)==16
logical_from_bits={(0,0):'I',(1,0):'X',(1,1):'Y',(0,1):'Z'}
rows=[]; weights={str(w):Counter() for w in range(6)}; enums={l:Counter() for l in 'IXYZ'}
for chars in product('IXYZ',repeat=5):
 s=''.join(chars); e=vec(s); sy=syn(e); r=add(e,cor[sy])
 assert syn(r)==(0,0,0,0)
 bits=(sp(r,LZ),sp(r,LX)); logical=logical_from_bits[bits]
 target=add(LX if bits[0] else vec('IIIII'),LZ if bits[1] else vec('IIIII'))
 assert add(r,target) in S
 w=5-s.count('I')
 if w<=1: assert logical=='I'
 weights[str(w)][logical]+=1
 counts=tuple(s.count(c) for c in 'IXYZ'); enums[logical][counts]+=1
 rows.append((s,sy,logical,counts))
assert len(rows)==1024
assert all(sum(w.values())==__import__('math').comb(5,int(i))*3**int(i) for i,w in weights.items())
def apply(q):
 out={l:F(0) for l in 'IXYZ'}
 for _,_,l,counts in rows:
  prob=F(1)
  for c,n in zip('IXYZ',counts): prob*=q[c]**n
  out[l]+=prob
 assert sum(out.values())==1
 p=1-q['I']; pn=1-out['I']
 assert pn<=10*p*p
 return out
samples={
 'identity':dict(zip('IXYZ',[F(1),F(0),F(0),F(0)])),
 'pure_X_p_1_25':dict(zip('IXYZ',[F(24,25),F(1,25),F(0),F(0)])),
 'pure_Y_p_1_25':dict(zip('IXYZ',[F(24,25),F(0),F(1,25),F(0)])),
 'biased_p_1_25':dict(zip('IXYZ',[F(24,25),F(1,50),F(1,75),F(1,150)])),
 'depolarizing_p_1_25':dict(zip('IXYZ',[F(24,25),F(1,75),F(1,75),F(1,75)])),
}
# Whole simplex rational grid, including cases well outside threshold.
grid=0
for x in range(21):
 for y in range(21-x):
  for z in range(21-x-y):
   apply(dict(zip('IXYZ',[F(20-x-y-z,20),F(x,20),F(y,20),F(z,20)]))); grid+=1
results={name:apply(q) for name,q in samples.items()}
# Bias does not have to remain the same across concatenation levels.
conc=[]; q=samples['biased_p_1_25']; p0=1-q['I']
for level in range(1,4):
 q=apply(q); p=1-q['I']; bound=(10*p0)**(2**level)/10
 assert p<=bound
 conc.append({'level':level,'p':float(p),'bound':float(bound)})
# Latent mixture: fixed hidden component for all carriers, not fresh per slot.
qa=samples['identity']; qb=samples['pure_X_p_1_25']; qm={c:(qa[c]+qb[c])/2 for c in 'IXYZ'}
true_mix={c:(apply(qa)[c]+apply(qb)[c])/2 for c in 'IXYZ'}
wrong_mix=apply(qm)
assert true_mix!=wrong_mix
# Correlated hardware counterexample: I^5 with 1-p, X^5 with p.
assert next(l for s,_,l,_ in rows if s=='XXXXX')=='X'
p=F(1,25); assert p>10*p*p
out={
 'errors_enumerated':len(rows),'single_error_syndromes':len(cor),
 'logical_counts_by_weight':weights,'simplex_grid_cases':grid,
 'biased_cases':results,'concatenation':conc,
 'shared_latent_mixture':true_mix,'incorrect_product_of_average':wrong_mix,
 'correlated_counterexample':{'marginal_p':p,'logical_p':p,'claimed_10p2':10*p*p},
 'complete_enumerator':{l:{','.join(map(str,k)):v for k,v in sorted(e.items())} for l,e in enums.items()},
}
def serial(v):
 if isinstance(v,F):return {'exact':str(v),'float':float(v)}
 raise TypeError(type(v).__name__)
path=Path(__file__).with_suffix('.json'); path.write_text(json.dumps(out,default=serial,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='complete_enumerator'},default=serial,indent=2))
