#!/usr/bin/env python3
"""Residual channel/candidate-library fixtures. No acquired source outcomes."""
from pathlib import Path
import runpy,json,hashlib,itertools
import numpy as np
import sympy as s
base=Path(__file__).parent
f=runpy.run_path(str(base/'ordinary_unknown_axis_positive_bloch_whitening_20261028.py'))
I=np.eye(2);P=[np.array(v,dtype=complex) for v in f['P']];P0=[I]+P
V=np.array(f['V'],dtype=complex);rho=V@np.kron(np.array(f['rho0'],complex),np.array(f['rho1'],complex))@V.conj().T
trueS=[np.array(f['t0'],float),np.array(f['t1'],float)]
trueT=[]
for i,rr in enumerate([f['rho0'],f['rho1']]):trueT.append(np.array([s.trace(pp*rr) for pp in f['P']],float))
def choi(T,t):
 J=np.eye(4,dtype=complex)
 for a in range(3):
  J+=t[a]*np.kron(P[a],I)
  for b in range(3):J+=T[a,b]*np.kron(P[a],P[b].T)
 return J/4
def affine(J):
 T=np.array([[np.trace(J@np.kron(P[a],P[b].T)).real for b in range(3)] for a in range(3)])
 t=np.array([np.trace(J@np.kron(P[a],I)).real for a in range(3)])
 return T,t
def apply1(M,T,t):
 a=np.trace(M)/2;out=a*(I+sum(t[j]*P[j] for j in range(3)))
 for j in range(3):out+=np.trace(P[j]@M)/2*sum(T[k,j]*P[k] for k in range(3))
 return out
def apply2(M,channels):
 out=np.zeros((4,4),complex)
 for a,b in itertools.product(range(4),repeat=2):
  out+=np.trace(np.kron(P0[a],P0[b])@M)/4*np.kron(apply1(P0[a],*channels[0]),apply1(P0[b],*channels[1]))
 return out
CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
SWAP=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],complex)
phi=np.array([1,0,0,1],complex)/np.sqrt(2)
def library_scores(channels):
 # Four fixed known encode/decode circuits; no optimized-code oracle.
 vals=[]
 for enc in [np.eye(4),SWAP,CNOT,SWAP@CNOT]:
  J=np.zeros((4,4),complex)
  for a,b in itertools.product(range(2),repeat=2):
   e=np.zeros((2,2),complex);e[a,b]=1
   inp=enc@np.kron(e,np.diag([1.,0]))@enc.conj().T
   out=enc.conj().T@apply2(inp,channels)@enc
   decoded=np.trace(out.reshape(2,2,2,2),axis1=1,axis2=3)
   J+=np.kron(decoded,e)/2
  vals.append(1-(phi.conj()@J@phi).real)
 return vals
