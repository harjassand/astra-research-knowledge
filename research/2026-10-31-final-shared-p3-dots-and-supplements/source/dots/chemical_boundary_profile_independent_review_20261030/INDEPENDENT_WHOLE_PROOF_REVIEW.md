# Independent whole-proof review: incoming composition profiles

2026-10-30. Reviewer: `producer-workspace/review_chemical_global_foster`.

## Verdict: distinguish the actual versions

**Frozen five-file V1: NEEDS REPAIR.** Its stopping list omits a low-phase immigration that enters an inactive high-B state. The next activation there is not rare, so the stated high-activation enumeration is not justified on that branch. This is a proof-coverage counterexample, not a transience result.

**Exact six-file V2, including `PROFILE_INACTIVE_WRAP_REPAIR_V2.md`: PASS**, with the completing arguments below. The actual incoming inverse-A profiles, weighted bad-return contraction, composition-dependent section correction, real stopped costs, complementary infinite-strip value, nonexplosion, closed-class positive recurrence and invariant exponential moments all close for the explicit multi-seed contract. The abstract Neumann hypothesis is earned from reaction kernels, not supplied as an assumed hard-return bound.

This is not a general weakly reversible recurrence theorem or novelty clearance. Previous pure-source and one-seed receipts are unchanged. In particular the scalar time/occupation gap remains false on the explicit obstruction class; this proof does not revive it.

## 1. Exact closure and scope

The frozen V1 source is `producer-workspace/chemical_boundary_profile_candidate_20261030`. Its five entries were verified against `INPUT_SHA256SUMS`. The only addition is the immutable V2 wrap repair from `producer-workspace/chemical_missing_pure_source_20261030`. Pinned copies of all six files are under `inputs/` here.

| Source | SHA-256 |
|---|---|
| `PROFILE_MECHANISM_GLOBAL_CLOSURE_CANDIDATE.md` | `4adc7f967f57edff000a5a8e796c2dff07881ab7875dd528cce36e5abf081d40` |
| `FULL_CYCLE_INCOMING_PROFILE_CANDIDATE.md` | `4c128934cc147a36f3527aacb7ab7c7346cdc21c36322a03ea3631616016c037` |
| `BOUNDARY_RETURN_NEUMANN_PRINCIPLE_V1.md` | `348fd50b6bd95547baa826d0e03e6ff80cc5b5437a06707f191514e3fe310109` |
| `INCOMING_MOMENT_MEMORY_LEMMA_CANDIDATE.md` | `90c94b4f707d00778ed65e589cd16f2984965ad382f9dd1f256132e15c0b43ed` |
| `GENERAL_BOUNDARY_POINTWISE_GAP_OBSTRUCTION.md` | `82085784b13f38003460ecf305de8d0a399fb833dd901ddc36d9e20e99a71034` |
| `PROFILE_INACTIVE_WRAP_REPAIR_V2.md` | `683a07de87af10e3562eee0c41235713b961e02a0f87be5f584ea8ada3a626e0` |

Contract: fixed d>=2, integers `2<=a0<m<q`, `v=m-a0>0`, fixed positive coefficients. The finite strongly connected fast composition graph is homogeneous of degree m; every complex contains at least a0 A; it contains mA and every a0 A+vX_i; each latter source has an immediate A-increasing edge. All fast complexes carry common catalyst qB. The connector is `0->A+B->mA+qB->0`. No dimension-uniform constants, arbitrary state-dependent rates or other missing-source graphs are approved.

Outside this closure only the explicitly rederived connector residual algebra and ordinary localized CTMC arguments are used. Neither an earlier pure-source clearing theorem nor the one-seed scalar-gap theorem supplies the new profile estimates. No source byte was edited.

## 2. The scalar-gap obstruction really holds

For `3A+2C <-> 4A+C <-> 5A`, take fast coefficient pairs (2,1), (1,3), fixed B=q>5, and start at A=3, C=N-3. Clearing is disabled. Total initial rate is O(N^2), so the first holding time gives `T>=cN^-2`.

For the normalized killed chain on A>=3, at A<=eta N the A-increasing source contributes rate at least cA^3N^2, and the negative increment of 1/A has size at least c/A^2. A-decreasing sources have an additional A/N factor. Thus `Q(1/A)<=-cAN^2` for sufficiently small eta. At A>=eta N, `|Q(1/A)|<=CN^3`. For `F=C/(AN^2)+C'/N^4`, low-region drift pays cost A; in the high region clearing contributes order -N^2, dominating possible +O(N) fast drift and the cost A<=N. Competitor killing only helps. Finite-shell Dynkin gives `U<=F(3)<=CN^-2`. Hence `T/U>=c0>0`.

