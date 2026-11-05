# Selection opening: make three-dimensional passive quantum storage operationally writable

Status: an independently selected question, proved compiler statements, an exact finite example, and a source-based instantiation argument requiring independent audit. The full operational theorem and strongest-method comparison have not yet passed that audit; this note does **not** claim a finalized physical memory result.

## The question and its consequence

For the proved random-embedding family of three-dimensional self-correcting stabilizer Hamiltonians in Balasubramanian–Davydova–Lin (BDL), can one load an arbitrary, possibly reference-entangled logical qubit from product ancillary states, store it passively for the stated stretched-exponential lifetime, and read it out, with polynomial classical computation and polynomial write/read quantum operations at fixed sufficiently low nonzero temperature?

The loading error is an independently specified delta, not an assumed pre-existing equilibrium resource. Active loading is permitted. Requiring passive initialization would unnecessarily restrict the question. A proof that an efficiently prepared cold code state already has the full lifetime would also resolve it; the opening below instead targets thermal loading directly.

The full result would turn a finite-temperature memory theorem into an executable write–wait–read operation: polynomial resources prepare and retrieve one unknown qubit; during a storage interval of order exp(c N^eta), no active correction is applied. The scientific consequence is computational accessibility of the protected three-dimensional thermal sector. This is not a claim of a practical material, a fault-tolerance threshold for loading hardware, robustness to arbitrary noncommuting perturbations, or a universal passive computer.

BDL's proved lifetime applies to a decoder-defined thermal encoding. Its stated initialization gap concerns efficient passive initialization, so it does not establish that every active construction is unknown. Use the proved Section 3 random-embedding family, not the more economical explicit Section 6 construction whose full lifetime analysis is deferred. Primary source: [BDL, arXiv:2605.10943v1](https://arxiv.org/html/2605.10943v1), Sections 1.2.4, 1.3, 2.5, 4, and 5.

## Exact loading compiler

Let a commuting stabilizer Hamiltonian encoding one logical qubit be

\[
H=\sum_{a=1}^{m}J_a(I-S_a)/2,\qquad J_a>0.
\]

Here J_a is the actual energy cost of a violated term. A convention H=-sum_a K_a S_a instead has J_a=2K_a after removing a scalar offset; inverse-temperature constants must be converted accordingly.

Let \(\mathcal S\subseteq\mathbb F_2^m\) be its valid syndrome space. All syndrome sectors have the same dimension. Fix a ground-code isometry \(V\) and the Pauli correction \(O(s)\) used by the lifetime theorem's decoder. This correction, rather than an unrelated syndrome solution, determines the dressed logical degree of freedom. Define

\[
\pi(s)=Z^{-1}e^{-\beta\sum_aJ_as_a},\qquad
\mathcal E_p(\rho)=\sum_{s\in\mathcal S}p(s)O(s)V\rho V^\dagger O(s)^\dagger.
\]

**Exact identity:** for any two distributions on valid syndromes,

\[
\boxed{\frac12\|\mathcal E_p-\mathcal E_q\|_\diamond=\|p-q\|_{\rm TV}.}
\]

Proof: with any reference, different syndromes occupy orthogonal blocks. Every normalized isometric block has trace norm one, so the output difference has trace norm \(\sum_s|p(s)-q(s)|\). This proves the upper bound and equality on every input state. Classical total variation controls arbitrary-reference quantum loading exactly, without a size factor.

Before the input arrives, sample s and compute O(s). On arrival, apply a Clifford encoder V to the input plus initialized ancillas, then apply the product Pauli O(s). Readout measures the syndrome, corrects it with the same decoder, and inverts V. For CSS codes, X and Z syndrome laws factor because the consistency spaces separate and all joint eigenspaces have equal dimension.

Conversely, efficient preparation of the **full Gibbs state** suffices: measure stabilizers to obtain its syndrome, then use this sample to load fresh input. Logical randomization of the full Gibbs state is therefore no reason to exclude it as a comparator. This reduction does not solve generic weighted linear-code sampling; it isolates that classical distribution as the hard operation.

