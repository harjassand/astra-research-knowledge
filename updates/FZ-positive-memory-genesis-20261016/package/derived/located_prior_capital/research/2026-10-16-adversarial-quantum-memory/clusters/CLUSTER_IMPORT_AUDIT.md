# Independent cluster-import audit

Audit date: 16 October 2026, Australia/Brisbane. Worker: Sol 3, `clusters`.

## Verdict and boundary

I found no mathematical failure in the infinite-volume probability import as
written for the native binary coarse process. The exact finite-coordinate map
is an attractive eroder, and the literal local primitive bad flags give the
strong spatial dependence hypothesis needed for product domination. Independent
primitive slabs allow a joint coupling of the entire future trajectory. The
comparison from upper-invariant initialization to the cold all-one trajectory
is in the correct direction for zero-cluster events.

This is a **conditional reconstruction with a source-retrieval boundary**, not
an independent proof of the imported LSS theorem. Hartarsky--Toninelli (HT)
arXiv:2212.08437v2 was freshly retrieved in full and its relevant PDF pages were
visually inspected. The original LSS abstract was read in its reproduction in
Liggett's complete bibliography. The original LSS theorem-page PDF was not
retrieved: the official journal endpoints return a security challenge, and the
historical author DVI link returns 404. I therefore state the precise standard
LSS premise explicitly rather than claiming that its original theorem pages
were verified. No older Astra `source_audit` document was used as validation.

The result reconstructed here is an anchored, infinite-volume space-time
component bound for the native coarse process, and consequently for the
sampled occupied-cell set dominated by it. The stopped finite-torus replay,
whole-slab transfer, homology argument, and quantum-channel argument require
their separate deterministic adapters. The two probability imports alone do
not establish those adapters.

## Inputs independently read

- `/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-autonomous-frontier-v2/THEOREM_AND_PROOF.md`, in full.
- `/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-autonomous-frontier-v2/sweep/MONOTONE_ENVELOPE.md`, in full.
- The freshly retrieved versioned HT sources identified in `PRIMARY_STATEMENTS.md` and `SOURCE_RECEIPTS.json`.

The preexisting cached HT PDF has the same manuscript date, 11 March 2024,
but a different PDF hash and build metadata from the arXiv v2 PDF. The argument
below uses the freshly downloaded arXiv v2 statement, not identity of those
files.

## 1. Exact deterministic map

Write `h(z)=z_1+z_2+z_3+z_4` and, for fixed positive integers `s,R` with
`R>=s+5`, define

```
A_i = {w in Z^4 : ||w||_infty <= R, w_i >= 0}, i=1,...,4,
A_5 = {w in Z^4 : ||w||_infty <= R, h(w) <= -s},
phi(x) = OR_(j=1,...,5) AND_(w in A_j) x_w.
Phi(x)_z = phi((x_(z+w))_(w in Z^4)).
```

All five sets are finite and nonempty. `phi(0)=0` and `phi(1)=1`.
Every AND and OR is nondecreasing in every argument. Consequently `Phi`
preserves the coordinatewise order and is a translation-invariant local
deterministic cellular automaton in precisely HT's Section 2.4 class.

There is no forbidden self-input: `0` belongs to `A_1,...,A_4`, while `0`
does not belong to `A_5`. HT's CA definition allows arbitrary finite input
sets, including the origin. The exclusion of the origin in HT's separate
definition of KCM update families in Section 2.1 is not a restriction on
the CA corollary. In particular, invoking the CA corollary does not require
identifying this map as an origin-free KCM constraint.

There is also no hypothesis that every coordinate in a nominated neighborhood
have positive influence, or that the origin have positive influence. Extra
ignored coordinates can be omitted from a support, and a finite DNF need
not be presented in minimal form. Neither operation changes the map or the
following direct eroder proof. The actual map is nonconstant, so no constant-map
edge case is being used.

### Eroder proof, without a convex-hull import

Let `Z_n={z:Phi^n(x)_z=0}` when `Z_0` is finite. A zero at site `z` at the
next time means that every one of the five AND terms fails. Thus, for every
`j`, there is some `w_j in A_j` with `z+w_j in Z_n`.

If `Z_n` is finite, all possible next zeros are contained in

```
union_(w in A_1) (Z_n-w),
```

which is finite. In particular, no finite-island argument silently assumes
that subsequent zero sets remain finite.

