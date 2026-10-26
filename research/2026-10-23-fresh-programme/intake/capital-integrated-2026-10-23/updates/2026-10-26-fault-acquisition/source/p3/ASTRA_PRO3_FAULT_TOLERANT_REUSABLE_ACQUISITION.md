# Astra Pro3 — Fault-tolerant reusable scientific acquisition and native experiment design

26 October 2026, Australia/Brisbane. Original constructive continuation of the temporary Pro3 role. **Claims are conditional mathematics plus executed rational synthetic-source experiments.** No physical instrument was measured, no new physical law or historical mathematical priority established, and no advantage over a strong equally informed retaining algorithm is claimed.

## 1. Scientific obstruction and change of procedure

The preceding scalar difference-constraint compiler retained a joint family from absolute and relative sensor reports and demonstrated complementary experiment paths. It required the declared measurement errors to be valid. If a few sensors instead produce **arbitrary and unbounded errors**, a negative cycle detects inconsistency but does not by itself restore a useful scientific source model. In future experiments, the source might also drift and several readings might fail **as one instrument group**, not as independent sensor edges.

This continuation changes **what is acquired**. An agent selects an *error-correcting topology of genuine native relative measurements*, decodes a globally compatible history up to the physically irrelevant common offset, then compiles unseen response and constrained-equilibrium operations. The observation architecture itself is an experimental choice, not a model fitting after the fact.

The mechanisms use established graph-code, robust synchronization, Menger/edge-connectivity, Euclidean projection, McShane scalar Lipschitz extension, and Kirszbraun vector extension mathematics. The particular research connection is among experiment topology, corruption units, operation-specific equivalence, later nonlinear control questions, source drift, and fully charged correctness certificates.

## 2. Complete exact criterion for corrupt relative readings

Let an unknown vector of scalar response values be `z=(z_0,...,z_(n-1))`, where each coordinate denotes a *specific component at a specific sampled operating point*. A native relative sensor on an undirected edge `e={u,v}` reports `y_e=z_v-z_u` in a fixed orientation, except that **at most f different edges can report arbitrary incorrect values**. Values and errors need no random distribution. The whole acquisition concerns one stable latent `z`, with no unknown edge-dependent transformations. Adding a constant to every `z_i` is invisible to the instrument.

**Theorem 1 — sharp universal fault-tolerance criterion.** All source differences are uniquely recoverable, up to one common additive gauge, from any such history with up to `f` corrupted edges **if and only if** the undirected acquisition graph has edge-connectivity

\[
\lambda(G)\ge 2f+1.
\]

Proof (necessity). If an edge cut has at most `2f` edges, let one latent vector be identically zero and the other be `delta` on one side of the cut, zero on the other. Their noiseless edge-difference codewords differ only across that cut. Partition those edges into two sets of size at most `f`, and publish one candidate's report on one part and the other's report on the other. The same full history is consistent with either source and at most `f` corruptions. For measured points belonging to a module with a strictly positive Lipschitz margin, choose `delta` small enough that both sources admit Lipschitz extensions; a hidden structure with an exact equality constraint could change this minimax premise.

Proof (sufficiency and executable decoder). Menger's edge theorem gives at least `2f+1` edge-disjoint paths from a fixed root to any vertex. Sum reports along each directed root-to-target path. An incorrect edge affects at most one of the edge-disjoint paths. At least `f+1` path sums equal the correct difference, so the median for real scalars gives exactly `z_v-z_root`. This decoder is adaptive-fault-safe so long as the **total** number of different corrupted edges stays at most `f`; it does not assume probabilistic independence. The root gauge is the only ambiguity. QED.

Equivalently, the real-valued graph incidence code has minimum edge-Hamming distance exactly `lambda(G)` between non-gauge-equivalent sources; this is classical coding logic. The theorem is **not** a claim that arbitrary real physical sensor classes can be turned into independent edge measurements at no cost.

### Optimal 12-node topology, two gross corruptions

