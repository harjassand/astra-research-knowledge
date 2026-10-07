from fractions import Fraction
from math import factorial
import json
from pathlib import Path
from time import perf_counter

# Species order A,B,C. Unit-rate reversible edges.
REACTIONS=[((1,0,1),(1,1,0)),((1,1,0),(1,0,1)),
           ((1,1,0),(0,1,0)),((0,1,0),(1,1,0)),
           ((0,0,1),(0,0,0)),((0,0,0),(0,0,1))]
COMPLEXES=sorted(set(z for reaction in REACTIONS for z in reaction))

def ff(x,y):
    z=1
    for xi,yi in zip(x,y):
        if xi<yi: return 0
        z*=factorial(xi)//factorial(xi-yi)
    return z

def potential_factor(x):
    # exp(F(x)), computed as an integer residual factorial minimum.
    return min(__import__('functools').reduce(lambda a,b:a*b,
               (factorial(xi-yi) for xi,yi in zip(x,y)),1)
               for y in COMPLEXES if all(xi>=yi for xi,yi in zip(x,y)))

def jumps(x):
    for y,yp in REACTIONS:
        rate=ff(x,y)
        if rate:
            yield rate,tuple(xi-yi+zi for xi,yi,zi in zip(x,y,yp))

def weight(x):
    return Fraction(1,factorial(x[0])*factorial(x[1])*factorial(x[2]))

def check():
    started=perf_counter()
    cases=0; drift_rows=[]
    # Exact rational identity for exp(F), not floating logs.
    for a in range(2,121):
        x=(a,0,1); e=potential_factor(x)
        assert e==factorial(a-1)
        ratios=[(rate,Fraction(potential_factor(xp),e),xp) for rate,xp in jumps(x)]
        assert ratios==[(a,Fraction(1),(a,1,0)),(1,Fraction(a),(a,0,0)),(1,Fraction(1),(a,0,2))]
        drift=sum(rate*(ratio-1) for rate,ratio,_ in ratios)
        assert drift==a-1
        drift_rows.append({'A':a,'state':x,'E_F_drift_over_E_F':str(drift),'F_drift':'log(A)'})
        cases+=1
    # At A=0,B=n,C=0, all enabled jumps are positive coordinate births.
    for n in range(1,121):
        x=(0,n,0)
        assert list(jumps(x))==[(n,(1,n,0)),(1,(0,n,1))]
        assert all(potential_factor(xp)==potential_factor(x) for _,xp in jumps(x))
        cases+=1
    # Product Poisson weights satisfy each reversible edge, pointwise.
    balances=0; class_checks=0
    for a in range(9):
      for b in range(9):
       for c in range(9):
        x=(a,b,c)
        for (y,yp) in REACTIONS:
            rate=ff(x,y)
            if not rate: continue
            xp=tuple(xi-yi+zi for xi,yi,zi in zip(x,y,yp))
            assert weight(x)*rate==weight(xp)*ff(xp,yp)
            balances+=1
            assert (a+b==0)==(xp[0]+xp[1]==0)
            class_checks+=1
    # Exact cube [1/2,2]^3 boundary signs; scalar monotonicity extends facets.
    half=Fraction(1,2); two=Fraction(2)
    def ode(x):
        a,b,c=x
        return (b*(1-a),a*(c-b),a*(b-c)+1-c)
    facet_checks=0
    for dim in range(3):
      for side in (half,two):
       for u in (half,two):
        for v in (half,two):
         x=[u,v];x.insert(dim,side)
         z=ode(x)[dim]
         assert z>=0 if side==half else z<=0
         facet_checks+=1
    out={'status':'PASS','source_order_max':max(sum(y) for y,_ in REACTIONS),
         'all_complex_order_max':max(sum(y) for y in COMPLEXES),
         'factorial_drift_cases':cases,'exact_edge_balance_checks':balances,
         'class_invariance_checks':class_checks,'cube_corner_facet_checks':facet_checks,
         'positive_factorial_drift_examples':drift_rows[:5],
         'elapsed_seconds':perf_counter()-started,
         'scope':'Finite exact identities only; infinite-class, recurrence, and no-go proofs are in INITIAL.txt.'}
    Path(__file__).with_name('exact_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': check()
