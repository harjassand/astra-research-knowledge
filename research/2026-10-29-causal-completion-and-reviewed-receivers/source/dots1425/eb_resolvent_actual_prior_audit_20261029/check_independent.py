import numpy as np,sympy as sp,json,hashlib
from pathlib import Path
p=Path(__file__).parent;src=p.parent/'eb_resolvent_actual_prior_20261029'
for ln in (src/'SHA256SUMS.txt').read_text().splitlines():
 if ln.strip():
  h,f=ln.split(maxsplit=1);assert hashlib.sha256((src/f.lstrip('*')).read_bytes()).hexdigest()==h
E=sp.Matrix([[sp.Rational(1,2),sp.Rational(3,4)],[0,0]]);Q=sp.Matrix([[0,0],[sp.Rational(1,2),sp.Rational(1,4)]]);left=(sp.eye(2)-Q).inv()*E;right=E*(sp.eye(2)-Q).inv()
assert list(sp.ones(1,2)*left)==[sp.Rational(5,6),sp.Rational(5,4)] and sp.ones(1,2)*right==sp.ones(1,2)
rng=np.random.default_rng(1344);I=np.eye(2,dtype=complex);P=[I,np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1]).astype(complex)]
def entropy(a):
 v=np.linalg.eigvalsh((a+a.conj().T)/2);v=v[v>1e-13];return -float(v@np.log(v))
def td(a,b):return float(abs(np.linalg.eigvalsh((a-b+a.conj().T-b.conj().T)/2)).sum()/2)
def superop(fn):
 M=np.zeros((4,4),complex)
 for j in range(2):
  for i in range(2):
   e=np.zeros((2,2),complex);e[i,j]=1;M[:,i+2*j]=fn(e).reshape(4,order='F')
 return M

def onref(M,r,d):
 out=np.zeros_like(r)
 for i in range(2):
  for j in range(2):
   block=r[i*d:(i+1)*d,j*d:(j+1)*d]
   for a in range(2):
    for b in range(2):out[a*d:(a+1)*d,b*d:(b+1)*d]+=M[a+2*b,i+2*j]*block
 return out

def choi(M):
 C=np.zeros((4,4),complex)
 for i in range(2):
  for j in range(2):C[i*2:(i+1)*2,j*2:(j+1)*2]=M[:,i+2*j].reshape(2,2,order='F')/2
 return (C+C.conj().T)/2
