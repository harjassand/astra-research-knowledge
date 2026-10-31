"""An exact invariant, coherently driven strip of the native pair corrector.

The long strip is a specified initial error background, not a cold-start
memory failure. No syndrome predicate is added to the tip Hamiltonian.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.integrate import quad_vec
from scipy.linalg import expm
from scipy.stats import poisson

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/"outputs/logical_phase_20261101"


def native_invariant_sector():
    spec = importlib.util.spec_from_file_location("native_young", ROOT/"work/coherent_young_barrier.py")
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    cases = []
    for ell in [1, 3, 8]:
        L = 4*ell+8
        row = 2
        labels = {}
        for j in range(ell+1):
            for q in range(2):
                state = sum(1 << (row*L+x) for x in range(j, ell))
                state ^= q << (row*L+ell)
                labels[state] = (j, q)
        assert len(labels) == 2*(ell+1)
        transitions = 0
        for state, (j, q) in labels.items():
            assert labels[state ^ (1 << (row*L+ell))] == (j, 1-q)
            active = {(x, y) for y in range(L) for x in range(L)
                      if native.pattern(state, x, y, L)[:2] == (1, 1)}
            expected = {(j, row)} if j < ell else ({(ell, row)} if q else set())
            assert active == expected
            for x, y in active:
                target = labels[state ^ (1 << (y*L+x))]
                assert target == ((j+1, q) if j < ell else (ell, 0))
                transitions += 1
        cases.append(dict(ell=ell, L=L, basis_states=len(labels),
                          exact_native_transitions=transitions))
    return cases


def lindblad(H, jumps):
    D = len(H)
    I = np.eye(D)
    G = -1j*(np.kron(I, H)-np.kron(H.T, I))
    for J in jumps:
        A = J.conj().T@J
        G += np.kron(J.conj(), J)-(np.kron(I, A)+np.kron(A.T, I))/2
    return G


def exact_delay_controls():
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Z = np.diag([1., -1.])
    I = np.eye(2)
    J = np.array([[0, 1], [0, 0]], dtype=complex)
    # A single persistent bath, with noncommuting drive and bath Hamiltonian.
    H = np.kron(X/8, (I+Z)/2)+np.kron(I, X/7+Z/11)
    gU = lindblad(H, [])
    init = np.kron(np.diag([1., 0.]), np.ones((2, 2))/2)
    v0 = init.reshape(-1, order="F")
    rows = []
    for ell in [3, 8]:
        for model in ["active", "completed"]:
            jumps = [np.kron(J, I)]
            if model == "completed":
                jumps.append(np.kron(np.diag([1., 0.]), I))
            gD = lindblad(H, jumps)
            # Counter blocks are density matrices; the actual native
            # generator preserves their initially diagonal counter algebra.
            G = np.zeros((16*(ell+1), 16*(ell+1)), dtype=complex)
            for j in range(ell+1):
                G[16*j:16*(j+1), 16*j:16*(j+1)] = gD if j == ell else gU-np.eye(16)
                if j:
                    G[16*j:16*(j+1), 16*(j-1):16*j] = np.eye(16)
            start = np.zeros(16*(ell+1), dtype=complex)
            start[:16] = v0
            for T in [3., 10.]:
                full = (expm(G*T)@start).reshape(ell+1, 16).sum(axis=0)
                # The same persistent bath evolves before AND after the
                # random erasure time. It is never reset in this formula.
                def integrand(u):
                    density = math.exp(-u)*u**(ell-1)/math.factorial(ell-1)
                    return density*(expm(gD*(T-u))@expm(gU*u)@v0)
                conv, error = quad_vec(integrand, 0., T, epsabs=1e-11)
                conv += poisson.cdf(ell-1, T)*(expm(gU*T)@v0)
                residual = np.linalg.norm(full-conv)
                assert residual < 1e-10
                assert abs(np.trace(full.reshape(4, 4, order="F"))-1) < 1e-10
                rows.append(dict(ell=ell, model=model, T=T,
                                 common_bath_dimension=2,
                                 convolution_residual=float(residual),
                                 quadrature_error_preview=float(error)))
    return rows


def large_background_example():
    h = 1/64
    T = math.pi/(2*h)
    ell = 512
    mu = T
    log_tail = -mu+ell*(1+math.log(mu/ell))
    assert log_tail < -420
    # Archimedes' 25/8 < pi < 22/7 gives mu>100 and ell/mu>56/11.
    # Certify exp(13/8)<56/11 with a rational Taylor remainder, so the
    # displayed -420 upper bound does not depend on floating logarithms.
    z = Fraction(13, 8)
    exp_upper = sum(z**j/math.factorial(j) for j in range(13))
    exp_upper += z**13/math.factorial(13)/(1-z/14)
    assert exp_upper < Fraction(56, 11)
    return dict(h_over_kappa="1/64", ell=ell, T_exact="32 pi / kappa",
                tip_error_lower="1-exp(-420)",
                poisson_chernoff_log_upper_preview=log_tail,
                rational_tail_certificate="100+512*(13/8-1)=420; exp(13/8)<56/11",
                argument="p_tip(T) >= P(Gamma(ell,kappa)>T) sin^2(h T)",
                scope="Specified rare long initial strip, unconditional one-face drive; not a logical error, cold-start failure or memory no-go")


def main():
    data = dict(exact_physical_sector=native_invariant_sector(),
                persistent_bath_convolution=exact_delay_controls(),
                coherent_delayed_response=large_background_example())
    data["program_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/"strip_delay_controls.json").write_text(json.dumps(data, indent=2)+"\n")
    print(json.dumps(dict(output=str(OUT/"strip_delay_controls.json"), checks=list(data))))


if __name__ == "__main__":
    main()
