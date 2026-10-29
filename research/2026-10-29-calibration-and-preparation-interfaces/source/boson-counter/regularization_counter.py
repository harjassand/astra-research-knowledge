"""Stable continuum-HS finite-part counter; exact constants + MP displays.

No assertion about expectation convergence of finite Gaussian-slice algorithms.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,math,time
import mpmath as mp
import sympy as sp

HERE=Path(__file__).resolve().parent
mp.mp.dps=90


def atan_bounds(x,terms):
    s=sum(((-1)**j*x**(2*j+1)/F(2*j+1) for j in range(terms)),F(0))
    nxt=(-1)**terms*x**(2*terms+1)/F(2*terms+1)
    return min(s,s+nxt),max(s,s+nxt)


def main():
    start=time.perf_counter()
    e3_lower=sum((F(3)**j/F(math.factorial(j)) for j in range(9)),F(0))
    assert e3_lower>20
    a0,a1=atan_bounds(F(1,5),8);b0,b1=atan_bounds(F(1,239),3)
    pi_lower=16*a0-4*b1
    assert pi_lower>F(25,8)
    determinant_upper=F(7,10)*(1+F(39,361))
    assert determinant_upper==F(280,361)<F(7,9)<1
    controls=[]
    for n in range(9):
        plus=sp.zeros(n+1)
        # basis m=n_b=0,...,n; b^dagger c raises m.
        for m in range(n):plus[m+1,m]=sp.sqrt((m+1)*(n-m))
        minus=plus.T
        sx=plus+minus;sy=-sp.I*(plus-minus);sz=sp.diag(*[2*m-n for m in range(n+1)])
        residual=sp.simplify(sx*sx+sy*sy+sz*sz-n*(n+2)*sp.eye(n+1))
        assert residual==sp.zeros(n+1)
        controls.append({'N':n,'dimension':n+1,'Casimir_exact':True})
    J=lambda a:mp.exp(mp.mpf(a)**2/2)*mp.erfc(mp.mpf(a)/mp.sqrt(2))/2
    physical=mp.fsum((n+1)*mp.exp(-mp.mpf(n*n)/2-2*n) for n in range(21))
    determinant=mp.fsum((n+1)*mp.exp(-n*(n+2))*(J(n)+J(n+2)) for n in range(21))
    assert determinant<mp.mpf(280)/361<1<physical
    primary=HERE/'sources/Yu_Wei_Li_2610.31541.pdf'
    out={'physical_H':'N^2/2+2N, beta=1; no chemical potential/scalar correction',
         'HS_channels':[{'O':'Sx','lambda':1},{'O':'Sy','lambda':1},{'O':'Sz','lambda':1},{'O':'N','lambda':'-1/2'}],
         'exact_e3_partial_sum_lower':str(e3_lower),
         'exact_Machin_pi_lower':str(pi_lower),
         'exact_Z_det_upper':str(determinant_upper),
         'exact_separation_lower':str(1-determinant_upper),
         'finite_Casimir_controls':controls,
         'mp_digits':mp.mp.dps,'series_terms':21,
         'physical_partition_display':mp.nstr(physical,70),
         'continued_determinant_integral_display':mp.nstr(determinant,70),
         'difference_display':mp.nstr(physical-determinant,70),
         'primary_pdf_sha256':hashlib.sha256(primary.read_bytes()).hexdigest(),
         'primary_claim':'SM S95-S103 post-continuum finite-part recovery; not configuration Kramers sign or trace-convergent algorithms.',
         'limit_boundary':'Exact continuum sectorwise HS identity only. Finite-slice determinant expectation convergence/uniform integrability is NOT_ESTABLISHED.',
         'seconds_after_imports':time.perf_counter()-start,
         'scope':'All-n proof and strict rational separation in STABLE_FINITE_PART_COUNTER.md. Finite Casimirs/MP series are controls, not the premise.'}
    (HERE/'STABLE_COUNTER.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
