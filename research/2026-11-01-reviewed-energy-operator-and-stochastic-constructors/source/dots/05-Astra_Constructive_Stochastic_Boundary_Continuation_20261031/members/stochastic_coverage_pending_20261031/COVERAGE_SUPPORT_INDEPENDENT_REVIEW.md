# Independent review: terminating tilted-support coverage construction

## Verdict and frozen objects

**ACCEPTED at the frozen versions below.** The acquired finite support table,
its monotonicity, actual-count comparison, rational small-tilt search, shifted
radial factor and compact Foster constant together prove the stated termination
and stability theorem for the recognized linear-service-core partial-row class.
At least one positive exponential moment is acquired. Arbitrary prescribed
exponents, general weak reversibility and historical novelty are not claimed.

| Object | SHA-256 |
|---|---|
| `COVERAGE_SUPPORT_THEOREM.md` | `40fc026d097ae0b69a68b3f133edb264efcc1e887dd21cff17946e4a02f4b91d` |
| `coverage_boundary.py` | `36a81f01731ff5ed9592ce2723c8871d688726d083b10e05ef1e2a546eccb673` |
| `results.json` | `517b631a155ccc8928555bedd640c129cb0d0705c9985af43478135275863130` |

Frozen copies, byte-identical replay, independent exact verifier and challenge
receipts are in `independent_audit/`. The original frozen JSON also passed direct
independent verification. No earlier accepted package was changed.

A pre-freeze implementation issue was corrected: the support-state count is now
checked against its budget **before** constructing the binary-state list. No
mathematical repair to the proof was needed.

## 1. Finite graph, transience and monotonicity

The covered supports are upward-closed because adding occupied hubs cannot
remove a satellite's neighbor. The all-occupied support is covered by the raw
coverage condition.

Strong connectivity of the monomolecular graph gives a directed out-tree rooted
at0. Its root edges are immigrations and all other tree edges are conversions;
no death edge is needed along a root-to-service path. Fill vertices in decreasing
tree-depth order, generating a token along the root-to-destination path for each
one. Previously filled deeper vertices cannot be on the current path. Existing
ancestor tokens merely coalesce with the moved token and do not obstruct the
next transition. This proves positive-probability access to all-occupied support
from **every** initial support, not only from the empty state. Because the binary
chain is finite, the killed matrix is transient and the hitting-time system is
nonsingular with positive solution.

The relevant conversion map is `(B\{i}) union {j}` when i is occupied, and the
identity when i is absent. This coalescing map is inclusion-monotone, including
an already occupied destination. Death and immigration maps are monotone too.
Common finite-rate arrows preserve inclusion; hitting an upward-closed target
from a larger support occurs no later. Thus tau and f=1+tau are decreasing.
This establishes the table property for the entire class, rather than treating
successful finite tests as a universal proof.

For every executed case the verifier independently reconstructs all binary
transitions using set operations, checks directed reachability from every state
to the target, solves the killed system by separate rational forward/back
elimination, checks every comparable pair of f values, and also checks monotonicity
of every graphical map. The full raw graph and core conditions are independently
recovered, not trusted from role labels.

## 2. Actual support comparison: the critical inequality

At a death source of count1, actual and binary supports update identically. At
count at least2, actual support does not change, while the binary removal has a
nonnegative f increment. Multiplying the actual zero increment by the count is
harmless.

For conversion i->j with count1 at i, the updates and rate factors coincide. With
count n>=2, actual support retains i and adds j, giving
`a=f(B union {j})-f(B)<=0`. Monotonicity gives

    n*a <= a <= f((B\{i}) union {j})-f(B).

This also handles occupied j: actual support has zero increment, whereas binary
coalescence can remove the i-token and increase f. Immigration agrees exactly.
Consequently the actual tilted support generator is bounded above by the binary
one term by term. No independence of actual particles or stationary fiber law
is used.

