# Fresh whole-proof review: homogeneous fast-connector family

Reviewed 2026-10-30 by `producer-workspace/review_chemical_global_foster`.

## Verdict and exact scope

**PASS for the exact frozen theorem in `FAMILY_THEOREM.md`.** For fixed integers k>=2 and q>m>=2, the homogeneous strongly connected composition graph containing all pure mX_i, the common qB catalyst, the connector `0->A+B->mA+qB->0`, and arbitrary fixed positive mass-action coefficients, the construction proves:

- nonexplosion from every nonnegative integer state;
- positive recurrence of every closed communicating class, with physical weak reversibility making all classes closed;
- every exponential moment of N+B under each class's invariant probability.

This is a fresh whole-proof check, not an inheritance of the child verdict. I read every load-bearing proof, independently reconstructed both traces and the correlated repair kernels, then compared the child audits. No frozen source file was edited. The strict-clearing dependency is the same exact V2 previously reviewed personally; its proof and scope were rechecked in this dependency chain. The broader all-face factorial argument is not a hidden prerequisite.

The theorem remains a restricted structural-family result, **not general weakly reversible recurrence**. Arbitrary time/state-dependent coefficients, q<=m, different connector geometries, and removal of the pure-complex/accessibility condition are not approved. **Novelty remains unverified.** Some family members are conventional deficiency-zero/product-form systems. `PRIMARY_APPLICABILITY.md` separately checks the strongest obvious primary criteria and methods.

## 0. Integrity and dependency closure

Frozen source: `producer-workspace/chemical_fast_connector_family_candidate_20261030`.

- Governing theorem SHA-256: `e14aa675f293d2f62f93e5c440daf33080c38ffb06eb8f7c029c4155c5783f17`.
- Source manifest SHA-256: `e2025ff2c64edfd4c21e0bdb4cf9e41408e696d24cd75a23b952d6e6bc33b586`.
- All 18 entries in that manifest verified. A copy is retained here as `SOURCE_SHA256SUMS.txt`.

Load-bearing proof files, under `proofs/`:

| File | SHA-256 |
|---|---|
| `STRICT_POWER_FAST_CLEARING_V2.md` | `99da4993b135ece91efe5d689d066e5985a2cd46aafff1d4c73c33ce551313dd` |
| `UNCAPPED_ACTIVITY_CREDIT_TRACE.md` | `cfe89dee337cd59845138aa4fa548c7da4d317edfe0278b5a279684ccae6d6ab` |
| `N_DIRECTED_RESET_WALK_V2.md` | `7d462ffb21e2ab248bbd7c95024efae6a995b2e8d8eb70bcaac920fbd9e09483` |
| `UNCAPPED_N_DIRECTED_VALUE_CANDIDATE.md` | `8e638fe1c219848b553cd921eba916b3de919c7eee41ea8c75bcc99bb8ab214d` |
| `GENERAL_FAST_CONNECTOR_RECURRENCE_CANDIDATE.md` | `bed8abcd3a74a23d1d8ac69784891853b6081bff67dd2b74bdb1887e4a8c780b` |

The included `UNIFORM_FAST_INTERIOR_AND_CLEARING_TIME_V2.md` supplies the family/small-state convention referenced by strict-power V2, not a prior mean bound. Old artificial-stop times, capped corners, entropy-selector arguments, and numerical kernel approximations are not used.

The earlier fixed-network whole receipt remains unchanged at `producer-workspace/INDEPENDENT_WHOLE_PROOF_REVIEW.md`, SHA-256 `7bd2ab1c58495998f58149663e38c11af89d9abfe3ba17e1c0f5d18f914ed8b9`. This receipt separately earns the larger scope rather than silently enlarging that one.

## 1. Nonexplosion and the actual clearing input

### 1.1 Independent nonexplosion

Let S=N+B. Fast reactions preserve S. The connector generator applied to 1+S is bounded above by

`C+C AB-c(A)_m(B)_q`.

