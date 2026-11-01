#!/usr/bin/env python3
"""Independent interval replay of the deterministic candidate variance.

Does not import either author solver. Reuses the independent scalar recurrence
from the prior scalar audit. A separate dyadic arithmetic implementation is
cross-checked against its Fraction-endpoint predecessor and exact fractions.
"""
import ast
from copy import deepcopy
from fractions import Fraction as R
import hashlib
import json
from pathlib import Path
import sys
import independent_scalar as ic

D=1<<120
FractionBox=ic.Box

def ceiling(n,d):
    assert d>0
    q,r=divmod(n,d)
    return q+(r!=0)

def ticks(x,up):
    x=R(x)*D
    return ceiling(x.numerator,x.denominator) if up else x.numerator//x.denominator

class Grid:
    __slots__=('a','b')
    def __init__(self,lower,upper=None):
        self.a=ticks(lower,False)
        self.b=ticks(lower if upper is None else upper,True)
        assert self.a<=self.b
    @classmethod
    def raw(cls,a,b):
        assert a<=b
        z=object.__new__(cls);z.a=a;z.b=b
        return z
    @property
    def lower(self):return R(self.a,D)
    @property
    def upper(self):return R(self.b,D)
    def __add__(self,y):
        if not isinstance(y,Grid):y=Grid(y)
        ic.count['add']+=1
        return Grid.raw(self.a+y.a,self.b+y.b)
    __radd__=__add__
    def __neg__(self):return Grid.raw(-self.b,-self.a)
    def __sub__(self,y):return self+(-y if isinstance(y,Grid) else -R(y))
    def __mul__(self,y):
        if not isinstance(y,Grid):y=Grid(y)
        ic.count['mul']+=1
        products=(self.a*y.a,self.a*y.b,self.b*y.a,self.b*y.b)
        return Grid.raw(min(products)//D,ceiling(max(products),D))
    __rmul__=__mul__
    def inv(self):
        ic.count['div']+=1
        assert self.a>0 or self.b<0
        if self.b<0:return -((-self).inv())
        return Grid.raw(D*D//self.b,ceiling(D*D,self.a))
    def __truediv__(self,y):
        if not isinstance(y,Grid):y=Grid(y)
        return self*y.inv()
    def power(self,n):
        result=Grid(1)
        for _ in range(n):result=result*self
        return result
    def contains(self,x):return self.lower<=x<=self.upper

ic.Box=Grid

def expbox(x):
    assert x.a>=0
    scales=0
    while x.b>D//8:
        x=x/2;scales+=1
    term=Grid(1);total=term
    for j in range(1,19):
        term=term*x/j
        total=total+term
    first=term*x/19
    tail=first/(Grid(1)-x/20)
    total=total+Grid.raw(0,tail.b)
    for _ in range(scales):total=total*total
    return total

def negative_exp(x):return expbox(x).inv()
def reciprocal_power(x,n):return x.power(n).inv()

def forward(degree,initial):
    # Independent sparse recurrence, not the author's convolution arrays.
    p={}
    for n in range(degree):
        sq=ic.product(p,p);fourth=ic.product(sq,sq)
        c=(R(2) if n==2 else R(0))+3*sq.get(n-1,R(0))+R(9,8)*fourth.get(n,R(0))
        if c:p[n+1]=c/(n+1)
    assert all(j%5==3 and c>=0 for j,c in p.items())
    t=R(1,2);residual=R(initial['residual_max']);L=R(initial['lipschitz'])
    cubic=residual/(t*t*(3-L*t));C=R(84,125)
    assert ic.evaluate(p,t)+cubic*t**3<R(1,4)
    assert ic.evaluate(p,t)/t**3+cubic<C
    coeff=[Grid(p.get(j,R(0))) for j in range(3,degree+1,5)]
    def value(s):
        ss=Grid(s);x=ss.power(5)
        v=coeff[-1]
        for c in coeff[-2::-1]:v=v*x+c
        cube=ss.power(3);pp=v*cube
        return Grid.raw(pp.a,(pp+cubic*cube).b)
    return value,cubic,C

def rectangles(levels,qs):
    out=Grid(0)
    for i in range(len(levels)-1):
        dl=Grid.raw(max(0,levels[i+1].a-levels[i].b),levels[i+1].b-levels[i].a)
        lower=Grid.raw(qs[i+1].a,qs[i+1].a).power(2)*Grid.raw(dl.a,dl.a)
        upper=Grid.raw(qs[i].b,qs[i].b).power(2)*Grid.raw(dl.b,dl.b)
        out=out+Grid.raw(lower.a,upper.b)
    return out

def q_interval(J):return Grid.raw(max(0,D-J.b),min(D,D-J.a))

def compute(grid=10,startup_steps=1024,E=8,order=5):
    a,initial,init=ic.initial(78)
    forward_at,cubic,C=forward(78,init)
    ic.count.update(add=0,mul=0,div=0)
    t=R(1,2);s=initial;e=a
    nodes=[(a,s,s+R(3,4)*Grid(a).power(2))]
    pieces=[]
    hh=R(1,2**grid)
    steps=0
    while e<E:
        h=min(hh,R(E)-e)
        midpoint,_,_=ic.advance(e,h/2,s,order)
        end,_,_=ic.advance(e+h/2,h/2,midpoint,order)
        Lbegin=nodes[-1][2]
        Lmid=midpoint+R(3,4)*Grid(e+h/2).power(2)
        Lend=end+R(3,4)*Grid(e+h).power(2)
        assert Lbegin.a>0
        Hmid=reciprocal_power(Lmid,3)
        low=Grid.raw(Lbegin.a,Lbegin.a)
        vmax=R(1,2)*reciprocal_power(low,2)+R(3,2)*Grid(e+h)
        curvature=12*vmax*vmax*reciprocal_power(low,5)+3*vmax*reciprocal_power(low,7)+R(9,2)*reciprocal_power(low,4)
        error=curvature*Grid(h**3/24)
        hp=Hmid*Grid(h)+Grid.raw(-error.b,error.b)
        assert hp.b>=0
        pieces.append(Grid.raw(max(0,hp.a),hp.b))
        e+=h;s=end;nodes.append((e,s,Lend));steps+=1
    end=R(E);low,high=s.lower,s.upper
    Tmax=R(8,27)/end**3;U=high+Tmax
    leading=R(64,135)/end**5
    Hlo=leading-R(256,189)*U/end**7
    Hhi=leading-R(256,189)*low/end**7+R(2048,729)*low*low/end**9
    assert 0<Hlo<=Hhi<=leading
    htail=Grid(Hlo,Hhi)
    sensitivities=[None]*len(nodes)
    sensitivities[-1]=negative_exp(htail)
    for i in range(len(pieces)-1,-1,-1):
        htail=htail+pieces[i]
        sensitivities[i]=negative_exp(htail)
    inverse=rectangles([x[2] for x in nodes],[q_interval(x) for x in sensitivities])
    e_gap=a-R(init['forward_e_lower'])
    Jhalf=Grid.raw((sensitivities[0]*Grid(1-8*e_gap)).a,sensitivities[0].b)
    assert 0<Jhalf.a<Jhalf.b<D
    klo=R(2,3)/(1+R(3,4)*C*C*t**5)
    khi=R(3,2)*C*C
    levels=[];qs=[]
    for j in range(startup_steps+1):
        ss=t*R(j,startup_steps);ee=forward_at(ss)
        levels.append(Grid(ss)+R(3,4)*ee*ee)
        if j==0:J=Grid(0)
        else:
            integral=Grid(klo*(t**5-ss**5)/5,khi*(t**5-ss**5)/5)
            J=Jhalf*Grid((ss/t)**2)*expbox(integral)
        qs.append(q_interval(J))
    startup=rectangles(levels,qs)
    gap=nodes[0][2].upper-levels[-1].lower
    assert gap>=0
    tail=R(4096,18225)*(R(8,117)/end**13+R(3,16)/end**8)
    total=startup+inverse+Grid(0,gap+tail)
    lo,hi=total.lower,total.upper
    charged=ic.ceil_grid(gap+tail)
    assert hi-lo == (startup.upper-startup.lower)+(inverse.upper-inverse.lower)+charged
    assert 0<=charged-gap-tail<R(1,D)
    assert hi-lo<R(1,1000)
    fields={'bits':120,'inverse_taylor_order':order,'inverse_grid_power':grid,
      'inverse_intervals':steps,'inverse_taylor_half_steps':2*steps,'startup_intervals':startup_steps,
      'terminal_e':str(end),'sigma_squared_lower':str(lo),'sigma_squared_upper':str(hi),
      'sigma_squared_decimal_outward':[ic.decimal(lo,10,False),ic.decimal(hi,10,True)],
      'total_width':str(hi-lo),'total_width_decimal_upper':ic.decimal(hi-lo,12,True),
      'startup_variance_lower':str(startup.lower),'startup_variance_upper':str(startup.upper),
      'startup_width':str(startup.upper-startup.lower),
      'inverse_variance_lower':str(inverse.lower),'inverse_variance_upper':str(inverse.upper),
      'inverse_width':str(inverse.upper-inverse.lower),'gap_variance_upper':str(gap),
      'tail_variance_upper':str(tail),'tail_and_gap_charged_width':str(charged),
      'tail_and_gap_rounding_excess':str(charged-gap-tail),'target_width_less_than_1e_minus_3':hi-lo<R(1,1000),
      'J_at_s_half_lower':str(Jhalf.lower),'J_at_s_half_upper':str(Jhalf.upper),
      'H_tail_lower':str(Hlo),'H_tail_upper':str(Hhi),'startup_cubic_barrier_delta':str(cubic),
      'startup_e_over_s3_upper':str(C),'startup_regular_integrand_coeff_lower':str(klo),
      'startup_regular_integrand_coeff_upper':str(khi),'inverse_s_terminal_width':str(s.upper-s.lower),
      'integer_interval_operations':ic.count.copy()}
    return fields,{'J_at_origin_exactly_zero':True,'inverse_nodes':len(nodes),'startup_nodes':len(levels),
                   'width_ledger_exact':True,'positive_ordered_sensitivity_tail':True}


def no_floats(value):
    assert not isinstance(value,float)
    if isinstance(value,dict):
        for x in value.values():no_floats(x)
    if isinstance(value,list):
        for x in value:no_floats(x)

def check(path):
    data=json.loads(path.read_text());no_floats(data)
    expected,extra=compute(data['inverse_grid_power'],data['startup_intervals'],R(data['terminal_e']),data['inverse_taylor_order'])
    for k,v in expected.items():assert data.get(k)==v,'mismatch: '+k
    no_floats(expected)
    out=dict(status='PASS_INDEPENDENT_DETERMINISTIC_VARIANCE_REPLAY',fields_exactly_replayed=len(expected),
       sigma_squared_decimal_outward=expected['sigma_squared_decimal_outward'],
       total_width_decimal_upper=expected['total_width_decimal_upper'],integer_interval_operations=expected['integer_interval_operations'],
       floats_in_proof_values=False,**extra)
    return out,expected

def main():
    path=Path(sys.argv[1]);result,expected=check(path)
    target=Path(__file__).with_name('INDEPENDENT_REPLAY.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    Path(__file__).with_name('INDEPENDENT_RECOMPUTED_FIELDS.json').write_text(json.dumps(expected,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
