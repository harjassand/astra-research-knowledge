# Independent occupation/siphon-extension review

2026-10-30. Reviewer: `producer-workspace/review_chemical_global_foster`.

## Verdict

**PASS for the four exact new V1 proofs pinned below, under their explicit A-catalytic graph contract.** The local occupation comparison, refined first-reset estimate, actual seeding repair, complementary uncapped trace, and global Foster consequences close. This is a fresh mathematical review, not an extension by inheritance of the earlier pure-source-family verdict.

For fixed dimension d>=2 and integers q>m>=2, the fast composition graph must be finite, strongly connected and homogeneous of degree m. Every complex contains A; mA and every A+(m-1)X_i are present; each latter source has a positive-rate edge increasing A. All fast complexes carry the same qB catalyst. Add `0->A+B->mA+qB->0`, with fixed positive coefficients. The resulting chain is nonexplosive, its closed classes are positive recurrent, and every class invariant probability has all exponential moments of N+B. Constants are not dimension-uniform. Arbitrary state-dependent rates or arbitrary missing-source graphs are not covered.

The infinite inactive A=0 face is actually seeded by immigration. The proof does not assign a clearing estimate to that face, replace an actual activation occupation by N times a mean time, or declare a noncompact stopping target finite. A downward clearing followed by seeding can exactly undo its residual decrease; the proof survives only because the relevant inactive-output probability is bounded in the joint clearing kernel, before conditioning on that output.

**No generic weakly reversible recurrence or novelty upgrade is made.** The exact old pure-source whole receipt remains unchanged, SHA-256 `82477728ddeca23169366ea9cf9bd499c0468f0b79e81227bc1cb1d028e724d8`.

## 1. Exact-source closure

New source directory: `producer-workspace/chemical_missing_pure_source_20261030`. Author confirmed these four files immutable during review. Copies are retained under `inputs/`.

| New proof | SHA-256 |
|---|---|
| `LOCAL_OCCUPATION_LEMMA_V1.md` | `1ef571169e6fcf3900191fc66e7a0f9efe2dab2e25aef6fa39553ba6becffc9f` |
| `REFINED_FIRST_RESET_LEMMA_V1.md` | `e9539e173e62bf12f21829a62c72ccc8798e875aad08ad5b401090a1d5afce0e` |
| `ACTUAL_SEED_REPAIR_V1.md` | `d1cac65f06b50354ca95e7cdcc5da3c611af348a5e6b8d4f925db83d62031cd9` |
| `ACTUAL_SIPHON_Z_AND_GLOBAL_V1.md` | `2c3c93ba9a3a280cfc66ae6fd9054f588d3d12fb289dd81afff45688f11ea271` |

The only earlier mathematical import is the **abstract finite positive-kernel reset-walk argument** in `N_DIRECTED_RESET_WALK_V2.md`, SHA-256 `7d462ffb21e2ab248bbd7c95024efae6a995b2e8d8eb70bcaac920fbd9e09483`. I reread and rederived that argument with the new p, including correlations. Its old strict-power clearing premise and subsequent pure-source conclusions are not imported.

Earlier provisional synthesis files were read for context but are not proof dependencies. In particular, this review uses the exact new siphon-aware Z file rather than presuming that the old bounded-inactive-population premise still holds. No source file was changed.

## 2. Local occupation lemma: independent completion

Remove the common catalyst, fix the conserved N, and restrict to A>=1. All fast products contain A, so this set is fast-invariant. Let Q_N be its finite-state generator and kill at `k_D(A)_m+u+vA`, with u,v bounded nonnegative constants. Write T and U for actual expected time and A-occupation before this first killing.

### 2.1 Logarithmic drift and finite killing time

Every A jump j has bounded magnitude, with A+j>=1. Thus `|log(A+j)-log A|<=C_m/A`; this remains true at small A by enlarging the fixed constant. All sources contain A, so total jump intensity is at most `C A N^(m-1)`. Hence `|Q_N log A|<=C N^(m-1)` globally.

