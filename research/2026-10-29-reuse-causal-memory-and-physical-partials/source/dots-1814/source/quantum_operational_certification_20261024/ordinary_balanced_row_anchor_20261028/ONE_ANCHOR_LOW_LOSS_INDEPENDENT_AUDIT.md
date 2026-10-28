# Independent receiving: one-anchor low-loss holdout and fresh fallback

28 October 2026. Reviewer `producer-workspace/review_repeated_service_factorization`.

**PASS for the new scoped composition.** Governing source: `ONE_ANCHOR_LOW_LOSS_HOLDOUT_AND_FALLBACK.md`, SHA-256 `75e1e1859886e134eb046328b71bce22738d4ba21151d112ea79d71e6415a06b`. No author or received import was changed. This review checks the new observable test, branch/comparator composition, fast-event transfer, source cap and source-derived separation. Accepted Bures-query, known-decoder SDP, generic-fallback and common-frame mathematics are used only at their named interfaces, not re-audited. Ten direct import hashes were reverified.

## 1. What is genuinely sufficient, and what is not being supplied

The algorithm learns one decoder at a predetermined implementable encoder x0, tests that actual frozen policy on fresh ordinary data, and uses the already received global learner only on rejection. Its sufficient fast condition is small **optimal loss at x0**, not a supplied good decoder, special row geometry or a globally easy encoder landscape. A physically acquired policy with absolutely small loss needs no estimate of ell_star to be additively near-optimal: the only comparison fact used on acceptance is ell_star>=0.

The acquisition step supplies a physical normalized loss-density estimate and a finite classical full-CPTP decoder description. The known-coefficient optimization is not an optimization over the unknown source: its objective coefficients are tau, obtained from actual ordinary probes. The accepted SDP contract has explicit primal/dual feasibility and objective certification and known-matrix Kraus/isometry synthesis. A floating success flag or an uncapped heuristic solver would not satisfy that contract. An unexplained numerical failure cannot be omitted from the fast-completion probability; the stated theorem uses the received deterministic finite solver guarantee, with implementation discrepancies paid separately. A replacement on explicit failure keeps all-source soundness physical.

In the retained-frame interface, the entire encoder family's support is defined before acquisition. The common frame is the same through training, holdout, any fallback and the payload. The source resets; the **frame's** quantum memory need not and must not be silently reset. Uniformity in the one mathematical frame U is exactly what permits conditioning on previous training/holdout records. No fresh Haar draw after rejection is assumed.

## 2. Actual six-state observable and its conditional law

For an arbitrary TP qubit channel, write its Bloch action as `v -> t+A v`. At input `(I+s sigma_j)/2`, matching-output failure has probability

`[1-s t_j-A_jj]/2`.

Averaging both signs and the three axes gives `(3-Tr A)/6`. Since `F_e=(1+Tr A)/4`, the ordinary holdout mean is exactly

`p=(2/3)(1-F_e)=(2/3)ell(x0,Dhat)`.

This independently derives the normalization from the actual prepare/decode/measure experiment, not from a protected entangled reference. The training bank's receiver-local anti-state and discarded label are different from the holdout's retained classical label used for a final local measurement.

Conditional on U and every frozen classical training history, the stationary/reset source and fresh holdout inputs/ancillas produce iid Bernoulli trials with that p. The received causal arbitrary-operator identity justifies this conditional ideal representation despite evolving frame memory. The final conclusions average U and histories only after applying the uniform conditional bounds. There is no claim that the approximate physical frame literally exposes U.

## 3. Threshold constants and complete bad-history accounting

With `a=epsilon/192` and `n>=768 log(1/beta_test)/epsilon`:

* If `ell_fast>epsilon/64`, then `p>2a`. Accepting implies `K<=np/2`; the usual Bernoulli lower-tail exponent `np/8` is at least `log(1/beta_test)`. Thus false acceptance has conditional probability at most beta_test on **every** frozen training record, regardless of tomography/optimizer success.
* If `ell_fast<=epsilon/1024`, then `p<=a/8`. The exact Bernoulli mgf at lambda=log 2 is `1+p<=exp(p)`. Rejection satisfies `K>floor(na)`, hence `K>na`. Since `log 2>=5/8`, its probability is at most `exp(-na/2)<=beta_test^2<=beta_test` at the displayed n. The integer threshold does not lose a floor correction.

