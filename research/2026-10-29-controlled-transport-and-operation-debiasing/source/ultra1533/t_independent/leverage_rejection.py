"""Exact positive product proposal using the harmonic leverage-score chord."""
from flint import fmpq, fmpq_mat, arb, ctx
from quantized_field import DyadicUniform, quantized_gaussian


def real_coin(probability, bits):
    uniform, depth = DyadicUniform(bits), 32
    while True:
        ctx.prec = 4 * depth + 128
        p, U = probability(), uniform.at(depth)
        if U < p:
            return True
        if U > p:
            return False
        depth *= 2


class LeverageRejection:
    def __init__(self, frame):
        self.frame = frame
        self.leverage = [(b.transpose() * frame.base_inverse * b)[0, 0] for b in frame.columns]
        assert sum(self.leverage, fmpq(0)) == frame.size
        self.base_det = frame.base.det()
        self.proposals = self.determinants = self.inverses = self.coins = 0

    def sample(self, bits, width=fmpq(1, 4)):
        f = self.frame
        while True:
            self.proposals += 1
            state = []
            for tau in self.leverage:
                def ptilde(tau=tau):
                    factor = (arb(f.q).log() * arb(fmpq(f.components, 2) * tau)).exp()
                    return arb(f.prior) / (arb(f.prior) + (1 - arb(f.prior)) * factor)
                state.append(int(real_coin(ptilde, bits)))
                self.coins += 1
            L = fmpq_mat(f.base)
            for (u, v), value in zip(f.edges, state):
                if value:
                    if u:
                        L[u - 1, u - 1] += f.rho
                    if v:
                        L[v - 1, v - 1] += f.rho
                    if u and v:
                        L[u - 1, v - 1] -= f.rho
                        L[v - 1, u - 1] -= f.rho
            ratio = L.det() / self.base_det
            self.determinants += 1
            tilt = sum((tau * x for tau, x in zip(self.leverage, state)), fmpq(0))
            def acceptance():
                return (arb(fmpq(f.components, 2)) * (arb(f.q).log() * arb(tilt) - arb(ratio).log())).exp()
            accepted = real_coin(acceptance, bits)
            self.coins += 1
            if accepted:
                covariance = L.inv()
                self.inverses += 1
                bins, stats = quantized_gaussian(covariance, f.components, width, bits)
                return state, bins, stats