rows=[];maxid=0;mincp=1;minppt=1;maxfixed=0
for trial in range(24):
 # Actual unital self-compatible phase-family channel, with unrelated input/output gauges.
 a=float(rng.uniform(.15,1/np.sqrt(2)));lam=[a,a,a*a];pr=np.array([1+sum(lam),1+lam[0]-lam[1]-lam[2],1-lam[0]+lam[1]-lam[2],1-lam[0]-lam[1]+lam[2]])/4
 ui=np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)))[0];uo=np.linalg.qr(rng.normal(size=(2,2))+1j*rng.normal(size=(2,2)))[0]
 lifts=[uo@z@ui for z in P];phi=lambda x:sum(w*z@x@z.conj().T for w,z in zip(pr,lifts));phiadj=lambda x:sum(w*z.conj().T@x@z for w,z in zip(pr,lifts))
 weights=np.zeros(4)
 for i,j in [(0,1),(2,3)]:weights[i]=weights[j]=min(pr[i],pr[j])
 alpha=float(sum(weights));assert abs(alpha-(1-a))<1e-12
 bb=lambda x:sum(w*z@x@z.conj().T for w,z in zip(weights/alpha,lifts));cc=lambda x:sum(w*z@x@z.conj().T for w,z in zip((pr-weights)/(1-alpha),lifts))
 d=2+trial%2;v=rng.normal(size=2*d)+1j*rng.normal(size=2*d);v/=np.linalg.norm(v);rho=np.outer(v,v.conj());sigma=np.trace(rho.reshape(2,d,2,d),axis1=1,axis2=3);nu=phi(sigma)
 sv,su=np.linalg.eigh(sigma);nv,nuu=np.linalg.eigh(nu);spj=[np.outer(su[:,i],su[:,i].conj()) for i in range(2)];npj=[np.outer(nuu[:,i],nuu[:,i].conj()) for i in range(2)];ss=(su*np.sqrt(sv))@su.conj().T;ni=(nuu*(1/np.sqrt(nv)))@nuu.conj().T
 r0=lambda x:ss@phiadj(ni@x@ni)@ss
 def rb(x):
  out=np.zeros((2,2),complex)
  for i,j,k,l in np.ndindex(2,2,2,2):
   th=(np.log(sv[i])-np.log(sv[j])-np.log(nv[k])+np.log(nv[l]))/2;kap=1 if abs(th)<1e-13 else th/np.sinh(th)
   out+=kap*spj[i]@r0(npj[k]@x@npj[l])@spj[j]
  return out
 RR=superop(rb);PH=superop(phi);EE=RR@superop(bb);DD=RR@superop(cc);PSI=RR@PH;FF=np.linalg.solve(np.eye(4)-(1-alpha)*DD,alpha*EE)
 resid=np.linalg.norm((np.eye(4)-(1-alpha)*DD)@(np.eye(4)-FF)-(np.eye(4)-PSI));maxid=max(maxid,float(resid));assert resid<1e-11
 trrow=np.array([1,0,0,1]);assert np.linalg.norm(trrow@FF-trrow)<1e-11
 CJ=choi(FF);mincp=min(mincp,float(np.linalg.eigvalsh(CJ)[0]));ppt=CJ.reshape(2,2,2,2).transpose(0,3,2,1).reshape(4,4);minppt=min(minppt,float(np.linalg.eigvalsh(ppt)[0]));assert mincp>-1e-11 and minppt>-1e-11
 fx=FF@sigma.reshape(4,order='F');maxfixed=max(maxfixed,float(np.linalg.norm(fx-sigma.reshape(4,order='F'))));assert maxfixed<1e-11
 shift=np.roll(np.eye(d),1,axis=0);phase=np.diag(np.exp(2j*np.pi*np.arange(d)/d));ens=[]
 for j,k in np.ndindex(d,d):
  U=np.kron(I,np.linalg.matrix_power(shift,j)@np.linalg.matrix_power(phase,k));ens.append(U@rho@U.conj().T)
 mean=sum(ens)/len(ens);assert np.linalg.norm(mean-np.kron(sigma,np.eye(d)/d))<1e-12
 outs=[onref(PH,r,d) for r in ens];delta=entropy(mean)-sum(entropy(r) for r in ens)/len(ens)-entropy(sum(outs)/len(outs))+sum(entropy(r) for r in outs)/len(outs)
 dist=sum(td(r,onref(FF,r,d)) for r in ens)/len(ens);assert dist<=np.sqrt(max(delta,0))/alpha+1e-11
 for r in ens[:1]:assert td(r,onref(FF,r,d))<=td(r,onref(PSI,r,d))/alpha+1e-11
 rows.append({'alpha':alpha,'reference_dimension':d,'actual_Holevo_loss':delta,'average_disturbance':dist,'bound':float(np.sqrt(max(delta,0))/alpha)})
out={'manifest_verified':True,'exact_TNI_left_column_sums':['5/6','5/4'],'exact_TNI_right_column_sums':['1','1'],'actual_universal_recovery_and_resolvent_cases':len(rows),'max_resolvent_identity_residual':maxid,'max_prior_fixed_residual':maxfixed,'minimum_choi_eigenvalue':mincp,'minimum_choi_partial_transpose_eigenvalue':minppt,'rows':rows,'scope':'Exact rational ordering obstruction and independent floating actual recovered-map/resolvent/actual-prior diagnostics; general proof analytic, no hardware.'}
(p/'INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='rows'})
