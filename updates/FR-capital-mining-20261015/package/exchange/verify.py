#!/usr/bin/env python3
"""Reproducible finite checks for condition-matched quantum state exchange.

These are synthetic linear-algebra checks, NOT hardware data, a novelty proof,
or a comparison with the strongest experimentally available protocols.
Requires Python 3.10+ and NumPy. Run: python verify.py
"""
from __future__ import annotations
import json
from fractions import Fraction
from itertools import product
from pathlib import Path
import numpy as np

TOL = 2e-12
RNG = np.random.default_rng(20261015)


def density(v: np.ndarray) -> np.ndarray:
    return np.outer(v, v.conj())


def tensor(*ops: np.ndarray) -> np.ndarray:
    out = np.array([[1.0 + 0j]])
    for op in ops:
        out = np.kron(out, op)
    return out


def marginal(rho: np.ndarray, dims: tuple[int, ...], keep: tuple[int, ...]) -> np.ndarray:
    """Partial trace, preserving the requested order of retained subsystems."""
    if len(set(keep)) != len(keep) or any(k < 0 or k >= len(dims) for k in keep):
        raise ValueError("Invalid retained-subsystem indices")
    dim = int(np.prod(dims))
    if rho.shape != (dim, dim):
        raise ValueError("Density matrix shape does not match subsystem dimensions")
    rest = tuple(k for k in range(len(dims)) if k not in keep)
    order = keep + rest
    kdim = int(np.prod([dims[k] for k in keep]))
    rdim = int(np.prod([dims[k] for k in rest]))
    arr = rho.reshape(dims + dims).transpose(order + tuple(k + len(dims) for k in order))
    return np.trace(arr.reshape(kdim, rdim, kdim, rdim), axis1=1, axis2=3)


def swap_matrix(dims: tuple[int, ...], a: int, b: int) -> np.ndarray:
    if dims[a] != dims[b]:
        raise ValueError("Swapped subsystems must have equal dimensions")
    dim = int(np.prod(dims))
    result = np.zeros((dim, dim), dtype=complex)
    for i in range(dim):
        coord = list(np.unravel_index(i, dims))
        coord[a], coord[b] = coord[b], coord[a]
        result[np.ravel_multi_index(tuple(coord), dims), i] = 1
    return result


def apply_permutation(rho: np.ndarray, unitary: np.ndarray) -> np.ndarray:
    # All unitaries passed here are computational-basis permutation matrices.
    order = np.argmax(unitary, axis=1)
    return rho[np.ix_(order, order)]


def td(a: np.ndarray, b: np.ndarray) -> float:
    delta = (a-b + (a-b).conj().T)/2
    return float(np.abs(np.linalg.eigvalsh(delta)).sum()/2)


def random_state(dim: int) -> np.ndarray:
    m = RNG.normal(size=(dim, dim)) + 1j*RNG.normal(size=(dim, dim))
    rho = m @ m.conj().T
    return rho / np.trace(rho)


I2 = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
P0, P1 = np.diag([1.,0.]), np.diag([0.,1.])
PLUS = np.array([1,0,0,1], dtype=complex)/np.sqrt(2)
MINUS = np.array([1,0,0,-1], dtype=complex)/np.sqrt(2)
BELL = density(PLUS)
BELL_MINUS = density(MINUS)
CZ = np.diag([1.,1.,1.,-1.])
ECHO = tensor(I2, CZ)  # subsystem order R,S,E
BELL_READ = tensor(BELL, I2)


def memory_state(u: float) -> np.ndarray:
    return (1-u)*tensor(BELL, P0) + u*tensor(BELL_MINUS, P1)


def bell_success(rho: np.ndarray, echo: bool) -> float:
    state = ECHO @ rho @ ECHO.conj().T if echo else rho
    return float(np.trace(BELL_READ @ state).real)


