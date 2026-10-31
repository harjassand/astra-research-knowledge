# Independent whole-proof audit: terminating fringe-compatible Dirichlet search

31 October 2026. Abstract count-process mathematics only.

## Verdict

**Accept the generalized shared-hub construction at the exact frozen versions
below**, including removal of the no-inactive-death guard, termination of the
unbudgeted finite compatibility search, nonexplosion, classwise positive
recurrence, and all finite exponential total-count moments. No substantive proof
or code gap was found after reconstructing the new activation, excess, and fringe
arguments. This acceptance is new: it is not inherited from the earlier narrower
phase-head theorem.

This is an independent internal review, not external refereeing, priority
clearance, an efficient algorithm, a general weak-reversibility theorem, or a
physical capability. Missing hub rows, hubs without direct death, nonlinear
service cores, and unclassified count-changing reactions remain outside scope.

## Frozen proof/code/result binding

* `GUARD_REMOVAL_THEOREM.md`:
  `e563c3bd8a1cb6d928ad85f7367c99a2d04f693ddef6fb134663e5ce7d073a52`.
* `phase_boundary_general.py`:
  `6c03436917dfbeb9c89f3e437b737578808289e1d64bb32c36d83b8dfdc4de4e`.
* `results.json`:
  `40fe2af7907337d11332254c15c5fbdeb91fddcec1e15d0c80be18e476721bfd`.

Frozen copies, independent verifier/challenges, full replay, and hashes are in
`independent_audit/`. Running the frozen main code reproduced the frozen results
**byte for byte**. The verifier subsequently used the frozen code, not a mutable
future source. The previously accepted package was preserved unchanged.

## 1. The revised single-particle calculation is the right one

Inactive t_i now measures absorption on H OR death, not guaranteed arrival at H.
The exact equation includes `-d_i t_i`. Strong connectivity of the monomolecular
core through zero guarantees that this finite killed chain is transient. With
v_i=L+t_i and common hub v_h=L,

    (Qv)_i=-1-d_i L<=-1

on inactive rows; the former hub inequality is unchanged. Thus allowing inactive
deaths does not invalidate the weighted core drift. The implementation and
independent verifier both charge these deaths in the first-hit matrix and in
single-particle departure rates.

All q_h still equal satellite weight T, so the exact star g-ratios and their
negative satellite-leading coefficients survive. The tail inequality is unchanged
except for its acquired numerical constants. Full raw-list recognition, complete
positive hub rows, direct hub deaths, strong core connectivity and neutrality of
every remaining reaction were rechecked, not assumed from the earlier package.

## 2. The uniform activation clock is acquired, not hypothesized

For a chosen raw immigration/conversion path with no pre-terminal hub, let
`a_i=sum_j k_ij+d_i`. For a new particle at i, the joint event of the prescribed
next conversion and holding time at most 1/a_i has probability

    (k_ij/a_i)(1-exp(-1)) >= k_ij/(2a_i).

Multiplying these exact rational lower bounds and summing their deadline bounds
gives p and D_path. Inactive death is included in a_i, so survival is not silently
conditioned for free. A direct hub immigration path has p=1 and D_path=0.

Preassign each immigrant an independent core lineage. The successful-lineage
arrival process is an independently thinned immigration process, of rate at
least lambda p. It is the ARRIVAL process that is Poisson; the argument does not
claim that delayed activation times themselves form the same process. The first
qualified immigrant reaches H within D_path after arrival, yielding

    E tau_H <= D_path+1/(lambda p).

Additional initial particles can only make first activation earlier in the
standalone monomolecular core. The core has no branching, only conversion, death
and constant-rate immigration, so this independent-particle representation is
valid. The clock is applied to that independently nonexplosive core. Before H,
stars are disabled and neutral reactions do not alter service counts. Thus no
full-network nonexplosion or fast stationary law is used circularly.

The independent verifier reconstructs the actual path, checks its initial
immigration edge, confirms every pre-terminal phase is inactive, and recomputes
all departure rates, probabilities, deadlines and the final bound from raw rates.
A tampered success probability is rejected.

