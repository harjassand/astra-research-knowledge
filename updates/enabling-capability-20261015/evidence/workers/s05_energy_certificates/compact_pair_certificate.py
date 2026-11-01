"""Integral-space electron/hole pair certificates without N-electron matrix.

These are established D/Q-cone lower bounds, not a novelty claim. The script
asks whether this cheapest exact pair representation competes on this genuine
N2 FCIDUMP. Its lower bound uses only 190-dimensional two-particle matrices.
"""
import time
START = time.perf_counter()
import hashlib
import itertools
import json
import math
import resource
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy import linalg
from pyscf import lib

from exact_decimal_bridge import parse_exact, assemble, exact_norm_bridge, FCI

lib.num_threads(1)
BASE = Path(__file__).resolve().parent
SOURCE = BASE.parent / "computation_search"
AUDIT = BASE / "inputs/STRONG_AUDIT.json"
if not AUDIT.exists():
    AUDIT = SOURCE / "STRONG_AUDIT.json"


def up(x):
    if isinstance(x, Fraction):
        value = float(x)
        return math.nextafter(value, math.inf) if Fraction.from_float(value) < x else value
    return math.nextafter(float(x), math.inf)


def down(x):
    if isinstance(x, Fraction):
        value = float(x)
        return math.nextafter(value, -math.inf) if Fraction.from_float(value) > x else value
    return math.nextafter(float(x), -math.inf)


def F(x):
    return Fraction.from_float(float(x))


def gamma(k):
    z = Fraction(k, 2**53)
    return up(z/(1-z))


def norm_inf(A):
    # Sum of positive exact stored floats, nextafter covers fsum's final rounding.
    return max(up(math.fsum(abs(float(v)) for v in row)) for row in A)


def lower_by_factor(Mnum, denominator):
    M = Mnum.astype(float) / denominator
    bridge = exact_norm_bridge(Mnum, denominator, M)
    approximate = float(linalg.eigh(M, subset_by_index=[0,0], eigvals_only=True)[0])
    shift = approximate - 1e-7
    C = M.copy()
    C[np.diag_indices_from(C)] -= shift
    factor = np.tril(linalg.cholesky(C, lower=True, check_finite=False))
    product = factor @ factor.T
    residual = M-product
    residual[np.diag_indices_from(residual)] -= shift
    raw = norm_inf(residual)
    factor_norm_product = F(norm_inf(factor)) * F(norm_inf(factor.T))
    dot_error = F(gamma(len(M))) * factor_norm_product
    # Computed residual = fl(fl(M-fl(FF^T))-shift I).
    subtract_error = F(gamma(3)) * (F(norm_inf(M))+abs(F(shift))+F(norm_inf(product)))
    delta = up(F(raw)+dot_error+subtract_error)
    lower = down(F(shift)-F(delta)-F(bridge["infinity_norm_upper"]))
    return dict(lower=lower, numerical_smallest=approximate,
                shift=shift, factor_residual_bound=delta,
                conversion_bridge=bridge, dimension=len(M),
                arithmetic_assumptions=["IEEE binary64 basic operations round to nearest",
                    "matrix dot products obey standard gamma_n forward error bound",
                    "no overflow, underflow, or nonfinite results",
                    "math.fsum is correctly rounded for positive finite inputs"])


