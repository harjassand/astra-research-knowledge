#!/usr/bin/env python3
"""A certified local sampler draw, NOT the full finite-output W1 algorithm.

Only Python, NumPy and SciPy are used. Floating point proposes factors/quantiles;
integer/rational inequalities certify every claim labelled exact below.
The fixed pseudorandom tape makes this a reproducible test, not empirical evidence
of the law or a replacement for independent uniform random bits.
"""
from __future__ import annotations
import argparse, hashlib, json, math, platform, random, sys, time
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
import scipy
from scipy.special import ndtri

sys.set_int_max_str_digits(0)
HERE = Path(__file__).resolve().parent
N, M, D = 128, 2, 4096
INPUT_SEED, DRAW_SEED = 20261010, 17391
Q_BITS, U_BITS, IV_BITS = 48, 32, 192
SCALE, IV_SCALE = 1 << Q_BITS, 1 << IV_BITS
EPSILON = Q(1, 1 << 24)
TIMES = {}


def timed(name):
    class Timer:
        def __enter__(self): self.t = time.perf_counter()
        def __exit__(self, *args): TIMES[name] = time.perf_counter() - self.t
    return Timer()


def fq(x):
    x = Q(x)
    return {'num': str(x.numerator), 'den': str(x.denominator), 'float': float(x)}


