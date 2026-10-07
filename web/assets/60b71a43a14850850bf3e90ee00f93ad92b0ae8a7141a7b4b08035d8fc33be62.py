"""Bounded exact algebra and an executable zero-power finite-permutation code."""
from pathlib import Path
from fractions import Fraction
from math import lcm
import json
import sympy as s

K, b = s.symbols('K b', real=True, nonzero=True)
# Frame (X,H,V): [X,H]=K V, [X,V]=-H, [H,V]=X.
# g_b(X,X)=1, g_b(H,H)=b^2, g_b(V,V)=b^-2.
g = s.diag(1,b*b,b**-2)
adx = s.Matrix([[0,0,0],[0,0,-1],[0,K,0]])
strain_cov = s.simplify(-(adx.T*g+g*adx)/2)
strain = s.simplify(g.inv()*strain_cov)
J = s.simplify(s.trace(strain*strain)/2)
m, k2, tau, v = s.symbols('m k2 tau v', positive=True)
checks = {
    'geodesic_metric_keeps_volume': g.det() == 1,
    'geodesic_strain_power': s.simplify(J-(b*b-K/b**2)**2/4) == 0,
    'sasaki_curvature_penalty': s.simplify((1-2*K+K*K)/4+K-(1+K)**2/4) == 0,
    'optimized_penalty_variance_identity': s.simplify(
        (s.sqrt(m*m+v)-m)/2-v/(2*(s.sqrt(m*m+v)+m))) == 0,
    'optimized_penalty_exact_difference': s.simplify(
        (tau-2*m+k2/tau)/4-(s.sqrt(k2)-m)/2
        -(tau-s.sqrt(k2))**2/(4*tau)) == 0,
}

def compile_permutation(p):
    """Compact torus decoding data: no expansion into L angular bins."""
    if sorted(p) != list(range(len(p))):
        raise ValueError('The supplied table must be a finite permutation.')
    seen, cycles = set(), []
    for start in range(len(p)):
        if start in seen:
            continue
        cyc=[];q=start
        while q not in seen:
            seen.add(q);cyc.append(q);q=p[q]
        cycles.append(cyc)
    period=lcm(*(len(c) for c in cycles)) if cycles else 1
    return {'cycles':cycles,'L':period,'speed':str(Fraction(1,period)),
            'description_states':len(p),'log2_L_ceiling':(period-1).bit_length()}

def decode(data, theta, y):
    theta=theta%1;y=y%1
    cycles=data['cycles'];C=len(cycles)
    cycle=cycles[(y*C).numerator//(y*C).denominator]
    angular=theta*data['L']
    j=angular.numerator//angular.denominator
    return cycle[j%len(cycle)]

permutation=[1,2,0,4,3,5,7,8,9,6]
data=compile_permutation(permutation)
C=len(data['cycles']);L=data['L']
tested=0
for ci,cyc in enumerate(data['cycles']):
    y0=Fraction(2*ci+1,2*C)
    for j in range(L):
        for offset in (Fraction(1,7),Fraction(1,2),Fraction(6,7)):
            theta=(j+offset)/L
            a=decode(data,theta,y0)
            nxt=decode(data,theta+Fraction(1,L),y0)
            assert nxt==permutation[a]
            tested+=1
checks['finite_permutation_decoding_fixtures']=tested==C*L*3
checks['finite_permutation_cell_mass'] = sum(
    (Fraction(1,C*len(cyc)) for cyc in data['cycles'] for _ in cyc),
    Fraction()) == 1

result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
        'permutation':permutation,'compiled_code':data,'fixtures':tested,
        'scope':'Exact geodesic strain/optimization identities and rational '
                'finite-permutation decoding fixtures. Riccati, entropy, '
                'compactness, invariant measures and physical implementation '
                'are not certified by these finite checks.'}
out=Path(__file__).with_name('second_checks.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if not all(checks.values()):
    raise SystemExit(1)
