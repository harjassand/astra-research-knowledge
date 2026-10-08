"""Finite Gibbs-sector and measurement diagnostics; not a substitute for proof."""
from math import comb, e, exp, gamma, lgamma, log, pi, sqrt
from pathlib import Path
import json
import numpy as np


alpha = 4/3
i0 = gamma(3/4)*alpha**(-3/4)/4
target_partition = 8*sqrt(2/pi)*i0
target_second_moment = alpha**(-1/2)*gamma(5/4)/gamma(3/4)
target_chi_constant = 2*(gamma(5/4)/gamma(3/4))**2
ustar = 648+24*exp(6)*(480/e)**(5/4)
astar = 216*ustar


def sectors(n):
    twice_j = np.arange(n % 2, n+1, 2, dtype=int)
    js = twice_j/2
    logweights = []
    for spin_twice, j in zip(twice_j, js):
        lower = (n-int(spin_twice))//2
        log_binomial = lgamma(n+1)-lgamma(lower+1)-lgamma(n-lower+1)
        logweights.append(2*log(2*j+1)-log(n/2+j+1)
                          +log_binomial-n*log(2)+2*j*(j+1)/n)
    logweights = np.array(logweights)
    largest = np.max(logweights)
    weights = np.exp(logweights-largest)
    probs = weights/np.sum(weights)
    partition = exp(largest)*np.sum(weights)
    return js, probs, partition


sector_diagnostics = []
for n in [256, 257, 512, 1024, 1025, 2048, 4096, 8192, 16384]:
    js, probs, partition = sectors(n)
    scale = n**0.75
    moment = np.dot(probs, np.exp((js/scale)**2))
    second = np.dot(probs, js*(js+1))/n**1.5
    assert abs(np.sum(probs)-1) < 1e-13
    assert partition >= scale/216
    assert moment <= astar
    c_pair = ((4/3)*np.dot(probs, js*(js+1))-n)/(n*(n-1))
    sector_diagnostics.append({"N": n,
        "scaled_partition": float(partition/scale),
        "partition_limit": target_partition,
        "scaled_spin_second_moment": float(second),
        "second_moment_limit": target_second_moment,
        "exponential_square_moment": float(moment),
        "finite_pair_chi_coefficient": float(1.5*n*c_pair*c_pair),
        "limiting_pair_chi_coefficient": target_chi_constant})


def measured_local_count(n, r):
    js, sector_probs, partition = sectors(n)
    tails = np.cumsum((sector_probs/(2*js+1))[::-1])[::-1]
    global_m = np.arange(-n, n+1, 2)/2
    lookup = (np.abs(global_m)-n % 2/2).astype(int)
    magnetic_probs = tails[lookup]
    assert abs(np.sum(magnetic_probs)-1) < 1e-12
    denominator = comb(n, r)
    local = np.zeros(r+1)
    for k, weight in enumerate(magnetic_probs):
        if weight == 0:
            continue
        for count in range(max(0, r-(n-k)), min(k, r)+1):
            local[count] += weight*(comb(k, count)*comb(n-k, r-count)/denominator)
    assert abs(np.sum(local)-1) < 1e-11
    assert np.max(abs(local-local[::-1])) < 1e-12
    return local


xgrid = np.linspace(0, 4, 50001)
density = xgrid*xgrid*np.exp(-alpha*xgrid**4)/i0
assert abs(np.trapezoid(density, xgrid)-1) < 1e-9
measurement_diagnostics = []
for n, r in [(256, 2), (1024, 2), (256, 16), (512, 22),
             (1024, 32), (256, 32), (1024, 64), (1024, 181)]:
    local = measured_local_count(n, r)
    white_count = np.array([comb(r, count)/2**r for count in range(r+1)])
    magnetic = 2*np.arange(r+1)-r
    cosine = np.cos(magnetic/sqrt(r))
    gap = float(np.dot(white_count-local, cosine))
    critical_ratio = r/sqrt(n)
    predicted_gap = exp(-0.5)*(1-np.trapezoid(
        density*np.sinc(2*sqrt(critical_ratio)*xgrid/pi), xgrid))
    local_js = np.arange(r % 2, r+1, 2)/2
    spin_probs = []
    white_spin_probs = []
    for j in local_js:
        index = int(r/2+j)
        next_probability = local[index+1] if index+1 <= r else 0
        spin_probs.append((2*j+1)*(local[index]-next_probability))
        lower = int(r/2-j)
        multiplicity = comb(r, lower)-(comb(r, lower-1) if lower else 0)
        white_spin_probs.append((2*j+1)*multiplicity/2**r)
    spin_probs = np.array(spin_probs)
    white_spin_probs = np.array(white_spin_probs)
    assert np.min(spin_probs) >= 0
    assert abs(np.sum(spin_probs)-1) < 1e-10
    assert abs(np.sum(white_spin_probs)-1) < 1e-12
    quantum_chi = float(np.sum(spin_probs*spin_probs/white_spin_probs)-1)
    mask = spin_probs > 0
    quantum_kl = float(np.sum(spin_probs[mask]*np.log(spin_probs[mask]/white_spin_probs[mask])))
    quantum_trace = float(np.sum(abs(spin_probs-white_spin_probs))/2)
    count_mask = local > 0
    count_kl = float(np.sum(local[count_mask]*np.log(local[count_mask]/white_count[count_mask])))
    count_trace = float(np.sum(abs(local-white_count))/2)
    assert quantum_trace >= abs(gap)/2-1e-11
    assert quantum_kl >= gap*gap/2-1e-11
    assert quantum_kl >= count_kl-1e-11
    assert quantum_trace >= count_trace-1e-11
    assert quantum_kl <= np.log1p(quantum_chi)+1e-10
    measurement_diagnostics.append({"N": n, "r": r,
        "r_over_sqrt_N": critical_ratio,
        "quantum_chi2": quantum_chi,
        "below_window_chi_prediction": target_chi_constant*r*(r-1)/n,
        "quantum_KL": quantum_kl,
        "quantum_trace_distance": quantum_trace,
        "count_KL": count_kl,
        "count_total_variation": count_trace,
        "bounded_cosine_gap": gap,
        "critical_limit_cosine_gap": float(predicted_gap)})

results = {"scope": "Finite diagnostics of exact sector/count formulas, not theorem validation.",
           "explicit_exponential_square_constant": astar,
           "quartic_density_normalizer": i0,
           "sharp_below_window_chi_constant": target_chi_constant,
           "sector_diagnostics": sector_diagnostics,
           "measurement_diagnostics": measurement_diagnostics}
Path(__file__).with_name("verification_results.json").write_text(json.dumps(results, indent=2)+"\n")
print(json.dumps(results, indent=2))
