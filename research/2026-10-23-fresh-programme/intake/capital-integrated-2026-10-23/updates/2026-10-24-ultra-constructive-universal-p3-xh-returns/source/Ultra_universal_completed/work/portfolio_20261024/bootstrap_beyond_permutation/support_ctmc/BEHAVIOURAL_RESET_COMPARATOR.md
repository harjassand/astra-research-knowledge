# Observable reset by acquired randomized controls: comparator and contract audit

24 October 2026. Bounded source comparison and algebra audit of the frozen `FIRST_CONSTRUCTION.md`. No novelty or empirical-advantage claim.

## Finding

The proposed operation is not covered end-to-end by the located PSR/OOM, synchronizing-automata, or finite-consensus theorems. The pieces are, however, classical: finite-Hankel-rank realization gives observable linear operators; exact synchronization asks for a word whose transition operator has identical rows; finite matrix switching can give asymptotic consensus; and, once a finite operator library is known, a positive mixture that resets an observable quotient is a linear-feasibility problem. The remaining candidate-specific obligation is to acquire and robustly certify such a *positive mixture of legal words* from the stipulated scalar experiments, with its randomization record and time interface specified.

There is a more immediate scope gate. A mixture of word operators resets the *marginal future test law* only when the selected word is marginalized. If the selected word is recorded or known to the next controller, it must reset conditionally on each supported word. The construction currently says “all future visible behaviour”; that wording needs the record convention made explicit.

## Exact observable algebra

Use row predictive coordinates. For a complete set of `r` test columns `T`, let the predictive row be `x(w) = (h(w t_j))_{j=1}^r`. Let `B = (b_i)_{i=1}^r` be a complete set of reachable histories and `H_ij = h(b_i t_j)` be nonsingular. For a fixed open-loop control word `u`, set `(H_u)_ij = h(b_i u t_j)`. Then

\[
H_u=H M_u,\qquad M_u=H^{-1}H_u,
\]

and `x(wu) = x(w) M_u` on the complete predictive quotient. If `c` is the normalization column, every normalized predictive row satisfies `x c = 1`, and probability-preserving control words satisfy `M_u c = c`. A basis change conjugates the `M_u` and changes `c` contragrediently; physical feasibility is basis-invariant.

For a probability vector `λ` on a **finite, legal** word library `W`, write `S_λ = Σ_{u∈W} λ_u M_u`. The condition for an exact reset of all test probabilities after *marginalizing the randomized word* is

\[
xS_\lambda=x'S_\lambda\quad\text{for every pair of reachable predictive rows }x,x'.
\]

Equivalently, if (D=\operatorname{span}\{x-x':x,x'\text{ reachable}}), then (DS_\lambda=0); the common target (v=xS_λ) is a valid normalized predictive state. If reachable rows affinely span the entire normalized hyperplane {x:xc=1}, then (D=c^\perp) and this is equivalent to (S_λ=cv), (vc=1), i.e. rank one with the normalization direction fixed. Without that full-affine-span condition, (S=cv) is sufficient but may be stronger than necessary. A finite basis of tests is enough only if its completeness has been established; untested continuations can distinguish states that coincide on a truncated test list.

Given exact `M_u` for a fixed finite `W`, searching a reset mixture is not a nonlinear rank-minimization problem: impose `λ ≥ 0`, `Σ_u λ_u = 1`, and either `S_λ = c v` with variable `v`, or `d S_λ = 0` for a basis of `D`. These are linear equalities and inequalities. Minimizing a stated additive word cost `Σ_u λ_u d(u)` is also an LP. Carathéodory bounds a feasible mixture’s support by `q + 1`, where `q` is the affine dimension of the legal operator hull (at most `r²`); this does not bound word length or discovery time. If words have unequal elapsed durations, either pad them with a supplied harmless idle to a common reset boundary or define time/duration records as unobserved; otherwise timing itself may distinguish the mixture components.

The LP weights must be nonnegative. Signed spectral/OOM coordinates are allowed, but a signed combination of word operators need not be executable. Conversely, if each `M_u` is the correctly identified quotient operator of a *real legal word* and `λ` is a genuine probability vector, the mixture itself is a physical randomized control, even if the matrices have signed entries in the chosen coordinates.

