"""Adopted exact-factory architecture; floating numerical demonstration only.

Known-probability random draws and logs use ordinary floating arithmetic here.
PROOF states the exact random-bit construction and separates that theorem from
this simulation. iid binomial aggregates are charged as represented experiments.
"""
import itertools
import json
import math
from pathlib import Path
import numpy as np


class Source:
    def __init__(self, parameters, seed=1309):
        self.__p = np.asarray(parameters, dtype=float)
        self.rng = np.random.default_rng(seed)
        self.physical_flips = 0
        self.batch_calls = 0

    def flip(self, label):
        self.physical_flips += 1
        return bool(self.rng.random() < self.__p[label])

    def estimate_all(self, n):
        self.physical_flips += n*len(self.__p)
        self.batch_calls += 1
        return self.rng.binomial(n, self.__p)/n


def huber_linear(coin, scale, gap, rng):
    """Scalar Cp factory, Huber 2016 Section 2, using floating auxiliaries.

    Contract: scale>1 and scale*mean(coin)<=1-gap. No source mean is received.
    The changing target (scale*p)^i is a bounded martingale until absorption.
    """
    if scale <= 1:
        return bool(rng.random() < scale and coin())
    epsilon = min(gap, .644)
    cutoff = 4.6/epsilon
    remaining = 1
    while remaining:
        while 0 < remaining < cutoff:
            success = coin()
            remaining -= 1
            if not success:
                remaining += int(rng.geometric((scale-1)/scale))
        if remaining == 0:
            return True
        if math.log(rng.random()) >= -remaining*math.log1p(epsilon/2):
            return False
        scale *= 1+epsilon/2
        epsilon /= 2
        cutoff *= 2
    return True


class ChainQuery:
    """Binary factor chain. First factor is unary; all others pairwise.

    Parameters are 2 first-site entries and 4 entries for each later edge.
    Pins are deterministic query constraints. DP is explicitly constructed.
    """
    def __init__(self, n, pins):
        self.n, self.pins = n, dict(pins)
        self.m = n
        self.M = 2+4*(n-1)

    def factors(self, x):
        return [x[0]] + [2+4*(i-1)+2*x[i-1]+x[i] for i in range(1,self.n)]

    def allowed(self, i, s):
        return i not in self.pins or self.pins[i] == s

    def compile(self, weights):
        backward = np.ones((self.n,2))
        for s in range(2):
            backward[-1,s] = float(self.allowed(self.n-1,s))
        for i in range(self.n-2,-1,-1):
            for s in range(2):
                backward[i,s] = float(self.allowed(i,s))*sum(
                    weights[2+4*i+2*s+t]*backward[i+1,t] for t in range(2))
        initial = weights[:2]*backward[0]
        if sum(initial) == 0:
            raise ValueError('Infeasible deterministic query')

        def draw(rng):
            x = [int(rng.random() >= initial[0]/sum(initial))]
            for i in range(1,self.n):
                row = np.array([weights[2+4*(i-1)+2*x[-1]+t]*backward[i,t]
                                for t in range(2)])
                x.append(int(rng.random() >= row[0]/sum(row)))
            return tuple(x)
        return draw


