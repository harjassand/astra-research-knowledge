#!/usr/bin/env python3
"""Exact finite controls for the separately proved one-port obstructions.
No simulation and no infinite-tail conclusion from finite checking.
"""
from fractions import Fraction as F
from itertools import product
import json

Z=(0,0,0,0); A=(1,0,0,0); AB=(1,1,0,0); CD=(0,0,1,1)
AA=(2,0,0,0); AC=(1,0,1,0); AD=(1,0,0,1)
RX=[(Z,A,F(1)),(A,Z,F(1)),(AB,CD,F(1)),(CD,AB,F(1)),
    (AA,CD,F(1)),(CD,AA,F(1)),(AC,CD,F(1)),(CD,AC,F(2)),
    (AD,CD,F(1)),(CD,AD,F(1))]
def ff(n,k):
    ans=1
    for j in range(k): ans*=n-j
    return ans

def rate(x,r):
    u,_,k=r
    if any(xi<ui for xi,ui in zip(x,u)): return F(0)
    ans=k
    for xi,ui in zip(x,u): ans*=ff(xi,ui)
    return ans

def jump(x,r):
    u,v,_=r
    assert rate(x,r)>0
    return tuple(xi-ui+vi for xi,ui,vi in zip(x,u,v))

def R(x): return x[0]+min(x[2],x[3])
def rank(rows):
    rows=[list(map(F,row)) for row in rows]; p=0
    for j in range(4):
        i=next((i for i in range(p,len(rows)) if rows[i][j]),None)
        if i is None: continue
        rows[p],rows[i]=rows[i],rows[p]
        d=rows[p][j]; rows[p]=[q/d for q in rows[p]]
        for i in range(len(rows)):
            if i!=p:
                d=rows[i][j]; rows[i]=[a-d*b for a,b in zip(rows[i],rows[p])]
        p+=1
    return p

def encode(x):
    if isinstance(x,F): return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'
    if isinstance(x,dict): return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [encode(v) for v in x]
    return x

