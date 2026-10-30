"""Exact finite-state compiler for the packed squared-residual guard.

This is not a PRF implementation or learner. All matrices are rational.
The readout represents ell = log(2)*row2 + log(15)*row15.
"""
from dataclasses import dataclass
from fractions import Fraction as F


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mv(a, x):
    return [sum((v * w for v, w in zip(row, x)), F()) for row in a]


def mm(a, b):
    n = len(a)
    return [[sum((a[i][k] * b[k][j] for k in range(n)), F())
             for j in range(n)] for i in range(n)]


def row_times(a, m):
    return [sum((a[i] * m[i][j] for i in range(len(a))), F())
            for j in range(len(a))]


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F())


@dataclass(frozen=True)
class Instruction:
    index: int
    zero: tuple
    one: tuple


class PackedGuard:
    def __init__(self, n, packing, instructions, accept=1):
        if n < 1 or packing < 1 or not instructions:
            raise ValueError("positive sizes and a nonempty program required")
        self.n, self.p = n, packing
        self.s = (n + packing - 1) // packing
        self.N = packing * self.s
        self.instructions = tuple(instructions)
        for ins in self.instructions:
            if not 0 <= ins.index < n:
                raise ValueError("instruction index out of payload range")
            if sorted(ins.zero) != list(range(5)) or sorted(ins.one) != list(range(5)):
                raise ValueError("instructions must be permutations of five states")
        if not 0 <= accept < 5:
            raise ValueError("invalid accepting coordinate")
        self.accept = accept
        self.K, self.C = n*n+1, 20*(n*n+1)
        self.delta = F(1, 2**(self.s+1))
        self.L = len(self.instructions)
        self.m = self.L*self.s
        self.active = self.N+self.m+1
        self.T = max(32, self.active,
                     16*(self.C+self.K+1)*(self.L+1)*2**(2*self.s))
        self.dim = 2*self.p+9
        self.alpha = self.dim*self.T+1
        self.r = list(range(1, self.p+1))
        self.z = list(range(self.p+1, 2*self.p+1))
        self.u, self.v, self.g = 2*self.p+1, 2*self.p+2, 2*self.p+3
        self.q = list(range(2*self.p+4, 2*self.p+9))
        self.initial = [F(0)]*self.dim
        self.initial[0] = 1
        for i in range(self.p):
            self.initial[self.r[i]] = self.delta
            self.initial[self.z[i]] = self.delta*self.delta
        self.initial[self.q[0]] = 1
        self.maps = [[self._make_map(t, b) for b in (0, 1)]
                     for t in range(self.active)]

    def _scratch_reset(self, block):
        a = eye(self.dim)
        a[self.u] = [F(0)]*self.dim
        a[self.v] = [F(0)]*self.dim
        a[self.u][self.r[block]] = 1
        a[self.v][self.z[block]] = 1
        return a

    def _make_map(self, t, b):
        a = eye(self.dim)
        if t < self.N:
            i, j0 = divmod(t, self.s)
            w = F(1, 2**(j0+1))
            a[self.r[i]][0] += b*w
            a[self.z[i]][self.r[i]] += 2*b*w
            a[self.z[i]][0] += b*w*w
            if t == self.N-1:
                block = self.instructions[0].index // self.s
                a = mm(self._scratch_reset(block), a)
        elif t < self.N+self.m:
            insno, j0 = divmod(t-self.N, self.s)
            w = F(1, 2**(j0+1))
            a[self.u][0] -= b*w
            a[self.v][self.u] -= 2*b*w
            a[self.v][0] += b*w*w
            ins = self.instructions[insno]
            if j0 == ins.index % self.s:
                perm = ins.one if b else ins.zero
                qmap = eye(self.dim)
                for qi in self.q:
                    qmap[qi] = [F(0)]*self.dim
                for old in range(5):
                    qmap[self.q[perm[old]]][self.q[old]] = 1
                a = mm(qmap, a)
            if j0 == self.s-1:
                guard = eye(self.dim)
                scale = 2**(2*self.s)
                guard[self.g][self.v] += scale
                guard[self.g][self.u] -= 2*scale*self.delta
                guard[self.g][0] += scale*self.delta*self.delta
                a = mm(guard, a)
                if insno+1 < self.L:
                    block = self.instructions[insno+1].index // self.s
                    a = mm(self._scratch_reset(block), a)
        return a

    def state(self, prefix):
        if len(prefix) >= self.T:
            raise ValueError("next-token query must be before horizon")
        x = list(self.initial)
        for t, b in enumerate(prefix[:self.active]):
            if b not in (0, 1):
                raise ValueError("binary prefix required")
            x = mv(self.maps[t][b], x)
        return x

    def readout(self, t):
        a, b = [F(0)]*self.dim, [F(0)]*self.dim
        if self.N <= t < self.N+self.m:
            j = (t-self.N) % self.s + 1
            scale = self.K*2**(self.s+1)
            a[self.u] = scale
            a[0] = -scale*F(1, 2**j)
        elif t == self.N+self.m:
            a[self.g] = -F(self.C, 2)
            b[self.q[self.accept]] = 1
            b[0] = -F(1, 2)
        return a, b

    def probability_from_state(self, t, x):
        a, b = self.readout(t)
        e2, e15 = 2*dot(a, x), 2*dot(b, x)
        if e2.denominator != 1 or e15.denominator != 1:
            raise ArithmeticError("integer odds exponents lost")
        odds = F(2)**int(e2) * F(15)**int(e15)
        return odds/(1+odds)

    def probability(self, prefix):
        return self.probability_from_state(len(prefix), self.state(prefix))

    def program_bit(self, payload):
        q = 0
        for ins in self.instructions:
            perm = ins.one if payload[ins.index] else ins.zero
            q = perm[q]
        return int(q == self.accept)

    def correct_scan(self, payload):
        out = []
        for ins in self.instructions:
            block = ins.index // self.s
            out.extend(payload[block*self.s:(block+1)*self.s])
        return tuple(out)

    def direct_guard(self, prefix):
        if len(prefix) < self.N:
            return 0
        payload = prefix[:self.N]
        g = 0
        complete = min(self.L, (len(prefix)-self.N)//self.s)
        for a in range(complete):
            block = self.instructions[a].index // self.s
            left, right = 0, 0
            for j in range(self.s):
                left = 2*left+payload[block*self.s+j]
                right = 2*right+prefix[self.N+a*self.s+j]
            g += (left-right)**2
        return g

    def simulated_probability(self, prefix, boolean_oracle):
        """Delegate only the public schedule, never permutations/state."""
        if len(prefix) >= self.T:
            raise ValueError("next-token query must be before horizon")
        return public_simulator_probability(prefix, self.n, self.p,
                    tuple(ins.index for ins in self.instructions), boolean_oracle)

    def native_coin(self, prefix, getrandbits, counts):
        """Exact under iid bits, without allocating giant denominators."""
        t = len(prefix)
        if t >= self.T:
            raise ValueError("next-token query must be before horizon")
        if t < self.N or t > self.N+self.m:
            counts["fair_bits"] = counts.get("fair_bits", 0)+1
            return getrandbits(1)
        x = self.state(prefix)
        if t < self.N+self.m:
            a, _ = self.readout(t)
            exponent = int(2*dot(a, x))
            minority = race_small_weight(abs(exponent), 0, getrandbits, counts)
            return 1-minority if exponent > 0 else minority
        guard = int(x[self.g])
        accept = int(x[self.q[self.accept]])
        if guard == 0:
            counts["fair_bits"] = counts.get("fair_bits", 0)+4
            return int(getrandbits(4) < (15 if accept else 1))
        return race_small_weight(self.C*guard, 1 if accept else -1,
                                 getrandbits, counts)


def public_simulator_probability(prefix, n, packing, read_indices, boolean_oracle):
    """Key-free majority-copy/guarded-label simulator, public data only."""
    s = (n+packing-1)//packing
    N, m = packing*s, len(read_indices)*s
    t = len(prefix)
    if t < N or t > N+m:
        return F(1, 2), 0
    payload = prefix[:N]
    if t < N+m:
        scan, j0 = divmod(t-N, s)
        block = read_indices[scan]//s
        original = sum(payload[block*s+j]*2**(s-j) for j in range(s))+1
        previous = sum(prefix[N+scan*s+j]*2**(s-j) for j in range(j0))
        S = original-previous-2**(s-j0)
        if S % 2 != 1:
            raise ArithmeticError("midpoint oddness lost")
        return F(int(S > 0)), 0
    guard = 0
    for scan, index in enumerate(read_indices):
        block = index//s
        left = sum(payload[block*s+j]*2**(s-1-j) for j in range(s))
        right = sum(prefix[N+scan*s+j]*2**(s-1-j) for j in range(s))
        guard += (left-right)**2
    if guard:
        return F(0), 0
    bit = boolean_oracle(prefix[:n])
    return (F(15, 16) if bit else F(1, 16)), 1


def _bit(getrandbits, counts):
    counts["fair_bits"] = counts.get("fair_bits", 0)+1
    return getrandbits(1)


def power_two_coin(exponent, getrandbits, counts):
    """Probability2^-exponent; expected <2 bits, arbitrary integer counter."""
    if exponent < 0:
        raise ValueError("nonnegative exponent required")
    counts["max_power_exponent"] = max(exponent,
                                      counts.get("max_power_exponent", 0))
    for _ in range(exponent):
        if _bit(getrandbits, counts):
            return 0
    return 1


def race_small_weight(exponent, factor15, getrandbits, counts):
    """Probability a/(1+a), a=15^factor15*2^-exponent.

    factor15 is0,+1,-1. Label callers have exponent>=40, so a<=1.
    Each iteration's B weight is1; no signed or estimated weights occur.
    """
    if factor15 not in (-1, 0, 1) or exponent < (4 if factor15 == 1 else 0):
        raise ValueError("unsupported positive race weight")
    while True:
        counts["race_rounds"] = counts.get("race_rounds", 0)+1
        if _bit(getrandbits, counts):  # B wins immediately.
            return 0
        power = exponent-(4 if factor15 == 1 else 0)
        if not power_two_coin(power, getrandbits, counts):
            continue
        if factor15 == 0:
            return 1
        if factor15 == 1:
            counts["fair_bits"] = counts.get("fair_bits", 0)+4
            if getrandbits(4) < 15:
                return 1
            continue
        # A's remaining independent1/15 coin; uniform0..14 via rejection.
        while True:
            counts["fair_bits"] = counts.get("fair_bits", 0)+4
            r = getrandbits(4)
            if r < 15:
                break
        if r == 0:
            return 1


def exact_rational_coin(probability, getrandbits, counts):
    """Exact under iid fair bits; seeded RNG runs are diagnostics only."""
    num, den = probability.numerator, probability.denominator
    width = (den-1).bit_length()
    while True:
        counts["fair_bits"] = counts.get("fair_bits", 0)+width
        counts["integer_attempts"] = counts.get("integer_attempts", 0)+1
        x = getrandbits(width)
        if x < den:
            return int(x < num)