If B<q, AB is at most a fixed multiple of N. If A<m, it is at most a fixed multiple of B. On A>=m,B>=q, fixed falling-factorial inequalities give `(A)_m(B)_q>=c'A^mB^q`. The latter dominates AB outside a bounded A/B region; hence the displayed expression is at most C(1+S). Finite-sublevel stopped Dynkin and Gronwall exclude escape to infinity in finite time. Since each finite set has bounded rates, this excludes explosion. Large populations in the other composition species cause no problem: their fast jumps conserve S.

This establishes full-process nonexplosion before any stopped value or recurrence assertion.

### 1.2 Strict clearing is an actual finite-shell theorem

For the homogeneous conservative subsystem, the previously checked V2 argument yields some fixed `0<epsilon<1` and

`sup_x E tau_clear <= C N^[-(m-1+epsilon)]/(B)_q`

for large N, B>=q, uniformly in composition. Its proof does not assume stationarity or mixing: from each initially dominant species, a fixed complex path produces the distinguished concentration with a uniform bound `z_A(t)>=ct^L`; consuming drift is bounded by Cz_A. For the rescaled chain `X(N^(1-m)t)/N`, falling-factorial drift differs from the polynomial ODE drift by O(1/N), and Doob plus Gronwall gives error probability `C(T/N+T^2/N^2)/eta^2`. Taking `T=N^-epsilon`, `eta~T^L`, with `epsilon=1/[4(mL+1)]`, gives vanishing error and actual cumulative killing hazard at least `cN^(3/4)`. Uniform block iteration then proves finite mean at the asserted scale without an older mean assumption. Fixed positive coefficients in a compact box give uniform constants; arbitrary state-dependent controls are not claimed.

Finite smaller **active states** can be included by increasing the constant. If a source y is enabled at x, a complex path from y to mA is enabled at `x-y+y_j`; at its end clearing is possible. The finite active part has no closed nonclearing class. Inactive small states are excluded from this estimate and are handled by actual connector races below. The preserved example `2A<->2C`, N=2, x=(1,1), confirms why a merely “active shell” would not suffice.

All uses of the resource factor occur at B>=q. Its vanishing at smaller B is never divided away.

## 2. Exact residual geometry

Put `h=q-m>0`, `nu=m-1`, and `a=nu/(q-1)<1`. Define activity I(x) to mean that a fast **composition source** is enabled, independent of B. An enabled fast reaction lands at a state enabling its target complex, and strong connectivity supplies its return path, so I is unchanged by every fast jump. Adding A cannot turn it off. Inactivity implies every composition coordinate is at most m-1, hence `N<=K=k(m-1)`.

For

`Z=B-N-hI`,

active activation raises Z by h; immigration turning activity on lowers it by h; clearing whose target stays active lowers it by h. All other jumps are neutral. Inactive activation adds m-1 copies of A, makes I turn on, and is exactly neutral.

For B>=1 write `B=u(q-1)+v`, with `1<=v<=q-1`, and set `H(B)=u(m-1)+v`, `H(0)=0`. Then

`H(B)-aB=(1-a)v`, so `0<=H(B)-aB<=h`.

For `r=N-H(B)`, activation is neutral. Immigration increases r by h exactly when B is a positive multiple of q-1. Clearing lowers r by h exactly at `B>=2q-1`, `B=1 mod(q-1)`; clearing q->0 is neutral. Fast reactions preserve r. These identities follow by the two cases v=1 and v>=2; no rate or composition approximation enters.

In particular N>=r in the large-r domain. At the pointwise section `S_q={B=q}`, N=r+m. At B=2q-1, every clearing before an immigration is a down-r exit, even after intervening activations.

## 3. The uncapped activity-credit value is earned

### 3.1 Uniform active episodes

At Z=z large, B=z+N+hI>=z. The clearing bound, including finite active states, gives

```
E(time to clearing or birth)<=C(1+N)^[-(m-1+epsilon)] B^-q,
P(birth before clearing)<=C(1+N)^(2-m-epsilon) B^(1-q).
```

Since m>=2, both are bounded uniformly in hidden N by `Cz^-q` and `Cz^[-(q-1)]`, respectively. These follow by additional killing or integrated competing hazards with birth rate at most C(1+N)B. No cap on N is used.

### 3.2 Finite head protocol covers inactive holes

Let `H_*=K+m`. If active N>H_*, the next clearing stays active and is a down-Z exit, with probability at least `1-Cz^[-(q-1)]` before a birth.