If A<=eta N for a sufficiently small fixed eta, some reservoir coordinate is at least `(1-eta)N/(d-1)`. Its required source A+(m-1)X_i is enabled for large N. Its A-increasing edge contributes at least `c A N^(m-1) * c'/A = c''N^(m-1)` to logarithmic drift, using a genuine lower falling-factorial bound on the reservoir count. An A-decreasing reaction has at least two source A molecules, since every product retains one. If its source A multiplicity is a>=2, its negative logarithmic contribution is at most `C A^(a-1) N^(m-a)<=C A N^(m-2)`. Summing and choosing eta small proves

`Q_N log A >= cN^(m-1)` for `1<=A<=eta N`.

Take `W=2log(N+1)-log A`, assigning zero at the cemetery. W is positive and at most 2log(N+1). At low A its killed-generator drift is at most `-cN^(m-1)`. At A>eta N the possible positive fast drift is O(N^(m-1)), whereas clearing contributes at most `-cN^m log(N+1)`. Thus the same negative bound holds everywhere for large N. Finite-state stopped Dynkin first up to tau wedge t, then monotone convergence, gives

`T <= C log(N+1)/N^(m-1)`.

No irreducibility or previously finite absorption mean is assumed here.

### 2.2 Mesoscopic survival and actual occupation

Put `gamma=(m-1)/(2m)` and `K=floor(N^gamma)`. For the unkilled chain starting at A<=K, stop at its first A>=K. Before this time the logarithmic drift lower bound applies; the stopped logarithm is bounded by log(K+m). Consequently its expected hitting time sigma is at most `C log(N+1)/N^(m-1)`, and sigma is finite. Before the hit, total killing intensity is at most `C(K^m+K+1)`. An independent integrated-hazard construction therefore gives

`P(killed before sigma) <= C K^m E sigma <= C N^[-(m-1)/2] log(N+1) = o(1)`.

At the hit, A lies within a fixed m-wide band around K. For an unkilled chain started in this band, exit from [K/2,2K] requires at least cK bounded jumps. Before exit, jump intensity is at most `C K N^(m-1)`. In time `t_N=c_0 N^[-(m-1)]`, its expected stopped jump count is at most Cc_0 K. Markov's inequality makes exit probability at most 1/4 by choosing c_0 small. The integrated killing hazard before exit or t_N is deterministically at most `C K^m t_N=o(1)`. Hence with probability at least 1/2 the actual killed process stays alive with A>=K/2 throughout that interval. Its expected occupation is at least

`c K/N^(m-1)`.

Strong Markov at the mesoscopic hit gives the same lower occupation bound for every A<=K. Combined with the time upper bound, this proves `T<=R_N U` there, where `R_N=C log(N+1)/K`. For A>K, stop at killing or first entrance into A<=K. Before that stop U_pre>=K T_pre; any entrance lands within m of K. Applying the already proved pointwise ratio at the entrance and choosing R_N>=1/K gives the identical ratio from all active starts. Thus

`T <= C N^-gamma log(N+1) U`.

Both estimates concern actual integrals up to the same killing time. No estimated mean population is inserted into a propensity.

### 2.3 Clearing probability and lower opportunity

The clearing compensator gives `E integral (A)_m <=1/k_D`. Since `A^m<=C[(A)_m+1]`, Holder on the finite occupation measure yields

`U <= C T^((m-1)/m)(1+T)^(1/m)=o(1)`.

The competing probability is exactly uT+vU, hence tends uniformly to zero. Clearing-first probability is therefore at least 1/2 for large N. Since `(A)_m<=N^(m-1)A`,

`U>=cN^[-(m-1)]`.

For physical B>=q, normalized competitors are `u=k_I/(B)_q` and `v=k_T B/(B)_q`, uniformly bounded. Both physical time and occupation are divided by (B)_q, so their ratio is unchanged. The lower opportunity estimate used later is at the fixed section B=q, where this factor is constant.

