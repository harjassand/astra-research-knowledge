"""Bounded deterministic tests; all generator checks retain all eight sites."""
from fractions import Fraction as F
from decimal import Decimal
import json
import random
from pathlib import Path
import numpy as np
import verify_slab as v

def point_exact(cores,x,order):
    z=[F(1)]
    for i,g in enumerate(cores):
        z=[sum((a*F.from_float(float(g[k,x[order[i]],j])) for k,a in enumerate(z)),F(0)) for j in range(g.shape[2])]
    return z[0]

def mass_exact(cores):
    z=[F(1)]
    for g in cores:
        local=[[sum((F.from_float(float(x)) for x in g[i,:,j]),F(0)) for j in range(g.shape[2])] for i in range(g.shape[0])]
        z=[sum((a*local[i][j] for i,a in enumerate(z)),F(0)) for j in range(g.shape[2])]
    return z[0]

def run():
    checks=0
    def check(b):
        nonlocal checks
        assert b
        checks+=1
    col,over=v.column(v.INITIAL)
    check(len(col)==37)
    check(col[v.INITIAL]==-F('114319.516'))
    check(sum(col.values(),over)==0)
    check(over==0)
    for x,a in col.items(): check(v.predecessors(x).get(v.INITIAL,0)==a)
    # Actual target and actual outward cap, never a smaller substitute model.
    check(v.column((15,)*8)==({},F(0)))
    y=(16,15,15,15,15,15,15,15)
    check(v.predecessors((15,)*8)[y]==v.death(16))
    check((15,)*8 not in v.predecessors(y))
    fullcap=(162,)*8
    c,o=v.column(fullcap)
    check(o==8*v.birth(162)+20*v.DIFF*162)
    check(sum(c.values(),o)==0)
    rng=random.Random(20261016)
    for _ in range(25):
        y=tuple(rng.randrange(163) for _ in range(8))
        c,o=v.column(y); check(sum(c.values(),o)==0)
        for x,a in c.items(): check(v.predecessors(x).get(y,0)==a)
    # Signed temporal cross terms: integral (1-2u)^2 = 1/3, not 7/3.
    p=[v.RI.exact(1),v.RI.exact(-2)]
    sq=v.integrated_square(p,F(1)); check(sq.lo==sq.hi==F(1,3))
    check(v.integrated_abs_lower(p,F(1),1)==0)
    check(v.integrated_abs_lower(p,F(1),2)==F(1,2))
    check(v.integrated_abs_lower(p,F(1),256)==F(1,2))
    # T_3(2u-1)=32u^3-48u^2+18u-1.
    p=v.cheb_to_power_u([v.RI.exact(0)]*3+[v.RI.exact(1)])
    check([x.lo for x in p]==list(map(F,[-1,18,-48,32])))
    check(all(x.lo==x.hi for x in p))
    # Independent exact-rational check of directed contractions on full 163^8 TT.
    nr=np.random.default_rng(20261016)
    ranks=[1,2,2,2,2,2,2,2,1]
    cores=[nr.normal(size=(ranks[i],163,ranks[i+1])).astype(np.float64) for i in range(8)]
    dc=v.DecimalContractor(35)
    for x in [v.INITIAL,(15,)*8,(162,)*8,tuple(range(8))]:
        enclosure=dc.point(cores,x,v.ORDER)
        exact=point_exact(cores,x,v.ORDER)
        check(enclosure.lo<=exact<=enclosure.hi)
    enclosure=dc.functional(cores)
    exact=mass_exact(cores)
    check(enclosure.lo<=exact<=enclosure.hi)
    sign=np.array([(-1.)**n for n in range(163)])
    enclosure=dc.functional(cores,[[Decimal(int(x)) for x in sign]]*8)
    exact=mass_exact([g*sign[None,:,None] for g in cores])
    check(enclosure.lo<=exact<=enclosure.hi)
    derivative_parity=sum((a*(-1)**sum(x) for x,a in col.items()),F(0))
    check(derivative_parity==-16*(v.birth(50)+v.death(50)))
    # The actual delta has an exact point contraction and exact sparse derivative.
    delta=[np.eye(163,dtype=np.float64)[50].reshape(1,163,1) for _ in range(8)]
    check(dc.point(delta,v.INITIAL,v.ORDER)==v.RI.exact(1))
    check(dc.functional(delta)==v.RI.exact(1))
    for x in col:
        derivative=sum((dc.point(delta,y,v.ORDER)*a for y,a in v.predecessors(x).items()),v.ZERO)
        check(derivative==v.RI.exact(col[x]))
    report={'status':'PASS','checks':checks,'initial_derivative_support':len(col),'initial_escape_rate_exact':str(-col[v.INITIAL]),'model_sites':8,'physical_count_max':162,'full_edges':v.EDGES,'new_simulation_or_fit':False,'tests':'Exact actual-model column conservation and absorption; full-operator sparse derivative; signed temporal Gram; dyadic-bin lower bound; directed Decimal contraction vs exact Fraction.'}
    Path(__file__).with_name('self_tests.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__': run()