For a nonempty `Z_n`, set

```
M_i(n)=max_(z in Z_n) z_i,
m(n)=min_(z in Z_n) h(z).
```

The failed `i`th coordinate term supplies a zero `y=z+w_i` with `w_i,i>=0`.
Hence `z_i<=y_i<=M_i(n)`, and therefore

```
M_i(n+1) <= M_i(n), i=1,...,4.
```

The failed fifth term supplies a zero `y=z+w_5` with `h(w_5)<=-s`. Hence

```
h(z)=h(y)-h(w_5)>=m(n)+s,
m(n+1)>=m(n)+s.
```

If zeros survive at time `n`, they therefore satisfy

```
m(0)+ns <= h(z) <= sum_i M_i(0).
```

They cannot survive once `ns>sum_i M_i(0)-m(0)`. This proves erosion in
at most `1+floor((sum_i M_i(0)-m(0))/s)` rounds. If the initial infinity
diameter is `D`, then `sum_i M_i(0)-m(0)<=4D`, giving a linear-diameter
bound. If a zero set becomes empty earlier, `phi(1)=1` keeps it empty.

The shift convention in the displayed definition is `z+w`, exactly the
translated forcing set used by the block comparison. All extrema inequalities
above were written for this convention. A simultaneous spatial reflection
would reverse the convenient extrema, but would not invalidate erosion.
There is no time-dependent shift of the rule or unmentioned self-retention
rule in this proof.

## 2. The actual dependence needed for LSS

Let `P_n` be the collection of all primitive vertex-clock increments and
per-face sector-birth increments in the half-open slab
`[n Delta,(n+1) Delta)`. For one sector, these are independent Poisson
processes across their spatial primitive indices, and `P_n` and `P_m` are
independent whenever `n!=m`. Exact clock times at slab boundaries form a
null event; a fixed half-open convention resolves it.

For a target coarse cell `z`, the proposed bad flag is a measurable function
of the restriction of `P_n` to a fixed guard of coarse radius at most
`q=R+3`. It is the union of a birth flag, a slow-clearance flag for a
freshly reset deterministic halfspace forcing configuration, and a long
ordered-clock-chain flag. In particular, it is not a function of the actual
input state or of clearance times carried forward from a previous slab.

The guard claim has a direct geometric check. For clearance, all predecessor
vertices lie at fine directed depth at most `(s+4)b`, which is below the fixed
guard reach. For a chain of `m=floor(Rb/2)` events, each backward dependency
step travels fine `l_1` distance at most two, so its first `m` clock locations
remain within distance `2m<=Rb` of the target. The extra guard cells cover
face bases whose corners meet the birth guard. Repeated visits to a vertex
are permitted; they are distinct chronologically ordered marks, because the
microscopic update reads the old state for all outputs.

This is stronger than pairwise independence of distant bad flags. If
`||z-w||_infty>2q`, the primitive support of `B_(z,n)` is disjoint from
that of `B_(w,n)`. Moreover, the support of `B_(z,n)` is disjoint from the
**union** of the supports of all such far flags. Therefore

```
B_(z,n) is independent of
sigma(B_(w,n): ||z-w||_infty > 2q).
```

Define a countable dependency graph on `Z^4` by joining distinct sites with
infinity distance at most `2q`. Its degree is at most `(4q+1)^4-1`, a fixed
number independent of `b`, lattice size, storage time, and `kappa`.

For `H_(z,n)=1-B_(z,n)` and a uniform marginal bound `P(B_(z,n)=1)<=delta`,
the displayed independence implies the stronger neighborhood-conditional
statement

```
P(H_(z,n)=1 | sigma(H_(w,n): w outside N[z]))
  =P(H_(z,n)=1) >= 1-delta, almost surely.
```

Here `N[z]` is the closed graph neighborhood. This is the bounded-degree
graph premise in the original LSS abstract. The precise external premise
used below is: for each fixed bounded dependency degree and each target
`rho<1`, a sufficiently small `delta>0` makes every such field dominate
an iid Bernoulli field of density `rho`. Equivalently, the bad field is
dominated by iid Bernoulli deaths of any prescribed positive small density.
The original theorem's sharp constants and one-dimensional refinements are
not used.

