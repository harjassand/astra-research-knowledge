"""Exact rational reference for collision-certified determinant completion.

No floating-point sampling probabilities or spectral oracles. Matrix arithmetic
uses Fraction. Random integer draws use Random.getrandbits with rejection.
The model treats these pseudorandom bits as independent fair bits; pass a
SystemRandom instance for OS-provided randomness. Expected random-bit cost is
charged explicitly in returned diagnostics. No unproved MCMC mixing assumption.
"""
from fractions import Fraction as F
import random
import math
import sympy as sp


def _dot(a,b): return sum((x*y for x,y in zip(a,b)),F(0))
def _matvec(A,x): return [_dot(row,x) for row in A]

def _bernoulli(p,rng,counters):
    if p<0 or p>1: raise ArithmeticError(f'Invalid exact probability {p}')
    if p==0: return False
    if p==1: return True
    b=p.denominator; k=(b-1).bit_length()
    while True:
        z=rng.getrandbits(k); counters['random_bits']+=k; counters['integer_trials']+=1
        if z<b: return z<p.numerator


class ExactCompletionSampler:
    """Exactly sample prod(p_i)*det(I + sum_{i in S} x_i x_i^T), one per group."""
    def __init__(self,X,groups,prior=None,prior_precision=None):
        self.X=[[F(x) for x in row] for row in X]
        self.N=len(X)
        if not self.N: raise ValueError('Empty feature matrix')
        self.d=len(X[0])
        if not self.d or any(len(row)!=self.d for row in self.X):
            raise ValueError('Feature rows must have equal positive length')
        self.groups=list(map(int,groups))
        if len(groups)!=self.N or min(groups)!=0:
            raise ValueError('Groups must match rows and begin at zero')
        self.g=max(groups)+1
        self.members=[[i for i in range(self.N) if groups[i]==g] for g in range(self.g)]
        if any(not part for part in self.members): raise ValueError('Group labels must be contiguous')
        self.p=[F(1,len(self.members[groups[i]])) for i in range(self.N)] if prior is None else list(map(F,prior))
        if len(self.p)!=self.N or any(x<=0 for x in self.p): raise ValueError('Prior must be positive')
        if any(sum(self.p[i] for i in part)!=1 for part in self.members):
            raise ValueError('Each group prior must sum EXACTLY to one')
        A=[[F(int(i==j)) for j in range(self.d)] for i in range(self.d)] if prior_precision is None else [[F(x) for x in row] for row in prior_precision]
        if len(A)!=self.d or any(len(row)!=self.d for row in A) or any(A[i][j]!=A[j][i] for i in range(self.d) for j in range(self.d)):
            raise ValueError('Prior precision must be a symmetric d-by-d matrix')
        MA=sp.Matrix([[sp.Rational(x.numerator,x.denominator) for x in row] for row in A])
        if prior_precision is not None and any(MA[:k,:k].det()<=0 for k in range(1,self.d+1)):
            raise ValueError('Prior precision must be strictly positive definite')
        da=MA.det(); self.prior_determinant=F(int(da.p),int(da.q))
        B=[[A[i][j]+sum(self.p[k]*self.X[k][i]*self.X[k][j] for k in range(self.N))
               for j in range(self.d)] for i in range(self.d)]
        M=sp.Matrix([[sp.Rational(x.numerator,x.denominator) for x in row] for row in B])
        inv=M.inv(); det=M.det()
        self.R=[[F(int(inv[i,j].p),int(inv[i,j].q)) for j in range(self.d)] for i in range(self.d)]
        self.dpp_normalizer=F(int(det.p),int(det.q))/self.prior_determinant
        H=[_matvec(self.R,x) for x in self.X]
        diag=[_dot(self.X[i],H[i]) for i in range(self.N)]
        C=F(0)
        for part in self.members:
            for pos,i in enumerate(part):
                for j in part[pos+1:]:
                    hij=_dot(self.X[i],H[j])
                    C+=self.p[i]*self.p[j]*(diag[i]*diag[j]-hij*hij)
        if C<0: raise ArithmeticError('Exact collision moment is negative')
        self.collision_sum=C
        self.acceptance_lower_bound=max(F(0),1-C)

    def proposal(self,rng,counters):
        """Draw an ordinary DPP subset; reject as soon as two choices clash."""
        R=[row[:] for row in self.R]
        chosen=[-1]*self.g
        for i in range(self.N):
            z=_matvec(R,self.X[i]); h=_dot(self.X[i],z); q=self.p[i]*h
            counters['conditional_updates']+=1
            inc=_bernoulli(q,rng,counters)
            if inc:
                g=self.groups[i]
                if chosen[g]>=0: return None
                chosen[g]=i
                coeff=-1/h
            else:
                coeff=self.p[i]/(1-q) if q!=0 else F(0)
            if coeff:
                for a in range(self.d):
                    for b in range(a,self.d):
                        R[a][b]+=coeff*z[a]*z[b]; R[b][a]=R[a][b]
        return chosen

    def _complete(self,chosen,rng,counters):
        for g,part in enumerate(self.members):
            if chosen[g]>=0: continue
            mass=F(1)
            for i in part[:-1]:
                if _bernoulli(self.p[i]/mass,rng,counters): chosen[g]=i; break
                mass-=self.p[i]
            if chosen[g]<0: chosen[g]=part[-1]
        return chosen

    def sample(self,count,seed=1,max_trials=None,rng=None):
        if not isinstance(count,int) or count<1: raise ValueError('count must be positive')
        rng=random.Random(seed) if rng is None else rng
        counters=dict(random_bits=0,integer_trials=0,conditional_updates=0,proposals=0)
        out=[]
        while len(out)<count:
            if max_trials is not None and counters['proposals']>=max_trials:
                raise RuntimeError('Budget exhausted; no biased fallback was returned')
            counters['proposals']+=1
            chosen=self.proposal(rng,counters)
            if chosen is not None: out.append(self._complete(chosen,rng,counters))
        return out,counters

    def normalizer_estimate(self,epsilon,delta,seed=1,max_proposals=1000000):
        """Relative-error estimate with a rationally allocated Chernoff budget.

        epsilon and delta are interpreted as exact Fraction inputs. No computed
        logarithm or floating acceptance bound is used to choose the budget.
        """
        epsilon,delta=F(epsilon),F(delta)
        if not 0<epsilon<1 or not 0<delta<1:
            raise ValueError('epsilon and delta must lie strictly between zero and one')
        a=self.acceptance_lower_bound
        if a<=0: raise ValueError('No positive acceptance lower bound is available')
        # b >= log_2(2/delta) >= ln(2/delta), entirely in integer/rational arithmetic.
        b=0
        while delta*(1<<b)<2: b+=1
        required=F(3*b)/(a*epsilon*epsilon)
        N=(required.numerator+required.denominator-1)//required.denominator
        if N>max_proposals:
            raise ValueError(f'Requested guarantee needs {N} proposals, over budget {max_proposals}')
        estimate,accepted,counters=self.normalizer_estimate_fixed(N,seed)
        counters.update(relative_error=str(epsilon),failure_probability_upper=str(delta),
                        acceptance_lower_bound=str(a))
        return estimate,accepted,counters

    def normalizer_estimate_fixed(self,N,seed=1):
        """N independent Bernoulli trials; estimate = det(B)*accept_count/N.
        For 0<epsilon<1: failure <= 2 exp(-N*a_lower*epsilon^2/3).
        N is user-specified to avoid hiding a confidence-parameter rounding.
        """
        if not isinstance(N,int) or N<1: raise ValueError('N must be positive')
        rng=random.Random(seed); counters=dict(random_bits=0,integer_trials=0,conditional_updates=0,proposals=N)
        accepted=0
        for _ in range(N):
            if self.proposal(rng,counters) is not None: accepted+=1
        return self.prior_determinant*self.dpp_normalizer*F(accepted,N),accepted,counters
