"""Finite ideal-instrument diagnostic for deferred Hamiltonian calibration.

This executes the new local calibration and a two-qubit retrospective reader.
It does not simulate the continuous field collector or certify a laboratory.
Synthetic Bernoulli observations are sampled from computed model probabilities.
"""
import itertools
import json
import math
from pathlib import Path
import numpy as np
from scipy.linalg import expm, eigvalsh
from scipy.stats import poisson

HERE = Path(__file__).resolve().parent
I = np.eye(2, dtype=complex)
PAULI = {"I": I, "X": np.array([[0, 1], [1, 0]], complex),
         "Y": np.array([[0, -1j], [1j, 0]], complex),
         "Z": np.diag([1., -1.]).astype(complex)}

def kron_all(xs):
    a = np.array([[1.]], complex)
    for x in xs:
        a = np.kron(a, x)
    return a

def pm(s):
    return kron_all(PAULI[x] for x in s)

def ptrace(rho, keep, n):
    keep = list(keep)
    drop = [i for i in range(n) if i not in keep]
    axes = keep + drop + [n+i for i in keep] + [n+i for i in drop]
    a = rho.reshape([2]*(2*n)).transpose(axes)
    a = a.reshape(2**len(keep), 2**len(drop), 2**len(keep), 2**len(drop))
    return np.einsum("aibi->ab", a)

def product_on(a, sites_a, b, sites_b, n):
    order = list(sites_a) + list(sites_b)
    assert sorted(order) == list(range(n))
    inverse = [order.index(i) for i in range(n)]
    return np.kron(a, b).reshape([2]*(2*n)).transpose(
        inverse + [n+i for i in inverse]).reshape(2**n, 2**n)

def replace(rho, sites, state, n):
    rest = [i for i in range(n) if i not in sites]
    return product_on(state, sites, ptrace(rho, rest, n), rest, n)

def local_u(rho, u, sites, n):
    sites = list(sites)
    rest = [i for i in range(n) if i not in sites]
    order = sites + rest
    axes = order + [n+i for i in order]
    a = rho.reshape([2]*(2*n)).transpose(axes)
    a = a.reshape(2**len(sites), 2**len(rest), 2**len(sites), 2**len(rest))
    a = np.einsum("ab,bxcy,dc->axdy", u, a, u.conj(), optimize=True)
    inverse = [order.index(i) for i in range(n)]
    return a.reshape([2]*(2*n)).transpose(inverse + [n+i for i in inverse]).reshape(rho.shape)

def apply_source_channel(rho, e, ns, n):
    ds, dr = 2**ns, 2**(n-ns)
    a = rho.reshape(ds, dr, ds, dr).transpose(0, 2, 1, 3).reshape(ds*ds, dr*dr)
    return (e @ a).reshape(ds, ds, dr, dr).transpose(0, 2, 1, 3).reshape(rho.shape)

def source_liouvillian(h, rate, ns):
    d = 2**ns
    l = -1j * (np.kron(h, np.eye(d)) - np.kron(np.eye(d), h.T))
    for i in range(ns):
        for p in "XYZ":
            label = ["I"]*ns
            label[i] = p
            w = pm(label)
            l += rate/4 * (np.kron(w, w.conj()) - np.eye(d*d))
    return l

def bell(d):
    v = np.eye(d).reshape(-1)/math.sqrt(d)
    return np.outer(v, v)

SWAP = np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]], complex)

def record(rng, ns, rate, w, required):
    events = []
    for i in range(ns):
        if i in required:
            z = math.exp(-rate*w)
            count = int(poisson.ppf(z + rng.random()*(1-z), rate*w))
            count = max(count, 1)
        else:
            count = rng.poisson(rate*w)
        events.extend((float(t), i) for t in rng.uniform(0, w, count))
    return sorted(events)

def calibration_mean(h, rate, label, tau, w, rng):
    ns = len(label)
    supp = [i for i, p in enumerate(label) if p != "I"]
    i = supp[0]
    qp = next(p for p in "XYZ" if p != label[i])
    qlabel = ["I"]*ns
    qlabel[i] = qp
    p, q = pm(label), pm(qlabel)
    r = 1j*p @ q
    # R is supported on supp. Its local tensor representation preserves order.
    rlocal = ptrace(r, supp, ns)/(2**(ns-len(supp)))
    n = ns + len(supp) + 1
    a_sites = list(range(ns, ns+len(supp)))
    bsite = n-1
    rho = np.kron(np.eye(2**ns)/2**ns,
                  np.kron(np.diag([1.] + [0.]*(2**len(supp)-1)), I/2))
    front = record(rng, ns, rate, w, supp)
    last = {j: max(t for t, site in front if site == j) for j in supp}
    old = 0.
    for t, j in front:
        rho = local_u(rho, expm(-1j*h*(t-old)), range(ns), n)
        if j in last and t == last[j]:
            rho = replace(rho, [j, a_sites[supp.index(j)]], bell(2), n)
        else:
            rho = replace(rho, [j], I/2, n)
        old = t
    rho = local_u(rho, expm(-1j*h*(w-old)), range(ns), n)
    rho = apply_source_channel(rho, expm(tau*source_liouvillian(h, rate, ns)), ns, n)
    back = record(rng, ns, rate, w, [i])
    first = min(t for t, site in back if site == i)
    old = 0.
    for t, j in back:
        rho = local_u(rho, expm(-1j*h*(t-old)), range(ns), n)
        if j == i and t == first:
            rho = local_u(rho, SWAP, [i, bsite], n)
        else:
            rho = replace(rho, [j], I/2, n)
        old = t
    rho = local_u(rho, expm(-1j*h*(w-old)), range(ns), n)
    ab = ptrace(rho, a_sites + [bsite], n)
    measured = float(np.trace(np.kron(rlocal.T, PAULI[qp]) @ ab).real)
    e = expm(tau*source_liouvillian(h, rate, ns))
    ideal = float(np.trace(q @ (e @ r.reshape(-1)).reshape(2**ns,2**ns)).real/2**ns)
    derivative = float(np.trace(q @ (source_liouvillian(h,rate,ns) @ r.reshape(-1)).reshape(2**ns,2**ns)).real/2**ns)
    return measured, ideal, derivative

