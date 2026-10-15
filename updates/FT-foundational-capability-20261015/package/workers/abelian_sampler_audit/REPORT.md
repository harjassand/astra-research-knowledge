# Independent audit of N610 finite-abelian subgroup absorption

**Audit status:** conditional mathematical mechanism supported by an independent reconstruction and exact finite checks. No counterexample found under the strict triangular, shared-category, delayed-Haar-value interface. Finite-abelian novelty, asymptotic separation from the strongest matched sampler, and practical superiority remain **UNKNOWN**. The prime-power ring class is already encodable by field digit layers; a generic new sampling capability is not established.

## Source and independence receipt

Capital checkout revision: `25fc24509a59aabee340b36b588c9e59a144253d`. Read its `AGENTS.md`, `00_START_HERE.txt`, current N610 dossier, and original note lines 11–161. Original note: `work/astra-capital-scientific-power-20261015/updates/CP/package/stratified_noise_absorption_research_package_2026-10-10/stratified_noise_absorption_research_2026-10-10.md`, SHA-256 `72e51b3a71b5ed01f54a0c602f027f86889ef9495fcfbde51119214588b9bc0b`.

`INDEPENDENT_DERIVATION.md` was saved before reading the new ring implementation. `exact_audit.py` imports no producer/worker sampler and uses separate forward and backward code. It uses rational probabilities throughout. Worker code was subsequently read for interface and implementation review; it was not treated as proof. No source or other worker files were changed by this auditor.

## Exact contract that survives

The supplied state group G must have an explicit finite presentation supporting its endomorphisms, subgroup membership, and uniform draws. Each site-time category is independent across site-times, shared across original layers, and has Haar probability s>0. Conditional on a Haar category, the G-valued coordinates at different original layers are independent uniform draws. Same-layer gates are sums of supplied endomorphisms applied to parent values. Forcing is a supplied computable function of strictly lower original layers. A finite batch of raw G-valued coordinates at arbitrary times is sampled jointly.

The method is exact sampling of that finite joint law. Distributional masking alone does not supply a pathwise stationary realization consistent across separate, incrementally enlarged query batches. Separate invocations ordinarily produce new independent samples. Any claim of an online extension service or a globally consistent finitary coding needs another construction.

## Independent proof reconstruction

For a layer with a requested outputs, use H=G^a. Every outstanding variable X_z has coefficient homomorphism T_z:G→H. Coincident variable occurrences must be aggregated by addition of homomorphisms before processing; descending time ensures no later propagation can revisit a processed site-time. A gate gives T_z∘A on a parent and the saved forcing term T_z(F_z). There is no division by A, and no nonunit inverse is allowed.

Each retained Haar event contributes an independent uniform element of im(T_z). Their sum is uniform on their generated subgroup V. This follows because the product of those image groups maps surjectively onto V with equal-size fibers. If im(T_z)⊆V, discard that pending ancestor.

The delicate step is independence, not just subgroup membership. Conditional on all categories and lower-layer histories, an upper Haar coordinate is independent of the entire lower process because lower gates never use upper values. A discarded same-layer variable is older than the retained Haar events, so it does not depend on them. Exploration addresses and masks are chosen from categories and deterministic coefficients alone; no Haar values or forcing values influence that selection. Thus the uniform mask is independent of the discarded contribution and retained lower variables. Integrating it out preserves their joint law.

For the most careful stationary-law argument, use finite-horizon dynamics from any deterministic initial configuration. On category histories for which all layer certificates close before the horizon, the conditional output law is independent of that initial configuration. The certificate closes almost surely with the bounds below. Hence the finite-horizon laws converge uniformly on every fixed batch to a unique consistent stationary family. This avoids assuming an already constructed bi-infinite process as a proof premise.

Already memoized categories at lower layers cause no independence problem: the upper exploration is a finite stopping exploration of an i.i.d. category field. Conditional on its full transcript, every unqueried address still has the original category law. An old event is processed at most once per layer. The necessary common oracle is not replaceable by independent layer oracles.

## Termination, tail and bit costs

Let L=Ω(|G|), counting prime factors with multiplicity. Every unmasked Haar query strictly grows V, and a subgroup chain in G^a has length at most aL. The number of **fresh** category queries at that layer is therefore dominated by NB(aL,s), even with finitely many categories cached by higher layers. The algorithm needs no factorization of |G|; a log2|G| bounds aL.

With h=kc² and m original raw coordinates, the original prerequisite accounting yields

    E Q ≤ (Lm/s) Σ_{j=0}^{c-1} (1+Lh/s)^j.

For G=Z/p^aZ, L=a. For fixed original depth c, this is polynomial in a,m,k,1/s. The same negative-binomial moment-generating-function recursion as N610 gives an exponential tail for fixed parameters: replace mψ_s(θ) with Lmψ_s(θ), and the recursion θ+hψ_s(θ) with θ+Lhψ_s(θ). Constants may be poor.

These are expected query and tail bounds, not a finite worst-case runtime guarantee. Geometric waiting and rejection-based exact integer sampling can take arbitrarily long. A deterministic time cap requires a disclosed failure/UNKNOWN outcome or introduces approximation.