def qceil(x): return -((-x.numerator) // x.denominator)
def qfloor(x): return x.numerator // x.denominator


def nearest(x, scale=SCALE):
    """Nearest dyadic, with ties rounded upward. Exact for rational x."""
    return qfloor(Q(x) * scale + Q(1, 2))


def quantize_float(x):
    return np.array([[nearest(Q(float(a))) for a in row] for row in x], dtype=object)


def exact_sqrt_interval(x, bits=Q_BITS):
    """Dyadic enclosure of sqrt(x), using integer square root only."""
    assert x >= 0
    sc = 1 << bits
    lo = math.isqrt((x.numerator * sc * sc) // x.denominator)
    hi = lo if Q(lo * lo, sc * sc) == x else lo + 1
    return Q(lo, sc), Q(hi, sc)


def atan_bounds(q, terms):
    s = sum((Q(1 if k % 2 == 0 else -1, (2*k+1)*q**(2*k+1))
             for k in range(terms)), Q(0))
    nxt = Q(1 if terms % 2 == 0 else -1, (2*terms+1)*q**(2*terms+1))
    return min(s, s+nxt), max(s, s+nxt)


def normal_constant():
    # Machin identity pi = 16 atan(1/5) - 4 atan(1/239), alternating remainder.
    a, b = atan_bounds(5, 180), atan_bounds(239, 60)
    pi_lo, pi_hi = 16*a[0]-4*b[1], 16*a[1]-4*b[0]
    lo = math.isqrt((IV_SCALE**2*pi_hi.denominator)//(2*pi_hi.numerator))
    hi = math.isqrt((IV_SCALE**2*pi_lo.denominator)//(2*pi_lo.numerator))+1
    return (lo, hi), {'pi_lower': fq(pi_lo), 'pi_upper': fq(pi_hi),
                     'inverse_sqrt_2pi_scaled_interval': [str(lo), str(hi)],
                     'interval_fraction_bits': IV_BITS}


NORMAL_C, NORMAL_CONSTANT_PROOF = normal_constant()


def ceildiv(a, b): return -((-a)//b)


def normal_cdf_interval(x):
    """Enclose Phi(x) by exact, directed fixed-point Taylor arithmetic.

    For x>=0 integrate exp(-t^2/2): t_k=x^(2k+1)/(2^k k!(2k+1)).
    Once k exceeds x^2/2 the terms decrease. The alternating-series
    remainder is enclosed by the first omitted term. All operations below
    use Python integers; float ndtri is never trusted by this certificate.
    """
    x = Q(x)
    if x < 0:
        a, b = normal_cdf_interval(-x)
        return IV_SCALE-b, IV_SCALE-a
    assert x <= 12
    tlo, thi = qfloor(x*IV_SCALE), qceil(x*IV_SCALE)
    q = x*x/2
    qlo, qhi = qfloor(q*IV_SCALE), qceil(q*IV_SCALE)
    slo = shi = 0
    for k in range(1024):
        if k % 2 == 0: slo, shi = slo+tlo, shi+thi
        else: slo, shi = slo-thi, shi-tlo
        den = IV_SCALE*(k+1)*(2*k+3)
        nlo = (tlo*qlo*(2*k+1))//den
        nhi = ceildiv(thi*qhi*(2*k+1), den)
        if k >= qceil(q) and nhi <= (1 << (IV_BITS-110)):
            if (k+1) % 2 == 0: shi += nhi
            else: slo -= nhi
            assert slo >= 0 and shi >= slo
            clo, chi = NORMAL_C
            return (IV_SCALE//2+(slo*clo)//IV_SCALE,
                    IV_SCALE//2+ceildiv(shi*chi, IV_SCALE))
        tlo, thi = nlo, nhi
    raise RuntimeError('Taylor limit reached; no result certified')


def gaussian_seed(rng):
    """One finite normal with a certificate for its entire uniform cell.

    The ideal uniform is anywhere in [k/2^b,(k+1)/2^b]. We enclose its exact
    Gaussian quantile, then return the rounded midpoint. Endpoint cells
    are explicitly unsupported here (the global fallback budget is absent).
    """
    k = rng.getrandbits(U_BITS)
    if k == 0 or k == (1 << U_BITS)-1:
        raise RuntimeError('Endpoint-tail cell: global fallback not implemented')
    ulo, uhi = Q(k, 1 << U_BITS), Q(k+1, 1 << U_BITS)
    guesses = [float(ndtri(float(ulo))), float(ndtri(float(uhi)))]
    for pad in [4, 16, 64, 256, 1024, 4096, 65536]:
        lo = qfloor(Q(guesses[0])*SCALE)-pad
        hi = qceil(Q(guesses[1])*SCALE)+pad
        if abs(Q(lo, SCALE)) > 12 or abs(Q(hi, SCALE)) > 12:
            continue
        cdf_lo = normal_cdf_interval(Q(lo, SCALE))
        cdf_hi = normal_cdf_interval(Q(hi, SCALE))
        # Upper CDF at lower endpoint <= ulo, lower CDF at upper >= uhi.
        if Q(cdf_lo[1], IV_SCALE) <= ulo and Q(cdf_hi[0], IV_SCALE) >= uhi:
            z = (lo+hi+1)//2
            error = Q(max(z-lo, hi-z), SCALE)
            return z, {'uniform_cell_index': k, 'uniform_bits': U_BITS,
                       'normal_interval_integer': [str(lo), str(hi)],
                       'rounded_normal_integer': str(z),
                       'fraction_bits': Q_BITS, 'coordinate_error_bound': fq(error),
                       'cdf_upper_at_lower': str(cdf_lo[1]),
                       'cdf_lower_at_upper': str(cdf_hi[0]),
                       'cdf_fraction_bits': IV_BITS}
    raise RuntimeError('Quantile failed certification; no uncertified seed returned')


def make_raw_input():
    rng = random.Random(INPUT_SEED)
    perturb = [np.array([[rng.choice([-1, 1]) for _ in range(N)] for _ in range(N)],
                        dtype=np.int64) for _ in range(M)]
    p0 = np.eye(N, dtype=np.int64)
    p1 = np.zeros((N,N), dtype=np.int64)
    for j in range(N): p1[j ^ 1, j] = 1
    b = [D*p0+perturb[0], D*p1+perturb[1]]
    assert all(np.count_nonzero(a) == N*N for a in b)
    return b


def acquire_certificate(b, require_noncommuting=True):
    # int64 products are safe here; assert a conservative arithmetic bound.
    max_entry = max(int(np.max(np.abs(a))) for a in b)
    assert N*N*max_entry**2 < 2**63
    g = [[int(np.sum(a*c)) for c in b] for a in b]
    detg = g[0][0]*g[1][1]-g[0][1]**2
    assert g[0][0] > 0 and detg > 0
    products = [[(a@c.T).astype(object) for c in b] for a in b]
    mp_num = (g[1][1]*products[0][0]-g[0][1]*(products[0][1]+products[1][0])
              +g[0][0]*products[1][1])
    assert np.array_equal(mp_num, mp_num.T)
    row_upper = [int(mp_num[i,i]+sum(abs(int(mp_num[i,j])) for j in range(N) if j != i))
                 for i in range(N)]
    upper = max(row_upper)
    r = detg//upper
    slack_num = detg-r*upper
    assert slack_num >= 0 and r >= 4*(M+1)**2
    comm = b[0]@b[1]-b[1]@b[0]
    if require_noncommuting: assert np.count_nonzero(comm) > 0
    gram = [[Q(a, D*D) for a in row] for row in g]
    return gram, r, {'method': 'Exact Gram inverse and symmetric Gershgorin bound on Mp',
        'G_integer': g, 'H': [[fq(x) for x in row] for row in gram],
        'det_G': str(detg),
        'H_inverse': [[fq(Q(D*D*(g[1][1] if i==j==0 else g[0][0] if i==j==1 else -g[0][1]), detg))
                       for j in range(2)] for i in range(2)],
        'Mp_common_denominator': str(detg),
        'Mp_Gershgorin_row_numerators': [str(x) for x in row_upper],
        'Mp_operator_upper_bound': fq(Q(upper, detg)),
        'r': r, 'threshold_4_mplus1_squared': 4*(M+1)**2,
        'exact_slack_1_over_r_minus_bound': fq(Q(1,r)-Q(upper,detg)),
        'ideal_acceptance_lower_bound': fq(1-Q(2,r)),
        'nonzero_entries_per_matrix': [int(np.count_nonzero(a)) for a in b],
        'commutator_nonzero_entries': int(np.count_nonzero(comm)),
        'commutator_integer_squared_Frobenius': str(sum(int(x)**2 for x in comm.flat))}


def precision_factor(b, lam):
    """Form exact K at rational lam; certify a proposed dyadic Cholesky.

    We support general rational lambda here, so the same routine verifies
    the two equal-H-radius nonradial witnesses.
    """
    den = math.lcm(*(x.denominator for x in lam))*D
    alnum = sum((a.astype(object)*int(x*den/D) for a,x in zip(b,lam)),
                np.zeros((N,N),dtype=object))
    kden = den**2
    knum = alnum@alnum.T + np.eye(N,dtype=object)*kden
    k_float = np.array([[float(Q(int(x),kden)) for x in row] for row in knum])
    lint = quantize_float(np.linalg.cholesky(k_float))
    pnum = lint@lint.T
    # Common denominator kden*SCALE^2. No claimed BLAS backward-error bound.
    enum = knum*SCALE**2-pnum*kden
    ed = kden*SCALE**2
    emax = max(sum(abs(int(x)) for x in row) for row in enum)
    delta = Q(emax,ed)
    assert delta < 1
    # K >= I by construction, so (1-delta)K <= LL^T <= (1+delta)K.
    detp = Q(math.prod(int(lint[i,i]) for i in range(N)), SCALE**N)**2
    det_bounds = [detp/(1+delta)**N, detp/(1-delta)**N]
    return lint, delta, detp, det_bounds, {'residual_norm_bound_delta': fq(delta),
        'factor_fraction_bits': Q_BITS,
        'rounded_factor_integer': [[str(x) for x in row] for row in lint],
        'det_P': fq(detp), 'det_K_lower': fq(det_bounds[0]),
        'det_K_upper': fq(det_bounds[1]),
        'proof': 'Exact row-sum bound ||K-LL^T||op<=delta and K>=I; det(P)/(1+delta)^N<=det(K)<=det(P)/(1-delta)^N'}


def triangular_solve_transpose(lint, rhs):
    """Solve L^T x=rhs exactly, then independently round coordinates."""
    n = len(rhs)
    out = [Q(0)]*n
    for i in range(n-1,-1,-1):
        out[i] = (rhs[i]-sum((Q(int(lint[j,i]),SCALE)*out[j] for j in range(i+1,n)),Q(0))) / Q(int(lint[i,i]),SCALE)
    return out


def fast_solve_certified(lint, rhs):
    """BLAS proposes x; exact rational residual certifies its solve error.

    Lambda_min(LL^T)>=1-delta is checked separately by precision_factor.
    """
    lfloat = np.array(lint,dtype=float)/SCALE
    guess = np.linalg.solve(lfloat.T,np.array([float(x) for x in rhs]))
    xint = [nearest(Q(float(x))) for x in guess]
    rr = [sum((Q(int(lint[j,i])*xint[j],SCALE**2) for j in range(i,N)),Q(0))-rhs[i]
          for i in range(N)]
    return xint, sum((x*x for x in rr),Q(0))


def one_draw(b, h, r):
    rng = random.Random(DRAW_SEED)
    with timed('certified_gaussian_seeds'):
        seeds = [gaussian_seed(rng) for _ in range(r+2*N)]
    zs = [Q(z,SCALE) for z,_ in seeds]
    seed_error2 = sum((Q(int(c['coordinate_error_bound']['num']),int(c['coordinate_error_bound']['den']))**2
                       for _,c in seeds),Q(0))
    zprop, zchi, gx, gy = zs[:M], zs[M:r], zs[r:r+N], zs[r+N:]
    v = sum((z*z for z in zchi),Q(0))
    assert v > 0
    # 2x2 proposal covariance factor, dyadically rounded and certified.
    hc = quantize_float(np.linalg.cholesky(np.array([[float(x) for x in row] for row in h])))
    hh = [[sum((Q(int(hc[i,k])*int(hc[j,k]),SCALE**2) for k in range(M)),Q(0))
           for j in range(M)] for i in range(M)]
    herror = max(sum((abs(h[i][j]-hh[i][j]) for j in range(M)),Q(0)) for i in range(M))
    hmin = min(h[i][i]-sum(abs(h[i][j]) for j in range(M) if j != i) for i in range(M))
    assert hmin > herror > 0
    scale_interval = exact_sqrt_interval(Q(r)/v)
    scale = sum(scale_interval)/2
    proposal_base = triangular_solve_transpose(hc,zprop)
    lamint = [nearest(scale*z) for z in proposal_base]
    lam = [Q(z,SCALE) for z in lamint]
    with timed('certified_precision_and_acceptance'):
        lint, delta, detp, detbounds, factorproof = precision_factor(b,lam)
        s = sum((lam[i]*h[i][j]*lam[j] for i in range(M) for j in range(M)),Q(0))
        numerator = (1+s/r)**r
        acceptance2 = [numerator/detbounds[1], numerator/detbounds[0]]
        assert 0 < acceptance2[0] <= acceptance2[1] <= 1
        uindex = rng.getrandbits(U_BITS)
        ulo, uhi = Q(uindex,1 << U_BITS), Q(uindex+1,1 << U_BITS)
        decision = 'accept' if uhi*uhi < acceptance2[0] else 'reject' if ulo*ulo > acceptance2[1] else 'undecided'
        assert decision == 'accept', 'This reproducible draw did not certify acceptance'
    with timed('covariance_solve_and_fiber_projection'):
        xint, solve_residual2 = fast_solve_certified(lint,gx)
        solve_error2 = solve_residual2/(1-delta)
        # F_i(x)=x^T A_i. These are exact rational entries.
        fden = D*SCALE
        fint = [[sum(xint[k]*int(b[i][k,j]) for k in range(N)) for j in range(N)] for i in range(M)]
        sint = [[sum(fint[i][k]*fint[j][k] for k in range(N)) for j in range(M)] for i in range(M)]
        dets = sint[0][0]*sint[1][1]-sint[0][1]**2
        assert dets > 0
        s_trace = sint[0][0]+sint[1][1]
        s_min_lower = Q(dets, s_trace*fden*fden)
        # z - F^T(FF^T)^-1 Fz. Common factors fden cancel exactly.
        zints = [int(z*SCALE) for z in gy]
        fz = [sum(fint[i][j]*zints[j] for j in range(N)) for i in range(M)]
        coeff_num = [sint[1][1]*fz[0]-sint[0][1]*fz[1],
                     sint[0][0]*fz[1]-sint[0][1]*fz[0]]
        yexact = [Q(zints[j]*dets-sum(fint[i][j]*coeff_num[i] for i in range(M)), SCALE*dets)
                  for j in range(N)]
        exact_resid = [sum((Q(fint[i][j],fden)*yexact[j] for j in range(N)),Q(0)) for i in range(M)]
        assert exact_resid == [0,0]
        yint = [nearest(y) for y in yexact]
        finalres = [Q(sum(fint[i][j]*yint[j] for j in range(N)), fden*SCALE) for i in range(M)]
        finalres2 = sum((z*z for z in finalres),Q(0))
        assert finalres2 <= EPSILON**2
        yround2 = sum(((Q(yint[j],SCALE)-yexact[j])**2 for j in range(N)),Q(0))
        assert yround2 <= Q(N,4*SCALE*SCALE)
    return {
        'accepted': True, 'seed_generation': {'engine': 'random.Random MT19937, deterministic reproducibility tape only',
            'seed': DRAW_SEED, 'normal_count':len(seeds), 'chi_square_degrees':r-M,
            'normal_constant_certificate':NORMAL_CONSTANT_PROOF,
            'seeds':[c for _,c in seeds], 'sum_coordinate_coupling_error_squared':fq(seed_error2),
            'scope':'Each inverse-CDF cell is certified. Independence/uniformity is conditional on an ideal bit source; this replay is pseudorandom. No global bad-event or W1 budget is implemented.'},
        'proposal': {'lambda':[fq(x) for x in lam], 'lambda_integer':[str(x) for x in lamint],
            'fraction_bits':Q_BITS,'chi_square_rounded_seed_sum':fq(v),
            'H_factor_residual_bound':fq(herror),'H_min_eigenvalue_lower':fq(hmin),
            'sqrt_r_over_V_interval':[fq(x) for x in scale_interval],
            'scope':'Proposal is rounded. A global propagation bound from ideal seeds through H factor, V and lambda is not allocated.'},
        'precision_factor':factorproof,
        'acceptance':{'decision':decision, 's':fq(s), 'squared_acceptance_lower':fq(acceptance2[0]),
            'squared_acceptance_upper':fq(acceptance2[1]),
            'uniform_cell_index':uindex,'uniform_bits':U_BITS,
            'uniform_squared_upper':fq(uhi*uhi),
            'exact_positive_comparison_margin':fq(acceptance2[0]-uhi*uhi),
            'scope':'Decision agrees for every U in this dyadic cell, at the rational rounded lambda. No bound is asserted for replacing the ideal unrounded proposal.'},
        'output':{'fraction_bits':Q_BITS, 'x_integer':[str(x) for x in xint], 'y_integer':[str(y) for y in yint],
            'requested_residual_tolerance':fq(EPSILON),
            'covariance_solve_residual_squared':fq(solve_residual2),
            'squared_distance_to_L_inverse_transpose_rounded_seed_upper':fq(solve_error2),
            'fiber_Gram_min_eigenvalue_lower':fq(s_min_lower),
            'fiber_exact_projection_residual':['0','0'],
            'fiber_rounding_error_squared':fq(yround2),
            'final_residual':[fq(x) for x in finalres], 'final_residual_squared':fq(finalres2),
            'final_residual_check_passed':True,
            'x_norm_squared':fq(sum((Q(x*x,SCALE*SCALE) for x in xint),Q(0))),
            'y_norm_squared':fq(sum((Q(y*y,SCALE*SCALE) for y in yint),Q(0)))}}


def nonradial_check(b,h):
    u=[Q(1),Q(0)]
    # Rational reflection in the H inner product preserves lambda^T H lambda.
    alpha=2*(h[0][0]+h[0][1])/(h[0][0]+2*h[0][1]+h[1][1])
    v=[1-alpha,-alpha]
    radius=lambda x:sum((x[i]*h[i][j]*x[j] for i in range(M) for j in range(M)),Q(0))
    assert radius(u)==radius(v)
    du=precision_factor(b,u)[3]
    dv=precision_factor(b,v)[3]
    assert du[1]<dv[0] or dv[1]<du[0]
    return {'lambda_1':[fq(x) for x in u], 'lambda_2':[fq(x) for x in v],
            'equal_H_radius_squared':fq(radius(u)),
            'det_K_1_interval':[fq(x) for x in du], 'det_K_2_interval':[fq(x) for x in dv],
            'intervals_disjoint':True}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--verify',action='store_true',help='Verify saved artifact with separate verifier')
    args=parser.parse_args()
    if args.verify:
        from verify_draw import main as verify
        verify(); return
    started=time.perf_counter()
    with timed('raw_input_and_native_certificate'):
        b=make_raw_input()
        np.savez_compressed(HERE/'RAW_INPUT.npz',B1=b[0],B2=b[1],denominator=np.array(D))
        h,r,cert=acquire_certificate(b)
    with timed('nonradial_witness'):
        nonradial=nonradial_check(b,h)
    draw=one_draw(b,h,r)
    TIMES['total_before_serialization']=time.perf_counter()-started
    report={'scope':'One certified finite-precision local draw; NOT a complete epsilon-W1 sampler',
        'dimensions':{'m':M,'p':N,'n':N},'parameters':{'input_seed':INPUT_SEED,'draw_seed':DRAW_SEED,
            'perturbation_denominator':D,'rounding_fraction_bits':Q_BITS,'uniform_bits':U_BITS},
        'raw_input_sha256':hashlib.sha256((HERE/'RAW_INPUT.npz').read_bytes()).hexdigest(),
        'environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,
                       'platform':platform.platform()},
        'native_certificate':cert,'nonradial_witness':nonradial,'draw':draw,'timings_seconds':TIMES}
    (HERE/'CERTIFIED_DRAW.json').write_text(json.dumps(report,indent=2)+'\n')
    summary={'r':r,'threshold':4*(M+1)**2,'native_Mp_bound':cert['Mp_operator_upper_bound']['float'],
        'ideal_acceptance_lower_bound':cert['ideal_acceptance_lower_bound']['float'],
        'actual_squared_acceptance_interval':[draw['acceptance']['squared_acceptance_lower']['float'],
                                               draw['acceptance']['squared_acceptance_upper']['float']],
        'precision_factor_residual':draw['precision_factor']['residual_norm_bound_delta']['float'],
        'solve_error_upper':math.sqrt(draw['output']['squared_distance_to_L_inverse_transpose_rounded_seed_upper']['float']),
        'final_residual':math.sqrt(draw['output']['final_residual_squared']['float']),
        'residual_tolerance':float(EPSILON),'nonradial':True,'timings_seconds':TIMES}
    (HERE/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