For smaller active states, an enabled complex y can follow the strongly connected path to mA through states x-y+y_j, then clear. Every finite active class therefore has finite killed mean. Smaller inactive states are not included in this claim.

## 3. The old strict-power premise is actually false here

At A=0, any N is possible, but every fast and clearing rate vanishes. Before physical immigration there is no clearing, so an unconditional all-composition fast-clearing bound is false.

Even restricting to active starts does not restore the earlier strict-power mean. Start at A=1, X_i=N-1 and all other reservoirs zero, for large N. Clearing is disabled. All enabled fast rates sum to at most `C N^(m-1)`; bounded normalized competitors add only O(1). The first holding time alone gives

`E tau >= cN^(1-m)`.

Thus no uniform `E tau<=C N^(1-m-epsilon)` for any epsilon>0 is possible. The new relative occupation proof genuinely removes a false premise, rather than weakening an available old estimate. This lower bound does not assert that the logarithmic upper bound is sharp.

## 4. Fast output kernels and refined first reset

Let `h=q-m`, `nu=m-1`, and use the exact residual r=N-H(B), where H(0)=0 and, for `B=u(q-1)+v`, `1<=v<=q-1`, `H(B)=u(m-1)+v`. Activation is r-neutral. Immigration raises r by h only at positive B divisible by q-1; clearing lowers r by h only at B>=2q-1 congruent to 1 modulo q-1. All other increments are zero. N>=r.

For large r set `p(r)=C log(2+r)/(1+r)^nu` and `beta=p^(1/m)`. The local lemma gives normalized active fast means at most p. By the occupation-Holder bound, the activation-before-clearing probability per fast stage is o(1), uniformly B>=q; immigration probability is O(p). This conclusion would not follow by replacing U with NT when m=2, and that replacement is not made.

At a fully specified active stage input, let K_D be the subkernel of clearing before either birth. The actual output moment obeys

`K_D[(1+A_after)^-m] <= C p`,

because `(A_before)_m/(1+A_before-m)^m<=C_m` and the clearing compensator bounds the integral by normalized time. Since K_D1>=1/2, this strengthens to the relative inequality

`K_D[(1+A_after)^-m] <= C p K_D1`.                 (K)

To condition on a selected terminal phase or downward clearing, disintegrate by its **final clearing-stage entrance**. The relevant phase/down predicate is a function of pre-clearing B, independent of the eventual A output. Apply (K) before normalization and integrate over entrance states. The same relative estimate survives even for a rare selected terminal event. It is not valid to observe A_after first and claim the moment bound pointwise.

Activation preserves B modulo q-1; in the absence of immigration, at most q-1 clearings lead to a low phase, the section, or a downward exit. Additional activations have uniformly small per-stage probability, giving bounded expected stage count. A high-B inactive output is a new designated bad branch of mass O(p), not another active fast input. Good low outputs have phase no greater than the launch phase minus one, with their full joint moment law retained.

At low b>=1, immigration wins the next race with probability at most `C/(1+A)`, including A=0. A run of ell immigrations therefore has probability at most `C_ell(1+A)^-ell`. A fresh output moment p implies run mass `C_ell beta^min(ell,m)`. Composite positive kernels are indexed **before the reset output is observed**. Their operator row bounds multiply; correlated output phase and A are not replaced by independent marginals. After q consecutive zero-immigration transitions the phase has fallen to absorption, so the surviving q-step kernel has row mass O(beta). This bounds expected runs. Enumerating short run strings, any n-run escape from b needs at least q-b+n-1 immigrations; summing their masses and adding long runs gives

`P(upward/bad escape from fresh phase b) <= C p^(min(q-b,m)/m)`.

