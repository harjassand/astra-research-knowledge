"""New bounded-solver three-role simulation; visible gaps, no target-gap abort.
No outer code/payload or physical source-clock implementation.
"""
import json,math,random,time,sys
sys.set_int_max_str_digits(0)
from fractions import Fraction as F
from pathlib import Path
import numpy as np
sys.path.insert(0,'producer-workspace/quaternion_oracle_controller_20261029')
import quartic_sos_oracle as qo
from bounded_sos_oracle import solve as bounded_solve,verify as bounded_verify
from dyadic_gap_counter import Counter
root=Path(__file__).parent
src=(Path('producer-workspace/quaternion_oracle_controller_20261029')/'capture_one_axis.py').read_text().split('T=60000;')[0];ctx={};exec(src,ctx)
I,X,Y,Z=ctx['I'],ctx['X'],ctx['Y'],ctx['Z'];pa=ctx['pa'];kron=ctx['kron'];base=ctx['base'];Us,U4,E0=ctx['Us'],ctx['U4'],ctx['E0'];D=16;d=2;n=4
T=120;p=F(1,3);dim=35;v=F(720**2*T,dim*p);radius=math.isqrt(v.numerator//v.denominator)
while radius*radius<v:radius+=1
bits=(4*dim*T*T-1).bit_length();M=2**bits;eps=F(radius,4*T*T)
prng=random.Random(2026102907);rng=np.random.default_rng(2026102908)
Vobs=[F(0)]*3;gap_counters=[Counter((T-1).bit_length()+32,F(T*720,p)+dim*radius) for _ in range(3)]
G=[{e:F(0) for e in qo.exps} for _ in range(3)];bath=np.array([[.7,.12j],[-.12j,.3]],complex);last=0
ops=[[ctx['op_at'](pp,i) for i in range(n)] for pp in pa]
match=[]
for pairs in [[(0,1),(2,3)],[(0,2),(1,3)],[(0,3),(1,2)]]:
 v=np.zeros(D,complex)
 for xx in range(D):
  bs=[(xx>>(n-1-j))&1 for j in range(n)]
  if all(bs[a]!=bs[b] for a,b in pairs):v[xx]=math.prod(1 if bs[a]==0 else -1 for a,b in pairs)/2
 assert abs(np.vdot(v,v)-1)<1e-12 and np.linalg.norm(E0@E0.conj().T@v-v)<1e-12
 match.append(v)
roles={'learn':0,'validate':0,'service':0};calls=[];certs=[];fails=0;bad_sum=0.;delta_sum=0.;oracle_seconds=0.;completed=True;start=time.time()
for t in range(T):
 # Source process fixed before current private candidate/role/probe draws.
 z=0 if t<T//5 else(1 if t<2*T//5 else 2+last%4)
 vs=[];cs=[];roundcert=[]
 for edge in range(3):
  perturb={e:F(radius*(2*prng.getrandbits(bits)+1-M),M) for e in qo.exps}
  query={e:(G[edge][e]+perturb[e])/2 for e in qo.exps}
  st=time.time();cert=bounded_solve(query);assert bounded_verify(query,cert);gap_counters[edge].add(cert['gap']);oracle_seconds+=time.time()-st
  roundcert.append(dict(edge=edge,query=[str(query[e]) for e in qo.exps],certificate=cert))
  if cert['status']!='sound_gap_certificate':completed=False;break
  q=np.array([float(F(x)) for x in cert['quaternion']]);v=q[0]*I-1j*sum(q[j+1]*pa[j] for j in range(3));vs.append(v)
  cs.append(np.array([[np.trace(pa[a]@v@pa[b]@v.conj().T).real/2 for b in range(3)] for a in range(3)]))
 certs.append(roundcert)
 if not completed:break
 current=[]
 for edge,C in enumerate(cs):
  S=.5*(np.eye(D)+sum(C[a,b]*ops[a][edge+1]@ops[b][0] for a in range(3) for b in range(3)));AA=np.kron(S,I)
  zz=(AA@Us[z].conj().T@AA@Us[z]).reshape(D,2,D,2);ef=I-np.trace(zz,axis1=0,axis2=2)/D;current.append(np.trace(bath@ef).real)
 delta_sum+=sum(current);rr=int(rng.integers(9));role='learn' if rr<3 else('validate' if rr<7 else 'service');roles[role]+=1
 record=dict(t=t+1,role=role,source_index=z,current_star_loss=sum(current),max_oracle_gap=max(float(F(c['certificate']['gap'])) for c in roundcert))
 if role=='learn':
  c=rng.integers(0,3,n);sign=rng.choice([-1,1],n);a=rng.integers(0,3,n)
  vin=kron([base[c[j]][int(sign[j])].reshape(2,1) for j in range(n)]).ravel();bout=kron([np.column_stack([base[a[j]][-1],base[a[j]][1]]) for j in range(n)])
  A=np.einsum('yx,xmzn,z->ymn',bout.conj().T,U4[z],vin,optimize=True);prob=np.einsum('ymn,nk,ymk->y',A,bath,A.conj(),optimize=True).real;prob=np.maximum(prob,0);prob/=prob.sum();out=int(rng.choice(D,p=prob));yy=np.array([1 if(out>>(n-1-j))&1 else -1 for j in range(n)])
  K=A[out];bath=K@bath@K.conj().T;bath/=np.trace(bath)
  for edge in range(3):
   i=edge+1;h=qo.add({},qo.mul(qo.Qpoly,qo.R[a[i]][a[0]]),-F(9,4)*int(yy[i]*yy[0]));h=qo.add(h,qo.mul(qo.R[a[i]][a[0]],qo.R[c[i]][c[0]]),-F(81,4)*int(yy[i]*yy[0]*sign[i]*sign[0]))
   increment={e:2*h.get(e,0)/p for e in qo.exps};Vobs[edge]+=sum(abs(v) for v in increment.values())**2
   for e in qo.exps:G[edge][e]+=increment[e]
  last=int(np.sum(yy<0)%4)
 else:
  W=kron([I]+vs);E=W@E0;P=E@E.conj().T
  if role=='validate':
   psi=W@match[int(rng.integers(3))];rho=Us[z]@np.kron(np.outer(psi,psi.conj()),bath)@Us[z].conj().T;tt=rho.reshape(D,2,D,2)
   pm=np.einsum('x,xmyn,y->mn',psi.conj(),tt,psi);pr=float(np.trace(pm).real);passed=rng.random()<pr
   bath=pm/pr if passed else (np.trace(tt,axis1=0,axis2=2)-pm)/(1-pr);fails+=not passed;record['matching_pass']=bool(passed)
  else:
   B=np.einsum('yx,xmyn->mn',P,U4[z])/d;bad=float(1-np.trace(B@bath@B.conj().T).real);assert bad<=8*sum(current)+1e-11;bad_sum+=bad;record['service_bad_weight']=bad
   rho=Us[z]@np.kron(P/d,bath)@Us[z].conj().T;bath=np.trace(rho.reshape(D,2,D,2),axis1=0,axis2=2)
  bath=(bath+bath.conj().T)/2;bath/=np.trace(bath)
 calls.append(record)
retrospective=[];empirical=F(3*3*roles['learn'],4*p)
for edge in range(3):
 query={e:G[edge][e]/2 for e in qo.exps};cert=bounded_solve(query);assert bounded_verify(query,cert);empirical+=F(cert['upper']);retrospective.append(cert)
result=dict(feedback_exponents=qo.exps,final_feedback=[[str(G[i][e]) for e in qo.exps] for i in range(3)],observed_squared_feedback_per_edge=list(map(str,Vobs)),shared_probe_count=roles['learn'],reported_gap_counters=[c.report() for c in gap_counters],retrospective_candidates=retrospective,retrospective_empirical_score=str(empirical),p=str(p),verified_outer_code_deployed=False,unknown_payload_transmitted=False,T=T,completed_horizon=completed,actual_source_calls=len(calls),roles=roles,validation_failures=fails,service_bad_sum=bad_sum,mean_service_bad=bad_sum/max(1,roles['service']),mean_selected_star_loss=delta_sum/max(1,len(calls)),oracle_seconds=oracle_seconds,total_seconds=time.time()-start,perturbation_radius=radius,perturbation_bits_per_coordinate=bits,requested_gap=str(eps),calls=calls,oracle_calls=certs,scope='Executed bounded discrete-clock FTPL diagnostic with actual sampled probes/matching validations and retained coherent bath; services use averaged orbit interface. No outer code, unknown payload or laboratory latency model. Fixed-budget solver always returns a visible sound gap; there is no target-gap timeout. Discrete source policy ignores wall-clock time by construction; no physical private-clock proof. No verified outer code was deployed, so no readiness certificate can be claimed. Seeded PRNG is reproducibility machinery, not a physical private-bit source.')
(root/'bounded_live_three_role_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['calls','oracle_calls','retrospective_candidates','final_feedback','feedback_exponents','reported_gap_counters']},indent=2))
