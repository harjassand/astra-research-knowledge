"""Equally informed conventional comparators, with different accuracy scopes."""
import math
import time
import numpy as np
from flint import fmpq, fmpq_mat, arb, ctx
from scipy.special import expit
from exact_conductance import LazyUniform
from quantized_field import GaussianRealSample, DyadicUniform, exact_ldl, quantized_gaussian


def proved_burnin(frame, epsilon=fmpq(1, 100)):
    precision = 64
    while True:
        ctx.prec = precision
        value = (arb(fmpq(frame.m) / epsilon).log() * frame.m / arb(1 - frame.c)).ceil()
        if value.is_exact():
            return int(value.unique_fmpz())
        precision *= 2


def approximate_draw(frame, bits, counts, epsilon=fmpq(1, 100), width=fmpq(1, 4)):
    steps = proved_burnin(frame, epsilon)
    state, inverse = [0] * frame.m, fmpq_mat(frame.base_inverse)
    for _ in range(steps):
        e = bits.edge(frame.m)
        inverse = frame.update(inverse, state, e, LazyUniform(bits), counts)
    field, stats = quantized_gaussian(inverse, frame.components, width, bits)
    return state, field, {"burnin_updates": steps, "tv_bound_per_output": str(epsilon), "field": stats}


class GaussianRejection:
    """Exact same quantized target, ordinary low-stiffness Gaussian rejection.

    Factor the proposal once. All acceptance and bin decisions use outward balls.
    This method is supplied the same graph/prior/contrast as CFTP.
    """
    def __init__(self, frame):
        self.frame = frame
        self.factor = exact_ldl(frame.base_inverse)
        self.proposals, self.rounds, self.max_depth = 0, 0, 0

    def sample(self, bits, width=fmpq(1, 4)):
        frame = self.frame
        while True:
            self.proposals += 1
            proposal = GaussianRealSample(frame.base_inverse, frame.components, bits, self.factor)
            coin = DyadicUniform(bits)
            depth = 32
            while True:
                self.rounds += 1
                self.max_depth = max(self.max_depth, depth)
                field = proposal.evaluate(depth)
                if field is None:
                    depth *= 2
                    continue
                score = arb(1)
                for u, v in frame.edges:
                    squared = arb(0)
                    for component in field:
                        left = component[u - 1] if u else arb(0)
                        right = component[v - 1] if v else arb(0)
                        difference = left - right
                        squared += difference * difference
                    score *= 1 - arb(frame.prior) + arb(frame.prior) * (-arb(frame.rho) * squared / 2).exp()
                U = coin.at(depth)
                if U < score:
                    bins, stats = proposal.quantize(width, depth)
                    return bins, stats
                if U > score:
                    break
                depth *= 2


def alternating_gaussian(frame, draws, seed, sweeps=32, width=0.25):
    """Float diagnostic only: stationary kernel is correct, burn-in not certified."""
    rng = np.random.default_rng(seed)
    columns = np.column_stack([np.array([[float(b[i, 0])] for i in range(frame.size)]).ravel() for b in frame.columns])
    q, p, rho = float(frame.q), float(frame.prior), float(frame.rho)
    logodds = math.log(p / (1 - p))
    output = []
    choleskys = 0
    for _ in range(draws):
        state = np.zeros(frame.m)
        for _ in range(sweeps):
            precision = (columns * (1 + rho * state)) @ columns.T
            root = np.linalg.cholesky(precision)
            field = np.linalg.solve(root.T, rng.standard_normal((frame.size, frame.components)))
            gradients = columns.T @ field
            probability = expit(logodds - rho * np.sum(gradients * gradients, axis=1) / 2)
            state = (rng.random(frame.m) < probability).astype(float)
            choleskys += 1
        output.append(np.floor(field.T.ravel() / width).astype(int).tolist())
    return output, {"sweeps_per_draw": sweeps, "cholesky_factorizations": choleskys,
                    "accuracy": "UNKNOWN: finite floating burn-in; not the exact-output comparator"}