Now distinguish the first B=0 clearing-output subprobability law nu_0, with inverse m-moment at most t and mass at most one. Its compulsory immigration increases A and preserves that moment bound. A zero-length further run activates straight from B=1 into B=q and is safe. A run of at least m additional immigrations costs O(t); any earlier upward escape lies in that event because q-1>=m. For `1<=ell<m`, the first-run mass is at most `C t^(ell/m)`. Its activation launches at b=ell+1. The subsequent uniform processor is bad with probability O(p), or resets at phase <=ell, or exits down. Its remaining escape probability is at most

`C[p+p^(min(q-ell,m)/m)] <= C p^((m+1-ell)/m)`.

The latter bound is pointwise at the new fast entrance, before its reset is sampled; integrating against the first-run entrance kernel is legitimate. Therefore

`E(t,p):=P(upward/bad escape) <= Ct+C sum_(ell=1)^(m-1) t^(ell/m)p^((m+1-ell)/m)`.       (R)

At an active section state B=q, its first output satisfies t<=CT, and the first activation probability is exactly k_T q U. Set `e_N=C N^-gamma log(N+1)` and `u_N=cN^-nu`. Using T<=e_N U and U>=u_N, each cross term of (R), divided by U, is at most

`C e_N^(ell/m)(p/u_N)^(1-ell/m)p^(1/m)`.

Relative to e_N its N power is `gamma(1-ell/m)-nu/m<0`, with only fixed logarithmic factors. Thus `T+E(t,p)<=C e_N U`. The distinction between the first actual law t and later worst-case p is essential.

## 5. Actual seeding repair and the downward-cancellation trap

Choose `rho=alpha h` with `0<rho<gamma` and phi(r)=(r!)^alpha above a large positive threshold. Large-r inactive states have exactly A=0. At such a state all channels except immigration vanish. One actual immigration waits mean 1/k_I, creates A=1 and an active state, and raises r by either zero or h. It costs real time; an arbitrary inactive initial state pays the initial factor O(r^rho).

**Explicit pointwise obstruction.** Take pre-clearing B=2q-1 and A=m, with a sufficiently large reservoir population. Clearing leaves A=0, B=q-1 and r reduced by h. Its compulsory immigration then raises B to q, turns activity on, and raises r by h, exactly restoring the original r. Conditional on this output there is no `O(r^-rho)` repaired downward weight. This old pointwise margin is false.

The correct joint estimate is different. A selected downward clearing obeys (K) before its A output is observed. Its high-B inactive-output mass is at most Cp times the selected down mass. Split the joint kernel:

- Active high-B outputs repair with factor `C phi(r-h)/phi(r)=O(r^-rho)`.
- Inactive high-B outputs have relative mass O(p), then physically seed; their post-seed weight is at most the original phi(r), with bounded mean seeding time. Their coefficient is O(p), not a negative-shift ratio.
- Low outputs retain their entire conditional fresh joint law, including A=0, and have the established fresh-low repair bound at r-h.

Thus the downward continuation coefficient is `O(r^-rho+p)`. No bound is conditioned on the observed inactive output and then incorrectly multiplied back as if independence held.

A repair round combines an active fast processor with the ensuing fresh low walk. The unit-probability neutral fast-to-low transition stays inside the round. Upward low wrap reaches the active section B=q directly. Continuations are down outputs, bad immigrations, or rare high-B inactive outputs with their physical seed. The fresh-low bad/up mass is O(beta); fast bad mass is O(p). Their fixed upward weight cost is O(r^rho). Together the continuation norm is bounded by

`C sup_(r>r0)[r^-rho+p+beta r^rho+p r^rho]`,

which tends to zero because rho<gamma=nu/(2m)<nu/m. Within-round real running cost is at most Cphi(r): low waiting times have an immigration floor, fast stages have bounded means and bounded expected count, and every seed has a constant mean. Truncating after n rounds gives `M_n<=C+eta M_(n-1)` with eta<1/2, over pointwise active inputs and admissible fresh low laws. Monotone positive-kernel iteration earns finite repair terminal weight and running cost, both at most Cphi(r). The same iteration bounds expected rounds; it does not assume finite repair in advance. An arbitrary low or inactive initial state pays at most the single initial O(r^rho) factor.

