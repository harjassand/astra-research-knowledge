"""Finite-ensemble checks for the explicit PPT qubit-concurrence deficit."""
from pathlib import Path
import json
import numpy as np
rng=np.random.default_rng(633792)
tol=2e-9

def gin(n,m):return rng.normal(size=(n,m))+1j*rng.normal(size=(n,m))
def pt(a,d):return a.reshape(2,d,2,d).transpose(2,1,0,3).reshape(2*d,2*d)
def redb(a,d):return np.einsum('aiaj->ij',a.reshape(2,d,2,d))
def reda_vector(v,d):
 z=v.reshape(2,d);return z@z.conj().T

def conc(v,d):return 2*np.sqrt(max(0,float(np.linalg.det(reda_vector(v,d)).real)))
def normf2(a):return float(np.vdot(a,a).real)

def check(a,d,label):
 a=(a+a.conj().T)/2;a/=np.trace(a)
 lam,U=np.linalg.eigh(a)
 assert lam.min()>-tol and np.linalg.eigvalsh(pt(a,d)).min()>-tol
 mask=lam>1e-11;lam=lam[mask];V=U[:,mask]*np.sqrt(lam);r=len(lam)
 cs=np.array([conc(V[:,i],d) for i in range(r)])
 deficit0=1-cs.sum();Dmax=deficit0;which='spectral'
 R=[[V[:,i].reshape(2,d)@V[:,j].reshape(2,d).conj().T for j in range(r)] for i in range(r)]
 B=[R[i][i]-lam[i]*np.eye(2)/2 for i in range(r)]
 assert sum(normf2(B[i])/lam[i] for i in range(r))<=deficit0+tol
 max_pair_error=0
 for i in range(r):
  for j in range(i+1,r):
   total=lam[i]+lam[j]
   for phase in [1,1j]:
    vp=(V[:,i]+phase*V[:,j])/np.sqrt(2)
    vm=(V[:,i]-phase*V[:,j])/np.sqrt(2)
    assert abs(np.vdot(vp,vp).real-total/2)<tol
    assert abs(np.vdot(vm,vm).real-total/2)<tol
    deficit=1-(cs.sum()-cs[i]-cs[j]+conc(vp,d)+conc(vm,d))
    cross=R[i][j]+R[j][i] if phase==1 else 1j*(R[j][i]-R[i][j])
    assert normf2(cross)<=total*deficit+tol
    if deficit>Dmax:Dmax=deficit;which=f'{i},{j},phase={phase}'
   H=R[i][j]+R[j][i];K=1j*(R[j][i]-R[i][j])
   max_pair_error=max(max_pair_error,abs(normf2(H)+normf2(K)-4*normf2(R[i][j])))
 delta2=sum(normf2(B[i]) for i in range(r))+sum(normf2(R[i][j]) for i in range(r) for j in range(r) if i!=j)
 pb=normf2(redb(a,d));pab=normf2(a)
 assert abs(delta2-(pb-pab/2))<tol
 assert pab<=pb+tol
 assert delta2>=1/(2*d)-tol
 upper=Dmax*(r-1+max(lam))
 assert delta2<=upper+tol
 assert Dmax>=1/(2*d*r)-tol
 assert 1-Dmax<=1-1/(4*d*d)+tol
 return {'d':d,'rank':r,'family':label,'tested_ensembles':1+r*(r-1),'best_deficit':float(Dmax),'rank_sensitive_guarantee':1/(2*d*r),'purification_defect_squared':delta2,'purity_lower_bound':1/(2*d),'pair_upper_bound':float(upper),'best_ensemble':which,'max_pair_identity_error':max_pair_error}

cases=[]
for d in [2,3,4,5,8]:
 for rep in range(3):
  z=gin(2*d,2*d);a=z@z.conj().T
  a+=(max(0,-np.linalg.eigvalsh(pt(a,d))[0])+0.2)*np.eye(2*d)
  cases.append(check(a,d,'positive-partial-transpose random shift'))
 for k in [1,2,min(d,4),min(2*d,7)]:
  a=np.zeros((2*d,2*d),complex)
  for j in range(k):
   x=gin(2,1).ravel();y=gin(d,1).ravel();v=np.kron(x,y)
   a+=np.outer(v,v.conj())
  cases.append(check(a,d,f'product mixture with {k} terms'))
# The entries below supply a 2x4 PPT test family. Only positivity and PPT are asserted here.
for b in [.05,.2,.5,.8]:
 a=np.zeros((8,8));a[np.diag_indices(8)]=[b,b,b,b,(1+b)/2,b,b,(1+b)/2]
 for i,j in [(0,5),(1,6),(2,7)]:a[i,j]=a[j,i]=b
 a[4,7]=a[7,4]=np.sqrt(1-b*b)/2
 cases.append(check(a,4,f'2x4 PPT matrix b={b}'))
report={'status':'PASS','seed':633792,'absolute_tolerance':tol,'cases':cases,'total_ensembles':sum(c['tested_ensembles'] for c in cases),'scope':'Checks the finite weighted-ensemble inequalities and purity identity, not an optimal convex-roof computation.'}
Path(__file__).with_name('explicit_concurrence_gap_verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','cases':len(cases),'total_ensembles':report['total_ensembles'],'smallest_observed_deficit':min(c['best_deficit'] for c in cases),'largest_pair_identity_error':max(c['max_pair_identity_error'] for c in cases)},indent=2))
