# Independent primary-literature challenge: recurrent normal unitary reservoirs

Date: 2026-10-21. Reviewer: `/root/recurrent_bath_literature`.

Scope: a new discrete-time open-systems question; this review does not reopen B2 R1, N33, N557, hidden entropy, or IQM. This is a literature comparison and independent boundary check, not external certification or a historical-priority claim.

## 1. Assessment

The candidate theorem is consistent with the primary literature examined. Its scientifically meaningful step is **trace-norm recurrence of one normal reservoir state under maximally mixed reference inputs implies a uniform finite-spectral approximation of the complete process**. Finite-environment rank bounds and the resulting maximal quantum communication rate are established perfect-memory-channel machinery. The contrast between repeated identical one-use channel marginals and a tensor-product process is also established and must be kept explicit.

I found no primary source in the searches below that states exactly the proposed combination: infinite-dimensional separable type-I reservoir, arbitrary normal density including infinite von Neumann entropy, recurrence only along a subsequence under reference inputs, and asymptotically maximal separation from every fixed nonunitary independent channel. This search result is not a priority certification. The proof ingredients are elementary or well-established enough that the strongest defensible description is a carefully scoped recurrence-to-perfect-memory extension, with an explicit process discrimination consequence.

The candidate statement should not be advertised as an impossibility of nonunitary one-use channels, nonunitary reduced semigroups, or memoryless noise from any separable normal infinite reservoir. All three broader claims would be false or outside its proved scope.

There is a useful split within the result. Intertwining already implies that the channel induced by each reference-orbit bath state is unital: tracing out the bath from `U(I/d⊗tau_t)U*=I/d⊗tau_(t+1)` gives `I/d`. The difficult comparison with repeated noisy marginals is therefore the nonunitary **unital** case, where one-use tests can agree forever and correlations reveal the obstruction.

## 2. Closest established results

### 2.1 Perfect finite memory: Kretschmann–Werner (2005)

D. Kretschmann and R. F. Werner, *Quantum Channels with Memory*, Physical Review A **72**, 062323 (2005), https://arxiv.org/abs/quant-ph/0502106 ; full source https://arxiv.org/pdf/quant-ph/0502106 .

Section III D, Theorem 1 establishes maximal classical and quantum capacity for pure/isometric finite-memory channels, including their initial/final-memory access conventions. Lemma 2 proves a block channel with memory dimension `m` has at most `m^2` Kraus operators, uniformly in block length. This is exactly the finite-environment rank mechanism needed here. Their Lemma 3 gives an exact code via repeated eigenvalue pairing, with dimension at least `floor(D/2^(K^2))` for input dimension `D` and `K` Kraus operators. The end of Section III D credits the stronger Knill–Laflamme–Viola convex-set bound `D/[K^2(K^2+1)]`.

Their Theorem 4 gives a broad causal-channel realization by concatenated memory channels; that realization theorem does not impose the present no-discard unitary reservoir or recurrence assumptions. Finite-memory quantum capacity is therefore inherited, not a fresh discovery.

Retrieved full-source references: `turn41view2`, `turn42view3`. The exponent in `2^(K^2)` is easily lost in text extraction; it follows directly from the repeated halving proof.

### 2.2 Subexponential exact environment growth: Giovannetti–Burgarth–Mancini (2009)

V. Giovannetti, D. Burgarth, and S. Mancini, *Communication through a quantum link*, Physical Review A **79**, 012311 (2009), https://arxiv.org/abs/0810.0170 ; full source https://arxiv.org/pdf/0810.0170 .

Definition 1, Eq. (5), calls a block-channel sequence perfect memory when it has representations with environment/Kraus size `k_n` satisfying `log(k_n)/n -> 0`. Theorem 2, Eq. (9), obtains zero-error quantum codes with size exceeding `d^n/(k_n^4+k_n^2)` for sufficiently large `n`, hence rate `log_2 d`. The proof explicitly applies convex-set error-correction arguments; its existence result makes no efficient encoder/decoder claim.

This definition concerns **exact** rank. A process produced from infinite-rank normal `tau` can have much larger exact block rank even when every horizon is uniformly close to a fixed-rank process. Consequently the proposed result should use a phrase such as “uniform approximation by perfect-memory processes,” rather than assert without proof that the untruncated process satisfies this exact definition.

Retrieved full-source references: `turn42view0`, `turn43view1`, `turn44view0`.

### 2.3 General low-error-space coding: Knill–Laflamme–Viola (2000)