Therefore `Pr(A and ell_fast>epsilon/64)<=beta_test`. On accepted good histories the loss is at most epsilon/64; all bad-history losses are at most one because the decoder is CPTP. Crucially, the test does not divide this mass by Pr(A), so no accepted-record posterior certificate is asserted.

On rejected histories the fallback calls are wholly fresh. For each prior history and fixed U, its received expected-risk contract at `(gamma/2,epsilon/128)` gives

`E[ell_fallback | rejected past,U] <= (1+gamma/2)ell_star+epsilon/128`.

The original encoder/full-CPTP optimum is invariant under the common output frame; it is not replaced by an optimum only over x0 or a learner-selected feasible subset. Combining the branches gives

`E ell_selected <= Pr(A)epsilon/64 + Pr(not A)[(1+gamma/2)ell_star+epsilon/128]+beta_test`

`<= (1+gamma/2)ell_star+17epsilon/1024`.

No beta_train term belongs in this all-source risk bound: holdout soundness already covers unsuccessful training records. Adding one would be safe but unnecessary; omitting beta_test would not be safe.

## 4. Operational comparator and the two implementation transfers

For one unknown qubit payload, independent private pre-source Pauli framing and inverse post-decoder framing turn each ideal conditioned logical channel into a Pauli channel. Averaging over U and training/selection histories remains a Pauli channel, with unhalved diamond error exactly `2 E ell_selected`. The compared channel discards private keys, calibration records and internal memory. No key-conditioned or unframed diamond guarantee is inferred.

A whole-process **unhalved** discrepancy at most epsilon/2 then gives

`Delta_actual <= (1+gamma/2)2ell_star+17epsilon/512+epsilon/2`

`<= (1+gamma)2ell_star+epsilon`.

The universal CPTP maximum gives the additional cap 2. The whole-process comparison includes branching, possible fallback, retained frame, all physical preparations/measurements, selected decoder and final frames; it is not a bound on one isolated invocation.

A separate, stronger early-stage requirement is necessary to transfer the probability of fast completion. The source correctly reserves a **predecision record-retaining** discrepancy `nu_pre<=epsilon/1024` inside that same whole epsilon/2 allowance. A final payload-only norm guarantee would not by itself control the accept/reject distribution. Retaining the decision record makes its actual event probability differ by at most nu_pre (conservatively, regardless of a possible extra half factor under unhalved convention). This is one allocation inside the total, not a second final risk debit.

## 5. Fast-completion proof and source/resource ledger

On the good Bures bank, the uniform full-decoder root-risk transfer and eta-inexact surrogate minimization give

`sqrt(ell_fast)<=sqrt(ell_0)+2sqrt(6m)+sqrt(eta)`.

At the stated choices and `ell_0<=epsilon/2^14`, its coefficient of sqrt(epsilon) is exactly bounded by `(6+2sqrt(6))/512<11/512`. Thus `ell_fast<121epsilon/2^18<epsilon/1024`. Ideal failure to accept is at most beta_train+beta_test; predecision transfer makes actual failure at most `3epsilon/1024`. This is a high-probability **actual call bill**, not an expected-call theorem or a changed deterministic worst-case cap.

The fast call count is exactly `n_train+n_test+1` when the early route accepts. `D0<2dr` gives `O_tilde((dr+1)/epsilon)+1`; in the rank-compressed interface `dr<=48R^2`, so this is `O_tilde(R^2/epsilon)+1`. The training, test and one payload are all counted. Rejection adds a complete fresh fallback at the declared local parameters. Since `r<=2k`, `0<gamma<=1` and k>=1, the fast cap is absorbed in the fallback's `O_tilde(k^4/(gamma epsilon))+1` worst-case source cap. No physical source query is allocated to each classical encoder-grid point by this composition.

The maximum horizon and precision must be declared before any decision. The accepted causal compiler emits outputs immediately and is consistent on finite prefixes, so stopping at an early accepted payload does not require executing unused fallback source calls. Choosing the compiler's precision against the full maximum horizon is conservative. Its internal frame memory remains retained throughout the actually executed prefix. A batch-only reduction that required all future inputs before the payload would not justify this early-stop statement.