For the bounded head N<=H_*, prescribe clearing from an active state. If it is neutral, the target is inactive. From inactive A>=1, prescribe activation before immigration, then clearing before another birth. The activation race succeeds with probability at least `1-C/z`; the active clearing race has the preceding uniform bound. If both are neutral, their combined N change is -1. At most K such pairs reach inactive A=0 or a down exit.

At inactive A=0, immigration is compulsory. At most m-1 further immigrations are needed to make a pure mA source active, and each beats activation with probability at least c/z while still inactive. The immigration turning activity on is a down exit. Thus each fixed protocol block, stopped at the first failed prescribed choice or genuine residual exit, satisfies

```
P(down)>=c z^[-(m-1)],
P(up)<=C z^[-(q-1)],
E duration<=C.
```

Failures that do not exit are neutral and start a new block at the same z. Conditional renewal, not independence, gives expected block count `O(z^(m-1))`, and hence

`P(first Z exit up)<=Cz^-h`, `E tau_z<=Cz^(m-1)`.

The finite-state head is treated by explicit paths/races, not a table asserted for every graph. Neutral excursions are nonexplosive also directly: before a Z exit, active activation is forbidden, inactive activation lands at bounded N, and `N_t<=max(N_0,H_*)+J_I(t)` with J_I the constant-rate immigration Poisson count. The resulting B is bounded on each finite time interval. This agrees with the independent global localization above.

### 3.3 Stopped cost and threshold defect

For `phi(u)=(u!)^alpha`, 0<alpha<1, the up/down jumps ±h give contraction of both phi and `(1+u)^nu phi(u)` at large u, since the two terms are `O(u^[-(1-alpha)h])` and `O(u^-alpha h)`. Multiplying the mean excursion duration by phi pays the expected running cost. Conditional contraction bounds the sum of the enlarged weight and the number of residual excursions until a large threshold z0. Therefore the actual value W_Z is finite, uniformly in hidden composition, with

`W_Z<=C(1+Z)^nu phi(Z)`, `L W_Z=-phi(Z)` above threshold.

It is zero below threshold. Only active activation can enter its domain from outside, on `z0-h<Z<=z0`. Its target weight lies in a fixed finite band, so

`(L W_Z)^+<=C AB` on that strip and is zero below it.

The strip is infinite. Its defect is retained for the global comparison, not called a compact boundary.

## 4. Fast reset kernels: controlling correlations before normalization

In the large-r domain choose r0 so N>=r>r0 implies activity. Set

`d=nu+epsilon`, `p(r)=r^-d`, `beta(r)=p(r)^(1/m)`.

A fast stage ends at its first clearing or connector birth. Its immigration probability is at most `Cp(r)B^-q`; activation probability is at most `C r^[-(m-2+epsilon)] B^(1-q)`. Both tend uniformly to zero over B>=q.

For `f(A_after)=(1+A_after)^-m`, the clearing compensator and

`(A_before)_m/(1+A_before-m)^m<=C_m`

give, at every fully specified stage input,

`K_D f<=Cp(r)`,

where K_D is the subprobability output kernel for clearing before either birth. Also `K_D1>=1/2` for sufficiently large r, so the crucial stronger statement is

`K_D f<=2Cp(r) K_D1`.                                    (K)

### Why selected rare terminal phases remain controlled

The low-return phase and down-exit classification of a clearing are functions of the **pre-clearing B**, not A_after. Decompose any such terminal event by its final clearing-stage entrance state. Apply (K) at that entrance and then integrate over the entrance measure. The same relative inequality survives. Normalizing by even a very small total selected-event probability therefore retains the inverse-moment bound. Fixed residual changes r->r-h only alter its constant.

This does not condition on an observed A_after and claim a pointwise inverse-moment bound. Such a statement would be false. The construction only averages the actual clearing output inside a stopped kernel.

Without immigration, activation preserves B modulo q-1 and each clearing advances the clearing residue toward a low return, S_q, or down exit. At most q-1 clearings are needed. Since competing activation probability per stage is uniformly o(1), the number of stage events has a uniform geometric bound. Fast-processing duration is uniformly bounded, and total bad immigration probability is O(p). For activation from low phase b>=2, direct first clearing returns to b-1 with probability 1-o(1); other neutral low outputs are at most b-1. For b=1, activation enters S_q directly and repair stops. This special case is necessary and correctly retained.

