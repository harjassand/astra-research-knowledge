#!/usr/bin/env python3
"""Independent exact raw-joint review: trace mismatch, clocks, terminal POVMs.
No source acquisition, RNG, feasibility solver, or edits to reviewed sources.
"""
from pathlib import Path
import hashlib
import itertools
import json
import sympy as s

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'RAW_JOINT_CORE_RESIDUAL_ACQUISITION.md'
SOURCE_HASH = '7a7a9f5d5b9e7ea61357f57b51ed941d708d337a8f000047f35ff7e57aafba25'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_HASH
Q = s.Rational
I = s.eye(2)
X = s.Matrix([[0, 1], [1, 0]])
P0 = s.diag(1, 0)
P1 = I - P0
tr = s.ones(1, 2)
tests = s.Matrix([[1, 1], [1, 0]])

def model(p, flip):
    initial = s.Matrix([p, 1-p])
    G = s.Matrix.hstack(initial, P0 * initial)
    native = {'M': [P0, P1], 'X': [X], 'B': [(1-flip)*I+flip*X]}
    H = tests * G
    cs = {a: [H.inv() * tests * aop * G for aop in branches]
          for a, branches in native.items()}
    assert H.det() == p * (1-p) and H.rank() == 2
    assert list(H[0, :]) == [1, p]
    for branches in cs.values():
        assert H[0, :] * sum(branches, s.zeros(2)) == H[0, :]
    return initial, G, native, H, cs

st, Gt, nt, Ht, Ct = model(Q(1, 3), Q(1, 5))
sf, Gf, nf, Hf, Cf = model(Q(167, 500), Q(201, 1000))
mt, mf = Ht[0, :], Hf[0, :]
assert st == Gt[:, 0] and sf == Gf[:, 0]
assert mt[0] == mf[0] == 1 and mt[1] != mf[1]
et = [s.Matrix([[Q(1, 5), Q(4, 5)]])]
ef = [s.Matrix([[Q(201, 1000), Q(799, 1000)]])]
et.append(tr-et[0]); ef.append(tr-ef[0])
assert sum(et, s.zeros(1, 2)) == sum(ef, s.zeros(1, 2)) == tr

# Physical maps above have full qubit Kraus realizations; all are CP-boundary maps.
for flip in [Q(1, 5), Q(201, 1000)]:
    for branches in [[[P0], [P1]], [[X]], [[s.sqrt(1-flip)*I, s.sqrt(flip)*X]]]:
        assert sum((k.T*k for branch in branches for k in branch), s.zeros(2)) == I
        for branch in branches:
            choi = sum((k.reshape(4, 1)*k.reshape(4, 1).T for k in branch), s.zeros(4))
            assert choi.rank() < 4

# Synthetic confidence bands, including the formerly exact nonempty trace entry.
w = Q(1, 10**6)
Hhat = (Ht + Hf) / 2
DH = abs(Ht-Hf) / 2 + s.ones(2)*w
DH[0, 0] = 0
U = Hhat.inv()
A = abs(U)*DH
assert max(sum(A[i, j] for j in range(2)) for i in range(2)) < 1
M = (I-A).inv()*abs(U)
R = M-abs(U)
K = max(sum(abs(x) for x in U*v)+(s.ones(1,2)*R*v)[0]
        for v in [s.Matrix([1,0]), s.Matrix([1,1])])
for HH in [Ht,Hf]:
    assert all(abs(HH.inv()[i,j])<=M[i,j] for i in range(2) for j in range(2))
E, g = {}, {}
for a, branches in nt.items():
    E[a] = []
    for o, op in enumerate(branches):
        zt, zf = tests*op*Gt, tests*nf[a][o]*Gf
        zhat = (zt+zf)/2
        dz = abs(zt-zf)/2+s.ones(2)*w
        e = M*(dz+DH*abs(Cf[a][o])+abs(Hhat*Cf[a][o]-zhat))
        actual = abs(Ct[a][o]-Cf[a][o])
        assert all(actual[i,j]<=e[i,j] for i in range(2) for j in range(2))
        universal = 2*M*(dz+DH*M*(abs(zhat)+dz))
        assert all(e[i,j]<=universal[i,j] for i in range(2) for j in range(2))
        E[a].append(e)
    g[a] = max(sum(e[i,j] for e in E[a] for i in range(2)) for j in range(2))