The fast **source-call** bill has no inverse-gamma factor. This must not be inflated into a gamma-independent total classical precomputation or hardware-runtime claim: maximum-horizon planning and precision can still depend on the fallback parameters. Quantum memory and collective processing of the loss-density bank are paid accepted resources; rank-squared call complexity is not a count-only or low-memory implementation.

For completeness, a literal finite six-state sampler is available without an unbounded ideal random draw. Use three fresh fair bits per attempt, accept labels 0 through 5, and reject 6 or 7. With at most B declared training/holdout draws, cap each at `r_rng=ceil(log_4(B/nu_rng))` attempts (at least one). The union exhaustion probability is at most `B 4^-r_rng<=nu_rng`; use a predetermined physical fallback on exhaustion. This costs at most `3B r_rng` bits, with the small record discrepancy assigned **inside nu_pre** (and the whole-process budget), allowing an extra factor two for an unhalved diamond allocation. Known encoder controls, local anti-state preparation, all output measurements, n_test uses of the compiled decoder with fresh ancillas, any private label delivery, and the final two frame bits and frame gates remain paid. This supplies a finite implementation mechanism for the new holdout randomness without claiming an actual device execution.

## 6. Source-derived separation from rank-one row hypotheses

The proposed W is unitary because O is orthogonal. At every x, `A_x=W V_x` is an isometry. A concrete mathematical recovery is

`D_x(B)=A_x^dagger B A_x + Tr[(I-A_x A_x^dagger)B]|0><0|`.

Both terms are CP and their trace effects sum to I, so this is a full CPTP extension and exactly inverts the encoded source. Thus ell_0=ell_star=0 for every chosen anchor. This proves existence of the comparator; the unknown W or inverse is not supplied to the learner, whose acquisition still uses the Bures bank and finite decoder SDP.

I independently derived the diagonal loss-density effects directly from the **six ordinary probes**. For a real output amplitude row `(u,v)`, the two receiver-reference diagonal entries are `u^2/6+v^2/3` and `u^2/3+v^2/6`. Substituting `u=x_s/sqrt(2)` and `v=t(o_s^T x)/sqrt(2)` gives exactly the source's sixteen quadratic effects. Each has rank two, trace 1/4, and eigenvalues `(3±sqrt(3))/24`; their sum is I4. Consequently the total best-rank-one row trace tail is exactly `2-2/sqrt(3)>0`.

Appending a fixed spectator preserves perfect recoverability by tracing it. In a tensor diagonal basis its nonnegative eigenvalues scale each row effect and sum to one, preserving the total tail, while Choi purity becomes `Tr sigma^2`. This is a valid perfectly recoverable mixed-spectator extension. No unknown spectral basis is handed to the algorithm.

The logical separation is appropriately limited: the exact-row sufficient hypothesis fails, and a bound containing a nonvanishing penalty from this fixed tail cannot certify arbitrarily vanishing loss through that tail estimate alone. It does **not** prove that every empirical residual-validation row learner must reject this example or perform poorly. The author explicitly preserves that distinction.

## 7. Independent evidence and final scope

`one_anchor_low_loss_independent_checks.py/.json` independently verifies the symbolic arbitrary-TP six-probe identity; all sixteen source-derived effects and their exact spectrum/tail; a concrete CPTP range-inverse comparator; 72 rational branch/final-risk budgets; exact integer threshold examples with conservative binary-log counts; and six finite-sampler caps. It uses exact symbolic/rational arithmetic, not the author's helper functions. All ten direct import hashes and the source hash match the frozen manifest. No new source observations, quantum acquisition, production SDP, compiled-frame execution or hardware run occurred.

Accepted scope: stationary/reset ordinary source, the fixed four-real-coordinate encoder family, a supplied actual output register or the received retained common-frame interface, one predetermined anchor, fresh ordinary holdout and fallback calls, known finite full-CPTP optimization/control, private one-payload framing, and both declared implementation norm allocations. This is a complementary absolute-low-loss sufficient fast path, not a generic rank-squared global learner, a promise of acceptance from a good encoder elsewhere, a new fixed-encoder recovery primitive, or a hardware/practical advantage. No unresolved new mathematical obligation was found within these interfaces.
