# Independent review: history-uniform noisy frame programs

2026-10-29. Reviewer `producer-workspace/review_history_program_bounds`.

**ACCEPT, at the specified IID physical-source / ideal-known-control scope.** The history-uniform envelope, heterogeneous symmetric-SWAP composition, conditional expected-cost bound, finite timeout/restart construction, and nine exact outward-rounded schedules pass. This is a receipt for an approximate program-acquisition interface, not a gate-execution, arbitrary-memory, native-hardware, or advantage theorem. The bound is sharp over the allowed public histories.

## 1. Actual quantum instrument and all-history invariant

The input is the separately received physical family with fixed parameters `R, eta`, `0 <= eta <= eta_U < 1`. Fresh acquired minus records have

`sigma = x Pc + a PW`, `x=eta/(8+eta)`, `a=1/(8+eta)`, and `q_minus=(8+eta)/18`.

The physical-source derivation and exact Lüders growth implementation are existing reviewed dependencies, copied with their receipts. A reduced marginal eigenvalue statement alone would not suffice: fresh source environments, acquisition ancillas and records, with no retained source memory, are essential here.

I independently reconstructed the complementary projector on the full `wedge^k C9 tensor C9` interface for every `k=1,...,7`. For a sorted total-label set `U`, the growth projector is the rank-one block `ss^T/(k+1)` on the product vectors `|U\{j}>|j>`, where `s` contains their wedge signs. Constructing the columns of `I-P`, then actually tracing the new register, gives the author's S and F matrices. This verifies the failure branch, not just successful antisymmetrization. The resulting old state is exactly uniform inside each occupation sector; the check does not artificially dephase a coherent failure output.

Invariance under the stabilizer `U(1) x U(8)` leaves the two inequivalent sectors `wedge^k W` and `c wedge wedge^(k-1) W`. Each recorded growth branch preserves that invariance. Acquisition plus flags and their waiting times concern fresh discarded systems, so they leave the old conditional state unchanged. No unknown-eigenbasis measurement is permitted or needed. At k=8, the fixed exterior/Hodge decoder produces the conjugate missing direction; the stipulated real `c=vec(R)/sqrt(3)` makes this precisely the intended c program, with isotropic error on W.

For a positive two-class matrix, the derivative of its normalized present-weight map has the sign of its determinant. S has nonnegative determinant. Independently of the author's Bernstein calculation, every F determinant is a strictly concave quadratic in x with positive values at both `x=0` and `x=1/9`. Hence F is monotone throughout the interval. The exact identities `S(b_k)=b_(k+1)` and

`[F(1-b_k,b_k)]_present - b_k Tr[F(1-b_k,b_k)] = k(9-k)a x(x-a)/[(k+1)((9-k)a+kx)^2] <= 0`

therefore prove by induction, for **every finite nonzero-probability complete public transcript**, that `r_k <= b_k`. This proof covers arbitrarily many failures; the finite tests are supplements, not the reason the all-history assertion holds. At completion,

`error <= b_8 = 8 eta/(1+8 eta) <= E0 := 8 eta_U/(1+8 eta_U) < 8/9`.

Any classical stopping event or coarsening of these transcripts is a mixture of states in the same convex isotropic envelope and inherits the bound. Zero-probability histories have no conditioned state and are excluded in the usual way.

**Sharpness:** completion in the minimum eight ordinary source calls requires eight minus flags and seven immediate growth successes. Every success saturates the envelope map, so this positive-probability history has error exactly b8. An envelope smaller than b8 cannot be valid for every allowed history without restricting the protocol or excluding fastest completions.

## 2. Independence, histories, and heterogeneous purification

Fix R and eta as physical parameters, not a Bayesian mixture shared by otherwise unrelated batches. For two separately generated batches, the joint branch instrument factors on fresh inputs when conditioned on their respective complete classical transcripts. This remains true under the specified depth-first generation: while a completed child is stored, the other child interacts only with fresh inputs and its own work registers. Protected storage and absence of source memory are load-bearing assumptions.

The two child states can have different conditional errors u and v. Applying the actual symmetric projector, retaining one system, gives unnormalized output `(rho+sigma+rho sigma+sigma rho)/4`, yielding precisely the stated p(u,v) and f(u,v). Exact differentiation verifies that f is increasing in each argument below `(d-1)/d`, while p is decreasing. Thus all accepted child histories with errors at most Ej give parent error at most `E_(j+1)=Ej(1+Ej/8)/D9(Ej)` and parent success at least `D9(Ej)/2`.

Conditioning only on a shared or coarsened schedule can correlate the child errors; one must not assert that such an averaged pair is a product, or plug averaged errors into the product formula without justification. The proof avoids that trap: resolve the separate complete transcripts first, apply the heterogeneous bound there, then mix. Conditioning on the parent success merely reweights outputs already in the same envelope. This is sufficient for the stated protocol. It is not sufficient for arbitrary quantum-correlated input pairs.

