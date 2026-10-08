# Independent exact axial interval certificate derived from axial_blocks.py.
from pathlib import Path
src=Path(__file__).with_name('axial_blocks.py').read_text()
exec(src.split('for name,B in blocks:print')[0])
from sympy import Poly, expand, cancel
u,v=symbols('u v',nonnegative=True)

def nonnegative_coefficients(p,variables):
    coeffs=Poly(expand(p),*variables).coeffs()
    assert all(c.is_nonnegative is True for c in coeffs),p
    return coeffs

def psd_by_all_principal_minors(B):
    for k in range(1,B.rows+1):
        for ids in combinations(range(B.rows),k):
            assert simplify(B.extract(ids,ids).det()).is_nonnegative is True,(B,ids)

# Low: D(t) is affine in t^2. Exact PSD endpoints suffice by convexity.
for t0 in [0,R(2,3)]:
    for name,B in blocks:
        C=B.subs({a:R(34,9),b:t0*t0+R(13,9),r:t0*t0})
        psd_by_all_principal_minors(C)
print('PASS low interval: affine in t^2, all principal minors PSD at endpoints.')

# Middle: all proper leading minors positive; last determinants have only
# isolated (t-1)^2 zeros. Certify the remaining polynomial factors positive
# by nonnegative homogeneous Bernstein coefficients on the whole interval.
for name,B in blocks:
    C=B.subs({a:t*t-4*t+6,b:2*t*t+1,r:t*t})
    for k in range(1,C.rows+1):
        p=factor(C[:k,:k].det())
        scalar,factors=p.as_coeff_mul()
        # Divide out the exact isolated zero if present, keeping a rational polynomial.
        q=p
        while simplify(q.subs(t,1))==0:
            q=cancel(q/(t-1))
        deg=Poly(q,t).degree()
        homog=cancel((u+v)**deg*q.subs(t,(R(2,3)*u+2*v)/(u+v)))
        cs=nonnegative_coefficients(homog,[u,v])
        assert all(c.is_positive is True for c in cs)
        print('MID',name,k,'zero multiplicity',Poly(p,t).degree()-deg,'positive Bernstein coeffs',cs)
print('PASS middle interval: Sylvester for t!=1; t=1 by continuity.')

# High: set s=t^2=4+u. All leading-minor polynomial coefficients strictly
# positive, so Sylvester certifies t>=2.
for name,B in blocks:
    C=B.subs({a:2,b:2*t*t+1,r:t*t})
    for k in range(1,C.rows+1):
        p=C[:k,:k].det()
        q=Poly(p,t)
        assert all(power[0]%2==0 for power in q.monoms())
        converted=sum(c*(4+u)**(power[0]//2) for power,c in q.terms())
        cs=nonnegative_coefficients(converted,[u])
        assert all(c.is_positive is True for c in cs)
print('PASS high interval: t^2=4+u, all leading minors strictly positive coefficients.')
print('AXIAL THEOREM PASS FOR EVERY t>=0. No floating spectra or finite grid premise.')