def captured_choi(h, events, final_t, ns):
    ne = len(events)
    n = 2*ns+ne
    sr = list(range(ns)) + list(range(ns+ne, n))
    baths = list(range(ns, ns+ne))
    rho = product_on(bell(2**ns), sr, np.eye(2**ne)/2**ne, baths, n)
    old = 0.
    for j, (t, site) in enumerate(events):
        rho = local_u(rho, expm(-1j*h*(t-old)), range(ns), n)
        rho = local_u(rho, SWAP, [site, ns+j], n)
        old = t
    rho = local_u(rho, expm(-1j*h*(final_t-old)), range(ns), n)
    return ptrace(rho, range(ns,n), n)

def decoded_choi(captured, hhat, events, final_t, ns):
    ne = len(events)
    n = 2*ns+ne
    rho = np.kron(np.eye(2**ns)/2**ns, captured)
    future = final_t
    for j in range(ne-1, -1, -1):
        t, site = events[j]
        rho = local_u(rho, expm(1j*hhat*(future-t)), range(ns), n)
        rho = local_u(rho, SWAP, [site, ns+j], n)
        future = t
    rho = local_u(rho, expm(1j*hhat*future), range(ns), n)
    return ptrace(rho, list(range(ns)) + list(range(ns+ne,n)), n)

def main():
    rng = np.random.default_rng(20261105)
    ns, rate = 2, 4.
    coefficients = {"XI": .37, "IY": -.23, "ZZ": .41, "XY": .19, "ZX": -.17}
    labels = ["".join(p) for p in itertools.product("IXYZ", repeat=ns) if p != ("I",)*ns]
    h = sum(v*pm(p) for p,v in coefficients.items())
    bnorm = sum(abs(v) for v in coefficients.values())
    tau, w, histories, shots = .015, .0002, 40, 2000000
    estimates, checks = {}, []
    for label in labels:
        trials = np.array([calibration_mean(h,rate,label,tau,w,rng) for _ in range(histories)])
        c, ideal, derivative = trials.mean(axis=0)
        count = rng.binomial(shots, (1+c)/2)
        estimates[label] = (2*count/shots-1)/(2*tau)
        checks.append({"label":label,"true_coefficient":coefficients.get(label,0.),
                       "estimated_coefficient":estimates[label],"clock_average_correlation":c,
                       "zero_window_correlation":ideal,"derivative":derivative,
                       "max_window_error":float(np.max(abs(trials[:,0]-trials[:,1]))),
                       "window_error_bound":4*bnorm*w,
                       "accepted_clock_probability":(-math.expm1(-rate*w))**(sum(p!='I' for p in label)+1)})
    assert max(abs(x["derivative"]-2*x["true_coefficient"]) for x in checks)<1e-10
    assert all(x["max_window_error"]<=x["window_error_bound"]+1e-12 for x in checks)
    hhat = sum(v*pm(p) for p,v in estimates.items())
    events = [(0.05,0),(0.10,1),(0.20,0),(0.30,1)]
    final_t = .35
    capture = captured_choi(h,events,final_t,ns)
    known = decoded_choi(capture,h,events,final_t,ns)
    learned = decoded_choi(capture,hhat,events,final_t,ns)
    target = bell(2**ns)
    tn = lambda a:float(sum(abs(eigvalsh((a+a.conj().T)/2))))
    modelnorm = float(max(abs(eigvalsh(h-hhat))))
    result = {"scope":"Synthetic ideal reset/export diagnostic; no physical data, no continuous collector simulation, no theorem-scale sampling executed.",
              "seed":20261105,"n":ns,"r":rate,"tau":tau,"window_width":w,
              "conditional_clock_histories_per_coefficient":histories,
              "synthetic_accepted_Bernoulli_shots_per_coefficient":shots,
              "checks":checks,
              "unknown_H_operator_error":modelnorm,
              "retrospective_example":{"record":events,"capture_time":final_t,
                 "known_H_choi_trace_error":tn(known-target),
                 "learned_H_choi_trace_error":tn(learned-target),
                 "learned_vs_known_choi_trace_distance":tn(learned-known),
                 "uniform_model_mismatch_bound":2*final_t*modelnorm,
                 "known_H_entanglement_fidelity":float(np.trace(target@known).real),
                 "learned_H_entanglement_fidelity":float(np.trace(target@learned).real)},
              "cost_warning":"Accepted shots have very small clock probability. They are binomial simulations, not executed rejected attempts. The full theorem pays all attempts."}
    assert result["retrospective_example"]["learned_vs_known_choi_trace_distance"]<=2*final_t*modelnorm+1e-10
    (HERE/"output_calibration_diagnostic.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="checks"},indent=2))

if __name__ == "__main__":
    main()