class ShiftedService:
    def __init__(self, source, query, a, seed=716, stage_cap=64):
        self.source, self.query, self.a = source, query, a
        self.rng = np.random.default_rng(seed)
        self.C = (1-a)/a
        self.B = max(query.m*self.C,3.)
        self.lam = 2*self.B
        self.eps = 1/self.lam
        self.lam_prime = self.lam/(1-2*self.eps)
        eta_p = min(1.,a/(2*query.m*(1-a)))
        eta_z = min(1.,a/(8*query.m*(1-a)))
        self.n_pilot = math.ceil(math.log(20*query.M)/(2*eta_p**2))
        self.n_shift = math.ceil(math.log(4*query.M/self.eps)/(2*eta_z**2))
        self.stage_cap = stage_cap
        self.pilots = self.attempts = self.z_calls = self.v_calls = 0
        self.hat = None

    def new_pilot(self):
        self.hat = self.a+(1-self.a)*self.source.estimate_all(self.n_pilot)
        self.h = -np.log(self.hat)/self.C
        self.propose = self.query.compile(self.hat)
        self.pilots += 1

    def log_coin(self, label):
        k = int(self.rng.geometric(self.a))
        if self.rng.random() >= 1/k:
            return False
        for _ in range(k):
            if self.source.flip(label):
                return False
        return True

    def residual_coin(self, labels):
        self.v_calls += 1
        alpha = self.query.m*self.C/self.B
        if self.rng.random() >= alpha:
            return bool(self.rng.integers(2))
        label = labels[int(self.rng.integers(len(labels)))]
        if self.rng.integers(2):
            return not self.log_coin(label)
        return bool(self.rng.random() < self.h[label])

    def shift_coin(self):
        self.z_calls += 1
        q = self.a+(1-self.a)*self.source.estimate_all(self.n_shift)
        upper = self.query.m*max(0.,float(np.max(np.log(q/self.hat))))
        v = min(1.,max(0.,.5+upper/(2*self.B)))
        return bool(self.rng.random() < v)

    def acceptance(self, x):
        labels = self.query.factors(x)
        def mixture():
            if self.rng.integers(2):
                return self.residual_coin(labels)
            return not self.shift_coin()
        for _ in range(int(self.rng.poisson(self.lam_prime))):
            if not huber_linear(mixture,2*(1-2*self.eps),self.eps,self.rng):
                return False
        return True

    def draw(self):
        if self.hat is None:
            self.new_pilot()
        while True:
            for _ in range(self.stage_cap):
                self.attempts += 1
                x = self.propose(self.rng)
                if self.acceptance(x):
                    return x
            self.new_pilot()


def exact_reference(query, parameters, a):
    weights = a+(1-a)*parameters
    states, masses = [], []
    for x in itertools.product(range(2),repeat=query.n):
        if all(query.allowed(i,s) for i,s in enumerate(x)):
            states.append(x)
            masses.append(float(np.prod(weights[query.factors(x)])))
    masses = np.asarray(masses)
    return states,masses/sum(masses)


def run():
    a = .85
    query = ChainQuery(4,{0:0,3:1})
    parameters = np.array([.1,.9,.05,.35,.8,.7,.95,.15,.45,.65,.05,.85,.6,.1])
    source = Source(parameters)
    service = ShiftedService(source,query,a)
    states,masses = exact_reference(query,parameters,a)
    counts = {x:0 for x in states}
    samples = 240
    for _ in range(samples):
        counts[service.draw()] += 1
    empirical = np.array([counts[x]/samples for x in states])
    # Independent numerical checks of the elementary log and linear components.
    rng = np.random.default_rng(991)
    linear_n, target_bias = 20000, .72
    input_p, scale, gap = .4,1.8,.25
    linear_emp = sum(huber_linear(lambda: rng.random()<input_p,scale,gap,rng)
                     for _ in range(linear_n))/linear_n
    assert abs(linear_emp-target_bias)<.02
    result = {
        'method':'Dughmi-style shifted rejection, capped pilot refresh, actual factor-chain DP',
        'status':'floating demonstration; ideal theorem exact, software not interval/bit verified',
        'a':a,'variables':query.n,'factors':query.m,'local_parameters':query.M,
        'pins':query.pins,'samples':samples,
        'reference_probabilities':{str(s):float(p) for s,p in zip(states,masses)},
        'sample_counts':{str(s):counts[s] for s in states},
        'empirical_total_variation':float(.5*sum(abs(empirical-masses))),
        'represented_physical_coin_flips':source.physical_flips,
        'primitive_count_batch_calls':source.batch_calls,
        'pilot_count':service.pilots,'proposal_attempts':service.attempts,
        'shift_coin_calls':service.z_calls,'residual_coin_calls':service.v_calls,
        'shots_per_pilot_coordinate':service.n_pilot,
        'shots_per_shift_coordinate':service.n_shift,
        'huber_linear_test_samples':linear_n,
        'huber_linear_target':target_bias,'huber_linear_empirical':linear_emp,
        'note':'Counts are independent synthetic binomial aggregates; physical reset cost is not free.',
    }
    Path(__file__).with_name('shifted_rejection_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    run()
