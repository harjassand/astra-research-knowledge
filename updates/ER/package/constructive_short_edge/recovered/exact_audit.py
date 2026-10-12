"""Exact rational diagnostics; NOT the full spectral algorithm or its runtime test."""
from __future__ import annotations
from dataclasses import asdict
import json, math, random
from pathlib import Path
import sympy as sp
from cell_repair import enclosing_cell_repair, dot

HERE = Path(__file__).resolve().parent
checks = []
def record(name, condition=True, **data):
    if not condition:
        raise AssertionError(name)
    checks.append(dict(name=name, passed=True, **data))

def cube(n):
    A=[]; b=[]
    for j in range(n):
        row=[0]*n; row[j]=1; A.append(row); b.append(1)
        row=[0]*n; row[j]=-1; A.append(row); b.append(0)
    return A,b

def report_repair(name, r):
    data=asdict(r)
    data['point']=[str(t) for t in r.point]
    record(name, **data)

# A singleton fractional cost slice: exact output is not dyadic.
A,b=cube(2)
r=enclosing_cell_repair([sp.Rational(1,3),sp.Rational(2,3)], A,b,
        [[1,1]],[1], [[1,0]],[sp.Rational(1,3)], mesh_bits=14)
record('nondyadic_exact_cost_slice', r.point==[sp.Rational(1,3),sp.Rational(2,3)])
report_repair('nondyadic_repair_details',r)

# Arbitrarily long candidate denominator, with fixed original cost target.
for bits in [64,256,1024,2048]:
    e=sp.Rational(1,2**bits+1)
    x=[sp.Rational(1,2)+e,sp.Rational(1,2)-e,
       sp.Rational(1,2)+2*e,sp.Rational(1,2)-2*e]
    A,b=cube(4)
    r=enclosing_cell_repair(x,A,b,[[1]*4],[2],[[1,1,0,0]],[1],mesh_bits=18)
    record(f'denominator_reset_{bits}',r.output_bits<=32)
    report_repair(f'denominator_reset_details_{bits}',r)

# Rank face event with every coordinate fractional.
A,b=cube(5); A.append([1,1,0,0,0]); b.append(1)
x=[sp.Rational(3,10)]*2+[sp.Rational(7,15)]*3
h=[3,3,-2,-2,-2]; t=sp.Rational(1,15)
y=[a+t*v for a,v in zip(x,h)]
record('rank_face_event_fractional',all(0<q<1 for q in y) and dot(A[-1],y)==1)
r=enclosing_cell_repair(y,A,b,[[1]*5],[2],[[0,0,1,2,-3]],[0],mesh_bits=14)
record('rank_face_not_released',dot([1,1,0,0,0],r.point)==1)
report_repair('rank_face_repair_details',r)

# Repair may descend to a smaller original face, but never releases one.
A,b=cube(2); tiny=sp.Rational(1,2**1024+1)
r=enclosing_cell_repair([1-tiny,sp.Rational(1,3)],A,b,
                       fixed_equations=[[0,1]],fixed_targets=[sp.Rational(1,3)],mesh_bits=16)
record('repair_can_descend',r.face_dimension_before==2 and r.face_dimension_after==1)
report_repair('repair_face_descent_details',r)

# A vertex of the clipped LP must not be mistaken for an original vertex.
A,b=cube(3)
r=enclosing_cell_repair([sp.Rational(1,3)]*3,A,b,[[1]*3],[1],mesh_bits=12)
record('artificial_cell_vertex_not_original',r.face_dimension_after==2 and all(0<t<1 for t in r.point))
report_repair('artificial_cell_vertex_details',r)

rng=random.Random(1302026)
for test in range(16):
    n=3+test%4
    A,b=cube(n)
    rank=1+(test%(n-1)); anchor=[sp.Rational(rank,n)]*n
    cost=[rng.randint(-4,4) for _ in range(n)]
    cost[0],cost[1]=0,1
    E=sp.Matrix([[1]*n,cost]); null=E.nullspace()
    v=null[test%len(null)]
    denom=sp.ilcm(*[t.q for t in v]); v=[t*denom for t in v]
    tiny=sp.Rational(1,2**(80+37*test)+1)
    x=[a+tiny*d for a,d in zip(anchor,v)]
    r=enclosing_cell_repair(x,A,b,[[1]*n],[rank],[cost],[dot(cost,anchor)],mesh_bits=10+test%8)
    record(f'random_exact_slice_{test}',dot(cost,r.point)==dot(cost,anchor) and r.output_bits<256,
           input_bits=r.input_bits,output_bits=r.output_bits,n=n)

# Exact count of the hidden-pairing Boolean-membership obstruction.
def pairings(items):
    if not items:
        yield []
    else:
        a=items[0]
        for j in range(1,len(items)):
            b=items[j]
            rest=items[1:j]+items[j+1:]
            for tail in pairings(rest):
                yield [(a,b)]+tail
