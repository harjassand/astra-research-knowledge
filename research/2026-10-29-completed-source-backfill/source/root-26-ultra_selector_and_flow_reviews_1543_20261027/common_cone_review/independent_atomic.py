"""Literal SymPy replay of actual atoms and full-35 perturbation openness.

This imports neither the atomic producer nor its Fraction verifier. The
arbitrary polynomial-selector reduction is analytic, in ATOMIC_REVIEW.md.
"""
from itertools import combinations_with_replacement as cw
from pathlib import Path
import json
import hashlib
import time
import sympy as s

ROOT = Path(__file__).resolve().parent


def main():
    start = time.monotonic()
    source = ROOT.parent/'quartic_boundary_alternative/EXACT_POLYNOMIAL_SELECTOR_OBSTRUCTION.json'
    raw = source.read_bytes()
    data = json.loads(raw)
    point_raw = (ROOT/'EXACT_SYMMETRIC_TARGET.json').read_bytes()
    assert hashlib.sha256(point_raw).hexdigest() == data['source_sha256']
    p = list(map(s.Rational,data['coefficients']))
    a,b,c,d = variables = s.symbols('a b c d')
    u,v,w,q = a*a+c*c,b*b+d*d,a*b+c*d,a*d-b*c
    f = s.Poly(sum(t*e for t,e in zip(p,[u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w])),*variables)
    monomials = [s.Poly(s.prod(variables[i] for i in indices),*variables)
                 for indices in cw(range(4),4)]
    assert len(monomials) == 35
    pairings = [s.S.Zero]*35
    selector_values = [s.S.Zero]*10
    selector_pairs = list(cw(range(4),2))
    literal_sum = s.S.Zero
    weight_sum = s.S.Zero
    for atom in data['atoms']:
        aa = tuple(map(s.Rational,atom['A']))
        xx = tuple(map(s.Rational,atom['X']))
        wt = s.Rational(atom['weight'])
        assert wt > 0
        weight_sum += wt
        ax = tuple(v+w for v,w in zip(aa,xx))
        detx = xx[0]*xx[3]-xx[1]*xx[2]
        def breg(poly):
            return poly(*ax)-poly(*aa)-sum(poly.diff(v)(*aa)*x
                                          for v,x in zip(variables,xx))
        literal_sum += wt*breg(f)
        for j,m in enumerate(monomials):
            pairings[j] += wt*breg(m)
        for j,(k,l) in enumerate(selector_pairs):
            selector_values[j] += wt*aa[k]*aa[l]*detx
    assert len(data['atoms']) == 24 and weight_sum > 0
    assert all(v==0 for v in selector_values)
    assert literal_sum == s.Rational(data['negative_Bregman_pairing']) < -s.Rational(1,100000)
    assert literal_sum == sum(f.coeff_monomial(m.monoms()[0])*g
                              for m,g in zip(monomials,pairings))
    sensitivity = sum(map(abs,pairings))
    assert sensitivity > 0
    # For each degree-four ordinary monomial, the sum of ALL literal Hessian
    # coefficients is 4*3=12. Bounding each coordinate by its Euclidean norm
    # gives the uniform perturbation estimate, valid without symmetry.
    assert all(sum(sum(abs(v) for _,v in m.diff(ai).diff(aj).terms())
                   for ai in variables for aj in variables)==12 for m in monomials)
    roc_mu = s.Rational(1,400000)
    radius = min(roc_mu/(2*35*12),-literal_sum/(2*sensitivity))
    assert radius > 0
    assert roc_mu-420*radius >= roc_mu/2
    assert literal_sum+radius*sensitivity < 0
    out = {
        'status':'ROOT_INDEPENDENT_LITERAL_ATOMIC_OBSTRUCTION_AND_FULL35_OPENNESS_PASS',
        'certificate_sha256':hashlib.sha256(raw).hexdigest(),
        'symmetric_point_sha256':hashlib.sha256(point_raw).hexdigest(),
        'engine':'SymPy exact literal polynomial evaluations and derivatives; no author imports',
        'strictly_positive_actual_atoms':24,
        'all_ten_quadratic_selector_pairings':list(map(str,selector_values)),
        'negative_Bregman_pairing':str(literal_sum),
        'full35_sensitivity_l1':str(sensitivity),
        'full35_coefficient_sup_radius':str(radius),
        'retained_ROC_lower_bound':str(roc_mu-420*radius),
        'strict_negative_pairing_at_box_edge_upper_bound':str(literal_sum+radius*sensitivity),
        'monomial_pairings':[{'power':m.monoms()[0],'pairing':str(g)}
                             for m,g in zip(monomials,pairings)],
        'seconds':time.monotonic()-start,
        'scope':'Strict ROC and no globally nonnegative polynomial minor-support selector, stable on a full35 box. Does not rule out nonlinear rational selectors or true PC/QC.'}
    (ROOT/'INDEPENDENT_ATOMIC_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='monomial_pairings'},indent=2))


if __name__=='__main__':
    main()