For the first clearing branch from the section, same-level return contributes exactly phi(r). Safe downward branches have repaired weight at most `Cphi(r-h)+Cp phi(r)<=phi(r)` for large r. These masses are paid with coefficient one, while genuinely bad/up branches have mass (R). Therefore the first-clearing contribution is at most

`P_D phi(r)+C E(t,p) r^rho phi(r)`.

An activation first enters B=2q-1. Clearing before immigration is a down event regardless of intervening activations; the corrected joint estimate gives repaired weight at most

`C[phi(r-h)+p phi(r)+p phi(r+h)]=o(phi(r))`.

Immigration first has probability k_I T and leads to an active fast input with bounded repair weight. Thus, using the actual P_T=k_T q U,

`E phi(r_next) <= [1-cU+C e_N r^rho U]phi(r) <= [1-c' r^-nu]phi(r)`.

This is pointwise in the full active section state, where N=r+m. Repeat the branch argument for `Psi(r)=(1+r)^nu phi(r)`: same-level coefficient remains exactly one, and only down/rare fixed shifts receive polynomial ratios. One must not append a generic O(1/r) relative error to the small r^-nu drift. The correct branch proof gives `E Psi_next<=Psi-cphi(r)`.

Actual section-cycle phi-cost is at most Cphi(r). Telescoping and the initial repair therefore construct the physical value

`W_r=E integral_0^{tau_{r<=r0}}phi(r_s)ds <= C(1+r)^(nu+rho)phi(r)`.

Finite expected section cycles and finite real costs earn threshold hitting. First-jump conditioning gives `LW_r=-phi(r)` above r0. Only constant-rate immigration can enter the positive domain from below, into a fixed h-wide band; the uniform value profile gives bounded exterior leakage. The target is noncompact, but no recurrence property of that target is assumed.

## 6. Siphon-aware uncapped Z construction

Let I indicate that a composition source is enabled and `Z=B-N-hI`. Fast jumps preserve I; adding A cannot disable it; an inactive activation creates m or more A and turns it on. Inactive A>=1 states satisfy

`N<=K=(m-1)+(d-1)(m-2)`,

since A<m and every reservoir count is <m-1. Inactive A=0 states can be arbitrarily large and are treated separately. For N>K, one immigration from A=0 necessarily makes a source active.

The exact nonzero Z jumps are +h for active activation, -h for immigration turning I on, and -h for clearing whose target stays active. Clearing landing inactive is neutral. These identities retain the activity credit when crossing the fast siphon.

Normalized clearing mean is uniformly bounded over all active states, by the new large-N estimate and finite active-state path arguments. The clearing compensator and `A<=C[1+(A)_m]` likewise give a uniformly bounded normalized A-occupation. Restoring the catalyst gives, uniformly in hidden N,

`P(immigration first)<=CB^-q`, `P(activation first)<=CB^(1-q)`, and `E(first connector time)<=CB^-q`.

This uses U directly; `N*T` would not provide the required uniform estimate.

At Z=z large, B>=z. If active N>K+m, prescribe clearing before a birth, with probability 1-O(z^(1-q)). An active target exits down immediately. An inactive target has N-m>K, so A=0; its actual next immigration has constant mean and activates, exiting down. A large initially inactive state is handled by that same single immigration. Thus the entire large-N tail has a near-one downward block, including its real seeding time.

The bounded head uses clearing from active states, or activation then clearing from inactive A>=1. A neutral pair lowers N by one. After a bounded number of pairs it reaches down exit or inactive A=0. At A=0, at most m immigrations suffice to activate mA; the first is compulsory, and each later prescribed immigration beats activation with probability at least c/z while the head is bounded. A failure stops the block; if no residual exit occurred, it restarts at the same z. Thus every block has