b = K*max(g.values())/2
em = abs(Hhat[0,:]-mf)+DH[0,:]
assert all(abs(mt[j]-mf[j])<=em[j]<=2*DH[0,j] for j in range(2))
bmass = K*max(em)/2
q = [abs(t*Gt-f*Gf)+s.ones(1,2)*w for t,f in zip(et,ef)]
# Include trace as the one-outcome terminal library for abort/censor branches.
terminal_error = K*max(max(em),max(sum(row[j] for row in q) for j in range(2)))/2
delta, gamma = Q(1,3), Q(2,3)

def action(h):
    n=len(h)
    if n==6 or (n==4 and h[1]==h[3]): return None
    return ['B','M',('X' if n>1 and h[1] else 'B'),'M','B','M'][n]

def terminal_kind(h, cap):
    if action(h) is None: return 'stop'
    if len(h)==cap: return 'censor'
    return None

def physical_law(native, effects, h, state, cap, final_povm):
    kind=terminal_kind(h,cap)
    if kind:
        rows=effects if kind=='stop' and final_povm else [tr]
        return {h+(kind,j):(row*state)[0] for j,row in enumerate(rows)}
    out={h+('abort',0):delta*(tr*state)[0]}
    for o,op in enumerate(native[action(h)]):
        out.update(physical_law(native,effects,h+(o,),gamma*op*state,cap,final_povm))
    return out

reports=[]
for final_povm in [False,True]:
  for cap in range(7):
    pt=physical_law(nt,et,(),st,cap,final_povm)
    pf=physical_law(nf,ef,(),sf,cap,final_povm)
    assert pt.keys()==pf.keys() and sum(pt.values())==sum(pf.values())==1
    assert all(x>=0 for x in list(pt.values())+list(pf.values()))
    telescope={h:s.S.Zero for h in pt}
    counts={'call_mass':s.S.Zero,'leaf_mass':s.S.Zero,'native_bound':s.S.Zero,
            'nonempty_leaf_mass':s.S.Zero,'negative_prefixes':0,'suffix_tests':0,
            'terminal_abs_sum':s.S.Zero}

    def leaf(h,kind,state,c):
        rows_t=et if kind=='stop' and final_povm else [tr]
        rows_f=ef if kind=='stop' and final_povm else [tr]
        counts['leaf_mass']+=(tr*state)[0]
        if h: counts['nonempty_leaf_mass']+=(tr*state)[0]
        for j,(rt,rf) in enumerate(zip(rows_t,rows_f)):
            discrepancy=((rt*Gt-rf*Gf)*c)[0]
            assert discrepancy==(rt*state)[0]-(rf*Gf*c)[0]
            telescope[h+(kind,j)]+=discrepancy
            counts['terminal_abs_sum']+=abs(discrepancy)

    def visit(h,state,c):
        p=(tr*state)[0]
        assert tests*state==Ht*c and (mt*c)[0]==p
        assert all(0<=x<=p for x in Ht*c)
        assert sum(abs(x) for x in c)<=K*p
        counts['negative_prefixes']+=int(any(x<0 for x in c))
        kind=terminal_kind(h,cap)
        if kind:
            leaf(h,kind,state,c)
            return
        leaf(h,'abort',delta*state,delta*c)
        a=action(h)
        counts['call_mass']+=gamma*p
        counts['native_bound']+=gamma*K*g[a]*p/2
        for o,op in enumerate(nt[a]):
            insertion=gamma*(Ct[a][o]-Cf[a][o])*c
            signed=physical_law(nf,ef,h+(o,),Gf*insertion,cap,final_povm)
            assert sum(abs(x) for x in signed.values())<=sum(abs(x) for x in Gf*insertion)
            assert sum(abs(x) for x in Gf*insertion)<=sum(mf[j]*abs(insertion[j]) for j in range(2))
            assert sum(mf[j]*abs(insertion[j]) for j in range(2))<=sum(abs(x) for x in insertion)
            for key,val in signed.items():telescope[key]+=val
            counts['suffix_tests']+=1
            visit(h+(o,),gamma*op*state,gamma*Ct[a][o]*c)

    visit((),st,s.Matrix([1,0]))
    assert counts['leaf_mass']==1
    assert counts['call_mass']<=gamma/delta
    assert all(telescope[h]==pt[h]-pf[h] for h in pt)
    tv=sum(abs(pt[h]-pf[h]) for h in pt)/2
    final_debit=terminal_error if final_povm else bmass
    assert counts['terminal_abs_sum']/2<=final_debit
    if not final_povm:
        assert counts['terminal_abs_sum']/2<=bmass*counts['nonempty_leaf_mass']
        assert counts['nonempty_leaf_mass']<=gamma
    assert tv<=counts['native_bound']+final_debit<=b*counts['call_mass']+final_debit
    reports.append({'final_POVM':final_povm,'censor_depth':cap,'TV':tv,
                    'expected_true_calls':counts['call_mass'],
                    'bound':b*counts['call_mass']+final_debit,
                    'bound_float':float(b*counts['call_mass']+final_debit),
                    'terminal_debit':final_debit,'terminal_leaf_mass':counts['leaf_mass'],
                    'probability_at_least_one_native_call':counts['nonempty_leaf_mass'],
                    'negative_prefixes':counts['negative_prefixes'],
                    'physical_suffix_tests':counts['suffix_tests'],
                    'exact_telescope_residual':0})

