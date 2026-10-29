# Exponential inverse degree does not force a conditioning or pole loophole

## Exact capability statement

There is an explicit family of compact polynomial vector-field circuits in even
dimension `n` for which the divergence/cyclic-chart route acquires `n+1` projective
coordinates and an inverse of degree `2^(n−1)`, yet a shared inverse DAG has size
`O(n)` and the original-state decoder is uniformly well conditioned on a specified
invariant set for **all real times**. No inverse-degree enumeration is required.

This is a constructed integrable family, not a claim about typical physical
systems, historical novelty, or superiority over equally informed classical
symbolic recognition. The compact-circuit acquisition route is now implemented
for a quadratic search budget in `quadratic_circuit_acquisition.py`; the older
general upstream front end still expands polynomials.

## Construction and global bounds

Let `n=2m`, and let the *forward* chart be

    F_i(x)=x_i+x_(i+1)^2  (i<n),       F_n(x)=x_n.

Its inverse is acquired by the strong-Jacobian-flag algorithm, without receiving
the triangular order. For analysis we can write the same inverse backwards:

    G_n(y)=y_n,       G_i(y)=y_i-G_(i+1)(y)^2.

Thus `deg G_1=2^(n−1)` but the entire vector `G` has an `O(n)` shared DAG.
The general fixed-point acquisition builds at most `O(n size(F))` gates; it can
retain dead intermediate gates, so build size and final reachable size differ.

Let `B` have `m` rotation blocks `[[0,−j],[j,0]]`, `1≤j≤m`, and let
`c=(1,0,1,0,...,1,0)^T`. Define

    g(y)=B y−(c^T y)y,
    M=[[0,c^T],[0,B]],
    f(x)=JF(x)^−1 g(F(x)).

Because `JN=J(F−Id)` is strictly upper triangular, its inverse is the finite
Neumann sum; `f` is polynomial, with a division-free circuit of polynomial size
in `n`, degree at most `n+3`, and coefficients of polynomial binary length. The
inverse polynomial `G` is **not** needed to generate or read that raw circuit.

Write `R(t)=exp(tB)`. The homogeneous flow is

    exp(tM)=[[1,c^T B^−1(R(t)−I)],[0,R(t)]].

Here `R(t)` is orthogonal, and

    ||c^T B^−1||_2^2=sum_(j=1)^m 1/j^2 < 2.

Hence `||exp(tM)||_2 ≤ 1+2 sqrt(2)` uniformly for every real `t`.
For `||y0||_2 ≤ 1/32`, the projective denominator satisfies

    |d(t)−1| ≤ 2 sqrt(2)||y0||_2 < 1/8,
    d(t) ≥ 7/8,
    ||y(t)||_2=||R(t)y0/d(t)||_2 ≤ 1/28 < 1/16.

There are no real-time poles on this entire initial set. If `||y||_infinity≤1/16`,
the backwards recursion proves `||G(y)||_infinity≤1/8`, since
`1/16+(1/8)^2=5/64<1/8`. On this set,

    ||JN(G(y))||_infinity ≤ 1/4,
    ||DG(y)||_infinity ≤ sum_(k=0)^(n−1)(1/4)^k < 4/3.

These are uniform dimension-independent bounds on the inverse decoder's absolute
condition number. Together with the denominator and homogeneous propagator
bounds, the whole decoded flow has polynomial amplification of **initial-state
perturbations** and evaluation roundoff, with only norm-conversion factors if
infinity and Euclidean norms are mixed. This is not a uniform bound on errors in
the generator: a frequency error accumulates phase error proportional to time.
The generator is acquired exactly over the rationals, not inferred noisily.
Nor does the bound assert small *relative* error for coordinates crossing zero.

Unknown fixed linear conjugations can be inserted into `F` when both the map norm
and its inverse norm are bounded; they only change the initial-set radius and
constants by those factors. A bound on condition number alone is not enough:
`L=aI` has condition number one but arbitrary scale. Such conjugation is not
needed for the theorem.

## Why the chart is actually acquired

The eigenvalues of `M` over the complex numbers are `0, ±i, ±2i,...,±mi`, all
distinct. The denominator row sees both eigenmodes in every rotation block and
the zero mode. Therefore `e_0^T` is cyclic and its Krylov rank is `n+1`.

The constant-Jacobian map `F` transports the raw operator
`T=f·grad−div(f)/(n+1)` to `M−tr(M)I/(n+1)=M` on affine hidden functions.
Here `tr(M)=0`. Raw acquisition from `1,T1,...` therefore spans
`(1,F_1,...,F_n)`, up to an acquired affine output transformation. Normalizing
the acquired chart at zero removes that transformation, because `F(0)=0` and
`JF(0)=I`. Its complete Jacobian coefficient-space flag terminates in `n` steps.
This yields a verified small inverse circuit, not an inverse supplied by the
test constructor. The inverse degree bound is irrelevant to that acquisition.

## All resources remain payable