def main():
    t = time.perf_counter()
    n, ne, os, scale, h, g, ecore, records = parse_exact(FCI)
    parse_seconds = time.perf_counter()-t
    pair_states = [sum(1<<i for i in pair) for pair in itertools.combinations(range(2*n),2)]
    zero_h = [[0]*n for _ in range(n)]
    t = time.perf_counter()
    H1pair, _, _ = assemble(pair_states, n, h, {}, 0)
    Vpair, _, _ = assemble(pair_states, n, zero_h, g, 0)
    assert int(np.abs(H1pair).max())+(ne-1)*int(np.abs(Vpair).max()) < 2**63
    pair_assembly_seconds = time.perf_counter()-t
    t = time.perf_counter()
    electron = lower_by_factor(H1pair+(ne-1)*Vpair, (ne-1)*scale)
    electron["energy_lower"] = down(Fraction(ecore,scale)+math.comb(ne,2)*F(electron["lower"]))
    electron["wall_seconds"] = time.perf_counter()-t
    t = time.perf_counter()
    hhole = [[-h[p][q]-sum(2*g.get((p,q,r,r),0)-g.get((p,r,r,q),0) for r in range(n))
              for q in range(n)] for p in range(n)]
    full_shift = ecore+2*sum(h[p][p] for p in range(n))+sum(2*g.get((p,p,q,q),0)-g.get((p,q,q,p),0)
                                                      for p in range(n) for q in range(n))
    Hhole1, _, _ = assemble(pair_states, n, hhole, {}, 0)
    nhole = 2*n-ne
    assert int(np.abs(Hhole1).max())+(nhole-1)*int(np.abs(Vpair).max()) < 2**63
    hole = lower_by_factor(Hhole1+(nhole-1)*Vpair, (nhole-1)*scale)
    hole["energy_lower"] = down(Fraction(full_shift,scale)+math.comb(nhole,2)*F(hole["lower"]))
    hole["hole_count"] = nhole
    hole["full_occupancy_shift_numerator"] = str(full_shift)
    hole["wall_seconds"] = time.perf_counter()-t
    # One predeclared Pauli-aware split, no post-hoc tuning: F=diag(h_hole).
    # The lowest energy of dGamma(F) in the 6-hole sector is the sum of its
    # six lowest spin-orbital diagonal entries, computed exactly as integers.
    t = time.perf_counter()
    hrem = [row.copy() for row in hhole]
    for p in range(n):
        hrem[p][p] = 0
    Hrem1, _, _ = assemble(pair_states, n, hrem, {}, 0)
    assert int(np.abs(Hrem1).max())+(nhole-1)*int(np.abs(Vpair).max()) < 2**63
    pauli = lower_by_factor(Hrem1+(nhole-1)*Vpair, (nhole-1)*scale)
    free_energy_num = sum(sorted([hhole[p][p] for p in range(n)]*2)[:nhole])
    pauli["energy_lower"] = down(Fraction(full_shift+free_energy_num,scale)
                                 + math.comb(nhole,2)*F(pauli["lower"]))
    pauli["free_fermion_minimum_numerator"] = str(free_energy_num)
    pauli["split"] = "F equals the exact diagonal of h_hole in the supplied orbital basis; no tuning"
    pauli["wall_seconds"] = time.perf_counter()-t
    best_lower = max(electron["energy_lower"],hole["energy_lower"],pauli["energy_lower"])
    upstream = json.loads(AUDIT.read_text())
    input_bridge = json.loads((BASE/"EXACT_BRIDGE.json").read_text())["bridge"]["infinity_norm_upper"]
    upper = up(F(upstream["verified_full_factor_comparator"]["upper"])+F(input_bridge))
    result = dict(
        status="STOP_CHEAP_PAIR_REPRESENTATION_ON_TARGET",
        claim="No new operation or comparative advantage established",
        scope="Exact printed FCIDUMP coefficients; pair lower bounds valid for the entire stated N-electron sector and hence its Ag compression; upper is for the declared Ag compression only",
        source_sha256=hashlib.sha256(FCI.read_bytes()).hexdigest(),
        target_width=0.00159360143764,
        electron_pair=electron, hole_pair=hole, pauli_diagonal_hole_split=pauli,
        best_lower=best_lower, certified_Ag_upper=upper,
        certified_Ag_interval_width=up(F(upper)-F(best_lower)),
        parse_seconds=parse_seconds,
        pair_assembly_seconds=pair_assembly_seconds,
        dimensions={"spin_orbitals":2*n,"two_particle":len(pair_states),"Ag_determinants_not_acquired_by_pair_method":1824},
        guarantee_note="PSD factor plus residual bound certifies each pair eigenvalue floor; exact pair-lifting identity gives N-electron lower floor. Integral-to-pair conversion bridge is included. Standard floating arithmetic model remains an explicit assumption.",
        prior_art="This is the pair-positive (D) and particle-hole-transformed pair-positive (Q) fragment of the fermionic SOS/v2RDM hierarchy. Degree-two SOS positivity and symmetry ideals already contain these certificates.",
        energy_and_inference_cost="UNKNOWN; no telemetry",
        elapsed_seconds=time.perf_counter()-START,
        peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (BASE/"COMPACT_PAIR.json").write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