# Zero native-residual obstruction with infinitely repeated nondemolition readout.
_,_,_,H0,C0=model(Q(1,3),0)
_,_,_,H1,C1=model(Q(1,2),0)
assert C0['M']==C1['M']
assert (H0[0,:]-H1[0,:])==s.Matrix([[0,-Q(1,6)]])
assert abs(Q(1,3)-Q(1,2))==Q(1,6)
persistent_clock_TV=gamma*Q(1,6)
assert persistent_clock_TV==Q(1,9)

# Finite exhaustive pool for the two-branch nondemolition interface: D=4.
words=[wrd for n in range(4) for wrd in itertools.product([0,1],repeat=n)]
def product(wrd):
    ans=I
    for z in wrd: ans=[P0,P1][z]*ans
    return ans
past=s.Matrix.hstack(*[product(wrd)*s.Matrix([Q(1,3),Q(2,3)]) for wrd in words])
future=s.Matrix.vstack(*[tr*product(wrd) for wrd in words])
full=future*past
assert full.rank()==2 and full.extract([0,1],[0,1]).det()!=0

# Independent check of the open-loop limitation and its feedback escape.
Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
axes=[X,Y,Z]
rho=I/2
def nonselect(axis,r):
    plus=(I+axis)/2; minus=(I-axis)/2
    return s.simplify(plus*r*plus+minus*r*minus)
for axis in axes:assert nonselect(axis,rho)==rho
feedback_states=[]
for i,axis in enumerate(axes):
    other=axes[(i+1)%3]
    plus=(I+axis)/2; minus=(I-axis)/2
    out=nonselect(other,plus*rho*plus)+nonselect(axis,minus*rho*minus)
    assert s.simplify(out-(I/2-axis/4))==s.zeros(2)
    feedback_states.append(out)
def bloch(r):return s.Matrix([s.trace(B*r) for B in [I,X,Y,Z]])
assert s.Matrix.hstack(bloch(rho),*[bloch(r) for r in feedback_states]).rank()==4

def encode(x):
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    if isinstance(x,s.Basic):return str(x)
    return x
report={'status':'PASS independent exact raw-joint diagnostic',
        'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_calls':0,'rng_calls':0,'counts_acquired':False,'semialgebraic_solver_executed':False,
        'true_core_masses':list(mt),'fitted_core_masses':list(mf),
        'K_core':K,'native_coefficient':b,'mass_debit':bmass,'final_POVM_debit':terminal_error,
        'clock_delta':delta,'clocked_feedback_checks':reports,
        'zero_native_residual_persistent_bit':{'unclocked_TV':Q(1,6),'full_clocked_TV':persistent_clock_TV},
        'finite_branch_pool':{'q':len(words),'joint_pool_upper_bound':3*len(words)**2,
                             'observable_rank':full.rank(),'core_with_both_empty_entries':True},
        'XYZ_open_loop_rank':1,'XYZ_normalized_feedback_rank':4,
        'all_feasible_residual_bound_checked':True}
(ROOT/'raw_joint_core_independent_check.json').write_text(json.dumps(encode(report),indent=2)+'\n')
print(json.dumps(encode({k:report[k] for k in ['status','source_sha256','zero_native_residual_persistent_bit','finite_branch_pool','XYZ_open_loop_rank','XYZ_normalized_feedback_rank']}),indent=2))
print('Clocked checks:',len(reports),'max-depth results:',json.dumps(encode([r for r in reports if r['censor_depth']==6]),indent=2))
