# Orientation memory: primary collision and physical scope

29 October 2026. Targeted complementary review by `controlled_realization_frontier` of root's `../ORIENTATION_MEMORY_AND_SUSTAINED_ENTROPY.md`. This checks antecedents and interpretation, not the algebra independently reviewed elsewhere. No new fixture, acquisition, or implementation advantage is claimed.

## Finding

The asymmetric orientation mechanism has a direct known special case. The correction separating stationary parity divergence from additive entropy production is also established. Neither should be presented as a new physical model or a new entropy identity.

Within the bounded primary reading below, I did **not** locate the assembled theorem: every finite source CTMC has its entire observed path law on any fixed finite horizon approximated by irreducible hidden-parity CTMCs of fixed size `4n`, with a common fixed microscopic escape clock and arbitrarily small sustained reversal-KL rate. Nor did I locate its consequent uniform finite-data nonidentifiability statement with explicit preparation and relaxation costs. This is a scoped search result, not a priority determination.

The proposed addition is a **universal quantitative closure obstruction**, built from established lifting and entropy ingredients. The source model is supplied. Its physically meaningful application depends on whether the declared reversal and preparation class are appropriate to the actual system.

## 1. Closest explicit entropy-model antecedent

**Kim, Lee and Jeong (2022), _Estimating entropy production with odd-parity state variables via machine learning_, Physical Review Research 4, 023051.** [Publisher](https://doi.org/10.1103/PhysRevResearch.4.023051); [primary preprint](https://arxiv.org/pdf/2112.04681).

Equations (3)–(14) explicitly separate forward/reversed two-time KL into additive entropy production plus `D(p || p∘Theta)`, estimating the latter separately. Section III supplies states `(n,v)` on a ring, reversal `(n,−v)`, motion rates `f_±`, and sign-flip rates `r_±`; it credits Lee–Kwon–Park. Equations (16)–(26) include both jump and waiting-time terms. The method observes the microscopic parity variables and supplies their reversal map.

**Exact specialization:** choose equal motion rates `f_+=f_-=f`, and `r_+=κ ε`, `r_−=κ(1−ε)`. This is root's two-copy construction for a unidirectional uniform cycle. The paper does not formulate arbitrary-source approximation, hidden-even-readout nonidentifiability, or common-clock completion. Its explicit two-time boundary subtraction is already the predecessor of `B+Tσ` accounting; root's universal path approximation is the distinct proposed implication.

## 2. General adjoint lifting is established machinery

**Andrieu and Livingstone (2021), _Peskun–Tierney ordering for Markovian Monte Carlo: Beyond the reversible scenario_, Annals of Statistics 49, 1958–1981.** [DOI](https://doi.org/10.1214/20-AOS2008); [author manuscript](https://discovery.ucl.ac.uk/10108137/1/Livingstone_20-AOS2008.pdf).

Section 3.3, equations (5)–(7), constructs two sign copies from adjoint sub-Markov kernels, with sign reversal as the involution. It gives free switching rates subject to a balance constraint and symmetric invariant sign weights. Section 4 treats the continuous-time counterpart. Choosing a kernel and its stationary adjoint gives the familiar forward/reverse lift. Thus introducing `Q*`, a persistent hidden orientation, or involution reversibility is established mathematics.

The asymmetrically weighted, weakly coupled nonequilibrium family in root's theorem deliberately leaves their symmetric invariant-measure class. Their goal is comparison of samplers, not a universal entropy-inference obstruction. The new claim should identify what the biased preparation and fixed-clock extension establish beyond applying this standard lift.

## 3. Parity asymmetry is not generally a purely transient entropy effect

**Lee, Kwon and Park (2013), _Fluctuation Theorems and Entropy Production with Odd-Parity Variables_, Physical Review Letters 110, 050602.** [Publisher](https://doi.org/10.1103/PhysRevLett.110.050602); [primary preprint, earlier title](https://arxiv.org/pdf/1209.0543).

The published abstract and preprint equations (3)–(5), (19)–(24) distinguish odd-state stationary asymmetry, detailed-balance violation and nontransient housekeeping contributions. The path formula retains escape-rate differences under physical reversal. Their equilibrium criterion includes symmetry of stationary probabilities between parity partners.

This does not undermine root's small positive `σ`. It forbids explaining a generic asymmetric stationary model by a boundary term alone. Root's special rate pairing makes its sustained contribution small; `B` and that contribution are separately calculated. At any positive `κ` the lift is not claimed to be an exact zero-entropy equilibrium system. The primary preprint retrieved is v1, not an inspection of the final article's complete text.

## 4. The finite-window path KL is not automatically physical additive entropy

**Degünther, van der Meer and Seifert (2024), _Fluctuating entropy production on the coarse-grained level: Inference and localization of irreversibility_, Physical Review Research 6, 023175.** [DOI](https://doi.org/10.1103/PhysRevResearch.6.023175); [primary preprint](https://arxiv.org/pdf/2309.07665).

Section IV A, equations (28)–(31), derives the system boundary as `log[P(I)/P(J)]` for an underdamped example. Replacing its denominator by `P(Theta J)` incorrectly assigns a system entropy change to a closed phase-space cycle and breaks additivity. Thus the stationary reversal-KL boundary offset has a directly documented physical interpretation limit. Their Markovian-event/snippet framework also makes clear why an actually regenerative observed interface supplies more information than a coarse label.

Root's asymptotic rate and finite-window KL are compatible with this distinction when `B` is displayed separately. Calling `B` preparation distinguishability is appropriate. Calling it dissipated heat or a universally defined preparation work is not justified by the algebra.

## 5. A physical parity assignment cannot be inferred merely by choosing a convenient lift

**Shankar and Marchetti (2018), _Hidden entropy production and work fluctuations in an ideal active gas_, Physical Review E 98, 020604.** [DOI](https://doi.org/10.1103/PhysRevE.98.020604); [primary preprint](https://arxiv.org/pdf/1804.03099).

The introduction and Table I compare even and odd reversal conventions for self-propulsion and show a hidden underdamped entropy contribution missed by removing inertia too early. The physical meaning of propulsion determines the appropriate reversal; a formally vanishing coarse or conjugated rate does not certify vanishing physical dissipation.

This is a limitation on interpreting the candidate theorem as a universal low-heat realization, not a collision with its mathematical finite-state closure statement. The supplied CTMC, involution and readout do not by themselves specify reservoirs, an energy function, permitted odd fields, or local detailed balance. A native system can exclude these lifts through those additional facts.

## 6. A current strong inference theorem has a different hypothesis class

**Schwarz, Kolomeisky and Godec, _Consistent time reversal and reliable and accurate inference in the presence of memory_.** [Primary manuscript](https://arxiv.org/pdf/2410.11819); [PRL accepted record, accepted 25 September 2026](https://journals.aps.org/prl/accepted/10.1103/gwf7-6kvr).

The inspected manuscript derives higher-order coarse entropy estimators. Supplementary Theorem 1 assumes a finite stationary irreducible CTMC and a specified finite semi-Markov order for the observed process. Assumption 1 uses ordinary bidirectional microscopic support; equation (S11) reverses time without a hidden state involution. Its order-saturation reasoning and fixed-process long-time limits are substantive, but do not certify a uniform mixing rate or a bound on hidden parity preparation over root's class.

Consequently this paper is a strong conventional comparator once its reversal and memory assumptions are supplied. A low-order estimate from an approximately low-order visible record cannot establish those hypotheses uniformly against an arbitrarily slow hidden orientation. Root does not refute the paper's theorem.

## 7. Precise proposed contribution

The result should keep the following conjunction explicit:

1. **Universal supplied source:** arbitrary finite irreducible `Q`, stationary law and finite readout, not only a directional cycle.
2. **Complete finite-window observation:** total variation of full continuous-time readout paths, not a fitted finite collection of moments or correlations.
3. **Finite irreducible alternatives:** each positive-parameter model is irreducible and uses `4n` states. The singular zero-switch limit is not used as an exact irreducible realization.
4. **Fixed common microscopic clock:** invisible state changes make every escape rate the same fixed `Λ`. This is stronger than bounding the maximum jump rate, but does not bound mixing time or transition-rate precision.
5. **Accounted obstruction:** the construction displays `B`, the small sustained rate, the path-TV estimate and the orientation relaxation eigenvalue. It therefore identifies the additional information whose absence defeats a uniform lower bound.

This is a potential theorem-level addition to existing ingredients. The absence of a direct collision in the bounded search does not establish novelty, and the easy ring specialization should be acknowledged openly.

## 8. Two interpretive corrections worth preserving

### 8.1 The preparation divergence is not memory capacity

This is a direct calculation for root's family, not a claim from the cited papers. Put `α=1−ε`. The orientation has two values, while

`B = D((α,ε) || (ε,α)) = (α−ε) log(α/ε)`

can diverge. In contrast, its KL to the symmetric sign reference is

`D((α,ε) || (1/2,1/2)) = α log(2α)+ε log(2ε) ≤ log 2`.

The word “unbounded” refers to distinguishability from the reversed preparation. It does not refer to an unbounded number of stored bits. Even identifying the second KL with a preparation free energy would require an appropriate equilibrium reference and an energy/temperature contract; the construction supplies neither.

### 8.2 Bounded clocks are not bounded acquisition or preparation time

Root explicitly exposes eigenvalue `−κ`. A common row escape rate limits how quickly individual microscopic events occur, while arbitrarily weak switching leaves orientation relaxation unbounded. Independent stationary preparations are also an observation assumption, not a free operation guaranteed by the existence proof. No positive finite-sample entropy certificate can invoke this theorem and simultaneously discard the preparation or mixing qualifications.

## 9. Suggested scope sentence

“Using established adjoint lifts and the known odd-parity boundary correction, we construct fixed-size hidden-parity alternatives with a fixed common escape clock whose finite-horizon observed paths approximate any supplied finite CTMC, while their sustained reversal-divergence rates approach zero. The nonidentifiability is uniform over preparations with unbounded parity distinguishability and arbitrarily slow hidden orientation relaxation; it is not a universal physical low-dissipation implementation.”

No broader archive was loaded. No direct external network or third-party contact was used. Source identities, inspected passages and retrieval references are preserved in `ORIENTATION_SOURCE_RECEIPT.json`.
