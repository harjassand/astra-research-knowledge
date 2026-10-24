"""New scratch research: rule acquisition and a certified finite-gate action.

This does not import or reconstruct historical Astra helpers.  All arithmetic
enclosures use Python Decimal directed rounding, including outward enclosures
around correctly rounded exp/sqrt.  The only floating solver is checked by a
separate interval residual calculation.
"""
from dataclasses import dataclass
from decimal import Decimal as D, Context, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN
from fractions import Fraction as F
from math import comb, factorial
import itertools
import json
import time
import numpy as np

DOWN = Context(prec=45, rounding=ROUND_FLOOR)
UP = Context(prec=45, rounding=ROUND_CEILING)
NEAR = Context(prec=45, rounding=ROUND_HALF_EVEN)

class I:
    __slots__ = ('lo','hi')
    def __init__(self, a, b=None):
        if isinstance(a, I):
            self.lo,self.hi=a.lo,a.hi
        elif isinstance(a,F):
            self.lo=DOWN.divide(D(a.numerator),D(a.denominator))
            self.hi=UP.divide(D(a.numerator),D(a.denominator))
        else:
            self.lo=D(a)
            self.hi=D(a) if b is None else D(b)
    def __add__(self,o):
        o=I(o); return I(DOWN.add(self.lo,o.lo),UP.add(self.hi,o.hi))
    __radd__=__add__
    def __neg__(self): return I(self.hi.copy_negate(),self.lo.copy_negate())
    def __sub__(self,o):
        o=I(o); return I(DOWN.subtract(self.lo,o.hi),UP.subtract(self.hi,o.lo))
    def __rsub__(self,o): return I(o)-self
    def __mul__(self,o):
        o=I(o)
        if self.lo>=0 and o.lo>=0:
            return I(DOWN.multiply(self.lo,o.lo),UP.multiply(self.hi,o.hi))
        ab=[(x,y) for x in (self.lo,self.hi) for y in (o.lo,o.hi)]
        return I(min(DOWN.multiply(x,y) for x,y in ab),max(UP.multiply(x,y) for x,y in ab))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=I(o); assert o.lo>0
        return self*I(DOWN.divide(D(1),o.hi),UP.divide(D(1),o.lo))
    def exp(self):
        return I(NEAR.exp(self.lo).next_minus(DOWN),NEAR.exp(self.hi).next_plus(UP))
    def sqrt(self):
        assert self.lo>=0
        return I(NEAR.sqrt(self.lo).next_minus(DOWN),NEAR.sqrt(self.hi).next_plus(UP))
    def midfloat(self): return float(NEAR.divide(NEAR.add(self.lo,self.hi),D(2)))
    def abs_upper(self): return max(self.lo.copy_abs(),self.hi.copy_abs())

@dataclass(frozen=True)
class Rule:
    guard: tuple
    update: tuple
    rate: F
    mark: str | None = None

def acquire(nsites, rules):
    """Obtain components from read/write scopes, not a supplied product claim.

    Restricted Boolean rule syntax: constant nonnegative rational rates,
    equality guards, fixed updates, and selected marked events.  A marked event
    must fully specify every relevant component.  Rejection is explicit.
    """
    parent=list(range(nsites))
    def root(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]]; i=parent[i]
        return i
    def union(i,j): parent[root(i)]=root(j)
    for r in rules:
        assert r.rate>=0
        if len(dict(r.guard))!=len(r.guard) or len(dict(r.update))!=len(r.update):
            raise ValueError('Repeated guard or update sites require normalization')
        for i,v in r.guard+r.update: assert 0<=i<nsites and v in (0,1)
        if r.mark is None:
            scope=sorted(set(i for i,v in r.guard+r.update))
            assert scope
            for i in scope[1:]: union(scope[0],i)
    components={}
    for i in range(nsites): components.setdefault(root(i),[]).append(i)
    gates=[r for r in rules if r.mark is not None]
    relevant=set(i for r in gates for i,v in r.guard)
    blocks=[v for v in components.values() if relevant.intersection(v)]
    local=[]
    for block in blocks:
        states=list(itertools.product((0,1),repeat=len(block)))
        index={s:i for i,s in enumerate(states)}
        Q=[[F(0) for _ in states] for _ in states]
        for r in rules:
            if r.mark is not None or not set(i for i,v in r.guard+r.update).intersection(block): continue
            assert set(i for i,v in r.guard+r.update)<=set(block)
            for s in states:
                env=dict(zip(block,s))
                if all(env[i]==v for i,v in r.guard):
                    new=env|dict(r.update)
                    j=index[tuple(new[i] for i in block)]; k=index[s]
                    if j!=k: Q[k][j]+=r.rate; Q[k][k]-=r.rate
        local.append((block,states,Q))
    active=set(i for block in blocks for i in block)
    for r in gates:
        if set(dict(r.guard))!=active:
            raise ValueError('Gate is not a fully specified configuration on the relevant modules')
    return local,gates

