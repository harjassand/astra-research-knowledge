# Independent statistics audit: mixed retained-memory payload service

28 October 2026. Reviewer: `producer-workspace/audit_count_pilot_fresh`.

**PASS at the finite mixed-controller, cumulative-marginal-comparator scope.** Final formal source `ordinary_prequential_mixed_payload_memory_service_20261028.md`, SHA-256 `ca691d92eb120edaf9ffbe1937db4a445e6b3cc902815a2a933beaba126a1133`. Prior versions and the exact clarification history are bound in the receipt. No source calls, RNG draws, acquisition simulation, generic optimizer execution or hardware validation occurred. Received base and fast-bandit artifacts were not changed.

## 1. Which occupation and conditional law are used

The analysis is the actual TEST/USE mixed process on the global Choi input, under the declared ideal trusted interface. It is not an all-probe replacement history. Previously delivered references/outputs can remain correlated with source memory; they are neither reset nor reduced to nonexistent microscopic labels. At an active history the next untouched Choi pair is still product with the previous process, so the existing conditional return-bit calculation applies. This property is used in the global Choi proof, not asserted for arbitrary entangled service inputs.

The active indicator A_t is predictable from the number of already completed USE attempts. It counts attempts, regardless of unknown correctness. Fresh role and exploration coins are independent of the past and of one another. The complete source port cannot receive an extra current role/decoder label. The sampled physical decoder is applied; its mean equals the center only after averaging its private exploration coins.

For the constant TEST probability p, the actual record is zero on USE and `ghat/p` on TEST. Conditional expectation gives

`E[gtilde_t|h]=A_t grad q_t`,

`E||gtilde_t||_*^2 <= (8D^2/p) A_t q_t(C_t)`.

The second denominator is p, not p^2: one factor is canceled by the TEST probability. There is no division by a random observed test count and no fabricated gradient from a payload. Inactive rounds extend the analysis by zero gradient and zero loss without requiring physical source calls. The existing center can simply be retained on zero-gradient rounds.

## 2. Mirror inequality and comparator

Apply the received pathwise residual inequality to these actual importance-weighted records. A fixed comparator is smoothed by zeta of the known center, and its active per-round loss increases by at most A_t zeta. Bounding the number of active rounds by N and taking conditional expectations yields exactly

`(1-8eta D^2/p)L <= E sum A_t q_t(C_D)+zeta N+k log(1/zeta)/eta+N delta/eta`,

where `L=E sum A_t q_t(C_t)` is the active center-loss sum, NOT the unweighted number of observed test mismatches. Equivalently it is the mean importance-weighted test mismatch sum. The role coin does not alter this argument through optional stopping because activity is predictable and the analysis has a fixed N-round zero extension.

The comparator D is deterministic and fixed, evaluated on this same mixed occupation. Infimizing the expected objective is valid; choosing a separate realized-path optimizer or a counterfactual control policy is not. Multiplying the comparator term by `(3/2)r` produces exactly C_N(D), a cumulative marginal Bell-loss sum. It can exceed one. It is not the global loss of a q-input oracle channel: a single correlated Pauli error with probability a can give global loss a but cumulative marginal loss qa. The source correctly retains this distinction.

For finite-control conclusions the benchmark remains the mixed occupation of the IDEAL declared controller used in the proof. A single final channel-error debit cannot transfer an N-term comparator to separately perturbed actual-controller histories. The source's final clarification makes this explicit. 'Actual mixed occupation' rules out all-probe/counterfactual substitutions within that declared experiment; it is not a free benchmark-stability theorem under implementation error.

## 3. New parameters really fit the finite learner

With p>=1/2 and eta=gamma/(128D^2),

`8eta D^2/p<=gamma/8`,

and the maximum importance-weighted local gradient has size at most `sqrt(8)D/p`. Its eta-scaled norm is at most 1/16, as required by the received proximal existence argument. The step, residual delta, comparator zeta and horizon N are all the NEW parameters; no unchanged numerical solve is inferred from the one-terminal theorem.

The learner-only interior bound remains valid over at most N updates. Importance weighting is a known rational scalar, so exact primal/dual coordinates, inverse computations and residual certificates remain rational. A fixed dyadic grid chosen for the new delta, N and mu prevents recursive denominator growth. Known convex optimization and compilation time is polynomial in these bit/resource parameters, not claimed near-linear in q or polynomial in inverse mu. On every history its finite certificates must still succeed under the implementation contract; a replacement channel does not acquire a free optimization guarantee.

## 4. Role shortfall and one bad-event charge

All N role coins may be imagined sampled in advance for analysis. Stopping immediately on the qth USE gives exactly the same shortfall event as `Binomial(N,r)<q`, with mean m_role. This event concerns the coins and completed transmissions, not correctness, a syndrome, a recovery flag or acceptance-conditioned data.

Because m_role>=2q, shortfall lies in the lower half-mean tail. An elementary exponential-moment proof gives

`Pr[X<=m_role/2] <= exp[-m_role(1-log 2)/2] <= exp[-m_role/8]`.

