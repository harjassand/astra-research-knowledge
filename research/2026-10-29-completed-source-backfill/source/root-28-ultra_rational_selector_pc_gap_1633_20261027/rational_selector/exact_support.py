"""Acquire and literally replay the rational-selector positive certificate.

An exact rational affine projection is already in EXACT_AFFINE_SUGGESTION.npz.
Positivity is proved by a dyadic Gram factor and an EXACT residual bound;
the floating Cholesky only suggests the factor and carries no proof weight.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations_with_replacement as cw
import json
import hashlib
import time
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parent


def exponent(ai,xi):
    e=[0]*8
    for i in ai:e[i]+=1
    for i in xi:e[i+4]+=1
    return tuple(e)


def main():
    started=time.monotonic()
    acquired=np.load(ROOT/'EXACT_AFFINE_SUGGESTION.npz')
    denominator=int(acquired['denominator'])
    assert denominator==80000000000
    q=[int(v) for v in acquired['q']]
    selector=[Q(int(v),denominator) for v in acquired['selector']]
    features=[exponent(ai,(k,)) for ai in cw(range(4),3) for k in range(4)]
    features += [exponent(ai,xi) for ai in cw(range(4),2) for xi in cw(range(4),2)]
    assert len(features)==180
    gram=np.zeros((180,180),dtype=np.int64)
    for v,(i,j) in zip(q,cw(range(180),2)):gram[i,j]=gram[j,i]=v
    shift=Q(1,200000);margin=Q(1,400000)
    float_gram=gram.astype(float)/denominator
    proposed=np.linalg.cholesky(float_gram-float(shift)*np.eye(180))
    dyadic=2**44
    low=np.rint(proposed*dyadic).astype(np.int64)
    assert np.array_equal(low,np.tril(low))
    ll=low.astype(object)@low.T.astype(object)
    residual=gram.astype(object)*dyadic**2-denominator*ll
    for i in range(180):residual[i,i]-=int(shift*denominator)*dyadic**2
    row_sums=[sum(abs(int(v)) for v in row) for row in residual]
    residual_bound=Q(max(row_sums),denominator*dyadic**2)
    assert residual_bound<shift-margin
    # Literal polynomial identity, independently rebuilt from the definition.
    a=s.symbols('a0:4');x=s.symbols('x0:4');variables=a+x
    aa,b,c,d=a
    u,v,w,det=aa*aa+c*c,b*b+d*d,aa*b+c*d,aa*d-b*c
    norm=u+v;hx,hy,hz=u-v,2*w,2*det
    selbasis=[hx**3,hx**2*hz,hx*hz**2,hz**3,hx*hy**2,hy**2*hz]
    numerator=sum(s.Rational(t.numerator,t.denominator)*m for t,m in zip(selector,selbasis))
    point_raw=(ROOT.parent/'common_cone_review/EXACT_SYMMETRIC_TARGET.json').read_bytes()
    p=list(map(s.Rational,json.loads(point_raw)['coefficients']))
    f=sum(t*m for t,m in zip(p,[u*u,v*v,u*v,w*w,u*w,v*w,det*u,det*v,det*w]))
    shifted=f.xreplace(dict(zip(a,(ai+xi for ai,xi in zip(a,x)))))
    breg=shifted-f-sum(s.diff(f,ai)*xi for ai,xi in zip(a,x))
    target=s.Poly(norm**2*breg-numerator*(x[0]*x[3]-x[1]*x[2]),*variables,domain=s.QQ)
    literal={e:Q(int(c.p),int(c.q)) for e,c in target.terms()}
    rebuilt={}
    for value,(i,j) in zip(q,cw(range(180),2)):
        if value:
            e=tuple(v+w for v,w in zip(features[i],features[j]))
            rebuilt[e]=rebuilt.get(e,Q(0))+Q(value*(1 if i==j else 2),denominator)
    rebuilt={e:v for e,v in rebuilt.items() if v}
    assert rebuilt==literal
    span={tuple(v+w for v,w in zip(aa,bb)) for aa in features for bb in features}
    assert len(span)==3185
    # Full35 perturbation coverage; the same rational selector is retained.
    perturb_l1=[]
    for indices in cw(range(4),4):
        m=s.prod(a[i] for i in indices)
        mb=m.xreplace(dict(zip(a,(ai+xi for ai,xi in zip(a,x)))))-m-sum(
            s.diff(m,ai)*xi for ai,xi in zip(a,x))
        polynomial=s.Poly(norm**2*mb,*variables,domain=s.QQ)
        assert set(polynomial.monoms())<=span
        perturb_l1.append(sum(abs(c) for c in polynomial.coeffs()))
    assert len(perturb_l1)==35 and set(perturb_l1)=={176}
    assert sum(perturb_l1)==6160
    radius=Q(1,4928000000)
    assert margin-6160*radius==margin/2
    out={
        'status':'EXACT_RATIONAL_HOMOGENEOUS_GLOBAL_SUPPORT_ACQUIRED_AND_LITERAL_REPLAYED',
        'target_coefficients':list(map(str,p)),
        'target_source_sha256':hashlib.sha256(point_raw).hexdigest(),
        'selector':'p6(A)/|A|^4 for A!=0; zero at A=0',
        'selector_Hopf_basis':['x3','x2z','xz2','z3','xy2','y2z'],
        'selector_coefficients':list(map(str,selector)),
        'gram_denominator':denominator,'gram_integer_matrix':gram.tolist(),
        'gram_proved_lower_bound':str(margin),
        'dyadic_factor_denominator':dyadic,'dyadic_lower_integer_matrix':low.tolist(),
        'factor_reference_shift':str(shift),
        'exact_residual_operator_norm_upper_bound':str(residual_bound),
        'exact_residual_criterion':'R = LL^T + shift I + E; ||E||2 <= max absolute row sum < shift - margin',
        'positive_polynomial_nonzero_coefficients':len(literal),
        'full_Gram_monomial_span':len(span),
        'full35_perturbation_Gram_l1_bound':6160,
        'full35_coefficient_sup_radius':str(radius),
        'perturbed_Gram_lower_bound':str(margin/2),
        'seconds':time.monotonic()-started,
        'scope':'Exact global rational minor support, hence PC and QC after the analytic support-to-finite-lift argument. Combined with the separately accepted24-atom theorem, PC has no polynomial globally nonnegative minor-support selector here. No world priority or physical capability claim.'}
    path=ROOT/'EXACT_RATIONAL_SUPPORT.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    print(json.dumps({k:v for k,v in out.items() if k not in ['gram_integer_matrix','dyadic_lower_integer_matrix']},indent=2))
    print('certificate_sha256',digest)


if __name__=='__main__':main()
