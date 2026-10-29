"""Independent coherent-channel objective, estimator moments, Naimark and ceiling tests."""
from pathlib import Path
import numpy as np,json,hashlib,itertools
from scipy.linalg import null_space
D=Path(__file__).parent;A=D.parent
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);P=[I,X,Y,Z]
rng=np.random.default_rng(202610282340)
def sqrtm(M):
 w,v=np.linalg.eigh((M+M.conj().T)/2);return (v*np.sqrt(np.maximum(w,0)))@v.conj().T
def povm(m,r):
 rows=[]
 for _ in range(m):a=rng.normal(size=(r,r))+1j*rng.normal(size=(r,r));rows.append(a@a.conj().T)
 S=sum(rows);w,v=np.linalg.eigh(S);inv=(v/np.sqrt(w))@v.conj().T
 return [inv@a@inv for a in rows]
def source_ks(d=2,r=2,count=3):
 a=rng.normal(size=(d*r*count,d))+1j*rng.normal(size=(d*r*count,d));v=np.linalg.qr(a)[0];return [v[d*r*j:d*r*(j+1)] for j in range(count)]
phi=np.array([1,0,0,1],complex)/np.sqrt(2);bell=[np.kron(I,p)@phi for p in P]
maxobjective=0.;maxmoment=0.;maxsecond=0.;maxcompile=0.;ceiling_excess=-1.
for trial in range(80):
 Ks=source_ks();J=sum(np.outer(k.reshape(2,2,2).transpose(2,0,1).reshape(8),k.reshape(2,2,2).transpose(2,0,1).reshape(8).conj())/2 for k in Ks)
 sig=[]
 for v in bell:
  B=np.kron(v.reshape(1,4),I);sig.append(B.conj()@J@B.T)
 assert abs(sum(np.trace(s).real for s in sig)-1)<1e-12
 effects=povm(4,2);dk=[]
 for p,M in zip(P,effects):
  sq=sqrtm(M)
  for j in range(2):dk.append(np.kron(p,sq[j:j+1,:]))
 direct=sum(abs(np.trace(d@k))**2 for d in dk for k in Ks)/4
 obj=sum(np.trace(M@s).real for M,s in zip(effects,sig));maxobjective=max(maxobjective,abs(direct-obj));assert abs(direct-obj)<1e-12
 # Check actual estimator mean and square by exhausting Pauli setting/outcomes.
 for s0 in sig:
  ey=np.zeros((2,2),complex);ey2=np.zeros((2,2),complex);p0=np.trace(s0).real
  for W in P:
   for b in [-1,1]:
    prob=np.trace((I+b*W)@s0).real/8
    # For identity the impossible outcome automatically has zero probability.
    YY=2*b*W;ey+=prob*YY;ey2+=prob*(YY@YY)
  maxmoment=max(maxmoment,float(np.max(abs(ey-s0))));maxsecond=max(maxsecond,float(np.max(abs(ey2-4*p0*I))));assert np.max(abs(ey-s0))<1e-12 and np.max(abs(ey2-4*p0*I))<1e-12
 # Explicit known Naimark completion, actual outcome blocks reconstruct each effect.
 V=np.vstack([sqrtm(M) for M in effects]);U=np.column_stack([V,null_space(V.conj().T)]);assert np.max(abs(U.conj().T@U-np.eye(8)))<1e-12
 for j,M in enumerate(effects):maxcompile=max(maxcompile,float(np.max(abs(U[2*j:2*j+2,:2].conj().T@U[2*j:2*j+2,:2]-M))))
 priors=sorted([np.trace(s).real for s in sig],reverse=True);ceiling_excess=max(ceiling_excess,obj-sum(priors[:2]));assert obj<=sum(priors[:2])+1e-12
# Sharp top-r prior fixture with two orthogonal flag states.
priors=[.4,.3,.2,.1];flags=[np.diag([1,0]),np.diag([0,1]),I/2,I/2];effects=[flags[0],flags[1],np.zeros((2,2)),np.zeros((2,2))]
assert abs(sum(p*np.trace(M@t).real for p,M,t in zip(priors,effects,flags))-.7)<1e-15
# Explicit coherent source counterexample: H unitary corrected perfectly before twirl.
H=(X+Z)/np.sqrt(2);weights=[abs(np.trace(p@H)/2)**2 for p in P];assert np.max(abs(np.array(weights)-[0,.5,0,.5]))<1e-15
# General-r Pauli flag moments r4 with arbitrary subnormalized quantum state.
paulis4=[np.kron(p,q) for p in P for q in P];a=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));sigma=a@a.conj().T;sigma*=.23/np.trace(sigma);E=np.zeros((4,4),complex);E2=np.zeros((4,4),complex)
for W in paulis4:
 for b in [-1,1]:
  prob=np.trace((np.eye(4)+b*W)@sigma).real/32;Y0=4*b*W;E+=prob*Y0;E2+=prob*Y0@Y0
assert np.max(abs(E-sigma))<1e-12 and np.max(abs(E2-16*.23*np.eye(4)))<1e-12
files=[A/'COMPACT_QUANTUM_FLAG_RECOVERY_v1.md',A/'check_compact_geometry_v1.py',A/'check_compact_geometry_v1.json',Path(__file__)]
out={'status':'PASS_INDEPENDENT_COMPACT_MECHANISM_CHECKS','general_coherent_sources':80,'full_channel_vs_Bell_block_objective_max_error':maxobjective,'qubit_estimator_mean_max_error':maxmoment,'qubit_estimator_second_moment_max_error':maxsecond,'Naimark_effect_reconstruction_max_error':maxcompile,'top_r_ceiling_max_excess':ceiling_excess,'r4_estimator_moments_pass':True,'coherent_H_twirl_loss_pass':True,'new_acquisition_calls':0,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(D/'check_compact_mechanism_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