Polynomial expected **bit** cost is available for a cyclic ring using exact integer lattice normal forms, without factoring M. Represent V by a full-rank lifted lattice containing MZ^a; membership of a coefficient vector is exact lattice membership. All stored ring coefficients have O(log M) bits. Group dimensions, gate circuits and address lengths must be charged. The theoretical existence of polynomial normal-form algorithms is classical: Kannan–Bachem bound both operation counts and intermediate binary lengths. This does not certify a particular computer-algebra implementation's asymptotic behavior. [Kannan–Bachem, 1979](https://epubs.siam.org/doi/10.1137/0208040)

A generic finite-group black box is insufficient for this bit-cost statement. For a general finite abelian group, supply cyclic decomposition/presentation and explicit compatible endomorphism matrices, or separately charge their acquisition. Gate-description sizes and evaluation costs need uniform bounds or an output-sensitive charge for the actually acquired descriptions. Local event counts do not bound arbitrarily expensive supplied forcing oracles.

## Exact finite evidence

Independent test model: N=1, G=Z/4Z, c=2, s=r=1/3, residual (1,2), gate

    x0' = 2x0+1 mod4,
    x1' = 2x1+x0²+1 mod4.

The coefficient 2 is a nonunit, its image has order 2, and two successive same-layer coefficients vanish. The full dynamics loses initial-state dependence within four updates, so finite forward enumeration determines its stationary law exactly.

* All 81 four-update category strings × all 16 initial states: **1,296 exact conditional distribution comparisons, zero mismatches** against an independent backward subgroup resolver.
* Joint output (X0^(0),X0^(1),X-1^(1)): all 243 five-update category strings × all 16 initial states: **3,888 exact conditional comparisons, zero mismatches**. These include shared same-layer ancestors across target times.
* The rational law obtained by category averaging satisfies πP=π **exactly**.
* Nonunit propagation test: coefficient vector (1,2), followed by multiplication by 2, gives vector (2,0) and image {(0,0),(2,0)} exactly.

These are exhaustive checks of this finite model, not a universal proof. The tiny audit enumerates subgroups deliberately; its implementation is not a scalable subgroup algorithm.

Explicit countermodels protect the proof's assumptions. If U is uniform on Z/4 and the discarded term is Z=U, then U+Z is supported only on {0,2}; independence is indispensable. For a one-site mixture with probability 1/2 Haar and probability 1/2 fixed-zero gate, two shared-category layer coordinates satisfy P(both zero)=17/32. Independent layer categories give 25/64. Duplicated parent occurrences also need aggregation: X+3X=0 mod4 exactly, while treating the two occurrences as independent produces a uniform value.

## Strongest matched comparator found

For M=p^a, write x=Σ_{d=0}^{a-1}p^d x_d. At digit d, Σ A_j x_j has same-digit affine coefficient A_j mod p. Everything else is a carry determined by lower digits. At original level ℓ, its forcing is determined by all digits of lower original levels. Ordering field layers as (ℓ,d) therefore produces a valid N610 model of depth ac with the *same site-time category field*. Haar ring values have independent uniform digits. A requested raw ring coordinate corresponds to a jointly requested a-digit batch. This is an exact input/output reduction, not an approximation.

The direct subgroup query bound keeps recursion depth c and multiplies the rank allowance by a. Applying the original conservative N610 bound mechanically to digit depth ac produces much worse dependence on a. This establishes an improved stated upper bound relative to that mechanical bound. It does not prove that the actual digit sampler requires that upper bound, an asymptotic lower bound for the digit sampler, or any universal execution-time advantage. Carry sparsity, constant forcing, algebraic simplification, quotient-specific prerequisites and faster field arithmetic can make the digit implementation competitive or faster.

For composite M, CRT does not justify independent component runs when arbitrary lower-level forcing couples prime components. Such a comparator must retain a shared category field and joint cross-component forcing prerequisites. The clean class-inclusion conclusion above is for prime powers. Arbitrary finite-abelian reduction needs a separate representation argument.

Global all-sites-Haar CFTP is a correct but weak baseline. Waiting for all sites to reset pays the artificial s^-N event. Exhaustive state-map CFTP also pays exponential state enumeration that the requested local task does not intrinsically require. A causal cone can fail to terminate on an infinite supercritical dependency graph, but specialized algebraic perfect samplers can erase influence without exploring that full cone. None of these baseline failures proves superiority over the digit-expanded original N610 sampler.

## Primary prior-art map and novelty limits

