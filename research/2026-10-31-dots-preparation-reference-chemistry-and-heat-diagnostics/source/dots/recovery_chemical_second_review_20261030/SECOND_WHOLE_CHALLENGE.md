# Second independent whole-bundle challenge

30 October 2026. Reviewer: `producer-workspace/challenge_recurrence_closure`. Theory only.

## Verdict and evidence boundary

**PASS, scoped to the completed frozen proof bundle for this four-species family.** I read all 17 Markdown sources named by `recovery_chemical_review_20261030/WHOLE_CLOSURE_SOURCE_SHA256.txt`, computed their SHA-256 hashes from actual bytes, and found all 17 exact matches. I also verified the first whole review's SHA-256 as `28d1e425400095a3d4758cd5ae7a45bbd9dacf463cf0081756e2a056a0f3a2a2`. My conclusion follows from the composition checks below, not the earlier review's PASS label.

For fixed positive rates, integer a0>=2, m=a0+2 and q>m, the completed argument supports nonexplosion, positive recurrence in each communicating class, and every exponential total-count moment of its invariant law. It does not certify the bare `FULL_NONBALANCED_DORMANT_CLOSURE_CANDIDATE.md`, general weakly reversible recurrence, uniform numerical constants, historical novelty, or formal proof verification. The word “classwise” is important. Weak reversibility supplies executable return reaction paths, making communicating components closed; it does not collapse different components into one.

Actual byte evidence is in `BYTE_AND_GEOMETRY_CHECKS.json`. Originals were not edited. No external PDF, website, upload, outreach, or physical action was used; the Wisconsin PDF denial was respected without alternate access. This review makes no new ordinary-literature exclusion claim.

## 1. Local input laws survive composition

I checked the all-positive-s extension rather than silently using the older s>=2 calculation for small s. Its split d>=Lx versus d<Lx, L>4/s, supplies the favorable simultaneous coordinate/denominator change. On the C-large face the potentially adverse denominator terms are absorbed by the C-return term. Thus the exponents a0-1 and, at a0=2, 1/2 used for physical time/occupation have an actual stated derivation.

The lower occupation survival event now includes the actual D=0 stop: for d_in>=x it requires at least x events; for d_in<x its extinction hazard is bounded by the displayed C x d_in estimate. This is essential to comparing T and U for the same episode. The subsequent dormant continuation uses its actual entrance law, not an independent average. The resulting full local estimates are T/U<=C/(1+A_in), positive-D T<=C/[n(b)_q], U<=C n^(-1/2)/(b)_q, and clearing-output f_m moment O(1/n).

The high-event inverse powers come from compensators and killed running-cost profiles. They are not products of a rare-event probability and an unconditioned reset estimate. Clearing preserves fixed f_s, immigration spends m powers, and activation spends m-1; low noncompulsory immigration spends one. These are the correct operators for the later finite-degree enumeration.

## 2. Tilt, constants, and the apparent recursion

I specifically tried to break the proof by letting seed B become arbitrarily large. That does not defeat the completed construction: its norm is exp(theta r+lambda B) f_s, and actual seed B is retained. A small designated-exit norm is NOT a uniform small unweighted probability across a long descent. The weighted-error convention correctly uses Cauchy–Schwarz under the finite positive measure exp(theta r_out+lambda B_out) dP. It does not require this measure to be a probability or require doubling theta/lambda.

A defensible dependency order is:

1. Fix theta and the finite profile and polynomial residual exponents needed for the desired cost, finite degree, and bad-set correction.
2. Obtain local profile constants for that finite list and the local doubled exponents.
3. Choose lambda to contract ordinary high clearings and low-activation/clearing pairs.
4. Obtain the dormant Green constants for this fixed tilt. These may be large but are finite independently of r0; killing only reduces positive values.
5. Increase r0 to absorb the positive-D activation/dormant kernels and the designated-exit/physical-approach constants.
6. Construct actual repair by positive truncated iteration; only afterwards append it to graded source exits.
7. Construct the bad-return correction by its separately preconditioned small-gain argument.

There is no infinite profile escalation here. To bound repair at s, its error upgrade can use stopped-processor transport at 2s. The latter's local rare-kernel estimate can use local 4s; it does not demand repaired transport at 4s. Selecting this finite list before lambda is sufficient.

The low-phase completion is load-bearing. A high clearing plus its no-race low approach has net B zero when b=q, and minus one when q<b<2q. Treating the low approach as a fresh exp(lambda q) multiplier on every block would invalidate the contraction. The completion combines those operations before taking the norm. Additional races contribute O_lambda(1/A), while an initial low approach pays a bounded multiplier only once. The bounded-A/high-B dormant leading endpoints also have nonincreasing B. These facts preserve the Green small-gain order even though its finite-corner constant can grow with the chosen B cutoff.

The active-section flag also matters: fast seed/reseed activity at the original B=q is not a completed cycle. Inactive B=q is physically continued rather than counted as an active return.

## 3. Positive source and negative event are logically separate

The strongest useful synthesis checks are the first-connector identities. At B=q, immigration, activation, and clearing are all r-neutral and have fixed output B equal to q+1, 2q-1, and 0.

For positive source, clearing's continuation needs m spent powers, activation's continuation needs one, and immigration is bounded by the earned repair. Their compensators are bounded by constant multiples of T because

