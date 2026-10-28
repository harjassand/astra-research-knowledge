#!/usr/bin/env python3
"""Predeclared single fresh large bank with exact source-CDF and rational receiver certificate.
Run only after independent HS confidence receipt. No automatic budget retry.
"""
from pathlib import Path
import json,hashlib,importlib.util,itertools,math,time
from fractions import Fraction
import numpy as np
import sympy as s
HERE=Path(__file__).parent;Q=HERE.parent
spec=importlib.util.spec_from_file_location('pilot',HERE/'run_pilot.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
I=s.eye(2);P=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
kron=s.kronecker_product

def exact_source_cdf(degree=40,denom=2**52):
 H=s.Rational(47,100)*kron(P[0],P[0])+s.Rational(31,100)*kron(P[1],P[2])+s.Rational(19,100)*kron(P[2],I)+s.Rational(37,100)*kron(I,P[0])
 V=s.eye(4);term=s.eye(4)
 for k in range(1,degree+1):term=term*(-s.I*H)/k;V+=term
 V=V.applyfunc(s.expand)
 r=s.Rational(67,50);tail=8*r**(degree+1)/s.factorial(degree+1)
 assert sum((s.Rational(2)**k/s.factorial(k) for k in range(7)),s.S.Zero)+(s.Rational(2)**7/s.factorial(7))/(1-s.Rational(1,4))<8
 R=s.Matrix([[3,-1],[1,3]]);K0=[s.diag(1,s.Rational(4,5)),s.Matrix([[0,s.Rational(3,5)],[0,0]])];K1=[R*k*R.T/10 for k in K0]
 p0=s.diag(1,0);pp=s.ones(2)/2;tables=[];minprob=None
 for axis,sg,ma,mb in p.SETTINGS:
  rho=(I+sg*P[axis])/2
  q0=sum((k*rho*k.H for k in K0),s.zeros(2));q1=sum((k*rho*k.H for k in K1),s.zeros(2))
  out=V*(kron(q0,p0)+kron(q1,pp))*V.H/2
  probs=[]
  for a,b in p.OUTCOMES:
   val=s.expand(s.trace(out*kron((I+a*P[ma])/2,(I+b*P[mb])/2)))
   assert val.is_Rational and val>=0;probs.append(val)
  mass=sum(probs);assert mass>0;probs=[v/mass for v in probs]
  minprob=min(probs) if minprob is None else min(minprob,min(probs))
  cumulative=[];v=0
  for k in range(3):v+=probs[k];cumulative.append(int(s.floor(v*denom)))
  cumulative.append(denom);assert sorted(cumulative)==cumulative
  tables.append(cumulative)
 deviation=2*tail+tail*tail+s.Rational(3,denom)
 return np.array(tables,dtype=np.int64),{'degree':degree,'CDF_denominator':denom,'unitary_operator_error_upper':str(tail),'one_block_output_TV_upper':str(deviation),'smallest_Taylor_normalized_probability':str(minprob),'CDF_thresholds':tables},deviation

def exact_contrasts(counts):
 N=int(counts.sum());ints=[[[0j for _ in range(4)] for _ in range(4)] for _ in range(3)]
 nr=np.zeros((3,4,4),dtype=np.int64);ni=np.zeros((3,4,4),dtype=np.int64)
 for t,(axis,sg,_,_) in enumerate(p.SETTINGS):
  for out in range(4):
   M=4*p.SHADOWS[t,out];re=np.rint(M.real).astype(np.int64);im=np.rint(M.imag).astype(np.int64)
   assert np.max(abs(M.real-re))+np.max(abs(M.imag-im))==0
   nr[axis]+=int(counts[t,out])*3*sg*re;ni[axis]+=int(counts[t,out])*3*sg*im
 return [s.Matrix(4,4,lambda a,b:s.Rational(int(nr[j,a,b]),4*N)+s.I*s.Rational(int(ni[j,a,b]),4*N)) for j in range(3)]

def rational_candidate_from_sdp(J,denom=2**24):
 images=[np.einsum('ba,axby->xy',q,J.reshape(2,4,2,4)).T for q in p.P];images=[(a+a.conj().T)/2 for a in images]
 X=p.sign(images[0]);odd=(images[2]-X@images[2]@X)/2
 if np.min(abs(np.linalg.eigvalsh(odd)))<1e-8:raise RuntimeError('Predeclared rounding gap failed: ABSTAIN')
 Z=p.sign(odd);ev,vec=np.linalg.eigh(Z);plus=vec[:,ev>0]
 if plus.shape[1]!=2:raise RuntimeError('Predeclared balanced rounding failed: ABSTAIN')
 U=np.column_stack([plus,X@plus])
 phases=[np.exp(2j*np.pi*k/5) for k in range(5)];phase=max(phases,key=lambda z:np.linalg.svd(np.eye(4)+z*U,compute_uv=False).min());U=phase*U
 HH=-1j*(U-np.eye(4))@np.linalg.inv(U+np.eye(4));HH=(HH+HH.conj().T)/2
 R=s.zeros(4)
 for a in range(4):
  R[a,a]=s.Rational(int(np.rint(HH[a,a].real*denom)),denom)
  for b in range(a+1,4):
   R[a,b]=s.Rational(int(np.rint(HH[a,b].real*denom)),denom)+s.I*s.Rational(int(np.rint(HH[a,b].imag*denom)),denom);R[b,a]=s.conjugate(R[a,b])
 Uq=((s.eye(4)+s.I*R)*(s.eye(4)-s.I*R).inv()).applyfunc(s.cancel)
 assert (Uq.H*Uq-s.eye(4)).applyfunc(s.cancel)==s.zeros(4)
 return Uq,R

def exact_fit(U,C,kappa):
 cp=[(U.H*c*U).applyfunc(s.cancel) for c in C]
 raw=[]
 for k in range(3):
  row=[]
  for j in range(3):
   m=kron(P[k],I)*cp[j]
   row.append(s.Matrix(2,2,lambda a,b:s.cancel(sum(m[2*z+a,2*z+b] for z in range(2))/2)))
  raw.append(row)
 S=[[(raw[k][j]+raw[j][k])/2 for j in range(3)] for k in range(3)]
 S=[[x.applyfunc(s.cancel) for x in row] for row in S]
 block=s.BlockMatrix(S).as_explicit();assert (block.H-block).applyfunc(s.cancel)==s.zeros(6)
 minors=[s.cancel((block-kappa*s.eye(6))[:k,:k].det(method='domain-ge')) for k in range(1,7)]
 fit=[sum((kron(P[k],S[k][j]) for k in range(3)),s.zeros(4)) for j in range(3)]
 r2=s.cancel(sum(s.trace((f-c).H*(f-c)) for f,c in zip(fit,cp)));assert r2.is_Rational and r2>=0
 return all(v>0 for v in minors),r2,{'gauge_block_leading_minors_at_fixed_kappa':[str(v) for v in minors],'residual_squared_exact':str(r2)}

def sqrt_upper(r,den=10**12):
 # Exact integer square root gives an outward rational bound, no floating certification.
 num=int(s.numer(r));dd=int(s.denom(r));a=math.isqrt((num*den*den)//dd)
 while s.Rational(a,den)**2<r:a+=1
 return s.Rational(a,den)

def main():
 plan=json.loads((HERE/'LARGE_BANK_PREDECLARATION.json').read_text());N=plan['N'];beta=s.Rational(plan['beta_total']);kap=s.Rational(plan['fixed_candidate_kappa']);L=plan['joint_HS_L'];unionQ=plan['finite_patch_bank_union_Q'];R=s.Integer(17);var=s.Integer(225)
 # Require exact independent confidence receipt before any fresh RNG record is drawn.
 receipts=list(Q.glob('joint_hs_contrast_independent_receipt_20261028.json'))
 if not receipts:raise RuntimeError('No independent joint-HS receipt found; source draws remain blocked')
 sourcepath=Q/'joint_hilbert_schmidt_contrast_confidence_20261028.md';sha=hashlib.sha256(sourcepath.read_bytes()).hexdigest()
 if not any(sha in rr.read_text() for rr in receipts):raise RuntimeError('HS source has no current version-bound independent receipt; no draws')
 partial=sum((s.Rational(L)**k/s.factorial(k) for k in range(60)),s.S.Zero);assert partial>49*unionQ/beta
 assert not (HERE/'large_bank_counts.npz').exists(), 'Do not silently repeat fresh acquisition'
 cdf,probmeta,deviation=exact_source_cdf(plan['unitary_Taylor_degree'],plan['probability_CDF_denominator'])
 budget=s.Rational(plan['sampling_record_TV_budget']);assert N*deviation<budget
 (HERE/'large_bank_source_probabilities.json').write_text(json.dumps(probmeta,indent=2)+'\n')
 rng=np.random.default_rng(plan['record_seed']);settings=rng.integers(len(p.SETTINGS),size=N);uniforms=rng.integers(plan['probability_CDF_denominator'],size=N,dtype=np.int64)
 outputs=(uniforms[:,None]>=cdf[settings,:3]).sum(1);counts=np.bincount(settings*4+outputs,minlength=216).reshape(54,4);assert counts.sum()==N
 np.savez_compressed(HERE/'large_bank_counts.npz',counts=counts)
 # From here on all candidate generation uses counts alone.
 Chat=p.learner_contrasts(counts);models={'contrasts':np.array(Chat)}
 U,A,search=p.unitary_search(Chat,plan['candidate_search_seed'],starts=4);models['variational_U']=U;models['variational_A']=np.array(A)
 candidates={'variational':A,'raw_sign':[p.sign(c) for c in Chat],'scalar_whitening':p.scalar_whitening(Chat)}
 AA,operatorgap=p.operator_whitening(Chat);candidates['operator_whitening']=AA
 dec,solver,J=p.sdp_recovery(Chat,return_choi=True);models['SDP_Choi']=J
 Uq,Hq=rational_candidate_from_sdp(J,plan['rational_Cayley_grid_denominator']);Cq=exact_contrasts(counts)
 positive,r2,proof=exact_fit(Uq,Cq,kap);rr=sqrt_upper(r2)
 eta=sqrt_upper((R*L/3)**2+2*N*var*L)/N+R*L/(3*N)
 assert N*eta*eta-2*R*L*eta/3-2*var*L>=0
 e=rr+eta;regret=e*e/(8*kap);total=regret+beta+budget;passed=bool(positive and total<=s.Rational(plan['target_unnormalized_accepted_native_oracle_regret']))
 Aq=[(Uq*kron(q,I)*Uq.H).applyfunc(s.cancel) for q in P];Afloat=[np.array(a,dtype=complex) for a in Aq];models['rational_candidate_U']=np.array(Uq,dtype=complex);models['rational_candidate_A']=np.array(Afloat);candidates['rational_candidate']=Afloat
 # Post hoc scoring only: the hidden source enters after the candidate and certificate are fixed.
 V,source,_,trueC=p.generator_only_source();scores={}
 for name,AA in candidates.items():
  if AA is None:scores[name]={'abstained':True}
  else:models[name+'_A']=np.array(AA);scores[name]={'abstained':False,**p.score_decoder(AA,V,source)}
 scores['full_CPTP_SDP']={**solver,'native_Bell_loss':1-p.bell_fidelity(lambda rho:dec(source(rho)))}
 exact={'Cayley_H':[[str(Hq[a,b]) for b in range(4)] for a in range(4)],'unitary_U':[[str(Uq[a,b]) for b in range(4)] for a in range(4)],'exact_signed_contrasts':[[[str(c[a,b]) for b in range(4)] for a in range(4)] for c in Cq],**proof,'residual_upper_rational':str(rr),'HS_radius_upper_rational':str(eta),'native_oracle_regret_upper_rational':str(regret),'observed_guard_plus_failure_debits_rational':str(total),'predeclared_joint_accepted_mean_regret_bound':plan['target_unnormalized_accepted_native_oracle_regret'],'source_sampling_record_TV_upper':str(N*deviation)}
 (HERE/'large_bank_exact_candidate_certificate.json').write_text(json.dumps(exact,indent=2)+'\n');np.savez_compressed(HERE/'large_bank_models.npz',**models)
 out={'status':'PASS_NOMINAL_IDEAL_CONTROL_NATIVE_ORACLE_GUARD' if passed else 'ABSTAIN_NATIVE_ORACLE_GUARD','new_individually_drawn_blocks':N,'record_seed':plan['record_seed'],'positive_block_exact_at_kappa':positive,'fixed_kappa':str(kap),'residual_upper':float(rr),'joint_HS_upper':float(eta),'native_oracle_regret_upper':float(regret),'observed_guard_plus_failure_debits':float(total),'predeclared_joint_accepted_mean_regret_bound':plan['target_unnormalized_accepted_native_oracle_regret'],'beta_total':str(beta),'sampling_record_TV_budget':str(budget),'all_methods_same_bank':True,'scores':scores,'unitary_search':search,'operator_whitening_block_gap':operatorgap,'scope':'Nominal ideal-control one-use stationary-source simulation. Exact rational known receiver and statistical guard; no hardware gate compilation, sampled unknown payload or arbitrary-memory oracle guarantee. Acceptance is simultaneous high-probability/joint-risk, not posterior confidence for this record. All numerical SDP failures and rejected methods retained.','sha256':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in [Path(__file__),HERE/'LARGE_BANK_PREDECLARATION.json',HERE/'large_bank_counts.npz',HERE/'large_bank_models.npz',HERE/'large_bank_exact_candidate_certificate.json',HERE/'large_bank_source_probabilities.json',sourcepath]}}
 (HERE/'large_bank_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