E. Knill, R. Laflamme, and L. Viola, *Theory of Quantum Error Correction for General Noise*, Physical Review Letters **84**, 2525–2528 (2000), https://arxiv.org/abs/quant-ph/9908066 ; full source https://arxiv.org/pdf/quant-ph/9908066 .

Theorems 3–4 construct large classical and quantum codes from the dimension of a self-adjoint error-detection space. Theorem 3 uses greedy orthogonal selection. Theorem 4 uses partitions whose convex hulls intersect, yielding approximately input dimension divided by the square of error-space dimension. This is the direct source of the familiar fourth power of Kraus count. The paper explicitly notes that this proof is not a straightforward constructive method.

The parent’s proposed refinement to `ceil(D/K^4)` can be proved by keeping the identity coordinate fixed and applying affine Tverberg in at most `K^2-1` real dimensions. This is a modest sharpening of inherited machinery, not the scientific bottleneck. No investment in the coding constant is warranted here.

Retrieved full-source references: `turn41view1`, `turn42view1`.

### 2.4 Repeatable one-use marginals: Rybár–Ziman (2008)

T. Rybár and M. Ziman, *Repeatable quantum memory channels*, https://arxiv.org/abs/0808.3851 ; full source https://arxiv.org/html/0808.3851v1 .

Section III, Theorem 1 constructs repeatable random-unitary channels using a finite controlled-unitary memory. Theorem 2 excludes nonunital repeatable channels with finite memory by an entropy budget. Their repeated-channel criterion concerns individual uses; Section II discusses why correlated inputs need a fuller framework. Thus their result permits nonunitary noisy marginals forever and does not give an independent tensor-product process.

Near the end of Section III they describe a shift reservoir and dismiss the infinitely many-cell limit as nonseparable. That sentence must not be used as an obstruction in the present model: the vacuum incomplete tensor-product Hilbert space is separable, and its pure vacuum is a normal state. An explicit construction is given below.

Retrieved full-source references: `turn38view0`, `turn40view0`.

### 2.5 Earlier finite-memory mechanism: Bowen–Mancini (2004)

G. Bowen and S. Mancini, *Quantum channels with a finite memory*, Physical Review A **69**, 012306 (2004), https://arxiv.org/abs/quant-ph/0305010 ; full source https://arxiv.org/pdf/quant-ph/0305010 .

Section II B, Eq. (4), distinguishes persistent memory from fresh independent environments. Removing those fresh environments defines their perfect-memory case. Section II C explicitly presents a correlated dephasing channel whose individual output density matrices agree with a memoryless dephasing channel while outputs are correlated. Section III discusses the negligible asymptotic information loss of a finite memory.

This provides an early physical formulation of the mechanism; the precise coding theorem and rank bound above are the sharper mathematical predecessors.

Retrieved full-source references: `turn38view3`, `turn39view4`.

### 2.6 Complete process versus reduced channels: Pollock et al. (2018)

F. A. Pollock, C. Rodríguez-Rosario, T. Frauenheim, M. Paternostro, and K. Modi, *Operational Markov Condition for Quantum Processes*, Physical Review Letters **120**, 040405 (2018), https://arxiv.org/abs/1801.09811 ; full source https://arxiv.org/html/1801.09811v1 .

The operational condition accounts for interventions and conditional histories. The paragraph preceding Eq. (3) gives the product form of a Markov process Choi operator. Their lemma and Appendix B distinguish this property from divisibility of reduced maps. The proposed witness using maximally entangled input-reference pairs and a joint final measurement is a valid complete-process test. A lower bound from that particular tester suffices for a lower bound on optimal causal discrimination; it does not require claiming that normalized Choi trace norm equals the full strategy norm.

Retrieved full-source references: `turn45view0`, `turn46view0`, `turn46view1`.

### 2.7 Discrete and continuous dilation results do not contradict recurrence obstruction

F. vom Ende and G. Dirr, *Unitary Dilations of Discrete-Time Quantum-Dynamical Semigroups*, Journal of Mathematical Physics **60**, 122702 (2019), https://arxiv.org/abs/1804.00918 ; full source https://arxiv.org/pdf/1804.00918 . Theorem 4 provides a fixed unitary, separable auxiliary Hilbert space, and pure normal auxiliary state with `T^n(A)=Tr_E[V^n(A⊗omega)V*^n]` for every `n`. This concerns powers of one reduced channel and does not assert recurrence of the full bath or equality of complete intervention-dependent processes. Retrieved references: `turn44view1`, `turn45view2`.

