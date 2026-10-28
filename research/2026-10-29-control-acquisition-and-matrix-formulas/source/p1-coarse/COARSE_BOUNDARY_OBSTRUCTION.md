# A coarse boundary report is not a regenerative state

29 October 2026, Brisbane. This is the next attack after the completed
observed-absorption construction. The attempted extension replaces an exactly
recognized boundary state by a coarse live-state label and a reproducible
initial distribution. That extension fails decisively, even with fresh
preparation on every acquisition trial and strictly contracting sources.

## Exact indistinguishable acquisition laws

There are two live microscopic states, both reported as the same coarse cell
B. Cemetery is correctly and irreversibly reported. Initial preparation is
uniform over the two live states. For 0<g<=1/32 take

    A_g=diag(1-g^3,1-g),
    p_g=1-(g+g^3)/2,
    B_g=p_g I.

Both killed kernels are symmetric, nonnegative, and have norm strictly below
one. Every coarse first-return trial ends at time one, either in B or in
cemetery. Under both sources its exact distribution is

    P(B)=p_g,  P(absorbed)=1-p_g,
    P(excursion return)=P(alive outside)=0.

Therefore any number of fresh trials of the proposed coarse first-return
protocol, with any censor horizon, has exactly the same joint record law for
the two sources. A larger statistical budget cannot resolve this ambiguity.
This is an obstruction for these records, not for arbitrary uninterrupted
long-word experiments.

The actual h-step coarse survival probability is

    f_A(h)=[(1-g^3)^h+(1-g)^h]/2,
    f_B(h)=p_g^h.

For g=1/m and h=10m, Bernoulli's inequality and p_g<=1-g/2 give

    f_A(h)-f_B(h) > 1/2-5g^2-1/100 > .48.

The bound exp(-5)<1/100 follows from a finite positive Taylor lower bound
for exp(5). Thus the same exact acquisition records are compatible with a
large later discrepancy. All states eventually absorb; an immortal hidden
mode is unnecessary.

## The missing physical residual

Let v=(1,1)/sqrt(2), the Hilbert-space preparation column. Its true residual is

    D=A_g v-p_g v
      =[(g-g^3)/2] (1,-1)/sqrt(2),
    ||D||^2=(g-g^3)^2/4>0.

Every microscopic state lies inside the reported cell. A positive flag based
only on leaving that cell is identically zero, yet the state distribution
inside the cell drifts. The finite-dimensional projection vv* is not the
diagonal projector onto all microscopic states carrying the label B. The
previous proof requires the former residual and acquires it from the latter
path events only when the recognized boundary states really are the declared
atoms. Confusing those projections would falsely erase D.

Even the restart claim fails for coarse labels: conditioned on survival, the
mixture increasingly favors the slow state. A positive B report does not
restore the original uniform distribution. The indistinguishability argument
above grants fresh preparation precisely to avoid relying on that separate
mistake.

## A real operation can impose closure, at an explicit price

Suppose an additional physical operation R randomizes the live cell uniformly
and leaves cemetery absorbed. Its live kernel is

    R=[[1/2,1/2],[1/2,1/2]],   R^2=R.

For any source primitive A_i,

    R A_i R=p_i R,
    p_i=(1/2)(1,1) A_i (1,1)^T.

The physically refreshed language consequently has exact scalar closure:
every standardized macro R A_i R has coefficient p_i, and an arbitrary word
has response equal to the product of its p_i values. This also holds for
noncommuting source primitives; the executable adds a second positive kernel
and checks nontrivial mixed words.

This operation changes the future program. For the counterexample its long
response becomes p_g^h instead of f_A(h), destroying the protected slow
population that caused the discrepancy. It does not certify unmodified
source words. A standardized h-step program pays h original applications
and h physical refreshes; a single final coarse read can omit the last
refresh. The refresh implementation and its conditional distribution must be
physically warranted. Calling a detector outcome a reset does not implement it.

This is ordinary projection/lumpability machinery, included as the strong
constructive alternative, not claimed as a new randomization principle.
Exact and approximate Markov aggregation already distinguish the conditions
under which a coarse process preserves original transient behavior; see
P. Buchholz, *Exact and ordinary lumpability in finite Markov chains*,
Journal of Applied Probability 31 (1994), 59-75,
https://doi.org/10.2307/3215235 .

## Executed evidence and resulting research obligation

core/coarse_boundary_obstruction.py executes the exact two-state algebra for
g=1/32,1/64,1/128,1/256. At h=10/g the source discrepancies are approximately
.4887151,.4922029,.4930465,.4932414. It verifies identical fresh one-step laws,
strict source contraction, and the refreshed projection identities. These
are exact rational checks, not new stochastic experiments. Large rationals
are stored as hexadecimal numerator/denominator pairs in the receipt.

The attempted coarse-label extension is rejected. The surviving routes are
to acquire additional within-cell memory information, to warrant a true
regeneration distribution, or to pay for an actual physical refresh and
certify the resulting altered language. The original scalar-word Gram
construction remains relevant to the first route: f(2)-f(1)^2 already exposes
the missing within-cell residual in this example. Its measurement precision
and long-horizon acquisition costs must still be paid. No autonomous discovery
of a suitable regenerative interface has been established by this continuation.
