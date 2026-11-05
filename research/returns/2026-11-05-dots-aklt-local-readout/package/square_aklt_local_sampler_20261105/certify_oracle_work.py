"""Exact geometric work majorants for every local-loop proposal.
No stochastic simulation or floating inequality is used in the certificate.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys,numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(HERE))
from local_birth_oracle import LocalLoopBirthSampler
s=LocalLoopBirthSampler(0)
z=np.load(ROOT/'square_aklt_loop_audit_20261105/trail_certificate_m6.npz')
v=z['v'];an=int(z['alpha_num']);ad=int(z['alpha_den']);N=len(v)
assert np.all((z['weights']*v[z['targets']]).sum(1)*ad<=5*v*an)
rho=F(an,3*ad);assert rho<1
# Q is the pre-Doob continuation matrix, weights w/15. V=v_state
# is constant over location/orientation, hence QV<=rho V.
c=max(F(int(s.g[o*N+i].max()),int(v[i])) for o in range(4) for i in range(N))
R=max(r for _,_,r in s.options)
bv=sum(3**(s.m-len(h)+r)*5**(R-r)*int(v[i]) for i,h,r in s.options if i>=0)
D=c*bv/s.total
# Initial prefix probabilities are b_h*g_h/Z, so the g denominators
# telescope. This average bound is stronger than worst-state max(v/g).
k=1
while D*rho**k>1:k+=1
# T=number of continuation steps selected, before geometric early reject.
# P(T>=n)<=min(1,D*rho^n); for n>=k use geometric bound.
tail0=D*rho**k/(1-rho)
tail1=D*rho**k*(F(k)/(1-rho)+rho/(1-rho)**2)
ET=F(k-1)+tail0
ET2=F((k-1)**2)+2*tail1-tail0
E_length=s.m+ET
E_length2=s.m**2+2*s.m*ET+ET2
assert E_length<F(68489,1000)
assert E_length2<10000
out={'rho':str(rho),'initial_mixture_prefactor_D':str(D),'geometric_tail_from_n':k,
 'expected_attempted_walk_steps_upper':str(E_length),'expected_attempted_walk_steps_decimal':float(E_length),
 'expected_squared_attempted_walk_steps_upper':str(E_length2),'expected_squared_attempted_walk_steps_decimal':float(E_length2),
 'expected_continuation_decisions_upper':str(ET+1),
 'total_steps_per_query_vertex_using_14_120548_calls':str(E_length*F(14120548,1000000)),
 'scope':'Uniform over finite query sets and boxes, including Z^2. One final continuation decision is additional. Walk steps and quadratic-length canonicalization proxies are not bit complexity or a wall-time guarantee.'}
(HERE/'oracle_work_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
