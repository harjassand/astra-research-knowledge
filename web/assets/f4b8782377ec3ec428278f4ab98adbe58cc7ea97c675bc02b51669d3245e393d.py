"""Finite convention checks for quantitative_cocycle.md; not a theorem prover."""
from collections import defaultdict, deque
from fractions import Fraction
from pathlib import Path
import json
import math
import mpmath as mp

OUT = Path(__file__).resolve().parent


def reduce_word(word):
    stack = []
    for letter in word:
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
    return tuple(stack)


def inverse(word):
    return tuple(-x for x in reversed(word))


def multiply(a, b):
    out = defaultdict(int)
    for x, c in a.items():
        for y, d in b.items():
            out[reduce_word(x + y)] += c * d
    return {x: c for x, c in out.items() if c}


def root_moments(m, count):
    """Number of walks of length 2r at the root of the (m+1)-tree."""
    state = {0: 1}
    answer = [1]
    for step in range(1, 2 * count + 1):
        nxt = defaultdict(int)
        for depth, value in state.items():
            nxt[depth + 1] += value * (m + 1 if depth == 0 else m)
            if depth:
                nxt[depth - 1] += value
        state = dict(nxt)
        if step % 2 == 0:
            answer.append(state.get(0, 0))
    return answer


def schreier_basis(k):
    n = 1 << k
    mask = n - 1

    def rotate(v):
        return ((v << 1) & mask) | (v >> (k - 1))

    perm = [{v: rotate(v) for v in range(n)},
            {v: rotate(v) ^ 1 for v in range(n)}]
    invperm = [{w: v for v, w in p.items()} for p in perm]
    assert all(len(p) == n for p in invperm)
    words = {0: ()}
    tree_edges = set()
    queue = deque([0])
    while queue:
        v = queue.popleft()
        for colour in range(2):
            letter = colour + 2  # a=1, y=2, z=3
            for sign, p in [(1, perm[colour]), (-1, invperm[colour])]:
                w = p[v]
                if w not in words:
                    words[w] = words[v] + (sign * letter,)
                    tree_edges.add((v if sign == 1 else w, colour))
                    queue.append(w)
    basis = []
    for v in range(n):
        for colour in range(2):
            if (v, colour) not in tree_edges:
                w = perm[colour][v]
                word = reduce_word(words[v] + (colour + 2,) + inverse(words[w]))
                assert word
                # Replay the word as an actual loop in the covering graph.
                current = 0
                for letter in word:
                    colour2 = abs(letter) - 2
                    current = (perm if letter > 0 else invperm)[colour2][current]
                assert current == 0
                basis.append(word)
    assert len(words) == n
    assert len(tree_edges) == n - 1
    assert len(basis) == n + 1
    assert max(map(len, words.values())) <= k
    assert max(map(len, basis)) <= 2 * k + 1
    prefixes = []
    p = ()
    for bword in basis[:n]:
        p = reduce_word(p + (1,) + bword)
        prefixes.append(p)
    w = reduce_word(p + (1,))
    # Every a occurrence is positive and its preceding prefix is exactly p_j.
    seen = [()]
    running = ()
    for letter in w:
        if letter == 1 and running:
            seen.append(running)
        assert letter != -1
        running = reduce_word(running + (letter,))
    assert seen == [()] + prefixes
    assert len(w) <= 2 * n * (k + 1) + 1
    return {
        "k": k, "vertices": n, "basis_count": len(basis),
        "max_basis_word_length": max(map(len, basis)),
        "w_length": len(w), "w_length_bound": 2 * n * (k + 1) + 1,
        "positive_a_count": n + 1,
    }


def theta_density(m, theta):
    if m == 1:
        return mp.mpf(2) / mp.pi
    return (4 * m * (m + 1) * mp.cos(theta)**2 /
            (mp.pi * ((m + 1)**2 - 4*m*mp.sin(theta)**2)))


