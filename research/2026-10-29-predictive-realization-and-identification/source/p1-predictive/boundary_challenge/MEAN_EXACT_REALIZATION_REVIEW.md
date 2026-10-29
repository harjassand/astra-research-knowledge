# Independent review: a positive mean-exact realization with at most twice the ports

29 October 2026, Brisbane. Root's construction, independently proved and
challenged here. The state lower bound and directional macro-source
extension below were developed during this review. Scope: finite reversible
continuous-time chains, exact feasible records, supplied numerical controls.

## 1. The positive realization works

Use the notation and closed-module contract in
`PASSIVE_EQUIVALENCE_AND_MEMORY.md`. There are m retained ports, with
boundary masses w_B>0, Schur Laplacian S, effective load b, and equilibrium
residual c. Set

```
v=b-w_B, V=sum(v).
```

For a feasible closed record, v>=0 because `v=H^T w_I` and H>=0.
Since H1=1, V is exactly the total eliminated mass. In the finite positive
model, `c=0` if and only if `V=0`: a nonempty interior of positive weights
has `w_I^T L_II^-1 w_I>0`. Thus no finite positive feasible record has
V>0,c=0 or V=0,c>0.

If V=c=0, the original record is realised by the m-port Laplacian S and
masses w_B, with no added states. Otherwise put `gamma=V/c>0`.
Retain boundary masses w_B and place direct conductance `-S_ij` between
ports i,j wherever it is positive. For each i with v_i>0, add a private
leaf of mass v_i and conductance `gamma v_i` to port i.

The result has at most 2m states, symmetric nonnegative conductances,
positive masses, and a conventional reversible generator. Every leaf
has the same exit rate gamma. It is irreducible when S connects its ports
(with the usual one-port interpretation).

The interior matrix is diagonal with entries gamma v_i. Each leaf's
harmonic boundary row is the unit vector of its owner port. Consequently

```
S_hat=S,
b_hat=w_B+v=b,
c_hat=sum_i v_i^2/(gamma v_i)=V/gamma=c,
w_hat_B=w_B,
mu_hat=sum(w_B)+V=sum(b)=mu.                            (R1)
```

More explicitly its boundary memory function is

```
K_hat(s)=S+s diag(w_B)+[gamma s/(gamma+s)] diag(v).
```

Only the selected zero-frequency contractions agree with the original
K(s). The common gamma is a leaf-exit clock, not a claim that the full
replacement has only one relaxation eigenvalue or the original spectrum.

This proves exact preservation of the whole declared mean query family:
conductance-calibrated passive exterior attachments, fixed native boundary
killing hazards compiled as `w_i kappa_i`, all boundary target subsets,
and the whole-module absorbing-union constructions below. The full
eliminated memory function, the native total port-exit rates, the raw
excursion law and arbitrary microscopic initial preparations need not
agree.

This is also a feasibility characterization for records of unrestricted
finite reversible closed modules: a connected graph Laplacian S, w_B>0,
v=b-w_B>=0 and either V=c=0 or V,c>0 suffice, because the construction
realises them. It is not a characterization inside narrower fixed-graph,
binary heat-bath, bounded-clock, geometrically local, or equipment classes.

## 2. The factor of two is worst-case necessary

Consider ANY positive reversible realization of the same record, with n
hidden states, interior block G and coupling J=L_IB. Its hidden Gram
matrix is

```
C=J^T G^-1 J,   rank(C)<=n.
```

The vector v is `-J^T G^-1 w_I`, and c is `w_I^T G^-1 w_I`.
Cauchy--Schwarz in the G^-1 inner product gives

```
C_ii >= v_i^2/c.                                      (R2)
```

Since -J>=0 and G^-1>=0, C is entrywise nonnegative. For i!=j,

```
-S_ij = (direct boundary conductance)_ij+C_ij >= C_ij.  (R3)
```

Therefore if

```
v_i^2/c > sum_{j!=i} (-S_ij)  for every i,             (R4)
```

C is strictly diagonally dominant and hence nonsingular. Thus rank(C)=m
and every compatible realization requires n>=m hidden states. A proof of
nonsingularity needs no spectral premise: if Cx=0, choose |x_i| maximal;
then `C_ii |x_i| <= sum_{j!=i} C_ij |x_j| < C_ii |x_i|` unless x=0.

For an explicit connected family, take `w_B=1`, `v=1`, `c=m`, and for
m>=2 let every edge of S have conductance

```
epsilon=1/[2m(m-1)].
```

The row sum is 1/(2m), smaller than v_i^2/c=1/m. The root's private-leaf
construction has gamma=1 and exactly 2m states. Equations (R2)--(R4)
show that NO positive reversible realization of this same retained
record has fewer states, even though this family is connected. At m=1,
v,c>0 itself requires one hidden state, so two total states are necessary.

This is a state-count lower bound for an exact, labelled-port, calibrated
realization class. It is not a computational lower bound, a memory-bit
bound, or a statement about non-Markovian/signed/nonreversible realizations.

For two ports the obstruction is particularly transparent. A single
hidden leaf has mass V and needs total conductance V^2/c, with incident
conductances `V v_i/c`. It induces boundary conductance `v_1 v_2/c`.
If `-S_12<v_1 v_2/c`, nonnegative direct conductances cannot cancel it.

