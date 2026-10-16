# Frozen independent audit: total-count envelope obstruction

Date: 2026-10-16. Worker: `gb_kinetic_audit`.

**Verdict: PASS for the exact stated mathematical class. No blocking error or countermodel was found.** Every finite, nonnegative, globally supercaloric continuation envelope depending only on time and total count has initial value strictly greater than

\[
1-10^{-18}-10^{-40}
\]

for the specified capped eight-site deadline-one problem. This audit reconstructs both the analytic argument and all exact finite arithmetic. It does not acquire the physical hitting probability, prove a solver advantage, certify historical novelty, or constitute external review.

## 1. Frozen inputs and authority

The audited candidate is `../gb_kinetic_genesis/check_total_count_obstruction.py`, SHA-256 `43578879f90c4f0ea640adc3cab04555f2ab089fcfe7d2792a6d775a2cf88fbe`. Its finalized proof is `PROOFS.txt`, SHA-256 `9f56f16e82d34eb926ebe7355624e726c45c1cb459ff3c4afcb5609c8de2b340`. Its report is `REPORT.txt`, SHA-256 `dbf661370654c2f946c35f7d6837da1b6eafffdf24dd08b18021589020990995`. Byte copies are under `candidate_frozen/`.

The source packet was read at `/Users/harjas/Downloads/Dots/kinetic_obstruction_packet_v2`, selectively: handoff, actual-boundary product proof, arbitrary-common-scalar proof, baseline generator contract, and the supplied exact product checker. These provide the supplied model and distinguish the earlier envelope classes. They are not treated as premises proving the new total-count result.

The requested Astra pin is `61389569d6c53b439764f0d148b35b7fa6083eec`. The live worktree had advanced to `19965c2120dc0c440072dc746821aabdc1dcd8b6` at this audit's first read. The requested pinned `AGENTS.md`, `00_START_HERE.txt` and N883 dossier were therefore read with `git show` and saved under `pinned_navigation/`. The N883 capability and inside-acquisition gates remain open. No other worker's scientific results were used, except the specifically assigned candidate.

`SOURCE_SNAPSHOT.json` and `MANUSCRIPT_SNAPSHOT.json` record the consumed bytes. The finalized candidate manifest was checked against every listed payload hash and size; its script and result match the earlier frozen copies. This is an integrity check, separate from the mathematical audit.

## 2. Exact accepted theorem class

The retained state set is \(K=\{0,\ldots,162\}^8\); \(B=\{0,\ldots,15\}^8\) is prescribed value one at first entry, and any transition creating count 163 has value zero. The initial point is \((50,\ldots,50)\), and the deadline is one. Labels are row-major on the open 2-by-4 ladder. There are 20 directed diffusion arcs.

The exact rational rates are

\[
 b(n)=2.676n(n-1)+108.102,\qquad
 a(n)=.040n(n-1)(n-2)+37.881n,
\]

and diffusion \(i\to j\) has rate \(8.2207n_i\). No physical parameter calibration or IEEE implementation error is audited.

On continuation states, \(g(t,n)=F(t,S(n))\), with \(S(n)=\sum_i n_i\). The candidate's finalized proof assumes finite nonnegative values, local absolute continuity and local boundedness before time one, nonnegative terminal lower limit, and \(\partial_tg+Qg\le0\) almost everywhere on every actual continuation state. These are sufficient. No monotonicity, convexity, exponential shape, factorization, or Markov closure of the physical total count is assumed.

Local absolute continuity, rather than continuously differentiable time dependence, is sufficient: on a compact time interval the finite vector of values obeys the integrated backward inequality. Taking a common full-measure set of times is harmless because there are only finitely many relevant totals and states.

Nonnegative values throughout time already justify dropping the value at total 500 and taking the terminal limit. If a signed variant were desired, global actual-state supercaloricity plus a nonnegative terminal **liminf** would imply nonnegativity by finite-state comparison. Merely assigning a nonnegative value at time one, while permitting a negative left limit and a discontinuity, would not suffice for that signed variant. The finalized candidate does not make this error.

## 3. Independent physical-row reconstruction

`independent_exact_audit.py` does not import producer functions. It reconstructs the graph from Manhattan adjacency of eight physical coordinates, uses integer numerators for the exact decimal rates, and directly forms the symbolic coefficients of \(Qg\) from every nonzero elementary jump. It then separately compares those coefficients with closed row formulas.