One must apply this to `H` or `B`, not to the native evolving `theta` field.
The latter has long correlations caused by its ancestry. Product domination
of an upper-invariant CA state is a different question; it is not needed here.

### Whole future trajectory coupling

Fix an iid death parameter `p_*` in the HT regime and choose `delta_*` from
LSS with target healthy density `1-p_*`. LSS supplies a joint law `Q` of
one pair `(B,Xi)` such that the first marginal is the one-slab bad-field law,
the second is iid Bernoulli(`p_*`) on `Z^4`, and `B<=Xi` everywhere almost
surely.

Take independent copies of this joint law for all slabs. Then the entire
`Xi_(z,n)` collection is iid in both space and time, and `B_(z,n)<=Xi_(z,n)`
holds for every site and slab simultaneously. To retain the original
primitive Poisson fields as well, disintegrate `Q(dXi|B)` and sample the
kernel with independent auxiliary randomness in each slab, conditional only
on the native `B_n` produced by that slab. This preserves the native
primitive law, the joint coupling inequality, and slab independence.

There is no need for `B_(z,n)` to be independent of nearby bad flags in
its slab. There is no need for the two CSS sectors to be independent: their
probability bounds can be combined by a union bound even though Y faults
correlate them.

## 3. A joint monotone comparison, including initialization

Write the native coarse process and an iid-death comparator as

```
theta_z(0)=omega_z(0)=1,
theta_z(n+1)=(1-B_(z,n)) phi(theta_n shifted by z),
omega_z(n+1)=(1-Xi_(z,n)) phi(omega_n shifted by z).
```

If `theta_n>=omega_n`, monotonicity and `B<=Xi` give

```
(1-B)phi(theta_n) >= (1-Xi)phi(omega_n)
```

at every site. Induction proves `theta>=omega` for the whole path.

For the second comparison, sample `bar_omega(0)` from the upper invariant
measure of the **same** map and the **same** death parameter `p_*`, independently
of all future death marks. Drive it using that one already chosen future
field `Xi`. Since `omega(0)=1>=bar_omega(0)`, attractiveness gives

```
theta_z(n) >= omega_z(n) >= bar_omega_z(n)
```

for every `z` and `n>=0` on a single joint probability space.

This establishes a path comparison, not merely separate single-time
stochastic inequalities. Its direction is essential: `bar_omega` may have
more zeros than the cold comparator. Thus every zero space-time point of
`theta` is a zero space-time point of `bar_omega`, and every connected zero
component of `theta` is contained in one of `bar_omega` under the same
connectivity rule.

If HT's stationary trajectory is interpreted two-sided in time, the same
coupling is available. Introduce iid death marks at all negative integer
times, start from all ones at time `-m`, and take the coordinatewise limit
as `m` increases. Monotonicity makes these limits exist, finite dependence
of each update passes the recursion to the limit, and time-translation
invariance gives the upper-invariant trajectory. Its time-zero state is a
function of past deaths, so it is independent of the future field. The
nonnegative-time cold zero set remains a subset of this two-sided stationary
zero set. Enlarging the latter with its negative-time points can only enlarge
components.

This use of upper-invariant initialization is also consistent with HT's own
all-one comparison in Section 10, equation (10.6), PDF page 31. It does not
license the same bound from an arbitrary initially defective configuration.

## 4. The exact infinite-volume consequence

Fix **any** positive finite connectivity radius `k` before choosing the
noise threshold. Use Euclidean distance in `Z^4 x Z`, as HT does. Let
`C_theta(z,n;k)` be the maximal zero component of `(z,n)` in the nonnegative
native trajectory, with the empty-set convention when the anchor is one.

Applying HT to the containing upper-invariant component gives constants
`c_HT>0,p_0>0`, depending on this fixed `phi,k`, such that, when
`0<p_*<=p_0` and the primitive marginal is at most the corresponding LSS
`delta_*`,

```
P(diam_2 C_theta(z,n;k) >= ell)
  <= p_*^(c_HT (ell+1))
  = exp(-a (ell+1)),
a = c_HT log(1/p_*) > 0.
```

The bound is uniform in the anchor time and location. For a finite set `V`
of possible insertion anchors, the probability of a component of diameter
at least `ell` meeting `V` is therefore at most

```
|V| exp(-a (ell+1)).
```

