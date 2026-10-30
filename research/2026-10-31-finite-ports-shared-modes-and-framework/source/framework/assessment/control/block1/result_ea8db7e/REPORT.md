# Unknown static gains with a moving retained medium

The arbitrary-accuracy problem remains open in this continuation. The
substantive results are a legal finite program with uniform full diamond
error below **0.84**, a lower bound **0.583910...** for every classical mixture
of completed `g_A g_B g_C F` rotations, and an exact order-four moving-bath
noise witness for the checkpoint cycle. The lower bound is explicitly
restricted; it is not a no-go theorem for all native randomized programs.

All three results preserve the stated first local-motion promise, unknown
gains in `[1,2]^3`, private coin independence, arbitrary finite spectators,
and arbitrary initial data-memory-reference correlations. No calibration,
memory initialization, bath inverse, measurement, extra logical pulse, or
higher temporal derivative bound was added.

## The construction

Write `c=g_A g_B g_C` and `F=Z1 X2`. The checkpoint cycle extends uniformly
to the gain box:

\[
\left\|\mathbb E\operatorname{Ad}_{U_{cycle}}
-\operatorname{Ad}_{e^{-4ic\delta^3F}\otimes B}\right\|_\diamond
\le100000\delta^4,\qquad\delta\le1/20.
\]

Fresh cycle signs permit composition on the same retained memory. Thus any
prescribed coefficient `Theta` gives a completed operation approximating
`exp(-i c Theta F)`, without learning `c`. This alone does not normalize the
angle.

Instead of replacing an average of unitaries by a unitary, retain its full
channel characteristic function `z(c)=E exp(-2icTheta)`. The exact channel
distance to the desired entangler is `|z(c)+i|`. An exponential angle law of
mean `3/8` gives a uniform distance at most `sqrt(26/37)=0.838273644...`.
An exactly finite capped geometric law approximates it. Compiling every
sampled angle with the native cycle gives the rigorous bound

\[
\text{error}\le\sqrt{26/37}+6/8192+2e^{-16}+1/2048
=0.839494573...<0.84.
\]

The finite program uses at most 131,072 geometric trials, each from thirteen
fair bits, then executes the selected number of fresh-sign native cycles.
All branches have a finite maximum duration and can finish at a common time
using bath-only idles. It is an existence result with astronomical costs:

| Resource | Explicit worst case |
|---|---:|
| Native cycle duration parameter | `delta=2^-30` |
| Cycles | `3*2^89` |
| Native segments | `15*2^90`, about `1.857e28` |
| Total native duration | `15*2^60`, about `1.729e19` |
| Absolute binary timing places sufficient for stated independent errors | 202 |
| Gain evaluations, measurements, resets | 0 |

This does not supply the requested arbitrary `epsilon`, and makes no
practical efficiency claim. The same construction can approach
`sqrt(26/37)` from above to any additional positive tolerance.

## The hardest restriction and failure test

Arbitrary compositions and classical mixtures of completed scalar rotations
cannot do arbitrarily better merely by making their native approximation
finer. Their moments at `c=1,...,8` form a positive semidefinite nine-by-nine
Toeplitz matrix. The desired moments, all `-i`, form a matrix with eigenvalue
`1-cot(pi/18)<0`. Perturbation by an error `d` in each moment has operator
norm at most `8d`, proving

\[
\sup_{c\in[1,8]}|z(c)+i|
\ge[\cot(\pi/18)-1]/8=0.583910227... .
\]

This tests every probability law of accumulated scalar angles, not just the
chosen geometric family. Completed rotations retain too little coherent
memory structure for the older polynomial compensation argument.

The tempting repair—cancel the mean cubic signal and expose a fifth or ninth
order term—also faces genuine channel noise. With admitted static bath
`H_M=sigma_y/2`, unit gains and initially maximally mixed memory, the
checkpoint cycle has averaged entanglement fidelity

\[
F_e=1-41\delta^4+O(\delta^5)
\]

relative to its intended third-order data gate. The coefficient is from two
independent sign-dependent errors of sizes `5 delta^2` and `4 delta^2`.
The exact forward-drift rational calculation reproduces `-41`. Thus this
cycle does not have a smaller channel remainder that can simply be reused
for higher gain powers. The statement concerns this cycle; it does not rule
out redesigned native words or a different coherent intermediate object.

## Artifacts and evidence

- [PROOF.md](PROOF.md) contains the continuum bounds, full operational scope,
  finite law, precision analysis, and restricted lower bound.
- [schedule.py](schedule.py) is a lazy native schedule generator, with exact
  finite private-coin sampling and resource calculation.
- [check.py](check.py) verifies the order-four coefficient by exact rational
  matrix algebra, checks the moment-matrix eigenvector, exercises a finite
  schedule prefix, and diagnoses the scalar response on a grid.
- [checks.json](checks.json) records the executed output. Its finite grid is
  a diagnostic; the analytic proof carries the moving-bath and continuum
  guarantees.

The supplied predecessor already contains sign projection, clean odd powers,
and polynomial gain compensation under stronger regularity. This work does
not claim those ideas as new, and does not import their stronger hypotheses.
The unresolved step is a native first-motion construction that retains
nonlinear gain response while controlling its actual channel variance, or a
quantitative obstruction for the full allowed policy class.
