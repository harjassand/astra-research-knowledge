"""Exact rational controls of the new interfaces; not producer replay.

No angular_dual import. Generality comes from PROOF, not these instances.
"""
import json
from pathlib import Path
from fractions import Fraction
from math import factorial
from time import perf_counter
import sympy as s


def sqrt_upper(x: Fraction, bits=90):
    # Exact outward dyadic square-root endpoint.
    from math import isqrt
    n = isqrt((x.numerator << (2*bits))//x.denominator)+1
    z=Fraction(n,1<<bits)
    assert z*z >= x
    return z


def main():
    start=perf_counter(); checks=[]
    u=s.Symbol('u'); z=s.Symbol('z'); h=s.Symbol('h')
    for q in range(1,17):
        for j in range(q+1):
            value=s.binomial(q,j)*s.integrate(u**j*(1-u)**(q-j),(u,0,1))
            assert value==s.Rational(1,q+1)
            checks.append(('marked_beta',q,j,str(value)))
    kappa=2*s.integrate(u*s.legendre(2,s.sqrt(u)),(u,0,1))
    assert kappa==s.Rational(1,2)
    # Even spherical quadratics: trace fixed, traceless part eigenvalue1/2.
    checks.append(('singleton_quadratic_eigenvalue',str(kappa)))
    # Highest Laurent term identity for ALL degree-2q binary monomials.
    # Third-variable/any-dimensional forms follow by multilinearity.
    a,b,c,d=s.symbols('a b c d',real=True)
    for q in range(1,6):
        for j in range(2*q+1):
            # n(theta)=(e^{it}(u-iw)+e^{-it}(u+iw))/2.
            poly=s.expand(((z*(a-s.I*b)+(a+s.I*b)/z)/2)**j
                          *((z*(c-s.I*d)+(c+s.I*d)/z)/2)**(2*q-j))
            term=s.expand(poly*z**(2*q)).coeff(z,0)*4**q
            target=(a+s.I*b)**j*(c+s.I*d)**(2*q-j)
            assert s.expand(term-target)==0
            checks.append(('polarization_monomial',q,j))
    c0=s.Rational(21,20); a0=s.Integer(1); b0=s.Rational(11,10)
    g=s.Rational(5,4); beta=s.Rational(17,20)
    covs=[s.diag(1,s.Rational(21,20),s.Rational(11,10)),
          s.Matrix([[s.Rational(26,25),s.Rational(1,25),0],
                    [s.Rational(1,25),s.Rational(26,25),0],
                    [0,0,s.Rational(21,20)]])]
    assert covs[0]*covs[1]!=covs[1]*covs[0]
    for cov in covs:
        assert all(e>=a0 and e<=b0 for e in cov.eigenvals())
    # Direct Gaussian density Taylor vs independent complex Gaussian
    # quadratic cumulants after shifting and integrating the contour.
    for cov in covs:
        e=(cov-c0*s.eye(3))/s.Rational(1,20)
        for v in [s.zeros(3,1),s.Matrix([1,s.Rational(1,2),-s.Rational(1,4)])]:
            cumulants={j:2**(j-1)*factorial(j-1)*(
                s.trace(e**j)/c0**j-j*(v.T*e**j*v)[0]/c0**(j+1))
                for j in range(1,7)}
            # exp(sum cumulant_j (-h/2)^j/j!) is Gaussian quadratic MGF.
            from_mgf=s.series(s.exp(sum(cumulants[j]*(-h/2)**j/s.factorial(j)
                                       for j in range(1,7))),h,0,7).removeO()
            # Independent log of direct Gaussian density ratio to G_c.
            log_direct=-s.log(s.det(s.eye(3)+(h/c0)*e))/2
            log_direct+=(v.T*(s.eye(3)/c0-(c0*s.eye(3)+h*e).inv())*v)[0]/2
            direct=s.series(s.exp(s.series(log_direct,h,0,7).removeO()),h,0,7).removeO()
            assert s.expand(from_mgf-direct)==0
            checks.append(('contour_gaussian_coefficients_0_through_6',str(e),str(v)))
    # Sympy conversion via p/q keeps exact source constants.
    rat=(a0*b0/(g*(2*a0-g)))**3
    i_upper=sqrt_upper(Fraction(int(s.numer(rat)),int(s.denom(rat))))
    c_sq=(g/beta)**3
    c_sq=Fraction(int(s.numer(c_sq)),int(s.denom(c_sq)))
    query_bound=19*c_sq*i_upper
    degree_factor=6*s.Rational(1,20)*(1/beta+a0/(g*(2*a0-g)))
    degree_factor=Fraction(int(s.numer(degree_factor)),int(s.denom(degree_factor)))
    receipt=dict(status='PASS exact finite interface controls; general proof separate',
      checks=len(checks),checks_detail=checks,noncommuting_input=True,
      scalar_constants=dict(C_squared=str(c_sq),I_upper=str(i_upper),
              total_queries_upper=str(query_bound),
              total_degree_upper=str(query_bound*degree_factor)),
      seconds=perf_counter()-start)
    path=Path(__file__).parent/'outputs'/'EXACT_CONSUMER.json'
    path.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='checks_detail'},indent=2))


if __name__=='__main__': main()
