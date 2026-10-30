# A non-complex-balanced dormant extension with earned local kernels

30 October 2026. New working theorem, not independently reviewed. This is NOT a global recurrence theorem or historical novelty claim.

## 1. Model and why the ordinary endpoint changes

In operational time, counts `(a,c,d)` have fixed total `n`, and positive fixed rate constants multiply these six fast reactions:

1. `2a -> a+d`, rate `k1 (a)_2`;
2. `a+d -> 2a`, rate `k2 a d`;
3. `a+d -> c+d`, rate `k3 a d`;
4. `c+d -> a+d`, rate `k4 c d`;
5. `2a -> 2d`, rate `k5 (a)_2`;
6. `2d -> a+d`, rate `k6 (d)_2`.

Clearing kills at rate `k0(a)_2`. All coefficients are fixed strictly positive. Restore physical `A=a+a0`, with integer `a0>=2`, `m=a0+2`, and common catalyst factor `(A)_a0(B)_q`, `q>m`. Attach connector `0 -> A+B -> mA+qB -> 0`. All physical time statements below require `B>=q` up to the first connector event.

The residual graph has four complexes, is strongly connected, and has conservative rank two. The full graph has six complexes, one linkage class, and rank four, hence deficiency one. For `k1=...=k6=1`, complex balance is impossible for any positive connector rates: the non-anchor `c+d` equation gives `c=a`, the `2d` equation gives `d=a`, while the `a+d` equation then demands `3a^2=2a^2`. Common seed/catalyst factors cancel. The connector cannot repair these three non-anchor equations.

Thus this extension is not exhausted by the deficiency-zero/product-Poisson argument that already solves the minimal dormant triangle. This does NOT exclude another ordinary recurrence criterion.

On `d=0`, `c` is exactly frozen until a seed event. Both seed reactions have rates proportional to clearing. The pre-seed connector path is therefore the same marked enhanced-clearing reference process used in the previous isolated dormant Green candidate, with total seed rate `k1+k5`. Actual seed marks have outputs `(A-1,c,1)` or `(A-2,c,2)`. Both preserve physical total composition and shift inverse-A profiles by a bounded factor. No fake reference clearing post-state is used.

## 2. Finite absorption and geometric creation budget

Every active state enables one of the four complexes. A graph path to `2a` takes at most two edges (`2d -> a+d -> 2a` is longest), followed by clearing. Along the path the original source molecule vector can be transported exactly, leaving all spectator molecules unchanged. Total rate is at most `C n^2`; any prescribed enabled rate is at least a fixed positive constant. Therefore an attempt reaches clearing within three events with probability at least `c n^-6`. Fast activity is preserved. Conditional geometric trials give `sup_active E tau_clear <= C n^6`.

The combined clock of clearing and reactions 1 and 5 has independent marks with clearing probability `p=k0/(k0+k1+k5)>0`. Thus the total number `M` of creation events before clearing satisfies `P(M>=j)<=(1-p)^j`. Each creation increases d by at most two and decreases `R=a+c` by at most two. All other reactions decrease d or keep it unchanged; they increase R or keep it unchanged. This is the exact replacement for the earlier unit-jump budget.

## 3. Small dormant-return probability survives the new channels

Let `J=floor(n^(1/8))`, `K=floor(n^(1/4))`. Start at d=1, stop at clearing, d=0, or d>=J.

On `a<K`, `1<=d<J`, we have `c>=n/2`. Reaction 4 gives a drift at least `cnd`; reactions 1,3,5 contribute at worst `C(a^2+ad)`. Reaction 6 increases a and is favorable. Consequently the unkilled fast chain has `Qa>=cn` in this strip, and the stopped mean time to `a>=K` or a d-boundary is at most `CK/n` by bounded stopped Dynkin. Clearing only shortens it. The ONLY d=0 entrance is reaction 2 at d=1, so its probability in this stage is at most `C K^2/n` (the looser `CJK^2/n` also suffices). Clearing in this stage has probability at most `CK^3/n`.

On `a>=K/2`, `d<J`, clearing hazard is at least `cK^2`. The clearing compensator bounds `E integral(a)_2 <=1/k0`; hence `E integral a d <=CJ/K`. Reaction 6 only increases a. Falling from a>=K to a<K/2 requires either order K total creation losses (exponentially small by Section 2) or order K negative conversion losses. The latter are bounded even by the looser `CJ/K` probability. Thus the high-to-low restart probability is at most `CJ/K+C exp(-cK)`.

Conditional restart summation gives mean time `O(n^-1/2)` to one of these stops, dormant-return probability `O(n^-1/8)`, and low-a clearing probability `O(n^-1/4)`. An upper d exit needs at least `(J-1)/2` creation events and has probability `O(exp(-cJ))`.

Any path from any d>=1 to d=0 must first visit d=1: every d-decreasing reaction changes d by exactly one, and reaction 6 is disabled at d=1. Strong Markov therefore gives, uniformly over active positive-d inputs,

`P(hit d=0 before clearing) <= C n^-1/8`.