def main():
    vertices=set(u for u,_,_ in RX)|set(v for _,v,_ in RX)
    unseen=set(vertices); components=[]
    while unseen:
        seen={next(iter(unseen))}
        while True:
            extra={v for u,v,_ in RX if u in seen}|{u for u,v,_ in RX if v in seen}
            if extra<=seen: break
            seen|=extra
        components.append(sorted(seen)); unseen-=seen
    assert len(vertices)==7 and len(components)==2
    vectors=[tuple(v[i]-u[i] for i in range(4)) for u,v,_ in RX]
    assert rank(vectors)==4 and rank(vectors[2:])==3
    assert all(sum(u)==sum(v)==2 for u,v,_ in RX[2:])
    assert not set.intersection(*[{i for i,k in enumerate(c) if k} for c in vertices if sum(c)==2])
    assert all((tuple(2 if i==j else 0 for i in range(4)) in vertices)==(j==0) for j in range(4))
    # Every binary reaction is horizontal for total-count normal w.
    assert all(sum(v)-sum(u)==0 for u,v,_ in RX[2:])
    assert sum(RX[0][1])-sum(RX[0][0])==1
    # Exact enabled reversible paths 0->A->2A->CD->AX->X, including translations.
    paths=[]; path_checks=0
    for j,leaf in [(1,AB),(2,AC),(3,AD)]:
        unit=tuple(int(i==j) for i in range(4))
        path=[Z,A,AA,CD,leaf,unit]
        for surplus in [Z,(3,2,1,4),(10**20,1,0,2)]:
            translated=[tuple(xi+si for xi,si in zip(x,surplus)) for x in path]
            for seq in [translated,list(reversed(translated))]:
                for x,y in zip(seq,seq[1:]):
                    matches=[r for r in RX if rate(x,r)>0 and jump(x,r)==y]
                    assert matches; path_checks+=1
        paths.append(path)
    inventory_checks=inactive_checks=core_checks=0
    for x in product(range(8),repeat=4):
        a,b,c,d=x
        expected=[0,0,-1,1,-1+int(d<c),1-int(d<=c),-1+int(c<d),1-int(c<=d)]
        for r,delta in zip(RX[2:],expected):
            if rate(x,r):
                y=jump(x,r)
                assert R(y)-R(x)==delta
                assert R(x)==0 or R(y)>=1
                inventory_checks+=1
        any_internal=any(rate(x,r) for r in RX[2:])
        if R(x)==0: assert not any_internal
        if R(x)>0 and sum(x)>=2: assert any_internal
        inactive_checks+=1
        if a==0:
            # A=0 can be internally active; exactly iff C,D are both positive.
            assert any_internal==bool(c*d)
            core_checks+=1
    assert R((0,20,1,1))==1 and R((1,20,0,0))==1
    assert F(0,R((0,20,1,1)))==0 and F(1,R((1,20,0,0)))==1
    # Complex-balance leaf equations force a=c=1,d=1/2, while cd must be1.
    forced_a=forced_c=F(1); forced_d=F(1,2)
    assert forced_c*forced_d!=forced_a**2
    # Unit-rate network has detailed balance at all-ones (monomial convention).
    for j in range(0,len(RX),2):
        u,v,_=RX[j]; vv,uu,_=RX[j+1]
        assert u==uu and v==vv
    # Exact first-core lower bound via two consecutive specified first events.
    lower=[]
    for n in [1,2,10,10**6,10**50]:
        x=(1,n,0,0)
        total=sum(rate(x,r) for r in RX)
        assert total==n+2
        y=jump(x,RX[2]); assert y==(0,n-1,1,1)
        inner=sum(rate(y,r) for r in RX[2:]); assert inner==5
        total_y=sum(rate(y,r) for r in RX); assert total_y==6
        p=rate(x,RX[2])/total*rate(y,RX[0])/total_y
        assert p==F(n,6*(n+2))
        # For t=7, the event alone makes expected t^DeltaN exceed one at n>12.
        if n>12: assert 7*p>1
        lower.append({'n':n,'p_up_lower':p,'gap_below_one_sixth':F(1,6)-p})
    # Exact affine coefficient rows underlying aggregate no-go, not numerical proof.
    # order (u_n,v_n,u_(n-1),F(2,n+1),C), generator + epsilon*v_n - C
    eps=F(1,4); rho=1-eps; q=2-eps
    for n in [2,3,20,10**20]:
        row=(F(n-1),eps-(n+1),F(1),F(1),F(-1))
        assert row[0]/(n-1)==1
        assert -row[1]/(n-1)==1+q/(n-1)
        if n>=20: assert rho*(1+q/(n-1))<F(7,8)
    # Raw negative control: no common A, no direct use of old common-seed theorem.
    assert CD[0]==0 and all(u[0]>=1 for u,_,_ in RX[2:] if u!=CD)
    return {'status':'exact finite controls passed; asymptotic claims proved in note',
      'reaction_count':len(RX),'complex_count':len(vertices),'linkage_count':len(components),
      'internal_rank':3,'full_rank':4,'deficiency':1,
      'translated_reversible_path_edges_checked':path_checks,
      'enabled_internal_inventory_increments_checked':inventory_checks,
      'inactive_face_states_checked':inactive_checks,'A_zero_states_checked':core_checks,
      'fixture_complex_balance':'contradiction cd=1/2 versus cd=1',
      'all_unit_control':'detailed balance at all-ones',
      'first_core_lower_bounds':lower,
      'aggregate_no_go':'ordinary proof, all positive rates; finite rows checked only',
      'radial_template_no_go':'ordinary proof when 2a(t-1)>lambda',
      'scope':'No recurrence claim for the non-CB fixture; no infinite-tail conclusion from tests.'}
if __name__=='__main__': print(json.dumps(encode(main()),sort_keys=True,indent=2))