With `n=12`, `f=2`, every vertex degree is at least five; hence `|E| >= ceil(12*5/2)=30`. Use vertices `Z_12` and join each `u` to `u+1`, `u+2`, and `u+6` modulo 12, treating edges as undirected. The resulting graph has 30 edges, degree five at every vertex, and minimum edge cut exactly five. The executable **exhaustively checked 2,047 nontrivial rooted cuts** and saved five edge-disjoint paths for each of the 11 non-root nodes.

Twelve latent values were actual source responses from four separate rational nonlinear modules at three sampling points each, with supplied spatial residual Lipschitz constant `a=1/10`. The decoder received 30 scalar difference-sensor readings. Faults of `+7` and `-11` were inserted into two edge reports, overwhelming the natural response scale. All 12 values were recovered **exactly modulo one common offset**, and both nonzero corrupted-edge residuals were identified. A second run imposed honest-edge errors of magnitude at most `eta=10^-4` while retaining those two arbitrary faults.

For `f=2` and honest errors `|epsilon_e|<=eta_e`, an uncorrupted path `P` satisfies

\[
\bigl|\textstyle\sum_{e\in P}\pm y_e-(z_v-z_0)\bigr|\le\sum_{e\in P}\eta_e.
\]

At least three of the five paths remain honest; hence their median lies within `max_P sum_(e in P) eta_e` of the correct answer. This is conservative; it is **not a sharp joint noisy posterior**, and the actual corrupt-edge identity need not be identifiable when errors lie inside honest budgets.

The code deletes one selected edge to yield 29 calls and constructs **two distinct scalar module families** whose old transcripts are identical, each with two corruptions. The required change of only `1/100` at a measured node respects the declared Lipschitz bound. The universal 30-call lower bound is therefore meaningful within the acquired scalar source interface.

## 3. How recovered relative readings generate future experiments

At future task time, response component `i` has an unknown residual scalar function `A_i(t)` with known `a`-Lipschitz bound. The graph records values at `s_j in {0,1/2,1}`, estimated as `c_ij` with valid radii `r_ij`. The unknown common additive constant is `h`. The following functions **enclose every source**, after choosing the common gauge `h=0`:

\[
L_i(t)=\max_j[c_{ij}-r_{ij}-a|t-s_j|],\qquad
U_i(t)=\min_j[c_{ij}+r_{ij}+a|t-s_j|].
\]

Every valid source satisfies `L_i(t)<=A_i(t)-h<=U_i(t)`. The midpoint `H_i=(L_i+U_i)/2` is itself `a`-Lipschitz. Let `R_i>=sup_t (U_i-L_i)/2`; the implementation obtains each rational `R_i` by evaluation at a 257-point mesh **plus** the proved interpolation inflation `a/512`. Thus `E=sqrt(sum R_i^2)` bounds the full 4-vector response error. All square roots and norm calculations are outward rounded to explicit dyadic rationals.

For a later, previously unknown signed feedback matrix `K` and load `p`, the fixed-dose constrained equilibrium is the unique fixed point of

\[
T_A(x)=\Pi_\Delta((p+Kx-A(x))/m),\quad
\Delta=\{x\ge0:\sum_i x_i=1\},\quad m=2,
\]

provided `q=(||K||_2+a)/m<1`. The implementation certifies this via `||K||_F` rather than pretending a floating eigenvalue is exact. The projection is Euclidean and nonexpansive. Adding a common scalar `h` to **every** component of `A` changes the projection's argument by a uniform vector and hence does not change `T_A` on the simplex. The unobserved absolute offset is therefore *physically irrelevant to this operation*, not learned.

For any computable surrogate point `xhat` and its exact projected-map residual `epsilon=||xhat-T_H(xhat)||_2`, the true equilibrium obeys

\[
\boxed{\|xhat-x_*\|_2\le {\epsilon+E/m\over 1-q}.}
\]

