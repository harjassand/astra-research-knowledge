#!/usr/bin/env python3
"""Read/recompute SAVED large-bank artifacts only. Never calls acquisition main.
Exact source-CDF, seeded record replay, rational fit certificate, saved-model scores.
"""
from pathlib import Path
import json,hashlib,itertools,math
import numpy as np
import sympy as s
from scipy.linalg import expm
D=Path(__file__).parent;Q=D.parent
plan=json.loads((D/'LARGE_BANK_PREDECLARATION.json').read_text());res=json.loads((D/'large_bank_results.json').read_text());cert=json.loads((D/'large_bank_exact_candidate_certificate.json').read_text());prob=json.loads((D/'large_bank_source_probabilities.json').read_text());counts=np.load(D/'large_bank_counts.npz')['counts'];models=np.load(D/'large_bank_models.npz')
for f,h in res['sha256'].items():
 p=D/f if (D/f).exists() else Q/f
 assert hashlib.sha256(p.read_bytes()).hexdigest()==h
N=plan['N'];den=plan['probability_CDF_denominator'];assert N==2**22 and counts.sum()==N and counts.shape==(54,4)
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);P=[X,Y,Z];k=s.kronecker_product;clean=lambda a:a.applyfunc(s.expand)
H=s.Rational(47,100)*k(X,X)+s.Rational(31,100)*k(Y,Z)+s.Rational(19,100)*k(Z,I)+s.Rational(37,100)*k(I,X)
# Independent grouped six-state Taylor calculation with separate power and factorial.
power=s.eye(4);V=s.eye(4)
for j in range(1,41):power=clean(power*(-s.I*H));V=clean(V+power/s.factorial(j))
r=s.Rational(67,50);tail=8*r**41/s.factorial(41);assert tail==s.sympify(prob['unitary_operator_error_upper'])
assert sum(s.Rational(2)**j/s.factorial(j) for j in range(7))+s.Rational(2)**7/s.factorial(7)/(1-s.Rational(1,4))<8
base=[s.diag(1,s.Rational(4,5)),s.Matrix([[0,s.Rational(3,5)],[0,0]])];R=s.Matrix([[3,-1],[1,3]]);rot=[R*a*R.T/10 for a in base];gauges=[s.diag(1,0),s.ones(2)/2]
cdfs=[];settings=list(itertools.product(range(3),[-1,1],range(3),range(3)));outs=list(itertools.product([-1,1],repeat=2));state_cache={};minp=None
for axis,sg in itertools.product(range(3),[-1,1]):
 rho=(I+sg*P[axis])/2;pre=sum((k(sum((a*rho*a.H for a in aa),s.zeros(2)),g)/2 for aa,g in zip([base,rot],gauges)),s.zeros(4));state_cache[axis,sg]=clean(V*pre*V.H)
for axis,sg,a,b in settings:
 o=state_cache[axis,sg];mass=s.expand(s.trace(o));ma=s.expand(s.trace(o*k(P[a],I)));mb=s.expand(s.trace(o*k(I,P[b])));mab=s.expand(s.trace(o*k(P[a],P[b])))
 ps=[s.cancel((mass+x*ma+y*mb+x*y*mab)/(4*mass)) for x,y in outs]
 assert sum(ps)==1 and all(v>=0 for v in ps);minp=min(ps) if minp is None else min(minp,min(ps));acc=s.S.Zero;row=[]
 for z in range(3):acc+=ps[z];row.append(int(s.floor(den*acc)))
 cdfs.append(row+[den])