The full graph has five complexes, one linkage class and stoichiometric rank three, hence deficiency one. Complex balance along the first fast edge would require A/C=2, and along the second A/C=1/3. Connector balance at 0 and A+B makes its net contribution at 5A+qB zero, so it cannot reconcile them. This is not automatically a product-form member. None of these facts implies transience; they only rule out the universal scalar-gap premise.

## 3. Exact V1 missing branch and V2 repair

In the same m=5,a0=3 example, start on the active section B=q with A=3. Activation gives B=2q-1,A=7. Two enabled reverse 5A->4A+C fast firings can reach A=5, and clearing then gives B=q-1,A=0. A low-phase immigration produces B=q,A=1<a0. This state is **not** the active section `{B=q,A>=a0}`. Its fast chemistry and clearing are disabled. Its next activation has probability `k_T q/(k_I+k_T q)>0`, independent of large N, rather than a vanishing rare-fast-event bound.

V1 designated inactive high-B **clearing outputs**, but not this inactive low-wrap entrance. Applying its high-activation rarity estimate here would be false. The author confirmed this omission and preserved V1 unchanged.

V2 stops and designates every inactive high-B entrance before any subsequent activation. At the newly covered wrap, A_pre<=a0-2, so

`1_{inactive wrap} <= (a0-1)^m (1+A_pre)^-m`.

Its entire subkernel can therefore be charged to the incoming inverse-m profile; no small probability is claimed after observing that low-A state. From A<a0, at most a0 actual immigrations, or an earlier activation, make the fast graph active. All waiting times have an immigration-rate floor; activation increases A by m-1 and helps. Upward residual displacement is bounded by a fixed multiple of h=q-m. Thus the new branch has the same O(t) profile charge and bounded weighted continuation as the other designated events. The following review uses precisely this corrected stopping rule.

## 4. Local incoming-profile estimates

Write `f_s(A)=(1+A)^-s`. On A>=a0, every fast jump preserves that lower bound. At A<=eta_s N an anchor source a0 A+vX_i, with X_i a macroscopic reservoir, gives negative f_s drift of order `A^(a0-s-1)N^v`. Every A-decreasing source has A multiplicity at least a0+1, so its positive contribution is smaller by O(A/N). Falling factorials are bounded below by fixed multiples of powers for A>=a0 on the anchor propensity. Thus

`Qf_s<=-c_s A^(a0-s-1)N^v` in the low region,
`|Qf_s|<=C_s N^(m-s-1)` in the high region.

For clearing terminal reward `g_s(A)=(1+A-m)^-s`, choose `F_s=C1 f_s+C2 N^-s` with C1>=(m+1)^s. Then g_s<=C1 f_s. With clearing killing k_D(A)_m,

`(Q-k_D(A)_m)F_s+k_D(A)_m g_s<=0`

for large N: low-region Qf_s is negative, and high-region killing of C2N^-s has order N^(m-s), one power above the possible positive fast drift. Finite-state killed Dynkin gives the joint clearing-output moment `<=C_s f_s(A_in)`.

Immigration and activation increase A. Adding their terminal f_s rewards subtracts `lambda(F_s-f_s(A_after))>=0` from the same inequality. Hence the **full first-connector kernel**, not only the clearing kernel, satisfies

`E[f_s(A_after); first connector event]<=C_s f_s(A_in)`.       (M)

For every rare connector subevent with probability <=epsilon, Cauchy–Schwarz and (M) at 2s imply its f_s-weighted mass is at most `C_s sqrt(epsilon) f_s(A_in)`. This is a profile norm estimate, not a conditional output claim.

Two genuine time bounds are also available. The same killed supersolution with s=m gives `T<=C f_m(A_in)`: below A=m its negative fast drift is large; above m the clearing term `(A)_m f_m` is bounded below; in the high region any positive Qf_m is O(1/N). Separately, `F=N^-v A^(1-a0)` has negative low-region generator bounded away from zero, since its derivative cancels the A^a0 source factor. In the high region QF=O(1), whereas clearing kills it at order N. Thus

`T<=C N^-v A^(1-a0)<=C N^-v=:p0(N)`.

Clearing output has inverse-m moment <=Cp0 by its compensator. Holder on the killed occupation measure, using `A^m<=C[1+(A)_m]`, gives U=o(1) uniformly and clearing-first probability 1-o(1). Restoring the catalyst makes normalized competitors uniformly bounded for B>=q, so all these assertions and the rare-high-activation profile bound are uniform in B. Every use is restricted to active large-N states; finite active states are handled separately when needed.