## Completed abstract compiler: decoder histories to a polymer gas

Retain the whole deterministic multiscale decoder history. Eliminating its intermediate variables can create long consistency checks; retaining them can restore bounded local constraint degree. This helps only if the history is energetically charged by physical defects. Locality alone is insufficient.

### Explicit hypotheses

Supply a graph G with M=poly(N) vertices, maximum degree Delta=O(1), and constant alphabet A containing zero. Local constraint scopes are cliques of G, a bounded number meet each vertex, and the zero assignment is accepted. Fixed-radius scopes can be made cliques by taking a fixed graph power. Also require:

1. Projection from accepted histories to physical syndrome variables is a **bijection** onto a good subset of valid syndromes. Hidden history multiplicity must not reweight the physical law.
2. Energy is nonnegative, vanishes at zero, and adds across nonzero history components. Physical unary syndrome energy suffices. Every accepted isolated component h satisfies \(E(h)\ge a|\operatorname{supp}h|\), with a>0 independent of N.
3. Acceptance and energy of a connected labelled support extended by zero are computable in polynomial time. Polynomial dependence on N suffices for the conservative finite-list algorithm; support-polynomial work permits sharper existing runtimes.

### Exact component lemma

In any accepted history, extend one connected nonzero component by zero. A constraint clique cannot contain nonzero vertices from two different components; it therefore sees either its original accepted local view or the all-zero view. Thus each zero-extended component is accepted. Conversely, pairwise distance-at-least-two accepted components recombine by the same argument. Energies add, and the bijection prevents overcounting.

Consequently the good physical partition function is exactly the hard-core polymer gas

\[
Z_{\rm good}=\sum_{\Gamma\ {\rm compatible}}\prod_{\gamma\in\Gamma}w_\gamma,
\qquad w_\gamma=e^{-\beta E(\gamma)}\le e^{-\beta a|\gamma|}.
\]

A polymer is an accepted connected labelled nonzero component. This is stronger than a bound on rare bad events: it represents the whole desired conditional law.

### Fully paid polynomial sampler

Bound labelled connected supports of size r containing a fixed vertex by kappa^r, with, for example, \(\kappa=(|A|-1)\max(2,\Delta)^2\). Put \(x=\kappa e^{-\beta a}\). Choose a fixed sufficiently low temperature satisfying \(x\le1/[8(\Delta+1)]\). For any polymer gamma_0,

\[
\sum_{\gamma\not\sim\gamma_0}|\gamma|w_\gamma
\le(\Delta+1)|\gamma_0|\sum_{r\ge1}r x^r
\le|\gamma_0|/4.
\]

Truncate at size L with \(M x^{L+1}/(1-x)\le\delta/2\), so L=O(log(M/delta)). A fixed polymer has inclusion probability at most its activity: deleting it embeds the remaining compatible configurations into all configurations. The Gibbs mass of configurations with a larger polymer is at most delta/2.

Enumerate all labelled connected supports through size L, validate their zero extensions, and evaluate activities. There are at most \(K\le M\sum_{r=1}^L\kappa^r=\operatorname{poly}(M,1/\delta)\) listed polymers. No rare-event rejection or implicit oracle is hidden.

Choose a listed polymer uniformly at each step. If any other listed polymer incompatible with it is present, set its occupancy to zero. Otherwise replace its occupancy with a Bernoulli variable of parameter \(w_\gamma/(1+w_\gamma)\). This is heat-bath dynamics on the finite incompatibility graph. Couple two states differing in one polymer gamma_0 using the same coordinate and uniform random number. Updating gamma_0 removes their disagreement. A neighboring update creates a disagreement of size |gamma| with probability at most w_gamma. The displayed bound contracts the weighted Hamming metric, which sums sizes of differing polymers, by at least \((3/4)|\gamma_0|/K\) per step. Path coupling gives \(O(K\log(M/\delta))\) mixing steps. Every step and activity is polynomially computable. For K=0 the output is deterministically the empty history.