The implemented compact front end keeps a quadratic trial dictionary of size
`(n+1)(n+2)/2`. For each current quadratic basis polynomial `p`, it evaluates
`T(p)=f·grad p+q p` from the raw circuit and its automatically differentiated
divergence. Interpolation at `0, ±e_i, e_i+e_j` reconstructs a quadratic trial.
Fresh PIT compares that trial to `T(p)` before it is admitted; a failure returns
not-acquired. Thus the quadratic degree is a *search budget*, not a supplied
oracle/promise. Exact rational Krylov elimination closes at `n+1` on this family.
Its normalized chart's complete Jacobian coefficient flag is deterministic.

No multivariate expansion of the raw circuit, its iterates, or the inverse is
needed by this route. The explicit Neumann source construction has polynomial
degree and coefficient heights, with no hidden repeated-squaring of huge
constants. Circuit evaluations at polynomial-bit rational points, interpolation,
and exact elimination consequently have polynomial intermediate bit lengths.
This height statement is for the displayed source family, not arbitrary short
circuits. The cyclic Krylov conditioning is handled by exact rational algebra;
it is not smuggled into an ordinary-precision rank decision.

For a residual of degree at most `D`, independent verification at `r` fresh points
from a finite integer set of size `Q` has false-acceptance probability at most
`(D/Q)^r`; allocating an error budget across all adaptive attempts gives the
ordinary union bound. Training randomness must not be reused for admission.
Fixed pseudorandom tests without deterministic replay are not unconditional
certificates. The implementation uses fresh system randomness and reports its
union bound; no deterministic polynomial-time PIT claim is made.

Before numerical evaluation, conjugate the acquired generator by the exact
affine normalization used on its acquired chart. On this family this recovers
the displayed `M` exactly; numerical evaluation is NOT performed in a potentially
ill-conditioned raw cyclic/Krylov basis. Evaluate its bounded rotation blocks,
the scalar denominator and the inverse DAG. For rational input time `t` of bit length `L` and absolute target
error `epsilon`, standard certified elementary-function arithmetic uses a number
of bit operations polynomial in `n`, `L`, initial-data bit length, and
`log(1/epsilon)`. Argument reduction must retain `O(L+log n+log(1/epsilon))`
working bits; treating huge-time trigonometric calls as unit-cost would be wrong.
Stable inverse recursion then has bounded rounding-error accumulation. Rational
*exact* output of a general inverse remains a different task and can require
exponentially many bits; the earlier `y=(3,...,3)` example lies outside this
bounded invariant set and demonstrates that distinction.

## Comparison and boundary

An equally informed ordinary algorithm can acquire the same chart, recover its
flag, and use the **identical** inverse recursion and matrix exponential. Newton,
triangularization, formal-series inversion and Darboux recognition are real
comparators; no lower bound against them is proved. Explicit time-stepping of a
periodic orbit is not the strongest comparator, so its time-horizon dependence
does not establish a general speed separation.

This warning is now executable. `same_syntax_comparator.py` scans the **same raw
DAG**, with no source syntax hidden, for literal `x_i+x_j^2` subgraphs. The
benchmark retains its constructor's chart subgraphs. Ordinary pattern/CSE
recognition extracts them, fits the projective generator, checks it using fresh
PIT, and invokes the same classical flag decoder. Its chart and matrix exactly
match the independently replayed normalized compiler outputs in all four saved
dimensions. Thus this benchmark provides **no evidence of algorithmic superiority**
over equally informed conventional symbolic recognition. Its inverse-degree
obstruction and uniform-conditioning construction are still valid capabilities.

What this closes is the claimed capability obstruction: even when inverse degree
is exponential, the complete raw-acquired decoder can be compact, globally
nonsingular in time on a known set, and well conditioned there. What remains open
is independent scientific application and a matched advantage over strong
symbolic methods. The classical strong-nilpotence ingredient is due to
[van den Essen and Hubbers](https://www.cs.ru.nl/E.Hubbers/pubs/strnil.pdf); it is
not new representation theory.

## Current executable receipts (not asymptotic timings)

`quadratic_circuit_results.json` retains the raw DAG/roots, acquired chart and
generator, normalized generator, phase timings and soundness bound. The recorded
`n=16` run starts from a 493-node raw circuit, uses 153 interpolation nodes, and
acquires 17 projective coordinates. Source-plus-divergence construction allocates
3,806 nodes. The returned inverse of the acquired, unnormalized chart has 226
reachable nodes and 896 total allocated nodes; its degree is 32,768. Normalizing
the chart before numerical evolution removes the affine-output overhead.
Raw-circuit point-evaluation integers peaked at 579 bits in one recorded run;
this is not a whole-program memory or bitgrowth measurement. Timings are recorded
separately and do not constitute a matched speed comparison.

The core acquisitions are labeled Monte Carlo. A separate independent audit
`audit/quadratic_circuit_replay.json` now supplies exact coefficient replay of all
34 closure components, including n=16, plus the normalized chart and rotation
matrix checks. This is deterministic evidence for those saved examples, not a
general derandomization. `conditioned_flow_checks.py` consumes acquired artifacts,
not the hidden constructor, for supplemental arbitrary-time precision tests.
All-time nonsingularity and conditioning come from the proof above, not from
sampling finitely many trajectories.
