"""Exact all-width extension of the incoming rational profile-graph calibration.
For each directed vertex pair, certify its adjusted edge polynomial is >=0
for every tau>0, using rational factorisation and Sturm root counts.
"""
from fractions import Fraction as Q
import json, sys
import sympy as sp
sys.path.insert(0, 'work/FO-continuous-calibration/source-copy/resonant')
from profile_algebra import averaged, poly_terms, edge_coeffs

PIN='work/FO-continuous-calibration/source-copy/resonant/profile_graph_certificate.json'
z=json.load(open(PIN))
vertices=[tuple(map(Q, row)) for row in z['vertices']]
P=[Q(int(x),int(z['common_denominator'])) for x in z['potential_numerators']]
G,N,_,_=averaged(1,-1,False)
gt,nt=poly_terms(G),poly_terms(N)
s=sp.symbols('s', real=True)
checked=0; zeros=0; root_edges=0; max_degree=0; failures=[]
for i,U in enumerate(vertices):
    for j,V in enumerate(vertices):
        gc=edge_coeffs(gt,U,V); nc=edge_coeffs(nt,U,V)
        # W_eta(tau)-[P(V)-P(U)] = sum_k c[k] tau**(1-k).
        c=[gc[k]-Q(1,4)*nc[k] for k in range(5)]
        c[1]-=P[j]-P[i]
        # q(s)=s*(W_eta(1/s)-Delta P) has the same sign for s>0.
        q=sp.Poly(sum(sp.Rational(x.numerator,x.denominator)*s**k for k,x in enumerate(c)),s)
        checked+=1; max_degree=max(max_degree,q.degree() if not q.is_zero else 0)
        if q.is_zero:
            zeros+=1; continue
        # The first nonzero coefficient fixes the sign sufficiently near 0+.
        low=min(k[0] for k,_ in q.terms())
        low_coeff=q.nth(low)
        if low_coeff < 0:
            failures.append((i,j,'negative near zero',str(q.as_expr())))
            continue
        # Each rational irreducible factor has simple roots; an odd exponent
        # would change sign at any positive root. Sturm counts roots exactly.
        _, facs=sp.factor_list(q.as_expr(),s)
        has_odd_positive=False
        for fac,exp in facs:
            if exp%2 and sp.Poly(fac,s).count_roots(0,sp.oo)>0:
                has_odd_positive=True
                break
        if has_odd_positive:
            root_edges+=1
            failures.append((i,j,'odd positive root',str(q.as_expr())))
        checked
print(json.dumps({'checked_directed_pairs':checked,'zero_polynomials':zeros,
                  'pairs_with_positive_real_roots':root_edges,'max_degree':max_degree,
                  'failures':failures[:5],'failure_count':len(failures)},indent=2))
if failures: raise SystemExit(1)
