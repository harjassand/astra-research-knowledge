from fractions import Fraction


R = Fraction(6, 5)
EPS = Fraction(1, 100)
D = 2
K = 2

# Species order: A1, A2, B1, B2. Each tuple is (source, target, rate).
zero = (0, 0, 0, 0)
reactions = [
    (zero, (1, 0, 0, 0), Fraction(1)),
    ((1, 0, 0, 0), zero, Fraction(1)),
    (zero, (0, 1, 0, 0), Fraction(1)),
    ((0, 1, 0, 0), zero, Fraction(1)),
    # Paired edge A1 <-> A1+B1, with p=1 and q=2.
    ((1, 0, 0, 0), (1, 0, 1, 0), Fraction(1)),
    ((1, 0, 1, 0), (1, 0, 0, 0), Fraction(2)),
    # Paired edge A2 <-> A2+B2, all rates one.
    ((0, 1, 0, 0), (0, 1, 0, 1), Fraction(1)),
    ((0, 1, 0, 1), (0, 1, 0, 0), Fraction(1)),
    # k=1 autocatalytic pairs on each base edge.
    ((1, 0, 1, 0), (2, 0, 1, 0), Fraction(1)),
    ((2, 0, 1, 0), (1, 0, 1, 0), Fraction(1)),
    ((0, 1, 0, 1), (0, 2, 0, 1), Fraction(1)),
    ((0, 2, 0, 1), (0, 1, 0, 1), Fraction(1)),
    # Added substrate-preserving deactivation pair A2+B1 <-> B1.
    ((0, 1, 1, 0), (0, 0, 1, 0), Fraction(1)),
    ((0, 0, 1, 0), (0, 1, 1, 0), Fraction(1)),
]


def falling(n, k):
    if n < k:
        return 0
    out = 1
    for j in range(k):
        out *= n - j
    return out


def propensity(x, source, rate):
    out = rate
    for n, k in zip(x, source):
        out *= falling(n, k)
    return out


def potential(x):
    a1, a2, b1, b2 = x
    total_a = a1 + a2
    total_b = b1 + b2
    h1 = int(total_a == 0)  # both catalysts can switch B1 support
    h2 = int(a2 == 0)       # A2 is the only B2 support
    correction = EPS / (1 + total_b) ** D
    return (
        Fraction(total_a + K * int(total_a == 0))
        + R**b1 * (1 + correction * h1)
        + R**b2 * (1 + correction * h2)
    )


def generator(x):
    base = potential(x)
    total = Fraction(0)
    for source, target, rate in reactions:
        jump_rate = propensity(x, source, rate)
        if not jump_rate:
            continue
        y = tuple(n - s + t for n, s, t in zip(x, source, target))
        total += jump_rate * (potential(y) - base)
    return total


def closed_form(n):
    # x=(N,0,1,n), N=n^(D+2). The first term is A1 immigration,
    # death, and its k=1 autocat pair; the next is A2 immigration plus
    # the added reverse activation B1 -> A2+B1.
    N = n ** (D + 2)
    a1_catalyst_drift = 1 - N * (N - 1)
    activation_drift = 2 * (1 - EPS * R**n / (n + 2) ** D)
    b1_pair_drift = N * (
        R * (R - 1)
        + EPS * R**n * (Fraction(1, (n + 3) ** D) - Fraction(1, (n + 2) ** D))
        + 2 * (1 - R)
        + 2 * EPS * R**n * (Fraction(1, (n + 1) ** D) - Fraction(1, (n + 2) ** D))
    )
    return a1_catalyst_drift + activation_drift + b1_pair_drift


def main():
    for n in (100, 250, 400, 600):
        N = n ** (D + 2)
        x = (N, 0, 1, n)
        direct = generator(x)
        formula = closed_form(n)
        assert direct == formula, (n, direct - formula)
        print(f"n={n}, N=n^(D+2)={N}, exact_LV_positive={direct > 0}")
        if n == 600:
            assert direct > 0
    print("PASS: exact generator equals closed form and LV>0 on the stated ray")
    print("Scope: this falsifies the global-denominator potential only; not recurrence")


if __name__ == "__main__":
    main()