## 3. Only positive Dirichlet excess needs control

For each finite service head F_R, the actual exit values h_0 occur in the
Dirichlet right-hand side. Setting w_R=u_R-h_0 gives exactly

    (-Q_R)w_R = f,   f=1+L_core h_0,

with zero exit boundary. For fixed R, finite killed-chain resolvent theory gives

    w_R(y)=E_y integral_0^tau_exit f(Y_s) ds.

If f<=M, this is <=M E tau_exit<=M C_act, because exit occurs no later than hub
activation. The finite chain is transient and all terms are integrable for that
fixed finite R. Negative forcing or negative w_R need not be bounded in absolute
value uniformly in R: their contribution to incoming leakage only helps. This
one-sided distinction is mathematically valid and avoids an unnecessary premise.

The upper bound is independent of R because M is acquired globally below, and
C_act is uniform in the initial inactive population. No small-head numerical
experiment is substituted for that uniform statement.

## 4. Positive forcing has an acquired finite support

The proof and code choose K satisfying

    delta K>=B+2cD+1,
    T K/(K+c)>=1,
    T^K g(K)>=1.

These imply that T^r g(r) is nondecreasing and >=1 for every r>=K. The core quotient
is at most -1 there, hence `f=1+L_core h_0<=0`. The finite maximum over every
inactive composition below K therefore supplies a genuine global upper bound M.
The value h_0(0)=1 is used consistently in this forcing calculation; the final
head still replaces it by u_R(0).

The verifier independently enumerates the forcing support, recomputes all forcing
values from actual core jumps, checks K's three conditions, and checks the bound
`E_+=M C_act`. It also checks `u_R-h_0<=E_+` on every acquired head state as an
additional finite challenge. Corrupting M is rejected.

## 5. The new inactive fringe is not ignored

The extra incoming patch term at a hub-empty state with r=R is precisely

    T^Z sum_(i inactive) d_i y_i w_R(y-e_i).

The previously acquired upper bound gives at most `T^Z d_I R E_+`. Dividing by
h_0(y)>=T^R g(R) proves the stated scalar sufficient inequality. The positive
leak is only linear in R, whereas T^R g(R) grows exponentially. Thus all
sufficiently large heads are compatible.

The submitted scalar-radius witness additionally satisfies

    T R^2 >= (R+c)(R+1).

This ensures that T^r g(r)/r is nondecreasing for r>=R: its successive ratio is
`T [r/(r+c)] [r/(r+1)]`, an increasing product of positive factors. Therefore the
recorded scalar witness really certifies all larger radii as well. This closes
the potential ambiguity between a sufficient single radius and a monotone
threshold. The independent verifier checks this extra inequality exactly.

The actual algorithm does something stronger operationally than trusting the
conservative radius: it solves a finite head, checks EVERY inactive composition
at r=R, and doubles only if one of those exact inequalities fails. Its termination
follows from the uniform excess theorem, not from an unbounded optimistic search
or a supplied good radius. A head-budget failure is returned as UNKNOWN.

## 6. Independent reconstruction of the failed first patch

I separately constructed and solved the R=2 killed-head equations, using an
independent rational Gaussian elimination rather than the submitted solver. At
the inactive service state 2A, the resulting exact full quotient is

    LV/V = 2159109577/927605760 >0.

No star is enabled on that service state. The same quotient holds for EVERY
satellite population, with V proportional to T^Z. Consequently no finite C and
positive epsilon can make `LV<=-epsilon V+C` hold on this ray for that first patch.
This is a genuine global-Lyapunov failure, not merely failure of a loose bound or
a finite sampling threshold. It is not an instability statement about the chain.

At R=4 the independently reconstructed accepted certificate covers all five
inactive fringe states and all 55 active service layers. The first failure and
the additional head-solve cost remain in the acquisition receipt.

## 7. Global drift, nonexplosion and moments remain justified

The final certificate covers four exhaustive regions:

1. the actual finite service head, with exact quotient -1/u_R;
2. every inactive fringe composition at r=R, checked exactly;
3. every active service state with 1<=r<=R, with an acquired constant quotient and
   strictly positive negative satellite slopes;