Proof: insert `T_H(xhat)` between `xhat` and `T_A(x*)`, use pointwise response enclosure, nonexpansive projection, and the contraction inequality; rearrange. This guarantees a useful prediction even if the midpoint surrogate does not represent one globally sensor-compatible source. For noisy data these envelopes are explicitly only an **outer** consistency family.

Four signed/nonsymmetric feedback structures and 15 independently specified loads each were compiled *after source acquisition*. Across **60 future tasks**, the exact-honest-reading acquisition yielded mean certified position radius `0.02052321`; the largest independent checker discrepancy was `0.00494051`. With bounded honest noise, the mean certified radius was `0.02090121`. **Zero additional learner native calls** were made for the 60 tasks in either case. The checker separately evaluated the source formula, including at least `60*56*4=13,440` component-function evaluations per 60-task run; these are not hidden in the learner budget.

An equally informed classical graph-code decoder and Lipschitz retainer could use exactly the same information and tie the result. The advancement is a concrete reusable source-to-operation pipeline, not exclusive superiority.

## 4. Correlated *instrument-group* failures are a different model

The preceding graph theorem is **false** if one failed physical instrument can corrupt several measurement edges and only the **number of failed instruments** is bounded. One group holding all five edges incident to the root can, by itself, erase the distinction between two source assignments, even though the edge graph still has connectivity five. The script gives an exact rational witness.

Suppose there are exactly `G=2f+1` independently fallible instrument groups; group `g` reports a collection of pairwise differences, and at most `f` whole groups can produce arbitrarily corrupted outputs. **Theorem 2.** Universal recovery of all differences requires each of the `G` individual measurement subgraphs to be connected. Indeed, for every nontrivial source cut, crossing edges must be present in at least `2f+1` distinct groups; otherwise partition the groups crossing that cut into two subsets of at most `f` and construct indistinguishable sources as above. Since there are exactly `2f+1` groups, every group must cross every cut, hence each group's subgraph is connected. Conversely, a connected subgraph in every group supplies one correct root-to-target path per healthy group, so a median across groups recovers each difference. Each connected group requires at least `n-1` scalar difference readings.

For **12 nodes, two faulty entire instruments and exactly five instrument groups**, at least `5*(12-1)=55` scalar values are necessary. The executed construction gives each of five independent vector-reading instruments an eleven-edge reference star. Instruments 1 and 4 corrupted **all eleven outputs each**, while the other three were honest. The per-target five-way medians recovered all relative values exactly and again certified 60 unforeseen equilibria with mean radius `0.02052321`.

This 55-scalar statement is conditional on *exactly five separately faulting groups and pairwise-difference observations*. It is not a lower bound for arbitrary analog linear-combination sensors, nor for an unlimited number of separately failing small instruments. The scenario uses five vector instrument calls returning 11 numbers each; it is not five scalar measurements.

## 5. Drift between measurements and future use

In a third changed observation interface, a stable node value no longer exists at the different acquisition times. Assume instead that each scalar node potential has **supplied** temporal drift `|z_i(t)-z_i(s)|<=v|t-s|` and every healthy relative sensor acquired edge `e={u,w}` at time `tau_e` with small error `eta_e`:

\[
\bigl|y_e-[z_w(t_0)-z_u(t_0)]\bigr|
\le (v_u+v_w)|\tau_e-t_0|+\eta_e.
\]

Summing along five edge-disjoint paths gives an honest-path snapshot bound; their median remains sound with two arbitrary corruptions. To use this posterior at future `t_*>t_0`, add `(v_i+v_0)|t_*-t_0|` to each decoded **relative** node uncertainty. There is no unjustified exact time-transport. The same later fixed-dose map is certified if its spatial Lipschitz contract continues to hold.

Executed control: 30 time-stamped scalar difference readings in `(0,1)`, two enormous edge corruptions, honest sensor error `eta=1/10000`, a nonlinear source that **really changes with time**, and a supplied temporal drift ceiling `v=1/200`. The new tasks were requested at time `3/2`, strictly after the acquisition window. An exact rational **61-candidate** reference-time menu gave:

