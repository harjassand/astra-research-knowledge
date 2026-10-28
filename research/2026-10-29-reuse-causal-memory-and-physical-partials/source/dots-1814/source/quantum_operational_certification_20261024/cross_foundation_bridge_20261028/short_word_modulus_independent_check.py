#!/usr/bin/env python3
"""Independent exact checks for relation distance, CP comparison and terminal seeds.
No generic quantifier elimination, source acquisition, randomness or synthesis.
"""
from pathlib import Path
import hashlib
import json
import sympy as s

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'SHORT_WORD_SEMIALGEBRAIC_PHYSICAL_PREDICTION.md'
SOURCE_HASH='b5f83e2d812b7dd64f0e244b7a55093f78f8d02feaff30026d9bfc86468d37fb'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_HASH
Q=s.Rational
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
basis=[I,X,Y,Z]; trace=s.Matrix([[1,0,0,0]])
Had=(X+Z)/s.sqrt(2); V=s.diag(1,s.I)
Pz=[(I+Z)/2,(I-Z)/2]; Px=[(I+X)/2,(I-X)/2]; Py=[(I+Y)/2,(I-Y)/2]
rho=(I+X/3+Y/4+Z/5)/2
assert rho.trace()==1 and rho.det()>0

def simp(A):return A.applyfunc(s.simplify)
def coord(A):return simp(s.Matrix([s.trace(B*A) for B in basis]))
def effect(F):return simp(s.Matrix([[s.trace(F*B)/2 for B in basis]]))
def frob2(A):return s.simplify(s.trace(A.conjugate().T*A))
def op(branch,A):return simp(sum((w*K*A*K.conjugate().T for w,K in branch),s.zeros(2)))
def choi(branch):
    return simp(sum((w*K.reshape(4,1)*K.reshape(4,1).conjugate().T for w,K in branch),s.zeros(4)))
def model(state,kraus,effects):
    assert state.trace()==1 and state.det()>=0
    liou={}; js={}
    for a,branches in kraus.items():
        assert simp(sum((w*K.conjugate().T*K for branch in branches for w,K in branch),s.zeros(2)))==I
        liou[a]=[s.Matrix.hstack(*[coord(op(branch,B))/2 for B in basis]) for branch in branches]
        js[a]=[choi(branch) for branch in branches]
    for rows in effects:
        assert sum(rows,s.zeros(2))==I
        assert all(F.det()>=0 and F.trace()>=0 for F in rows)
    return {'rho':state,'initial':coord(state),'kraus':kraus,'maps':liou,'choi':js,
            'effects':effects,'rows':[[effect(F) for F in rows] for rows in effects]}

kb={'U':[[(s.S.One,Had)]],'M':[[(s.S.One,P)] for P in Pz]}
eb=[Px,Py]
bar=model(rho,kb,eb)
gauge=lambda A:simp(V*A*V.conjugate().T)
kbp={a:[[(w,gauge(K)) for w,K in branch] for branch in branches] for a,branches in kb.items()}
barprime=model(gauge(rho),kbp,[[gauge(F) for F in rows] for rows in eb])
eps,eta=Q(1,1000),Q(1,1250)

def perturbed(base,amount,target_state,unitary,measurement,terminal):
    kk={}
    kk['U']=[[(w*(1-amount),K) for w,K in base['kraus']['U'][0]]+[(amount,unitary)]]
    kk['M']=[[(w*(1-amount),K) for w,K in base['kraus']['M'][j]]+[(amount,measurement[j])] for j in range(2)]
    effects=[[(1-amount)*base['effects'][a][j]+amount*terminal[a][j] for j in range(2)] for a in range(2)]
    return model((1-amount)*base['rho']+amount*target_state,kk,effects)

theta=perturbed(bar,eps,Pz[0],I,Px,[Pz,Py[::-1]])
theta_prime=perturbed(barprime,eta,Pz[1],X,Py,[Px[::-1],Pz])

def parameter_sq(m,n,include_terminal=True):
    total=frob2(m['rho']-n['rho'])
    total+=sum(frob2(j-k) for a in m['choi'] for j,k in zip(m['choi'][a],n['choi'][a]))
    if include_terminal:total+=sum(frob2(f-g) for ff,gg in zip(m['effects'],n['effects']) for f,g in zip(ff,gg))
    return s.simplify(total)

# A physically separated equivalent pair, not model identification.
assert parameter_sq(bar,barprime)>0
R=s.Matrix.hstack(*[coord(gauge(B))/2 for B in basis])
assert R*bar['initial']==barprime['initial']
for a,branches in bar['maps'].items():
    for j,A in enumerate(branches):assert R*A==barprime['maps'][a][j]*R
for fs,gs in zip(bar['rows'],barprime['rows']):
    for f,g in zip(fs,gs):assert f==g*R