## 5. Whole-cycle profile transport is a positive-kernel calculation

Use the exact r=N-H(B), where H(0)=0 and `H(B)=u(m-1)+b` for `B=u(q-1)+b`, 1<=b<=q-1. Activation is neutral; immigration raises r by h exactly at positive multiples of q-1; clearing lowers it by h exactly at B>=2q-1 congruent to 1 modulo q-1. N>=r.

Fix large r0, `p0(r)=Cr^-v`, and stop the profile processor at section return, threshold, m counted noncompulsory low immigrations, a fast immigration, or any inactive high-B entrance under V2. Its initial B is bounded in the applications before the extra-high-activation history is accounted for.

The nonnegative phase height

`J(B)=B-(q-1)1_{B>=q}`

is unchanged by a low activation, increases by q-1 under a high activation, decreases by at least one under clearing, and increases by at most one under immigration. Each nonterminal visit to B=0 must consume a noncompulsory immigration: after its compulsory immigration, immediate activation would reach the active section. Thus before the m-th counted immigration the number of compulsory ones is bounded too. The total connector count is at most `C+C_q T_high`, where T_high counts high activations from **active** inputs. V2 stops before any inactive high activation, so none is falsely assigned a rare factor.

For a path with k such high activations, ordinary first-event profile operators cost at most a fixed C_s per stage; each high activation costs C_s sqrt(epsilon(r0)); low activation only decreases f_s. The number of event-type strings grows exponentially in k, while stage count is O(1+k). Choosing r0 large makes the sum geometric. This proves bounded full-processor profile norms for every fixed exponent needed below. No incoming A is forgotten at a reset.

At positive low B, one immigration race maps f_s to at most `C f_(s+1)`, because its race probability is <=C/(1+A) and immigration increases A. Work backward through the actual operators, spending one inverse power at each counted immigration and transporting the remaining power with (M). Reaching m counted immigrations costs C f_m of the first input. A fast immigration costs C f_m by the incoming-dependent mean bound. An inactive clearing costs C f_m by (M); the new inactive wrap costs C f_m by its indicator bound. Event strings before these stops are the same geometrically summable family. Exponents stay in a fixed finite range, so r0 can be chosen for all of them simultaneously.

Consequently, for a first clearing-output subprobability law nu with `int f_m dnu=t`,

`P(designated stop before section return)<=C t`.          (E)

This is repeated composition of actual joint kernels, not multiplication of unconditional reset marginals.

### An exact count supplies the first-branch coefficient one

Starting at B=0, let I,D be total immigrations and clearings, and ell the counted noncompulsory immigrations. If B>0, direct connector algebra gives

`r-r_start=h floor((I-D-1)/(q-1))`.

The compulsory count is at most D+1, so I-D-1<=ell. At B=0 the corresponding count is at most D and gives the same upper conclusion. Therefore while ell<m<=q-1,

`r<=r_start`.

This is stronger than merely bounded upward displacement. On an undesignated first-clearing path, terminal weight never exceeds its initial exponential weight. Only the O(t) designated part needs an arbitrary repair constant. That proves the exact leading coefficient one in the first-clearing contribution.

## 6. Actual exponential repair, including its near-one coefficient

Let w(r)=exp(theta r), theta>0. A physical repair round groups neutral active fast processing with its fresh low walk. It ends at active section/threshold, first down continuation, or a designated bad continuation. At most q-1 clearings are needed for a down/low outcome without immigration; repeated high activations have geometrically bounded count. Fresh low laws have inverse-m moment Cp0, so the finite phase/run kernel bounds their upward/bad probability by O(p0^(1/m)). Include every inactive high entrance, with its actual finite seeding wait. No low or inactive observed state is assigned a pointwise fresh-law bound.

Uniformly above r0, the bad-round probability is eta0->0 as r0 increases. A good continuation lowers r by h. A bad continuation, including seeding, raises r by at most a fixed Lh. Within-round real w-cost is at most Cw: low waits have an immigration floor, fast stages have bounded means and bounded expected count, and seeds have bounded mean. Truncated positive-kernel iteration with continuation coefficient `exp(-theta h)+C_theta eta0<1` earns finite actual cost and terminal weight. Arbitrary initial low/inactive states have a bounded initial number of races/seeds and only a fixed exponential multiplier.

For the required **near-one terminal bound**, fix u>0 so `(1+u)exp(-theta h)<1`. Assume inductively the truncated continuation value is <=(1+u)w. Good terminal/down branches then contribute at most their total mass times w. A bad branch contributes at most `(1+u)exp(theta Lh)w`. Thus the new terminal value is at most