For example take the test factor 2^(-X), use `(1-r/2)^N<=exp(-m_role/2)` and `log 2<=3/4`. Since m_role>=8 L_short and `L_short>=log(16/epsilon)`, beta<=epsilon/16. The base-2 ceilings are conservative and exactly computable from rational comparisons.

The separate quantum-process review establishes the actual global Choi operator-union bound and the delivered-marginal equality. Completed-history global loss is bounded by its sum of delivered marginal failures. Dropping completion restrictions increases each positive term; later complete trace-preserving instruments preserve isolated earlier marginals after averaging their records. On shortfall only the bound one for GLOBAL loss is used. Therefore

`ell_global<=beta+(3/2)r L`.

The shortfall debit is once, not q beta. Physical replacement of missing outputs and discard of unsent inputs remain necessary; no trusted-storage bypass is used. There is no conditioning by a small probability of completed histories.

## 5. Accuracy and complete source cap

For the specified r=m_role/N, zeta and delta, the three additive contributions before the factor `(3/2)/(1-gamma/8)` are respectively at most epsilon/16, epsilon/8 and epsilon/64. The barrier contribution follows directly from the NEW lower bound on N and the base-2 upper bound L0 on log(1/zeta). Thus the statistical Bell debit is at most 39epsilon/112. The multiplier on C_N is at most 1+gamma.

Including role shortfall and the complete implementation allowance gives

`39/112 + 1/16 + 1/2 = 51/56 <1`

as the total additive coefficient. The second N threshold dominates 2m_role throughout the stated range. Rounding to the least power of two gives exactly

`N<2048 m_role D^2 k L0/(gamma epsilon)`

` =36864 m_role d^5 L0/(gamma epsilon)`.

Each active USE sends one real unknown qubit; the other actual calls are consumed TEST calls. The q inputs are not sent simultaneously and the cap includes every completed attempted payload. At fixed local dimension and target, the displayed source cap is near-linear in q up to logs, but the finite classical processing/storage/compilation cost is not claimed near-linear.

## 6. Samplers, physical controls and complete discrepancy

Because N is a power of two and m_role is an integer, each role coin is exact using log2 N fair bits and an integer threshold. It needs no rejection. The two inherited index/axis rejection samplers use the new N, at most R trials each, and at most 2N total draws. Their exhaustion probability is bounded by `2N 2^(-R)<=nu_rng/2`. Independent signs add two bits per possible round. The stated worst-case cap

`N[log2 N+2+R(ceil log2 D+2)]`

therefore holds before optional framing. Dummy labels on USE can be drawn and retired to maintain the public schedule. The framing adds 2q private shared key bits, not a free communicated resource. Exhaustion couples to an ideal label process until abort and its uniform bounded-loss debit is included in the one complete allowance; no regret statement is conditioned on good sampler records.

At most N source calls, N actual exploratory decoder applications and N return measurements are conservatively charged. The stored q inputs, isolated q outputs, trusted idle duration, fixed encoder, known output patch, compiled receiver environments, resets and dense routing/precision cost remain real premises. There is no protected calibration reference or source reset.

The final source correctly strengthens nu to a whole-q-input half-diamond (or stronger complete-process) discrepancy uniform over arbitrary joint inputs/references. This is necessary for the optional actual-channel diamond claim; a Bell-score-only or calibration-trajectory allowance is insufficient. The ideal averaged framed service is Pauli, so its half-diamond loss equals its global Bell loss. The actual imperfect framed service need not remain Pauli: its distance from the ideal framed service is added once by triangle inequality. Frames, private-key boundaries, missing-output framing, storage and adaptive instruments are all included in that same allowance. No separate second debit or free comparator transfer is implied.

## 7. Independent evidence and acceptance boundary

`prequential_mixed_service_statistics_check_20261028.py/.json` independently records:

* 18 exact adaptive TEST/USE trees and 276 conditional importance-weight identities in a physical scalar Choi/depolarizing subfamily;
* exact stopped-role/binomial shortfall equality and `E[completed USES]=r E[active calls]`;
* 18 exact binomial-tail diagnostics, certified against a rational upper series for the required exponential;
* 72 full new parameter, local-gradient, expected-error, source-horizon and random-bit budget cases;
* an explicit correlated-Pauli witness distinguishing cumulative marginal from global oracle loss.

The diagnostic scalar controller is not the full mirror-descent algorithm and does not claim a bandit performance run. No random outcomes were sampled. One intermediate replay stopped only at its final stale-source hash guard while the author applied the comparator clarification; all mathematical checks had passed, no output was overwritten, and that script/output history is preserved. The final-source replay passes. The general result uses the received exact bandit proof plus the conditional identities above; full-reference transfer and global twirling are independently bound by the quantum-process reviewer. No production convex solver or hardware was executed.

No unresolved statistical or resource objection remains at the frozen scope: finite ordinary TEST acquisition and multiple actual unknown USE inputs on one retained-memory process, with a cumulative marginal comparator on the ideal mixed occupation, paid complete controls/storage, and an averaged joint-channel guarantee. It is not a relative global-oracle theorem, a per-record high-confidence certificate, a counterfactual-policy guarantee or an indefinitely reusable service.
