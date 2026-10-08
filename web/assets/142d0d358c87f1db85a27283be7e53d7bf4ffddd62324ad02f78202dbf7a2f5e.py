from fractions import Fraction as F
from itertools import permutations, product


def episode_law(pi, emission, transition):
    k = len(pi)
    law = {word: F(0) for word in product(range(k), repeat=4)}
    for start in range(k):
        for end in range(k):
            path_mass = pi[start] * transition[start][end]
            for word in product(range(k), repeat=4):
                mass = path_mass
                for symbol in word[:3]:
                    mass *= emission[symbol][start]
                mass *= emission[word[3]][end]
                law[word] += mass
    return law


def marginal_pre(law):
    out = {}
    for word, mass in law.items():
        pre = word[:3]
        out[pre] = out.get(pre, F(0)) + mass
    return out


def tv(p, q):
    return sum(abs(p[x] - q[x]) for x in p) / 2


def matmul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(len(b)))
                        for j in range(len(b[0]))) for i in range(len(a)))


def inverse2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return ((a[1][1] / det, -a[0][1] / det),
            (-a[1][0] / det, a[0][0] / det))


def main():
    pi = (F(1, 2), F(1, 2))
    emission = (
        (F(3, 4), F(1, 4)),
        (F(1, 4), F(3, 4)),
    )
    p0 = (
        (F(3, 4), F(1, 4)),
        (F(1, 4), F(3, 4)),
    )
    p1 = (
        (F(5, 8), F(3, 8)),
        (F(3, 8), F(5, 8)),
    )
    f0 = episode_law(pi, emission, p0)
    f1 = episode_law(pi, emission, p1)
    assert marginal_pre(f0) == marginal_pre(f1)

    # The observable transition pair obeys J = E diag(pi) P E^T, and
    # unknown-label inversion recovers P exactly in the common permutation.
    d_pi = ((pi[0], F(0)), (F(0), pi[1]))
    e_t = tuple(zip(*emission))
    j0 = matmul(matmul(matmul(emission, d_pi), p0), e_t)
    recovered_p0 = matmul(matmul(matmul(((1 / pi[0], F(0)), (F(0), 1 / pi[1])),
                                        inverse2(emission)), j0),
                           tuple(zip(*inverse2(emission))))
    assert recovered_p0 == p0
    distance = tv(f0, f1)
    assert distance == F(11, 256)

    midpoint = {w: (f0[w] + f1[w]) / 2 for w in f0}
    # Same pre marginal means the midpoint conditional law changes only V.
    pre = marginal_pre(f0)
    replace0 = F(0)
    replace1 = F(0)
    for w, mass in f0.items():
        if pre[w[:3]]:
            replace0 += abs(f0[w] - midpoint[w]) / 2
            replace1 += abs(f1[w] - midpoint[w]) / 2
    # Summing over full records gives TV(F_b, midpoint)=TV(F0,F1)/2.
    assert replace0 == F(11, 512)
    assert replace1 == F(11, 512)
    assert tv(f0, midpoint) == tv(f1, midpoint) == F(11, 512)

    # Both transition matrices are fixed by state swap, so this is the
    # permutation-orbit Frobenius distance.
    orbit_sq = []
    for perm in permutations(range(2)):
        orbit_sq.append(sum((p0[i][j] - p1[perm[i]][perm[j]]) ** 2
                            for i in range(2) for j in range(2)))
    assert min(orbit_sq) == F(1, 16)
    frobenius = F(1, 4)
    assert frobenius * frobenius == min(orbit_sq)

    print({
        "pre_marginals_equal": True,
        "episode_TV": str(distance),
        "midpoint_post_replacement_each_world": "11/512",
        "transition_orbit_Frobenius": str(frobenius),
        "unavoidable_error_radius": "1/8",
    })


if __name__ == "__main__":
    main()