## 5. Independent reconstruction of the low reset-walk estimate

At low phase b>=1, only immigration and activation act, and

`P(next jump immigration | A,b)<=C/(1+A)`.

Thus an immigration run of length ell has probability at most `C_ell(1+A)^-ell`. For a fresh clearing-output law satisfying the inverse m-moment bound, Holder's inequality gives

`P(run length at least ell)<=C_ell beta^min(ell,m)`.

These are **kernel bounds**, not unconditional probabilities multiplied after observing reset A. A composite kernel consists of a fast reset followed by a prescribed immigration run; its row mass, summed over admissible output phases and compositions, has this bound uniformly in the full pre-reset input. Property (K) also permits phase-selected outputs when needed. Products of positive-kernel operator norms therefore bound a specified run-length string.

The expected number of runs is uniformly bounded. Index at fast-episode entrances, before sampling reset output. If q consecutive run transitions contain no immigration, each reset lowers the low phase by at least one, forcing absorption. Consequently the surviving q-step kernel has row mass at most `q C beta<1/2` for large r. Its positive geometric series bounds expected runs; no conditional phase drift after observing A is assumed.

For an upward escape starting at b, if all n run lengths are below m, their sum must be at least `q-b+n-1`: each nonfinal reset lowers the phase by at least one. There are at most m^n strings, with joint mass at most `C^n beta^(sum ell)`. Their sum is bounded by

`C beta^(q-b) sum_(n>=1)(C' beta)^(n-1)`.

Any run of length at least m contributes O(p) times the bounded expected number of runs. Bad fast immigrations also total O(p). Therefore

`P(upward/bad escape)<=C p^(min(q-b,m)/m)`.

The auxiliary upper phase used in this enumeration depends only on previous run lengths, not on conditioning on a rare actual output phase. This resolves the correlation objection. The correct exponent is phase dependent: phases with q-b>=m earn p; a general fresh phase may only earn beta. From fresh B=0, compulsory neutral immigration gives phase 1, and q-1>=m guarantees the full p bound.

## 6. Weighted physical repair, including neutral bad events

Choose rational alpha with `0<alpha<1` and `rho=alpha h<epsilon`. The safe strict exponent has epsilon<1, hence `epsilon<d/m`; therefore

`r^-rho`, `beta(r) r^rho`, and `p(r) r^rho` all tend to zero.

Repair ends at S_q or at r<=r0. A round includes one fast-processing segment, if needed, **together with** the ensuing fresh low-phase walk. The potentially unit-mass neutral fast-to-low step stays inside the round. Only down exits and bad active states need another round; a low upward wrap lands directly in S_q. This composition is important: a unit fast-to-low transition alone is not a small continuation kernel.

Consider separately pointwise fast inputs and admissible fresh low-output laws. For a down continuation the weight ratio is `O(r^-rho)`. For an upward or bad branch it is at most `O(r^rho)`, while branch mass is at most O(beta), and O(p) on a fast bad branch. Each round has bounded expected duration at its initial residual, so its expected actual running phi-cost is at most Cphi(r).

For a formal construction, truncate after n rounds. Take the largest normalized expected terminal weight plus running cost over pointwise fast inputs and fresh low laws. The final-clearing disintegration ensures that any selected down-low output belongs again to the admissible law family. The truncated quantities satisfy

`M_n<=C+eta_0 M_(n-1)`,

where `eta_0<=C sup_(r>r0)[r^-rho+beta(r)r^rho+p(r)r^rho]<1/2`
after choosing r0. Thus their monotone limits are finite. The same continuation estimate bounds the expected sum of phi over round starts, and hence the number of rounds, since phi>=1. Each round takes finite actual time. This earns termination and running-cost finiteness; it is not a prior finite-return assumption. Neutral bad immigrations are actually continued from their physical states.

