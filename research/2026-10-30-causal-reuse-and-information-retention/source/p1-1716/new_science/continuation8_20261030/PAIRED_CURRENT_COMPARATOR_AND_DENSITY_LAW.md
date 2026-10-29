# A strong paired-current comparator: identical complete density law

30 October 2026. Root reconstruction of an ordinary linear mechanism, informed
by the direct paired-current predecessors. The result is useful selection
information, not a claim that pairing currents or projecting Gaussian noise is
new. The physical variables here are signed harmonic density/charge fluctuations,
not nonnegative particles or the exclusion process of the other theorem.

## 1. Actual harmonic current operation

Let x in R^N have conserved sum zero and let (B j)_i=j_(i-1)-j_i on a ring.
An actual reversible current bath with symmetric positive semidefinite mobility C
is specified by

    dJ=-(1/2)C B^T x dt + sqrt(C) dW,
    dx=B dJ.                                                (1)

The matching drift and noise are both parts of the operation. Merely adding
anticorrelated noise while leaving an incompatible dissipative response does
not supply (1). The invariant state law is the unit Gaussian on sum x=0,
because the state drift is -(1/2)B C B^T x and its noise covariance is B C B^T.
It may be initialized at this law or at any explicitly supplied common x_0
when comparing complete state paths. White noise is an ideal rate model, not
a finite-bandwidth apparatus claim.

For each bond pair (b,b+r), put v_(b,r)=e_b-e_(b+r). It produces equal and
opposite physical bond currents. Give each pair an independent scalar bath,
with covariance weight s(N-1)/(2NR), and the corresponding reversible force
response. The resulting physical mobility is

    C_R=[s(N-1)/(2NR)] sum_(r=1)^R sum_b v_(b,r)v_(b,r)^T.   (2)

All pair currents sum to zero, including their drift, so

    sum_b J_b(t)=0                                          (3)

on every path, when initial integrated currents are zero. The active coupling
range is R (or its circular counterpart); a pair separated by a macroscopic
fraction of the ring is a nonlocal operation. No sensor is presumed to create
that operation for free.

## 2. At full range, all density histories match ordinary diffusion

Let P=I-11^T/N. For R=N-1, the ordered-pair sum in (2) equals 2NP, hence

    C_(N-1)=sP,    B P=B,    P B^T=B^T.                    (4)

The ordinary reference bath has C_0=sI. Its density generator is identical:

    B C_(N-1) B^T=s B B^T=B C_0 B^T.                      (5)

With the same initial x_0 the COMPLETE density-path laws agree, for every finite
N and every horizon, not merely their mean equation, invariant distribution or
Gaussian large-scale approximation. An explicit mathematical coupling uses
the same N-dimensional W and sets

    dJ_ref=-(s/2)B^T x dt+sqrt(s)dW,
    dJ_pair=-(s/2)B^T x dt+sqrt(s)P dW.                    (6)

Both produce exactly the same dx path because B P=B. This coupling is a proof
between two supplied physical architectures, not an experiment requiring two
futures from one hidden specimen. The pair decomposition in (2) supplies a
separate implementation of the same Gaussian covariance.

The total reference current has variance sNt, whereas the paired total current
is identically zero. The removed stochastic mode is invisible to the density
continuity equation. Output currents and their implementing apparatus must be
specified; calling an unchanged physical current a different mathematical
observable would not implement this construction.

## 3. The locality tradeoff is explicit

For spatial Fourier wave number k, the current mobility and density decay rate
are respectively

    c_R(k)=[s(N-1)/(2NR)] sum_(r=1)^R |1-exp(ikr)|^2,
    lambda_R(k)=(1/2)|1-exp(ik)|^2 c_R(k).                 (7)

For the fundamental k=2pi/N and R=o(N),

    lambda_R(k) ~ [s(N-1)/(24N)](R+1)(2R+1) k^4.          (8)

Thus its relaxation time is of order N^4/R^2. At full range,

    lambda_(N-1)(k)=(s/2)|1-exp(ik)|^2                    (9)

for every nonzero Fourier mode, giving ordinary diffusive N^2 relaxation.
Including every separation from 1 to R avoids a spurious extra null mode caused
by a single pair separation commensurate with N.

This is exact attainment of the analogous range scaling in a harmonic
continuous-current model. It is not a proof of sharpness inside every bounded
occupation jump class used in `LOCALITY_COST_OF_CURRENT_CONTROL.md`.

## 4. What this comparison changes

The broad goal "same density behavior, different current noise" already has a
simple constructive solution when equal/opposite distant-current ports and a
compatible bath are supplied. The event-updated bit does not earn a novelty
claim merely by suppressing circulation or retaining mean diffusion. Its
potential contribution is a different discrete transition operation and its
actual cost, robustness and receiving law.

This harmonic comparator grants no unknown kinetic bath for free. Its mobility
and fluctuation-dissipation pairing are known. The event-memory graph result
instead permits arbitrary unselected reversible kinetics but supplies its
selected mean rates. The earlier independent-phase result tolerates a different,
larger class of unknown selected amplitudes through actual fast control. These
interfaces are not silently identified with one another.

Hexner--Levine, *Noise, diffusion, and hyperuniformity*, arXiv:1611.02386, already
constructs center-of-mass-conserving kicks and altered noise with ordinary mean
diffusion in a driven active setting. Morningstar--O'Dea--Richter,
*Hydrodynamics in long-range interacting systems with center-of-mass conservation*,
arXiv:2304.12354, explicitly derives a variable-range paired-current dispersion
and subdiffusive/diffusive regimes. Wachtel--Vollmer--Altaner,
arXiv:1407.2065, proves current gauge invariance under bounded coboundaries.
Those primary constructions preclude broad priority claims for the ideas used
here. The present calculation is a transparent exact comparator for the actual
operation/resource question, not an asserted new universality class.
