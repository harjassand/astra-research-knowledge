# Independent review: common-seed inverse-mass acquisition

## Verdict and frozen boundary

**Accepted at the mathematical and exact-code scope below.** I independently
reconstructed the all-count drift proof, the hard-family halving termination, the
stochastic moment passage, and the aggregate-coordinate obstruction. A separately
written raw-data receiver and acquisition replay passed the bound tests. This is
ordinary proof/code review, not formal proof-assistant verification or a hardened
hostile-input service. Finite tests supplement, rather than establish, the theorem.

The accepted main proof is `SEEDED_INVERSE_MASS_THEOREM.md`, SHA256
`4d694097659d13b1e6659e1fd16f0c2c090eaf6f276d7c5bc5a358930418353d`.
The frozen constructor is `seeded_inverse_mass.py`, SHA256
`599b2884be7eab68e5cfbf61fa9e9b70654e722a4d9b44e21a2b744b708c4e1f`.
The main demonstration is `hard_demo.json`, SHA256
`2f0e7a61a7d4423c0459660dfc94e5c93dd6a7070fecb65b829262fde8ef6028`.
The exact package-relative allowlist, including all sources, tests, outputs,
mechanism notes, frozen copies, and this receipt, is
`independent_audit/AUDIT_MANIFEST.json`; it excludes itself and caches.

The initially supplied proof had SHA256
`d07ffcb415160903ca28581eb1bf9add4c7ed3849e8e5a14dc5959816fbd78db`.
Its sole subsequent change explicitly restricts the exact acquisition algorithm to
positive rational rate input. A byte-identical reconstruction of that initial proof
is retained as `independent_audit/original_theorem_d07ffcb4.md`; the final proof and
code are separately frozen. No constructor or main-result bytes changed during this
review. README/comparator material has its own manifest binding.

## What is established, and what is not

For the raw reversible family

```
0 <-> A
2A+B <-> A+B+C
2A+C <-> A+2B
A+B+C <-> A+2C
```

the proof gives positive recurrence of every closed communicating class and every
finite exponential total-count moment of every stationary distribution, for all
positive real rates. Exact numerical acquisition is implemented for positive
rational rates and rational `t>1`. The structural receiver recognizes this family
from raw reactions and uses the proved all-rate theorem without doing numerical
profile acquisition.

The broader generic implementation is only a sufficient profile finder for its
stated common-seed, unary/binary-stripped architecture. A profile at one base `t`
proves that base's moment, recurrence, and smaller exponential moments. It is **not**
automatically an all-exponent certificate. All-exponent scope follows separately
for the hard skeleton by halving termination, or for a valid zero-weight profile
because its head-compatibility condition is absent for every `t>1`.

The generic search is exhaustive only over rational profiles in its own sufficient
certificate family if run without a cap. A capped failure is UNKNOWN. The opposing
pure-ray example has no real inverse-linear profile of this form; that is a complete
obstruction to this profile family, not a negative stability theorem. No general
weak-reversibility or general seeded-lift conjecture is resolved here.

## Proof joins checked independently

### Exact seed stripping, extinction, and the first layer

All internal source and target complexes retain A. On `A>=1`, writing `r=A-1`,
`(A)_(u_A+1)=A(A-1)_(u_A)` gives the exact internal generator `A Q(r,B)`.
This identity does not include immigration or death. The seeded region is invariant
under internal jumps, but not under the actual death channel. At `A=0` all internals
are disabled. Both facts are used explicitly, not replaced by a token-lifetime or
stationary-fiber premise.

For `R=A+w dot B`, both endpoints of every enabled internal jump satisfy `R,R'>=1`.
The bound `R/ell<=R'<=ell R`, with `ell=1+max|Delta R|`, is valid even when `ell>2`.
The positive and negative increments must be bounded differently. The receiver
reconstructs exactly

```
rho(d)=d/ell (d>=0),   rho(d)=ell*d (d<0),
L_int h <= -c A Psi/R^2,   h=1+c/R.
```

Aggregating by stripped source is essential: no reaction's favorable coefficient
is counted twice, and negative mixed satellite coefficients are not discarded.
With the acquired pure coefficients `u_j>0` and nonnegative mixed coefficients,
the ordinary square completion gives

```
Psi >= Q/2-K A^2,       Q=sum u_j B_j^2,
L_int h/h <= c K A-c A Q/[2(1+c)R^2].
```

The `K1` unary term and `K2` seed-containing binary term are both included. Independent
checks cover a nonzero `K1`, an `ell=3` zero-weight profile, and four species.

The patched value `h0=2t(1+c)` on the entire extinction face makes its exact quotient
at most `-lambda/2`. At `A=1`, death goes to this patch: its quotient is bounded by
`mu(1+2c)<=3mu`, not treated as an ordinary inverse-mass decrement. For `A>=2`, the
death correction is bounded by `mu`. Immigration retains its positive upper bound
`lambda(t-1)`. These yield the stated global positive-A inequality

```
LW/W <= C-(3D/4)A-c A Q/[2(1+c)R^2].
```

