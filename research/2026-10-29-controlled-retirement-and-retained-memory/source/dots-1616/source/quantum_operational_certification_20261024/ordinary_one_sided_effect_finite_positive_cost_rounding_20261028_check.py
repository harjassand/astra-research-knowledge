from pathlib import Path
from fractions import Fraction as F
import hashlib,json,math
import numpy as np
rng=np.random.default_rng(203441)
def cm(k):return rng.normal(size=(k,k))+1j*rng.normal(size=(k,k))
def he(a):return (a+a.conj().T)/2
def tr(a):return np.trace(a).real
errs={'component_reconstruction':0.,'cross_parity':0.,'rational_rotation_unitarity':0.,'Jacobi_energy_slack_violation':0.}
counts={'covariance_cases':0,'components':0,'favorable_actual_effect_checks':0,'exact_quaternion_cases':0,'rational_Jacobi_steps':0}
min_psd=0.
# Exact rational quaternion parametrization, plus actual gap-free Jacobi energy diagnostics.
for j in range(120):
 t=[F(int(v),32) for v in rng.integers(-16,17,3)]
 r=sum(x*x for x in t);v=[(1-r)/(1+r)]+[2*x/(1+r) for x in t]
 assert sum(x*x for x in v)==1
 counts['exact_quaternion_cases']+=1
for k in range(2,7):
 for eta in [.02,.07,.125]:
  X=cm(k);rho=X@X.conj().T;rho*=.45/np.linalg.norm(rho,2)
  dctrl=eta**2/(128*k**3)
  bits=math.ceil(math.log2(100/dctrl));den=2**bits
  N=k*k*math.ceil(math.log2(32*k/eta**2))
  for step in range(N):
   off=rho-np.diag(np.diag(rho));E=np.linalg.norm(off,'fro')**2
   if E<=eta**2/16:break
   i,j=np.unravel_index(np.argmax(np.abs(off)),off.shape)
   if i>j:i,j=j,i
   _,u=np.linalg.eigh(rho[np.ix_([i,j],[i,j])]);u[:,1]/=np.linalg.det(u)
   # SU2 form [[a,b],[-b*,a*]], scalar quaternion coordinate nonnegative.
   if u[0,0].real<0:u=-u
   q=np.array([u[0,0].real,u[0,0].imag,u[0,1].real,u[0,1].imag])
   tt=q[1:]/(1+q[0]);t=[F(round(float(v)*den),den) for v in tt]
   rr=sum(v*v for v in t);qq=[(1-rr)/(1+rr)]+[2*v/(1+rr) for v in t]
   assert sum(v*v for v in qq)==1
   a=complex(float(qq[0]),float(qq[1]));b=complex(float(qq[2]),float(qq[3]));uv=np.array([[a,b],[-b.conjugate(),a.conjugate()]])
   assert np.linalg.norm(uv-u,2)<dctrl*1.01,(k,eta,np.linalg.norm(uv-u,2),dctrl)
   full=np.eye(k,dtype=complex);full[np.ix_([i,j],[i,j])]=uv
   rnext=he(full.conj().T@rho@full);En=np.linalg.norm(rnext-np.diag(np.diag(rnext)),'fro')**2
   errs['Jacobi_energy_slack_violation']=max(errs['Jacobi_energy_slack_violation'],En-((1-2/k**2)*E+eta**2/(64*k**2)))
   errs['rational_rotation_unitarity']=max(errs['rational_rotation_unitarity'],np.linalg.norm(uv.conj().T@uv-np.eye(2)))
   rho=rnext;counts['rational_Jacobi_steps']+=1
  assert np.linalg.norm(rho-np.diag(np.diag(rho)),'fro')<=eta/4+1e-12