### Logged-word counterexample

Take two hidden states and two controls, identity (I) and swap (F), with a later visible binary test of which state is occupied. In row convention,

\[
I=\begin{pmatrix}1&0\\0&1\end{pmatrix},\quad
F=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
S=\tfrac12(I+F)=\begin{pmatrix}\tfrac12&\tfrac12\\\tfrac12&\tfrac12\end{pmatrix}.
\]

The unconditioned post-mixture state is uniform from either initial state, so `S = c v` and outcome-only future tests agree exactly. But condition on the known chosen control: initial state 0 followed by `I` yields state 0, while initial state 1 followed by `I` yields state 1; `F` swaps the distinction rather than removing it. Thus the joint law of `(chosen word, future test)` differs between initial histories. This is an exact behavioural reset only if the word/seed is discarded from the downstream interface and the reset statement is marginal over it. If the downstream learner sees the reset action trace—as ordinary controlled-process histories do—the correct condition is `x M_u = x′ M_u` for every supported `u`. This example also shows why independently randomizing each letter is not interchangeable with sampling one correlated whole word: the implemented policy class must match the convex hull being optimized.

## Strongest located outside comparators

**Observable realization and system identification.** Thon and Jaeger unify stochastic multiplicity automata, OOMs, and PSRs as algebraic sequential models; the finite Hankel rank is the dimension of a minimal linear observable realization. This directly covers the construction's `H^{-1} H_u` coordinate extraction, but not positivity of the chosen representation or synthesis of a reset [Thon & Jaeger (2015)](https://jmlr.org/papers/v16/thon15a.html). James and Singh's original PSR discovery/learning algorithm is explicitly for controlled systems *with a reset operation*; it treats reset as an available access primitive rather than learning one from the operators [James & Singh (ICML 2004)](https://doi.org/10.1145/1015330.1015359). McCracken and Bowling provide online empirical PSR discovery/learning, but no theorem that an unknown system can be forced to a common future predictive state by an acquired randomized intervention [McCracken & Bowling (NeurIPS 2005)](https://papers.nips.cc/paper_files/paper/2005/hash/c3008b2c6f5370b744850a98a95b73ad-Abstract.html).

The strongest finite-sample single-stream comparator located is Balle and Maillard. Their controlled result learns a reactive PSR from a single trajectory under a *known finite-state policy*, an action-exploration lower bound, a supplied finite Hankel prefix/suffix basis and rank, plus geometric mixing of both the coupled behavior and a normalized reference process. The theorem controls Hankel estimation; their conclusion explicitly leaves full PSR PAC-RL for future work. This is strong observable-model acquisition without resets, but it neither produces a repeatable initial distribution nor certifies the positive word-mixture LP. Moreover, their spectral weighted-automaton realization need not be a same-rank probabilistic/nonnegative realization; a signed minimal quotient is a prediction model, not a physical hidden-state simplex [Balle & Maillard (ICML 2017), Sec. 5 / Thm. 6](https://proceedings.mlr.press/v70/balle17a.html). The acquired-reset contract still needs its own sample/conditioning margin, because exact rank-one feasibility is unstable under noisy Hankel estimates near the boundary.

**Exact probabilistic synchronization.** Kfoury's classical “synchronizing sequence” for a probabilistic automaton is a *single input word* that leaves the automaton in the same state distribution regardless of its initial distribution, i.e. in a state-coordinate realization the word product has identical rows. A later primary treatment distinguishes Kfoury's exact criterion from its own asymptotic strong/weak concentration semantics and reports the Kfoury decision problem as undecidable [Kfoury (1970), DOI 10.1002/SAPM1970491101](https://doi.org/10.1002/SAPM1970491101); [Doyen, Massart & Shirmohammadi (2011), Sec. 1](https://www.lsv.fr/~doyen/papers/Infinite_Synchronizing_Words_for_Probabilistic_Automata.pdf). That is the closest exact reset comparator for a **pure word** and known transition matrices. It does not subsume mixtures: the `I/F` example has a rank-one convex mixture although neither pure word synchronizes. The 2011 paper's strong/weak notions instead ask for an infinite action-distribution sequence whose hidden-state distribution becomes concentrated on one state asymptotically. They are not the one-shot, possibly non-pure output-equivalence operation proposed here.

**Finite-matrix consensus.** Chevalier, Hendrickx, and Jungers prove that for a known finite set of stochastic matrices, an open-loop switching schedule drives every initial opinion vector to asymptotic consensus iff a product has a positive column; they give an `O(n^4)` pair-graph decision algorithm and an `O(n^3)` positive-column witness-length bound. Repeated iid switching with every matrix assigned nonzero probability then converges almost surely. This is a useful approximate-forgetting baseline for repeated use of known operators, not exact finite-time reset: positive-column products are generally not rank one, and the convergence rate depends on the positive-column mass. It also assumes the operators are already known [Chevalier, Hendrickx & Jungers (2015), Props. 1–2, Thms. 4–5](https://arxiv.org/abs/1505.00144). Finite-time consensus papers that do obtain a rank-one finite product impose graph/update-matrix structure and design the sequence; this is the pure-product access class, not an acquired convex mixture [Hendrickx, Shi & Johansson](https://arxiv.org/abs/1302.6668).

These results provide a strong conventional pipeline when their inputs are supplied: learn/identify predictive operators; find a pure synchronizing word, or a mixing schedule for an approximate reset; keep all preparation actions and stateful data; and replan. The candidate's only potentially distinct step is to estimate an *unknown system's* complete predictive operator set and certify a finite **positive randomized-word** reset under a charged experiment interface. There is no located primary finite-sample theorem for that full pipeline.

## Internal governing-source boundary

The older Astra files do not supply that missing step:

* N189's parity acquisition proof uses a supplied noiseless parity-block subclass and GF(2) equations; it explicitly withholds a general unknown-HMM claim and makes no advantage claim over direct algebra. Its predictive-feature mask is not an acquired control reset. The preserved archive status is `source_derived_unreviewed`; its indexed proof range was not completeness-audited.
* N662's stationary sampler takes rational local generators, additive reset hazards, product reset laws and a positive reset channel as model inputs. Its sampler uses those specified resets; it does not synthesize a new behavioral reset from outcomes.
* N665's acquisition corollary explicitly requires isolated local clock probes, known hazard-zero pattern and forced labelled reset draws, with rate/conditioning floors. It is a scoped model-identification route under stronger intervention access, not passive discovery or positive-mixture reset synthesis.

The exact governing files read were `work/astra-capital/frontier/dossiers/N189.txt`, `frontier/proof_ranges/baf54d7d0f3f03e438497a9d.txt`, `updates/BR/package/research_packet/work/learning_acquisition/RESULT.txt`, `work/astra-capital/frontier/dossiers/N662.txt`, `updates/CY/package/landmark_capability/research/reset_sampler/RESULT.txt` and `REGENERATIVE.txt`, and `frontier/dossiers/N665.txt` plus `updates/CY/package/landmark_capability/research/reset_sampler/ACQUISITION.txt`. These archive records themselves retain unreviewed/source-reported statuses; this note does not elevate them.

## Decision gates for the frozen construction

1. Define whether the reset random seed/word and its elapsed duration remain visible. If visible, require conditional reset for every positive-weight word; if hidden and marginalized, state that the intervention changes the experimenter's information state and include the record-erasure mechanism/cost.
2. State whether “future behavior” includes all action-observation continuations, or a finite test family. Exact behavioral reset needs a complete continuation basis and a complete reachable affine span (or use the weaker `D S = 0` criterion on a certified reachable-difference basis).
3. Fix the intervention library and word-duration budget. With exact operators, solve the LP and report infeasibility as a meaningful failure. Do not assume a mixture exists.
4. For noisy probabilities, give a robust certificate with a bound on Hankel conditioning, model-rank/completeness and reachable-state coverage. A small residual on acquired basis rows is not a uniform reset guarantee without that bridge.
5. Compare total acquisition, fitting, verification, random-word execution and elapsed-time costs against both the expensive external initializer and an equally informed full-history PSR/stateful likelihood learner. No savings theorem or capability gain follows from the exact algebra alone.