The block inequality `zeta_n>=theta_n` further gives the same component
bound for sampled infected coarse cells `{zeta=0}`. It is not an assertion
that continuum fine-lattice infections are themselves this CA.

### Metric and fixed-radius bookkeeping

HT's statement is for every fixed `k`, with the threshold and exponent
allowed to depend on `k`. It is not uniform for `k` growing with system
size. The proof's choice `k=4R+4` is fixed when `R` is fixed.

A forcing parent `(z+w,n)` of `(z,n+1)` is at Euclidean distance at most
`sqrt(4R^2+1)<2R+1`, so it is connected for `k=4R+4`. If coarse witness
cells are chosen within infinity distance `R` of adjacent fine cells, their
spatial separation is at most `2R+1` in each coordinate and their time
separation is at most one. Their Euclidean distance is at most
`sqrt(4(2R+1)^2+1)<4R+4`. Thus that value also covers this intended
adjacency conversion.

If any separate torus argument defines its `k`-edges as **all** pairs at
infinity distance at most `k`, an explicit norm conversion is still required
before applying HT: a safe Euclidean radius is `sqrt(5) k` in full five
dimensional space-time. Since it is another fixed radius, this is repairable
by choosing that radius before the death threshold. It must not be silently
identified with the same numerical Euclidean `k`.

## 5. Noncircular parameter order and microscopic flag checks

Fix `s=1`, `C>10 log(8)`, and then
`R>=max(6,ceil(280 e C)+10)`. This fixes `phi`, its finite support, the
desired connectivity radius, and the dependency graph. Choose `p_*` inside
the HT regime, then choose `delta_*` for LSS on that fixed graph. Only then
choose the fixed block side `b` large enough to make both

```
2 b^4 exp(((s+4)log(8)-C/2)b) <= delta_*/3,
b^4 2^(-floor(Rb/2)) <= delta_*/3.
```

The first exponent is negative by the choice of `C`; the second term also
decays exponentially in `b`. Both choices are possible. Neither changes
the CA, its connectivity radius, or the coarse dependency graph.

Set `Delta=Cb/kappa` and

```
sigma_0/kappa = delta_* / (18 C b ((2R+5)b+3)^4).
```

Then any sector fault rate `sigma<=sigma_0` makes the birth term at most
`delta_*/3`. The threshold is strictly positive and independent of `L,T`.
It need not be useful numerically. Applying the same fixed target `p_*`
for every `sigma` below this threshold makes the component constants
uniform over the whole allowed interval, including the zero-noise case.

For completeness, two potential hidden dependence problems in the flag
estimate have direct resolutions for the exact map. Permanent clearance
of a predecessor is determined by clocks at predecessor-or-lower sites;
it does not inspect the future clock process at the site now being cleared.
The residual own-clock wait after all predecessors clear is therefore a
fresh exponential variable. Processing the finite predecessor DAG in rank
order gives the standard independent last-passage residual representation.
An exponential-moment bound at parameter `kappa/2`, together with at most
four choices per directed step, yields the stated conservative `8^H`
factor and the slow term above.

For fast influence, an ordered sequence may revisit a clock location, but
Poisson factorial-moment counting still gives `(kappa Delta)^m/m!` for
the chronologically ordered distinct marks of a fixed spatial choice
sequence. At most 35 choices per dependency step yields the stated
`b^4(35 kappa Delta)^m/m!`. This counts terminal times anywhere in the
slab, not just a fixed terminal observation. The old-state convention
rules out using one mark repeatedly as an instantaneous chain through its
different outputs. These facts explain why the flags can be both local
and fresh; they do not add independence of the evolving physical state.

## 6. First failure search and final classification

The concrete attacks in `COUNTERMODELS.md` show that the conclusion fails
if one keeps only small marginals, only per-slab product domination without
fresh time slabs, arbitrary initial conditions, or all-time finite-torus
stationarity. They do not satisfy the exact assumptions of the proposal,
which explicitly avoid those weakenings.

No extra mathematical assumption was added to repair an observed
counterexample to the exact infinite-volume chain. The explicitly imported
premises remain (i) the bounded-neighborhood LSS density-to-one theorem,
and (ii) HT Corollary 9.5 for attractive eroders. The first has an original
full-text retrieval gap in this audit. The second was verified in its named
version. The finite-torus and quantum-memory conclusions remain conditional
on the other campaign workers' adapters, not on any stronger claim made here.