The exact exponential conjugation separates the linear potential
`B + sum eta*y_i*(Qv)_i/q_i <= B-delta*r`. On uncovered supports the binary
quotient is at most -1/F; on covered supports f=1 and it is at most K. The signs
and denominator inequalities in both cases are correct.

These are pointwise generator facts; they do not presuppose nonexplosion of the
full satellite chain.

## 3. Rational halving is an acquired terminating operation

The v,L weight data are independent of T. For each T=1+2^-n the code builds and
solves the actual finite tilted system. At T=1 the same finite graph is transient;
its matrix is nonsingular. Matrix entries and inverse are continuous near1, so
the finitely many hitting-time entries, and their maximum F(T), remain bounded.
Meanwhile B(T)->0. Thus the exact rational test B(T)F(T)<=1/4 eventually succeeds.
This proves termination of the enumerated loop without supplying a favorable T
or a modulus/clock oracle. It gives no uniform efficient number of trials.

The independent verifier recomputes the finite table at **every attempted T**,
not merely the accepted trial, and checks the BF tests, first successful index,
state dimensions and summed matrix-entry accounting. The numerical LP from the
previous package is not invoked at all.

## 4. Extinction layers and the shifted radial factor

The shift g(0)=1, g(r+1)/g(r)=(r+1)/(r+1+c) handles zero and first service layers
without a separate patch. Immigration's g factor improves the conjugated bound;
conversion leaves r unchanged. Death adds at most c D F because its ratio is
1+c/r, f(next)/f(current)<=F, and sum d_i*y_i/q_i<=D*r. At r=0 there is no death,
so the same upper bound is harmless.

Stars preserve the hub's presence. With q_h=T their exponential and support
factors cancel. Their forward contribution is at most c*alpha*r; their reverse
contribution is exactly

    -c/(r+1+c) sum beta_hj*y_h*z_j.

Choosing c<=delta/(4alpha) and c<=1/(4DF^2), together with BF<=1/4, yields uniform
negative drift on every uncovered support, including r=0 and r=1 and arbitrary
satellite populations. The master inequality is therefore correctly global.

## 5. Compact exception constant and recurrence

Covered states with r>=R have negative radial drift. For the remaining covered
states r<R, the denominator r+1+c is at most **R+c**, so each satellite slope is
at least c*beta_min/(R+c). The code's cutoff uses this correct denominator;
R+1+c would be safe but unnecessarily looser. The explicit Z_star covers every
allocation of satellite total, not just a selected coordinate axis.

On the remaining finite exception region,
`V<=F*q_max^R*T^Z_star`, while `LV+epsilon V<=(A+epsilon)V`. Hence the factored
constant `F(A+epsilon)*q_max^R*T^Z_star` is sufficient. The verifier checks all its
rational factors, integer exponents, defining inequalities and unreduced bit
upper bounds without materializing the powers. This is a fully defined finite
rational constant, not an assumed oracle; writing its entire expanded bit string
would be a different, potentially prohibitive computation.

Since c<=1, g(r)>=1/(r+1) and V>=T^N/(r+1), so V is normlike. The global upper
bound LV<=A*V proves nonexplosion by stopped finite sublevels. The finite-set
Foster inequality and weak-reversibility return paths then yield classwise
positive recurrence.

**Ordinary independent nonexplosion comparator.** In this restricted linear-core
architecture, only immigration increases total count, at constant total rate
Lambda. Core conversions, stars and neutral channels conserve total count;
deaths decrease it. Coupling to the immigration Poisson clock bounds
`N(t)<=N(0)+Poisson(Lambda*t)`. Up to every finite time the allowed count states
are then finite, and their rates are bounded, ruling out explosion. This gives
a simpler conventional check independent of the new Lyapunov function.
Recurrence and acquired control of uncovered boundary fibers, not nonexplosion
alone, are the substantive result.