assert cdfs==prob['CDF_thresholds'];assert minp==s.sympify(prob['smallest_Taylor_normalized_probability'])
TV=2*tail+tail*tail+s.Rational(3,den);assert TV==s.sympify(prob['one_block_output_TV_upper']);assert N*TV<s.Rational(plan['sampling_record_TV_budget'])
# Exact saved-RNG replay; streamed outcome draws after original full setting array.
cdf=np.array(cdfs,np.int64);rng=np.random.default_rng(plan['record_seed']);setting=rng.integers(54,size=N);replay=np.zeros(216,np.int64)
for start in range(0,N,131072):
 n=min(131072,N-start);u=rng.integers(den,size=n,dtype=np.int64);lab=setting[start:start+n];out=(u[:,None]>=cdf[lab,:3]).sum(1);replay+=np.bincount(4*lab+out,minlength=216)
assert np.array_equal(replay.reshape(54,4),counts)
# Exact shadow arithmetic directly from Pauli projectors, not floating shadow arrays.
C=[s.zeros(4) for _ in range(3)]
for row,(axis,sg,a,b) in enumerate(settings):
 for col,(x,y) in enumerate(outs):C[axis]+=s.Rational(3*sg*int(counts[row,col]),N)*k((I+3*x*P[a])/2,(I+3*y*P[b])/2)
C=[clean(a) for a in C];Cs=[s.Matrix([[s.sympify(v) for v in row] for row in a]) for a in cert['exact_signed_contrasts']];assert C==Cs
U=s.Matrix([[s.sympify(v) for v in row] for row in cert['unitary_U']]);HC=s.Matrix([[s.sympify(v) for v in row] for row in cert['Cayley_H']]);simp=lambda a:a.applyfunc(s.cancel)
assert HC.H==HC and simp(U.H*U-s.eye(4))==s.zeros(4);assert simp(U*(s.eye(4)-s.I*HC)-(s.eye(4)+s.I*HC))==s.zeros(4)
cp=[simp(U.H*a*U) for a in C];coef=[]
for a in range(3):
 row=[]
 for b in range(3):
  M=k(P[a],I)*cp[b];row.append(s.Matrix(2,2,lambda x,y:s.cancel((M[x,y]+M[x+2,y+2])/2)))
 coef.append(row)
S=[[simp((coef[a][b]+coef[b][a])/2) for b in range(3)] for a in range(3)];block=s.BlockMatrix(S).as_explicit();kap=s.Rational(plan['fixed_candidate_kappa']);M=s.MutableDenseMatrix(simp(block-kap*s.eye(6)));assert M.H==M
# Exact Schur/LDL pivots, independently of author's determinant algorithm.
pivots=[];prod=s.S.One
for j in range(6):
 pv=s.cancel(M[j,j]);assert pv.is_Rational and pv>0;pivots.append(pv);prod=s.cancel(prod*pv);assert prod==s.sympify(cert['gauge_block_leading_minors_at_fixed_kappa'][j])
 for x in range(j+1,6):
  for y in range(j+1,6):M[x,y]=s.cancel(M[x,y]-M[x,j]*M[j,y]/pv)
