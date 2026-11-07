"""Independent exact FCIDUMP assembly and norm bridge to saved binary64 H.

This certifies the declared Ag compression of the exact printed Hamiltonian.
All Slater signs and coefficient accumulation use Python integers. Decimal
FCIDUMP fields have a common denominator. No eigensolve is part of this bridge.
The complete omitted block is acquired here and its acquisition cost is charged.
"""
import time
START = time.perf_counter()
import hashlib
import itertools
import json
import math
import platform
import re
import resource
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parent
SOURCE = BASE.parent / "computation_search"
FCI = BASE / "inputs/N2.STO3G.FCIDUMP"
FLOAT_MATRIX = BASE / "inputs/hamiltonian_binary64.npz"
if not FCI.exists():
    FCI = SOURCE / "source/data/N2.STO3G.FCIDUMP"
if not FLOAT_MATRIX.exists():
    FLOAT_MATRIX = SOURCE / "hamiltonian.npz"


def up_fraction(x):
    f = float(x)
    if Fraction.from_float(f) < x:
        f = math.nextafter(f, math.inf)
    return f


def parse_exact(path):
    txt = path.read_text()
    head, body = re.split(r"&END", txt, maxsplit=1, flags=re.I)
    n = int(re.search(r"NORB\s*=\s*(\d+)", head).group(1))
    ne = int(re.search(r"NELEC\s*=\s*(\d+)", head).group(1))
    raw_sym = list(map(int, re.search(r"ORBSYM\s*=([\d,\s]+)ISYM", head).group(1).replace(",", " ").split()))
    records = []
    for line in body.splitlines():
        fields = line.split()
        if not fields:
            continue
        value = Decimal(fields[0].replace("D", "E"))
        records.append((value, *map(int, fields[1:])))
    digits = max(max(0, -v.as_tuple().exponent) for v, *_ in records)
    scale = 10 ** digits
    h = [[0] * n for _ in range(n)]
    g = {}
    ecore = None
    for value, i, j, k, l in records:
        num = int(value * scale)
        assert Decimal(num) / Decimal(scale) == value
        if i == j == k == l == 0:
            assert ecore is None
            ecore = num
        elif k == l == 0:
            i -= 1
            j -= 1
            assert not h[i][j] or h[i][j] == num
            h[i][j] = h[j][i] = num
        else:
            i -= 1
            j -= 1
            k -= 1
            l -= 1
            for key in {(i,j,k,l),(j,i,k,l),(i,j,l,k),(j,i,l,k),
                        (k,l,i,j),(l,k,i,j),(k,l,j,i),(l,k,j,i)}:
                assert key not in g or g[key] == num
                g[key] = num
    assert ecore is not None and len(raw_sym) == n
    return n, ne, raw_sym, scale, h, g, ecore, len(records)


def remove(state, p):
    if not state & (1 << p):
        return None
    sign = -1 if (state & ((1 << p) - 1)).bit_count() % 2 else 1
    return state ^ (1 << p), sign


def create(state, p):
    if state & (1 << p):
        return None
    sign = -1 if (state & ((1 << p) - 1)).bit_count() % 2 else 1
    return state | (1 << p), sign


def spatial_to_spin_pairs(n, g):
    pairs = list(itertools.combinations(range(2*n), 2))
    terms = {}
    nonzero = 0
    for k, l in pairs:
        entries = []
        for i, j in pairs:
            direct = g.get((i % n, k % n, j % n, l % n), 0) if i//n == k//n and j//n == l//n else 0
            exchange = g.get((i % n, l % n, j % n, k % n), 0) if i//n == l//n and j//n == k//n else 0
            value = direct - exchange
            if value:
                entries.append((i, j, value))
                nonzero += 1
        terms[k, l] = entries
    return terms, nonzero


