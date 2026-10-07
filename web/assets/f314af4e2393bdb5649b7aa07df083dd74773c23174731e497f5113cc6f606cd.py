"""Finite checks of the bounded-steering EPR/antisymmetric ladder obstructions.

These are channel/formula diagnostics, not a proof of the broad conjecture.
Requires NumPy only. Run from the task root with python3.
"""
import itertools
import json
import math
from pathlib import Path
import numpy as np

rng = np.random.default_rng(701469683)
worst = {"epr_consistency": 0., "epr_broadcast_error": 0.,
         "epr_joint_trace": 0., "epr_trace_bound_violation": 0.,
         "anti_steering": 0., "anti_consistency": 0.,
         "anti_split_isometry": 0., "anti_variance": 0.,
         "anti_trace_bound_violation": 0.}
counts = {"epr_fixtures": 0, "epr_joint_channels": 0,
          "anti_fixtures": 0, "anti_joint_channels": 0}

def kron_all(xs):
    out = np.array([[1.]], dtype=complex)
    for x in xs:
        out = np.kron(out, x)
    return out

def trace_norm(x):
    return float(np.sum(np.abs(np.linalg.eigvalsh((x + x.conj().T)/2))))

def tdist(x, y):
    return trace_norm(x-y)/2

def random_density(d):
    z = rng.normal(size=(d,d)) + 1j*rng.normal(size=(d,d))
    z = z @ z.conj().T + np.eye(d)*.2
    return z / np.trace(z)

def random_contraction(d, tau=None):
    z = rng.normal(size=(d,d)) + 1j*rng.normal(size=(d,d))
    a = (z + z.conj().T)/2
    mean = np.trace(a)/d if tau is None else np.trace(tau@a)
    a -= mean.real*np.eye(d)
    return a / np.max(np.abs(np.linalg.eigvalsh(a)))

def partial_trace(x, dims, keep):
    keep = sorted(keep)
    d = len(dims)
    t = x.reshape(tuple(dims)+tuple(dims))
    for i in reversed(range(d)):
        if i not in keep:
            t = np.trace(t, axis1=i, axis2=i+d)
            d -= 1
    dk = math.prod(dims[i] for i in keep)
    return t.reshape(dk, dk)

def conditional_product(a, taus, subset):
    # E_S(A) = Tr_{S^c}[(I_S tensor tau_{S^c}) A].
    q = taus[0].shape[0]
    n = len(taus)
    weight = kron_all([np.eye(q) if i in subset else taus[i]
                       for i in range(n)])
    ans = partial_trace(weight@a, [q]*n, subset)
    assert np.linalg.norm(ans-ans.conj().T) < 1e-9
    return (ans+ans.conj().T)/2

def root(x):
    v,u = np.linalg.eigh(x)
    return (u*np.sqrt(np.maximum(v,0)))@u.conj().T

def permute_qubits(x, order, q=2):
    n = len(order)
    return x.reshape([q]*2*n).transpose(order+[n+i for i in order]).reshape(q**n,q**n)

def run_epr(n, l, reps):
    rs = [2**j for j in range(l)]
    assert rs[-1] == n
    all_subsets = {r:list(itertools.combinations(range(n),r)) for r in rs}
    for rep in range(reps):
        taus = [random_density(2) for _ in range(n)]
        tau_all = kron_all(taus)
        a = random_contraction(2**n, tau_all)
        amplitude = .5
        sigmas, rhos, es = {}, {}, {}
        for r in rs:
            m = math.comb(n,r)
            sigmas[r], rhos[r], es[r] = {}, {}, {}
            dist, second_moment = 0., 0.
            for s in all_subsets[r]:
                ts = kron_all([taus[i] for i in s])
                e = conditional_product(a, taus, s)
                rt = root(ts).T
                rho = (ts.T + amplitude*rt@e.T@rt)/m
                sigmas[r][s], rhos[r][s], es[r][s] = ts.T/m, rho, e
                ev = np.linalg.eigvalsh(rho-.5*sigmas[r][s])
                assert ev.min() > -1e-10
                assert np.linalg.eigvalsh(1.5*sigmas[r][s]-rho).min() > -1e-10
                dist += tdist(rho,sigmas[r][s])
                second_moment += np.trace(ts@e@e).real/m
            assert second_moment <= r/n + 1e-9
            violation = dist-amplitude/2*math.sqrt(r/n)
            worst["epr_trace_bound_violation"] = max(worst["epr_trace_bound_violation"],violation)
            if r > 1:
                s = r//2
                marginal = {t:np.zeros_like(rhos[s][t]) for t in all_subsets[s]}
                for flag,x in rhos[r].items():
                    for t in itertools.combinations(flag,s):
                        positions = [flag.index(i) for i in t]
                        marginal[t] += partial_trace(x,[2]*r,positions)/math.comb(r,s)
                residual = max(np.linalg.norm(marginal[t]-rhos[s][t]) for t in marginal)
                worst["epr_consistency"] = max(worst["epr_consistency"],residual)
        # Actual two-output channel, with joint state stored by classical flags.
        # It dephases the input flag, applies reordering isometries to each
        # subset block, and replaces the bottom input by sigma_1 tensor sigma_1.
        # Every joint block is an actual positive output density matrix.
        joint = {}
        for j,r in enumerate(rs):
            for flag,x in rhos[r].items():
                if j == 0:
                    for t,st in sigmas[1].items():
                        for u,su in sigmas[1].items():
                            key = (0,t,0,u)
                            z = float(np.trace(x).real)/l*np.kron(st,su)
                            joint[key] = joint.get(key,0)+z
                else:
                    s = r//2
                    for t in itertools.combinations(flag,s):
                        u = tuple(i for i in flag if i not in t)
                        order = [flag.index(i) for i in t+u]
                        key = (j-1,t,j-1,u)
                        z = permute_qubits(x,list(order))/l/math.comb(r,s)
                        joint[key] = joint.get(key,0)+z
        trace = sum(np.trace(x).real for x in joint.values())
        worst["epr_joint_trace"] = max(worst["epr_joint_trace"],abs(trace-1))
        marginal_b, marginal_c = {}, {}
        for (j,t,h,u),x in joint.items():
            assert np.linalg.eigvalsh(x).min() > -1e-10
            nt,nu = len(t),len(u)
            b = partial_trace(x,[2]*(nt+nu),list(range(nt)))
            c = partial_trace(x,[2]*(nt+nu),list(range(nt,nt+nu)))
            marginal_b[(j,t)] = marginal_b.get((j,t),0)+b
            marginal_c[(h,u)] = marginal_c.get((h,u),0)+c
        for marginal in [marginal_b,marginal_c]:
            error = 0.
            for j,r in enumerate(rs):
                for flag,x in rhos[r].items():
                    got = marginal.get((j,flag),np.zeros_like(x))
                    error += trace_norm(got-x/l)/2
            worst["epr_broadcast_error"] = max(worst["epr_broadcast_error"],abs(error-1/l))
        counts["epr_fixtures"] += 1
        counts["epr_joint_channels"] += 1