| Reference snapshot | Max certified future node radius | Mean future equilibrium radius |
|---|---:|---:|
| `t_0=0` | 0.03959355 | 0.05691673 |
| `t_0=1/2` | **0.02201290** | **0.04384710** |
| `t_0=1` | 0.03185161 | 0.05106451 |

All three candidate reference choices certified 60 later network equilibria. The minimizer at `1/2` is only optimal over the 61 tested reference times; it is not a claimed continuous optimum. The improvement is a change of *evidence management and timing* with **zero extra native source calls**, conditioned on the temporal regularity contract.

## 6. Vector-valued extension and its exact boundary

Path-majority reconstruction does not depend on scalar ordering. For any additive abelian group, five edge-disjoint path sums contain at least three exact copies of the true group difference under two arbitrary edge faults. Taking the **most frequent full vector**, not an ill-defined vector median, recovers the vector difference exactly. A separate two-coordinate rational nonlinear-source control used 30 *vector-valued* relative readings (60 returned scalar coordinates), corrected two arbitrary vector corruptions and reconstructed all twelve vectors up to one common vector offset.

The next 24 fixed-input vector requests were outside the measured sites. With a justified Euclidean `L=3/25` spatial Lipschitz ceiling, nearest old readings supplied sound nonsharp balls, and all 24 independent checker values were enclosed with no new native calls.

**Theorem 3 — sharp one-input vector posterior.** For one future fixed input `t`, old vector readings `(s_j,y_j)` determine the exact possible vector-response set

\[
\boxed{\mathcal V_t=\bigcap_j \{y:\|y-y_j\|_2\le L|t-s_j|\}.}
\]

Necessity is Lipschitz continuity. Conversely, every point of this intersection extends the old finite vector assignment without increasing `L`, by the **Kirszbraun theorem** (provided the old assignment itself satisfies the supplied Lipschitz contract). Thus the intersection is not merely outer: it is the complete one-input source-family image.

For a two-dimensional vector and a new linear readout `c·y`, its extrema over the intersection of finitely many disks are attained at a disk's supporting tangent point in direction `+/-c`, or at a pairwise circle-intersection point. All candidate points can be written `b+sqrt(q)*d` with rational `b,d,q`. The script enumerates *all* such candidates, checks their disk feasibility using exact signs of rational expressions `alpha+beta*sqrt(q)`, and encloses their readout values using outward `48`-fractional-bit square-root intervals. It does not trust floating circular-intersection tests. This is classical planar geometry and Kirszbraun extension integrated with acquired, fault-corrected source information—not a claimed new Lipschitz theorem.

The executed programme certified **72 unforeseen directional vector-response questions**. Compared with nearest-observation balls, **50 received strictly tighter widths**, with maximum tightening `4.70588235x` and median finite tightening `1.13270853x`. All actual source projections were enclosed; the sharp endpoints are rational-outward enclosures of algebraic optima, not exactly rational extrema.

A further **12 two-input contrast questions** impose the extra necessary consistency relation

\[
|c\cdot (A(t_1)-A(t_2))|\le L|t_1-t_2|
\]

in addition to their individually sharp one-input intervals. This reduced certified interval width by up to `15.45138889x` versus the naive independent combination. Unlike the **single-input** disk-intersection result, these two-input intervals are **valid outer bounds only**, not asserted jointly sharp. The true joint two-input posterior also constrains the two unknown vectors relative to every old observation simultaneously.

## 7. Cost, limitations, and strong equal-information alternatives

| Acquisition interface | Learner acquisition | Later source calls | Verified future questions |
|---|---:|---:|---:|
| Exact scalar, two unbounded edge faults | 30 scalar differential calls | 0 | 60 equilibria |
| Small honest noise + two edge faults | 30 scalar differential calls | 0 | 60 equilibria |
| Two entire bad instrument groups | 5 vector/group calls, 55 scalar results | 0 | 60 equilibria |
| 30 asynchronous calls, bounded drift and edge faults | 30 scalar differential calls | 0 | 240 equilibrium/control certificates across four reference choices |
| Two-coordinate vector source + two bad edges | 30 vector differential calls, 60 scalar results | 0 | 24 direct vector + 72 sharp projections + 12 coupled contrasts |