`P(down)>=cz^-nu`, `P(up)<=Cz^[-(q-1)]`, `E duration<=C`.

Conditional renewal, not independent blocks, gives actual residual-exit estimates `P(up)<=Cz^-h` and `E sigma_z<=Cz^nu`. Factorial fixed-shift ratios imply contraction of both phi(z) and `(1+z)^nu phi(z)`. Positive iteration constructs

`W_Z<=C(1+Z)^nu phi(Z)`, `LW_Z=-phi(Z)` above z0.

Only active activation enters from below threshold, into a fixed band. Hence exterior positive drift is at most CAB on the **infinite** threshold strip, and zero further below. This defect is not treated as compact.

## 7. Independent nonexplosion, global drift, closed classes and moments

Establish nonexplosion before using either stopped-value consequence. For S=N+B the fast part preserves S and

`L(1+S)<=C+CAB-c(A)_m(B)_q<=C'(1+S)`.

When A<m or B<q, AB is at most a constant times S. On the complementary quadrant fixed falling-factorial lower bounds make the negative product dominate AB outside a bounded A/B region. Finite sublevels and stopped Gronwall exclude finite-time escape; finite sets have bounded total rates, so the unrestricted process is nonexplosive.

For either stopped value, the first physical holding interval supplies a lower bound `phi(residual)/[C(1+S)^(m+q)]` when its residual is above threshold. With `a=(m-1)/(q-1)<1`, r=N-aB+O(1), Z=B-N+O(1), and

`(1+a)(B-N)+2(N-aB)=(1-a)(N+B)`.

Therefore `max(r,Z)>=(1-a)S/(3+a)-C`, and V=W_r+W_Z is normlike. If both residuals are high, both drifts are negative. If Z is below threshold at large S, r is a linear fraction of S and its negative factorial absorbs the CAB strip leakage. If r is below threshold, Z absorbs the bounded leakage of W_r. Both residuals bounded above imply bounded S. Thus every theta>0 admits a finite F_theta and b_theta such that

`LV<=-exp(theta S)+b_theta 1_(F_theta)`.

These cases include all boundary cylinders; neither component alone is claimed normlike.

The countable locally finite, nonexplosive Foster argument gives positive recurrence of each closed communicating class. In fact the shared complex mA+qB makes the full graph strongly connected; every enabled reaction has a physical return path x-y+y_j, so its communicating classes are closed, without global irreducibility. For each positive recurrent class, choose a finite-mean regenerative return time sigma. Localized Dynkin, nonnegativity of V, nonexplosion and Fatou/monotone passage give

`E integral_0^sigma exp(theta S_t)dt <= V(X_0)+b_theta E sigma < infinity`.

The regenerative occupation formula yields the invariant exponential moment. This does not assume the invariant law already integrates V. Finite classes are immediate.

## 8. Scope and preserved failures

- The A=0 fast siphon, failure of all-state clearing, and impossibility of a uniform active strict-power mean are retained explicitly.
- The down-clearing/seed cancellation is an actual counterexample to a pointwise repaired-downward margin. Only its rare joint-kernel mass is controlled.
- No reset moment is asserted after conditioning on an observed A output. Rare terminal phase selection is handled before normalization.
- Artificial bad-event stops are not returns: the new proof physically continues bad immigrations and inactive outputs, including their holding times.
- Small inactive A>=1 states are confined to the explicit finite head; the unbounded A=0 tail is never called finite.
- Previous pure-source and fixed-network counterexamples and receipts remain unchanged. The new proof does not revive their failed bounds.

This mathematical acceptance is not novelty clearance. Standard mass-action/weak-reversibility notions, Foster localization, killed occupation identities and positive-kernel arguments remain standard tools. No new broad primary-applicability claim is inferred from this proof review. No external upload or publication occurred. No mathematical or exact-source blocker remains within the stated four-file scope.