* Propp–Wilson establishes CFTP exactness from a sufficiently distant past and pathwise coalescence. It is foundational prior art, not a matched runtime bound for this algebraic local-output operation. [1996 paper](https://www.stat.berkeley.edu/~aldous/206-RWG/RWGpapers/propp_wilson.pdf)
* Bušić–Mairesse–Marcovici develops perfect PCA sampling without monotonicity through an envelope/bounding PCA. Local perfect sampling and shared space-time randomness predate this work. Applicability and cost depend on termination of the bounding process. [STACS 2011](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2011.296)
* Marcovici–Sablik–Taati, Section 3.1/Proposition 3.3, gives finite-window perfect sampling under a pathwise coalescence criterion. Section 5.1/Theorem 5.1 proves uniform ergodicity for XOR with positive zero-range noise by Fourier analysis; its Fourier proof traces characters under the additive dual map. Their Section 4 surjective/additive-noise theorem has a shift-invariant initial-measure qualification. These establish substantial algebraic/noisy-CA precedent but were not found to state the present arbitrary-network triangular subgroup query bound. [2019 paper](https://arxiv.org/html/1712.05500)
* Lubetzky–Sly studies information-flow clusters in space-time to obtain Ising mixing/cutoff results. This is conceptual prior art for following only the information relevant to outputs; the theorem's target and temperature hypotheses differ. [Information percolation, 2016](https://arxiv.org/abs/1401.6065)
* Galves–Garcia–Loecherbach gives perfect simulation/finitary coding for multicolor infinite-range particle systems under continuity and decay assumptions. Exact local finite windows and coding from independent randomness are established concepts; these assumptions do not automatically cover arbitrary low-noise triangular networks. [2008 preprint](https://arxiv.org/abs/0809.3494)
* Anand–Jerrum gives perfect finite-window sampling for potentially infinite Gibbs spin systems under strong spatial mixing and subexponential graph growth. It cannot simply be applied to an arbitrary supplied stationary PCA law without a Gibbs representation and those premises. [2022 paper/preprint](https://arxiv.org/abs/2106.15992)
* Moore's deterministic nonlinear-CA decomposition into linear components shows that algebraic layering itself is established. It addresses prediction rather than this stationary sampling interface. [1998 paper](https://doi.org/10.1016/S0167-2789(97)80003-6)

This targeted primary-source review does not establish priority. In particular, duality, additive group filters, strong stationary times, and exact algebraic random-map reductions may contain a closer predecessor. **True novelty UNKNOWN.**

## Implementation review at the inspected snapshot

The worker's `n610_ring_sampler.py` uses exact Hermite normal form, not invalid division by nonunits. Its lifted-lattice membership and uniform sampling formulas are mathematically sound. It aggregates coincident dependencies, processes descending time, delays Haar values, and shares one category oracle across recursive layers.

At the first inspected snapshot, `sample_coordinates` called `model.check()` on every sample; that method scanned every i in range(n), and the model used full N-sized arrays. Hence its total executable work/acquisition was Ω(N) even when its fresh-event counter was independent of N. **This issue was corrected by the worker and independently rechecked.** The final inspected sampler SHA-256 is `6c164a5b0f75236d04735b26df828ff4fb20d1311f55d0d459d7a6fb5a390286`: `check()` reads metadata only, and parent/coefficient/residual callables are validated when acquired. A second discovered issue—re-querying a parent descriptor inside coefficient validation while counting it once—was also fixed by passing the already acquired parent count.

The auditor's instrumented N=1,000,000 execution uses only local callables and no N-sized arrays. Two requested outputs exposed 4 categories, made exactly 2 parent descriptor calls, 2 coefficient descriptor calls and 2 forcing calls, agreeing with the reported incidence/forcing counters in this k=1 example. This execution exercises both gates and residuals. It verifies the on-access correction at the pinned source, not a scaling theorem from one run. See `on_access_results.json` and `hnf_audit.py`.

The same independent adapter audit checked 160 successive subgroup extensions over moduli 4,6,8,12 (dimensions 2, plus dimension 3 over modulus 4). All **10,368 exhaustive membership comparisons** agreed with independently enumerated additive closure; uniform pushforwards through the HNF basis had equal fiber counts in every case. These are exact tiny adapter tests, not a general sampler or complexity proof.

The digit comparator's mathematical carry formula is correct for prime powers. Its initial factor search by trial division is not polynomial in log M for arbitrary primes; a supplied p,a presentation or a separately charged factorization step is required for a fair bit-cost comparison. The latest inspected comparator also uses local callable caches for parent/coefficient/residual descriptors, correcting its earlier full-site conversion.

The worker reports the matched tiny N=2,c=2,Z/4 case over 800 draws: subgroup HNF averaged 5.73 categories, 12.63 parent incidences and 4.21 forcing calls; the original N610 digit sampler averaged 6.89 categories, 28.73 parent incidences, 3.20 original forcing evaluations and 9.58 carry callbacks. Reported total times were **0.717 seconds subgroup versus 0.095 seconds digit** (causal cone 0.015 seconds). These timings are worker-reported and were not independently rerun by this auditor. They establish no practical speedup; fewer fresh categories did not offset HNF overhead in that test. The final benchmark receipt and source pin must be retained by the producing worker.

## Decision

Proceed as conditional mathematical research capital and a candidate fixed-original-depth query-bound improvement. Do not promote it as a novel generic sampling operation, a full finite-abelian executable, a worst-case polynomial-time result, or an end-to-end practical speedup. Before stronger promotion, pin the final code, audit the final theorem text, benchmark against the digit sampler on the same targets/forcing/model access, and disclose time, memory, subgroup dimensions, circuit acquisition/evaluation, random-bit and validation costs. A win on fresh categories alone is narrower than a win on total work.