F. vom Ende, *Quantum-Dynamical Semigroups and the Church of the Larger Hilbert Space*, https://arxiv.org/abs/2211.08351 ; full source https://arxiv.org/html/2211.08351v3 . Theorem 1 says a finite-dimensional quantum dynamical semigroup has a dilation with bounded total Hamiltonian exactly when the semigroup is unitary. This is a continuous-time derivative obstruction, not the present discrete-time recurrence argument. The paper’s “type I Stinespring curve” means bounded Hamiltonian; it must not be confused with a type-I von Neumann reservoir algebra. Retrieved references: `turn38view1`, `turn39view2`.

### 2.8 Multiplicative rigidity is inherited operator theory

M. Rahaman, *Multiplicative Properties of Quantum Channels*, https://arxiv.org/abs/1701.06205 ; full source https://arxiv.org/html/1701.06205v4 . Theorem 1.3 relates the multiplicative domain to fixed points of `E*E`; Theorem 2.5 identifies the automorphic peripheral part of a finite-dimensional unital channel. Retrieved references: `turn38view2`, `turn46view2`.

E. Størmer, *Multiplicative properties of positive maps*, Mathematica Scandinavica **100**, 184–192 (2007), https://arxiv.org/abs/math/0607090 ; full source https://arxiv.org/pdf/math/0607090 . Theorem 7 places weak orbit limit points in the multiplicative core under a faithful family of invariant normal-state hypotheses. This is relevant background but is not automatically applicable to the parent’s single recurrent, potentially nonfaithful density. A direct Hilbert–Schmidt argument avoids assuming those additional hypotheses. Retrieved references: `turn44view2`, `turn45view3`.

## 3. Independent boundary constructions

The following calculations are supplied explicitly to test the model; they are not assertions of historical novelty.

### 3.1 A recurrent finite memory produces the same nonunitary marginal indefinitely

Take a qubit environment with `tau=I/2` and

`U = I_S⊗|0><0|_E + Z_S⊗|1><1|_E`.

Every individual use on independently prepared inputs induces dephasing `N(rho)=(rho+Z rho Z)/2`. The environment marginal is unchanged. The full `n`-use channel is

`M_n(rho) = [rho + Z^(⊗n) rho Z^(⊗n)]/2`,

not `N^(⊗n)`. On normalized Choi states, the former is supported on the two global error strings `00...0` and `11...1`; the latter is uniform over all `2^n` error strings. Therefore

`(1/2)||J(M_n)-J(N)^(⊗n)||_1 = 1-2^(1-n)`.

For `n=1` this is zero; it tends to one. This example verifies both that the proposed theorem is compatible with indefinitely repeatable nonunitary marginals and that the joint-process quantifier carries real content.

### 3.2 Any finite-dimensional channel has a normal separable shift-bath realization without recurrence

Let `N` be any channel on a finite-dimensional system. Choose a finite ancilla `a`, a vector `|0>_a`, and a unitary `W` on `S⊗a` realizing `N`. Let `E` be the Hilbert completion of finite-excitation vectors over the bilateral lattice `Z`, with each site a copy of `a` and all but finitely many sites in `|0>`. Its standard finite-support tensor basis is countable, so `E` is separable. The all-vacuum vector `|Omega>` belongs to it, and `|Omega><Omega|` is a normal rank-one density.

The lattice shift `L` permutes that orthonormal basis and extends to a unitary. Choose its direction so that, after acting on site zero, the next unused vacuum site arrives at zero. Define a single fixed global unitary

`U = (I_S⊗L) W_(S,0)`.

Each use couples the incoming system to a new vacuum cell. Used cells remain in the same persistent `E`. By induction, the complete channel on `n` incoming ports is `N^(⊗n)`, including inputs entangled across ports and ancillary references; adaptive operation also follows because no used cell returns to the interaction site. There are no newly appended cells after initialization, only the infinitely many cells already included in `E`.

Normality and separability alone therefore do not give the candidate obstruction.

For a direct recurrence calculation, take `a=S`, `W=SWAP`, and `N(rho)=|0><0|`. Under the maximally mixed reference input, after `n` steps exactly `n` used cells are maximally mixed and the others are vacuum. The bath state commutes with the initial vacuum projector and assigns it weight `d^(-n)`. Thus

`(1/2)||tau_n-tau_0||_1 = 1-d^(-n)`.

The full return error is twice this value. The bath is maximally nonrecurrent in the large-`n` limit. This is an explicit counterexample to any proposal that treats a stationary supply of local fresh sites as return of the entire environment.

### 3.3 Non-atomic stationary baths change the algebraic assumption

