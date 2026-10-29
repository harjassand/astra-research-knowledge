import sympy as s,itertools,json,hashlib
from pathlib import Path
p=Path(__file__).parent;src=p.parent/'eb_resolvent_actual_prior_20261029'
for mn in ['SUPPORT_SHA256SUMS.txt','TNI_SALVAGE_SHA256SUMS.txt']:
 for ln in (src/mn).read_text().splitlines():
  h,f=ln.split(maxsplit=1);assert hashlib.sha256((src/f.lstrip('*')).read_bytes()).hexdigest()==h
K=s.diag(s.Rational(4,5),s.Rational(3,5));eff=s.eye(2)-K*K;plus=s.ones(2,2)/2;tau=s.diag(1,0)
def smat(fn):
 cols=[]
 for j in range(2):
  for i in range(2):
   e=s.zeros(2);e[i,j]=1;z=fn(e);cols.append(s.Matrix([z[0,0],z[1,0],z[0,1],z[1,1]]))
 return s.Matrix.hstack(*cols)
R=smat(lambda x:K*x*K);E=smat(lambda x:s.trace(eff*x)*plus);Psi=E+R;assert R*E!=E*R
tr=s.Matrix([[1,0,0,1]]);assert tr*Psi==tr
positivitychecks=0
for m in range(1,9):
 Rm=R**m;effect=tr*Rm
 rep=s.Matrix([1,0,0,0])*effect;B=Psi**m-Rm+rep;assert tr*B==tr
 C=s.zeros(4)
 for i,j in itertools.product(range(2),repeat=2):
  v=B[:,i+2*j];block=s.Matrix([[v[0],v[2]],[v[1],v[3]]])/2
  for a,b in itertools.product(range(2),repeat=2):C[2*i+a,2*j+b]=block[a,b]
 PT=s.zeros(4)
 for i,j,a,b in itertools.product(range(2),repeat=4):PT[2*i+b,2*j+a]=C[2*i+a,2*j+b]
 for mat in [C,PT]:
  for n in range(1,5):
   for inds in itertools.combinations(range(4),n):assert mat.extract(inds,inds).det()>=0;positivitychecks+=1
 assert max(effect)==s.Rational(16,25)**m
out={'manifests_verified':True,'exact_noncommuting_quantum_event':True,'event_lower_effect':'9/25','depths':8,'exact_principal_minor_checks_Choi_and_PPT':positivitychecks,'CPTP_completion_all_depths':'pass','residual_effect_norm':'(16/25)^m','scope':'Exact rational finite-depth quantum-channel check; general CP-word proof governs.'}
(p/'TNI_INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
