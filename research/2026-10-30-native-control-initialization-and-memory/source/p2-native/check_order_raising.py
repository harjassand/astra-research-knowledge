#!/usr/bin/env python3
"""Exact abstract order-raising identity and actual same-memory pulse checks.

The abstract coefficient field is Q[r]/(r^5-2); r is its positive real root.
L is central; D,M,N are arbitrary memory generators, and E is the first
data-dependent error after the native sign-group projection. No drift reversal.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np
from scipy.linalg import expm
from check_bus import fixture,kron,norm
from explore_word import base_word,symmetrize

ZERO=(F(0),)*5
ONE=(F(1),F(0),F(0),F(0),F(0))
R=(F(0),F(1),F(0),F(0),F(0))

def radd(a,b):return tuple(x+y for x,y in zip(a,b))
def rscale(a,s):return tuple(x*s for x in a)
def rmul(a,b):
    out=[F(0)]*5
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[(i+j)%5]+=x*y*(2 if i+j>=5 else 1)
    return tuple(out)
def rpow(a,n):
    out=ONE
    for _ in range(n):out=rmul(out,a)
    return out
def degree(key):
    word,l=key
    return sum({'D':1,'M':3,'N':5,'E':5}[x] for x in word)+3*l
def add(a,b):
    c=a.copy()
    for key,x in b.items():
        c[key]=radd(c.get(key,ZERO),x)
        if c[key]==ZERO:del c[key]
    return c
def scale(a,s):return {k:v for k,x in a.items() if (v:=rscale(x,s))!=ZERO}
def mul(a,b):
    c={}
    for (w,l),x in a.items():
        for (v,m),y in b.items():
            key=(w+v,l+m)
            if degree(key)<=6:c[key]=radd(c.get(key,ZERO),rmul(x,y))
    return {k:x for k,x in c.items() if x!=ZERO}
def exp(a):
    result={((),0):ONE};term=result.copy()
    for n in range(1,7):
        term=scale(mul(term,a),F(1,n));result=add(result,term)
    return result
def log(a):
    q=add(a,{((),0):rscale(ONE,-1)});result={};term={((),0):ONE}
    for n in range(1,7):
        term=mul(term,q);result=add(result,scale(term,F((-1)**(n+1),n)))
    return result

def abstract_check():
    positive={(('D',),0):ONE,(('M',),0):ONE,((),1):ONE,(('N',),0):ONE,(('E',),0):ONE}
    negative={k:rscale(rpow(R,degree(k)),(-1 if k[1] or 'E' in k[0] else 1)) for k in positive}
    result=log(mul(mul(exp(positive),exp(negative)),exp(positive)))
    logical={k:x for k,x in result.items() if k[1] or 'E' in k[0]}
    assert logical=={((),1):radd(rscale(ONE,2),rscale(rpow(R,3),-1))},logical
    assert not any(degree(k)%2==0 for k in result)
    outer=scale(positive,F(16))
    doubled={k:rscale(ONE,2**degree(k)*(-1 if k[1] or 'E' in k[0] else 1)) for k in positive}
    integer_result=log(mul(mul(exp(outer),exp(doubled)),exp(outer)))
    integer_logical={k:x for k,x in integer_result.items() if k[1] or 'E' in k[0]}
    assert integer_logical=={((),1):rscale(ONE,24)},integer_logical
    assert not any(degree(k)%2==0 for k in integer_result)
    return {'scope':'Exact rational algebraic-number calculation in the stated abstract quotient; root check only.',
            'field':'Q[r]/(r^5-2), positive real r=2^(1/5)',
            'log_through_degree_six':{(''.join(w) or 'I')+f'*L^{l}':[str(v) for v in a]
                                      for (w,l),a in result.items()},
            'integer_clock_composition':'S_+(tau)^16 S_-(2*tau) S_+(tau)^16',
            'integer_clock_log_through_degree_six':{(''.join(w) or 'I')+f'*L^{l}':[str(v) for v in a]
                                      for (w,l),a in integer_result.items()}}


GROUP=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
GROUP_PAL=GROUP+list(reversed(GROUP))

def native_cycle(ops,d,tau,control_signs=(1,1,1)):
    primitive={(a,s):expm(-1j*tau*(d+s*control_signs['ABC'.index(a)]*ops[a]))
               for a in 'ABC' for s in [-1,1]}
    u=np.eye(16,dtype=complex)
    for a,s in symmetrize(base_word()):u=primitive[(a,s)]@u
    return u

def projected_cycle(ops,d,tau,chirality=1):
    # Flip C to reverse the useful term while retaining the physical drift.
    cache={g:native_cycle(ops,d,tau,(g[0],g[1],g[2]*chirality)) for g in GROUP}
    u=np.eye(16,dtype=complex)
    for g in GROUP_PAL:u=cache[g]@u
    return u

def raised_cycle(ops,d,tau):
    r=2**.2
    plus=projected_cycle(ops,d,tau,1)
    minus=projected_cycle(ops,d,r*tau,-1)
    return plus@minus@plus

def integer_raised_cycle(ops,d,tau):
    plus=projected_cycle(ops,d,tau,1)
    minus=projected_cycle(ops,d,2*tau,-1)
    outer=np.linalg.matrix_power(plus,16)
    return outer@minus@outer

def product_gauge(u,logical):
    residual=kron(logical.conj().T,np.eye(4))@u
    gauge=np.einsum('aiaj->ij',residual.reshape(4,4,4,4))/4
    a,_,b=np.linalg.svd(gauge)
    return a@b

def physical_checks():
    ops,d,hm,bs,target,triple=fixture()
    r=2**.2;coefficient=512*triple*(2-r**3)
    angle=np.pi/4;rows=[]
    for maximum in [.04,.025,.016,.01,.006]:
        n=max(1,int(np.ceil(angle/(coefficient*maximum**3))))
        tau=(angle/(coefficient*n))**(1/3)
        w=raised_cycle(ops,d,tau)
        local=expm(1j*coefficient*tau**3*target)
        memory=product_gauge(w,local)
        per_cycle=norm(w-kron(local,memory))
        actual=np.linalg.matrix_power(w,n)
        desired=expm(1j*angle*target)
        chosen_memory=np.linalg.matrix_power(memory,n)
        whole_gauge=product_gauge(actual,desired)
        row={'tau':tau,'cycles':n,'native_segments':2304*n,
             'physical_duration':n*768*(2+r)*tau,
             'one_cycle_product_error':per_cycle,
             'telescoping_bound':n*per_cycle,
             'fixed_cycle_memory_reference_error':norm(actual-kron(desired,chosen_memory)),
             'whole_gate_frobenius_gauge_error':norm(actual-kron(desired,whole_gauge)),
             'unitarity_error':norm(actual.conj().T@actual-np.eye(16))}
        rows.append(row);print(json.dumps(row),flush=True)
    single=[]
    for tau in [.006,.004,.0025,.0016,.001]:
        w=raised_cycle(ops,d,tau);local=expm(1j*coefficient*tau**3*target)
        memory=product_gauge(w,local);error=norm(w-kron(local,memory))
        single.append({'tau':tau,'one_cycle_error':error,'error_over_tau_seven':error/tau**7,
                       'unitarity_error':norm(w.conj().T@w-np.eye(16))})
    return {'scope':'Finite root floating-point full-memory tests; product gauge is a chosen comparison unitary, not a physical reset or a claim of optimal operator-norm gauge.',
            'logical_coefficient':coefficient,'runs':rows,'single_cycle_asymptotic_check':single}

def main():
    abstract=abstract_check()
    Path(__file__).with_name('order_raising_certificate.json').write_text(json.dumps(abstract,indent=2)+'\n')
    physical=physical_checks()
    Path(__file__).with_name('order_raising_checks.json').write_text(json.dumps(physical,indent=2)+'\n')

if __name__=='__main__':main()
