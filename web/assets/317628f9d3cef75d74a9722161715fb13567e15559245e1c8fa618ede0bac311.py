from fractions import Fraction as Q
from pathlib import Path
from time import perf_counter
import json

REACTIONS = [((1,0,1),(1,1,0)), ((1,1,0),(1,0,1)),
             ((1,1,0),(0,1,0)), ((0,1,0),(1,1,0)),
             ((0,0,1),(0,0,0)), ((0,0,0),(0,0,1))]

def ceilq(x):
    return -((-x.numerator)//x.denominator)

def synthesize(rates):
    k1,k2,k3,k4,k5,k6 = map(Q,rates)
    assert min(k1,k2,k3,k4,k5,k6)>0
    beta,gamma = k2,k1
    center_b = (beta+3*gamma)/(2*beta)
    lin_a = 3*k3+2*k4+2*k2*(k1+k2)
    lin_c = 3*k5+2*k6
    drift_c_max = k1*lin_c**2/(8*k5)
    drift_a_max = lin_a**2/(8*k3)
    eps = min(Q(1), k1, k1*k6)
    a_threshold = max(1,ceilq(lin_a/k3),ceilq((drift_c_max+1)/k3)+1,
                      ceilq((lin_c+1)/(2*k1)))
    delta = min(k2**2, 2*k1*k5/(1+2*k1**2/k2**2))
    joint_threshold = ceilq((drift_a_max+k1*lin_c+delta+1)/delta)
    b_threshold_zero_a = ceilq((drift_c_max+eps)/k4)+1
    c_threshold_zero_a = max(1,ceilq((lin_c+1)/(2*k5)))
    return {'rates':tuple(map(Q,rates)), 'beta':beta,'gamma':gamma,
            'center_b':center_b,'eps':eps,'delta':delta,
            'a_threshold':a_threshold,
            'b_threshold':max(joint_threshold,b_threshold_zero_a),
            'c_threshold':max(joint_threshold,c_threshold_zero_a)}

def potential(x,cert):
    a,b,c=map(Q,x)
    return 1+(a-1)**2+cert['beta']*(b-cert['center_b'])**2+cert['gamma']*(c-1)**2

def propensity(x,y,k):
    val=k
    for xi,yi in zip(x,y):
        for j in range(yi):
            val*=max(0,xi-j)
    return val

def direct_generator(x,cert):
    old=potential(x,cert)
    ans=Q(0)
    for (y,yp),rate in zip(REACTIONS,cert['rates']):
        lam=propensity(x,y,rate)
        if lam:
            xp=tuple(xi-yi+zi for xi,yi,zi in zip(x,y,yp))
            ans+=lam*(potential(xp,cert)-old)
    return ans

def formula_generator(x,cert):
    a,b,c=map(Q,x)
    k1,k2,k3,k4,k5,k6=cert['rates']
    h=-2*k3*a*a+(3*k3+2*k4+2*k2*(k1+k2))*a-k4
    return b*h-2*a*(k2*b-k1*c)**2+k1*(-2*k5*c*c+(3*k5+2*k6)*c-k6)

def outside_box(x,cert):
    return any(v>=cert[n+'_threshold'] for v,n in zip(x,('a','b','c')))

def main():
    started=perf_counter()
    rate_sets=[(1,1,1,1,1,1),(Q(1,2),Q(3,2),2,3,Q(1,3),2),
               (3,Q(1,4),Q(1,2),Q(1,3),2,Q(1,2)),
               (Q(1,5),4,Q(2,3),Q(5,2),Q(7,4),Q(3,5))]
    identity_checks=0; outside_checks=0; targeted_checks=0
    certificates=[]
    for rates in rate_sets:
        cert=synthesize(rates)
        for a in range(7):
          for b in range(8):
            for c in range(8):
                x=(a,b,c)
                assert direct_generator(x,cert)==formula_generator(x,cert)
                assert potential(x,cert)>=1
                identity_checks+=1
                if a+b and outside_box(x,cert):
                    assert formula_generator(x,cert)<=-cert['eps']
                    outside_checks+=1
        aa,bb,cc=(cert[n+'_threshold'] for n in ('a','b','c'))
        for x in [(aa,0,0),(aa,0,1),(aa,1,0),(0,bb,0),
                  (0,1,cc),(1,bb,0),(1,0,cc),(aa,bb,cc),
                  (aa+1,2*bb,3*cc)]:
            assert direct_generator(x,cert)==formula_generator(x,cert)
            assert outside_box(x,cert)
            assert formula_generator(x,cert)<=-cert['eps']
            targeted_checks+=1
        certificates.append({k:([str(v) for v in val] if k=='rates' else str(val))
                             for k,val in cert.items()})
    # Tighter exact unit-rate box from the separate hand inequalities.
    unit=synthesize(rate_sets[0]); unit_outside=0
    for a in range(11):
      for b in range(26):
        for c in range(22):
          if not a+b: continue
          if a>=5 or b>=20 or c>=16:
            assert formula_generator((a,b,c),unit)<=-1
            unit_outside+=1
    out={'status':'PASS','symbolic_formula_exact_checks':identity_checks,
         'outside_synthesized_box_checks':outside_checks,
         'large_exact_threshold_checks':targeted_checks,
         'unit_tighter_box_checks':unit_outside,'certificates':certificates,
         'elapsed_seconds':perf_counter()-started,
         'scope':'Bounded exact diagnostics; universal inequalities in quadratic_certificate.txt prove drift outside the synthesized box.'}
    Path(__file__).with_name('quadratic_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
