"""Exact rational/symbolic checks for the accompanying analytic proofs.
Finite checks support the identities; the general proofs are in PROOFS.md.
No novelty or external proof-validation claim is made.
"""
import json,platform,sys
from pathlib import Path
import numpy as np
import sympy as s
k,d=s.symbols('k d',positive=True)
checks=[]
def check(name,condition):
    assert bool(condition),name
    checks.append(name)
a=s.Matrix([1+d,1-d]); R=s.zeros(2); M=s.zeros(2)
for i in range(2):
 j=1-i
 R[i,j]=a[j]/a[i]
 M[i,j]=1/R[i,j]
 M[i,i]=R[i,j]+k/a[i]-2*(1+k)
expected_det=(k+2)*(k-4*(k+1)*d*d)/(1-d*d)
check('CT two-state determinant',s.factor(M.det()-expected_det)==0)
check('CT two-state trace',s.factor(s.trace(M)-(-2-2*k+(6+4*k)*d*d)/(1-d*d))==0)
K=s.zeros(2); b=s.zeros(2,1)
for i in range(2):
 j=1-i
 R_ij=a[j]/(a[j]+k)
 K[i,j]=1/((1+k)**2*R_ij)
 b[i]=k*(a[j]+k)/(1+k)**2
rho2=((1+k)**2-d*d)/((1+k)**4*(1-d*d))
check('embedded two-state spectral square',s.factor(K[0,1]*K[1,0]-rho2)==0)
v=(s.eye(2)-K).inv()*b
lim=[s.factor(s.limit(z,k,0,dir='+')) for z in v]
for i in range(2):check(f'embedded normalized second-moment limit {i}',s.factor(lim[i]-(1-d*d)/(1-2*d*d))==0)
# Triangle: original internal rate 1 along each directed edge, total 2.
a3=s.Matrix([1+d,1,1-d]);K3=s.zeros(3)
for i in range(3):
 den=sum(a3[j] for j in range(3) if j!=i)+k
 for j in range(3):
  if i!=j:K3[i,j]=den/((k+2)**2*a3[j])
expected_det3=(k+3)**2*(k*(k+2)**2-(k**3+4*k*k+7*k+4)*d*d)/((k+2)**5*(1-d*d))
check('embedded triangle determinant',s.factor((s.eye(3)-K3).det()-expected_det3)==0)
ks=s.Rational(1,10**6);ds=s.Rational(1,100)
KR=K3.subs({k:ks,d:ds})
w=s.Matrix([s.Rational(100000017,100000000),s.Rational(125006261,125000000),s.Integer(1)])
margin=KR*w-w
check('triangle exact positive Perron witness vector',all(x>0 for x in w))
check('triangle exact strict growth witness',all(x>0 for x in margin))
check('triangle exceeds sharp threshold',ds**2>ks*(ks+2)**2/(ks**3+4*ks**2+7*ks+4))
check('CT exceeds sharp threshold',ds**2>ks/(4*(1+ks)))
# Exact loop contraction for an arbitrary 3-state irreducible internal generator.
z=s.symbols('z',positive=True)
G=s.Matrix([[-3,1,2],[4,-5,1],[2,3,-5]])
fullblock=G-k*s.eye(3)
check('lumped exit transform',all(s.factor(x-k/(z+k))==0 for x in (z*s.eye(3)-fullblock).inv()*(k*s.ones(3,1))))
# K row sum expansion coefficient, tested on nonuniform irreducible rational S.
S=s.Matrix([[s.Rational(1,3),s.Rational(2,3),0],[0,s.Rational(1,4),s.Rational(3,4)],[s.Rational(2,5),0,s.Rational(3,5)]])
f=s.Matrix([2,-1,3]); aa=s.ones(3,1)+d*f
for i in range(3):
 row=(S*aa)[i]*sum(S[i,j]/aa[j] for j in range(3))
 coeff=(S*(f.applyfunc(lambda x:x*x)))[i]-(S*f)[i]**2
 check(f'general row first derivative {i}',s.diff(row,d).subs(d,0)==0)
 check(f'general row second derivative {i}',s.factor(s.diff(row,d,2).subs(d,0)/2-coeff)==0)
result={'exact_checks_passed':len(checks),'checks':checks,
 'triangle_rational_witness':[str(x) for x in w],
 'triangle_exact_growth_margin':[str(x) for x in margin],
 'triangle_float_spectral_radius':float(max(np.linalg.eigvals(np.array(KR,float)).real)),
 'CT_float_spectral_abscissa':float(max(np.linalg.eigvals(np.array(M.subs({k:ks,d:ds}),float)).real)),
 'two_state_clock_marginalized_normalized_second_moment':[float(x.subs({k:ks,d:ds})) for x in v],
 'kappa':str(ks),'relative_h_error':str(ds),'rarity_p_example':'1/1000000000000'}
Path('algebra_checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