def integrate_density(m, fn, delta=None):
    cuts = [mp.mpf(0)]
    if delta is not None:
        cuts.extend([mp.sqrt(delta) / 10, mp.sqrt(delta), 10 * mp.sqrt(delta)])
    cuts.extend([mp.pi / 8, mp.pi / 4, mp.pi / 2])
    cuts = sorted(set(x for x in cuts if 0 <= x <= mp.pi / 2))
    return mp.quad(lambda t: fn(4 * mp.sin(t)**2) * theta_density(m, t), cuts)


def main():
    mp.mp.dps = 65
    exact = []
    for m in [1, 2, 3, 4]:
        t = {(): 1, **{(j,): 1 for j in range(1, m + 1)}}
        ts = {inverse(w): c for w, c in t.items()}
        q = multiply(t, ts)
        moments = root_moments(m, 4)
        qp = {(): 1}
        for r in range(5):
            assert qp.get((), 0) == moments[r]
            exact.append({"m": m, "r": r, "group_ring_moment": moments[r]})
            if r < 4:
                qp = multiply(qp, q)
    spectral = []
    for m in [1, 2, 3, 4, 16, 256]:
        moments = root_moments(m, 6)
        for r in range(7):
            val = integrate_density(m, lambda x, r=r: x**r)
            expected = mp.mpf(moments[r]) / m**r
            error = abs(val - expected)
            assert error < mp.mpf("1e-55")
            spectral.append({"m": m, "r": r, "abs_error": str(error)})
    ridge = []
    resource = []
    for eta_frac in [Fraction(1), Fraction(1, 2), Fraction(1, 4), Fraction(1, 8)]:
        eta = mp.mpf(eta_frac.numerator) / eta_frac.denominator
        need = Fraction(2048, 1) / eta_frac**4
        m = 1
        while m < need:
            m <<= 1
        delta = eta**4 / 4096
        size2 = integrate_density(m, lambda x: x / (x+delta)**2, delta) / m
        error2 = integrate_density(m, lambda x: delta**2 / (x+delta)**2, delta)
        assert size2 <= 3 * eta**2 / 64
        assert error2 <= 3 * eta**2 / 128
        # The real-log value is only a resource upper estimate, not the exact test.
        L = int(mp.ceil(5 / delta * mp.log(4 / eta)))
        k = m.bit_length() - 1
        w_bound = 2 * m * (k+1) + 1
        support_log10 = math.log10(m+1) + L * math.log10((m+1)**2+1)
        ridge.append({"eta": str(eta_frac), "m": m,
                      "ridge_norm": str(mp.sqrt(size2)),
                      "ridge_residual_norm": str(mp.sqrt(error2)),
                      "norm_bound_eta_over_4": str(eta / 4)})
        resource.append({"eta": str(eta_frac), "m": m, "k": k,
                         "L_safe_upper": L, "w_length_upper": w_bound,
                         "expanded_support_log10_upper": support_log10})
    # Negative control: the same sum with cyclic powers is not a free-prefix sum.
    m = 4
    cyclic_second = (m+1)**2 + 2 * sum(j*j for j in range(1, m+1))
    tree_second = root_moments(m, 2)[2]
    assert cyclic_second == 85 and tree_second == 45
    result = {
        "scope": "Finite exact group-ring and covering checks; numerical integrals corroborate formulas only.",
        "exact_moment_checks": exact,
        "spectral_integral_checks": spectral,
        "ridge_integrals": ridge,
        "covering_checks": [schreier_basis(k) for k in range(1, 9)],
        "resources_not_emitted": resource,
        "negative_control": {"m": m, "cyclic_second_moment": cyclic_second,
                             "free_second_moment": tree_second},
    }
    (OUT / "cocycle_checks.json").write_text(json.dumps(result, indent=2))
    print(json.dumps({"exact_checks": len(exact), "spectral_checks": len(spectral),
                      "covering_checks": 8, "ridge_checks": len(ridge),
                      "negative_control": result["negative_control"],
                      "output": str(OUT / "cocycle_checks.json")}, indent=2))


if __name__ == "__main__":
    main()