fit=[sum((k(P[a],S[a][b]) for a in range(3)),s.zeros(4)) for b in range(3)]
r2=s.cancel(sum(s.re(z)**2+s.im(z)**2 for a,b in zip(fit,cp) for z in simp(a-b)));assert r2==s.sympify(cert['residual_squared_exact'])
rr=s.Rational(cert['residual_upper_rational']);eta=s.Rational(cert['HS_radius_upper_rational']);beta=s.Rational(plan['beta_total']);budget=s.Rational(plan['sampling_record_TV_budget']);L=plan['joint_HS_L'];union=plan['finite_patch_bank_union_Q']
assert rr>=0 and rr*rr>=r2 and (rr-s.Rational(1,10**12))**2<r2
assert sum(s.Rational(L)**j/s.factorial(j) for j in range(60))>49*union/beta
assert eta>=0 and N*eta*eta-2*s.Rational(17*L,3)*eta-2*225*L>=0
regret=(rr+eta)**2/(8*kap);assert regret==s.Rational(cert['native_oracle_regret_upper_rational']);total=regret+beta+budget;assert total==s.Rational(cert['observed_guard_plus_failure_debits_rational']);assert total<=s.Rational(plan['target_unnormalized_accepted_native_oracle_regret'])
# Saved numerical scores via explicit Kraus receiver, with no candidate refit.
In=np.eye(2,dtype=complex);Pn=[np.array(p,complex) for p in P];Xn,Yn,Zn=Pn;Vn=expm(-1j*np.array(H,complex));Rn=np.array(R,float)/np.sqrt(10);bn=[np.array(a,complex) for a in base];gn=[np.array([[1.],[0.]]),np.array([[1.],[1.]])/np.sqrt(2)];Ks=[Vn@np.kron(a,g)/np.sqrt(2) for aa,g in zip([bn,[Rn@a@Rn.T for a in bn]],gn) for a in aa]
maxscore=0.;scored=0
for name,score in res['scores'].items():
 if name=='full_CPTP_SDP':
  J=models['SDP_Choi'];ev,vec=np.linalg.eigh((J+J.conj().T)/2);assert ev.min()>-1e-12;Ls=[np.sqrt(max(0,e))*vec[:,j].reshape(2,4) for j,e in enumerate(ev)]
 else:
  if score['abstained']:continue
  A=models[name+'_A'];AA,ZZ=A[0],A[2];q=np.kron((np.eye(4)+ZZ)/2,In)+np.kron((np.eye(4)-ZZ)/2,Xn);cx=np.kron(np.eye(4),(In+Zn)/2)+np.kron(AA,(In-Zn)/2);W=q@cx@q;Ls=[W.reshape(4,2,4,2)[x,:,:,y]/np.sqrt(2) for x in range(4) for y in range(2)]
  T=np.zeros((2,2),complex)
  for ell in Ls:
   t=np.array([np.trace(ell@Vn@np.kron(In,np.eye(2)[:,r:r+1])) for r in range(2)]);T+=np.outer(t.conj(),t)/4
  maxscore=max(maxscore,abs(1-np.linalg.eigvalsh(T).min()-score['worst_gauge_inverse_Bell_loss']))
 loss=1-sum(abs(np.trace(ell@kk))**2 for ell in Ls for kk in Ks)/4;maxscore=max(maxscore,abs(loss-score['native_Bell_loss']));scored+=1
assert maxscore<1e-12
out={'status':'PASS_EXACT_NOMINAL_NATIVE_ORACLE_CERTIFICATE_AND_SAVED_RECORD_AUDIT','source_blocks_replayed':N,'fresh_acquisition_during_review':0,'one_predeclared_bank':True,'exact_CDF_thresholds_recomputed':216,'raw_counts_replayed_exactly':True,'rational_Cayley_unitarity_exact':True,'exact_positive_LDL_pivots':6,'fixed_kappa':str(kap),'exact_residual_squared_reproduced':True,'residual_upper':float(rr),'joint_HS_radius':float(eta),'observed_good_event_native_regret_bound':float(regret),'observed_guard_plus_failure_debits':float(total),'predeclared_joint_accepted_mean_bound':plan['target_unnormalized_accepted_native_oracle_regret'],'sampling_record_TV_upper_float':float(N*TV),'saved_model_methods_rescored':scored,'max_saved_model_score_difference':float(maxscore),'uniform_inverse_error_bound_not_target':float(2*(rr+eta)/kap),'scope':'Exact rational model/statistical guard under the stated ideal-control stationary source experiment, with finite source-CDF record-TV debit. Not posterior confidence, actual gate compilation, hardware, or a successful uniform inverse certificate.','sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [Path(__file__),D/'LARGE_BANK_PREDECLARATION.json',D/'large_bank_results.json',D/'large_bank_counts.npz',D/'large_bank_models.npz',D/'large_bank_exact_candidate_certificate.json',D/'large_bank_source_probabilities.json']}}
(D/'large_bank_independent_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