def fermionic_j(a,r):
    d = len(a)
    basis = list(itertools.combinations(range(d),r))
    index = {s:i for i,s in enumerate(basis)}
    out = np.zeros((len(basis),len(basis)),dtype=complex)
    for c,s in enumerate(basis):
        for ann in s:
            after = list(s)
            sign1 = (-1)**after.index(ann)
            after.remove(ann)
            for cre in range(d):
                if cre in after:
                    continue
                loc = sum(i<cre for i in after)
                t = tuple(sorted(after+[cre]))
                out[index[t],c] += sign1*(-1)**loc*a[cre,ann]
    return out

def wedge_split(d,r,s):
    bs = list(itertools.combinations(range(d),s))
    bt = list(itertools.combinations(range(d),r-s))
    br = list(itertools.combinations(range(d),r))
    is_,it_ = {x:i for i,x in enumerate(bs)},{x:i for i,x in enumerate(bt)}
    v = np.zeros((len(bs)*len(bt),len(br)),dtype=complex)
    for c,flag in enumerate(br):
        for x in itertools.combinations(flag,s):
            y = tuple(i for i in flag if i not in x)
            inversions = sum(i>j for i in x for j in y)
            v[is_[x]*len(bt)+it_[y],c] = (-1)**inversions/math.sqrt(math.comb(r,s))
    return v,len(bs),len(bt)

def run_anti(d,l,reps):
    rs = [2**j for j in range(l)]
    assert rs[-1] <= d-1
    for _ in range(reps):
        a = random_contraction(d)
        amp = .5
        rhos = {}
        for r in rs:
            m = math.comb(d,r)
            j = fermionic_j(a,r)
            rho = (np.eye(m)-amp*j/(d-r))/m
            rhos[r] = rho
            assert np.linalg.eigvalsh(rho).min() > -1e-10
            assert np.linalg.norm(j-j.conj().T) < 1e-10
            actual_var = np.trace(j@j).real/m/(d-r)**2
            predicted_var = r/((d-1)*(d-r))*np.trace(a@a).real/d
            worst["anti_variance"] = max(worst["anti_variance"],abs(actual_var-predicted_var))
            bound = amp/2*math.sqrt(r/((d-1)*(d-r)))
            worst["anti_trace_bound_violation"] = max(worst["anti_trace_bound_violation"],tdist(rho,np.eye(m)/m)-bound)
            # Build the actual normalized antisymmetric (r+1)-body state
            # as an isometric projector on R tensor wedge^r, then steer it.
            u,dr,db = wedge_split(d,r+1,1)
            omega = u@u.conj().T/math.comb(d,r+1)
            steered = partial_trace(np.kron(np.eye(d)+amp*a,np.eye(db))@omega,[d,db],[1])
            worst["anti_steering"] = max(worst["anti_steering"],np.linalg.norm(steered-rho))
            if r>1:
                v,ds,dt = wedge_split(d,r,r//2)
                residual = np.linalg.norm(v.conj().T@v-np.eye(m))
                worst["anti_split_isometry"] = max(worst["anti_split_isometry"],residual)
                joint = v@rho@v.conj().T
                mb = partial_trace(joint,[ds,dt],[0])
                mc = partial_trace(joint,[ds,dt],[1])
                target = rhos[r//2]
                worst["anti_consistency"] = max(worst["anti_consistency"],np.linalg.norm(mb-target),np.linalg.norm(mc-target))
                counts["anti_joint_channels"] += 1
        counts["anti_fixtures"] += 1

run_epr(2,2,12)
run_epr(4,3,12)
for d,l in [(3,2),(4,2),(5,3),(6,3),(7,3)]:
    run_anti(d,l,12)
assert max(worst.values()) < 1e-8, worst
result = {"seed":701469683,"status":"PASS", "counts":counts,
          "maximum_residuals_or_violations":worst,
          "scope":"finite channel and formula checks only; no broad-conjecture proof or counterexample"}
out = Path(__file__).with_suffix('.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
