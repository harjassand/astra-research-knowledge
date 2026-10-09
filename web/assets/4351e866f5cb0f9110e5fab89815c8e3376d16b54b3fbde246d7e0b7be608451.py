#!/usr/bin/env python3
"""Finite diagnostic of spin normalization/marginals and entropy identity."""
from pathlib import Path
import json, math
import numpy as np
ROOT=Path(__file__).resolve().parent
def spins(j):
 m=np.arange(-j,j+1,1,dtype=float)
 plus=np.zeros((len(m),len(m)),complex)
 for i,x in enumerate(m[:-1]):
  plus[i+1,i]=math.sqrt(j*(j+1)-x*(x+1))
 minus=plus.conj().T
 return [(plus+minus)/2,(plus-minus)/(2j),np.diag(m)]
def partial(x,dims,keep):
 ds=list(dims); a=x.reshape(ds+ds)
 for i in sorted(set(range(len(ds)))-set(keep),reverse=True):
  a=np.trace(a,axis1=i,axis2=i+len(ds)); ds.pop(i)
 d=math.prod(ds)
 return a.reshape(d,d)
def entropy(x):
 es=np.linalg.eigvalsh((x+x.conj().T)/2)
 es=es[es>1e-12]
 return float(-np.sum(es*np.log(es)))
def cmi(x,dims,X,Y,Z):
 def h(ks):
  return entropy(partial(x,dims,sorted(ks)))
 return h(set(X)|set(Z))+h(set(Y)|set(Z))-h(Z)-h(set(X)|set(Y)|set(Z))
def dephase_records(x,dims):
 a=x.reshape(dims+dims); out=np.zeros_like(a)
 for b in range(dims[1]):
  for c in range(dims[2]):
   out[:,b,c,:,b,c]=a[:,b,c,:,b,c]
 return out.reshape(x.shape)
def halfnorm(x):
 return float(np.abs(np.linalg.eigvalsh((x+x.conj().T)/2)).sum()/2)
def hbin(q):
 return -q*math.log(q)-(1-q)*math.log(1-q)
spin_results=[]
for j in [.5,1,1.5,2,3,4]:
 d=int(2*j+1); dims=[2,d,d]; J=2*j
 sj=spins(j); sa=spins(.5); eye=np.eye(d)
 big=[np.kron(s,eye)+np.kron(eye,s) for s in sj]
 cas=sum(s@s for s in big)
 eig,vec=np.linalg.eigh(cas)
 pj=vec[:,np.abs(eig-J*(J+1))<1e-8]
 PJ=pj@pj.conj().T
 ident=np.kron(np.eye(2),PJ)
 coupling=sum(np.kron(a,b) for a,b in zip(sa,big))
 PM=ident@(J*np.eye(2*d*d)-2*coupling)/(2*J+1)
 PP=ident-PM
 rho=PM/(2*J); rhop=PP/(2*J+2)
 p=2*J/(2*J+1); sep=p*rho+(1-p)*rhop
 q=1/(4*j+2)
 HAB=hbin(q)+(1-q)*math.log(2*j)+q*math.log(2*j+2)
 delta=HAB+math.log(4*j+1)-math.log(2*j+1)-math.log(4*j)
 db=cmi(rho,dims,[0],[2],[1])
 dc=cmi(rho,dims,[0],[1],[2])
 ab=partial(rho,dims,[0,1]); bc=partial(rho,dims,[1,2])
 rd=dephase_records(rho,dims); bcd=partial(rd,dims,[1,2])
 cb=entropy(np.diag(np.diag(partial(rho,dims,[1]))))-entropy(partial(rho,dims,[1]))
 cc=entropy(np.diag(np.diag(partial(rho,dims,[2]))))-entropy(partial(rho,dims,[2]))
 CR=entropy(rd)-entropy(rho); CK=entropy(bcd)-entropy(bc)
 tprime=cmi(rd,dims,[0],[2],[1])+cmi(rd,dims,[0],[1],[2])
 cdrop=cmi(rho,dims,[1],[2],[0])-cmi(rd,dims,[1],[2],[0])
 identity=(db+dc)-tprime+2*CK-cb-cc-cdrop
 row={
  "j":j,"dimension_ABC":2*d*d,
  "projector_defect_frobenius":float(np.linalg.norm(PM@PM-PM)),
  "projector_rank":int(round(np.trace(PM).real)),
  "trace_error":float(abs(np.trace(rho)-1)),
  "AB_entropy_error":abs(entropy(ab)-HAB),
  "delta_numeric":db,"delta_exact":delta,
  "two_CMI_difference":abs(db-dc),
  "delta_formula_error":abs(db-delta),
  "halftrace_to_explicit_sep":halfnorm(rho-sep),
  "exact_sep_distance_formula":1/(4*j+1),
  "A_marginal_error":halfnorm(partial(rho,dims,[0])-partial(sep,dims,[0])),
  "BC_marginal_error":halfnorm(bc-partial(sep,dims,[1,2])),
  "dephasing_identity_error":abs(CR-identity),
  "CMI_drop_under_dephasing":cdrop,
  "proof_scope":"Finite diagnostics only; twirl separability and all-dimensional theorem are analytic."
 }
 for key in ["projector_defect_frobenius","trace_error","AB_entropy_error","two_CMI_difference","delta_formula_error","A_marginal_error","BC_marginal_error","dephasing_identity_error"]:
  assert row[key]<2e-9,(j,key,row[key])
 assert cdrop>-2e-9
 assert abs(row["halftrace_to_explicit_sep"]-row["exact_sep_distance_formula"])<2e-9
 spin_results.append(row)
out={"status":"PASS","scope":"Finite six-spin diagnostic; not a proof of arbitrary states or a counterexample.","results":spin_results}
(ROOT/"FINITE_DIAGNOSTICS.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":"PASS","cases":len(spin_results),"max_entropy_formula_error":max(r["delta_formula_error"] for r in spin_results),"max_identity_error":max(r["dephasing_identity_error"] for r in spin_results)}))

