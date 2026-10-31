# Costs, strongest retaining alternatives, and failure boundary

## What the run actually computed

`capacity.py` starts from rational polynomial monomials, not a known
committor or a basis handed directly to the integrator. All five main runs
use coordinate-aligned sparse input; the coordinate is recognized from its
degree-six monomials and the entire coefficient list is checked. The
separate rotated five-dimensional example is fully expanded before the
acquirer sees it: 295 monomials, exact nullspace of the quadratic Hessian, a rational
orthogonal projector, full polynomial equality, exact LDL, and checked
determinant coefficients. It recovers `(53,-4,-6,-8,-10)/55` in about
0.40--0.46 seconds in author runs. Nonsquare direction normalization and irrational fiber
eigenvalues are handled exactly, without a numerical eigensystem.

These are different acquisition bills. The 129-dimensional example does
NOT establish that expanding a generic rotated 129-dimensional degree-six
polynomial and verifying its full identity is cheap. A generic degree-six dense
coefficient representation has O(n^6) entries. Our sparse JSON stores full
n-component exponent vectors, so even its 3m monomials take O(m^2) small
integer entries. An O(m) sparse-exponent encoding is not silently assumed.

At beta=1, kappa_i ranges linearly from 1/2 to 3/2. Values below are
capacity/mass in the stated nondimensional diffusion clock, not physical
time measurements and not arbitrary-start first-passage rates.

| Dimension | Raw monomials | Exact quadrature points | Product factors | Largest product integer bits | Full conductance interval |
|---:|---:|---:|---:|---:|---:|
|3|6|4,097|8,194|98|[0.30275683, 0.57604644]|
|5|12|2,049|8,196|182|[0.23263105, 0.44217607]|
|17|48|2,049|32,784|752|[0.01109235, 0.02113003]|
|65|192|4,097|262,208|3,396|[3.4423282e-9, 6.5622351e-9]|
|129|384|8,193|1,048,704|7,571|[2.2772960e-18, 4.3298081e-18]|

For the last row, arithmetic/quadrature took about 3.2--3.5 seconds on the
available machine and raw sparse acquisition about 0.008 seconds. These
are one-run diagnostic timings, not a universal benchmark. The interval
width is the rigorous 17/9 finite-rate factor times at most 1.01 numerical
width; actual numerical factor was 1.00657. The barrier is not crossed
once by a simulated trajectory. A sequential receiving verifier reacquires
the raw model and recomputes all exact bounds, incurring the same order of
cost again. Repeated valid requests may retain this result; comparators
may retain it too.

## Exact arithmetic and truncation

At each rational y, the sparse program forms the exact numerator and
denominator of `D(v)=product(1+kappa_i v)`. The generic acquired route
evaluates the verified determinant polynomial by rational Horner arithmetic. It encloses its square root and reciprocal
square root by integer square root on the scaled rational, with outward
dyadic endpoints. There is no floating eigensolver, quadrature estimate,
or underflowed exponential in an accepted bound. Python's arbitrary-size
integer arithmetic is part of the bill.

Both q and 1/q are monotone on each of [0,1/2], [1/2,1], and [1,T].
Endpoint Darboux bounds therefore enclose each integral. The unbounded
tail is bounded analytically by Proof (6); T is increased and charged
until it is sufficiently small. The dyadic grid is refined and charged
until the PRODUCT of the mass and resistance interval ratios meets the
external relative tolerance. If it cannot, the computation returns UNKNOWN.
The receiving verifier binds beta, the exact acquired coordinate, basin
threshold, observable, dimension, tail, and final intervals to the raw
input. It checks a separate external quadrature tolerance. Float display
fields and timings are not proof inputs.

Independent review found and repaired three executable boundary defects:
an unresolved zero seed lower bound could previously leave the cutoff loop
unbounded; a non-exact NaN tolerance could bypass the receiving comparison;
and binary64 diagnostic display could overflow despite valid exact output.
The repaired version fails closed on unresolved seed mass, validates all
external tolerance/budget types before work, checks initial and total grid
budgets, and caps cutoff, precision, product/Horner bit size and point count.
Display values outside binary64 range are null with an explanatory status;
the exact rational remains the evidence. Interpreter decimal serialization
limits produce an explicit UNKNOWN, not a partial certificate.
`max_integer_bits` is specifically the determinant-product/Horner rational
size proxy, not a measurement of every integral/reciprocal/output integer;
beta and final output arithmetic also have their ordinary bit cost.

## Why rare probability is not an exponential arithmetic cost here

This paragraph is a bound for kappa_i in a fixed positive compact interval,
fixed beta, and the aligned sparse route, not for arbitrary ill-conditioned
coefficients. Let W=q(0)^-1. For 0<=y<=1/(2sqrt(m)),
`w(y)>=exp(-1/2)W`, so `R0>=exp(-1/2)W/sqrt(m)`, while R0<=W. On
`1<=y<=1+1/sqrt(m)`, `q(y)>=exp(-9 kappa_+/2)`, hence
`MA>=exp(-9 kappa_+/2)/sqrt(m)`. The displayed fixed-endpoint constants
are conservative; their only role is proving polynomial dependence.

With common grid width h, the exact monotone Darboux widths are at most
`2h W` for R0 and `2h` for the compact mass integral. Thus relative
quadrature width O(epsilon) follows from `h=O(epsilon/sqrt(m))`, plus a
tail budget and ordinary rounding allowance. A cutoff polynomial in
1/epsilon suffices uniformly for m>=2, since the slowest allowed tail is
order T^-3 and the tail bound improves with m once T is a suitable fixed
constant. The actual adaptive code also pays all unsuccessful grids.

