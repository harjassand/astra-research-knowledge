"""Exact acoustic-face computation for the supplied anisotropic quartics.

Read-only input: case ARC_PROOF.txt acoustic formulas. No optimization.
The coefficient unknowns range over all 35 homogeneous quartics in R^4.
"""
from pathlib import Path
import json
import time
import sympy as s

OUT = Path(__file__).resolve().parent
start = time.perf_counter()
a, b, c, d, t, x, y = s.symbols("a b c d t x y")
av = (a, b, c, d)
powers = [(i, j, k, 4-i-j-k)
          for i in range(5) for j in range(5-i) for k in range(5-i-j)]
monomials = [a**i*b**j*c**k*d**l for i,j,k,l in powers]

def compute(tau):
    B = 1-3*tau*tau
    H = 1+3*tau*tau
    beta = B/H
    r = 4-12*tau/H
    mod = s.Poly(B**2*(1-t*t)**2-(1-4*tau+3*tau*tau)*H*(1+t*t)**2,t).monic()
    K = s.Matrix([
        -B*(tau*(1-t*t)+H*t*t)*(1+t*t),
        B*t*(H-tau*(1-t*t))*(1+t*t),
        B*B*t*(1-t*t)-tau*H*t*(1+t*t)**2,
        B*B*t*t*(1-t*t)+tau*H*(1+t*t)**2,
    ]).applyfunc(lambda p:s.rem(p,mod.as_expr(),t))
    Ku = s.Matrix([x*K[0]-y*K[2], x*K[1]-y*K[3],
                   y*K[0]+x*K[2], y*K[1]+x*K[3]])
    R = dict(zip(av,(x,x*t,y,y*t)))
    # All coefficients in u=(x,y) and in Q[t]/m. These are linear
    # constraints on an arbitrary quartic's coefficients.
    columns=[]
    for mon in monomials:
        hh=s.hessian(mon,av).subs(R, simultaneous=True)
        col=[]
        for v in hh*Ku:
            pp=s.Poly(s.expand(v),x,y)
            for ix in range(4):
                rem=s.Poly(s.rem(pp.coeff_monomial(x**ix*y**(3-ix)),mod.as_expr(),t),t)
                col.extend(rem.nth(j) for j in range(4))
        columns.append(col)
    L=s.Matrix.hstack(*[s.Matrix(col) for col in columns])
    rr,pivots=L.rref()
    basis=L.nullspace()
    T=a*a+b*b+c*c+d*d
    q=a*d-b*c
    X=a*a+c*c-b*b-d*d
    F=s.Poly(s.expand(T*T+4*(r-1)*q*q+4*beta*q*X),*av)
    fv=s.Matrix([F.coeff_monomial(m) for m in monomials])
    assert L*fv==s.zeros(L.rows,1)
    polys=[s.factor(sum(v*m for v,m in zip(vec,monomials))) for vec in basis]
    record={"tau":str(tau),"beta":str(beta),"r":str(r),
            "monomial_powers":powers,"matrix_rows":L.rows,"matrix_columns":L.cols,
            "rank":len(pivots),"nullity":len(basis),"nullspace_polynomials":list(map(str,polys)),
            "F_in_kernel":True,"modulus":str(mod.as_expr()),
            "constraint_matrix":[list(map(str,row)) for row in L.tolist()]}
    label=f"{tau.p}_{tau.q}"
    (OUT/f"face_{label}.json").write_text(json.dumps(record,indent=2)+"\n")
    print(json.dumps({k:v for k,v in record.items() if k not in
                      ("constraint_matrix","monomial_powers")},indent=2),flush=True)
    return L,basis,F.as_expr(),mod,K

if __name__=="__main__":
    for tau in (s.Rational(1,6),s.Rational(1,30)):
        compute(tau)
    print("seconds",time.perf_counter()-start,flush=True)
