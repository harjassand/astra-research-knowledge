# Acquired operations with explicit domains and compositional warrants

Private ASTRA P3 research result, 23 October 2026.

## Scientific conclusion

The harder circuit reuse comparison is complete. Its strongest improvement is explained by an analytic response warrant and ordinary retention. A separate finite-state construction now demonstrates an acquisition chain: acquire a coordinate program, acquire actions in those coordinates, derive an exactly sampled domain, acquire a genuinely new action and readout on that domain, and compose their approximate source warrants. The new action and readout predicted 558 never-queried states each in the independent 1024-state case.

This establishes a restricted working mechanism. It does not establish a new general law of intelligence, a practical physical advantage, or superiority to retaining program learners. The equally informed program-retaining baseline ties. A stronger scientific question remains: how does a learner acquire an affordable certificate that its represented domain is the *intended* physical condition? A compact representation alone does not supply that certificate. The constant-width decision-diagram obstruction below makes this limitation quantitative.

All corpus arguments used here are pinned to revision `0451552424b4679fa9a73faf5849ea5a4af21cf6` of [astra-research-knowledge](https://github.com/harjassand/astra-research-knowledge/tree/0451552424b4679fa9a73faf5849ea5a4af21cf6), beginning with `00_START_HERE.txt`. N780's comparison-decoder theorem and exact-recognition obstruction govern the construction. N51 is not used. The source texts and their hashes remain in `../sources/`.

## 1. What the previous comparison resolved

The first star result remains intact: 27 queries versus 24 for the stronger retaining baseline, with the failed case and its later exact optimal-face repair preserved. The subsequent frozen eight-case circuit comparison used five identical query points for the exponential and ordinary quadratic interpolators; the exponential method was slower. Stronger structural analysis then gave the sharp two-terminal derivative cone and current envelopes. Combining those envelopes with retained local jets answered seven cases without queries and the eighth with one query.

That one-query result is useful, but all eight cases were already exposed. The final query occurred on the last case, so it does not demonstrate subsequent transfer. The source analytic warrant and retained information supply the benefit. An equally informed library learner can perform the same calculation. See `../module_theory/posthoc_retained_local_jet.py`, `../results/posthoc_retained_local_jet_v1.json`, and the unchanged network proofs in `../curvature_theory/`.

The sharp closure remains a substantive mathematical result. For edge derivatives $g=j'>0,q=j'',r=j'''$, the contract

\[
 \frac{3q^2/g-\kappa^2g}{2}\le r\le\kappa^2g
\]

is closed under the stated passive two-terminal network composition. The proof, finite-bit implementations, failures, and exact audit remain available; this work is not replaced by the new representation experiment.

## 2. The representation object and its source contract

The acquired object contains four different things:

1. An executable bijection $C:\{0,1\}^r\to S$, with an exact membership/inverse procedure for its declared raw domain $S$.
2. Candidate operations $P_a:S\to S$ whose permutation property follows from their program syntax.
3. Version-bound observations of the actual source operations $F_a$, plus an acquired bound on their disagreement with $P_a$ under a declared sampling law.
4. Composition rules that state which later programs inherit those bounds and what additional acquisition they require.

The distinction between program syntax and source agreement is essential. A triangular coordinate program can be proved bijective even when it is wrong about the comparison order that suggested it. A program can define and sample its own fiber exactly without proving that the fiber equals a physical energy level or a true rank interval.

The source interface is strong and explicit: exact chosen comparisons; reset to an arbitrary supplied finite bit state; application of one named action; full raw successor-state readout; and later Boolean observable queries. The source is deterministic and version-stable. This is an obtainable interface for some discrete simulators, but it is not automatically available for a laboratory system. N780's comparisons do not themselves supply reset or transition access. No real-valued oracle, source normalizer, source truth table, or global class-membership oracle is an input.

## 3. Acquire a useful chart without claiming recognition

The independent implementation in `acquired_chart.py` follows N780's hidden affine triangular decoder acquisition under its degree promise. Its capped chosen-comparison cost is retained in full.

There is also a source-independent syntactic fact. On every completed binary transcript, the implementation constructs an invertible basis and prefix polynomials. The next constructed subspace excludes the selected basis vector because its constructed response is one. The final triangular program is therefore a bijection. This does not require the arbitrary comparator to belong to N780's class.

Under the source promise, the chart agrees with the true rank. Without that promise, true-rank agreement remains UNKNOWN. The operational experiment uses only the proved bijection and then acquires source evidence for its actions directly. The exact-recognition lower bound is not evaded.

## 4. Acquire actions, derive a domain, and acquire something new

In Boolean coordinates, an involutive shear has the form

\[
 P_{b,f}(y)=y+b f(y),\qquad f(y+b)=f(y).
\]

All arithmetic is over \(\mathbb F_2\). Applying the map twice cancels the same displacement, proving it is a permutation.

For a candidate degree $d$, query the raw source at the chart inverses of all points of Hamming weight at most $d$. There are

\[
 M_d(n)=\sum_{j=0}^{d}\binom nj
\]

such points. Boolean Möbius inversion recovers the vector polynomial interpolant of the displacement. Accept a shear candidate only if all its nonzero vector coefficients equal one direction $b$ and exact symbolic substitution proves $f(y+b)+f(y)=0$. Otherwise retain UNKNOWN and the counterexample.

This is ordinary polynomial interpolation with a structural check. Without a degree promise it produces a candidate, not source membership. For known $b\ne0$, exact identification of degree $d$ controls on $n-1$ independent coordinates already requires at least $M_d(n-1)$ one-bit responses in the worst case. This is a useful tailored baseline, not a new interpolation claim.

Let $B$ be the span of the acquired nonzero directions, of rank $r$. Exact elimination gives a basis $B_1,\ldots,B_r$ and its orthogonal complement $H$. Every candidate preserves $Hy$. For a released raw anchor, form its acquired coordinate $y_0$ and define

\[
 S=\left\{R^{-1}\left(y_0+\sum_{i=1}^{r}t_iB_i\right):t\in\{0,1\}^r\right\}.
\]

This is an exact sampler from $r$ bits, with no rejection or state-space enumeration. Its membership procedure uses the retained inverse chart and elimination. The fiber need not be a dynamical orbit.

The sampler is then used to acquire a NEW source action and readout. They are new targets, released only after the first-stage representation has been saved. A degree $e$ fit now needs $M_e(r)$ chosen target evaluations. Every raw target response is paid. A new action that escapes the fiber on an observed training point receives UNKNOWN. Symbolic restriction of an old candidate uses no new information, but its source agreement on the new domain requires its own warrant.

## 5. A sharp audit that uses retained observations

Fix the final candidate, domain, source version, tolerance and confidence allocation after arbitrary prior learning. Recheck all $k$ distinct retained addresses in the domain against this final candidate. Reject on a mismatch. Let

\[
 N=|S|,\qquad U=N-k,\qquad K=\lfloor\epsilon N\rfloor+1.
\]

A bad candidate with disagreement mass greater than \(\epsilon\) has at least $K$ errors, all among the $U$ unqueried addresses. If $U<K$, the remaining possible error is deterministically at most $U/N\le\epsilon$. Otherwise query a uniform sample of $m$ distinct unqueried addresses, with

\[
 m=\min\left\{j:\frac{\binom{U-K}{j}}{\binom Uj}\le\delta\right\}.
\]

Pass only if every observation agrees. Conditional on the previous history,

\[
 \Pr(\mathrm{PASS}\ \&\ e>\epsilon)\le\delta.
\]

The old observations may have selected the candidate adaptively. The new sampling must remain fresh. This is a frequentist false-warrant statement; it is not a posterior probability following a pass. It has no tolerant-completeness guarantee: a candidate with small positive error can be rejected.

The formula is exact minimax for a cap of $m$ additional queries, arbitrary source completions consistent with the old transcript, and certain acceptance of a clean candidate. To prove this, choose the hidden $K$-error subset uniformly. On any clean run, the verifier has at most $m$ distinct new addresses; unless it hits the hidden set, the transcript is unchanged and it accepts. Its average miss probability is at least the displayed ratio. Uniform sampling without replacement attains it. For expected-query budgets, randomizing between adjacent sample counts can save less than one clean-source query; that is a different optimization problem.

The implementation selects a random rank in the complement of the retained sorted address set and finds the corresponding address by exact rank/select. It does not enumerate $S$. All inverse-chart calls, retained checks, random-bit requests, rejected random draws, rational arithmetic and failed attempts are recorded.

The theorem is in `verification/RETAINED_COMPLEMENT_AUDIT.md`. Its prospectively bound exact check passed 1,640 assertions. Independent implementation review found two accounting/error-handling defects, preserved them, and verified the fixes before confirmation. Earlier helper review likewise preserved and repaired a consumed-generator guard, a mixed-chart composition, and missing estimator argument validation. These development failures remain part of the evidence.

## 6. What can be composed

Let $\mu=U(S)$. Suppose each accepted action warrant gives

\[
 \mu\{F_a\ne P_a\}\le\epsilon_a,
\]

and every candidate $P_a$ preserves \(\mu\). Start the actual and candidate paths from the same fresh state. For any fixed word $a_1,\ldots,a_T$, the first disagreement occurs at a candidate-path state in the corresponding action error set. Each candidate prefix preserves \(\mu\), so

\[
 \Pr(\text{complete paths disagree})\le
 \min\left(1,\sum_{t=1}^{T}\epsilon_{a_t}\right).
\]

The true source need not preserve the domain or its uniform law. An initial law bounded pointwise by \(\rho\mu\) adds a factor \(\rho\). The same valid audit event covers later fixed words selected before the new start. Repeated uses of a warrant multiply its error contribution, while its confidence-failure budget is counted once.

For an acquired Boolean readout with disagreement at most \(\epsilon_h\), the path observable used in confirmation is

\[
 p=\Pr\{h(X_0)\ne h(X_T)\}.
\]

Its source/model difference is at most

\[
 \min\left(1,2\epsilon_h+\sum_t\epsilon_{a_t}\right).
\]

The factor two is necessary because both endpoints use the readout. A terminal mean alone would have been an uninformative choice under uniform permutation candidates: it would not depend on the word.

A further algebraic reuse rule is valid. If an exact guard $g$ makes $f g$ invariant under translation by $b$, the guarded candidate is also an involution. If the actual intervention applies the same source action only when that guard is one, its error set is a subset of the old error set. The guard can therefore be selected after the original audit. Its structural identity and computation must still be checked. Arbitrary state-feedback choice among individually warranted actions does not have this property.

The full operational theorem, counterexamples and horizon-dependent lower bound are in `verification/OPERATIONAL_TRANSPORT_AUDIT.md`. The exact bounded audit passed 88,818 checks. In the arbitrary source contract, certifying complete path accuracy through horizon $T$ can require \(\Omega(T/\eta)\) acquired queries even for a simple cyclic candidate; a reversible-source variant retains the lower bound. The statement does not imply that every particular terminal observable requires that many queries.

## 7. Frozen independent confirmation

Method and criteria were frozen at 2026-10-23 12:56:40 UTC. Freeze SHA256: `60edb7ae270c08b1aa40fba848d6411d9e95fc5f99df40c44b267cf82da22005`. The seven worlds had previously been generated and sealed by an independent native worker who had not read the root implementation. World SHA256: `bf843decd6615e12c5ed8634d86cd782fa98a7bf1467c0ab9834070514afd4cc`.

The root saw the public interface and control categories, but no generated values before freezing. Root-authored integration examples and all helper counterexamples were exposed development data. The learner ran once. All predictions and observations were saved before separate truth validation. No root learner source was changed afterward.

| Case | Declared fiber size | Warranted words / requested | Complete method calls | Direct retaining control calls | Main diagnostic |
|---|---:|---:|---:|---:|---|
| 01 | 8 | 3 / 3 | 397 | 397 | Regular source |
| 02 | 4 | 3 / 3 | 245 | 245 | Actual orbit sizes 1 and 3 |
| 03 | 8 | 3 / 3 | 589 | 589 | Global action error 1/16, local error zero |
| 04 | 4 | 0 / 3 | 665 | 687 | Global error 1/512 becomes local error one; new action escapes |
| 05 | 8 | 3 / 3 | 475 | 475 | Comparator differs on two ranks; operational tasks still valid |
| 06 | 8 | 3 / 3 | 990 | 990 | New readout valid only on selected domain |
| 07 | 1024 | 3 / 3 | 6238 | 8534 | Genuine predictions beyond queried states |

The lower call count in case 04 is not a successful comparison: the learned mechanism returned UNKNOWN, while the direct control answered. No false warrant was observed. All 18 issued composition intervals and path bounds contained the separately computed truths. All seven candidate domains happened to equal the fixtures' intended fibers; that is evaluator evidence, not a domain-membership certificate acquired by the learner.

The large case used 20 raw bits, ten acquired directions and a 10-bit fiber. Stage one cost 2328 comparisons plus 2110 transition queries, or 4438 calls. The later stage used 112 fitting calls and 1688 audit calls, for 1800 additional calls. Both the new action and the new readout queried 466 of 1024 domain states; each predicted the remaining 558 correctly. These targets were unavailable before stage two. The three source change probabilities were $1/4,13/32,3/8$. The reported intervals were respectively $[13/64,19/64]$, $[21/64,31/64]$, and $[9/32,15/32]$.

The direct retaining control used the same first-stage observations and sampler, and retained every later raw result across words. It chose a source census whenever cheaper in trajectory count than its prescribed Hoeffding estimator. Its 4096 later calls give 8534 complete calls. This control is not the strongest possible estimator. The equally informed program-retaining learner can fit and execute the same ordinary ANF programs, use the same structural checks and audits, and tie. The frozen independent interpreter matched all 18 candidate expectations.

The stronger retaining baseline was then implemented separately as a labeled **post-test reconstruction**, using only the raw training observations and the common acquired chart/fiber. Its ordinary degree-two Möbius fitter reconstructed all six available new actions and all seven readouts, with exact identity of every canonical polynomial coefficient. It independently returned UNKNOWN on case 04's observed domain escape. Functional identity on the entire declared fiber transports the same 13 source warrants without further confidence allocation; replay also matched all 1008 saved audit rows. This is stronger than giving a baseline the already fitted programs.

The reconstruction used 181 originally paid training responses, totaling 4421 declared payload bits. It made no new source query and read no ground truth. Across all seven cases, both online pipelines retain the same 9599 counted comparison/transition/readout calls: 7649 shared first-stage calls and 1950 extension calls. The retrospective reconstruction does not make those acquisitions free. Its complete successful projection/fit/validation body took 0.467762264 seconds; a preserved projection-field-name failure before fitting added 0.033277346 seconds. These are analysis costs, not an online speedup. Details, functional-identity proof, input separation and failures are in `implementation/retaining_baseline_posttest/RESULT_AND_PROOF.md`.

No DreamCoder training or benchmark run was performed; no claim about beating DreamCoder or another general library learner follows. The comparison is to an explicit, strong tailored retaining program mechanism with the same interface and observations.

### Complete costs and precision

Verification supplied 93.8% of the large case's later source calls. A claim based only on the 56 fitting points per new target would be misleading. The complete source-response payload was 71,674 bits for the learned process versus 106,992 for the direct control. Raw input addresses, comparison inputs, random bits and cache payloads are separately recorded.

All source states were exact finite bits. Confidence arithmetic used exact integers/rationals; the largest audit denominator was 116 bits. The large case requested 22,600 audit random bits, including rejection sampling. Seeded PRNG execution tests the algorithm; the statistical theorem assumes fresh independent uniform randomness. The conservative union allocation used 48 statements at $1/12800$, totaling $3/800$, below the frozen $1/100$ ceiling. Exact small-domain warrants did not actually need statistical risk.

All candidate expectations were integrated exactly because the domain enumeration required fewer candidate trajectories than the prescribed Monte Carlo count. This was enumeration of an acquired program, not free enumeration of the source. The large case's main work plus final acquisition-file serialization took approximately 1.7823 seconds after subtracting the separately timed retaining interpreter. The direct process with the same shared acquisition and its output serialization took approximately 1.7761 seconds. These are one-run instrumented timings, not a demonstrated speed improvement. The entire seven-case comparison took 2.9226 seconds; separate truth validation took 3.3086 seconds. These code timers exclude interpreter imports, tool orchestration and theory development.

Full observations, failed attempts, arithmetic/work records and costs are in `confirmation_v1/`, with aggregation in `confirmation_analysis.json`. Exact validation enumerated only small domains and small ambient cubes; the 20-bit ambient transition table was not solved. A frozen validator counter is conservatively interpreted on short-circuit chart mismatches, as disclosed before execution. Its large-case true-rank status remains UNKNOWN where the evaluator's mode-label test did not establish it; no operational claim relies on that status.

## 8. A stronger representation meets a different obstruction

The Q2R Ising source is a useful scientific boundary. Its published dynamics is reversible and conserves a nonlinear two-layer Ising energy. Exact counting for its $4\times4$ system gives 2720 states at energy \(-24\). Since 2720 is not a power of two, that complete energy level cannot be a single affine fiber in *any* bijective binary chart. The proof and count are in `../application_agent/action_program_challenge/`; the model's energy definition is in Section 2.3.3 of [Montalva-Medel, Rica and Urbina, 2019](https://arxiv.org/html/1903.11761v1).

A counted decision diagram can represent non-affine sets. It still does not cheaply acquire or certify their completeness. Here is a precise information obstruction.

Let $B\subseteq\{0,1\}^n$ be one prefix cylinder of density $q=2^{-k}$. Partition its complement into $M=(2^k-1)2^d$ cylinders $C_a$, each of size $|B|/2^d$. The true energy-zero set is either $B$, or $B\cup C_a$ for one hidden $a$. Every alternative has an ordered binary decision diagram with at most two nonterminal nodes per level and $O(k+d)$ nodes. Counting and sampling its supplied description are easy.

Every sample drawn from $B$ passes the energy check in every alternative. Yet

\[
 \operatorname{TV}(U(B),U(B\cup C_a))
 =\frac1{2^d+1}=:\varepsilon.
\]

A certifier accepting the complete case with probability at least $1-\alpha$ and each incomplete case with probability at most \(\beta\) must, on the complete case, query each possible cylinder with probability at least $1-\alpha-\beta$. A point query visits at most one cylinder. Thus

\[
 \mathbb E Q\ge (1-\alpha-\beta)M
 =(1-\alpha-\beta)\frac{(1-q)(1-\varepsilon)}{q\varepsilon}.
\]

The obstruction is acquisition of omitted mass, not counting or storing a known representation. More candidate samples cannot resolve it. A supplied target description, target sampler, equivalence oracle or independently proved structural law changes the information contract.

A valid paid audit separates support correctness and completeness. For true condition $A$, write $u=\Pr(A\mid B)$, $v=\Pr(A\mid B^c)$. Rejecting invalid candidate samples gives $U(A\cap B)$, whose exact error relative to $U(A)$ is

\[
 \frac{(1-q)v}{qu+(1-q)v}.
\]

Estimating $u$ and omitted mass $v$ produces a sound certificate, with the same inverse-rarity scale in the zero-discovery regime. See `../application_agent/conditioning_coverage/PROOF.md` and its exact checks. This is a scoped indistinguishability result, not a claim that cumulative learning is impossible.

## 9. The next direction and the existing-method boundary

The strongest continuation is acquisition of a *verified local dependency interface* that makes a scientifically meaningful domain complete. For example, if the dependency set of each single-bit energy difference is independently verified from an exact source program, the learner can acquire its finite local table. Starting at one reference state, summing those local differences along a fixed bit-flip path telescopes to the exact global energy. A finite-width count/unrank program can then compute energy-level counts and sample complete conditions without receiving a normalizer.

The verification of those dependency sets is the substantive input. Observing a few local differences does not prove that an unobserved high-order interaction is absent. In Q2R, locality follows from the published equation, and a full-source transfer-matrix method receives the same fact and can avoid acquiring already explicit tables. Therefore this example supplies a clean scientific access contract, not a new advantage over the tailored solver. Large square systems still have exponential frontier-width costs.

Generic inverse/sampler-assisted learning already has direct prior: [Binnendyk et al., ALT 2022, Lemma 9](https://proceedings.mlr.press/v167/binnendyk22a/binnendyk22a.pdf). Counting and conditioning tractable compiled representations are established knowledge-compilation operations: [Darwiche and Marquis, JAIR 2002](https://arxiv.org/pdf/1106.1819). The candidate-path error propagation also belongs to standard coupling/simulation-lemma machinery; [MOPO, NeurIPS 2020, Lemma 4.1 and Assumptions 4.2–4.3](https://proceedings.neurips.cc/paper/2020/file/a322852ce0df73e204b7e67cbbef0d0a-Paper.pdf) already uses learned-model occupancy and an assumed admissible error interface.

For a fixed feedback policy, an obtainable replacement for an assumed error interface is to sample independent candidate trajectories, choose a uniform time in each, and query the true successor at that candidate state/action. If the average disagreement is at most \(\eta/H\), first-disagreement coupling bounds the entire $H$ step path error by \(\eta\). This removes the permutation requirement for the fixed audited policy. It costs $O((H/\eta)\log(1/\delta))$ source comparisons and naive $O((H^2/\eta)\log(1/\delta))$ candidate simulation work. A single trajectory with many sampled times does not provide independent audit observations. Prior uniform warrants transfer only with a proved state-action occupancy bound. This extension is a known type of coupling result with an explicit acquisition procedure; it is not a new general policy-learning theorem.

The concrete next scientific investigation is whether a source with previously unavailable local structure permits acquisition and verification of such a dependency interface at a cost below its best retaining solver, then reuses it across changed physical conditions. Additional circuit size, derivative order, authored hidden encodings or larger tables would not answer that question. The present mechanism, exact lower bounds, scientific counterexamples and baseline ties are retained as constraints on that investigation.

## Evidence status

Proved: syntactic chart/domain facts, shear/invariant construction, operation-specific composition, guarded inheritance, finite-support audit and its scoped minimax lower bound, and the stated completeness obstruction. Executed: authored development, independent finite checks, one frozen seven-case acquisition comparison, separate exact validation, and a labeled post-test retaining baseline. Acquired physical measurements: none. Historical novelty: UNKNOWN. Advantage over equally informed retaining program learners: none established. Consequential physical computation newly made tractable: UNKNOWN under the access contracts examined.

The bounded construction and requested harder comparison are complete. The remaining programme question is a different scientific contract: acquiring warranted local structure rather than presuming it or merely retaining its consequences.