Let `Omega={0,1}^Z` with its fair Bernoulli product measure, and let the bath observable algebra be `L∞(Omega)`. Read coordinate zero as a control bit for `I` or `Z`, then shift. The Bernoulli measure is invariant, and independent successive coordinates produce the independent dephasing process. This is a normal stationary state on a **non-atomic commutative algebra**, not a normal density on the full type-I algebra `B(E)` satisfying the candidate’s return condition.

One may represent this commutative algebra on the separable Hilbert space `L²(Omega)`, with constant vector `1`. However, extending the observable algebra to `B(L²(Omega))` changes what return means. Under a maximally mixed system input, a controlled phase produces a mixture of the vector `1` and the independent coordinate-sign vector; its rank-one initial density is not preserved. Keeping only multiplication observables hides those lost coherences.

Hence “stationary classical bath,” “normal state on some von Neumann algebra,” and “normal trace-class full quantum bath state returns” are distinct contracts. The first two do not refute the candidate theorem. A further non-atomic generalization would require a different conclusion or an additional atomicity/compactness assumption.

## 4. Coding consequence and its honest boundary

Assume the parent proves the common device supplies, for every `eta>0`, a truncated block channel `M_(n,eta)` with at most `r_eta^2` Kraus operators and

`||M_n-M_(n,eta)||_diamond <= 2 eta`

uniformly over `n`. The same initial-state estimate also holds under arbitrary causal testers. Apply the established exact-code theorem to the truncated channel. An exact decoder for it gives an effective actual encoded channel whose diamond error is at most `2 eta`; the associated worst-case half-trace error is at most `eta`.

Choose cutoffs sufficiently slowly so that `eta_n -> 0` and `log r_(eta_n)=o(n)`. Such a diagonal choice exists because each fixed cutoff has finite rank. Then code dimension has logarithm `n log d-o(n)`, yielding asymptotic quantum transmission rate `log_2 d` qubits per port, with no access to the final reservoir required. This is a consequence of uniform approximation and known coding, not a separately novel capacity theorem.

There is no universal quantitative rate of convergence from normality alone: spectral tails may decay arbitrarily slowly, and infinite entropy is allowed. The argument does not provide efficient encoding, efficient joint measurements, experimentally accessible bath spectra, an energy bound, a finite-time recurrence guarantee, or robustness to an unspecified fixed return error.

## 5. Proof obligations and recommended claim language

1. Define recurrence as a subsequence tending to infinite times; do not include the trivial `t=0` return.
2. Establish the reference channel’s bistochastic extension and Hilbert–Schmidt contraction without a finite-entropy premise.
3. Derive product intertwining from equality in the partial-trace Hilbert–Schmidt contraction, then obtain **spectral-projection** intertwining for all times. Keeping arbitrary top eigenvectors through a degenerate eigenvalue requires care; full spectral blocks are the clean choice.
4. Show the finite spectral subspaces are invariant for all external inputs and histories, although recurrence was assumed only for the maximally mixed reference trajectory.
5. Keep the same initializer and device when passing to every horizon. The finite-rank state approximation may depend on the requested tolerance, but never on the horizon.
6. Bound complete process error by initial-state trace distance using a single global tester channel; avoid a per-use hybrid bound that introduces a spurious factor `n`.
7. State normalized Choi conventions and make the distinction between a witness lower bound and equality with strategy distance explicit.
8. Attribute rank-to-coding, multiplicative-domain rigidity, and the operational distinction between marginals and processes to prior work. Describe recurrence-to-uniform spectral approximation as the candidate extension; leave priority open.

My recommended narrow conclusion is: **For a fixed closed unitary device with a normal trace-class reservoir, recurrence under maximally mixed reference inputs precludes indefinite independent nonunitary noise and makes the complete process uniformly approximable by finite-memory unitary processes.** Its force lies in counting the entire reservoir and in the absence of a finite-entropy assumption. It leaves conventional nonrecurrent infinite reservoirs and non-atomic stationary noise models available, as it should.

## 6. Search and provenance record

Primary sources were opened directly at arXiv; publisher results were used to check publication identities. Searches included repeatable channels, finite-environment Markovianity, quantum dynamical semigroup dilation, perfect-memory channels, finite Kraus rank coding, multiplicative cores, and operational Markov conditions. No outreach occurred. No inaccessible private proof was inferred from a summary. The literature search is bounded and cannot certify historical novelty.

The parent should open the cited web references or URLs in its own tool context before using their citation IDs in a public-facing answer. The source content references above identify actual retrieved pages; they are not invented citations.