For \(16\le s\le121\), the representative has count 16 at site zero, and the other seven entries are filled sequentially up to 15. For \(122\le s\le499\), entries are filled sequentially up to 100. The closed representative formulas in the independent checker differ in implementation from the producer's loop/division construction but give the same configurations.

Every selected state is a continuation state with total \(s\). Every immediate successor has maximum count at most 101, so **none of these rows has a physical overflow transition**. This avoids a cap-sign or reflection/killing ambiguity in the selected rows. It does not check all rows of the full box.

The independent reconstruction checks 484 rows and 10,456 nonzero elementary channels. The graph degree sequence is \([2,3,3,2,2,3,3,2]\). There are 106 target-entry rows and 75 target-entering diffusion channel instances. The model has 36 potential local reaction/diffusion channels per state; many have zero rates at zero counts and are omitted by both enumerators.

Writing the grouped up, down and success rates as \(\beta_s,\delta_s,\kappa_s\), the exact symbolic generator row is

\[
 \beta_s(F_{s+1}-F_s)+\delta_s(F_{s-1}-F_s)+\kappa_s(1-F_s).
\]

For \(s\le121\),

\[
 \kappa_s=a(16)+16D\big(1_{x_1(s)\le14}+1_{x_4(s)\le14}\big),\qquad
 \delta_s=\sum_i a(x_i(s))-a(16).
\]

For larger totals, \(\kappa_s=0\) and \(\delta_s=\sum_i a(x_i(s))\). Always \(\beta_s=\sum_i b(x_i(s))\), and \(\delta_{16}=0\).

The target overwrite is load-bearing and is handled correctly. A jump from a unique count 16 to an adjacent count at most 14 can enter \(B\) **without changing total count**; it contributes \(D16(1-F_s)\), rather than zero. Conversely, diffusion between continuation states contributes zero. A target state and a continuation state can share the same total: \((15,1,0,\ldots,0)\) and \((16,0,\ldots,0)\) both have total 16. The representation is required to be total-only on continuation states, with the target separately overwritten; the proof never conflates those values.

## 4. Reconstructed comparison proof

Define a finite chain \(Y\) with continuation states \(16,\ldots,499\), success \(A_*\), and failure \(F_*\). It uses the rates above, with the birth from 499 sent to \(F_*\). Both sinks are absorbing.

For every selected actual configuration, global supercaloricity gives

\[
 \partial_tF_s+\beta_s(F_{s+1}-F_s)
 +\delta_s(F_{s-1}-F_s)+\kappa_s(1-F_s)\le0.
\]

At total 499, replacing \(F(t,500)\ge0\) by zero decreases the left side. Thus the same inequality holds for the finite chain's failure payoff zero. At total 16 the down rate is zero and no lower-boundary value is required. The comparison direction is therefore correct.

Finite-state backward comparison, integrated first to \(1-\epsilon\), then passed to one by nonnegativity, gives

\[
 F(0,400)\ge\Pr_{400}(Y\text{ reaches }A_*\text{ by }1).
\]

This uses the same value at physical configurations with the same total. It does not require a physical path to realize the chosen representatives. For example, the selected configuration at total 400 is \((100,100,100,100,0,0,0,0)\), whereas the actual initial configuration is all 50. Their exact total birth/death rates are respectively

\[
 (106834.416,170384.4),\qquad (53314.416,52784.4).
\]

The physical total count is consequently not the constructed Markov chain. The row policy discards profile information and may effectively choose a new physical representative after each total jump. That freedom is legitimate for testing a global total-only envelope, and would be invalid as a physical trajectory approximation. The candidate states this distinction correctly.

## 5. Independent exact finite-deadline certificate

The independent solver uses forward affine shooting, not Thomas elimination. It expresses each unknown as \(v_s=A_sz+C_s\), propagates the second-order recurrence, imposes the upper absorbing boundary, and then separately replays every equation. All arithmetic is rational.

The failure vector \(p\) has success value zero, failure value one and \(Lp=0\). The clock vector \(m\) has both absorbing values one and \(Lm+100m=0\) on continuation states. The independent checker verifies all 968 scalar equations, \(0<p_s<1\) and \(m_s>1\) at all 484 states, and the corresponding independently reconstructed pivots are positive.

The exact strict comparisons are

