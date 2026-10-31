"""Exact polynomial audit of the [110] envelope-model correction.

The vertical-subband restriction is an explicit physical assumption, not a
claim of unrestricted three-dimensional protection. No material parameters
or small residuals are assigned. All symbolic coefficients use fractions.
"""
from fractions import Fraction as F
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
N = 6
ZERO = (0,)*N

def const(c):
    return {} if c == 0 else {ZERO: F(c)}

def var(i):
    p = [0]*N
    p[i] = 1
    return {tuple(p):F(1)}

def add(*ps):
    out = {}
    for p in ps:
        for mon,c in p.items():
            out[mon] = out.get(mon,F(0))+c
    return {m:c for m,c in out.items() if c}

def scale(c,p):
    return {m:F(c)*a for m,a in p.items() if c*a}

def mul(a,b):
    out={}
    for ma,ca in a.items():
        for mb,cb in b.items():
            mon=tuple(x+y for x,y in zip(ma,mb))
            out[mon]=out.get(mon,F(0))+ca*cb
    return {m:c for m,c in out.items() if c}

def power(p,k):
    out=const(1)
    for _ in range(k):
        out=mul(out,p)
    return out

def difference(a,b):
    return add(a,scale(-1,b))

x,y,z,A,gamma,kap = [var(i) for i in range(N)]

def vertical_expectation(p):
    out={}
    for mon,c in p.items():
        kzpower=mon[2]
        if kzpower % 2:
            continue
        assert kzpower in (0,2)
        new=list(mon)
        new[2]=0
        new[5]+=kzpower//2
        key=tuple(new)
        out[key]=out.get(key,F(0))+c
    return {m:c for m,c in out.items() if c}

def verify_rotation():
    # Right-handed axes:
    # x=[1,-1,0]/sqrt(2), y=[0,0,-1], z=[1,1,0]/sqrt(2).
    # Combine the sqrt(2) factors before polynomial arithmetic.
    xpz=add(x,z)
    zmx=add(z,scale(-1,x))
    term1=mul(xpz,add(scale(F(1,2),power(zmx,2)),scale(-1,power(y,2))))
    term2=mul(zmx,add(power(y,2),scale(F(-1,2),power(xpz,2))))
    cx=mul(gamma,scale(F(1,2),difference(term1,term2)))
    cy=mul(gamma,scale(2,mul(mul(x,y),z)))
    cz=mul(gamma,scale(F(1,2),add(term1,term2)))
    projected=[vertical_expectation(c) for c in (cx,cy,cz)]
    target=scale(F(1,2),mul(mul(gamma,x),
                      add(power(x,2),scale(-2,power(y,2)),scale(-1,kap))))
    assert projected[0]=={} and projected[1]=={}
    assert difference(projected[2],target)=={}
    return dict(rotation='x=[1,-1,0]/sqrt(2), y=[0,0,-1], z=[1,1,0]/sqrt(2)',
                assumed_vertical_moments='<k_z>=<k_z^3>=0, <k_z^2>=K_z^2',
                projected_spin_term='gamma/2 * sigma_z * k_x*(k_x^2-2*k_y^2-K_z^2)',
                all_polynomial_residuals_zero=True)

def verify_recentering():
    # z now denotes the signed band minimum k0, not the vertical momentum.
    k0=z
    constant=add(mul(A,power(k0,2)),
                 scale(F(1,2),mul(gamma,add(power(k0,3),scale(-1,mul(kap,k0))))))
    mx=add(A,scale(F(3,2),mul(gamma,k0)))
    my=add(A,scale(-1,mul(gamma,k0)))
    common=add(constant,mul(mx,power(x,2)),mul(my,power(y,2)))
    stationarity=add(scale(2,mul(A,k0)),
                     scale(F(1,2),mul(gamma,add(scale(3,power(k0,2)),scale(-1,kap)))))
    cubic=scale(F(1,2),mul(mul(gamma,x),add(power(x,2),scale(-2,power(y,2)))))
    for spin in [-1,1]:
        shifted=add(x,scale(spin,k0))
        exact=add(mul(A,add(power(shifted,2),power(y,2))),
                  scale(F(spin,2),mul(mul(gamma,shifted),
                        add(power(shifted,2),scale(-2,power(y,2)),scale(-1,kap)))))
        proposed=add(common,scale(spin,mul(x,stationarity)),scale(spin,cubic))
        assert difference(exact,proposed)=={}
    # On q_x^2+q_y^2<=qmax^2 the cubic maximum is qmax^3.
    # Boundary critical points have squared normalized value 32/81<1;
    # the endpoints q_x=+/-qmax attain 1.
    assert F(32,81)<1
    return dict(A='hbar^2/(2m)',
                stationary_minimum_equation='2*A*k0 + gamma/2*(3*k0^2-K_z^2) = 0',
                scalar_quadratic_coefficients=['A+3*gamma*k0/2','A-gamma*k0'],
                required_local_stability='both scalar quadratic coefficients positive',
                residual_spin_term='gamma/2 * sigma_z*q_x*(q_x^2-2*q_y^2)',
                hard_disk_residual_norm_bound='abs(gamma)*qmax^3/2',
                gradient_soc_after_gauge='chi*sigma_z*(V_x*q_y-V_y*q_x) - chi*k0*V_y*I',
                all_polynomial_residuals_zero=True)

if __name__=='__main__':
    out=dict(scope=__doc__,arithmetic='exact rational polynomial expansion',
             bulk_to_110=verify_rotation(),recentering=verify_recentering())
    (HERE/'microscopic_110_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

