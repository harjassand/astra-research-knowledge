#!/usr/bin/env python3
"""Exact four-state preparation example; no physical data or reset is executed."""
from fractions import Fraction as F
from pathlib import Path
import json
import hashlib


def mm(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def mv(a,v):
    return [sum(x*y for x,y in zip(row,v)) for row in a]


def serialize(v):
    if isinstance(v,F): return str(v)
    if isinstance(v,list): return [serialize(x) for x in v]
    if isinstance(v,dict): return {k:serialize(x) for k,x in v.items()}
    return v


def main():
    eps,beta,a,alpha=F(1,10),F(1,2),F(1,2),F(1)
    r=alpha/(alpha+1)
    states=[(-1,-1),(-1,1),(1,-1),(1,1)]
    n=len(states)
    pi=[(1+eps*h*y)/4 for h,y in states]
    w=[1+beta*y for h,y in states]
    mu=[p*ww for p,ww in zip(pi,w)]
    g=[1+a*h for h,y in states]
    init=[p*gg for p,gg in zip(pi,g)]
    yy=[F(y) for h,y in states]; hh=[F(h) for h,y in states]
    one=[F(1)]*n
    Q=[[F(0) for j in range(n)] for i in range(n)]
    W=[[F(0) for j in range(n)] for i in range(n)]
    Winf=[[F(0) for j in range(n)] for i in range(n)]
    for i,(h,y) in enumerate(states):
        mh=(beta+eps*h)/(1+beta*eps*h)
        for j,(hp,yp) in enumerate(states):
            if hp==h:
                p=(1+yp*mh)/2
                Winf[i][j]=p
                W[i][j]=(r if i==j else F(0))+(1-r)*p
                if j!=i: Q[i][j]=p
        Q[i][i]=-sum(Q[i])
    I=[[F(i==j) for j in range(n)] for i in range(n)]
    resolvent_left=[[alpha*I[i][j]-Q[i][j] for j in range(n)] for i in range(n)]
    assert mm(resolvent_left,W)==[[alpha*x for x in row] for row in I]
    assert mv(W,one)==one and mv(W,hh)==hh
    assert mm([mu],W)[0]==mu
    assert sum(pi)==sum(mu)==sum(init)==1
    for i in range(n):
        for j in range(n):
            assert W[i][j]>=0
            assert mu[i]*Q[i][j]==mu[j]*Q[j][i]
    m0=beta*(1-eps*eps)/(1-beta*beta*eps*eps)
    m1=eps*(1-beta*beta)/(1-beta*beta*eps*eps)
    b=(1-r)*m0
    kappa=r+(1-r)*m1*eps
    wy=mv(W,yy)
    leak=[wy[i]-b-kappa*yy[i] for i in range(n)]
    leak2=sum(p*x*x for p,x in zip(pi,leak))
    assert sum(p*x for p,x in zip(pi,leak))==0
    assert sum(p*y*x for p,y,x in zip(pi,yy,leak))==0
    assert leak2==(1-r)**2*m1*m1*(1-eps*eps)
    assert b/(1-kappa)==beta
    assert sum(p*x*x for p,x in zip(pi,g))==1+a*a
    rows=[]
    power=I
    for m in range(11):
        pred=sum(p*x for p,x in zip(init,mv(power,yy)))
        formula=r**m*a*eps+(1-r**m)*(m0+a*m1)
        assert pred==formula
        if m in [0,1,2,10]: rows.append({'calls':m,'actual_visible_mean':pred})
        power=mm(power,W)
    limit_mean=sum(p*x for p,x in zip(init,mv(Winf,yy)))
    gap=limit_mean-beta
    assert gap==m1*(a-beta*eps) and gap>0
    assert kappa==F(67,133) and leak2==F(99,70756)
    assert F(5,4)<=F(9,8)**2 and F(3)<=F(7,4)**2
    assert leak2<=F(1,25)**2 and kappa<=F(51,100)
    floor_upper=F(9,8)*F(7,4)*F(1,25)/(1-F(51,100))
    assert floor_upper==F(9,56)
    five_call_tv=(floor_upper+(1-floor_upper)*F(51,100)**5)/2
    assert five_call_tv<F(1,10)
    source=Path(__file__).with_name('FINITE_ERROR_BIASED_PREPARATION.md')
    result={'status':'PASS','scope':'Exact synthetic algebra; no physical acquisition.',
      'proof_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
      'epsilon':eps,'beta':beta,'initial_hidden_bias':a,'alpha':alpha,
      'pi':pi,'target_mu':mu,'initial_density':g,'Q':Q,'W':W,
      'initial_density_norm_squared':1+a*a,'quotient_kappa':kappa,
      'affine_b':b,'kernel_leakage_squared':leak2,
      'affine_target_mean':b/(1-kappa),'actual_infinite_preparation_mean':limit_mean,
      'persistent_mean_bias':gap,'persistent_endpoint_tv':gap/2,
      'density_contract_norm_squared_ceiling':F(5,4),
      'five_call_visible_tv_upper':five_call_tv,
      'finite_call_checks':rows}
    dest=Path(__file__).with_name('BIASED_PREPARATION_FLOOR_EXACT.json')
    dest.write_text(json.dumps(serialize(result),indent=2)+'\n')
    print(json.dumps({'status':'PASS','persistent_mean_bias':str(gap),
        'persistent_endpoint_tv':str(gap/2),'output':str(dest)},indent=2))


if __name__=='__main__': main()