An independent verifier checked **all 2,047 cuts**, the saved disjoint paths, exact path sums and robust medians, rational upper error budgets, projected-map residual proofs and held-out source checks. In total, **528 reported later-task certificates** passed (some reuse the same task portfolio under distinct acquisition assumptions, so these are not 528 independent physical systems). The 420 equilibrium reference checks alone involved at least 94,080 synthetic source-function evaluations inside their independent reference solvers, plus the separate validation/source consistency evaluations. Acquisition graph construction and arithmetic, retained vector widths and dyadic rounding are executable and not free.

The strongest classical equal-information comparison is graph error-correcting synchronization followed by ordinary Lipschitz completion and fixed-point residual verification. Given the same native readouts, fault group definitions and contracts, such an algorithm can tie every construction here. Robust group synchronization has a substantial established literature (e.g. Lerman–Shi, *Robust Group Synchronization via Cycle-Edge Message Passing*, Foundations of Computational Mathematics 2021, https://doi.org/10.1007/s10208-021-09532-w), though that paper's model and performance theorem differ from this deterministic finite-edge code. Edge-disjoint paths come from classical Menger/max-flow/min-cut, e.g. https://www.cs.cornell.edu/courses/cs6820/2016fa/handouts/flows.pdf . Kirszbraun is classical; an explicit extension reference is https://www.cambridge.org/core/journals/canadian-mathematical-bulletin/article/kirszbrauns-theorem-via-an-explicit-formula/15797B44C630B0E2A4BB12547759929D .

**Contracts not acquired:** the correctness of the source-relative sensor semantics, stationarity within the exact experiment, the maximum number of faulty edges or instruments, independently justifiable drift and spatial Lipschitz ceilings, and the physical projection/digital control law. Finite consistency does not establish any of them globally. A single failing group invalidates an unqualified independent-edge fault guarantee. Correlated honest measurement noise can be accommodated only insofar as its declared deterministic component bounds remain true; its exact joint posterior may be tighter than the stored outer balls. Physical instruments returning differences across different modules and different positions may be expensive or nonexistent; their availability cannot be inferred from the mathematics.

**Strongest next unresolved frontier:** joint *vector-valued* posterior optimization across several unknown future inputs and networks after fault correction, together with independently acquiring credible sensor-group fault and source-regularity contracts. In general, scalar McShane upper/lower lattice arguments do not apply. For *fixed* new input locations, second-order cone consistency is exact under Kirszbraun; if equilibrium inputs are themselves unknown, the resulting constraints are nonconvex and require honest global certificates rather than simply running a local optimiser.

## 8. Reproduction

The ordinary working directory contains six separate executable investigations and six actual corresponding JSON output files:

- `fault_tolerant_acquisition.py`: exact scalar edge decoder, 30-edge proof/control, noise correction and 60 future source-to-operation queries.
- `group_fault_acquisition.py`: joint hardware-group failure theorem, 55-scalar construction, impossibility witness and 60 later tasks.
- `drifting_fault_robust_acquisition.py`: asynchronous native reading times, snapshot/reference selection, source expiry and 240 late queries.
- `vector_fault_acquisition.py`: vector-valued majority decoder, 24 later vector readings.
- `vector_joint_lipschitz_support.py`: complete fixed-input vector disks, exact radical candidate feasibility and 72 + 12 future queries.
- `verify_fault_tolerant_research.py`: independent source/checker audit, emitting `independent_verification_results.json`.

All query counts reflect **native readout capabilities declared by the fixture**. A genuine differential instrument producing one scalar/one vector is distinguished from software taking two independently charged absolute-source calls and subtracting them; the latter would require different cost accounting and may expose more information. The mathematical progress is reusable acquisition under corruption and uncertain future operations, not a demonstrated universal learning advantage.
