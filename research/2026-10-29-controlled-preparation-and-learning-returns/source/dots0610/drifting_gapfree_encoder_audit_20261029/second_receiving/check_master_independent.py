from fractions import Fraction as F
from itertools import product
from math import lcm,log,ceil,sqrt
from pathlib import Path
import json,random
rng=random.Random(290606)
# Exact all-path expansion of a two-expert, five-step fixed-share kernel.
M=2;T=5;alpha=F(1,4);eta=F(1,8)
losses=[[F(1,3),F(4,3)],[F(0),F(0)],[F(3,2),F(1,2)],[F(0),F(0)],[F(0),F(0)]]
w=[F(1,2)]*2;total=F(1)
for losses_t in losses:
 v=[w[j]*(1-eta*losses_t[j]) for j in range(M)];z=sum(v);total*=z;w=[(1-alpha)*x/z+alpha/M for x in v]
paths=F(0)
for path in product(range(M),repeat=T):
 q=F(1,M)
 for t,j in enumerate(path):
  q*=1-eta*losses[t][j]
  if t:q*=((1-alpha) if path[t-1]==j else 0)+alpha/M
 paths+=q
assert paths==total
# Different-size bases, exact integer versus independent Fraction implementation.
p=F(1,3);etas=[F(1,12),F(1,24)];shares=[F(0),F(1,4)];sizes=[2,3];H=2;eta0=F(1,12)
W=[[1]*m for m in sizes];refs=[[F(1,m)]*m for m in sizes];V=[1,1];vref=[F(1,2)]*2;maxbits=0;steps=36
for t in range(steps):
 learning=rng.randrange(3)==0
 # Same synthetic current record generates distinct finite-net loss arrays.
 record=[rng.randrange(7) for _ in range(3)]
 obs=[[F(record[j],6) for j in range(m)] for m in sizes]
 ell=[[x/p if learning else F(0) for x in row] for row in obs]
 ml=[sum(F(W[b][j],sum(W[b]))*ell[b][j] for j in range(sizes[b])) for b in range(H)]
 mf=[1-eta0*x for x in ml];den=lcm(*(x.denominator for x in mf));V=[V[b]*int(mf[b]*den) for b in range(H)]
 vr=[vref[b]*mf[b] for b in range(H)];vref=[x/sum(vr) for x in vr]
 assert [F(x,sum(V)) for x in V]==vref
 for b,m in enumerate(sizes):
  factors=[1-etas[b]*x for x in ell[b]];den=lcm(*(x.denominator for x in factors));tmp=[W[b][j]*int(factors[j]*den) for j in range(m)];aa=shares[b].numerator;bb=shares[b].denominator
  W[b]=[(bb-aa)*m*x+aa*sum(tmp) for x in tmp]
  rr=[refs[b][j]*factors[j] for j in range(m)];refs[b]=[(1-shares[b])*x/sum(rr)+shares[b]/m for x in rr]
  assert [F(x,sum(W[b])) for x in W[b]]==refs[b]
 maxbits=max(maxbits,*(x.bit_length() for x in V))
# Check bank coverage against deterministic envelopes, no fitted data choices.
bankchecks=[]
for L in [4,8,16,32,64]:
 T=2**L;J=(L+3)//4
 for x in [0.,T**(-.5),1./L]:
  target=max(T**(-.25),x**.2);eps_candidates=[2.**(-j) for j in range(J+1)]
  eps=min(eps_candidates,key=lambda e:abs(log(e/target)));assert .5<=eps/target<=2
  S=min(T-1,ceil(x*T/eps));M=(int(5/eps)*2+1)**3
  shares_f=[0.]+[2.**(-k) for k in range(1,L+2)]
  if S==0:a=0.;K=log(M)
  else:
   optimum=min(.5,S/(T-1));a=min(shares_f[1:],key=lambda z:abs(log(z/optimum)));assert .5<=a/optimum<=2
   K=log(M)+S*log(M/a)+(T-1-S)*(-log(1-a))
  opteta=min(float(p)/2,sqrt(float(p)*K/T));eta_values=[float(p)*2.**(-ll-1) for ll in range(L+2)];ee=min(eta_values,key=lambda e:abs(log(e/opteta)));assert .5<=ee/opteta<=2
  bankchecks.append(dict(log2T=L,variation_ratio=x,epsilon=eps,switch_budget=str(S),entropy_per_round=K/T))
out={'scope':'Exact kernel/path identity and integer/Fraction master consistency; parameter-bank coverage diagnostics use floating logarithms, not quantum data.','all_path_expansion_exact':str(total),'integer_fraction_update_steps':steps,'base_sizes':sizes,'master_max_integer_bits':maxbits,'bank_checks':bankchecks,'post_selection_cap_bias':str(F(4,7)),'all_base_prefetch_restored':str(F(1,2))}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='bank_checks'},indent=2))
