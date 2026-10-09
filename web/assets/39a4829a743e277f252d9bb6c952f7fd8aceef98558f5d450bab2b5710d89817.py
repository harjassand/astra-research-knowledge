#!/usr/bin/env python3
"""Finite diagnostic: rare-sector exact entropy and conservative cost gates."""
from pathlib import Path
from decimal import Decimal, localcontext
import itertools, math, json
import numpy as np
ROOT=Path(__file__).resolve().parent
def F(q,a):
 if not q: return Decimal(0)
 if q==1: return -(a.ln())
 v=a+q*(1-a)
 return v*(v/a).ln()+(1-v)*((1-v)/(1-a)).ln()
def bern(v,s):
 if v==1: return -s.ln()
 if v==0: return -(1-s).ln()
 return v*(v/s).ln()+(1-v)*((1-v)/(1-s)).ln()
rows=[]
with localcontext() as ctx:
 ctx.prec=70
 for m in [1,2,3,10,100,1000]:
  k=2*m+1
  for d in [4*m,100*m+1,100000*m+1]:
   a=Decimal(d-2*m)/(d*k)
   A=Decimal(d-m)/(d*(m+1))
   for qstr in ["0","1e-12","1e-8","1e-4","0.01","0.1","0.5","0.99","1"]:
    q=Decimal(qstr)
    delta=F(q,a)-F(q,A)
    bound=q*q*k/32 if q<=a else q/32
    assert delta+Decimal("1e-60")>=bound,(m,d,q,delta,bound)
    status="SEPARABLE_BELOW_THRESHOLD"
    dsep=None
    if q>Decimal(1)/(d+1) and q<=a:
     s=Decimal(1)/k; v=a+q*(1-a)
     dsep=bern(v,s)
     assert dsep<=48*delta+Decimal("1e-60")
     status="LOW_LIKELIHOOD_RELATIVE_ENTROPY"
    elif q>a:
     assert q<=32*delta+Decimal("1e-60")
     status="HIGH_LIKELIHOOD_TRACE"
    rows.append({"m":m,"d":d,"q":qstr,"delta":str(delta),
                 "lower_bound":str(bound),"regime":status,
                 "relative_entropy_to_explicit_sep":None if dsep is None else str(dsep)})
def wedge(d,r):
 n=d**r; cols=[]
 for subset in itertools.combinations(range(d),r):
  v=np.zeros(n,complex)
  for perm in itertools.permutations(subset):
   sign=(-1)**sum(perm[i]>perm[j] for i in range(r) for j in range(i+1,r))
   idx=sum(x*d**(r-1-i) for i,x in enumerate(perm))
   v[idx]=sign/math.sqrt(math.factorial(r))
  cols.append(v)
 mat=np.stack(cols,axis=1)
 return mat@mat.conj().T
def partial(x,dims,keep):
 ds=list(dims); a=x.reshape(ds+ds)
 for i in sorted(set(range(len(ds)))-set(keep),reverse=True):
  a=np.trace(a,axis1=i,axis2=i+len(ds)); ds.pop(i)
 return a.reshape(math.prod(ds),math.prod(ds))
def entropy(x):
 es=np.linalg.eigvalsh((x+x.conj().T)/2); es=es[es>1e-12]
 return float(-np.dot(es,np.log(es)))
dense=[]
for d in [4,5]:
 m=1; k=3; D=d*math.comb(d,2); R=math.comb(d,3)
 P=wedge(d,3); Q=np.kron(np.eye(d),wedge(d,2))
 prod=Q/D; omega=P/R; kappa=wedge(d,2)/math.comb(d,2)
 s=1/3; sep=s*omega+(1-s)*(Q-P)/(D-R)
 pt=sep.reshape(d,d*d,d,d*d).swapaxes(0,2).reshape(d**3,d**3)
 assert np.linalg.eigvalsh(pt).min()>-1e-10
 assert np.linalg.norm(partial(sep,[d,d,d],[1,2])-kappa)<1e-10
 for q in [.0001,.2,.8,1]:
  rho=(1-q)*prod+q*omega
  hab=entropy(partial(rho,[d,d,d],[0,1]))
  hbc=entropy(kappa); hg=entropy(rho)
  delta=hab+hbc-math.log(d)-hg
  with localcontext() as ctx:
   ctx.prec=50
   a=Decimal(d-2)/(3*d); A=Decimal(d-1)/(2*d)
   exact=float(F(Decimal(str(q)),a)-F(Decimal(str(q)),A))
  assert abs(delta-exact)<2e-10
  dense.append({"d":d,"q":q,"delta_numeric":delta,"delta_binary_formula":exact,"error":abs(delta-exact),"sep_boundary_PT_minimum":float(np.linalg.eigvalsh(pt).min())})
out={"status":"PASS","scope":"Finite decimal parameter inequalities and 8 dense matrices only; not a general proof or a counterfamily.","parameter_cases":len(rows),"dense_cases":len(dense),"parameters":rows,"dense":dense}
(ROOT/"RARE_SECTOR_DIAGNOSTICS.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":"PASS","parameter_cases":len(rows),"dense_cases":len(dense),"max_entropy_formula_error":max(r["error"] for r in dense)}))