Stationary integration is justified using stopped exponential Dynkin, invariant
concave truncations min(V,n), and Fatou with a finite constant lower bound. Thus
pi(V)<=C/epsilon without circular integrability assumptions. Exponential count
moments follow only for theta<log T of the acquired certificate. All polynomial
moments follow, but all exponential exponents do not.

## 6. Independent exact execution

`verify_coverage.py` does not call the submitted recognizer, table constructor,
linear solver, quotient or master-bound functions while verifying a receipt.
It reconstructs the raw architecture, solves/checks every finite table, derives
all constants and verifies the factored exception expression. The parent
constructor only proposes receipts.

Seven cases passed **4,788 ordinary exact master-bound checks**, **792 targeted
large-state checks**, and **364 actual-support generator comparisons**. Another
**81 small states** were checked using the explicitly expanded small-state V and
raw generator, independently of bounded-jump ratio evaluation. No giant Foster
constant was expanded.

| Case | Acquired T | Tilt trials | Binary / killed states | Ordinary / targeted checks |
|---|---:|---:|---:|---:|
| Original partial-row input | 65/64 | 7 | 4 / 3 | 252 / 72 |
| Complete-row target recovery | 9/8 | 4 | 4 / 1 | 252 / 72 |
| Additional inactive phase previously declined by LP budget | 65/64 | 7 | 8 / 6 | 756 / 144 |
| Single immigration root, simultaneous hub filling | 513/512 | 10 | 8 / 6 | 756 / 144 |
| Three hubs with overlapping satellite coverage | 33/32 | 6 | 8 / 4 | 2,268 / 216 |
| Degree-seven neutral motion | 65/64 | 7 | 4 / 3 | 252 / 72 |
| Species permutation / reacquired roles | 65/64 | 7 | 4 / 3 | 252 / 72 |

The additional-inactive-phase input is the same raw extension on which the
previous finite LP attempt stopped at its200-state budget. Its successful
support certificate is a separate acquisition, not a reinterpretation of that
UNKNOWN result. The single-root case tests the reverse-depth filling argument
without assuming direct immigration into each hub. The three-hub case has several
minimal covering supports rather than only the all-hubs-occupied target.

The original example independently reproduces T=65/64, R=7581 and
Z_star=3822285280. The compact constant's unreduced numerator-bit upper bound is
26,756,050,111. The single-root challenge is substantially worse: R=751993,
Z_star=1261949382957937 and an unreduced numerator-bit upper bound about1.26e16.
These are conservative upper bounds on unreduced expansions, not measurements
of a materialized or fully reduced number. The enormous cost is disclosed, not
hidden behind a formal word "constant".

Mutations of coverage labels, coalescing event lists, hitting-time values,
halving acceptance flags, radial c, compact coefficient/exponent and bit bounds
were rejected. Full-WR mutations introducing unsupported nonlinear service
reactions or leaving a satellite uncovered were rejected structurally. Support
budget3 versus required4 and tilt budget6 versus required7 return UNKNOWN;
no mathematical instability is inferred.

## 7. Retained limits

The theorem applies to the stated monomolecular service core, positive direct
hub deaths, paired star shapes, global satellite coverage and neutral remainder.
It does not settle general weak reversibility or arbitrary nonlinear service
interactions. The finite support problem is exponential in the number of service
species; raw partition search, all attempted rational solves, comparisons and
coefficient growth are actual work. Final solved-value bit fields are not a
complete bound on every intermediate elimination numerator or memory use.

The compact C makes a qualitative constructive theorem verifiable without
expanding astronomic integers. It does not make the displayed tail/mixing bound
practically useful. The earlier LP route may acquire a much larger T and tighter
constants on the same network, but lacks this structural termination guarantee.
Neither route is claimed uniformly superior.

The finite support-coverage target is distinct from first-hub activation. A
single logical token can address that other target but cannot record simultaneous
multi-hub coverage by itself. No conclusion about the separate single-token
package is imported into this verdict.