def run() -> dict:
    results: dict = {
        "scope": "Synthetic finite checks; no experimental data and no novelty/advantage certification",
        "seed": 20261015,
    }
    # 1. An arbitrary mixed RSE state, including quantum correlations, not only a classical toy.
    max_error = 0.0
    max_rs_error = 0.0
    for _ in range(32):
        dims = (2,2,3)
        rho = random_state(12)
        pair = tensor(rho, rho)
        sw = swap_matrix(dims+dims, 1, 4)
        exchanged = apply_permutation(pair, sw)
        # Recipient site 1 now contains donor S2: follow donor reference R2.
        graft = marginal(exchanged, dims+dims, (3,1,2))
        target = tensor(marginal(rho, dims, (0,1)), marginal(rho, dims, (2,)))
        max_error = max(max_error, td(graft, target))
        max_rs_error = max(max_rs_error, td(marginal(graft, dims, (0,1)), marginal(rho,dims,(0,1))))
    assert max_error < TOL and max_rs_error < TOL
    results["random_quantum_identity"] = {
        "instances":32, "dimensions_R_S_E":[2,2,3],
        "maximum_trace_distance": max_error,
        "maximum_reference_system_marginal_error":max_rs_error,
    }
    # 2. Exact rational decision-reversal model.
    p = [Fraction(9,10), Fraction(1,10)]
    u = [Fraction(1,5), Fraction(2,5)]
    prod_echo = [(1-x)**2+x*x for x in u]
    native_echo = Fraction(1)
    isolate = sum(pc*(1-uc) for pc,uc in zip(p,u))
    ideal_echo = sum(pc*f for pc,f in zip(p,prod_echo))
    rows = []
    for n in [2,4,8,16,32,64]:
        a = [(1-pc)**(n-1) for pc in p]
        singleton_mass = sum(pc*ac for pc,ac in zip(p,a))
        f = sum(pc*(ac+(1-ac)*fc) for pc,ac,fc in zip(p,a,prod_echo))
        assert native_echo > isolate > f
        assert abs(f-ideal_echo) <= singleton_mass
        rows.append({"batch_size":n,"singleton_mass":float(singleton_mass),
                     "echo_fidelity":float(f),"isolate_fidelity":float(isolate),
                     "echo_fidelity_exact":str(f)})
    # Independently enumerate all classical label configurations for small batches.
    max_enum_error = 0.0
    for n in range(2,9):
        numerical = 0.0
        for labels in product(range(2), repeat=n):
            prob = float(np.prod([float(p[c]) for c in labels]))
            scores = [1.0 if labels.count(c)==1 else float(prod_echo[c]) for c in labels]
            numerical += prob*sum(scores)/n
        formula = sum(float(pc)*((1-float(pc))**(n-1)
                    +(1-(1-float(pc))**(n-1))*float(fc)) for pc,fc in zip(p,prod_echo))
        max_enum_error=max(max_enum_error, abs(numerical-formula))
    assert max_enum_error < TOL
    quantum_error = 0.0
    for x in u:
        rho = memory_state(float(x))
        prod_rho = tensor(marginal(rho,(2,2,2),(0,1)), marginal(rho,(2,2,2),(2,)))
        quantum_error=max(quantum_error, abs(bell_success(rho,True)-1),
                          abs(bell_success(rho,False)-float(1-x)),
                          abs(bell_success(prod_rho,True)-float((1-x)**2+x*x)))
    assert quantum_error < TOL
    results["decision_reversal"] = {
        "flag_probabilities":[float(x) for x in p],
        "residual_phase_probabilities":[float(x) for x in u],
        "native_echo":float(native_echo),"native_isolate":float(isolate),
        "ideal_exchange_echo":float(ideal_echo),"ideal_exchange_isolate":float(isolate),
        "finite_batches":rows,
        "label_enumeration_maximum_error":max_enum_error,
        "density_matrix_maximum_error":quantum_error,
        "warning":"The engineered model is already soluble and has no demonstrated baseline advantage.",
    }
    # 3. A positive naive exchange signal without conditional correlations.
    results["conditioning_false_positive"] = {
        "state":"C is uniform; given C=c, S=c and E=c deterministically",
        "future_score":"Probability that S equals E",
        "native":1.0,"conditional_exchange":1.0,"unconditional_exchange":0.5,
    }
    # 4. Identical one-replica marginals do NOT establish independent replicas.
    v0, v1 = tensor(BELL,P0), tensor(BELL_MINUS,P1)
    up = 0.2
    correlated_pair = (1-up)*tensor(v0,v0) + up*tensor(v1,v1)
    dims6 = (2,)*6
    sw = swap_matrix(dims6,1,4)
    actual = marginal(apply_permutation(correlated_pair,sw),dims6,(3,1,2))
    independent_prediction = (1-up)**2+up*up
    actual_score = bell_success(actual,True)
    assert abs(actual_score-1)<TOL
    results["replica_dependence_counterexample"] = {
        "each_replica_state": "(1-u)|Phi+><Phi+| tensor |0><0| + u|Phi-><Phi-| tensor |1><1|",
        "u":up,"independent_prediction":independent_prediction,
        "common_hidden_bit_actual_echo":actual_score,
        "error":actual_score-independent_prediction,
    }
    # 5. Perfect reduced SWAP and perfect round-trip do not bound hidden-bath disturbance.
    start = tensor(v0,v0)
    flip_baths = tensor(I2,I2,X,I2,I2,X)
    bad = flip_baths @ sw
    final = apply_permutation(start,bad)
    bad_local = marginal(final,dims6,(3,1,2))
    ideal_local = marginal(apply_permutation(start,sw),dims6,(3,1,2))
    bad_score = bell_success(bad_local,True)
    ideal_score = bell_success(ideal_local,True)
    round_trip = float(np.linalg.norm(bad @ bad - np.eye(64)))
    assert abs(bad_score)<TOL and abs(ideal_score-1)<TOL and round_trip<TOL
    reduced_gate_error=0.0
    for _ in range(10):
        arbitrary = random_state(64)
        after_bad=apply_permutation(arbitrary,bad)
        after_good=apply_permutation(arbitrary,sw)
        # Entire accessible R1,S1,R2,S2 channel is identical even for correlated inputs.
        reduced_gate_error=max(reduced_gate_error,
            td(marginal(after_bad,dims6,(0,1,3,4)),marginal(after_good,dims6,(0,1,3,4))))
    assert reduced_gate_error<TOL
    results["hidden_bath_gate_counterexample"]={
        "implemented_gate":"SWAP(S1,S2) tensor X(E1) tensor X(E2)",
        "ideal_future_echo_fidelity":ideal_score,"bad_future_echo_fidelity":bad_score,
        "round_trip_operator_error":round_trip,
        "accessible_channel_maximum_error":reduced_gate_error,
    }
    # Conservative independent-batch Hoeffding accounting; no within-batch iid claim.
    B,N,K,delta=4000,32,4,.05
    r=float(np.sqrt(np.log(2*K/delta)/(2*B)))
    results["conservative_sampling_example"]={
        "batches_per_arm":B,"replicas_per_batch":N,"arms":K,
        "failure_probability":delta,"per_arm_radius":r,
        "two_arm_statistical_radius":2*r,"prepared_replicas":B*N*K,
        "scope":"Assumed independent batches, bounded unbiased scores, fixed policies; excludes systematic errors.",
    }
    results["all_assertions_passed"] = True
    return results


if __name__ == "__main__":
    data=run()
    target=Path(__file__).with_name("verification_results.json")
    target.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(data,indent=2))