rng=np.random.default_rng(202610282020);rows=[];selection=[]
for a in [1e-6,1e-7,1e-8]:
 acquired=[];etas=[]
 for i in range(2):
  D=[np.array(x,complex) for x in f['all_delta'][i]];B=[np.array(x,complex) for x in f['all_B'][i]]
  H=[]
  for j in range(3):
   perturb=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));perturb=(perturb+perturb.conj().T)/2;perturb/=np.linalg.norm(perturb,2)
   H.append(D[j]+a*perturb)
  G=np.array([[np.trace(x@y).real for y in H] for x in H]);ev,U=np.linalg.eigh(G);q=max(1.,np.trace(G));h=ev.min()*.999;g=12*(2*a+a*a)
  assert h>g
  W=U@np.diag(ev**-.5)@U.T;W0=np.round(W,14);u=np.linalg.norm(W0-W,2)+1e-13
  E=np.sqrt(3)*a/np.sqrt(h)+np.sqrt(3)*g/(2*(h-g)**1.5)+np.sqrt(3)*(1+a)*u
  C=[sum(H[k]*W0[k,j] for k in range(3)) for j in range(3)]
  fitted=[];delta=0
  for c in C:
   eig,vec=np.linalg.eigh(c);ell=np.min(abs(eig));assert ell>E
   fitted.append((vec*np.sign(eig))@vec.conj().T);delta=max(delta,2*E/(2*ell-E))
  vl=1e-13;lhat=sum(abs(np.linalg.eigvalsh(C[0])));el=4*E+vl
  Shat=lhat*(G@W0)
  DS=el*np.sqrt(q)+2*g/(np.sqrt(h)+np.sqrt(h-g))+(2+el)*q*u
  perturb=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));perturb=(perturb+perturb.conj().T)/2;perturb-=np.trace(perturb)*np.eye(4)/4;perturb/=np.linalg.norm(perturb,2)
  rhohat=rho+a*perturb;that=np.array([np.trace(b@rhohat).real for b in fitted]);tau=4*a+delta
  actualS=np.linalg.norm(Shat-trueS[i],2);actualt=np.max(abs(that-trueT[i]))
  assert actualS<=DS and actualt<=tau
  e=3*tau+3*np.sqrt(3)*DS
  Jhat=choi(Shat,that);Jtrue=choi(trueS[i],trueT[i]);Jphys=(Jhat+e*np.eye(4)/4)/(1+e)
  assert np.linalg.eigvalsh(Jphys).min()>-1e-12
  assert np.linalg.norm(np.trace(Jphys.reshape(2,2,2,2),axis1=0,axis2=2)-I/2)<1e-12
  normerr=np.linalg.svd(Jphys-Jtrue,compute_uv=False).sum();eta=min(1.,2.5*e/(1+e));assert normerr<=eta+1e-12
  acquired.append(affine(Jphys));etas.append(eta)
  rows.append({'known_matrix_radius':a,'input':i,'S_error_actual':actualS,'S_error_bound':DS,'translation_error_actual':actualt,'translation_error_bound':tau,'repaired_Choi_min_eigenvalue':np.linalg.eigvalsh(Jphys).min(),'normalized_Choi_trace_error':normerr,'half_diamond_upper_bound':eta})
 true_scores=library_scores(list(zip(trueS,trueT)));fit_scores=library_scores(acquired);chosen=int(np.argmin(fit_scores));Eta=min(1.,sum(etas))
 assert max(abs(np.array(true_scores)-np.array(fit_scores)))<=Eta+1e-12
 regret=true_scores[chosen]-min(true_scores);assert regret<=2*Eta+1e-12
 selection.append({'radius':a,'four_true_library_losses':true_scores,'four_model_library_losses':fit_scores,'chosen':chosen,'actual_regret':regret,'certified_regret_bound':min(1.,2*Eta)})
# Fully rational Choi positivity/TP repair: all principal minors, not a float claim.
exact_minors=0
for idx in range(2):
 S=f['t0'] if idx==0 else f['t1'];rr=f['rho0'] if idx==0 else f['rho1'];t=s.Matrix([s.trace(p*rr) for p in f['P']])
 for a in [s.Rational(1,100),s.Rational(1,10000)]:
  Sbar=S+a*s.diag(1,-1,1);tbar=t+s.Matrix([a,-a,a]);e=9*a # 3tau+6 D_S, with tau=D_S=a.
  J=s.eye(4)
  for j in range(3):
   J+=tbar[j]*s.kronecker_product(f['P'][j],s.eye(2))
   for k in range(3):J+=Sbar[j,k]*s.kronecker_product(f['P'][j],f['P'][k].T)
  J=s.simplify((J/4+e*s.eye(4)/4)/(1+e))
  assert J.H==J
  for m in range(1,5):
   for inds in itertools.combinations(range(4),m):assert s.simplify(J.extract(inds,inds).det())>=0;exact_minors+=1
  partial=s.Matrix(2,2,lambda x,y:sum(J[2*z+x,2*z+y] for z in range(2)));assert partial==s.eye(2)/2
out={'status':'PASS_RESIDUAL_CHANNEL_AND_FINITE_LIBRARY_FIXTURES','source_outcomes':0,'actual_calibration_not_executed':True,'known_matrix_perturbation_cases':rows,'four_candidate_library_cases':selection,'exact_rational_PSD_principal_minors':exact_minors,'scope':'exact rational repair and floating known-matrix confidence/model-selection checks, not acquired source data, hardware, generic code optimization or a continuing-memory model','sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_suffix('.md'),base/'ordinary_unknown_axis_positive_bloch_whitening_20261028.md',base/'local_noise_polar_identifiability_extension_20261028.md']}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
