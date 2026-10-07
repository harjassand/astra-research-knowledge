"""Bounded Dicke-Gaussian quadrature with exact posterior certification.

Numerical acquisition: mpmath Cholesky + symmetric eigensolve.
Certificate: exact rational final binomial mixture versus rational exp intervals.
No interval-eigensolver claim. Requires Python 3.10+ and mpmath 1.3.
"""
import argparse
import bisect
from fractions import Fraction as F
from functools import lru_cache
import json
import math
import os
from pathlib import Path
import random
import time

# These prototypes use assertions as exact verification obligations. Refuse
# an interpreter mode that would silently remove them.
if not __debug__:
    raise RuntimeError('certified compiler requires Python without -O/-OO')

# mpmath itself does not call BLAS. Bound any optional dependency threads.
for _name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
              "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_name] = "1"
import mpmath as mp

N_CAP = 64


def ceil_fraction(x):
    return -((-x.numerator) // x.denominator)


def as_record(x):
    x = F(x)
    return {"numerator": str(x.numerator), "denominator": str(x.denominator)}


def from_record(x):
    return F(int(x["numerator"]), int(x["denominator"]))


def ceil_log2_reciprocal(x):
    """Least nonnegative b with 2**(-b) <= positive rational x."""
    x = F(x)
    if x <= 0:
        raise ValueError("positive accuracy required")
    b = max(0, x.denominator.bit_length() - x.numerator.bit_length())
    while F(1, 1 << b) > x:
        b += 1
    return b


def outward_dyadic(x, bits, up=False):
    scaled = F(x) * (1 << bits)
    z = ceil_fraction(scaled) if up else scaled.numerator // scaled.denominator
    return F(z, 1 << bits)


def exp_negative_interval(r, accuracy_bits):
    """Exact rational enclosure of exp(-r), r>=0, width <=2^-accuracy_bits.

    Range reduce to [0,1], enclose exp(y) by positive Taylor remainder,
    invert and square with outward dyadic rounding. All arithmetic is exact.
    """
    r = F(r)
    if r < 0:
        raise ValueError("r must be nonnegative")
    if not r:
        return F(1), F(1), {"terms": 0, "squarings": 0}
    s = max(0, r.numerator.bit_length() - r.denominator.bit_length())
    while r > (1 << s):
        s += 1
    y = r / (1 << s)
    bits = accuracy_bits + s + 8
    cutoff = F(1, 1 << (bits + 3))
    total = F(1)
    term = F(1)
    degree = 0
    while True:
        nxt = term * y / (degree + 1)
        rem = nxt / (1 - y / (degree + 2))
        if rem <= cutoff:
            break
        total += nxt
        term = nxt
        degree += 1
    lo = outward_dyadic(1 / (total + rem), bits)
    hi = outward_dyadic(1 / total, bits, up=True)
    for _ in range(s):
        lo = outward_dyadic(lo * lo, bits)
        hi = min(F(1), outward_dyadic(hi * hi, bits, up=True))
    assert 0 <= lo <= hi <= 1
    assert hi - lo <= F(1, 1 << accuracy_bits)
    return lo, hi, {"terms": degree + 1, "squarings": s}


def exponents(n, delta, h):
    if n == 0:
        return [F(0)]
    return [-delta * F((2*k-n)**2, 4*n) + h * F(2*k-n, 2)
            for k in range(n+1)]


def target_intervals(n, delta, h, bits):
    a = exponents(n, delta, h)
    peak = max(a)
    enclosed = [exp_negative_interval(peak - x, bits) for x in a]
    total_lo = sum(x[0] for x in enclosed)
    total_hi = sum(x[1] for x in enclosed)
    assert total_lo >= 1
    populations = [(lo/total_hi, hi/total_lo) for lo, hi, _ in enclosed]
    stats = {"max_taylor_terms": max(t["terms"] for _, _, t in enclosed),
             "max_squarings": max(t["squarings"] for _, _, t in enclosed)}
    return populations, stats


def recovered_populations(n, node_integers, weight_integers, bits):
    """Independent exact integer evaluation, common denominator D**(n+1)."""
    D = 1 << bits
    assert len(node_integers)==len(weight_integers)>0
    assert all(0 <= x <= D for x in node_integers)
    assert all(w >= 0 for w in weight_integers)
    assert sum(weight_integers) == D
    denominator = D ** (n+1)
    q = [F(math.comb(n,k) * sum(w * x**k * (D-x)**(n-k)
                               for x,w in zip(node_integers,weight_integers)),
           denominator) for k in range(n+1)]
    assert sum(q) == 1
    assert all(x >= 0 for x in q)
    return q


def certify_measure(n, delta, h, nodes, weights, bits, exp_bits):
    q = recovered_populations(n, nodes, weights, bits)
    intervals, stats = target_intervals(n, delta, h, exp_bits)
    errors = [max(abs(qk-lo), abs(qk-hi))
              for qk,(lo,hi) in zip(q,intervals)]
    l1 = sum(errors)
    # Store small exact upper bounds, rather than huge recovered fractions.
    bound_bits = max(bits + 32, exp_bits)
    return {
        "kind": "EXACT_RATIONAL_POSTERIOR_CERTIFICATE",
        "definition": "trace_distance = half trace_norm",
        "population_l1_upper": as_record(outward_dyadic(l1,bound_bits,True)),
        "target_trace_distance_upper": as_record(outward_dyadic(l1/2,bound_bits,True)),
        "max_population_error_upper": as_record(outward_dyadic(max(errors),bound_bits,True)),
        "exp_interval_bits": exp_bits,
        "bound_rounding_bits": bound_bits,
        "normalization_exact": True,
        "nodes_nonnegative_and_at_most_one_exact": True,
        "weights_nonnegative_exact": True,
        **stats,
    }


def apportion_weights(weights, bits):
    D = 1 << bits
    total = mp.fsum(weights)
    raw = [w / total * D for w in weights]
    ints = [int(mp.floor(x)) for x in raw]
    leftover = D - sum(ints)
    assert 0 <= leftover <= len(ints)
    order = sorted(range(len(ints)), key=lambda i: raw[i]-ints[i], reverse=True)
    for i in order[:leftover]:
        ints[i] += 1
    return ints


def phase_sampling_budget(n,bits):
    q = n+1
    if q & (q-1) == 0:
        return (q-1).bit_length(),F(0)
    return bits,F(q,2*(1 << bits))


def numeric_quadrature(n, delta, h, dps):
    with mp.workdps(dps):
        mh = mp.mpf(h.numerator) / h.denominator
        a = [mp.mpf(x.numerator)/x.denominator for x in exponents(n,delta,h)]
        peak = max(a)
        unnormalized = [mp.exp(x-peak) for x in a]
        total = mp.fsum(unnormalized)
        p = [x/total for x in unnormalized]
        target_u = [mp.fsum(mp.mpf(math.comb(k,l))*p[k]/math.comb(n,l)
                           for k in range(l,n+1)) for l in range(n+1)]
        target_u[0] = mp.mpf(1)
        if n == 0:
            return [mp.mpf(0)], [mp.mpf(1)], {"type":"VACUOUS", "dps":dps}
        if n == 1:
            return [target_u[1]], [mp.mpf(1)], {"type":"ONE_SITE", "dps":dps}
        # Acquire at zero field. The positive polynomial tilt below reproduces
        # all populations exactly for exact quadrature, and avoids ill-
        # conditioned moment matrices when the field concentrates at an edge.
        a0 = [mp.mpf(x.numerator)/x.denominator for x in exponents(n,delta,F(0))]
        base_raw = [mp.exp(x-max(a0)) for x in a0]
        base_total = mp.fsum(base_raw)
        base_p = [x/base_total for x in base_raw]
        u = [mp.fsum(mp.mpf(math.comb(k,l))*base_p[k]/math.comb(n,l)
                    for k in range(l,n+1)) for l in range(n+1)]
        u[0] = mp.mpf(1)
        m = n // 2
        d = m+1
        H = mp.matrix([[u[i+j] for j in range(d)] for i in range(d)])
        K = mp.matrix(d,d)
        for i in range(d):
            for j in range(d):
                if i+j+1 <= n:
                    K[i,j] = u[i+j+1]
        if n % 2 == 0:
            top = mp.matrix([[u[i+j+1] for j in range(m)] for i in range(m)])
            v = mp.matrix([u[i+m+1] for i in range(m)])
            K[m,m] = (v.T * mp.lu_solve(top,v))[0]
        L = mp.cholesky(H)
        Linv = L**-1
        J = Linv*K*Linv.T
        asymmetry = max(abs(J[i,j]-J[j,i]) for i in range(d) for j in range(d))
        J = (J+J.T)/2
        eigenvalues, eigenvectors = mp.eigsy(J)
        nodes = [eigenvalues[i] for i in range(d)]
        weights = [eigenvectors[0,i]**2 for i in range(d)]
        radau_zero_before_clamp = abs(nodes[0]) if n%2 == 0 else mp.mpf(0)
        if n % 2 == 0:
            nodes[0] = mp.mpf(0)
        tol = mp.mpf(10)**(-dps//3)
        if any(x < -tol or x > 1+tol for x in nodes):
            raise ArithmeticError("numerical nodes outside support; increase precision")
        nodes = [max(mp.mpf(0),min(mp.mpf(1),x)) for x in nodes]
        field_factor = mp.exp(mh)
        tilt_factors = [(1-x)+field_factor*x for x in nodes]
        tilted_log_weights = [mp.log(w)+n*mp.log(t) for w,t in zip(weights,tilt_factors)]
        max_log_weight = max(tilted_log_weights)
        weights = [mp.exp(v-max_log_weight) for v in tilted_log_weights]
        weight_total = mp.fsum(weights)
        weights = [w/weight_total for w in weights]
        nodes = [field_factor*x/t for x,t in zip(nodes,tilt_factors)]
        moment_error = max(abs(mp.fsum(w*x**ell for x,w in zip(nodes,weights))-target_u[ell])
                           for ell in range(n+1))
        population_error = max(abs(math.comb(n,k)*mp.fsum(w*x**k*(1-x)**(n-k)
                                  for x,w in zip(nodes,weights))-p[k])
                               for k in range(n+1))
        diagnostics = {
            "type": "GAUSSIAN_ODD" if n%2 else "RADAU_ZERO_EVEN",
            "field_acquisition": "h=0 quadrature followed by positive exponential tilt",
            "dps": dps, "dimension": d,
            "numeric_moment_error": mp.nstr(moment_error,12),
            "numeric_population_error": mp.nstr(population_error,12),
            "numeric_J_asymmetry": mp.nstr(asymmetry,12),
            "numeric_Radau_zero_before_clamp": mp.nstr(radau_zero_before_clamp,12),
            "numeric_min_weight": mp.nstr(min(weights),12),
            "numeric_min_node": mp.nstr(min(nodes),12),
            "numeric_max_node": mp.nstr(max(nodes),12),
            "numeric_condition_H_inf": mp.nstr(mp.norm(H,'inf')*mp.norm(H**-1,'inf'),12),
            "status": "FLOATING_DIAGNOSTICS_ONLY",
        }
        return nodes, weights, diagnostics


def compile_state(n, delta="0", h="0", epsilon="1e-20", bits=None,
                  dps=None, max_attempts=3, density_bits=None):
    start = time.perf_counter()
    delta, h, epsilon = F(delta), F(h), F(epsilon)
    if not isinstance(n,int) or not 0 <= n <= N_CAP:
        raise ValueError("bounded implementation requires 0<=n<=64")
    if not 0 <= delta <= 1:
        raise ValueError("internally admitted analytic family requires 0<=delta<=1")
    if not 0 < epsilon < 1:
        raise ValueError("requires 0<epsilon<1")
    requested_bits = ceil_log2_reciprocal(epsilon)
    bits = max(128,requested_bits+16+(n+1).bit_length()) if bits is None else bits
    density_bits = max(bits,requested_bits+8+(n+1).bit_length()) if density_bits is None else density_bits
    if bits < 1 or density_bits < 1:
        raise ValueError("positive bit budgets required")
    density_budget = F(8*n,1 << density_bits)
    phase_bits,phase_budget = phase_sampling_budget(n,bits)
    # Arbitrarily large binary h has a bounded exact product-state branch.
    threshold_bits = ceil_log2_reciprocal(epsilon/4)
    endpoint = n if h >= 0 else 0
    tail_bound = F(1,(1 << threshold_bits)-1)
    if n > 0 and abs(h)-delta >= threshold_bits:
        D = 1 << bits
        nodes = [D if endpoint==n else 0]
        weights = [D]
        certificate = {
            "kind":"EXACT_ENDPOINT_TAIL_CERTIFICATE",
            "target_trace_distance_upper":as_record(tail_bound),
            "tail_proof":"p[n-r]/p[n] <= exp(-(abs(h)-delta)*r) <= 2^(-threshold_bits*r)",
            "threshold_bits":threshold_bits,
            "normalization_exact":True,
            "nodes_nonnegative_and_at_most_one_exact":True,
            "weights_nonnegative_exact":True,
        }
        diagnostics = {"type":"CERTIFIED_LARGE_FIELD_PRODUCT_BRANCH",
                       "status":"NO_EIGENSOLVE_REQUIRED"}
        attempts = []
    else:
        dps = max(100,math.ceil(bits*0.302)+2*n+50) if dps is None else dps
        attempts = []
        for attempt in range(max_attempts):
            attempt_start = time.perf_counter()
            try:
                xs, ws, diagnostics = numeric_quadrature(n,delta,h,dps)
                with mp.workdps(dps):
                    D = 1 << bits
                    nodes = [max(0,min(D,int(mp.floor(x*D+mp.mpf('0.5'))))) for x in xs]
                    weights = apportion_weights(ws,bits)
                certificate = certify_measure(n,delta,h,nodes,weights,bits,bits+32)
                phase_bits,phase_budget = phase_sampling_budget(n,bits)
                accepted = from_record(certificate["target_trace_distance_upper"])+density_budget+phase_budget <= epsilon
                attempts.append({"dps":dps,"bits":bits,"accepted":accepted,
                                 "elapsed_seconds":time.perf_counter()-attempt_start})
                if accepted:
                    break
            except (ArithmeticError,ValueError,ZeroDivisionError) as error:
                attempts.append({"dps":dps,"bits":bits,"accepted":False,
                                 "error":repr(error),"elapsed_seconds":time.perf_counter()-attempt_start})
            dps += 60
            bits += 32
            density_bits = max(density_bits,bits)
            density_budget = F(8*n,1 << density_bits)
        else:
            raise ArithmeticError("bounded acquisition exhausted; no uncertified output: "+json.dumps(attempts))
    total_budget = from_record(certificate["target_trace_distance_upper"])+density_budget+phase_budget
    if total_budget > epsilon:
        raise ArithmeticError("certificate does not meet requested accuracy")
    model = {
        "format":"DICKE_GAUSSIAN_CERTIFIED_V1", "n":n,
        "delta":as_record(delta),"h":as_record(h),"epsilon":as_record(epsilon),
        "node_weight_bits":bits,"node_integers":[str(x) for x in nodes],
        "weight_integers":[str(w) for w in weights],
        "phase_modulus":n+1,"component_count":len(nodes)*(n+1),
        "phase_sampling_bits":phase_bits,"phase_uniform_TV_upper":as_record(phase_budget),
        "predetermined_random_bits_per_sample":bits+phase_bits,
        "product_components_stored":False,
        "density_bits":density_bits,"finite_density_trace_distance_upper":as_record(density_budget),
        "total_output_trace_distance_upper":as_record(total_budget),
        "certificate":certificate,"floating_diagnostics":diagnostics,
        "acquisition_attempts":attempts,"compile_seconds":time.perf_counter()-start,
        "analytic_input_dependency":"c07_s02 AXIAL_ONE_CERTIFICATE plus c02_s01/c05_s03 independent audits; exponential h tilting preserves positive coherent measure",
        "randomness":"Exact sampling law assumes independent uniform random bits; seeded examples use Python PRNG",
    }
    return model


def verify_model(model):
    """Recompute the certificate using exact arithmetic, independent of eigensolve."""
    assert model['format']=='DICKE_GAUSSIAN_CERTIFIED_V1'
    n, bits = model["n"],model["node_weight_bits"]
    delta,h = from_record(model["delta"]),from_record(model["h"])
    assert type(n) is int and 0<=n<=N_CAP
    assert type(bits) is int and bits>=1
    assert type(model['density_bits']) is int and model['density_bits']>=1
    assert 0<=delta<=1 and 0<from_record(model['epsilon'])<1
    assert type(model['phase_modulus']) is int and model['phase_modulus']==n+1
    assert type(model['phase_sampling_bits']) is int and model['phase_sampling_bits']>=0
    assert type(model['predetermined_random_bits_per_sample']) is int
    assert isinstance(model['node_integers'],list) and isinstance(model['weight_integers'],list)
    assert len(model['node_integers'])==len(model['weight_integers'])>0
    assert type(model['component_count']) is int and model['component_count']==len(model['node_integers'])*(n+1)
    assert model['product_components_stored'] is False
    assert all(type(x) is str and str(int(x))==x for x in model['node_integers']+model['weight_integers'])
    nodes = [int(x) for x in model["node_integers"]]
    weights = [int(x) for x in model["weight_integers"]]
    recovered_populations(n,nodes,weights,bits)
    stored = model["certificate"]
    if stored["kind"] == "EXACT_RATIONAL_POSTERIOR_CERTIFICATE":
        fresh = certify_measure(n,delta,h,nodes,weights,bits,stored["exp_interval_bits"])
        for key in ("target_trace_distance_upper","population_l1_upper","max_population_error_upper"):
            assert from_record(fresh[key]) <= from_record(stored[key])
    elif stored["kind"] == "EXACT_ENDPOINT_TAIL_CERTIFICATE":
        b = stored["threshold_bits"]
        assert n>0 and abs(h)-delta >= b
        assert nodes == [(1 << bits) if h>=0 else 0] and weights == [1 << bits]
        assert F(1,(1 << b)-1) <= from_record(stored["target_trace_distance_upper"])
    else:
        raise ValueError("unknown certificate kind")
    density_budget = F(8*n,1 << model["density_bits"])
    assert density_budget == from_record(model["finite_density_trace_distance_upper"])
    phase_bits,phase_budget = phase_sampling_budget(n,bits)
    assert phase_bits == model['phase_sampling_bits']
    assert phase_budget == from_record(model['phase_uniform_TV_upper'])
    assert model['predetermined_random_bits_per_sample'] == bits+phase_bits
    total = from_record(stored["target_trace_distance_upper"])+density_budget+phase_budget
    assert total == from_record(model["total_output_trace_distance_upper"])
    assert total <= from_record(model["epsilon"])
    return True


@lru_cache(maxsize=8)
def pi_interval(bits):
    """Machin identity with exact alternating-series bounds."""
    def arctan_inverse(q):
        total = F(0)
        j = 0
        while True:
            term = F((-1)**j,(2*j+1)*q**(2*j+1))
            total += term
            j += 1
            nxt = F((-1)**j,(2*j+1)*q**(2*j+1))
            if abs(nxt) <= F(1,1 << (bits+14)):
                return min(total,total+nxt),max(total,total+nxt)
    a,b = arctan_inverse(5)
    c,d = arctan_inverse(239)
    return 16*a-4*d,16*b-4*c


@lru_cache(maxsize=8)
def trig_degree(bits):
    degree = 8
    while F(7**(degree+1),math.factorial(degree+1)) > F(1,1 << (bits+8)):
        degree += 1
    return degree


def trig_intervals(j, modulus, bits):
    plo,phi = pi_interval(bits)
    alo,ahi = 2*F(j,modulus)*plo,2*F(j,modulus)*phi
    center = (alo+ahi)/2
    radius = (ahi-alo)/2
    degree = trig_degree(bits)
    rem = F(7**(degree+1),math.factorial(degree+1))
    sin_value = sum((F((-1)**((k-1)//2))*center**k/math.factorial(k)
                     for k in range(1,degree+1,2)),F(0))
    cos_value = sum((F((-1)**(k//2))*center**k/math.factorial(k)
                     for k in range(0,degree+1,2)),F(0))
    error = radius+rem
    assert 2*error <= F(1,1 << (bits+5))
    def enclosure(value):
        return max(F(-1),value-error),min(F(1),value+error)
    return enclosure(cos_value),enclosure(sin_value)


def interval_product(a,b):
    vals = [x*y for x in a for y in b]
    return min(vals),max(vals)


def conservative_component(interval,bits):
    """Round toward zero using the interval endpoint nearest zero."""
    lo,hi = interval
    if lo > 0:
        return outward_dyadic(lo,bits)
    if hi < 0:
        return outward_dyadic(hi,bits,up=True)
    return F(0)


def finite_local_density(x,j,modulus,bits):
    """Certified PSD dyadic approximation to the sampled pure local state."""
    D = 1 << bits
    r2 = x*(1-x)
    scaled = r2*D*D
    root_floor = math.isqrt(scaled.numerator // scaled.denominator)
    rlo = F(root_floor,D)
    rhi = rlo if rlo*rlo == r2 else F(root_floor+1,D)
    cosine,sine = trig_intervals(j,modulus,bits)
    real_interval = interval_product((rlo,rhi),cosine)
    imag_interval = interval_product((rlo,rhi),(-sine[1],-sine[0]))
    re = conservative_component(real_interval,bits)
    im = conservative_component(imag_interval,bits)
    assert re*re+im*im <= r2  # PSD exact; trace one exact.
    local_error = max(abs(re-real_interval[0]),abs(re-real_interval[1]))
    local_error += max(abs(im-imag_interval[0]),abs(im-imag_interval[1]))
    assert local_error <= F(8,D)
    return {"diagonal":[as_record(1-x),as_record(x)],
            "upper_right_real":as_record(re),"upper_right_imag":as_record(im),
            "lower_left":"complex conjugate of upper right",
            "PSD_and_trace_one_exact":True,
            "local_trace_distance_upper":as_record(outward_dyadic(local_error,bits+16,True))}


def sample_product(model,rng=None,phase_mode='bounded'):
    """Draw one iid-product component; exact probabilities from uniform bits.

    Returns compact exact pure-state recipe and a certified finite PSD local
    density matrix to repeat on n sites. Uses no expanded 2**n matrix.
    """
    # Cheap schema bindings for sampler inputs; callers verify the expensive
    # posterior certificate once after compilation or loading.
    assert model['format']=='DICKE_GAUSSIAN_CERTIFIED_V1'
    assert type(model['n']) is int and 0<=model['n']<=N_CAP
    assert model['phase_modulus']==model['n']+1
    expected_phase_bits,expected_phase_bias=phase_sampling_budget(model['n'],model['node_weight_bits'])
    assert model['phase_sampling_bits']==expected_phase_bits
    assert expected_phase_bias<=from_record(model['phase_uniform_TV_upper'])
    assert F(8*model['n'],1 << model['density_bits'])<=from_record(model['finite_density_trace_distance_upper'])
    rng = random.SystemRandom() if rng is None else rng
    bits = model["node_weight_bits"]
    weights = [int(x) for x in model["weight_integers"]]
    cumulative = []
    count = 0
    for w in weights:
        count += w
        cumulative.append(count)
    draw = rng.getrandbits(bits)
    index = bisect.bisect_right(cumulative,draw)
    x = F(int(model["node_integers"][index]),1 << bits)
    modulus = model["phase_modulus"]
    phase_bits = model['phase_sampling_bits']
    used = bits
    if phase_mode == 'bounded':
        j = (rng.getrandbits(phase_bits)*modulus) >> phase_bits
        used += phase_bits
        phase_status = 'BOUNDED_DYADIC_PHASE; bias to uniform included in ensemble budget'
    elif phase_mode == 'exact':
        phase_bits = (modulus-1).bit_length()
        j = 0
        phase_status = 'EXACT_UNIFORM_PHASE; rejection has finite expected cost'
        if modulus > 1:
            while True:
                j = rng.getrandbits(phase_bits)
                used += phase_bits
                if j < modulus:
                    break
    else:
        raise ValueError('phase_mode must be bounded or exact')
    density = finite_local_density(x,j,modulus,model["density_bits"])
    with mp.workdps(50):
        mx = mp.mpf(x.numerator)/x.denominator
        angles = {"polar_theta":mp.nstr(2*mp.asin(mp.sqrt(mx)),30),
                  "azimuth_phi":mp.nstr(2*mp.pi*j/modulus,30),
                  "status":"DISPLAY_ONLY_FLOATING_ANGLES; use exact recipe or certified density"}
    return {"node_index":index,"phase_index":j,"phase_modulus":modulus,
            "phase_sampling_status":phase_status,
            "x":as_record(x),"sites":model["n"],"random_bits_consumed":used,
            "exact_pure_local_ket":"sqrt(1-x)|0> + exp(2*pi*i*phase_index/phase_modulus)*sqrt(x)|1>",
            "finite_product_local_density":density,"display_angles":angles,
            "finite_product_trace_distance_to_sampled_pure_upper":
                as_record(model["n"]*from_record(density["local_trace_distance_upper"])),
            "ensemble_total_target_trace_distance_upper":model["total_output_trace_distance_upper"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n',type=int,required=True)
    parser.add_argument('--delta',default='0.5')
    parser.add_argument('--h',default='1/3')
    parser.add_argument('--epsilon',default='1e-20')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--samples',type=int,default=2)
    parser.add_argument('--seed',type=int,default=0)
    args = parser.parse_args()
    model = compile_state(args.n,args.delta,args.h,args.epsilon)
    verify_model(model)
    rng = random.Random(args.seed)
    result = {"model":model,"samples":[sample_product(model,rng) for _ in range(args.samples)]}
    text = json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text,end='')


if __name__ == '__main__':
    main()
