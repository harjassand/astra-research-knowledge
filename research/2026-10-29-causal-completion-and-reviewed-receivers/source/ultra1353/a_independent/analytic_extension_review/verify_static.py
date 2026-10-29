"""Independent read-only intake arithmetic, not the producer's model run.

No producer function imports, symbolic Hessian rerun, Fourier truncation,
ODE, optimization, random draw or new source case. Exact Fraction algebra
reconstructs native norm bounds and whole-space/tube polynomial constants;
formal coefficients check the finite geometric-ray interface. The all-input
analytic statements are challenged in REVIEW.md, not inferred from these
finite controls or source hashes.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import math
import time

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent.parent/'b_conventional'/'independent_opening'


def add(*polys):
    n = max(map(len,polys))
    return [sum((p[i] if i<len(p) else F(0) for p in polys),F(0))
            for i in range(n)]


def mul(p,q):
    r = [F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,c in enumerate(q):
            r[i+j] += a*c
    return r


def scale(p,a):
    return [a*x for x in p]


def power(p,n):
    out = [F(1)]
    for _ in range(n):
        out = mul(out,p)
    return out


def factorial_envelope(p):
    assert all(x>=0 for x in p)
    return sum((x*math.factorial(j) for j,x in enumerate(p)),F(0))


def hessian_poly(M,f,g):
    # Independently form the nested ordinary product/chain bounds using
    # coefficient arrays, not the producer's SymPy expression/function.
    c = [F(math.factorial(j)*128**j) for j in range(4)]
    A = [c[j]*g+c[j+1]*f for j in range(3)]
    R1,R2 = 1+c[1]*M,c[2]*M
    B = [f,A[0]]
    DB = [c[1]*f+R1*A[0],A[1]]
    DDB = [c[2]*f+R2*A[0]+2*R1*A[1],A[2]]
    uB = [F(0)]+B
    uDB = [F(0)]+DB
    DG = add(DB,scale(uB,2*R1))
    DDG = add(DDB,scale(uDB,4*R1),
              mul([2*R1*R1,2*R2,4*R1*R1],B))
    v = [M,F(1)]
    P = add(scale(power(v,2),2),power(v,4))
    DP = add(scale(v,4),scale(power(v,3),4))
    DDP = add([F(4)],scale(power(v,2),12))
    return add(mul(P,DDG),scale(mul(DP,DG),2),mul(DDP,B))


def main():
    start = time.perf_counter()
    frozen = json.loads((SOURCE/'FROZEN.json').read_text())
    hashes = []
    for x in frozen['files']:
        path = SOURCE/x['path']
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == x['sha256']
        hashes.append({'path':x['path'],'sha256':digest,'bytes':path.stat().st_size})
    cost = json.loads((SOURCE/'SOURCES_AND_COST.json').read_text())
    inherited = []
    for item in cost['frozen_prior_inputs']:
        p = Path(item['path'])
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        assert digest == item['sha256']
        inherited.append({'path':str(p),'sha256':digest,
                          'scope':'Binding only; prior acceptance retained, no new whole audit.'})
    raw = (SOURCE/'RESULT.json').read_bytes()
    result = json.loads(raw)
    tube = json.loads((SOURCE/'TUBE_RESULT.json').read_text())
    assert hashlib.sha256(raw).hexdigest() == tube['input_result_sha256']
    assert result['compiler_sha256'] == hashlib.sha256((SOURCE/'compile_extension.py').read_bytes()).hexdigest()
    assert tube['compiler_sha256'] == hashlib.sha256((SOURCE/'compile_tube_bound.py').read_bytes()).hexdigest()
    assert result['delta'] == '1/2^204'
    delta = F(1,2**204)
    M = 4+4*delta
    f = F(17,4)*delta*delta
    u = 34*delta*delta
    up = 128*delta*delta
    g = 12*delta+(4+16*delta)*u/(1-u)+(4+8*delta)*up/(2*(1-u)**2)
    assert [M,f,g] == [F(result['native_norm_bounds'][k]) for k in ('Q','f','g')]
    assert u < 1 and delta < 1
    poly = hessian_poly(M,f,g)
    hess = factorial_envelope(poly)
    assert len(poly)-1 == 7 and hess == F(result['global_hessian_bounds']['fourier_constructor'])
    f_basis = factorial_envelope(hessian_poly(M,F(1),F(0)))
    g_basis = factorial_envelope(hessian_poly(M,F(0),F(1)))
    assert hess == f*f_basis+g*g_basis
    assert hess < F(213,10**52) < F(1,100)
    ordinary = F(result['global_hessian_bounds']['ordinary_defining_equations'])
    assert ordinary < F(5349,10**10) < F(1,100)
    ordinary_unit = ordinary/delta
    assert ordinary_unit.numerator.bit_length() == result['global_hessian_bounds']['ordinary_unit_delta_constant_bits']

    radius = F(1,128)
    assert (M+radius)**2 < 17
    ac = g+256*f
    v = [M+radius,F(1)]
    Pc = mul(add(scale(power(v,2),2),power(v,4)),
             [f+(2*M+radius)*ac,ac])
    tube_bound = 3**17*factorial_envelope(Pc)
    assert len(Pc)-1 == 5
    assert tube_bound == F(tube['supremum_bound_rational'])
    assert tube_bound < F(5415,10**52)

    # Formal v^-2 coefficients: sums(q+m+1)(q+1)t^q are exactly
    # (1+t)/(1-t)^3+m/(1-t)^2, a geometric-series identity. Check its
    # finite coefficient implementation without using small delta floats.
    coeff_checks = 0
    for m in range(21):
        for q in range(21):
            rhs = math.comb(q+2,2)+(math.comb(q+1,2) if q else 0)+m*(q+1)
            assert rhs == (q+m+1)*(q+1)
            coeff_checks += 1
    # Actual numerator modes are among -10..10. The ray compiler must
    # yield exactly one copy of each m>=0 and m<0 with nonnegative powers
    # of zeta or zetabar. Tags (1,abs(m)) denote coefficients a+b|m|.
    ray_checks = 0
    zero_mode_checks = 0
    for k in range(-10,11):
        N = max(0,(-k+3)//4)
        NN = max(1,(k+3)//4)
        for m in range(-24,25):
            ell = k+4*m
            expected = ((max(ell,0),max(-ell,0)),(1,abs(m)))
            if m >= 0:
                if m < N:
                    got = ((0,-k-4*m),(1,m))
                else:
                    j = m-N
                    got = ((k+4*N+4*j,0),(1,N+j))
            else:
                mm = -m
                if mm < NN:
                    got = ((k-4*mm,0),(1,mm))
                else:
                    j = mm-NN
                    got = ((0,4*NN-k+4*j),(1,NN+j))
            assert got == expected
            ray_checks += 1
            zero_mode_checks += int(ell==0)
    # The literal source point really lies on the supplied family, not an
    # independently specified force table. Analytic all-family equality
    # is reconstructed in REVIEW, not inferred from this one identity.
    xx,yy = F(3,5),F(4,5)
    assert xx*xx+yy*yy == 1
    assert delta*(xx*xx-yy*yy) == -7*delta/25
    output = {'scope':'Independent whole-proof/code intake plus exact Fraction norm/majorant/formal-ray/binding checks; no producer model, symbolic Hessian or kinetic rerun.',
        'producer_hashes':hashes,'inherited_input_bindings':inherited,
        'all_frozen_hashes_match':True,
        'native_norms_match':True,'hessian_polynomial_coefficients':list(map(str,poly)),
        'global_hessian_bound':str(hess),'linear_input_norm_dependence_checked':True,
        'ordinary_saved_global_hessian_bound':str(ordinary),
        'ordinary_bound_scope':'Saved rational bound + full code/proof derivation challenged; no independent full symbolic coefficient re-expansion.',
        'tube_polynomial_coefficients':list(map(str,Pc)),'tube_bound':str(tube_bound),
        'geometric_coefficient_controls':coeff_checks,
        'ray_split_controls':ray_checks,'zero_fourier_boundary_controls':zero_mode_checks,
        'source_point_fraction_identity':True,'seconds_after_stdlib_imports':time.perf_counter()-start,
        'producer_model_rerun':False,'new_ODEs':0,'new_random_draws':0,
        'primary_scope':['Cieliebak--Eliashberg Cor8.16/8.17 global jets/zero set; Prop8.20 compact approximation.',
                         'Johanis Theorem1 fine derivative approximation; epsilon(x)<=1/2 includes two derivatives.',
                         'Tao1707.02389v3 ordinary natural-well universality; old source acceptance not reopened.']}
    (HERE/'STATIC_RECEIPT.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ('all_frozen_hashes_match','native_norms_match','linear_input_norm_dependence_checked','geometric_coefficient_controls','ray_split_controls','zero_fourier_boundary_controls','seconds_after_stdlib_imports','producer_model_rerun')},indent=2))


if __name__ == '__main__':
    main()