\[
 p_{400}<10^{-18},\qquad m_{400}<100,\qquad
 \frac{100^{100}}{100!}>10^{42}.
\]

For orientation, the independently reconstructed values are

\[
 p_{400}=2.08304978946501844191144790328151801226127141\times10^{-20},
\]

\[
 m_{400}=3.02062254605722674739583172327849861481607058.
\]

Those decimals are descriptive and are unused in the strict tests. All exact rows and both exact solution vectors are saved in `EXACT_WITNESS.json`; the exact initial numerators/denominators are also saved separately.

Let \(\tau\) be first absorption in either sink. On every bounded time interval,

\[
 Z_t=e^{100(t\wedge\tau)}m(Y_{t\wedge\tau})
\]

is a true martingale: its pre-absorption drift is zero, and the stopped process is bounded for fixed \(t\) because the state set is finite. Since \(m\ge1\),

\[
 \Pr_{400}(\tau>t)\le m_{400}e^{-100t}.
\]

This proves almost-sure absorption as well. The bounded harmonic vector \(p\) then identifies \(p_{400}\) as eventual artificial-failure probability by stopped sampling and bounded convergence. No existence of an exponential moment is presumed from the linear solve, and no numerical eigenvalue claim is needed.

Failure to reach success by time one is contained in eventual artificial failure or unfinished absorption at time one. Hence

\[
 1-\Pr_{400}(Y\text{ reaches }A_*\text{ by }1)
 \le p_{400}+m_{400}e^{-100}
 <10^{-18}+10^{-40}.
\]

Here \(e^{100}>100^{100}/100!>10^{42}\). Combining this strict finite-deadline bound with the comparison proves the audited theorem. This is not an eventual-obstruction-to-deadline transfer.

The producer was replayed only in the owned `producer_replay/` directory, preserving frozen inputs. Every supplied nontiming result field matched. The independent reconstructed rational values also match both descriptive producer decimals exactly to their displayed precision.

## 6. Adversarial checks and limits

The following possible failures were specifically sought and excluded within the stated class:

- Wrong graph or diffusion directions: the independent geometric 20-arc graph agrees.
- Overflow silently reflected or omitted at selected rows: all selected successors are at most 101, so no such loss is present there.
- Missing target-entering diffusion at constant total: all 75 nonzero instances are explicitly classified as success.
- Wrong sign at the artificial boundary: dropping nonnegative \(F_{500}\) makes the residual smaller and preserves an upper-envelope inequality.
- Initial state confused with the selected concentrated state: values agree only by the total-count representation; physical rates differ, as shown above.
- Treating a positive-pivot solve as proof of a moment or tail: all-state positive clock values and exact generator identities supply the stopped-martingale proof directly.
- Confusing eventual failure with finite-deadline success: the unfinished-path term is separately bounded below \(10^{-40}\).
- Using rounded displays as strict evidence: all acceptance inequalities are rational or integer comparisons.

The theorem needs the all-state pointwise envelope constraint. It does not exclude a restricted-domain solve with a separately charged outside-risk budget, a total marginal carrying conditional profile information, or a representation with dispersion, spatial/pair data, history or tensor structure. It does not supply any lower bound on the physical hitting probability.

The inherited overflow allowance from N883 was not re-proved here. The reported consequence that adding that allowance makes this envelope class's unbounded-model upper bound trivial is a conditional arithmetic consequence of that separately certified allowance, not new overflow evidence from this audit. No acquired eight-site probability, matched solver timing, memory bound, physical validation or historical-priority finding follows.

## 7. Replay and frozen status

Run `python3 independent_exact_audit.py` in this audit directory. It reconstructs the graph and all selected rows, independently solves both exact boundary problems, checks all residuals and strict inequalities, replays the candidate in an owned subdirectory, and writes the exact witness and `INDEPENDENT_EXACT_AUDIT.json`. It uses only the Python standard library. The recorded wall time is descriptive certificate-checking time, not physical solver performance.

`EARLY_GATE.md` records the initial viability gate. Final mathematical status is **FROZEN_INDEPENDENT_EXACT_AUDIT_PASS** for the frozen candidate and stated class. Capability remains **NOT_ACQUIRED**; physical probability, external correctness, historical novelty and practical advantage remain **UNKNOWN**. No repository, worktree or source-packet bytes were edited; all audit writes are confined to the assigned worker directory.