# Covariance/band identities and actually returned effects; classical draws only.
for k in range(2,7):
 for case in range(16):
  gs=[he(cm(k)) for _ in range(k+2)];rho=sum(g@g for g in gs)
  fac=math.sqrt(.4/np.linalg.norm(rho,2));gs=[fac*g for g in gs];rho=sum(g@g for g in gs)
  zz=cm(k);W=zz@zz.conj().T/k;m=2.**(-(case%10))
  ops=[he(cm(k)) for _ in range(3)];a=max(1,sum(np.linalg.norm(o,'fro')**2 for o in ops))
  n=lambda A:sum(tr(o@A)**2 for o in ops)
  s=sum(n(g) for g in gs);q=tr(W@rho);delta=min(1/16,s/(64*a*k));eta=min(1/8,m/(8*(1+tr(W))))
  ev,Q=np.linalg.eigh(rho);D=ev+eta/2;bar=(Q*D)@Q.conj().T
  inds={}
  for i,v in enumerate(D):
   if v<delta:continue
   j=0
   while v<=4.**(-(j+1)):j+=1
   inds.setdefault(j,[]).append(i)
  bands=[]
  for j,ids in sorted(inds.items()):
   P=Q[:,ids]@Q[:,ids].conj().T;bands.append((4.**(-j),P))
  P=sum(p[1] for p in bands);skeep=sum(n(P@g@P) for g in gs)
  assert skeep+1e-9>=s/4
  comps=[]
  for p,Pi in bands:
   gl=[Pi@g@Pi for g in gs];si=sum(n(g) for g in gl);bi=p*(m+tr(W@Pi));comps.append(('diag',p,Pi,None,gl,si,bi,0))
  for i in range(len(bands)):
   for j in range(i+1,len(bands)):
    pi,Pi=bands[i];pj,Pj=bands[j]
    if pi>pj:pi,pj,Pi,Pj=pj,pi,Pj,Pi
    gl=[Pi@g@Pj for g in gs];si=sum(n(g+g.conj().T) for g in gl);t=sum(tr(W@g@g.conj().T) for g in gl)
    bi=pj*m+2*pj*tr(W@Pj)+48*t;comps.append(('off',pj,Pi,Pj,gl,si,bi,t))
  ell=len(bands);K=ell*(ell+1)//2;qb=tr(W@bar)
  assert sum(c[6] for c in comps)<=(8*ell+56)*(m+qb)+1e-8
  assert max(c[5]/c[6] for c in comps)+1e-9>= (s/(m+q))/(8*K*(8*ell+56))
  for z,g in enumerate(gs):
   rec=sum((c[4][z] if c[0]=='diag' else c[4][z]+c[4][z].conj().T) for c in comps)
   errs['component_reconstruction']=max(errs['component_reconstruction'],np.linalg.norm(rec-P@g@P))
  R0=2*math.ceil(math.sqrt(math.ceil(math.log2(192*max(2,k)))))
  for typ,p,Pi,Pj,gl,si,bi,t in comps:
   counts['components']+=1
   for trial in range(4):
    G=sum(z*g for z,g in zip(rng.normal(size=len(gl)),gl))
    numerator=n(G if typ=='diag' else G+G.conj().T)
    favorable=numerator>=si/2 and np.linalg.norm(G,2)<=R0*math.sqrt(p)
    if typ=='off':favorable=favorable and tr(W@G@G.conj().T)<=48*t+1e-12
    if not favorable:continue
    if typ=='diag':
     T=G/(2*R0*math.sqrt(p));outs=[(Pi+T)/2,(Pi-T)/2]
    else:
     B=G/(4*R0*math.sqrt(p));base=2*B@B.conj().T+Pj-2*B.conj().T@B;outs=[base+B+B.conj().T,base-B-B.conj().T]
    for A in outs:
     min_psd=min(min_psd,np.linalg.eigvalsh(he(A)).min(),np.linalg.eigvalsh(np.eye(k)-he(A)).min())
    ratio=max(n(A)/(m+tr(W@A)) for A in outs)
    assert ratio+1e-9>=si/(256*R0**2*bi)
    counts['favorable_actual_effect_checks']+=1
  counts['covariance_cases']+=1
assert max(errs.values())<1e-10,errs
assert min_psd>-1e-10,min_psd
source=Path(__file__).with_name('ordinary_one_sided_effect_finite_positive_cost_rounding_20261028.md')
out={'status':'PASS author identities and finite-operation diagnostics; independent receiving pending','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'counts':counts,'max_residuals':errs,'minimum_effect_slack':min_psd,'source_calls':0,'scope':'Classical seeded matrices and Gaussian draws only; no quantum source records or executed SDP. Local rational rotations are exactly unitary by Fraction identities; matrix replay uses floating point and does not itself certify a production arbitrary-precision compiler. Does not estimate or claim empirical confidence probabilities.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
