#!/usr/bin/env python3
"""Exact deterministic boundary/obligation diagnostic. No source acquisition or RNG."""
import hashlib, itertools, json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parent
I=sp.eye(2); X=sp.Matrix([[0,1],[1,0]]); Y=sp.Matrix([[0,-sp.I],[sp.I,0]]); Z=sp.diag(1,-1)
B=[I,X,Y,Z]; tau=sp.Matrix([[1,0,0,0]])

def coord(A): return sp.Matrix([sp.simplify(sp.trace(b*A)) for b in B])
def channel(K): return sp.Matrix.hstack(*[coord(K*b*K.conjugate().T)/2 for b in B])
def absM(A): return A.applyfunc(abs)
def colnorm(A): return max(sum(abs(A[i,j]) for i in range(A.rows)) for j in range(A.cols))
def js(x):
    if isinstance(x, dict): return {str(k):js(v) for k,v in x.items()}
    if isinstance(x, list): return [js(v) for v in x]
    if isinstance(x, tuple): return [js(v) for v in x]
    if isinstance(x, sp.Basic): return str(x)
    return x

P=[(I+b)/2 for b in [Z,-Z,X,Y]]
G=sp.Matrix.hstack(*map(coord,P))
F=sp.Matrix.vstack(tau,*[(tau+sp.eye(4)[j,:])/2 for j in [3,1,2]])
H=F*G; U=H.inv(); assert H.det()!=0
Had=(X+Z)/sp.sqrt(2); S=sp.diag(1,sp.I)
n=1000
Rot=((n*n-1)*I+2*n*sp.I*Z)/(n*n+1)
Ktrue={'X':[X],'H':[Had],'S':[S],'Q':[Rot]}
for name,b in [('Mx',X),('My',Y),('Mz',Z)]: Ktrue[name]=[(I+b)/2,(I-b)/2]
Kfit={**Ktrue,'Q':[I]}
Ltrue={a:[channel(k) for k in ks] for a,ks in Ktrue.items()}
Lfit={a:[channel(k) for k in ks] for a,ks in Kfit.items()}
# Exact Kraus completeness, and every branch has rank-one Choi, including Q.
for maps in (Ktrue,Kfit):
    for a,ks in maps.items():
        assert (sum((k.conjugate().T*k for k in ks),sp.zeros(2))-I).applyfunc(sp.simplify)==sp.zeros(2)
        for k in ks:
            v=sp.Matrix(k).reshape(4,1); choi=v*v.conjugate().T
            assert choi.rank()==1 and choi.det()==0
# The core states really are the declared normalized legal preparations.
for j,word in enumerate([[],['X'],['H'],['H','S']]):
    v=G[:,0]
    for a in word: v=Lfit[a][0]*v
    assert v==G[:,j]
Ctrue={a:[U*F*l*G for l in ls] for a,ls in Ltrue.items()}
Cfit={a:[U*F*l*G for l in ls] for a,ls in Lfit.items()}
for maps in (Ctrue,Cfit):
    for a,ms in maps.items(): assert sp.ones(1,4)*sum(ms,sp.zeros(4))==sp.ones(1,4)
# Hypothetical outward rational bands centered on analytic probabilities.
# This is NOT counted data and NOT a statistical acquisition claim.
w=sp.Rational(1,10**7)
DH=sp.ones(4)*w; DH[0,:]=sp.zeros(1,4)
A=absM(U)*DH; assert max(sum(A[i,j] for j in range(4)) for i in range(4))<1
M=(sp.eye(4)-A).inv()*absM(U); R=M-absM(U)
vertices=[sp.Matrix((1,)+v) for v in itertools.product([0,1],repeat=3)]
K=max(sum(abs(x) for x in U*v)+(sp.ones(1,4)*R*v)[0] for v in vertices)
E={}; glocal={}
for a,ms in Cfit.items():
    E[a]=[]
    for o,c in enumerate(ms):
        Hz=F*Ltrue[a][o]*G
        Dz=sp.ones(4)*w
        # Known deterministic branch trace is one, otherwise measured event.
        if len(ms)==1: Dz[0,:]=sp.zeros(1,4)
        e=M*(Dz+DH*absM(c)+absM(H*c-Hz))
        assert all(e[i,j]>=abs(Ctrue[a][o][i,j]-c[i,j]) for i in range(4) for j in range(4))
        E[a].append(e)
    glocal[a]=max(sum(e[i,j] for e in E[a] for i in range(4)) for j in range(4))
b=K*max(glocal.values())/2
# Adaptive feedback: measured outcomes affect later native unitary/test choices.
DEPTH=11
schedule=['H','Q','My','X','Q','Mx','Q','My','H','Q','Mz']
def action(h):
    t=len(h); a=schedule[t]
    if t==3 and sum(h)%2: a='H'
    if t==8 and sum(h)%2: a='S'
    return a