Consequently, from any fast input or fresh low law, repair terminal weight and running cost are at most Cphi(r). From an arbitrary observed low state, at most q low jumps precede first fast entry, their mean time is bounded by immigration's positive rate, and r can increase by at most h. Its initial-repair bound is therefore `C r^rho phi(r)`. No fresh-law premise is assigned to such an observed state.

### 6.1 The coefficient-one fresh B=0 bound

Start with a genuine fresh clearing law at B=0. Partition the first repair round into same-level S_q return, down continuation, and up/bad branches. Same-level terminal weight is **exactly** phi(r). A down branch has subsequent expected weight at most `Cphi(r-h)<=phi(r)` for large r. These two branch masses sum to at most one. The remaining mass is O(p), with future expected weight at most Cphi(r+h). Hence

`E phi(r_S)<= [1+Cp(r)r^rho]phi(r)`.                      (R0)

An arbitrary constant instead of the leading one would destroy the later small drift. The actual kernel decomposition retains that one correctly. R0 is not a pointwise claim for every B=0 composition.

### 6.2 The activation-branch improvement

From B=2q-1, every clearing before immigration is a down exit, independent of intervening activations. Bad immigration has total probability O(p). Applying the established fast/fresh-low repair bounds after those branches gives

`E phi(r_S)<=Cphi(r-h)+Cp(r)phi(r+h)=o(phi(r))`.           (R1)

For low outputs of a selected down branch, (K), before normalization, is what permits the fresh-law estimate. It is not a fabricated pointwise bound on A_after.

## 7. Pointwise section-return drift and actual cost

Start from any fully observed state on S_q, B=q, N=r+m. Wait for the first connector event, allowing every fast reaction. Write its probabilities as P_D,P_I,P_T. The clearing estimate gives `P_I<=Cp` and `P_D=1-o(1)`. Pointwise along the fast path,

`lambda_T>=c r^-nu lambda_D`,

because `(A)_m<=A N^(m-1)` where clearing is enabled, and the inequality is trivial where it is disabled. Integrating to the first connector event yields

`P_T>=c r^-nu P_D>=c' r^-nu`.

All three connector events from B=q preserve r. Clearing lands at B=0 with an actual fresh law, so R0 applies. Activation lands at B=2q-1, so R1 applies pointwise. Immigration lands at B=q+1, so the arbitrary-fast repair bound applies. Therefore

`E phi(r_next)/phi(r)
 <=1-P_T(1-o(1))+Cp(r)r^rho
 <=1-c r^-nu`,

since `p(r)r^rho=o(r^-nu)`. This inequality is conditional on the full incoming section state, which is enough to iterate the actual embedded chain.

The same branch argument applies to `Psi(r)=(1+r)^nu phi(r)`. Same-level returns still have ratio exactly one; only the already down or rare branches use fixed-shift estimates. It would be invalid to multiply the final small-drift inequality by a generic `1+O(1/r)` error when nu>1. The proof does not do that. Repeating the branch comparison gives

`E Psi(r_next)<=Psi(r)-c phi(r)`.

The expected **real-time** phi-cost of a section cycle is at most Cphi(r): the initial fast race and all three physical repair branches have the proved finite costs. Telescoping at finitely many section returns therefore bounds the total expected phi-cost until the threshold by CPsi(initial r). Because phi>=1, it also bounds the expected number of section cycles. The process reaches the threshold almost surely; neither an infinite succession of instantaneous trace events nor an infinite waiting time is assumed away.

Initial arbitrary-state repair adds at most `r^rho` to the profile. Thus the actual value

`W_r(x)=E_x integral_0^T phi(r(X_t))dt`, `T=inf{t:r(X_t)<=r0}`,

is finite with

`W_r<=C(1+r)^(nu+rho)phi(r)` uniformly in every hidden state.

Set W_r=0 below threshold. Since the value and stopped cost are finite and each state has finitely many outgoing targets, first-jump conditioning proves the exact physical identity `L W_r=-phi(r)` above threshold. Fast composition jumps are included in this identity; W_r need not be composition-invariant.

Only constant-rate immigration enters from the zero side, and its target r lies in a fixed h-wide band. The uniform profile therefore yields `(L W_r)^+<=C` there, with zero leakage further below. The noncompact stopping target has not been declared recurrent or finite.

