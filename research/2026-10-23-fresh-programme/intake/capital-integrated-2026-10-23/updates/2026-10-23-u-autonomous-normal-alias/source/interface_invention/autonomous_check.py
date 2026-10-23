"""Independent finite calculations for AUTONOMOUS_CYCLE.txt; no hardware claim."""

from __future__ import annotations

import json
import math
import numpy as np
from scipy.linalg import expm


def h(p):
    p = np.asarray(p)
    p = p[p > 0]
    return float(-np.dot(p, np.log(p)))


def shift(n):
    return np.roll(np.eye(n), 1, axis=0)


def generator(n, forward, backward=0.0):
    c = shift(n)
    return forward*(c-np.eye(n))+backward*(c.T-np.eye(n))


def ep_stationary(q):
    n = len(q)
    total = 0.0
    for i in range(n):
        for j in range(i):
            a, b = q[i,j], q[j,i]
            if a == b:
                continue
            if a <= 0 or b <= 0:
                return math.inf
            total += (a-b)*math.log(a/b)/n
    return total


def robust_bound(q, t, alpha):
    j = -math.log(alpha)
    r0 = alpha*min((math.pi-j)/8, 0.25)
    g = (math.pi**2-j*j)/2
    b = t*np.linalg.norm(q, 2)
    return r0*math.sqrt(g/(b*b+g))


def main():
    rng = np.random.default_rng(20261023)
    z = np.array([1.,1.,-1.,-1.])
    w = shift(4) @ z
    basis = [(1+z)/4, (1-z)/4]
    ring = []
    assertions = 0
    for kp, km in [(1.,0.),(1.7,0.2),(1.0,0.3),(0.7,0.6)]:
        q = generator(4,kp,km)
        s, d = kp+km, kp-km
        t = math.pi/d
        alpha = math.exp(-s*t)
        p = expm(q*t)
        identity_res = np.max(np.abs(p @ z + alpha*z))
        assert identity_res < 2e-14
        assert np.max(np.abs(p.sum(axis=0)-1)) < 2e-14
        assert np.max(np.abs(p.sum(axis=1)-1)) < 2e-14
        assert np.max(np.abs(q@q.T-q.T@q)) < 1e-14
        assertions += 4
        return_res = 0.0
        for sign, p0 in zip([1,-1],basis):
            target = (1-sign*alpha*z)/4
            res = np.max(np.abs(p@p0-target))
            assert res < 2e-14
            return_res = max(return_res,res)
            assertions += 1
        entropy = ep_stationary(q)
        if km:
            ell = math.log(kp/km)
            assert abs(entropy-d*ell) < 1e-13
            assert abs(entropy*t-math.pi*ell) < 1e-12
            eps = (1-alpha)/2
            delta_h = h(p@basis[0])-h(basis[0])
            assert abs(delta_h-h([eps,1-eps])) < 2e-13
            assertions += 3
        else:
            assert math.isinf(entropy)
            assertions += 1
        timing = []
        for rel in [-0.1,0.01,0.1]:
            dt = t*rel
            pt = expm(q*(t+dt)) @ basis[0]
            sys = np.array([pt[:2].sum(),pt[2:].sum()])
            product = np.repeat(sys/2,2)
            tv = np.linalg.norm(pt-product,1)/2
            beta = alpha*math.exp(-s*dt)*math.cos(d*dt)
            chi = alpha*math.exp(-s*dt)*math.sin(d*dt)
            assert abs(tv-abs(chi)/2) < 2e-14
            assert abs(sys[1]-(1+beta)/2) < 2e-14
            assertions += 2
            timing.append({"relative_time_error":rel,"return_TV":tv})
        ring.append({"k_plus":kp,"k_minus":km,"T":t,"alpha":alpha,
                     "success":(1+alpha)/2,"mode_residual":float(identity_res),
                     "product_return_residual":float(return_res),
                     "stationary_EP_rate":entropy if math.isfinite(entropy) else "infinite",
                     "timing":timing})

    # Verify the normal flat-sign energy inequality and conservative robust
    # residual bound on normal generators whose profiles do not return exactly.
    normal_checks = 0
    smallest_ratio = math.inf
    for n in [4,6,8,10,12,20]:
        c = shift(n)
        for instance in range(4):
            q = sum(float(r)*(np.linalg.matrix_power(c,j)-np.eye(n))
                    for j,r in enumerate(rng.uniform(0.01,1.0,n-1),1))
            zt = rng.permutation(np.r_[np.ones(n//2),-np.ones(n//2)])
            ll = -(q+q.T)/2
            aa = (q-q.T)/2
            assert np.linalg.norm(aa@zt) <= np.linalg.norm(ll@zt)+1e-12
            assertions += 1
            for t in [0.05,0.3,1.0]:
                pp = expm(q*t)
                for alpha in [0.05,0.25,0.8,0.99]:
                    actual = np.linalg.norm(pp@zt+alpha*zt)/np.linalg.norm(zt)
                    lower = robust_bound(q,t,alpha)
                    assert actual+1e-13 >= lower
                    assert t*np.linalg.norm(q,2) <= -2*t*np.diag(q).min()+1e-12
                    smallest_ratio = min(smallest_ratio,actual/lower)
                    assertions += 2
                    normal_checks += 1

    # Directed large rings achieve a good raw logical flip, with residual
    # correlations: this does not contradict exact-return theorems.
    raw_cycles = []
    for n in [8,20,80,200]:
        memory = n//2
        q = generator(n,1.0)
        zz = np.r_[np.ones(memory),-np.ones(memory)]
        p0 = (1+zz)/n
        p = expm(q*memory) @ p0
        wrong = p[:memory].sum()
        memory_marginal = p[:memory]+p[memory:]
        product = np.r_[np.full(memory,wrong/memory),
                        np.full(memory,(1-wrong)/memory)]
        return_tv = np.linalg.norm(p-product,1)/2
        ideal_tv = np.linalg.norm(p-(1-zz)/n,1)/2
        assert np.max(np.abs(memory_marginal-1/memory)) < 1e-13
        assert wrong <= 1/math.sqrt(memory)+1e-13
        assert abs(ideal_tv-wrong) < 1e-13
        assert return_tv <= 2*wrong*(1-wrong)+1e-13
        assertions += 4
        raw_cycles.append({"states":n,"memory_levels":memory,
                           "wrong_probability":float(wrong),
                           "product_return_TV":float(return_tv),
                           "ideal_flip_joint_TV":float(ideal_tv)})

    return {"assertions":assertions,"four_state":ring,
            "normal_robust_instances":normal_checks,
            "smallest_actual_to_robust_bound_ratio":smallest_ratio,
            "large_directed_ring_raw_not_exact_return":raw_cycles,
            "scope":"Floating checks complement proofs; no general nonnormal search or physical validation."}


if __name__ == "__main__":
    print(json.dumps(main(),indent=2))
