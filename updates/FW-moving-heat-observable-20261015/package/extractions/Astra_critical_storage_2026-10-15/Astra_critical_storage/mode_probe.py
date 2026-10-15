#!/usr/bin/env python3
"""Reusable compatible relative-Fourier symbol. Numerical output discovers candidates only.
Exact acceptance for the m=3 candidate is in verify.py.
"""
import sympy as s

def integrand_and_hessian(k):
    a,b,c,d=s.symbols('a b c d',real=True)
    u=a*a+c*c;v=b*b+d*d;j=a*d-b*c
    G=3*(u+v-2*j)**2+s.Rational(35,24)*u*u+j*j-s.Rational(5,2)*j*u
    return G,s.hessian(G,(a,b,c,d)).subs({a:k,b:0,c:0,d:1})

def compatible_mode_symbol(k,m,xi=0):
    """Hermitian v* M v; row-major A convention, positive rotation R_y."""
    _,H=integrand_and_hessian(k)
    X=(s.I*xi-k)*s.eye(2)
    Y=s.I*m*s.eye(2)+s.Matrix([[0,-1],[1,0]])
    C=s.Matrix.vstack(X[0,:],Y[0,:],X[1,:],Y[1,:])
    return s.simplify(C.conjugate().T*H*C)

if __name__=='__main__':
    k=s.symbols('k',real=True)
    P=107*k**4-232*k**3+152*k*k-24
    kp=s.RootOf(P,1)
    print('Candidate scan only; xi=0; k is the isolated positive algebraic root.')
    for m in range(7):
        M=compatible_mode_symbol(k,m).subs(k,kp)
        lo=(s.trace(M)-s.sqrt(s.trace(M)**2-4*M.det()))/2
        print('m=',m,'minimum eigenvalue approximately',s.N(lo,12))
