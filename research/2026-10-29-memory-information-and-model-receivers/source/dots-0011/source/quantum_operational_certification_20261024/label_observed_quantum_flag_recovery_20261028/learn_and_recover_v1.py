#!/usr/bin/env python3
import numpy as np,json,math
from fractions import Fraction as F
from pathlib import Path
H=Path(__file__).parent;plan=json.loads((H/'PLAN_v1.json').read_text());n=plan['n'];N=plan['N_training'];D=2**n
counts=np.zeros(D,np.int64);mom=np.zeros((D,3),np.int64);rng=np.random.default_rng(plan['training_seed'])
def errors(rng,m):
 e=np.zeros((m,n),np.int8);e[:,0]=rng.integers(0,2,m)
 for j in range(1,n):e[:,j]=e[:,j-1]^(rng.integers(0,1000,m)==999)
 return e
for start in range(0,N,16384):
 m=min(16384,N-start);e=errors(rng,m);word=e@(2**np.arange(n-1,-1,-1));a=rng.integers(0,3,m);u=rng.integers(0,10,m)
 # Exact probability of flag + outcome for X,Y,Z axes, conditional root.
 thresholds=np.array([[5,5,10],[8,5,1]],np.int8);b=np.where(u<thresholds[e[:,0],a],1,-1)
 counts+=np.bincount(word,minlength=D)
 for j in range(3):mom[:,j]+=np.bincount(word,weights=(a==j)*b,minlength=D).astype(np.int64)
np.savez_compressed(H/'training_counts_v1.npz',counts=counts,mom=mom)
selected=[max(range(a*2**(n-1),(a+1)*2**(n-1)),key=lambda x:(counts[x],-x)) for a in [0,1]]
# Empirical state differences Hhat=(tI+h.P)/2; all t,h exact rationals.
t=int(counts[selected[0]]-counts[selected[1]]);h=3*(mom[selected[0]]-mom[selected[1]]);L=sum(int(z)**2 for z in h)
assert t*t<L # one positive and one negative eigenvalue: ordinary binary projective Helstrom.
# Rational stereographic projector, proposal computed by floating sqrt then rounded.
# The saved exact projector is physical regardless of proposal accuracy.
hx,hy,hz=map(int,h);den=math.sqrt(L)+hz;B=plan['measurement_stereographic_denominator'];tx=F(round(B*hx/den),B);ty=F(round(B*hy/den),B);norm=1+tx*tx+ty*ty
Pexact=[[1/norm,complex(float(tx),-float(ty))/float(norm)],[complex(float(tx),float(ty))/float(norm),(tx*tx+ty*ty)/norm]]
P=np.array(Pexact,complex);assert np.max(abs(P@P-P))<1e-14
# Certified implementation objective slack can be bounded directly: all exact
# rational coefficients, and sqrt(L) enclosed by integer isqrt at120 bits.
scale=2**120;slo=F(math.isqrt(L*scale*scale),scale);shi=slo+F(1,scale)
# Projector Bloch direction is exactly rational; h dot b is exact.
bloch=[2*tx/norm,2*ty/norm,(1-tx*tx-ty*ty)/norm]
objective_slack=(shi-sum(F(int(x))*y for x,y in zip(h,bloch)))/(2*N)
assert objective_slack>=0
# Fresh same physical instrument holdout; exact rational flag measurement
# probabilities sampled by rejection-free uniform integers over their denominators.
tau=[[[F(1),F(0)],[F(0),F(0)]],[[F(1,10),F(3,10)],[F(3,10),F(9,10)]]]
p0=[(tau[a][0][0]+(tx*tx+ty*ty)*tau[a][1][1]+2*tx*tau[a][0][1])/norm for a in range(2)]
# Use exact64-bit rejection uniforms; denominators fit uint64 here.
assert max(p.denominator for p in p0)<2**63
rngh=np.random.default_rng(plan['holdout_seed']);Nh=plan['N_holdout'];e=errors(rngh,Nh);word=e@(2**np.arange(n-1,-1,-1));dec=np.empty(Nh,np.int8)
for a in (0,1):
 ix=np.flatnonzero(e[:,0]==a);p=p0[a];dec[ix]=np.where(rngh.integers(0,p.denominator,len(ix))<p.numerator,0,1)
success=word==np.array(selected)[dec];fail=int(np.sum(~success));np.savez_compressed(H/'holdout_counts_v1.npz',feature=e[:,0],decision=dec,success=success)
# Exact lower-tail P_Bin(N,1/20)[failures<=fail] for Fe>=19/20.
def tail(N,k):
 term=19**N;total=term
 for j in range(1,k+1):term=term*(N-j+1)//(j*19) if False else math.comb(N,j)*19**(N-j);total+=term
 return total,20**N
num,denom=tail(Nh,fail);passed=1000*num<=denom
# Rational upper bound exp(-x) from Taylor lower polynomial.
def exp_upper(x):
 term=F(1);s=term
 for k in range(1,101):term*=x/k;s+=term
 return 1/s
dp=F(1,500);dr=F(1,200);fp=2*D*exp_upper(2*N*dp*dp);fr=6*D*exp_upper(N*dr*dr/(6+F(8,3)*dr));failure=fp+fr
# epsilon_sigma<=sqrt3 dr, rounded up rational 173206/100000 dr.
eps=F(173206,100000)*dr;regret=4*(dp+eps)+objective_slack
w=F(999,1000)**(n-1);trueFe=w*(p0[0]+1-p0[1])/2;oracle=float(w)*(1+math.sqrt(.9))/2
out={'selected_words':selected,'selected_bits':[format(x,f'0{n}b') for x in selected],'projector_parameters':{'tx':str(tx),'ty':str(ty),'normalizer':str(norm)},'exact_projector_p0_by_feature':[str(x) for x in p0],'empirical_optimization_slack_upper':str(objective_slack),'simultaneous_failure_bound_float':float(failure),'simultaneous_failure_bound_exact':str(failure),'oracle_regret_bound':str(regret),'oracle_regret_float':float(regret),'holdout_N':Nh,'holdout_failures':fail,'holdout_success_rate':1-fail/Nh,'fixed_target_Fe':'.95','exact_tail_pass':bool(passed),'exact_tail_numerator_sha256':__import__('hashlib').sha256(str(num).encode()).hexdigest(),'exact_tail_denominator_sha256':__import__('hashlib').sha256(str(denom).encode()).hexdigest(),'posthoc_true_Fe':float(trueFe),'posthoc_full_CPTP_oracle':oracle,'posthoc_no_gauge_oracle':float(w/2),'new_source_full_calls':N+Nh,'native_data_qubit_exposures':n*(N+Nh),'output_flag_qubits':N+Nh,'stored_reference_qubits_training':0,'trusted_quantum_interface':'product |0>^n/Z probe readout; random one-qubit flag readout; compiled exact rational rank-one flag projector; conditional product X correction; no new encoder'}
(H/'results_v1.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if 'exact' not in k and 'parameters' not in k},indent=2))