No favorable continuation is assigned to an upper exit; its event itself already bounds any possible later contribution to this probability.

## 4. Two-coordinate profile and actual new-reaction drift

For each fixed s>0 choose eta<1 sufficiently close to one, and let

`f_s(A)=(1+A)^-s`, `h_s(A,c)=(1+A+eta c)^-s`, `F_s=C1 f_s+C2 h_s`.

The old three linear-in-d channels 2,3,4 obey the reviewed paired-profile calculation: choose C2/C1 large enough that their total drift is nonpositive; it is strictly negative of order `d h_s` when `c<=M(1+A)` and of order `dc f_s/(1+A)` when c is larger, provided `a+c>=1`.

Reaction 6 increases A and `A+eta c` by one. It therefore has nonpositive drift on BOTH profile terms. More quantitatively, its negative contribution is at least a constant times `(d)_2 F_s/(1+A+eta c)`. This supplies strict negativity on the newly possible active states `a=c=0,d>=2`, where the old linear calculation alone is zero. It also strengthens every other state.

Reactions 1 and 5 decrease both profile coordinates by respectively one and two. Since they require a>=2 and A=a+a0, their total positive drift is at most `C_s a F_s`. At clearing the physical A output is a-2; the reward `g_s=(1+a-2)^-s` is at most `C_(a0,s) f_s(A)`. After enlarging C1, clearing supplies `-c(a)_2 F_s` even with that terminal reward.

For a above a fixed threshold the quadratic clearing term absorbs the seed drift. For bounded a and large n: if c is large, reaction 4 and the paired linear bound give a negative term of order dc; if c is bounded and a+c>=1, the paired linear bound is order d; if a=c=0, reaction 6 is order d^2. Hence the full killed-generator inequality is nonpositive on ALL active positive-d states for sufficiently large n. Finite active n are covered by finite-shell absorption and enlarging a boundary value; no asymptotic statement is extended to an inactive state.

Stopping at clearing, first connector birth, or first d=0 entrance gives

`E f_s(A_out) <= C_s f_s(A_in)`.

At a d=0 entrance reaction 2 increases A by one. Connector immigration and activation also increase both profile coordinates, so their terminal rewards are paid by their killing terms. This is a joint stopped kernel inequality, never an output-conditioned claim.

Combine the inequality at 2s with Section 3 using Cauchy–Schwarz:

`E[f_s(A_out); d=0 entrance] <= C_s n^-1/16 f_s(A_in)`.

At d=0 the first seed has either a one- or two-unit loss of A, each with a uniformly bounded profile ratio. Thus the actual dormant-to-seeded profile operator has finite norm, and the product with the positive-to-dormant return operator is small for large n. Truncated two-kernel equations and monotone convergence earn the full first-connector/clearing profile bound over every active input. This is an earned local two-face construction, not global connector recurrence.

## 5. Incoming physical time and inverse-power gain

At exponent s=m, restore `(A)_a0(B)_q`. For large a the negative killed drift is at least `c(A)_m F_m >=c'>0` in units of `(B)_q`. For bounded a and large n, the strict negative terms of Section 4 similarly dominate a fixed unit cost. Thus the stopped positive-d time is bounded by `C f_m(A_in)/(B)_q`. The d=0 first-event waiting time has the same bound, and the two seed outputs have bounded f_m ratios. The actual small return operator then yields

`(B)_q E tau_first_connector <= C (1+A_in)^-m`.

The only dormant-entry channel remains reaction 2 at d=1, with operational rate `k2 a`. At terminal reward f_s(A+1), a multiple of F_(s+1) has killed negative margin of order `(a)_2 F_(s+1)`, which pays `k2 a f_s(A+1)` for large a. For bounded a and large n the strict negative drift pays it. Therefore

`E[f_s(A_out); dormant entrance first] <= C_s f_(s+1)(A_in)`.

This last inequality is another local working proof; the earlier triangle version was itself unreviewed. It must not be cited as independently accepted merely because the paired-profile theorem was accepted.

## 6. Exact progress and unresolved global interface

The new reactions preserve the non-small dormant connector block, while removing the minimal fixture's automatic complex-balance solution. The local joint profiles, physical time, geometric seed budget, and dormant-return gain have an explicit proof under the new channels, including the formerly forbidden R=0 active face.

Still missing: the coefficient-one exponential-residual drift for the COMPLETE connector cycle and its phase-dependent outgoing forcing through the non-small d=0 Green operator. The isolated Green itself remains an unreviewed candidate. A norm bound C_theta on each block cannot replace the required drift margin, particularly for small theta. No full recurrence, all-exponential-moments, general weak reversibility, or historical novelty conclusion follows from this note.

Sources: prior exact local receipt `producer-workspace/INDEPENDENT_LOCAL_REVIEW.md`; prior working `DORMANT_WEIGHTED_GREEN_CANDIDATE.md` and `DORMANT_RETURN_POWER_GAIN_CANDIDATE.md`; primary-source scope note `PROFILE_PRIMARY_FRESHNESS_20261030.md`. Original frozen sources were not edited.
