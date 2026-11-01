"""Same-author rational INTERVAL checks at genuinely enormous count states.
No huge profile power is expanded. q^M>=2 gives certified truncation intervals.
This is not an independent proof and does not replace the analytic tails.
"""
from fractions import Fraction as F
from pathlib import Path
import multiface as M
import json,hashlib
root=Path(__file__).resolve().parent
p=M.construct(M.fixture());r=p['raw'];precision=8192
counts=dict(pointwise_foster=0,global_sum=0,nonempty_large_subset=0,strict_subset_transfer=0,terminal_empty=0)

def zinterval(j):
 k=j+p['s0']
 if k<=20000:
  z=M.profile(p,j);return z,z
 # q^M>=2, hence q^-k<=2^-floor(k/M); clipping only weakens the bound.
 power=min(k//p['M'],precision);upper=F(1,2**power)
 return (1-upper)/k,F(1,k)

def dinterval(j):
 k=j+p['s0']
 if k<=20000:
  d=M.diff(p,j);return d,d
 power=min(k//p['M'],precision);upper=F(1,2**power)
 base=F(1,k*(k+1));corr=F(1,k)-1/(p['q']*(k+1))
 return base-upper*corr,base

def psi_interval(x):
 lo=hi=F(0)
 for f in p['faces']:
  j=sum(w*z for w,z in zip(f['resource_weights'],x));a,b=zinterval(j);lo+=f['weight']*a;hi+=f['weight']*b
 return lo,hi

def h_interval(x):
 lo,hi=psi_interval(x);A=x[r['A']];N=sum(x);Q=sum(x[u]*x[v] for u,v in r['edges'])
 base=1-p['e']*A/(N+1)+(p['H'] if A==0 and Q==0 else 0)
 return lo+base,hi+base

def gen_interval(x,fn):
 lox,hix=fn(x);lo=hi=F(0)
 for u,v,k in r['channels']:
  rate=k*M.propensity(u,x)
  if rate:
   y=tuple(xx+vv-uu for xx,uu,vv in zip(x,u,v));ly,hy=fn(y);tt=p['t']**(sum(v)-sum(u))
   lo+=rate*(tt*ly-hix);hi+=rate*(tt*hy-lox)
 return lo,hi

N=p['Nstar']+10;T=p['T'];U=T+2
# Triangle 1,2,3 plus edge4,5. I={1,4} independent. Include a smaller inactive
# Far tier (4 relative to I={1}), active outside hubs, last-A states, large ratios.
states=[(0,N,0,0,0,0),(1,N,0,0,0,0),(0,N,0,0,N//10,0),
        (0,N,0,0,N//(10*T),0),(1,N,0,0,N//(10*T),0),
        (0,N,1,0,N//(10*T),0),(0,N,0,0,N//(10*T),1),
        (0,N,N,0,0,0),(N,N,0,0,0,0),(0,N,0,0,U,U),
        (1,N,0,0,T+1,0),(0,N,T,0,T+1,1),
        (0,N,0,0,1,1),(1,N,0,0,1,1)]
for ix,x in enumerate(states):
 assert sum(x)>=p['Nstar']
 low,high=gen_interval(x,h_interval)
 assert high<=-p['nu'],(ix,'pointwise Foster failed')
 counts['pointwise_foster']+=1
 actual_lo,actual_hi=gen_interval(x,psi_interval);pl,ph=psi_interval(x);Supper=F(0)
 A=x[r['A']];nn=sum(x);Q=sum(x[u]*x[v] for u,v in r['edges'])
 for f in p['faces']:
  FI=sum(x[i] for i in f['I']);ui=nn-FI;j=sum(w*z for w,z in zip(f['resource_weights'],x));dl,dh=dinterval(j)
  assert dl>0
  cross=sum(x[u]*x[v] for u,v in r['edges'] if (u in f['I'])!=(v in f['I']))
  far=sum(x[u]*x[v] for u,v in r['edges'] if u in f['Far'] and v in f['Far'])
  Supper+=f['weight']*(p['g']*A*FI+p['h']*(cross+far))*dh
  large=frozenset(i for i in f['I'] if x[i]>=T*(ui+1))
  if not large:
   counts['terminal_empty']+=1;assert nn<=p['B']*(ui+1)
  else:
   counts['nonempty_large_subset']+=1
   assert FI>=T*(ui+1)
   if large!=f['I']:
    counts['strict_subset_transfer']+=1
    fj=next(g for g in p['faces'] if g['I']==large);uj=nn-sum(x[i] for i in large)
    assert uj<=p['B']*(ui+1)
    for u,v in r['edges']:
     if u in f['I'] or v in f['I'] or not(u in f['Near'] or v in f['Near']):continue
     if u not in fj['Near'] and v not in fj['Near']:assert u in fj['Far'] and v in fj['Far']
 rhs_low=r['lam']*p['eps']*pl-Supper/2+p['RA']*A/F(nn+1)+p['RQ']*Q/F((nn+1)**2)
 assert actual_hi<=rhs_low,(ix,'global sum failed')
 counts['global_sum']+=1
 print('certified huge state',ix,'Nbits',nn.bit_length(),flush=True)
assert counts['strict_subset_transfer']>0 and counts['nonempty_large_subset']>0
result=dict(status='PASS_SAME_AUTHOR_CERTIFIED_INTERVAL_TIER_CHECKS',counts=counts,precision_bits=precision,Nstar_bits=p['Nstar'].bit_length(),bindings={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in ['THEOREM_PENDING.md','multiface.py','check_large_tiers.py']})
(root/'large_tier_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
