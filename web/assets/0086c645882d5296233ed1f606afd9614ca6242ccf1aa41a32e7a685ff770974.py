"""Anytime EP lower certificate for independent stationary blocks or known mixing.

This implements the reconstructed theorem in REPORT.txt. It cannot verify its
sampling, stationarity, reversal, or mixing premises from trajectory data.
Standard-library only. Floating-point arithmetic is not a formal certificate.
"""
from collections import Counter
from math import exp, log, sinh


class ReversalCertificate:
    def __init__(self, reverse, rate_grid, alpha=.05, clip=.5,
                 betting_fractions=(.02,.1,.3,.5)):
        if not (0<alpha<1 and clip>0):
            raise ValueError("Require alpha in (0,1) and positive clip")
        if not rate_grid or any(s<0 for s in rate_grid):
            raise ValueError("Require a nonempty nonnegative rate grid")
        if not betting_fractions or any(not 0<e<1 for e in betting_fractions):
            raise ValueError("Require fractions strictly between zero and one")
        self.reverse=reverse
        self.grid=tuple(sorted(set(rate_grid)))
        self.alpha=alpha
        self.clip=clip
        self.etas=tuple(betting_fractions)
        self.counts=Counter()
        self.log_capital=[[0. for _ in self.etas] for _ in self.grid]
        self.n=0
        self.duration=0.
        self.lower=0.

    def update(self, word, duration, mixing_tv=0.):
        """Consume one new block, with its actual physical duration.

        mixing_tv=0 requires a fresh independent stationary block. Otherwise,
        pass a supplied, valid upper bound on conditional start-state TV error.
        Observed words must be hashable, and reverse must be an involution that
        commutes with physical path reversal. Critics use previous blocks only.
        """
        if duration<=0 or not 0<=mixing_tv<=1:
            raise ValueError("Invalid duration or TV bound")
        rw=self.reverse(word)
        if self.reverse(rw)!=word:
            raise ValueError("Reversal must be an involution")
        # Symmetric unit pseudocounts imply exact antisymmetry of this critic.
        critic=log((self.counts[word]+1)/(self.counts[rw]+1))
        critic=max(-self.clip,min(self.clip,critic))
        score=critic+1-exp(-critic)
        score_min=-self.clip+1-exp(self.clip)
        score_range=2*(self.clip+sinh(self.clip))
        drift_allowance=score_range*mixing_tv
        for j,s in enumerate(self.grid):
            denominator=duration*s+drift_allowance-score_min
            ratio=(score-score_min)/denominator
            for k,eta in enumerate(self.etas):
                self.log_capital[j][k]+=log(1-eta+eta*ratio)
            mx=max(self.log_capital[j])
            wealth_log=mx+log(sum(exp(v-mx) for v in self.log_capital[j])/len(self.etas))
            if wealth_log>=log(1/self.alpha):
                self.lower=max(self.lower,s)
        # Updating counts after scoring is essential for predictable learning.
        self.counts[word]+=1
        self.n+=1
        self.duration+=duration
        return self.lower


if __name__=="__main__":
    c=ReversalCertificate(lambda x:x[::-1], [i/100 for i in range(101)])
    for i in range(1000):
        # Merely an API demonstration; these manufactured words are not CTMC data.
        c.update((0,1,2) if i%5 else (2,1,0), duration=1.)
    print({"blocks":c.n,"example_lower":c.lower,
           "note":"Manufactured API demo, no thermodynamic experiment"})
