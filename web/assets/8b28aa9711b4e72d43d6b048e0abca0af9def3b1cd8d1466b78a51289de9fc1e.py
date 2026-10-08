"""Independent full-space trace-invariant audit of the Spin(11) star blocks.

This does not import or rerun the candidate extractor.  It contracts the
reported exact multiplicity blocks with their Gram metrics and compares the
resulting full 32^3-dimensional traces against Pauli orthogonality formulas.
"""
import json
from pathlib import Path
from math import comb
import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "work/agents/c5_quantum_dimension_obstruction/cycle10_spin11_probe/spin11_fullstar_blocks.json"
DATA = json.loads(SOURCE.read_text())
IRREP_DIMS = [32 * (comb(11, r) - (comb(11, r - 1) if r else 0)) for r in range(6)]
FULL = 32**3
GRADES = 5


def rational_matrix(raw):
    return sp.Matrix([[sp.Rational(x) for x in row] for row in raw])


def reduced_operators(key):
    block = DATA["blocks"][key]
    gram = rational_matrix(block["gram"])
    inverse = gram.inv()
    return [inverse * rational_matrix(bilinear) for bilinear in block["bilinear_H"]]


def actual_trace_word(word):
    total = 0
    for r, dim in enumerate(IRREP_DIMS):
        for eps in (1, -1):
            key = f"{r},{eps:+d}"
            if key not in DATA["blocks"]:
                continue
            mats = reduced_operators(key)
            product = sp.eye(mats[0].rows)
            for grade in word:
                product = product * mats[grade - 1]
            total += dim * sp.trace(product)
    return sp.factor(total)


def expected_trace_word(word):
    d = 32
    if len(word) == 1:
        return 0
    if len(word) == 2:
        a, b = word
        return 2 * comb(11, a) * d**3 if a == b else 0
    if len(word) == 3:
        a, b, c = word
        if not (a == b == c):
            return 0
        if a == 5:
            # In odd Clifford dimension the grade-11 volume element is central
            # and scalar in the spin representation.  Three 5-subsets can
            # have symmetric difference all 11 indices: choose the two
            # indices in all three sets, then partition the other nine into
            # three private triples.
            triples = comb(11, 2) * comb(9, 3) * comb(6, 3)
            return 2 * triples * d**3
        if a % 2:
            return 0
        # For fixed A (|A|=a), choose A∩B of size a/2; C=A△B
        # is then the unique a-set closing the Clifford product to identity.
        triples = comb(11, a) * comb(a, a // 2) * comb(11 - a, a // 2)
        return 2 * triples * d**3
    raise ValueError(word)


def main():
    cases = []
    words = [(k,) for k in range(1, 6)]
    words += [(a, b) for a in range(1, 6) for b in range(1, 6)]
    words += [(k, k, k) for k in range(1, 6)]
    for word in words:
        got = actual_trace_word(word)
        want = expected_trace_word(word)
        cases.append({"word": word, "reported_blocks_trace": str(got),
                      "independent_pauli_trace": str(want), "pass": got == want})
        if got != want:
            raise AssertionError((word, got, want))
    result = {
        "status": "PASS",
        "scope": "trace invariants of the reported full ordinary-tensor Spin(11) star blocks",
        "full_dimension": FULL,
        "block_key_count": len(DATA["blocks"]),
        "checks": len(cases),
        "cases": cases,
        "derivation": {
            "Tr(H_k)=0": "Every tensor-Pauli word in H_k has a nonidentity factor.",
            "Tr(H_k H_l)": "Pauli orthogonality gives delta_kl * 2*C(11,k)*32^3.",
            "Tr(H_k^3)": "Only the two all-same-output triples contribute. For even k=2,4, A△B△C=empty gives C(11,k)C(k,k/2)C(11-k,k/2) triples. Grade 5 also contributes because the 11-index Clifford volume is scalar: choose the two triple-common indices, then partition the other nine as three private triples. Grades 1 and 3 contribute zero."
        },
        "limits": "This checks global trace moments and is not by itself a full reconstruction or PSD verification of every star block."
    }
    (Path(__file__).with_name("independent_trace_invariants.json")).write_text(json.dumps(result, indent=2) + "\n")
    print(f"PASS: {len(cases)} exact full-space trace moments; 11 reported blocks; dimension {FULL}.")


if __name__ == "__main__":
    main()