- (A)_m f_m(A-m) is bounded on A>=m;
- A f_1(A+m-1)=A/(A+m)<=1;
- immigration has mass iT.

Consequently E[(w_next-w)_+]<=CwT. This yields the needed O(w/r) source on every positive-D input without assigning a favorable sign to failed activation paths. In particular, no term U o(1) is being mislabeled O(1/r).

The same first-connector decomposition, now using already earned f_m repair from each fixed output phase, gives the unrestricted P(w_next f_m(A_next))<=CwT. This is a sharper and adequate replacement for the bare candidate's restricted M+ assertion. Direct fast dormant entries are already inside T and the actual first-connector law; an extra reset term is unnecessary.

Independently, a useful activation has probability t q U. All but O(U/K) of that mass is qualified. The finite prescribed word clears 2q-1 to q-1, then follows low activation/clearing pairs down to B=1 and a final activation to q. It has no earlier active-section return and lowers r by exactly h. Positive-D clearings supply reserve A>=K/4 with error CK^m/r; direct dormant segments lose only a bounded O(qm) amount. With gamma m<1 all finitely many failure probabilities vanish. Killing at the r threshold improves the negative reward. Hence a genuine event of probability at least cU has terminal factor exp(-theta h); combining it with the independently bounded positive part gives Pw-w<=-cUw+CwT. This is the correct coefficient-one drift argument.

## 4. The non-small bad row is not assumed small

Pure dormant bad-to-bad cycles can have order-one return mass. Their earned Green is used first. Only the additional seed-mediated dormant return is small, since it must pass through a positive-D-to-dormant entrance, with the actual seed phase and residual still retained. After preconditioning, the two-type majorant has a small dormant diagonal, a small positive-D diagonal, bounded positive-D-to-dormant entry, and dormant-to-positive-D entry O(r^(gamma m-1)). Its off-diagonal product tends to zero. This is a genuine positive-kernel small-gain argument, not scalar rarity substituted for a Green.

I also checked the output/input residual issue: paths may decrease r substantially, so a terminal inverse-r factor cannot simply be replaced by its initial value. The real polynomial-weight extension, including j=gamma m-1<0, is necessary. Raising r0 so (1+r)^j exp(theta r) is increasing and using the weighted kernel handles this. It is not differentiation of a potential or an unpriced pointwise substitution.

The constructed correction satisfies its actual bad-set kernel equation and is zero on good states. Its good-state leakage is controlled by the unrestricted inverse-m identity, hence by CwT, with the same finite residual-power bookkeeping. Since T/U vanishes for good incoming A, the negative margin survives. The Green and correction constants can be fixed before the final threshold increase; killing does not enlarge their positive operator bounds.

## 5. Physical clock, complementary strip, and exterior leakage

Multiplying the section construction by residual order m pays physical cycle cost: at B=q, N=r+H(q), bad dormant f_m>=c r^-m, bad positive-D margin has scale r^-1, and good U>=c r^(-(m-1)). The processor controls actual running time, not just the number of connector events. Thus stopped cycle telescoping constructs W_r, rather than merely proving recurrence of a clock-free embedded chain.

The arbitrary-phase bound must remain C exp(lambda B)(1+r)^m exp(theta r). Its exterior threshold leakage is C exp(lambda B), not bounded. The complementary Z construction is essential, not optional decoration.

I checked the Z trials across both hidden-N regimes. Large-N trials use complete local stopping episodes, not a uniformly bounded number of fast jumps. In the finite-N regime neutral activation/clearing pairs reduce N by one; unexpected births abort the trial rather than being silently recycled. At A=0, at most m immigrations suffice and only m-1 are noncompulsory races. Conditional renewal therefore gives mean strict-level-exit time O(z^(m-1)) and up-exit probability O(z^(-(q-m))), uniformly in hidden N. No independent-trials assumption is needed. Z's exterior leakage is C AB, because only active activation enters its domain from below.

Finally r=N-alpha B+O(1), Z=B-N+O(1), alpha=(m-1)/(q-1)<1. On the r-threshold strip choose theta_Z(1-alpha)>lambda to absorb the actual exp(lambda B) leakage. On the Z-threshold strip, r grows linearly in total count and exp(theta r) absorbs AB. This choice is not circular: lambda is already fixed by the r construction and the Z estimate permits any fixed theta_Z. Thresholds can then be enlarged. The two negative running costs dominate any prescribed total-count exponential after choosing sufficiently large exponents.

The stopped-value sum is normlike: its first-holding lower bound is exponential divided by a fixed polynomial total jump rate. Independent nonexplosion follows from the linear total-count Foster bound: fast reactions conserve N+B, high-degree clearing controls activation in the high corner, and AB is at most linear on the complementary strips. Finite rates on finite sets permit localization. These steps complete the continuous-time Foster/invariant-moment inference rather than assuming it from the section chain.

## Disposition

No counterexample or remaining load-bearing closure gap was found in this second whole challenge. The named completions are indispensable parts of the accepted object. This report does not upgrade mutable later edits, the historical bare candidate, or a broader network class.

As a falsification aid only, direct finite checks additionally verified 25,551 phase-identity parameter/count cases and 7,980 enabled fast transitions preserving the active predicate. Those finite checks do not prove the infinite-state estimates and are not the basis of this verdict.