## 3. Expected cost and finite cap

The growth hazard given a fresh record is `[1-ka+(a-x)r]/(k+1)`. Since `a<=1/8`, `a>=x` and `r>=0`, it is at least `(1-k/8)/(k+1)` even without using the tighter history envelope. Multiplication by `q_minus>=4/9` pays for every ordinary source call. Summing the conditional geometric waiting bounds gives exactly

`M0 = (9/4)[1+sum_(k=1)^7 8(k+1)/(8-k)] = 41481/140`.

This is attained by the ideal eta=0 family. Conditional failures need not be independent; the uniform lower hazard bounds their survival tails. At a fresh level-j invocation, the expected cost is bounded uniformly over external past histories. This is the fresh-start bound used by the cap, not an unwarranted assertion that a past-conditioned total lifetime has the same mean.

At the next level a trial has conditional expected cost at most `2Mj` and success at least `p_min=D9(Ej)/2`. If trial t is reached, its fresh conditional mean cost is still at most `2Mj`; its reach probability is at most `(1-p_min)^(t-1)`. Summing gives `M_(j+1)<=2Mj/p_min=4Mj/D9(Ej)`. A trial's own cost may correlate arbitrarily with its success and output error. No cost/success independence assumption enters this sum.

The older inverse-error cost lemma is separately accepted **with its frozen boundary erratum**. For fixed `E0<8/9` and target `0<epsilon<E0`, its geometric-decay / bounded-product argument proves `Mj=O(1/epsilon)` at the first target-hitting level. For `epsilon>=E0`, take j=0; for E0=0 the program is already pure. Constants are not uniform as eta_U approaches 1.

Let `L=ceil(2Mj)` and accept a completion at or before the Lth call. Markov gives `Pr(T>L)<=Mj/L<=1/2`. On timeout the specified protocol discards all partial batch/work states and restarts with fresh independent source uses and reset known controls. Therefore r failures have probability at most `2^-r`; a conditional hazard argument would already suffice, so no unneeded independence assertion is required. Total calls are deterministically at most rL. For N separately generated outputs, `r=ceil(log2(N/delta))`, `0<delta<1`, gives union abort probability at most delta and cap NrL.

Every successful attempted transcript still has error at most Ej. Selecting the first successful attempt, its completion time, attempt number, or a cap does not add a quality correction. **This preserves the certified envelope, not the actual output law or actual error.** For eta=.01, the error is exactly 2/27≈.074074 at cap8, while at cap593 it is approximately .0363106366. The uncapped average must not be substituted for either. The title's “availability only” language is accepted solely in this uniform-guarantee sense, consistent with the manuscript's explicit acknowledgement of time bias.

## 4. Reproduction and schedules

`independent_checks.py` performs:

- 9,018 exact projector-column checks in dimension9 and 28 exact sector-input cases, including the full reduced-sector isotropy;
- symbolic success/failure envelope identities and independent determinant-concavity endpoint certificates;
- symbolic heterogeneous SWAP identities/monotonicity in dimensions2,4,9, plus 15 dense unequal-input projector-and-partial-trace checks at random complex orientations (maximum entry residual about2.23e-16);
- exact ordinary-source-call evolution for four eta values through cap593, checking every possible completion-time-conditioned aggregate from8 through593 (2,344 checks), the sharp cap8 equality, and seven-attempt failure bounds;
- all nine outward-rounded schedules reproduced by a separate integer-grid implementation, with no imported author schedule function or floating branch decision.

All three author scripts were rerun in `author_replay/`, never in the immutable source directory. Their JSON results match the captured JSON exactly. Source and dependency hashes are recorded in `SOURCE_MANIFEST.json`; the receipt binds the final review, independent code and results.

For eta_U=.01 and target1e-4, the received schedule has ten levels, per-attempt cap709476 and seven-attempt cap4966332, with abort at most1/128. The target1e-6 cap is635799115. These are conservative ordinary-call budgets, not wall-clock or practical-resource estimates.

## Scope and exclusions

Accepted: the fixed full-rank noisy source family with a valid promised eta upper bound, fresh acquisition batches, exact trusted controls and protected memory; all-history isotropic program envelopes; recursive heterogeneous purification; finite capped fresh retries; and the supplied rational schedules. Existing source-acquisition, physical-label and cost-lemma receipts are dependencies, not silently reaccepted broader manuscripts.

Not accepted here: generic contamination or source memory, drifting frames/noise, statistical identification of eta_U, controller synthesis errors, storage noise, arbitrary eigenbasis-dependent extra measurements, exact finite noisy-frame recovery, native circuit or wall-clock costs, the quaternion transducer, a Choi/PBT gate-execution budget, historical novelty, or an advantage over classical frame calibration. Subsequent use of multiple outputs still needs the appropriate independence or branchwise composition interface; the scalar error envelope alone is not permission to replace arbitrary correlated resources by IID ports.
