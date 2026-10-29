#!/usr/bin/env python3
"""Standard-library exact controls and deterministic heat quadrature.

Ordinary proofs carry the general results. No trajectories, native
calibration, external libraries or stochastic simulation are used.
"""
from pathlib import Path
from fractions import Fraction as R
import hashlib
import json
import math

ROOT=Path(__file__).resolve().parent
def zeros(n): return [[R(0) for _ in range(n)] for _ in range(n)]
def transpose(A): return [list(row) for row in zip(*A)]
def mul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]
def add(*As):
    return [[sum(A[i][j] for A in As) for j in range(len(As[0][0]))]
            for i in range(len(As[0]))]
def qform(v,A):
    return sum(v[i]*A[i][j]*v[j] for i in range(len(v)) for j in range(len(v)))

gamma,eps,a=R(3,2),R(1,10**6),R(1,3)
Q,U=zeros(4),zeros(4)
for e in range(2):
    for bit in range(2):
        i=2*e+bit
        Q[i][2*(1-e)+bit]=eps
        Q[i][2*e+1-bit]=gamma/2
        Q[i][i]=-eps-gamma/2
        U[i][2*e+1-bit]=1
v=[1+a,1-a,1+a,1-a]
energy=-qform(v,Q)/(4*(1+a*a))
affinity=qform(v,U)/(4*(1+a*a))
assert energy==gamma*a*a/(1+a*a)
assert 1-affinity==2*energy/gamma
assert mul(Q,U)==mul(U,Q)
eigenvectors=[([1,1,1,1],R(0)),([1,-1,1,-1],gamma),
              ([1,1,-1,-1],2*eps),([1,-1,-1,1],gamma+2*eps)]
for w,lam in eigenvectors:
    assert [sum(Q[i][j]*w[j] for j in range(4)) for i in range(4)]==[-lam*x for x in w]

mass,temp,spring,omega=R(2),R(3),R(5),R(7,3)
drift=zeros(4)
drift[0][2]=drift[1][3]=1
drift[2][0]=drift[3][1]=-spring/mass
drift[2][2]=drift[3][3]=-gamma
drift[2][3]=-omega
drift[3][2]=omega
cov,noise=zeros(4),zeros(4)
for i in range(4):
    cov[i][i]=temp/spring if i<2 else temp/mass
    if i>=2: noise[i][i]=2*gamma*temp/mass
assert add(mul(drift,cov),mul(cov,transpose(drift)),noise)==zeros(4)
third=mul(mul(mul(drift,drift),drift),cov)
expected=[[gamma*temp/mass,omega*temp/mass],[-omega*temp/mass,gamma*temp/mass]]
assert [row[:2] for row in third[:2]]==expected

# Cubic bridge coefficients in s/t, with endpoint position/momentum data.
t,dq,dp=R(5),R(2),R(3)
coeff=[dq,t*dp,-3*dq-2*t*dp,2*dq+t*dp]
value=lambda x:sum(coeff[k]*x**k for k in range(4))
derivative=lambda x:sum(k*coeff[k]*x**(k-1) for k in range(1,4))/t
assert value(R(0))==dq and value(R(1))==0
assert derivative(R(0))==dp and derivative(R(1))==0

# A=gamma=theta=K=tau=1. pi<22/7 and sqrt(2)<3/2.
cq_upper=R(33,7)
c0_upper=cq_upper+R(1,2)
C_init=2*c0_upper*c0_upper+4
C_derived=3*(C_init+3)
assert C_derived<185
d0,tv_floor=R(1,8),R(1,12000)
assert 185*tv_floor<(d0-tv_floor)**2

def simpson(f,a,b,tol=1e-12):
    c=(a+b)/2; fa,fc,fb=f(a),f(c),f(b)
    whole=(b-a)*(fa+4*fc+fb)/6
    def recurse(a,b,fa,fc,fb,whole,tol,depth):
        c=(a+b)/2; d=(a+c)/2; e=(c+b)/2
        fd,fe=f(d),f(e)
        left=(c-a)*(fa+4*fd+fc)/6
        right=(b-c)*(fc+4*fe+fb)/6
        error=left+right-whole
        if depth==0 or abs(error)<15*tol:
            return left+right+error/15
        return (recurse(a,c,fa,fd,fc,left,tol/2,depth-1)
               +recurse(c,b,fc,fe,fb,right,tol/2,depth-1))
    return recurse(a,b,fa,fc,fb,whole,tol,24)

def heat(n):
    def fun(z):
        t=z/n
        return math.exp(-t-n*n*(t+math.expm1(-t)))/(2*n)
    return sum(simpson(fun,a,b) for a,b in [(0,1),(1,3),(3,8),(8,20),(20,80)])

rows=[]
for n in [1,2,4,8,16,32,64,128]:
    sigma=heat(n)
    nn=n*n
    upper=(math.sqrt(math.pi*math.e/(2*nn))
           +math.exp(-1-nn/math.e)/(1+nn/math.e))/2
    assert 0<sigma<upper<2/n
    if n==1: assert abs(sigma-(math.e-2)/2)<1e-11
    rows.append({"n":n,"sigma":sigma,"n_sigma":n*sigma,
                 "analytic_upper_bound":upper})

result={
 "status":"PASS",
 "scope":"Exact rational parity and magnetic covariance controls, exact cubic endpoint bridge, exact rational TV certificate, deterministic heat quadrature. No trajectories or calibration.",
 "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 "odd_gap":"gamma", "full_gap":"min(gamma,2epsilon)",
 "affinity_exact_instance":str(affinity),
 "energy_exact_instance":str(energy),
 "magnetic_q_covariance_third_derivative_exact_instance":[[str(x) for x in row] for row in expected],
 "likelihood_second_moment_rational_upper":str(C_derived),
 "likelihood_second_moment_clean_upper":185,
 "native_path_KL_floor":str(d0),
 "native_path_TV_floor":str(tv_floor),
 "finite_heat_bound":"sigma_n < 2/n with all scalar parameters one",
 "heat_asymptotic_constant":math.sqrt(math.pi)/(2*math.sqrt(2)),
 "heat_values":rows,
 "quadrature_scope":"Floating adaptive Simpson corroboration, not certified intervals. Analytic heat upper bound and asymptotic have ordinary proofs.",
 "execution_correction":"An initial draft used unavailable optional mpmath/sympy imports. It did not run. This final checker uses only the Python standard library."}
(ROOT/"NATIVE_PARITY_AND_SHEAR_CHECKS.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