def leaves(maps, prefix, state):
    if len(prefix)==DEPTH: return {prefix:(sp.ones(1,4)*state)[0]}
    out={}; a=action(prefix)
    for o,c in enumerate(maps[a]): out.update(leaves(maps,prefix+(o,),c*state))
    return out

e1=sp.eye(4)[:,0]
p=leaves(Ctrue,(),e1); q=leaves(Cfit,(),e1)
assert sum(p.values())==sum(q.values())==1 and min(p.values())>=0 and min(q.values())>=0
TV=sum(abs(p[h]-q[h]) for h in p)/2
# Explicit true-prefix / fitted-suffix signed tree telescope.
telescope={h:sp.S.Zero for h in p}; prefix_nodes=[((),e1)]
max_c_ratio=sp.S.One; has_negative=False; insertion_bound=sp.S.Zero
for depth in range(DEPTH):
    next_nodes=[]
    for h,c in prefix_nodes:
        mass=(sp.ones(1,4)*c)[0]
        if mass:
            ratio=sum(abs(x) for x in c)/mass
            max_c_ratio=max(max_c_ratio,ratio); assert ratio<=K
            assert (H*c)[0]==mass and all(0<=x<=mass for x in H*c)
        has_negative=has_negative or any(x<0 for x in c)
        a=action(h)
        insertion_bound+=K*glocal[a]*mass/2
        for o,ct in enumerate(Ctrue[a]):
            d=(ct-Cfit[a][o])*c
            for leaf,value in leaves(Cfit,h+(o,),d).items(): telescope[leaf]+=value
            next_nodes.append((h+(o,),ct*c))
    prefix_nodes=next_nodes
assert all(telescope[h]==p[h]-q[h] for h in p)
assert TV<=insertion_bound<=DEPTH*b and has_negative
# Clock diagnostic: no actual clock samples. Both physical models obey the same coin.
delta=sp.Rational(1,3); clock_bound=b*(1-delta)/delta
# Rank obligation negative control: exact one-step tables, depth-two TV=1.
source0=sp.Matrix([[1]])
P0=sp.Matrix([[0,0],[1,0]]); P1=sp.Matrix([[0,0],[0,1]])
s0=sp.Matrix([1,0]); tr2=sp.ones(1,2)
assert (tr2*P0*s0)[0]==1 and (tr2*P1*s0)[0]==0
assert (tr2*P0*P0*s0)[0]==0 and (tr2*P1*P0*s0)[0]==1
# Its finite Hankel rank is 2: rows empty/next1, columns empty/past0.
H_bad=sp.Matrix([[1,1],[0,1]]); assert H_bad.rank()==2
# Nonintertwining positive core lift remains sound if rank checked.
G1=coord((I+Z)/2); K1=coord(Z); Phi=channel(X)
assert Phi*K1==-K1 and Phi*G1==G1-K1 and tau*K1==sp.zeros(1,1)
assert Phi*G1!=G1 and (tau*Phi**17*G1)[0]==1
report={
 'status':'PASS: exact deterministic diagnostic, not independent receipt',
 'source_calls':0,'episode_starts':0,'rng_calls':0,'counts_acquired':False,
 'intervals':'hypothetical rational bands around analytic probabilities; not acquisition',
 'source_sha256':hashlib.sha256((ROOT/'COUNT_CERTIFIED_PHYSICAL_RESIDUAL_SIMULATOR.md').read_bytes()).hexdigest(),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'physical_dimension':2,'source_and_candidate_observable_rank':4,
 'core_determinant':H.det(),'all_native_branch_choi_ranks':1,
 'true_Q_unitary':f'(({n*n-1}) I + ({2*n}) i Z)/({n*n+1})','fit_Q_unitary':'I',
 'interval_halfwidth':w,'K_core':K,'K_core_float':float(K),'g_by_action':glocal,
 'local_TV_coefficient':b,'local_TV_coefficient_float':float(b),
 'horizon':DEPTH,'full_transcript_TV':TV,'full_transcript_TV_float':float(TV),
 'true_prefix_insertion_bound':insertion_bound,'true_prefix_insertion_bound_float':float(insertion_bound),
 'uniform_horizon_bound':DEPTH*b,'uniform_horizon_bound_float':float(DEPTH*b),
 'clock_delta':delta,'clock_bound':clock_bound,'clock_bound_float':float(clock_bound),
 'exact_telescope_residual':0,'negative_true_preparation_coefficients_observed':has_negative,
 'max_observed_true_coordinate_mass_ratio':max_c_ratio,
 'drop_rank_negative_control':{'one_step_core_residual':0,'claimed_rank':1,'actual_candidate_rank':2,'depth_two_TV':1},
 'physical_section_intertwining_negative_control':{'rank':1,'intertwining':False,'all_word_probabilities':1,'kernel_witness_checked':True}
}
(ROOT/'physical_residual_simulator_exact_check.json').write_text(json.dumps(js(report),indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','source_calls','K_core_float','local_TV_coefficient_float','full_transcript_TV_float','uniform_horizon_bound_float','clock_bound_float','exact_telescope_residual']},indent=2))
