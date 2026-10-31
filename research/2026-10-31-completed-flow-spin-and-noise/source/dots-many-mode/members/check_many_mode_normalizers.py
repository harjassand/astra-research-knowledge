"""Floating diagnostics of factorized row and first-event normalizers.
Not a certified arithmetic or quantum circuit implementation.
"""
import json,math
import numpy as np
rng=np.random.default_rng(310640)
rows=[]
for r in [1,2,4,8,16,32,64]:
  for repetition in range(20):
    lam=10.**rng.uniform(-8,12,size=r)
    G=10.**rng.uniform(-4,2,size=r)
    Gamma=sum(G);tau=1/(4*r*Gamma)
    t=tau*rng.uniform(.001,1)
    c=np.exp(G*tau/2)*(1+np.sqrt(G*tau/2))
    prod=float(np.prod(c));assert prod<2
    actual=[];jump=[]
    for l,gam in zip(lam,G):
      g=math.sqrt(gam*l);om=math.hypot(l,g);s=g*g/(om+l);d=om+l
      e=math.exp(-2*om*t);es=math.exp(s*t)
      aa=es*(d+s*e)/(2*om);dd=es*(s+d*e)/(2*om)
      bb=es*g*(-math.expm1(-2*om*t))/(2*om)
      actual.append(aa+bb);jump.append(2*math.sqrt(l)*(bb+dd))
    assert np.all(np.array(actual)<=c+1e-12)
    for i in range(r):
      row=jump[i]*prod/c[i]
      w=64*math.exp(Gamma*tau/2)*math.sqrt(lam[i]*math.exp(-4*lam[i]*t)+G[i])
      assert row<=w+1e-10,(r,i,row,w)
    mass=4+4096*math.exp(Gamma*tau)*sum((-np.expm1(-4*lam*tau))/4+G*tau)
    A=256*2**(((r).bit_length()+1)//2)
    assert mass<A*A
    rows.append({'modes':r,'row_bound_product':prod,'actual_row_product':float(np.prod(actual)),
                 'first_event_squared_mass':float(mass),'padded_normalizer':A})
print(json.dumps({'seed':310640,'scope':'floating diagnostic only','checks':len(rows),'rows':rows},indent=2))