`[1+eta0((1+u)exp(theta Lh)-1)]w <=(1+u)w`

after raising r0. Monotone iteration proves this bound. It is separate from the generally larger running-cost constant. In particular a repaired down branch has expected terminal weight strictly below w, and an activation-first branch can retain a fixed theta-dependent negative margin. Replacing this by an unspecified `C exp(-theta h)` would not suffice.

The same arguments apply directly to fixed polynomial enlargements `(1+r)^j w` and to `r^-v w`: choose r0 so they are increasing and their fixed down-shift ratio remains strictly below one. No differentiation of a constructed correction is used.

## 7. Bad-entry estimate, including unbounded first-clearing B

On the active section B=q, N=r+m. The first clearing output satisfies `t<=C T` by the actual compensator at this fixed B. Along undesignated paths, the profile transport gives terminal f_m moment <=Ct. For `K(r)=r^gamma`, the bad-section indicator `1_{A<=K}` is bounded by C K^m f_m. Since r can increase by only a fixed amount before designation, K at the terminal state is at most a fixed multiple of K(r). The designated continuation costs C_theta t w by (E) and the actual repair. Thus the clearing-first bad-entry contribution is at most `C_theta K^m T w`.

The first immigration branch has mass k_I T and bounded weighted continuation. The first activation has mass k_T q U and enters B=2q-1. Prior to its first clearing there may be arbitrarily many further high activations. Their history cannot be discarded. Starting from B=2q-1, a history of k such activations increases the phase height by O(k); the subsequent ordinary profile constant grows at most exponentially in k. Each preceding active high activation supplies its rare profile norm, so the history sum is geometric. At each actual pre-clearing entrance, the inverse-m output bound Cp0 holds relative to clearing mass; normalize only after disintegrating by that entrance. Hence the activation-first bad-entry contribution is at most `C_theta K^m p0 U w`. Its preceding fast-immigration and inactive-output branches fit the same order after real repair.

The resulting actual whole-cycle kernel P satisfies

`P[w(r_next)1_bad] <= C_theta K^m [T+p0 U]w(r)`.        (Bentry)

For g(r)=r^-v, the same shift-wise argument with gw gives an extra factor Cg(r), not a changed reset law. Downward motion is harmless because gw is increasing above r0; designated continuations use its separately earned repair bound.

## 8. Good-region occupation and earned Neumann contraction

Choose `0<gamma<eta<v/(v+1)` and also gamma<v/m. For K<=A<=M=N^eta, over time `c/[A^(a0-1)N^v]` a bounded-jump counting estimate gives a fixed positive probability of staying in [A/2,2A]. Clearing integrated hazard there is O(A^(v+1)/N^v)=o(1); bounded normalized competing hazards are also o(1). Thus `U>=c A^(2-a0)N^-v`. Combining with the actual mean bound gives `T/U<=C/A<=C/K`.

For A>M, stop at killing or first entrance below M. Prior occupation is at least M times prior elapsed time; any entrance lands within a fixed distance of M. Strong Markov extends T/U<=C/K to all good inputs. No vanishing ratio is asserted for bounded A.

The uncorrected section drift is

`Pw-w <= [-c_theta U+C_theta T]w`.

Indeed the first-clearing safe paths have coefficient one by the exact count above; their designated cost is CT. First immigration also costs CT. Activation-first produces a down clearing before immigration, and the near-one actual repair gives a strict fixed discount; its rare inactive/immigration exceptions vanish with p0. This earns the negative U term instead of assuming it.

On the bad section A<=K, T<=Cp0 and (Bentry) give the restricted bad-return norm in weight gw at most `C K^m p0(1+U)->0`. On the good section, (Bentry) and T/U<=C/K give correction leakage relative to U w at most

`C[p0 K^(m-1)+p0^2 K^m]->0`.

These are the difficult hypotheses of the Neumann principle, now derived. For D0 exceeding the bad scalar-drift constant, define

`H=sum_(n>=0) P_bad^n[D0 g w]` on bad states, and H=0 on good states.

The earned norm <1 proves convergence and H<=Cgw. On bad states `PH-H=-D0gw`, giving negative corrected drift. On good states the preceding leakage estimate is absorbed by -c_theta U w. H retains full incoming composition through the actual return kernel; it is not a supplied invariant phase law.

Repeat the construction directly for every polynomial enlargement. Clearing-first probability tends to one and `(A)_m<=N^(m-1)A` gives `U>=c r^[-(m-1)]` on every active section state. Also g>=c r^[-(m-1)]. Taking j=m-1 yields corrected section drift at most -c exp(theta r). Actual full-cycle exp(theta r)-cost is at most C exp(theta r), by the proved processors and real repair. Telescoping the full-state section chain constructs