If rational coefficients have bit length B and grid coordinates bit length
O(log N+log T), each unreduced product has
O(m(B+log N+log T)) bits. Dyadic precision may be chosen polynomial in
m, B, and log(1/epsilon); the executed choice is max(192,4m+128).
There are O(m) rational factors per point, polynomial-time integer
multiplications/square roots on those bit lengths, and polynomially many
points in this conditioned regime. The final rate of order exp(-Theta(m))
requires Theta(m) output bits, not exp(Theta(m)) simulation time.

This is NOT a polynomial-in-input-bits guarantee for arbitrary kappa_i:
an exponentially narrow well induced by huge kappa_i can defeat uniform
gridding, and generic dense symbolic acquisition/identity checking is charged but
not given a tight complexity theorem here. Fixed precision can fail and
returns UNKNOWN. A low-dimensional representation by itself is not
claimed to make its acquisition cheap.

## Strong retaining comparisons (all get the SAME raw input and acquisition)

1. **Gaussian elimination/free energy + classical Thomson/Dirichlet.**
   These are the strongest exact ordinary primitives. Located primary
   sources supply the variational principles, coarse-grained upper bound,
   Gaussian transport geometry, and scalar integration machinery. The
   explicit acquired current together with THIS dimension-free resistance
   estimate is the construction proved here; no located pre-existing source
   has yet been shown to supply the same guarantee. An equally informed
   comparator augmented with this newly earned certificate can implement
   the entire result. That shows no proprietary algorithmic separation,
   not a separate prior-art victory or a reason to count our proof twice.
   Historical novelty is unresolved. The scoped contribution is a
   proof-producing multiplicative full-rate certificate beyond the
   free-energy upper bound, constructed using ordinary mathematics.
2. **Free-energy effective one-dimensional dynamics.** It computes the
   same scalar `k_free` cheaply and gives the rigorous variational upper
   bound. In general its generator is not the full projected generator.
   The contribution tested here is an acquired, finite-rate lower bound
   with loss <=17/9 at beta=1. Standard capacity methods are allowed to
   use the newly constructed lower-bound current as well, so this is not
   a proprietary computational separation. This augmented comparator is
   not misidentified as an independently located prior theorem.
3. **Global saddle-point / convex-fiber minimization.** This already
   gives exact energy sublevel reduction where appropriate; the original
   candidate was not pursued as novel. For THIS family it returns zero
   energy along the entire z=0 line and cannot by itself compute the
   entropic conductance. Adding exact Gaussian integration repairs it
   and reduces to comparator 1, which is credited.
4. **Direct rare-trajectory sampling.** Observing events of exponentially
   small stationary flux is a poor baseline here. We demonstrate its
   unnecessary cost, not a universal lower bound on all simulation
   methods. Importance sampling, splitting, umbrella sampling, TPT,
   committor learning, and optimized reaction coordinates are all real
   alternatives; their exact conditional Gaussian specialization should
   be used rather than a deliberately blind sampler. No head-to-head
   empirical superiority over those optimized implementations was run.
5. **Full elliptic PDE/tensor solver.** It can resolve the actual committor
   and potentially tighten the interval. Its useful trial functions or
   flows also yield ordinary certified bounds. Generic dense n-dimensional
   grids are not the strongest baseline once the acquired structure is
   visible. Distinct kappa_i remove full radial symmetry, but retain
   independent Gaussian diagonalization, which is fully credited.
6. **Classical Fick--Jacobs/entropic transport and conditional dynamics.**
   Entropic bottlenecks and Gaussian free-energy elimination are old.
   Source-ledger comparisons distinguish asymptotic/narrow-channel or
   time-marginal approximations from this finite variational conductance
   statement. The latter distinction is scope, NOT a historical novelty
   proof. An exhaustive search for the exact constant-factor theorem
   has not been completed.
7. **Sample-based sliced-committor variational rates.** Petersen,
   Lichtinger, and Covino (2026) already estimate rates from reused
   equilibrium/reweighted configurations and one-dimensional profiles,
   without requiring rare crossing samples. Their exact flux-fidelity
   variational principle is credited. Their implemented substitution of
   basin-average fidelity for flux-weighted boundary fidelity is explicitly
   approximate and can lose the bound direction. Our exact full-fiber
   boundaries and acquired current avoid that particular approximation,
   but solve a much narrower structured exact-input task. This is not a
   claim to beat their general data-driven capabilities.

## Boundaries that stay real

* The task returns the two full-fiber basins acquired from the polynomial
  grammar. It does not answer arbitrary preselected basin shapes.
* A Gaussian conditional distribution alone is insufficient. The proven
  dimension-free bound uses the fixed eigenspaces of I+vH. Rotating
  eigenspaces or varying conditional means add transport cost while
  potentially leaving the determinant/free energy unchanged. The general
  transport sandwich then remains available only if its current and cost
  are acquired and finite; the 17/9 estimate does not follow.
* Small kappa is not zero kappa. Degenerate fibers or extra uncontrolled
  directions can destroy normalization/acquisition and are rejected.
* A lower bound on capacity/mass is not a finite-horizon success
  probability, a pointwise MFPT, a spectral gap, or a verified device rate.
* No coefficient noise, model misspecification, physical parameter
  acquisition, nonreversibility, or equipment interface is covered.
* Historical novelty, practical advantage over the strongest retaining
  method, and civilisation-scale significance remain unestablished.
