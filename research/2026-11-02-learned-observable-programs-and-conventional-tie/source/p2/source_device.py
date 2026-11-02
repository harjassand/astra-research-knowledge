"""Reproducible synthetic experimental instrument, NOT an input file for learner.
A local pinned-neighbour bath clamps a three-spin configuration for exposure E;
conditional counts are Poisson(c(s)*E). Learner gets counts and E only.
No physical experiment has been performed.
"""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class PrivateBath:
    alpha: float
    left: float
    right: float
    catalytic: float

    def rate(self, spins):
        l,c,r=spins
        return self.alpha-self.left*l*c-self.right*c*r-self.catalytic*l*r

class MeasuredDevice:
    def __init__(self, modes, seed=3457):
        self._modes=dict(modes)
        self.rng=np.random.default_rng(seed)
        self.exposures=0.
        self.calls=0
        self.reported_events=0
    def observe(self, mode, spins, exposure):
        assert spins in tuple((a,b,c) for a in (-1,1) for b in (-1,1) for c in (-1,1))
        assert exposure>0
        self.calls+=1
        self.exposures+=exposure
        c=self._modes[mode].rate(spins)
        assert c>0
        k=int(self.rng.poisson(c*exposure))
        self.reported_events+=k
        return k

BATHS={
    'baseline':PrivateBath(.80,.18,.16,.035),
    'reduced_noise':PrivateBath(.55,.18,.16,.035)
}