4. the unchanged analytic tail.

Star jumps never enter the inactive head: a forward star leaves a hub particle
and a reverse creates one. Outside the fringe, inactive or active core states
cannot jump down far enough to enter the head. Neutral channels preserve the
entire function. Every active-layer threshold and the global rational C are
therefore paid rather than omitted.

The resulting V is positive and normlike. Stopped Dynkin rules out escape to
infinite V in finite time; finite sublevels have bounded rates even with
high-degree neutral channels, ruling out hidden explosion. Exterior Foster drift,
weak-reversibility population return paths and finite-set regeneration establish
positive recurrence. The stopped-semigroup/concave-truncation argument proves
pi(V)<=C/epsilon without presupposing integrability.

For every requested finite exponential moment, choosing rational T>exp(theta)
and completing its finite search gives V>=K exp(theta N). The same classwise
stationary probability receives these conclusions. All-exponent validity is an
ordinary theorem of the terminating construction; it is not inferred from the
finite list of executed T values or from overriding a work-budget decline.

## 8. Independent finite verifier and executed challenges

`independent_audit/verify_general.py` verifies the raw partition, absorption
weights, tail constants, full Dirichlet equations, inactive fringe coverage,
active layer constants/slopes, Foster C, paid path clock, global forcing support,
one-sided excess and scalar radius. Its verifier does not call the submitted
`recognize`, `construct`, `solve`, `value` or `generator` routines. It uses the
submitted constructor only to propose certificates, which are then independently
checked. The failed R=2 head has an additional independent solve.

All six executed cases passed:

| Case | T | Accepted R | Head states | Active layers | Exact state checks |
|---|---:|---:|---:|---:|---:|
| Added inactive death; repaired head required | 2 | 4 | 10 | 55 | 840 |
| Recovery of no-inactive-death subclass | 2 | 2 | 3 | 9 | 280 |
| Larger exponential base | 4 | 2 | 3 | 9 | 280 |
| Death at both inactive phases | 2 | 4 | 10 | 55 | 840 |
| Two satellites, seventh-order neutral mixing, inactive death | 2 | 4 | 10 | 55 | 2,520 |
| All service species are hubs; direct immigration clock | 2 | 2 | 1 | 5 | 60 |

Total additional finite state checks: **4,820**. They supplement, not replace, the
all-state proof and finite exact certificates. The original frozen demonstration
was replayed byte-identically, retaining its separate 1,050 state challenges.
Fringe-coverage, clock-probability, forcing-bound and head-value tampering were all
rejected.

With a budget of only three head states, the code correctly records the invalid
R=2 trial and then declines at R=4, which needs ten states. It does not label the
first local Dirichlet solution a global certificate. The receipt remains UNKNOWN
for that budgeted request.

## 9. Costs and retained limitations

The default head budget bounds each finite head solve, not every possible scalar
or forcing-enumeration operation. The positive-forcing enumeration below K and
the scalar termination witness have their own real costs; they are recorded and
must not be described as free merely because the accepted head is small. Every
failed head solve is charged. No polynomial complexity, compact certificate size,
useful mixing rate, or uniform rare-phase bound is established.

The positive clock lower bound may be small, and u_R, E_+, C, thresholds and
rational numerators may be large. This is explicit acquired work, not an oracle
premise. The mathematical unbudgeted search terminates for the stated finite
architecture; a default-budget run can stop earlier without settling recurrence
by itself.

The architecture still requires a monomolecular core, complete positive hub rows,
direct death at every hub, and a genuinely neutral remainder. Hubs without direct
death, arbitrary nonlinear cores, separate absent-hub geometries and general weak
reversibility are not discharged. The non-complex-balance example is valid, but
non-complex-balance alone does not establish novelty against conventional
non-product-form recurrence methods. No external priority search or physical
validation is part of this acceptance.

No upload, publication, outreach, laboratory or biological procedure, or denied-
source retry occurred in this review. Earlier accepted artifacts remain unchanged.
