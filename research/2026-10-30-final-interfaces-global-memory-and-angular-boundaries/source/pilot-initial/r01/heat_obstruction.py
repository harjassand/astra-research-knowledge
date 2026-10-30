#!/usr/bin/env python3
"""Exact periodic-gradient witness against completeness of heat corrections.

The symbols S,C,J,K stand for sin(y),cos(y),sin(X),cos(X), X=x+sin(y).
Physical differentiation and torus integration are polynomial operations.
Requires SymPy, no network or producer imports. Run with python3 -B.
"""
from math import factorial
from pathlib import Path
import sympy as s

S,C,J,K,h = s.symbols('S C J K h', real=True)


def dx(p):
    return s.expand(K*s.diff(p,J)-J*s.diff(p,K))


def dy(p):
    return s.expand(C*s.diff(p,S)-S*s.diff(p,C)+C*dx(p))


def laplacian(p):
    return s.expand(dx(dx(p))+dy(dy(p)))


def circle_moment(i,j):
    if i % 2 or j % 2:
        return s.S(0)
    a,b = i//2,j//2
    return s.Rational(factorial(2*a)*factorial(2*b),
                      4**(a+b)*factorial(a)*factorial(b)*factorial(a+b))


def average(p):
    # x -> X=x+sin(y) is a translation on each circle; hence dXdy=dxdy.
    return s.factor(sum(co*circle_moment(e[0],e[1])*circle_moment(e[2],e[3])
                        for e,co in s.Poly(s.expand(p),S,C,J,K).terms()))


def main():
    # w=(x+sin(y), y+sin(x+sin(y))) is a composition of area-preserving shears.
    # v_h=w+h*Delta(w-(x,y)) is an explicit smooth identity+periodic map.
    phi1 = (1-h)*S
    phi2 = (1-h*(1+C*C))*J-h*S*K
    A = s.eye(2)+s.Matrix([[dx(phi1),dy(phi1)], [dx(phi2),dy(phi2)]])
    LA = A.applyfunc(laplacian)
    assert s.expand(A.det().subs(h,0)-1) == 0
    assert all(s.expand(dx(dy(p))-dy(dx(p))) == 0 for p in (phi1,phi2))
    # Verify the Euler-predictor formula independently through the generator.
    assert s.expand(phi1-(S+h*laplacian(S))) == 0
    # This expression vanishes on both physical circles.
    predictor_error = s.expand(phi2-(J+h*laplacian(J)))
    assert s.rem(predictor_error,s.Poly(S*S+C*C-1,S),S) == 0
    T = sum(z*z for z in A)
    q = s.expand(A.det())
    qdot = s.expand(A[1,1]*LA[0,0]+A[0,0]*LA[1,1]
                   -A[1,0]*LA[0,1]-A[0,1]*LA[1,0])
    E_T_prime = average(4*T*sum(a*b for a,b in zip(A,LA)))
    E_q_prime = average(2*q*qdot)
    expected_T = -(2304559*h**4-3189560*h**3+2786384*h*h-953024*h+144768)/4096
    expected_q = -h*(955*h**3+576*h*h+544*h-64)/128
    assert s.expand(E_T_prime-expected_T) == 0
    assert s.expand(E_q_prime-expected_q) == 0
    h0 = s.Rational(1,10)
    qprime = E_q_prime.subs(h,h0)
    Tprime = E_T_prime.subs(h,h0)
    assert qprime == s.Rational(577,256000)
    assert Tprime == -s.Rational(743703359,40960000)
    rcrit = s.factor(1-Tprime/(4*qprime))
    assert rcrit == s.Rational(744072639,369280)
    energy_prime = s.factor(Tprime+4*(2048-1)*qprime)
    assert energy_prime == s.Rational(12212801,40960000) and energy_prime > 0
    # A separate direct reconstruction of the compatible-Hessian density
    # checks the sign and determinant second-derivative convention.
    A0 = A.subs(h,h0)
    T0, q0 = sum(z*z for z in A0), s.expand(A0.det())
    density = 0
    for diff in (dx,dy):
        B = A0.applyfunc(diff)
        det_prime = (A0[1,1]*B[0,0]+A0[0,0]*B[1,1]
                     -A0[1,0]*B[0,1]-A0[0,1]*B[1,0])
        density += (8*sum(a*b for a,b in zip(A0,B))**2
                    +4*T0*sum(z*z for z in B)
                    +2*8188*det_prime**2+4*8188*q0*B.det())
    integrated_density = average(density)
    assert integrated_density == -energy_prime
    # Mean determinant is the null-Lagrangian value det(I)=1, also checked
    # directly rather than assumed in the differentiations above.
    assert average(q) == 1 and average(qdot) == 0
    text = '\n'.join([
        'EXACT HEAT-FLOW OBSTRUCTION IN THE ORIGINAL 2x2 QUARTIC FAMILY',
        '',
        'Normalized torus average: (2*pi)^(-2) integral_[0,2*pi]^2.',
        'X=x+sin(y); h=1/10.',
        'v1=x+(1-h) sin(y).',
        'v2=y+[1-h(1+cos(y)^2)] sin(X)-h sin(y) cos(X).',
        'Energies are differentiated along actual componentwise heat flow starting at v.',
        '',
        'For general h, d/dt average |Dv_t|^4 at t=0 = '+str(E_T_prime),
        'For general h, d/dt average (det Dv_t)^2 at t=0 = '+str(E_q_prime),
        '',
        'At h=1/10: derivative of |A|^4 = '+str(Tprime)+'.',
        'At h=1/10: derivative of det(A)^2 = '+str(qprime)+' > 0.',
        'For beta=0, this witness excludes a global exact-form heat certificate whenever r > '+str(rcrit)+'.',
        'For r=2048, F=|A|^4+8188 det(A)^2 is polyconvex and quasiconvex.',
        'Its heat derivative = '+str(energy_prime)+' > 0.',
        'Direct integrated compatible-Hessian density = '+str(integrated_density)+' < 0.',
        'Therefore no globally defined exact 2-form can make the heat Hessian density pointwise nonnegative for this F.',
        'This excludes every regular acquired primitive, not merely P5/T profiles.',
        'It does not imply failure of quasiconvexity or exclude the already accepted boundary seed certificates.',
    ])+'\n'
    (Path(__file__).resolve().parent/'HEAT_EXACT.txt').write_text(text)
    print(text)


if __name__ == '__main__':
    main()
