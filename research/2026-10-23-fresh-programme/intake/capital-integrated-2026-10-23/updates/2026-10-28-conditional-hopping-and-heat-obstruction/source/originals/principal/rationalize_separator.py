from pathlib import Path
import runpy,json
import numpy as np
import sympy as S
OUT=Path(__file__).parent
ns=runpy.run_path(str(OUT/'build_interfaces.py'))
ON=ns['O']*ns['N']; rr,piv=ON.T.rref();free=[j for j in range(210) if j not in piv]
d=np.load(OUT/'interfaces.npz');cand=np.load(OUT/'symmetric_0.npz')
lam=-d['D'].T@d['Ti'].T@cand['dual'];lam/=np.linalg.norm(lam)
xp=ns['xpairs'];zp=ns['zpairs'];cov=np.zeros((6,6),int)
for h in [0,3]:cov[h:h+3,h:h+3]=[[3,0,1],[0,1,0],[1,0,3]]
interior=np.array([(1 if i==j else 0)*cov[k,l] for i,j in xp for k,l in zp],float)
lam+=1e-4*interior
exact=S.zeros(210,1)
for j in free:exact[j]=S.Rational(round(lam[j]*10**8),10**8)
for i,j in enumerate(piv):exact[j]=-sum(rr[i,k]*exact[k] for k in free)
assert ON.T*exact==S.zeros(45,1)
lookup={(i,j,k,l):21*h+m for h,(i,j) in enumerate(xp) for m,(k,l) in enumerate(zp)}
Z=S.zeros(24)
for i in range(24):
 for j in range(24):
  a,b=sorted((i//6,j//6));c,e=sorted((i%6,j%6));Z[i,j]=exact[lookup[a,b,c,e]]
L,DD=Z.LDLdecomposition(hermitian=False)
assert L*DD*L.T==Z and all(t>0 for t in DD.diagonal())
p=S.Matrix([1,1,16,-13,0,0,4,-4,0]);basis=ns['basis']
Ef=ns['coeff'](ns['diss'](sum(v*f for v,f in zip(p,basis))))
Ed=ns['coeff'](ns['diss'](ns['q']**2))
pair=(exact.T*Ef)[0];minor=(exact.T*Ed)[0]
assert pair<0 and minor>=0
x=ns['x'];a,b,c,e=x;s,t=ns['s'],ns['t'];F=sum(v*f for v,f in zip(p,basis))
ac=S.expand(s*s*S.diff(F,a,a)+2*s*t*S.diff(F,a,b)+t*t*S.diff(F,b,b))
M11=S.hessian(ac.coeff(s,2).coeff(t,0),x)/2
M12=S.hessian(ac.coeff(s,1).coeff(t,1),x)/4
M22=S.hessian(ac.coeff(s,0).coeff(t,2),x)/2
ks=[1,0,0,0,0,15];K=S.zeros(4)
for (i,j),v in zip(ns['formpairs'],ks):K[i,j]=v;K[j,i]=-v
Q=M11.row_join(M12+K).col_join((M12-K).row_join(M22));_,LD=Q.LDLdecomposition(hermitian=False)
assert all(v>0 for v in LD.diagonal())
result={'p':[str(v) for v in p],'acoustic_skew':[str(v) for v in ks],'lambda_xpair_zpair':[str(v) for v in exact],'pair_F':str(pair),'pair_det2':str(minor),'dual_ldl_diagonal':[str(v) for v in DD.diagonal()],'acoustic_ldl_diagonal':[str(v) for v in LD.diagonal()]}
(OUT/'EXACT_HEAT_SEPARATOR.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'exact_status':'PASS','pair_F':str(pair),'pair_det2':str(minor),'dual_min_eigenvalue_diagnostic':float(np.linalg.eigvalsh(np.array(Z,float))[0])}),flush=True)
