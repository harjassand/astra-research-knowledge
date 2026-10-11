"""Independent exact finite diagnostics for structural's nonperiodic example.

These checks supplement the universal written proof; they do not prove it.
Only Python standard-library integer/rational arithmetic is used.
"""

from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path


states = ["s", "x0", "x1", "z0", "z1"]
states += [f"c{i}" for i in range(3)]
states += [f"m{i}{b}" for i in range(3) for b in range(2)]
index = {j: k for k, j in enumerate(states)}
accept = {"z0", "c0"}


def step(j, b):
    if j == "s":
        return f"x{b}"
    if j == "x0":
        return "z0" if b == 0 else "c0"
    if j == "x1":
        return "c0"
    if j == "z0":
        return "z1"
    if j == "z1":
        return "z0"
    if j.startswith("c"):
        return f"m{j[1]}{b}"
    i, previous = int(j[1]), int(j[2])
    return f"c{i}" if previous == b == 0 else f"c{(i + 1) % 3}"


assert len(states) == 14
assert all(step(j, b) in index for j in states for b in range(2))
law = {"s": F(1)}
acceptance = []
for r in range(403):
    acceptance.append(sum(law.get(j, F(0)) for j in accept))
    new = {}
    for j, mass in law.items():
        for b in range(2):
            k = step(j, b)
            new[k] = new.get(k, F(0)) + mass / 2
    law = new

# a_t = Re(lambda**t), without floating-point complex arithmetic.
a_previous, a_current = F(1), -F(1, 8)
real_parts = [a_previous, a_current]
for t in range(2, 201):
    a_previous, a_current = a_current, -a_current / 4 - 7 * a_previous / 16
    real_parts.append(a_current)
for t, a in enumerate(real_parts):
    assert acceptance[2 + 2 * t] == (1 + a) / 2
assert acceptance[0] == 0
assert all(acceptance[r] == 0 for r in range(1, 403, 2))


def raw_word(branches, final):
    j, word = "s", []
    for b in branches:
        word.append(str(b))
        word.extend(str(b ^ int(j == k)) for k in states)
        j = step(j, b)
    if final and j not in accept:
        return None
    word.append(str(final))
    return "".join(word)


def raw_accepts(word):
    if len(word) % 15 != 1:
        return False
    j, k = "s", 0
    while k + 1 < len(word):
        b = int(word[k])
        checks = word[k + 1 : k + 15]
        if checks != "".join(str(b ^ int(j == state)) for state in states):
            return False
        j = step(j, b)
        k += 15
    return word[-1] == "0" or j in accept


def encode(word, left, right):
    return left + "".join("01" if b == "0" else "10" for b in word) + right


def wrapped_accepts(word):
    if len(word) < 10 or word[:4] not in ("0001", "1110"):
        return False
    if word[-4:] not in ("1000", "0111"):
        return False
    body = word[4:-4]
    if len(body) % 2:
        return False
    pairs = [body[i : i + 2] for i in range(0, len(body), 2)]
    if any(pair not in ("01", "10") for pair in pairs):
        return False
    return raw_accepts("".join(pair[0] for pair in pairs))


wrapped = []
raw_count = 0
for r in range(7):
    branches = list(product(range(2), repeat=r))
    for choice in branches:
        for final in range(2):
            raw = raw_word(choice, final)
            if raw is None:
                continue
            raw_count += 1
            assert raw_accepts(raw)
            for left, right in product(("0001", "1110"), ("1000", "0111")):
                word = encode(raw, left, right)
                assert wrapped_accepts(word)
                triples = [i for i in range(len(word) - 2)
                           if word[i : i + 3] in ("000", "111")]
                assert triples == [0, len(word) - 3]
                wrapped.append(word)

assert len(wrapped) == len(set(wrapped))
factor_tests = 0
for u in wrapped:
    for v in wrapped:
        if len(u) < len(v):
            assert u not in v
            factor_tests += 1

contexts = [""] + ["".join(bits) for n in range(1, 4)
                     for bits in product("01", repeat=n)]
context_tests = 0
for u in wrapped:
    for x, y in product(contexts, repeat=2):
        assert wrapped_accepts(x + u + y) == (not x and not y)
        context_tests += 1

# An exact small feasible horizon witness: r=2; choose the two blocks and
# final bit independently fairly, and both wrapper markers independently.
# All states after two blocks lie in F, so every final bit is allowed.
witness = [raw_word(branches, final)
           for branches in product(range(2), repeat=2) for final in range(2)]
assert all(word is not None for word in witness)
assert len({len(word) for word in witness}) == 1
assert all(sum(int(word[k]) for word in witness) * 2 == len(witness)
           for k in range(len(witness[0])))
wrapped_witness = [encode(word, left, right)
                   for word in witness
                   for left, right in product(("0001", "1110"), ("1000", "0111"))]
assert all(len(word) == 70 for word in wrapped_witness)
assert all(sum(int(word[k]) for word in wrapped_witness) * 2 == len(wrapped_witness)
           for k in range(70))

receipt = {
    "status": "PASS",
    "exact_acceptance_microsteps": len(acceptance),
    "exact_macro_eigenvalue_identities": len(real_parts),
    "accepted_raw_words_checked": raw_count,
    "wrapped_words_checked": len(wrapped),
    "proper_factor_tests": factor_tests,
    "context_tests": context_tests,
    "horizon_70_fair_witness_words": len(wrapped_witness),
    "scope": "Finite exact diagnostics, not universal proof or priority evidence.",
}
here = Path(__file__).resolve()
receipt["script_sha256"] = hashlib.sha256(here.read_bytes()).hexdigest()
output = here.with_name("nonperiodic_diagnostics.json")
output.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