### Head compatibility and finite box

For `S=sum w_j^2/u_j>0`, Cauchy-Schwarz and
`Q>=9 A_cut^2/S` give `Q/R^2>=1/(2S)`. The required inequality
`c/[4(1+c)S]>=C+zeta` is therefore sufficient. It is not optional: the accepted
`t=2` weights fail this exact condition when reused at `t=100`, while independently
acquired smaller weights pass there.

For `S=0`, every weight vanishes and `R=A`; the separately stated quadratic cutoff
is sufficient. Exact ceilings and integer square roots produce the finite exception
box. The entire infinite `A=0` face is outside that box and already has negative
drift. The declared box size, `N_max`, and factored Foster constant follow directly;
no box enumeration or undisclosed finite maximization is needed.

### Acquired hard-family halving

For `(w_B,w_C)=(eta,0)` and
`eta<=min(1/4,beta1/(4alpha3))`, direct source aggregation gives `ell=2`, positive
`u_B=beta2(1-2eta)/2`, positive `u_C=beta3 eta/2`, and nonnegative mixed coefficient.
The proof's `Kbar` satisfies `eta K<=Kbar`, including the singular `u_C` term.
Thus `c>=c0 eta` and the head strength is at least `c0 umin/(8eta)`. It diverges as
eta halves, while `C+zeta` is fixed at each requested base. This proves termination
without supplying a successful weight to the compiler.

The sufficient halving bound, actual rejected trials, accepted trial, source-term
evaluations, and retained-record bit accounting were independently reconstructed.
At the non-complex-balanced main fixture the actual count is nine profiles versus
eleven sufficient trials. The qualitative structural path was also guarded against
calling either implementation's numerical routines, including at rates `10^100`
and `10^-100`.

### Nonexplosion, recurrence, and stationary moments

The simple ordinary nonexplosion comparison is retained: only constant-rate
immigration increases N, so `N(s)<=N(0)+Pois(lambda s)` pathwise. Bounded count
sublevels have finitely many states and bounded rates, despite cubic channels.

On finite time intervals, this same domination integrates both W and a polynomial
in N times W. Stopped Dynkin identities therefore pass to the full semigroup without
assuming a stationary exponential moment. The integrated geometric drift bound
gives tight occupation averages and, by the countable nonexplosive invariant-measure
argument and Fatou, a stationary law with the stated W moment on each closed
irreducible class. This establishes positive recurrence.

Weak reversibility closes state classes by following a complex return path with
the fixed nonnegative surplus retained. Distinct A-only and satellite classes are
not conflated. The uniform moment constant applies to each class and hence stationary
mixtures; the finite-sublevel argument in the proof also bounds the number of classes.
All-exponent conclusions come from these exact generator bounds and all-t acquisition,
not from a generic fluid-stability theorem.

## Representation obstruction and ordinary comparators

The copied independent `SEEDED_MEDIATED_AGGREGATE_NO_GO.md` proves more than failure
of a separable exponential ansatz: every positive normlike function of `(A,N)` fails
one-step geometric Foster on one closed positive-satellite class. Eliminating the
pure-C `A=0,1,2` layers forces a contraction for the sequence `F(1,n)`, contradicting
normlikeness. The proof checks the actual last-seed death and fast `A=2` loss. The
finite reversible paths connect all compared pure-C rays within one class; 15 exact
generator identities and 38 enabled forward/reverse path edges supplement that
ordinary argument. No assertion about all additive, sampled-time, excursion,
history-dependent, or composition-sensitive methods follows.

The simpler seeded star already admits the ordinary service-only correction
`1+c/A`, with an extinction patch. Its infinite extinction face has constant negative
quotient, not negative-linear-in-N quotient; the proof keeps this distinction.
Its A-neutral conservative remainder can have higher order because it is invisible
to that correction, although the generic parser here deliberately has narrower
syntax. The copied baseline also retains the compatible product-Poisson control
and the precise incompatible neutral-pair condition. It does not exclude every
non-Poisson factorized representation.

For the hard family, all rates equal to one are complex balanced at unit
concentrations, so ordinary Poisson product form proves stability there even while
the `(A,N)` no-go remains true. Representation loss alone is not recurrence novelty.
The executed `alpha3=2`, other-rates-one fixture instead violates the exact
complex-balance equations, as the main proof demonstrates.

I checked the separate template-comparison note. Positive linear mass and its
positive exponential have positive immigration drift on the extinction ray. The
standard unweighted chemical entropy has positive eventual drift at `(n,n,n)`:
the cubic conservative second difference contributes order `n^2`, exceeding the
death term of order `n log n`. The fixed-reference-vector extension uses integer
approximations to the ray and controls the signed first-order error; it is sound.
Four exact rational lower-bound controls replay and were independently recomputed.
These exclusions do not extend to weighted, nonsmooth, repaired, or sampled-time
entropy functions.

## Independent receiving and executed controls