def assemble(states, n, h, g, ecore):
    lookup = {state: k for k, state in enumerate(states)}
    assert len(lookup) == len(states)
    pair_terms, nterms = spatial_to_spin_pairs(n, g)
    one_terms = {q: [(p, h[p % n][q % n]) for p in range(2*n)
                     if p//n == q//n and h[p % n][q % n]] for q in range(2*n)}
    H = np.zeros((len(states), len(states)), dtype=np.int64)
    bound = 0
    for col, state in enumerate(states):
        entries = {col: ecore}
        occ = [p for p in range(2*n) if state & (1 << p)]
        for q in occ:
            rem, s1 = remove(state, q)
            for p, value in one_terms[q]:
                made = create(rem, p)
                if made is not None:
                    out, s2 = made
                    row = lookup.get(out)
                    if row is not None:
                        entries[row] = entries.get(row, 0) + s1*s2*value
        for k, l in itertools.combinations(occ, 2):
            rem, s1 = remove(state, k)
            rem, s2 = remove(rem, l)
            for i, j, value in pair_terms[k, l]:
                madej = create(rem, j)
                if madej is None:
                    continue
                out, s3 = madej
                madei = create(out, i)
                if madei is None:
                    continue
                out, s4 = madei
                row = lookup.get(out)
                if row is not None:
                    entries[row] = entries.get(row, 0) + s1*s2*s3*s4*value
        for row, value in entries.items():
            assert -(2**63) <= value < 2**63
            H[row, col] = value
            bound = max(bound, abs(value))
    assert np.array_equal(H, H.T)
    return H, nterms, bound


def exact_norm_bridge(Hnum, scale, Hfloat):
    """Exact infinity norm of Hnum/scale - exact stored binary64 Hfloat."""
    rows, cols = np.where((Hnum != 0) | (Hfloat != 0))
    ratios = [float(Hfloat[i,j]).as_integer_ratio() for i,j in zip(rows,cols)]
    binary_den = max(d for _, d in ratios)
    assert binary_den & (binary_den - 1) == 0
    row_sums = [0] * len(Hnum)
    max_entry = 0
    for i, j, (num, den) in zip(rows, cols, ratios):
        delta = abs(int(Hnum[i,j])*binary_den - num*scale*(binary_den//den))
        row_sums[i] += delta
        max_entry = max(max_entry, delta)
    denom = scale * binary_den
    norm = Fraction(max(row_sums), denom)
    entry = Fraction(max_entry, denom)
    return dict(exact_infinity_norm_numerator=str(norm.numerator),
                exact_infinity_norm_denominator=str(norm.denominator),
                infinity_norm_upper=up_fraction(norm),
                max_entry_error_upper=up_fraction(entry),
                matrix_entries_compared=len(rows))


def main():
    t = time.perf_counter()
    n, ne, raw_sym, scale, h, g, ecore, nrecords = parse_exact(FCI)
    parsed = time.perf_counter()-t
    # D2h Molpro labels to XOR character labels used by PySCF.
    sym_map = {1:0, 2:7, 3:6, 4:1, 5:5, 6:2, 7:3, 8:4}
    orb_sym = [sym_map[x] for x in raw_sym]
    strings = sorted(sum(1<<i for i in comb) for comb in itertools.combinations(range(n), ne//2))
    string_sym = [0 for _ in strings]
    for a, state in enumerate(strings):
        irrep = 0
        for p in range(n):
            if state & (1<<p):
                irrep ^= orb_sym[p]
        string_sym[a] = irrep
    old = np.load(FLOAT_MATRIX)
    addr = old["addresses"]
    assert len(set(addr.tolist())) == len(addr)
    states = [strings[int(a)//len(strings)] | (strings[int(a)%len(strings)] << n) for a in addr]
    allowed = [a*len(strings)+b for a in range(len(strings)) for b in range(len(strings)) if string_sym[a] == string_sym[b]]
    assert set(allowed) == set(addr.tolist())
    t = time.perf_counter()
    Hnum, nterms, maxnum = assemble(states, n, h, g, ecore)
    assembly = time.perf_counter()-t
    t = time.perf_counter()
    bridge = exact_norm_bridge(Hnum, scale, old["H"])
    bridge_seconds = time.perf_counter()-t
    sym_break_h = sum(abs(h[p][q]) for p in range(n) for q in range(n) if orb_sym[p] != orb_sym[q]) * 2
    sym_break_g = sum(abs(value) for (p,q,r,s), value in g.items() if orb_sym[p]^orb_sym[q]^orb_sym[r]^orb_sym[s]) * 2
    sym_break = Fraction(sym_break_h+sym_break_g, scale)
    np.savez_compressed(BASE / "exact_decimal_hamiltonian.npz", H_numerator=Hnum, denominator=str(scale), addresses=addr)
    result = dict(
        status="EXACT_DECIMAL_ASSEMBLY_AND_NORM_BRIDGE_PASSED",
        scope="P_Ag H_printed_decimal P_Ag; Nalpha=Nbeta=7; nuclear scalar included; finite-basis computational model only",
        input_sha256=hashlib.sha256(FCI.read_bytes()).hexdigest(),
        saved_float_input_sha256=hashlib.sha256(FLOAT_MATRIX.read_bytes()).hexdigest(),
        saved_float_input_path=str(FLOAT_MATRIX),
        decimal_denominator=str(scale), records=nrecords,
        norb=n, spin_orbitals=2*n, electron_count=ne, determinant_count=len(states),
        molpro_orbsym=raw_sym, xor_orbsym=orb_sym,
        antisymmetric_pair_matrix_nonzeros=nterms,
        exact_integer_matrix_nonzeros=int(np.count_nonzero(Hnum)),
        max_matrix_integer_abs=str(maxnum),
        parse_seconds=parsed, exact_assembly_seconds=assembly,
        exact_bridge_seconds=bridge_seconds, bridge=bridge,
        symmetry_forbidden_terms_norm_upper=up_fraction(sym_break),
        symmetry_note="Printed small symmetry-breaking coefficients exist. Certified target is the declared Ag compression, not an asserted exactly invariant subspace of all printed coefficients. A bound for the full Nalpha=Nbeta=7 Hamiltonian additionally needs all other symmetry sectors or an independently certified global floor.",
        arithmetic="Python unbounded integer coefficient accumulation and exact common-denominator norm; only final displayed norm upper rounded to binary64 via exact Fraction comparison",
        energy_and_inference_cost="UNKNOWN; no actual telemetry available",
        elapsed_seconds=time.perf_counter()-START,
        peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        platform=platform.platform())
    (BASE/"EXACT_BRIDGE.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
