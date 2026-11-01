# Pending separate scalar-acquisition corollary

Depends on, and does not alter, the pending complete small-tilt theorem
`stochastic_multiface_small_t_20261101/THEOREM_PENDING.md`, hash
dc96226443a99ee0a8541f03cce5af28ff735a95c6855053d223cf87d5001327.
No independent whole acceptance is claimed for either package.

## Replace independent-set counting by a literal bound

In the base theorem, M,q,g,h,CA,CH,d,T,B,R,K are acquired before the independent-
set weight sum P. Preserve all those constants and the actual function

 Psi(x)=sum_{nonempty independent I} K^(n-|I|) Z_(J_I(x)).

The binomial identity gives the acquired scalar upper bound

 P <= Pbar=(K+1)^n = sum_{all I subset [n]} K^(n-|I|).

Use Pbar instead of P in RA,RQ,Cbirth,H,Htot, and reacquire eps,t,D,e,Nstar,nu,zeta
and the final finite moment expression in that order. Every use of P in the proof
is an upper bound on either the face-weight sum or Psi, so the exact same proof
applies. The source-transfer reserve S and its sstar lower bound are unchanged.
The drift expression still uses the actual sum Psi, not a fictitious all-subsets
profile. In particular no non-independent face is introduced into the proof.

This supplies actual rational t>1, finite integer Nstar, rational zeta,Htot, and
an exact finite expression for CF and pi(t^N)'s upper bound **without enumerating
or counting independent sets**. Qualitative raw admission is just the raw scan.

## Representation and bit cost

Let L be the total ordinary binary input length of the explicit species/complex/
rate list. Species count n, directed-channel count and all rational rate bit
lengths are charged in L; n<=O(L). Summing rational rates gives numerator and
denominator bit lengths bounded by O(L), before any harmless polynomial overhead
for canonicalization. M=ceil(12s/b) may be exponentially large in numerical value,
but its binary length is O(L). All formula operations up to K have fixed algebraic
degree, except 2^n, whose binary representation has n+1 bits. Thus their rational
bit lengths remain O(L) up to a fixed polynomial bound.

Pbar=(K+1)^n has O(n*bits(K+1)) bits. The selector's hh=eta^(n-1)/(2n) has
O(n log n) bits. Every subsequent scalar is obtained by a fixed number of rational
operations, minima/maxima and ceilings on these numbers. The rational lower
bound dA=1/[8(3M+1)^2], rather than exact D_(2M), is crucial: there is no scalar
power q^M whose bit length is proportional to M's possibly exponential value.
Consequently the scalar output and arithmetic running time are polynomially
bounded in L under ordinary exact-integer algorithms. This is a bit-complexity
claim for the displayed scalar formulas, not a small-constant practicality claim.

The final power t^(Nstar+1) remains factored. Expanding that number may have
exponential or worse output length and is separately budgeted. Likewise the
actual Lyapunov multiplier retains a finite algorithmic sum over at most 2^n-1
independent sets, with the raw graph and exact weights as its descriptor. Expanding
or evaluating that sum remains potentially exponential and is NOT claimed
polynomial. Individual q^(-J) evaluations have exponent and rational bit costs.
The compact sum recipe is not a supplied independent-set or stationary-law oracle:
its literal enumeration semantics and proof are explicit.

## Scope

The result remains one acquired nonzero exponential stationary moment for the
stated full reversible square-free binary one-port hub architecture. It does not
supply all finite exponential moments, arbitrary weak reversibility, or historical
novelty. The binomial upper-bound idea is an ordinary counting bound suggested by
the root, and all finite subset and Foster ingredients are retained as components.
