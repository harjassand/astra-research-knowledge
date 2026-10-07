"""Exact numerical certificate; no astronomical graph is materialized."""
from fractions import Fraction
from math import comb, gcd, isqrt, prod
import json
from pathlib import Path

def trial_prime(p):
    if p < 2:
        return False
    if p % 2 == 0:
        return p == 2
    return all(p % d for d in range(3, isqrt(p)+1, 2))

def pocklington(q, factors, witness):
    # Complete factorization of q-1: Lucas/Pocklington primality certificate.
    assert prod(p**e for p,e in factors.items()) == q-1
    assert all(trial_prime(p) for p in factors)
    assert pow(witness,q-1,q) == 1
    assert all(gcd(pow(witness,(q-1)//p,q)-1,q)==1 for p in factors)
    return {"q":q,"q_minus_one_factors":factors,"witness":witness}

def budget(q,r,N,rank_fraction=Fraction(1,2)):
    m=q**5
    rho=Fraction(N,m)
    mu=(q-1)*rho
    margin=mu-4*r*r
    assert margin>0
    # isqrt+1 is an integer upper bound for sqrt(q).
    E_fraction=Fraction((2*(isqrt(q)+1)+1)**2)*rho*(1-rho)/margin**2
    # rank_fraction multiplies rank_R >= rD/2.
    Delta_fraction=rank_fraction*r*rho/2-2-r*E_fraction
    # Triangle term plus an upper bound for rectangle term at error 1/(100rq).
    error_upper=Fraction(r,100*q)*rho*(q-1+rank_fraction/4)
    assert E_fraction<Fraction(1,2*r)
    assert Delta_fraction>error_upper
    return {"q":q,"r":r,"m_digits":len(str(m)),"N_digits":len(str(N)),
      "incidences_digits":len(str(N*(q-1))),
      "triangles_upper_digits":len(str(N*(q-1)*r*r)),
      "rho":str(rho),"mu":str(mu),"E_fraction_upper":str(E_fraction),
      "Delta_fraction_lower":str(Delta_fraction),"error_fraction_upper":str(error_upper),
      "E_fraction_decimal":float(E_fraction),"Delta_fraction_decimal":float(Delta_fraction),
      "error_fraction_decimal":float(error_upper)}

def run():
    q_old=2**61-1
    # Lucas-Lehmer certificate for the retained N27 prime.
    ll=4
    for _ in range(59):
        ll=(ll*ll-2)%q_old
    assert ll==0
    old=budget(q_old,1200000,(q_old//10)**5)
    q=17592186044423
    prime=pocklington(q,{2:1,11:1,53:1,97:1,155542661:1},5)
    s=(q-3)//2
    assert 2*s<q-1
    simplex=budget(q,32768,comb(s+5,5))
    assert Fraction(simplex["Delta_fraction_lower"])>Fraction(1,8)
    # Optional stronger rank-reduction version: q >= r^3 gives factor >=5/6.
    q_small=8796093022237
    small_prime=pocklington(q_small,{2:2,3:1,13:1,71:1,227:1,3498493:1},5)
    r_small=19000
    assert q_small>r_small**3
    small=budget(q_small,r_small,comb((q_small-3)//2+5,5),Fraction(5,6))
    result={"status":"exact finite numerical certificate only",
      "old_grid":old,"simplex_prime":prime,"simplex":simplex,
      "stronger_small_prime":small_prime,"stronger_small":small}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    for key in ["old_grid","simplex","stronger_small"]:
        b=result[key]
        print(key,{k:b[k] for k in ["q","r","m_digits","N_digits","incidences_digits","triangles_upper_digits","E_fraction_decimal","Delta_fraction_decimal","error_fraction_decimal"]})

if __name__=='__main__':
    run()
