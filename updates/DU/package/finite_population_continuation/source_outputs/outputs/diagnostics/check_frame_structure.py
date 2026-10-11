"""Finite diagnostics for the proved structural lemmas; no universal certification."""
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np


def exact_simplex(q):
 n=q+1
 if q>40:
  mean=(F(1)+q*F(1,q*q))/n
  assert mean==F(1,q)
  assert (F(1)-mean)/(1-mean)==1
  assert (F(1,q*q)-mean)/(1-mean)==F(-1,q)
  return dict(q=q,states=n,clone_defect=str(mean),mode="exact two-entry symmetry formulas")
 gram=[[F(1) if i==j else F(-1,q) for j in range(n)] for i in range(n)]
 target=[[z*z for z in row] for row in gram]
 mean=[sum(row,F(0))/n for row in target]
 norm=sum(mean,F(0))/n
 assert norm==F(1,q) and all(v==F(1,q) for v in mean)
 center=[[target[i][j]-mean[i]-mean[j]+norm for j in range(n)] for i in range(n)]
 vgram=[[z/(1-F(1,q)) for z in row] for row in center]
 assert vgram==gram
 fidelity=(1-F(1,q))**2/(1-F(1,q))
 assert fidelity==1-F(1,q)
 return dict(q=q,states=n,clone_defect=str(1-fidelity))


def compression_test(effects, reps):
 d=len(reps[0]);k=len(reps);n=max(d,k)
 rows=[];risks=[]
 for m,psi in zip(effects,reps):
  a=float(np.vdot(psi,m@psi).real)
  assert a>0
  v=m@psi/np.sqrt(a)
  assert np.linalg.eigvalsh(m-np.outer(v,v.conj())).min()>-1e-10
  rows.append(v.conj());risks.append(1-a)
 t=np.zeros((n,d),dtype=complex);t[:k]=rows
 assert np.linalg.eigvalsh(np.eye(d)-t.conj().T@t).min()>-1e-10
 l,s,rh=np.linalg.svd(t,full_matrices=False)
 u=l@rh
 assert np.linalg.norm(u.conj().T@u-np.eye(d))<1e-10
 margins=[]
 for c,psi in enumerate(reps):
  wrong=1-abs((u@psi)[c])**2
  assert wrong<=4*risks[c]+1e-10
  margins.append(float(4*risks[c]-wrong))
 return dict(d=d,k=k,n=n,max_representative_risk=float(max(risks)),minimum_four_risk_margin=min(margins))


def main():
 out={'scope':'Finite exact simplex identities and floating-point polar examples only.'}
 out['exact_simplex']=[exact_simplex(q) for q in (2,3,7,29,2801,5603)]
 tests=[]
 for d in (2,3,9):
  reps=np.eye(d,dtype=complex)
  for noise in (.001,.07):
   effects=[(1-noise)*np.outer(v,v.conj())+(noise/d)*np.eye(d) for v in reps]
   tests.append(compression_test(effects,reps))
 for d in (3,9,40):
  n=d+1
  raw=np.eye(n)-np.ones((n,n))/n
  vals,vec=np.linalg.eigh(raw)
  basis=vec[:,vals>.5]
  reps=np.sqrt(n/d)*basis.conj()
  for noise in (.001,.03):
   effects=[(1-noise)*(d/n)*np.outer(v,v.conj())+(noise/n)*np.eye(d) for v in reps]
   assert np.linalg.norm(sum(effects)-np.eye(d))<1e-10
   tests.append(compression_test(effects,reps))
 out['polar_examples']=tests
 out['passed']=True
 Path(__file__).with_name('FRAME_CHECKS.json').write_text(json.dumps(out,indent=2))
 print(json.dumps(dict(passed=True,exact_simplex_cases=len(out['exact_simplex']),polar_cases=len(tests))))

if __name__=='__main__':main()
