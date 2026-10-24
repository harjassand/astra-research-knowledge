# Local guard-island construction: exact predecessor and interface boundary

24 October 2026. Bounded source comparison for `FIRST_CONSTRUCTION.md`; no novelty or advantage claim.

## Mathematical core is standard PCA coupling

For a binary finite-range synchronous process, fix the guard-stage action (a_i) at each trained site and write its local rule as (p_i(x_{N_i})=\Pr[X_i(t+1)=1\mid X(t)=x,a_i]). Define

\[
 C_{ij}=\max_{x_{N_i},x'_{N_i}:\,x_\ell=x'_\ell\ (\ell\ne j)}|p_i(x_{N_i})-p_i(x'_{N_i})|,
\]
with (C_{ij}=0) off the supplied dependency graph. A coordinate telescoping gives
\[
 |p_i(x)-p_i(y)|\leq\sum_{j:x_j\ne y_j} C_{ij}.
\]
Couple the two Bernoulli updates using the same fresh uniform (U_i); their mismatch probability is exactly (|p_i(x)-p_i(y)|). Thus, with (D_t(i)=\Pr[X_i(t)\ne Y_i(t)]),
\[
 D_{t+1}(i)\leq\sum_j C_{ij}D_t(j).
\]
This is the usual Dobrushin–Vaserstein one-step disagreement inequality for a probabilistic cellular automaton (PCA), with the influence orientation chosen so each row is a destination site. If the selected modes have row sums at most (q<1), disagreement contracts in the sup norm by (q). Product-form independent updates are part of the PCA contract; the coordinate bound itself uses only the common-uniform coupling.

For a finite guard (B), comparing arbitrary outside configurations while applying the same chosen modes inside (B) gives, for (i\in B),
\[
 D_{t+1}(i)\leq\sum_{j\in B}C_{ij}D_t(j)+b_i,\qquad b_i=\sum_{j\notin B}C_{ij}.
\]
Iterating yields the initial-interior term at most (q^t). The boundary term is
\(\sum_{s=0}^{t-1}(C_B^s b)_i\). Normalize (C) by (q): its rows are substochastic, and these summands are the probabilities of first exiting (B) at step (s+1), discounted by (q^{s+1}). If the shortest directed dependency-path distance from i to B^c is d (infinite if there is no such path), exit cannot occur before d steps; for symmetric wiring this is ordinary graph distance, so their sum is at most (q^d). Hence the stated bound
\[
 D_t(i)\leq q^t+q^{d(i,B^c)}
\]
is valid (for (q=0), interpret it directly as zero influence after one update). This first-exit interpretation is useful: summing (q^{s+1}) over all (s\ge d-1) without the disjoint exit-time probabilities would introduce an unnecessary (1/(1-q)) factor.

If the future visible support is (A) and the next experiment runs for (H) updates with all controls respecting the same finite-range graph, let (F_H(A)) be its backwards causal cone at the preparation boundary. Common uniforms and common policy randomization couple its full visible transcripts whenever the two prepared configurations agree on (F_H(A)). A union bound therefore gives
\[
 d_{TV}(\mathsf{Law}_x(\text{future transcript}),\mathsf{Law}_y(\text{future transcript}))
 \leq \sum_{i\in F_H(A)}D_t(i)
 \leq |F_H(A)|\big(q^t+q^{R-H+1}\big)
\]
when B is a backwards-dependency guard of depth R around A, R≥H (for symmetric wiring, the ordinary radius-R neighborhood). This is **target- and finite-horizon behavioral equivalence**, not a reset of the global physical state or its hidden state. The claim survives an adaptive future policy if it chooses the same action on the coupled common transcript; it does not assert equivalence for unbounded horizons or for controls outside the graph contract.

## Closest primary predecessors

- Vaserstein, “Markov Processes over Denumerable Products of Spaces, Describing Large Systems of Automata” (1969), is the foundational product-space/local-automata coupling and stationary-uniqueness criterion. The direct modern PCA framing is Louis, “Ergodicity of PCA: Equivalence between Spatial and Temporal Mixing Conditions” (2004), DOI [10.1214/ECP.v9-1116](https://doi.org/10.1214/ECP.v9-1116). Louis defines synchronous PCA as independently updated local kernels and states that, for attractive PCA, exponential decay of boundary influence for finite-volume invariant measures is equivalent to exponential temporal ergodicity (Theorem 1); the reversible Gibbs subclass is treated separately. The candidate is not required to be attractive or Gibbsian: its stronger local row-sum contraction gives the simpler direct coupling above, and its finite guard / finite target cone is a finite-time corollary rather than a new mixing principle.
- The 2024 primary paper by Bayraktar, Lu, Maggioni, Wu, and Yang, [“Probabilistic cellular automata with local transition matrices: synchronization, ergodicity, and inference”](https://arxiv.org/abs/2405.02928), is the closest learning comparator. It estimates local dynamics and proves non-asymptotic accuracy bounds (Theorem 4.12) under identifiability for multiple-trajectory/ensemble data, and handles a single long trajectory asymptotically under ergodicity (Theorem 4.6). But its kernel is constrained to depend linearly on the empirical neighborhood-state distribution; it assumes fully observed trajectories and a known finite cyclic graph, and it does not treat noisy nondemolition sensing, action-conditioned local tables, mode selection by a robust Dobrushin certificate, or a finite guard-island task. Thus it is a strong precedent for estimation and PCA analysis, not a theorem already supplying this exact interface.
- Billings and Yang, [“Identification of Probabilistic Cellular Automata”](https://doi.org/10.1109/TSMCB.2003.810437) (2003), directly addresses extracting local stochastic rules and neighborhoods from spatiotemporal patterns, but is a specialized binary rule/noise representation and simulation-based neighborhood-search/GA method, not a finite-sample certificate for arbitrary local response tables.
- Dobrushin’s 1968 conditional-probability paper, [DOI 10.1137/1113026](https://doi.org/10.1137/1113026), is the Gibbs random-field uniqueness/regularity predecessor. It should not be described as the transition-learning or guard-preparation theorem: a Gibbs conditional specification is not the same object as a controlled one-step PCA kernel.

## What is genuinely additional, and what remains supplied

The operation not supplied by classical coupling is the *data-acquisition wrapper*: pay for initializer draws, local QND reads, and action/update trials; estimate the finite table entries with simultaneous confidence intervals; compute upper bounds on every (C_{ij}^{a}); and select deterministic public site modes only when a robust row-sum margin (q<1) is certified. This is conventional local system identification plus a standard contraction certificate. A stateful model-based comparator given the same wiring contract and the same ordered read/action/outcome data can fit the same tables, compute the same intervals, and run the identical selector and guard protocol; it ties the operation. No algorithmic superiority is established.

The structural assumptions remain supplied, not learned: known cell identities and bounded-degree graph; complete binary physical state; true finite interaction radius; synchronous updates; independent fresh local transition noise conditional on the current configuration; legal site-mode interventions; and a measurement/hold window in which repeated QND reads refer to an unchanged bit. Finite observations cannot certify absence of unrepresented long-range or persistent memory. Majority sensing further needs independent fresh read errors (or a separately calibrated readout model); a per-read error ceiling below (1/2) alone does not make repeated reads concentrate. To report a valid confidence statement, bound sensor errors over the full capped adaptive run and use time-uniform/simultaneous intervals for context counts. Sensor error and finite sampling must leave enough slack to certify (q<1).

Every required local context and action must be visited. The supplied initializer may make some rare contexts prohibitively costly; if they are never covered, or if their confidence intervals cannot certify contraction, the correct output is `UNKNOWN`, not an inferred favorable kernel. With radius/degree (s), the unrestricted binary table has (2^s) contexts per action, so cost can grow exponentially in local degree. The capability is plausible only within the explicit complete-state/local-wiring and coverage contract; finite guard preparation does not remove that acquisition or physical-interface burden.

## Sources checked

1. L. N. Vaserstein (1969), “Markov Processes over Denumerable Products of Spaces, Describing Large Systems of Automata,” *Problems of Information Transmission* 5(3), 47–52. [Primary Math-Net record and full-text link](https://www.mathnet.ru/eng/ppi1811).
2. P.-Y. Louis (2004), “Ergodicity of PCA: Equivalence between Spatial and Temporal Mixing Conditions,” *Electronic Communications in Probability* 9, 119–131. [Primary article page](https://doi.org/10.1214/ECP.v9-1116).
3. E. Bayraktar, F. Lu, M. Maggioni, R. Wu, S. Yang (2024), “Probabilistic cellular automata with local transition matrices: synchronization, ergodicity, and inference.” [Primary preprint](https://arxiv.org/abs/2405.02928).
4. S. A. Billings and Y. Yang (2003), “Identification of Probabilistic Cellular Automata,” *IEEE Trans. SMC Part B* 33(2), 225–236. [DOI](https://doi.org/10.1109/TSMCB.2003.810437).
5. R. L. Dobrushin (1968), “The description of the random field by its conditional distributions and its regularity conditions,” *Theory of Probability and its Applications* 13(2), 197–224. [DOI](https://doi.org/10.1137/1113026).