This conservative construction exposes all costs. Sharper existing algorithms are in Chen, Galanis, Goldberg, Perkins, Stewart, and Vigoda, [Fast algorithms at low temperatures via Markov chains, arXiv:1901.06653v6](https://arxiv.org/pdf/1901.06653), Theorems 2 and 5; also Helmuth–Perkins–Regts, [Algorithmic Pirogov–Sinai theory, arXiv:1806.11548](https://arxiv.org/abs/1806.11548). The sampler is existing machinery. The proposed new physical use is the history representation meeting its premises.

Project to the physical syndrome. If the target Gibbs distribution assigns mass b_N outside the good set, total variation and hence half-diamond loading error are at most delta+b_N. Activity and transition errors need only inverse-polynomial precision relative to the polynomial number of steps and listed objects.

## Instantiation route and the exact remaining lemma

The relevant decoder records coarse syndromes and local corrections satisfying relations of the form

\[
\sigma_i=\delta_i f_i+\mathcal F_{i-1}(\sigma_{i-1}).
\]

Retain syndrome bits only, computing the local correction blocks as functions of their bounded syndrome neighborhoods rather than independently sampled variables. Enforce both the local deterministic decoder tables and the cochain relations. This avoids charging a separate correction register in the history support bound. The source's alternate nonincrease and factor-two syndrome contraction would then give

\[
\sum_i|\sigma_i|\le4|\sigma_{\rm top}|,
\qquad E(h)\ge(J_{\min}/4)|\operatorname{supp}h|.
\]

This estimate assumes that support counts individual syndrome bits and that all accepted histories really are canonical valid decoder traces. Using block alphabets and explicit corrections also works conditionally, but incurs a constant support overhead C and gives a=J_min/(4C).

Fix the base coarse syndrome to zero. The cochain recurrences can then certify top-syndrome validity inductively, without separately imposing long eliminated metachecks. The intended omitted mass is the exponentially small Gibbs probability of nonzero base syndrome. The source's coarse-defect counting gives the relevant kind of control, but one must match the chosen base condition and constants exactly.

**Instantiation checklist:** a polynomially generated bounded-degree, constant-alphabet local factor system for the actual canonical decoder of the proved random-embedding BDL family must verify all of the following. The canonical-table construction immediately below discharges its logical requirements conditionally on explicitly identified source premises.

- Each valid fine syndrome reaching zero base has exactly one accepted trace.
- Every accepted trace has a valid top syndrome and equals its canonical decoder trace. Necessary local relations alone are insufficient.
- Zero extensions are legitimate despite overlapping solvers, cohomology choices, consistency conditions, and tie breaking.
- Energy is coercive for every isolated accepted component, not merely the component containing a coarse defect in a rare-event witness proof.
- Graphs, factor tables, energies, projection, and physical corrections are polynomially computable with size-independent constants.

### Canonical local-table construction: a complete conditional proof

Suppose the supplied maps on valid syndromes are deterministic, polynomially computable, and have bounded neighborhood dependence; suppose the cochain matrices and residual equations have uniformly bounded incidence. For each local input pattern, test whether it extends to a valid syndrome by GF2 linear algebra. On extendable patterns choose a canonical global extension and evaluate the decoder; local computability makes the local output independent of that extension. On nonextendable inputs choose any fixed default. This produces total local tables for both g_i(s_i)=s_(i-1) and f_i(s_i), at polynomial total cost because neighborhoods have fixed size.

Impose the deterministic coarse-output tables and every coordinate of

\[
s_i=\delta_i f_i(s_i)+F_{i-1}s_{i-1}.
\]

Now impose the **entire valid-syndrome constraint of the constant-size base code**, rather than fixing its syndrome to zero. Induct upward: a valid coarse syndrome is a coboundary; the residual equation and cochain property force the fine syndrome to be a coboundary. Thus every accepted level is globally valid, its local inputs are extendable, and its table outputs equal the supplied decoder. Determinism proves that accepted histories biject onto **all** valid fine syndromes. Conversely every valid fine syndrome and its decoder history satisfy the tables, residuals, and base constraint. The zero assignment is accepted, and the abstract component lemma applies.

The base constraint is a fixed-arity factor because BDL's modified level-2 code has size O(ell^4), independent of N (Section 5.1.1, equation 206). Making its whole scope a clique raises the host degree by a fixed constant. There is no growing global validity oracle. All accepted zero-extended components satisfy the same upward validity induction and inherit alternating syndrome contraction. Therefore the syndrome-only energy constant a=J_min/4 applies.

**Consequence:** once bounded residual incidence and the supplied local decoder premises are audited, the compiler samples the **full** syndrome Gibbs law to arbitrary delta at fixed N in poly(N,1/delta) time. The earlier zero-base conditional version is optional and weaker; its b_N approximation floor is unnecessary. This observation reduces the remaining work to checking source premises and the complete operation/comparator audit, rather than inventing an additional global closure conjecture.

### Precise source audit for those premises

BDL Definition 4.3 and equations 124–126 give neighborhood dependence of local correction blocks (directed radius one) and coarse syndrome outputs (radius two). Remark 4.4 bounds the further propagation under the coboundary by one graph step. Section 5.2 states that the decoding graph has maximum degree O(ell^2); local replacement complexes have fixed size for the fixed ell family. Theorems 4.6 and 4.7 provide the residual cochain identity and alternate nonincrease/halving. Lemma 5.6 applies contraction to every component of the source history graph, not merely the root witness. The compiler itself can use the factor primal graph, because validity plus the global contraction theorem already gives its component coercivity.

The source's existence of a cochain map alone would not establish sparse residual constraints. Here is the additional deduction. In Section 3.2.4 the coarse degree-2 basis enters local H^2(C_Z) through the diagonal inclusion (equation 85). For the R_Z step, Section 4.2 represents each coarse syndrome in its own local C_z. Choose the initial homological contractions separately in each local complex, by fixed GF2 bases. The perturbation g only connects X to Q to Z (Section 2.3.2, equation 38). It vanishes on the terminal Z sector. The corrected inclusion from Appendix A is i'=i+h Sigma i (equation 247). For coarse degree-2 input, Sigma i=0, so the syndrome component F^2 equals its local representative inclusion i. Its columns lie within one fixed-size C_z and its rows meet at most the fixed number of coarse coordinates assigned there. Thus F^2 has uniformly bounded row and column incidence. R_X duplicates a coarse syndrome within the two local H^2 representatives; R_Z uses one local representative. This sparsity inference should be independently checked against the chosen chain-map conventions, but it is a concrete deduction, not a missing theorem one should silently assume.

For uniform decoder construction, fix every local solution by lexicographic tie breaking among the finite candidates meeting the source's required local weight inequalities. The local problems in Sections 4.2–4.3 have constant size; exhaustive local search is a large constant, and zero input can choose zero output. Alternatively use the canonical-extension tables above. The modified base decoder in Section 5.1.1 is also finite and explicitly permits a lookup table. These choices preserve the cited locality and contraction conditions. Provided this source-premise audit is accepted, the local representation follows from the displayed conditional proof; no separate history-closure obstruction remains.

## Exact model and failure diagnostic

The executable model uses a four-child tree, where a parent s and children a,b,c,d obey

\[
a\oplus b=c\oplus d=s.
\]

The root is zero and only occupied leaves cost energy. Each accepted leaf assignment has a unique history. Eliminating intermediate bits leaves growing-support checks, whereas the retained primal graph has maximum degree eight. Every nonzero parent forces at least two nonzero children, so history support is at most twice the number of physical defects. The compiler applies with a=1/2 for unit energy.

Ordinary tree dynamic programming gives

\[
Z_{k+1}(0)=[Z_k(0)^2+Z_k(1)^2]^2,
\quad Z_{k+1}(1)=4Z_k(0)^2Z_k(1)^2.
\]

With \(r_k=Z_k(1)/Z_k(0)\) and \(r_0=e^{-\beta}<1/4\),

\[
r_{k+1}=\frac{4r_k^2}{(1+r_k^2)^2},
\qquad r_k\le\frac{(4r_0)^{2^k}}4.
\]

For N=4^k this is coarse-defect suppression exp[-Omega(sqrt(N))] accompanied by an exact recursive sampler. Existing elementary dynamic programming solves this toy. Its role is to show that long eliminated checks can conceal an easy representation, not to claim a new quantum memory or sampler.

The executed depth-two verification used rational arithmetic on all 65,536 leaf strings: 1,024 valid root-zero histories, 300 distinct polymer components, and 246 compatible component-pair recombinations. Component deletion, recombination, history uniqueness, energy factorization, and recursive probability equality with the target Gibbs law all passed. See `history_polymer_example.py` and `history_polymer_example.json` in this directory. No BDL code or physical experiment was implemented.

A binary XOR tree shows why uniqueness and closure alone are inadequate. Put one occupied leaf in each root branch and all others zero. The root is zero and energy is two, but the nonzero history contains two long paths. Turning each constraint scope into a clique connects them through the sibling edge below the zero root, so one valid component has size proportional to depth at constant energy. Uniform energy per history site fails. The contraction hypothesis is essential.

## Strongest existing methods and remaining novelty checks

The direct sector-preparation comparator is Bergamaschi–Gheissari–Liu, [Rapid mixing for Gibbs states within a logical sector, arXiv:2507.10976](https://arxiv.org/abs/2507.10976). Its usable hypotheses include controlled local redundancy/metachecks; BDL states those assumptions do not directly cover its construction. This does not exclude another representation or another sampler.

Newer methods that must also be checked are:

- Hwang–Jiang, [Gibbs state preparation for commuting Hamiltonian: Mapping to classical Gibbs sampling, arXiv:2410.04909](https://arxiv.org/abs/2410.04909). Test its actual locality, dimension, and correctability hypotheses; the word “commuting” does not denote a universal efficient method.
- Hangleiter–Ju–Vazirani, [Code Swendsen–Wang Dynamics, arXiv:2510.08446](https://arxiv.org/abs/2510.08446). The parent team is testing whether BDL's physical syndrome code admits the method's efficiently samplable graphic/co-graphic representation with logarithmic allowed defect. Non-LDPC metachecks and Tanner/sheaf descriptions do **not** rule this out. An exact nonregular matroid minor alone would not exclude a logarithmic-defect representation either. If applicable, this method should replace the polymer construction immediately and supply the classical distribution used by the exact loading compiler.
- Piveteau–Quek–Franco Garrido, [Gibbs state preparation through quantum decoding, arXiv:2610.03566](https://arxiv.org/abs/2610.03566), and Shang–Wang–Stilck França, [Quantum Gibbs State Preparation via Relative Decoding, arXiv:2610.06667](https://arxiv.org/abs/2610.06667). Primary abstracts were verified; full texts were inaccessible in this session. The former advertises decoder-dependent temperature thresholds for uniformly random Hamiltonian signs. The latter requires a prepared source and efficient quotient-code decoding; linear relative distance/radius certifies a constant inverse-temperature window. These abstracts do not establish the all-positive low-temperature BDL corollary, but they cannot rigorously exclude it. Full applicability remains a necessary check.

The selected question must change if an existing theorem already supplies its complete loading operation. Perturbation-stable loading and storage would then be a stronger possible question, but needs its own constructive opening and is not silently claimed here. No theorem-level priority assertion follows from an abstract-level literature check.

## Resource and uncertainty bill

Let \(b_N\le e^{-cN^\eta}\) bound unstable-syndrome mass after choosing the relevant constants. The source's logical-state trace stability bound has the form \(8\|\mathcal L\|_1t b_N\). Because the input is one qubit, polarization gives an arbitrary-reference extension with a constant factor: a conservative half-diamond bound is \(16\|\mathcal L\|_1t b_N\). Under bounded local bath rates, \(\|\mathcal L\|_1=O(\Gamma N)\). The full-law sampler gives the conditional operation bound

\[
\frac12\|\mathcal D\Phi_t\widetilde{\mathcal E}-\operatorname{id}\|_\diamond
\le\delta_{\rm sample}+\delta_{\rm calibration}
+\delta_{\rm write/read}+16\|\mathcal L\|_1t b_N.
\]

The earlier zero-base conditional variant would add b_N as a preparation floor. Including the constant-size base validity factor removes that floor: sampling accuracy delta is independent of N and of the bad-syndrome probability. Choose N to meet the storage term, then set sampler/write/read precision budgets separately.

Polynomial classical sampling, syndrome decoding, Clifford synthesis, physical routing, write/read gates, and initialized ancillas are part of setup and retrieval. The syndrome and its correction can be computed before the unknown input arrives. No unknown-input copies, rare-event postselection, or already equilibrated protected block are assumed. Product-state initialization/reset and the chosen temperature remain physical resources. Passive storage assumes an exact local stabilizer Hamiltonian and a bounded-rate local Gibbs-stationary Markov bath within the source theorem's class.

The write/read access model must supply local Clifford control, measurement, reset, and routing. It must also allow isolation or switching of the passive Hamiltonian and bath during the circuit, or supply a controlled compensation/protection method whose errors are included in the circuit budget. Polynomial Clifford synthesis by itself does not prove that an encoding circuit run under an uncontrolled thermal bath succeeds. These active-control assumptions are separate from the passive-storage theorem.

Reuse requires readout and reset/reinitialization, paying fresh ancillary purity and the polynomial control/computation bill each cycle. A stationary finite-temperature reservoir remains an environmental resource during the entire waiting interval. Absence of active error correction does not establish zero power or a finite refrigeration-work estimate. Such a hardware energy claim would require an additional reservoir and control model.

The polynomial statement fixes the replacement parameter ell once and for all. If a local truth-table neighborhood contains r(ell) bits, compiling it can cost 2^r(ell); the polymer enumeration exponent and required inverse temperature also depend on the resulting graph degree. These enormous family constants are paid and may be prohibitive. No runtime polynomial jointly in ell and N is asserted. Physical coupling/temperature inputs must be specified to computable finite precision; the calibration bound below accounts for that approximation.

Positive commuting coupling disorder \(J_a\in[J_{\min},J_{\max}]\) is a natural extension to audit. The history coercivity uses J_min, and component-deletion comparisons can use each actual positive coupling. Parameter uncertainty in the prepared Gibbs distribution satisfies a uniform bound

\[
\|\pi_{\beta,J}-\pi_{\widehat\beta,\widehat J}\|_{\rm TV}
\le C\sum_a|\beta J_a-\widehat\beta\widehat J_a|.
\]

To see this, interpolate between the dimensionless energies. The total-variation derivative is one half the Gibbs expectation of the absolute centered energy difference, bounded by its range. Inverse-polynomial calibration can therefore suffice for initialization. Such initial mismatch contracts under all later channels, so it does not require precision inverse in the exponential wait time. Uniformly extending the lifetime theorem to positive disorder still needs verification; it is not claimed as already established by the source.

Arbitrary noncommuting Hamiltonian errors are a separate unresolved robustness problem. A naive hybrid estimate over exponential time can require exponentially small error. For a write/read circuit with G primitives, it suffices that primitive half-diamond errors sum below delta_write/read; the conservative per-primitive requirement is O(delta_write/read/G). This does not prove a fixed physical-noise threshold or remove raw-input injection error. The consequence sought is a completed ideal-model memory operation with explicit precision requirements.

## Selection judgment

The question has a consequential operation, an isolated bottleneck, a conditional compiler with a full proof, and an exact checked example. Its strength is connecting polynomial access to an existing exponential passive-protection theorem. Its vulnerability is that the decoder instantiation might be either a tractable audit or an immediate corollary of a stronger existing sampler. The question-level exchange should challenge those points first, then assess whether access to this conditional physical model is the best target compared with genuinely perturbation-stable operation. Existing equilibrium-inference and partial-SWAP results remain preserved at their established scope.