# Direct-sum span saturation with terminal seeds, independently of gauge proof.
def span_check(m,n):
    mats=[s.diag(A,B) for a in m['maps'] for A,B in zip(m['maps'][a],n['maps'][a])]
    v=m['initial'].col_join(n['initial'])
    vectors=[v]; words=[()]; dims=[1]
    for depth in range(1,8):
        old=list(zip(vectors,words)); changed=False
        for vv,ww in old:
            for z,A in enumerate(mats):
                candidate=A*vv
                if s.Matrix.hstack(*vectors,candidate).rank()>len(vectors):
                    vectors.append(candidate);words.append(ww+(z,));changed=True
        dims.append(len(vectors))
        if not changed:break
    reachable=s.Matrix.hstack(*vectors)
    assert len(vectors)<=8 and max(map(len,words))<=7
    # Stopping span is invariant under every branch.
    for A in mats:assert reachable.row_join(A*reachable).rank()==reachable.rank()
    rows=[trace.row_join(-trace)]
    rows += [f.row_join(-g) for ff,gg in zip(m['rows'],n['rows']) for f,g in zip(ff,gg)]
    equal=all(row*reachable==s.zeros(1,reachable.cols) for row in rows)
    witness=next((ww for row in rows for vv,ww in zip(vectors,words) if (row*vv)[0]!=0),None)
    return {'growth':dims,'dimension':len(vectors),'equivalent':equal,'short_witness':witness}

equiv=span_check(bar,barprime)
different=span_check(theta,theta_prime)
assert equiv['equivalent'] and not different['equivalent']

# Exact feedback records for four physical models. Final seed selected by record.
def policy(h):
    if len(h)>=3 and h[-2:]==(1,1):return None
    return 'M' if len(h)%2==0 or sum(h)%2 else 'U'

def law(m,h,state,H,delta,terminal):
    a=policy(h)
    finish=len(h)==H or a is None
    def end(kind,v):
        rows=m['rows'][sum(h)%2] if terminal else [trace]
        return {h+(kind,j):(row*v)[0] for j,row in enumerate(rows)}
    if finish:return end('end',state)
    out=end('abort',delta*state) if delta else {}
    for o,A in enumerate(m['maps'][a]):out.update(law(m,h+(o,),(1-delta)*A*state,H,delta,terminal))
    return out

def tv(p,q):
    assert p.keys()==q.keys()
    return sum(abs(p[k]-q[k]) for k in p)/2

records=[]
for terminal in [False,True]:
 for delta in [s.S.Zero,Q(1,3)]:
  for H in range(8):
    laws=[law(m,(),m['initial'],H,delta,terminal) for m in [theta,bar,barprime,theta_prime]]
    assert all(sum(p.values())==1 and min(p.values())>=0 for p in laws)
    assert laws[1]==laws[2]
    observed=tv(laws[0],laws[3]);outer=tv(laws[0],laws[1])+tv(laws[2],laws[3])
    assert observed<=outer
    a2=parameter_sq(theta,bar,terminal)+parameter_sq(theta_prime,barprime,terminal)
    cap=H if not delta else (1-delta)/delta
    M=s.Integer(2)*(1+2*cap)+(2 if terminal else 0)
    assert outer**2<=M*M*a2
    records.append({'terminal':terminal,'delta':delta,'horizon':H,'TV':observed,
                    'outer_TV_sum':outer,'parameter_pair_witness_distance_squared':a2,
                    'M':M,'squared_stability_margin':M*M*a2-outer*outer})

# Boundary unitary attack: native-only words carry no information about final Y.
N=250
U=s.Matrix([[Q(N*N-1,N*N+1)+s.I*Q(2*N,N*N+1),0],
            [0,Q(N*N-1,N*N+1)-s.I*Q(2*N,N*N+1)]])
assert simp(U.conjugate().T*U)==I
assert choi([(1,U)]).rank()==1
state=Px[0]
short_errors=[]
long_error=None
for length in range(99):
    assert state.trace()==1
    error=abs(s.simplify(s.trace(Py[0]*state)-Q(1,2)))
    if length<=7:short_errors.append(error)
    if length==98:long_error=error
    state=simp(U*state*U.conjugate().T)
assert max(short_errors)<Q(1,16)
assert long_error>Q(499,1000)

def encode(x):
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    if isinstance(x,s.Basic):return str(x)
    return x
report={'status':'PASS independent exact relation and CP stability diagnostics',
 'source_sha256':SOURCE_HASH,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'source_calls':0,'episode_starts':0,'rng_calls':0,'generic_QE_executed':False,'candidate_feasibility_executed':False,
 'equivalent_gauge_pair':equiv,'perturbed_pair':different,
 'physical_separation_of_equivalent_models_squared':parameter_sq(bar,barprime),
 'feedback_clock_terminal_checks':len(records),'records':records,
 'terminal_seed_omission_attack':{'d':2,'L':7,'unitary_parameter_N':N,
    'all_native_word_probabilities':1,'native_only_F':0,
    'max_short_terminal_probability_difference':max(short_errors),
    'max_short_terminal_probability_difference_float':float(max(short_errors)),
    'long_horizon':98,'long_terminal_TV_float':float(long_error),
    'exact_long_TV_above_0_499':True,'exact_short_max_below_0_0625':True}}
(ROOT/'short_word_modulus_independent_check.json').write_text(json.dumps(encode(report),indent=2)+'\n')
print(json.dumps(encode({k:v for k,v in report.items() if k not in ['records','terminal_seed_omission_attack']}),indent=2))
print('terminal attack:',json.dumps({k:encode(v) for k,v in report['terminal_seed_omission_attack'].items() if k!='max_short_terminal_probability_difference'},indent=2))