for rank in range(1,7):
    total=accepted=0
    for pairing in pairings(list(range(2*rank))):
        total+=1
        accepted+=int(all((a<rank)!=(b<rank) for a,b in pairing))
    expected=sp.Rational(2**rank,math.comb(2*rank,rank))
    record(f'hidden_pairing_count_{rank}',sp.Rational(accepted,total)==expected,
           total_pairings=total,accepted=accepted,probability=str(expected))

# Weighted replication reduction: exact operator and edge-budget identities.
for test in range(30):
    n=3+test%8
    blocks=[]; cursor=0
    while cursor<n:
        size=min(n-cursor,rng.randint(1,4)); blocks.append(list(range(cursor,cursor+size)));cursor+=size
    mu=[sp.Rational(rng.randint(0,12),rng.randint(1,13)) for _ in range(n)]
    if all(t==0 for t in mu):mu[0]=sp.Rational(1)
    budget=max(sum(mu[j] for j in block) for block in blocks)
    clones=[max(1,int(sp.ceiling(n*w/budget))) for w in mu]
    record(f'weighted_size_{test}',sum(clones)<=n*n)
    record(f'weighted_edges_{test}',all(sum(clones[j] for j in block)<=2*n for block in blocks))
    # Pythagorean vector columns have exact prescribed Euclidean norms.
    for j in range(n):
        a=sp.Matrix([sp.Rational(3,5)*mu[j],sp.Rational(4,5)*mu[j]])
        new=(sp.Rational(n,1)/budget/clones[j])*a
        assert (new.T*new)[0]<=1
        assert clones[j]*new==(sp.Rational(n,1)/budget)*a
    record(f'weighted_norm_and_map_{test}',budget=str(budget),clone_count=sum(clones))

# Nearest-integer cells of integral base polyhedra: exact residual ranks.
# Exhaustive tests use small coverage-plus-modular functions. Modular terms
# may be negative; neither coordinate positivity nor small capacity is assumed.
for test in range(24):
    n=3+test%5
    masks=list(range(1<<n)); full=(1<<n)-1
    cover=[(rng.randrange(1,1<<n),rng.randint(1,7)) for _ in range(n+2)]
    modular=[rng.randint(-1000000,1000000) for _ in range(n)]
    fv=[sum(w for edge,w in cover if edge & S)+
        sum(modular[j] for j in range(n) if S>>j&1) for S in masks]
    vertices=[]
    for _ in range(3):
        order=list(range(n));rng.shuffle(order);S=0;v=[0]*n
        for j in order:
            v[j]=fv[S|(1<<j)]-fv[S];S|=1<<j
        vertices.append(v)
    x=[sp.Rational(sum(a*v[j] for a,v in zip([5,7,11],vertices)),23) for j in range(n)]
    a=[int(sp.floor(t)) for t in x]; residue=[t-floor for t,floor in zip(x,a)]
    hs=[fv[S]-sum(a[j] for j in range(n) if S>>j&1) for S in masks]
    assert min(hs)>=0
    rank=[min(hs[T]+(U & (full^T)).bit_count() for T in masks) for U in masks]
    assert rank[0]==0 and rank[full]==hs[full]
    for U in masks:
        assert 0<=rank[U]<=U.bit_count()
        for j in range(n):
            if not U>>j&1: assert 0<=rank[U|(1<<j)]-rank[U]<=1
        for V in masks:
            assert rank[U]+rank[V]>=rank[U|V]+rank[U&V]
    accepted=0
    for B in masks:
        values=[int(B>>j&1) for j in range(n)]
        original=(sum(a[j]+values[j] for j in range(n))==fv[full] and
                  all(sum(a[j]+values[j] for j in range(n) if S>>j&1)<=fv[S] for S in masks))
        residual=(B.bit_count()==rank[full] and
                  all((B&S).bit_count()<=rank[S] for S in masks))
        assert original==residual
        if original and all(values[j]==0 for j in range(n) if residue[j]==0):accepted+=1
    assert accepted>0
    record(f'integral_base_cell_{test}',n=n,integer_cell_base_count=accepted,
           maximum_integer_coordinate=max(abs(t) for t in a))

# The final bound and strict dimension reserve, using rational inequalities.
for k in range(1,1001):
    K=64*k; R=math.isqrt(K)
    assert R*R>=K/2
    assert 16*R*R+2*K+8*k+1<=1161*k
    N=8*k+1
    assert sp.Rational(N,k)-sp.Rational(35*N,K)-2>0
record('parameter_and_dimension_range',k_values=1000)

summary={'status':'Exact local/repair diagnostics, not an implementation of the complete spectral rounding algorithm',
         'number_of_checks':len(checks),'all_passed':True,'checks':checks}
(HERE/'exact_audit_results.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({'checks':len(checks),'all_passed':True,
                 'denominator_cases':[c for c in checks if c['name'].startswith('denominator_reset_details')]},indent=2))