## 8. Global coercivity, all cylinders, and invariant moments

At an initial state inside either stopped-value domain, its stopping time cannot precede the first physical reaction. Total intensity is at most `C(1+S)^(m+q)`, so

`W_r>=phi(r)/[C(1+S)^(m+q)]`,
`W_Z>=phi(Z)/[C(1+S)^(m+q)]`

in the respective domains. With bounded H/activity offsets, the exact linear identity

`(1+a)(B-N)+2(N-aB)=(1-a)(N+B)`

gives

`max(r,Z)>=(1-a)S/(3+a)-h`.

Hence V=W_r+W_Z is normlike: a factorial on a linear fraction of S dominates the polynomial first-holding denominator. Adding a constant if desired makes V strictly positive without changing drift.

If both residuals are above threshold, both generator terms are negative. In the Z entrance strip, r grows linearly with S and its negative factorial forcing absorbs CAB. In the r entrance strip, Z grows linearly and its negative factorial forcing absorbs the constant defect. Below an entrance strip the corresponding component has zero generator. If both residuals are below threshold, S is bounded. These cases cover all boundary cylinders and all unbounded simultaneous limits.

In particular, off a finite set, `LV<=-1`. More quantitatively, for every theta>0 there are finite K_theta and b_theta with

`LV<=-exp(theta S)+b_theta 1_(K_theta)`.

No angular selector, entropy mismatch, finite cap, or reflecting halo appears in this final comparison.

The full complex graph is strongly connected because the connector and fast graph share mA+qB. A physical reaction `z+y -> z+y'` has an enabled return path `z+y_j` along a complex return path, using the same nonnegative leftover z. Thus physical communicating classes are closed. Stopped Foster localization gives finite expected entrance into a finite set and classwise positive recurrence; it does not assume irreducibility of the whole lattice.

For stationary moments, let sigma be a finite-mean regenerative return time to a chosen state in a closed class, obtained from the finite-set return argument. Stop Dynkin additionally on finite sets and time bounds. Nonnegativity of V gives

`E integral_0^sigma exp(theta S_t)dt <= V(X_0)+b_theta E sigma < infinity`

after monotone/Fatou passage using nonexplosion. The regenerative occupation formula then yields the finite invariant moment. This avoids any assumption that the invariant law already integrates V. The conclusion is for each unique class invariant probability and every fixed theta>0.

## 9. Failures and restrictions preserved

- The uncorrected scalar composition residual still fails on the enlarged pure-triple graph at `(A,C,D)=(1,2,0)`, B large: fast channels and clearing are disabled, activation has rate proportional to B and produces an upward scalar move with probability tending to one. The activity indicator credit fixes the representation in the new construction; it does not make that old estimate true.
- The old reset note's time to an artificial bad-event stop is not an actual return time. Neutral bad immigrations are genuinely repaired here. The old claim remains superseded, not retroactively approved.
- A fresh inverse-moment law is not a pointwise statement after observing A_after. This proof uses relative clearing kernels and final-stage disintegration instead.
- The infinite Z threshold strip is not compact. Its CAB defect is paid by the other residual's factorial forcing.
- Small inactive shells and zero catalyst factors never receive an assumed clearing estimate. The Z protocol explicitly handles inactive states; r>r0 excludes them by population size.
- Earlier fixed-network balanced-ray and Green-entry failures remain preserved in their existing frozen receipts. This proof uses neither invalid kernel transport nor the old F-alone certificate.

## 10. Prior applicability is a separate verdict

The companion `PRIMARY_APPLICABILITY.md` documents the bounded fresh primary check. Pure-fast-complex-only members have deficiency zero and conventional product-form laws. For the larger family, ACK's general tier hypothesis fails on the reachable B=0 ray; ASE/ADE large-volume estimates do not become fixed-volume recurrence; the 2026 nonlinear first-order domination theorem requires a dissipative first-order subsystem absent here. Standard graph notions and stopping/Poisson/fluid/kernel tools are not new by being combined in this manuscript.

No checked primary theorem automatically replaces the whole positive-deficiency family proof, but this is not exhaustive novelty clearance. No external upload or publication was performed. No mathematical or source-integrity blocker remains in the exact reviewed scope.