def moments(lambdas,off,order):
    a=[F(1)]+[F(0)]*order
    for lam,p in zip(lambdas,off):
        a=[a[d]+p*sum(F(comb(d,j))*a[j]*lam**(d-j) for j in range(d)) for d in range(order+1)]
    return a

def experiment(n=80, steps=1000, horizon=10):
    started=time.time()
    lambdas=[1+F(1,2**i) for i in range(1,n+1)]
    on=F(n-1,n); off=1-on; kappa=F(1)
    rules=[]
    for i,lam in enumerate(lambdas):
        rules += [Rule(((i,0),),((i,1),),on*lam),Rule(((i,1),),((i,0),),off*lam)]
    rules.append(Rule(tuple((i,1) for i in range(n)),(),kappa,'product'))
    local,gates=acquire(n,rules)
    assert len(local)==n and all(len(s)==2 for b,s,Q in local)
    # Actual overlapping guard must be rejected, rather than accepted by a
    # false low-rank-hazard shortcut.  Keep all modules relevant through gate2.
    bad=rules+[Rule(((0,1),),(),F(1),'wildcard')]
    try: acquire(n,bad)
    except ValueError: wildcard_rejected=True
    else: raise AssertionError('Wildcard accepted')

    # Obtain the return kernel from the acquired generators and gate.  The
    # product formula specializes the compiler output to binary modules.
    gate=gates[0]; target=dict(gate.guard)
    lambdas=[]; ons=[]; offs=[]
    for block,states,Q in local:
        alpha,beta=Q[0][1],Q[1][0]
        lam=alpha+beta
        assert lam>0
        stationary=(alpha if target[block[0]]==1 else beta)/lam
        lambdas.append(lam); ons.append(stationary); offs.append(1-stationary)
    kappa=gate.rate
    ls=[I(x) for x in lambdas]; pos=[I(x) for x in ons]; pfs=[I(x) for x in offs]; kap=I(kappa)
    def K(t):
        prod=I(1)
        for lam,po,pf in zip(ls,pos,pfs): prod=prod*(po+pf*(-lam*t).exp())
        return kap*prod
    h=F(horizon,steps); hi=I(h)
    # Four-point Gauss-Legendre on [0,1], algebraic interval nodes/weights.
    zeta=(I(F(6,5))).sqrt()
    xbig=((I(3)+2*zeta)/7).sqrt(); xsmall=((I(3)-2*zeta)/7).sqrt()
    root30=I(30).sqrt()
    wbig=(18-root30)/72; wsmall=(18+root30)/72
    nodes=[((1-xbig)/2,wbig),((1-xsmall)/2,wsmall),((1+xsmall)/2,wsmall),((1+xbig)/2,wbig)]
    mom=moments(lambdas,offs,8)
    # Gauss error: h^9 (4!)^4/[9 (8!)^3] sup |(w K)^(8)|.
    ge=F(factorial(4)**4,9*factorial(8)**3)*h**9*kappa*(mom[8]+8*mom[7]/h)
    err=I(ge)
    left=[I(0)]; right=[I(0)]; b=[]
    for j in range(steps+1):
        b.append(K(I(j)*hi))
        if j==0: continue
        a=I(0); c=I(0)
        for z,w in nodes:
            kval=K((I(j-1)+z)*hi)
            a=a+w*z*kval; c=c+w*(1-z)*kval
        a=a*hi; c=c*hi
        left.append(I(DOWN.subtract(a.lo,err.hi),UP.add(a.hi,err.hi)))
        right.append(I(DOWN.subtract(c.lo,err.hi),UP.add(c.hi,err.hi)))
    weights=[I(0)]+[left[j]+right[j+1] for j in range(1,steps)]
    wf=np.array([w.midfloat() for w in weights])
    lf=np.array([w.midfloat() for w in left])
    bf=np.array([w.midfloat() for w in b])
    density=np.zeros(steps+1); density[0]=bf[0]
    denominator=1+right[1].midfloat()
    for j in range(1,steps+1):
        density[j]=(bf[j]-density[0]*lf[j]-np.dot(density[1:j],wf[j-1:0:-1]))/denominator
    # All approximate values are now exact binary64 rationals inside intervals.
    fi=[I(D.from_float(float(v))) for v in density]
    knot_abs=[(fi[0]-b[0]).abs_upper()]
    for j in range(1,steps+1):
        r=fi[j]*(1+right[1])+fi[0]*left[j]-b[j]
        for l in range(1,j): r=r+fi[l]*weights[j-l]
        knot_abs.append(r.abs_upper())
    assert min(density)>=0
    mass=hi*(sum(fi[1:-1],I(0))+(fi[0]+fi[-1])/2)
    assert mass.hi<=1
    tvf=sum((I((fi[j+1]-fi[j]).abs_upper()) for j in range(steps)),I(0))
    # Piecewise-linear residual interpolation: integral error <=h²/8 integral |r''|.
    curvature=kap*tvf+2*kap*I(mom[1])*mass+kap*I(mom[1])
    knot_bound=hi*(I(knot_abs[0])+I(knot_abs[-1])+2*sum((I(x) for x in knot_abs[1:-1]),I(0)))/2
    residual=knot_bound+I(h*h/F(8))*curvature
    pi=I(1)
    for probability in ons: pi=pi*I(probability)
    mean=I(1)/(kap*pi)
    selected=[]
    for t in [0.25,0.5,1,2,5,10]:
        j=round(t/float(h))
        cm=hi*(sum(fi[1:j],I(0))+(fi[0]+fi[j])/2)
        # The global certificate also bounds every earlier-time CDF.
        selected.append({'time':t,'cdf_approx':cm.midfloat(),'lower':str(max(D(0),DOWN.subtract(cm.lo,residual.hi))),'upper':str(min(D(1),UP.add(cm.hi,residual.hi)))})
    return {
      'new_work':True,'sites':n,'silent_rules':len(rules)-1,'gates':len(gates),
      'acquired_local_states':sum(len(s) for b,s,Q in local),
      'unexpanded_configurations':str(2**n),'wildcard_rejected':wildcard_rejected,
      'time_step':str(h),'horizon':horizon,'density_nonnegative':True,
      'mass_interval':[str(mass.lo),str(mass.hi)],
      'gauss_weight_error_bound':str(err.hi),'max_interval_knot_residual':str(max(knot_abs)),
      'residual_integral_upper':str(residual.hi),'first_event_law_TV_upper':str(residual.hi),
      'mean_interevent_time_interval':[str(mean.lo),str(mean.hi)],'cdf':selected,
      'elapsed_seconds':time.time()-started
    }

if __name__=='__main__':
    result=experiment()
    print(json.dumps(result,indent=2))
    with open('pro3_gate_experiment_result.json','w') as f: json.dump(result,f,indent=2)