`W_r=E integral_0^{tau_{r<=r0}}exp(theta r_s)ds <=C(1+r)^(m-1)exp(theta r)`.

The same estimates bound expected cycles and repair rounds, so termination is earned, not inferred from finite cost alone. First-jump conditioning gives `LW_r=-exp(theta r)` above threshold. Constant-rate immigration is the only entrance from below, into a fixed band, hence exterior leakage is uniformly bounded. The threshold target is noncompact.

## 9. Infinite inactive strip and global closure

Let I indicate an enabled composition source and `Z=B-N-hI`. Fast firings preserve I; inactive activation turns it on; nonzero Z jumps are +h for active activation and -h for immigration turning activity on or clearing whose target remains active. Inactive states with A>=a0 satisfy `N<=K0=(m-1)+(d-1)(v-1)`. The strip A<a0 has unbounded N and is not put into a finite head.

Uniform normalized active clearing mean follows from the new large-N estimate and finite complex-path access on small active states. The clearing compensator and `A<=C[1+(A)_m]` give uniformly bounded normalized A-occupation. Thus active birth probabilities are `O(B^-q)` for immigration and `O(B^(1-q))` for activation, with no hidden N factor. Actual clearings have inactive-output probability O(p0(N)).

For large hidden N, prescribe clearing from active states, with active output having uniformly positive probability. From an inactive A>=1 state, prescribe activation before immigration, which has probability 1-O(1/B), then clearing with active output. From A=0 take its compulsory actual immigration first. These blocks have bounded mean time and uniformly positive down-Z probability. Only an already-active activation can exit up, with probability O(z^(1-q)). No consecutive-immigration protocol is imposed against the arbitrarily large AB rate on this strip.

The bounded head uses neutral inactive-activation/clearing pairs, each reducing N by one, followed if necessary by at most m immigrations to enable mA. Its noncompulsory prescribed immigration races each win with probability at least c/z because that head truly has bounded N. Uniformly all blocks therefore have down probability >=cz^[-(m-1)], up probability <=Cz^[-(q-1)], and bounded mean duration. Conditional renewal gives up-exit probability <=Cz^-h and mean exit time <=Cz^(m-1).

Exponential and polynomially enlarged exponential exit weights contract by `exp(-theta h)+o(1)<1`. They construct the actual complementary value W_Z, with running cost exp(theta Z), profile `C(1+Z)^(m-1)exp(theta Z)`, and exact generator -exp(theta Z) above threshold. Its entrance leakage is CAB on an infinite strip, not finite support.

Independently, before relying on recurrence, the conservative fast part and connector give `L(1+N+B)<=C(1+N+B)`. The negative `(A)_m(B)_q` term dominates AB when both A>=m and B>=q; otherwise AB is at most linear in total count. Finite-sublevel localization proves unrestricted nonexplosion.

Both values have first-holding lower bound `exp(theta residual)/[C(1+N+B)^(m+q)]`. With a=(m-1)/(q-1)<1, r=N-aB+O(1), Z=B-N+O(1), and

`(1+a)(B-N)+2(N-aB)=(1-a)(N+B)`,

their maximum is a positive linear fraction of total count up to a constant. Hence W_r+W_Z is normlike. On each threshold cylinder the other exponential negative drift absorbs the actual polynomial leakage. Both residuals bounded above imply bounded total count. For any desired exp(lambda(N+B)) cost, choose theta sufficiently large; a finite-set Foster inequality follows.

The full complex graph is strongly connected through the shared mA+qB complex. Every enabled reaction has an enabled complex-path return with the same nonnegative leftover population, so physical communicating classes are closed, without global irreducibility. Localized Foster gives their positive recurrence. On a finite-mean regenerative cycle, nonnegative-value stopped Dynkin bounds the expected integral of exp(lambda(N+B)); localization, nonexplosion and Fatou justify passage to the full cycle. The occupation formula then gives every invariant exponential moment, without assuming stationary integrability of the Lyapunov function.

## 10. Final boundary of this receipt

The six-file V2 mechanism is accepted; the original five-file stopping list is not retroactively approved. The inactive-wrap counterexample, the scalar T/U obstruction, all older fixed-network kernel/ray failures, and earlier exact receipts remain preserved. Low activations are not called rare, arbitrarily high B histories are explicitly summed, and unbounded inactive strips are not capped.

This review establishes mathematical correctness in the stated structural class, not priority or novelty. No external upload or publication occurred. No remaining mathematical blocker was found in the exact repaired closure.