## 3. Actual macroscopic transition means, with a specified source union

Keep the modular geometry of the preceding note: every endpoint of every
cross-module edge is a retained port. Ground a nonempty union A of target
modules, and assemble the live boundary matrix K_A and source b_live.
The port Poisson field is

```
h_ports=K_A^-1 b_live.
```

For each surviving module j, eliminating its interior gives the exact
weighted contribution of that entire module to the Poisson field:

```
sum_{x in C_j} w_x h_x = c_j+b_j^T h_ports|_{B_j}.      (R5)
```

Thus for ANY nonempty union C of source modules disjoint from A,

```
E_{w(.|C)} tau_A
 = [sum_{j in C} c_j+sum_{j in C} b_j^T h_ports|_{B_j}]
   /sum_{j in C} mu_j.                                (R6)
```

Each replacement preserves (R5), not only the sum over all live modules.
It therefore preserves means between arbitrary disjoint whole-region
source/target unions. Arbitrary mixtures of equilibrium preparations
inside individual modules are preserved as well, by linearity. Here
equilibrium INSIDE a module means the native stationary weights restricted
and normalized there, not an assumed first-entrance distribution.

This closes the macroscopic initial-law detail left implicit by merely
conditioning outside the target. It still requires actual preparation of
the specified source ensemble for an operational experiment. Arbitrary
microscopic sources, source-biased conditional laws, history-dependent
switches or modifications inside eliminated regions are not covered.

## 4. Information, precision and implementation costs remain separate

The realization is an exact compiler FROM an already valid record. It
neither observes nor estimates that record. A finite confidence set must
be propagated through the requested mean or a proved stability bound;
plugging a point estimate into (R1) is not itself a confidence argument.
In particular v=b-w_B can be poorly resolved by subtraction, and gamma
can be highly sensitive when c is uncertain. Infeasible input boxes are
not made valid by silently clipping negative v or setting c to zero.

After the record is known, the construction needs O(m^2) scalar storage
and arithmetic to copy possibly dense S, at most m private leaves, and
ordinary rational operations to form gamma and the rates. Direct edges
can be dense even though the state count is at most 2m. Rate magnitudes,
rate precision and clock implementation are not bounded by the state
count. A binary heat-bath or spatially local source need not have an
emulator in the same physical class. No physical emulator was operated.

Computing a mean from the reduced formula is generally preferable to
simulating a long trajectory of the realization. The state theorem does
not assert faster Monte Carlo, a direct-solve speedup, or cheap acquisition.

## 5. Prior art and what the construction adds

The following primary sources were read for this comparison:

- D. J. Sharpe and D. J. Wales, *Numerical analysis of first-passage
  processes in finite Markov chains exhibiting metastability*, PRE 104,
  015301 (2021), equations (6)--(8) and their surrounding explanation.
  Their graph transformation renormalizes branching probabilities and
  mean waiting times while preserving first-passage means; the paper
  also computes higher first-passage statistics and handles macrostates.
  https://api.repository.cam.ac.uk/server/api/core/bitstreams/92bd7a0f-0d44-4b86-9447-c3c34b3bd10c/content
- R. S. MacKay and J. D. Robinson, *Aggregation of Markov flows I: theory*
  (2018), sections 2--4 and 6. Exact local elimination and hierarchical
  aggregation of mean/stationary flow information are established;
  their aggregation represents entrance-edge states and does not preserve
  all temporal dynamics. (The source spells out that lost dynamics matter.)
  https://wrap.warwick.ac.uk/id/eprint/97255/8/WRAP-aggregation-Markov-flows-I-theory-MacKay-2018.pdf
- The current 2026 preprint by D. Aristoff, R. J. Webber and D. M.
  Zuckerman, *Markov state models revisited: Principles and algorithms
  for unbiased observables*, arXiv:2607.19452v2, was retrieved at the
  primary abstract level. It uses equilibrium and source-sink matrices
  matched to the observable and explicitly requires properly weighted
  data. Full-text retrieval was unavailable here, so no claim of detailed
  non-overlap with that preprint is made.
  https://arxiv.org/abs/2607.19452

These results preclude claiming that preserving means while forgetting
dynamics, exact aggregation, or mean-preserving state elimination is new.
The specific established construction here is an explicit positive
CTMC realization with retained boundary masses, one common leaf clock,
at most twice the port count, and the stated universal passive/context
mean scope, together with a matching worst-case state-count obstruction.
The targeted literature read did not establish historical priority for
that exact realization theorem; novelty remains open. The conventional
methods can use this realization or the smaller Schur record directly.

## 6. Independent executable check

`check_mean_exact_realization.py` builds original supplied graphs and the
replacement independently, compares their exact records and actual
killed solves, checks native hazards and passive attachments, compiles
all macroscopic source/target unions of a four-module example, and checks
the strict dominance inequalities of the lower-bound family. It uses
`fractions.Fraction` through the small matrix implementation in the
preceding control, not a floating spectral test. Its checks establish
their finite scope; the ordinary arguments above establish the theorem.