`independent_audit/independent_seeded_receiver.py` does not call the candidate's
recognizer, derivation, or search. It independently checks the raw exact domain,
normalization, open coordinate, stripped architecture, full graph reversibility,
source coefficients, all mathematical fields, and compact constants. Its graph-work
count is obtained from separate reachability sets. Hard and generic search audit
routines additionally reconstruct the tested sequence and work metadata. In
contrast, the author's public `receive` is correctly described as semantic
recomputation using the constructor, not an independent search audit.

The final independent driver passed:

* **5,093 ordinary states**, **378 boundary/huge states** (including counts `10^50`),
  and **539 separately expanded small-W generator checks**, across nine cases;
* **30 semantic corruptions**, **18 halving/accounting corruptions**, and **six
  qualitative structural corruptions**, all rejected;
* all six coordinate permutations with raw ordering changes, positive rate splitting,
  and a valid null reaction;
* exact capped hard and generic acquisition replays; preservation of the separate
  qualitative all-t result under a quantitative UNKNOWN;
* the fixed-weight `t=100` negative control, `c=1`, initial-trial success, heterogeneous
  rates, four species, nonzero unary penalty, and zero-weight/ell-three branches;
* six invalid independent-audit bases rejected before bound preprocessing: exact
  `1,0,1/2,-1`, float `1.0`, and Boolean `True`.

The last group records a reviewer-code correction: the parent found that my initial
`hard_audit` lacked an early `t>1` check and could loop forever on `t=1` while acquiring
the sufficient bound. The guard was added before that loop and the full independent
driver reran successfully. The candidate already checked this domain; no accepted
mathematical or constructor result changed. The manifest binds only the repaired
independent receiver and its final output.

The author's main demonstration, main exercise output, and entropy output replayed
byte-identically. The main exercise reports 6,366 ordinary and 518 targeted states,
15 semantic corruptions and 15 invalid-input controls; these are not silently added
to the independent counts as disjoint evidence. The three copied independent
mechanism scripts also replayed byte-identically, and their outputs are retained
separately; their earlier narrower
inverse constants need not coincide with the generic compiler constants.

One metadata nuance is preserved, not papered over: in capped `generic_search`,
`last_denominator` is the **cap-check cursor**, not necessarily the last denominator
actually tested. After the four denominator-one profiles in two dimensions, a cap
of four reports cursor two. Independent replay checks that behavior. Actual profile
and source-evaluation counts remain exact; the README now states this semantics.

## Cost, source, and receiving limits

The main `t=2` certificate has an implicit exception box of **3,462,766,534,656**
states. Its Foster constant contains `2^3692711`. Neither the box nor that rational
power was expanded. The exact prefactor/base/exponent expression is sufficient for
the mathematical certificate, not a claim of useful numerical sharpness.

Profile caps do not cap raw validation, graph work, bound preprocessing, rational
bit arithmetic, output size, or memory. The retained-record bit peak does not bound
every transient arithmetic operand. The qualitative receiver avoids numerical
profile work by applying a reusable proved structural theorem, not a stationary-law
oracle. The independent audit uses Python assertions and standard-library exact
arithmetic; run it under ordinary Python, not `python -O`.

No priority claim is established. Conventional Foster, conservation, inverse
corrections, exact mass-action algebra, graph reachability, and product-form results
receive ordinary credit. This receipt validates the displayed proof directly; it
does not turn a literature abstract or an unavailable source into a theorem premise.
The announced all-two-species result remains announced work in preparation in the
retained source scope, not an inspected manuscript. No new external transfer was
needed for this audit. Historically denied/gated transfers and the optional
eScholarship HTTP429 source were not retried; the latter remains uncompleted and
irrelevant to the proof dependency.

Earlier accepted packages and original mechanism files are unchanged. Their copies
in this package are byte-identical. This review ends at the frozen seeded-inverse
boundary and conveys no acceptance of any future polynomial, nonsmooth, or
excursion-based extension.

## Local replay commands

From this package directory, with ordinary Python 3:

```sh
python seeded_inverse_mass.py > producer-workspace/seeded_demo.json
cmp hard_demo.json producer-workspace/seeded_demo.json
python exercise_seeded.py > producer-workspace/seeded_exercise.json
cmp exercise_results.json producer-workspace/seeded_exercise.json
python entropy_exact_controls.py > producer-workspace/seeded_entropy.json
cmp entropy_exact_controls.json producer-workspace/seeded_entropy.json
python independent_audit/run_independent_audit.py > producer-workspace/seeded_independent.json
cmp independent_audit/independent_results.json producer-workspace/seeded_independent.json
python independent_audit/mechanism/exact_seeded_checks.py > producer-workspace/seeded_mechanism.json
cmp independent_audit/mechanism/exact_seeded_results.json producer-workspace/seeded_mechanism.json
python independent_audit/mechanism/extra_inverse_and_poisson_controls.py > producer-workspace/seeded_extra.json
cmp independent_audit/mechanism/extra_inverse_and_poisson_results.json producer-workspace/seeded_extra.json
python independent_audit/mechanism/generic_inverse_controls.py > producer-workspace/seeded_generic.json
cmp independent_audit/mechanism/generic_inverse_results.json producer-workspace/seeded_generic.json
```
