# Exact-dynamics quantum memory: rare thermal boundaries, operational access, and priority

Research dossier, 6 November 2026. Governing family: N1645; distinct related construction N1653. This is a research record, not a submission manuscript or a claim of a working quantum memory.

## 0. Result of this round

The strongest completed advance is an improved **conditional exact-Hamiltonian storage theorem**. When logical drift is supported on a thermally rare bad sector of probability $p$, the former consumer lost a square root and gave a useful time scale proportional to $p^{-1/2}$. Two independently checked arguments now give $p^{-1}$, up to explicit norm and temperature factors. One is deterministic and uses relative entropy; the other has a better prefactor and uses endpoint Pauli randomization and a thermal sandwich correlation. These are new derivations within this round. Their historical firstness has not been established.

This does **not** construct a new 3D code, prove N1645's unavailable theorem, prepare an interacting bath, or tolerate a realistic fixed rate of faulty writing. It strengthens a dynamical consumer at explicitly stated static and access hypotheses. The existing 3D construction, native hardware class, fixed-temperature window, perturbation restrictions and ideal endpoints are retained exactly.

Other completed results are:

1. A simple correlation-to-channel theorem for **any correlated resource and any joint CPTP HOLD**, with an infinite-bath C*-algebra version. It removes unnecessary Gibbs, Markov and bath-independence assumptions from this implication. It synthesizes established noiseless-subsystem and channel machinery; no new passive mechanism or priority is claimed.
2. A rigorous obstruction to a tempting noisy-writing interface: global CP domination by one thermal encoder can require an exponential constant even for independent local faults that leave storage perfectly noiseless. A normalized-sector replacement avoids that artificial obstruction but needs a genuine conditional dynamical theorem.
3. A collective-field transfer and its precise obstruction. Full thermal support does not support an exact universally conserved qubit algebra in the entire collective-spin commutant; rare flagged sectors nevertheless allow an approximate full-resource construction. Generic symmetry-breaking leakage remains a separate problem.
4. A primary-source priority review, including actual 2026 Zenodo artifacts. A substantial November predecessor, **Soryun IV**, has a genuine common-recovery construction under a spatial regularity contract. It cannot be replaced by a generic-local-bath claim, and cannot be ignored in a paper about non-Markovian quantum storage.

The most consequential remaining operation is a **noise-tolerant writer-to-long-storage basin theorem for the same microscopic bath and physical model**. That operation, and a favorable full-resource comparison with active fault tolerance, remain OPEN / NOT ACHIEVED.

## 1. Governing evidence, model separation, and dependencies

### 1.1 N1645 is a visible report, not an available theorem

The complete available N1645 update reports a 3D encoded qubit under weak generic local spin-environment interactions and exact physical dynamics, with actual interacting thermal initialization, ideal logical write/read, and enormous constants. Its original manuscript, code family, interaction norm, temperature range and size–time–error contract are unavailable. Internal reviews and ten checks are reported by the producer; their original artifacts are unavailable here. No missing archive was reconstructed or retried.

Pinned current repository revision: `78ff1e3a865e3d0a05af901f77eb1ffd128b00d4`, observed on 6 November 2026. The earlier queue pin was `3918bf6eb69e3b8e902bcbeaae3c5a72f26d6b62`. The exact visible source is unchanged and hashes to `ed3c13e3785d4dd015ef3537f1e95ec5d7a4820bea4f51c49307ce03d08e26dc`.

Primary evidence: [N1645 packet](https://github.com/harjassand/astra-research-knowledge/blob/78ff1e3a865e3d0a05af901f77eb1ffd128b00d4/knowledge/current/packets/N1645.json), [complete visible update](https://github.com/harjassand/astra-research-knowledge/blob/78ff1e3a865e3d0a05af901f77eb1ffd128b00d4/research/2026-11-02-reported-disorder-robust-3d-memory-visible-update/source/dots/DOTS_VISIBLE_UPDATE.txt). The raw-file manifest is in the [supporting record](QUANTUM_MEMORY_RESEARCH_RECORD/sources/SOURCE_MANIFEST.json).

### 1.2 Related capital remains distinct

| Record | Actual available scope | Not supplied by that scope |
|---|---|---|
| N1646 | Commuting-code ideal thermal initialization and a calibrated, sufficiently small, known terminal-Pauli loading construction | Generic noncommuting equilibrium preparation or a universal noisy writer |
| N1649 | Ideal noncommuting thermal encoder with a supplied logical input, known couplings, accessible finite polynomial bath, cutoff and intrinsic accuracy floor | Inaccessible-bath preparation or reliable noisy release |
| N1653 | Native qubit/seven-level-clock model, actual-Gibbs static/protection premises, ideal overwrite, exact same-H storage, and a separately conditional reader | A completed noisy write–store–read device or arbitrary bath/perturbation classes |
| N1694 | A separate three-body candidate, accepted ideal isolated loading at its stated scope, and a short-time noisy handoff boundary | A noisy long-HOLD theorem with the actual correlated bath |

N1653's [robust root](https://github.com/harjassand/astra-research-knowledge/blob/78ff1e3a865e3d0a05af901f77eb1ffd128b00d4/research/2026-11-02-native-memory-read-and-release-boundaries/source/native/construction/ROOT_ROBUST_NATIVE_MEMORY_JOIN.md) and [exact-time consumer audit](https://github.com/harjassand/astra-research-knowledge/blob/78ff1e3a865e3d0a05af901f77eb1ffd128b00d4/research/2026-11-02-native-memory-read-and-release-boundaries/source/native/construction/EXACT_PHYSICAL_TIME_JOIN_AUDIT.md) were read completely. They **already contain** system/clock-only logical SWAP writing, retention of the actual gauge–bath marginal, arbitrary-reference protection and physical-time evolution. Those operations are not discoveries of this round.

The current cached robust-root SHA-256 is `5aa2c40543e2d305e6a26f9a9ef18eb3705d637e532dbd83ffb7606408e84660`. The historical audit names an audited root hash beginning `d833625e`, which is different. The present consumer proofs independently check the displayed interface; they neither extend that historical receipt to different bytes nor invalidate the older result. The separate mixed-source/rod static argument was inspected for its interface but was not independently rederived in this round. Its previous status is retained at its exact scope.

Dependency chain for the proposed application is therefore:

```text
separately established actual interacting-Gibbs rare-tail estimate
  + exact accessible full-space decoder algebra
  + logical commutators supported on the bad sector on both sides
  + supplied actual equilibrium and ideal physical write/read
        -> Theorems E and K below
        -> full rare-tail exponent in the ideal-access storage horizon
```

None of these arrows identifies N1653 with the missing N1645 construction.

## 2. Strongest completed theorem: retain the full rare-event exponent

All finite-dimensional statements use $hbar=k_B=1$, natural logarithms, normalized density matrices, and channel error $d_\diamond(\Phi,\Psi)=\tfrac12\|\Phi-\Psi\|_\diamond$.

### 2.1 Complete assumptions and physical protocol

Let the accessible system $S$ have a **specified full-space** identification

\[
\mathcal H_S\simeq \mathbb C^2_L\otimes\mathcal H_A,
\qquad G=A\otimes B,
\]

where $B$ is an inaccessible finite bath. The corresponding exact logical Paulis $Q_X,Q_Y,Q_Z$ act on $S$ alone. This assumption includes a usable system operation, not merely operators involving the bath or a low-energy code subspace.

Let $H=H^*$ be the actual total Hamiltonian on $L\otimes G$, including all disorder and memory–bath interactions, and let

\[
\omega=Z^{-1}e^{-\beta H},\qquad 0\le\beta<\infty.
\]

Suppose a projector $P$ commutes with every $Q_a$ and

\[
A_a=i[H,Q_a]=P A_aP,\qquad \|A_a\|\le a_a,
\quad p=\operatorname{Tr}(P\omega),\quad A=\sum_{a=X,Y,Z}a_a. \tag{2.1}
\]

No commutation of $P$ with $H$ or $\omega$ is assumed. Two-sided support is essential. If a good-sector protection calculation proves $[H,Q_a](I-P)=0$, Hermiticity supplies the other side; commutation of $P$ with $Q_a$ is still used below.

An unknown input qubit, possibly entangled with any external reference $R$, is initially independent of one supplied resource $\omega$. SWAP it into $L$ and discard the former logical subsystem. In the specified coordinates this deterministic system-only operation gives

\[
E(\rho_{RL})=\rho_{RL}\otimes\omega_G,
\qquad\omega_G=\operatorname{Tr}_L\omega. \tag{2.2}
\]

HOLD is $U_t=e^{-itH}$ under the **same** total Hamiltonian. Readout returns $L$ through the specified system identification and discards $A$. Denote the resulting logical channel by $N_t$. Thus $N_0=\mathrm{id}_2$. Actual-Gibbs preparation, coherent subsystem access, control duration/noise, and readout remain charged resources.

### 2.2 Theorem E: deterministic entropy consumer

For $K\ge0$, define

\[
F(K)=\inf_{\lambda>0}\frac{K+e^\lambda-1}{\lambda},
\qquad F(0)=1,
\quad F(K)\le K+e-1.
\]

**Theorem E — PROVED.** Under (2.1)–(2.2), for every real physical time $t$,

\[
\boxed{
d_\diamond(N_t,\mathrm{id}_2)
\le\min\!\left\{1,
 A p |t| F(\beta A/4)\right\}
\le\min\!\left\{1,
 A p |t|(\beta A/4+e-1)\right\}.} \tag{2.3}
\]

This requires neither a Markov generator nor a weak-coupling limit, a fresh bath, a product initial memory–bath state, or a bath mixing rate. It is a theorem about the stated exact joint state and dynamics.

**Proof.** Put

\[
\Omega=E(I/2)=\frac14\sum_{Q\in\{I,X,Y,Z\}}Q\omega Q.
\]

For each nonidentity $Q$, Gibbs conjugation gives

\[
D(Q\omega Q\|\omega)
 =\beta\operatorname{Tr}\omega(QHQ-H)
 \le\beta a_Q p. \tag{2.4}
\]

Indeed $QHQ-H=-iQA_Q$ is Hermitian, supported on $P$ on both sides, and has norm at most $a_Q$. Convexity in the first argument yields

\[
D(\Omega\|\omega)\le\frac{\beta A p}{4}. \tag{2.5}
\]

Stationarity implies $D(U_t\Omega U_t^*\|\omega)=D(\Omega\|\omega)$. Let $q_t=\operatorname{Tr}(P U_t\Omega U_t^*)$. Data processing under the binary measurement (\{P,I-P\}) gives

\[
d(q_t\|p)\le\beta Ap/4.
\]

For any $\lambda>0$, compare the Bernoulli law of $q_t$ with the tilted law of success probability $pe^\lambda/(1-p+pe^\lambda)$. Classical relative-entropy nonnegativity gives

\[
\lambda q_t
\le d(q_t\|p)+\log(1-p+pe^\lambda)
\le p(\beta A/4+e^\lambda-1).
\]

Consequently

\[
q_t\le pF(\beta A/4)\quad\text{for all }t. \tag{2.6}
\]

This rare-event estimate replaces a Pinsker estimate. It uses the entropy scale $D=O(p)$, rather than converting it to an $O(\sqrt p)$ total-state distance.

For an arbitrary reference-entangled input $\xi_{LR}$, its logical marginal satisfies $\xi_L\le I$, hence $E(\xi_L)\le2\Omega$. Positivity of exact evolution bounds its bad-sector probability $p_{\rm bad}(t)\$ by $2q_t$. No domination involving the dimension of $R$ is used.

Write the derivative of the decoded state as

\[
\dot\xi_{LR}(t)=\frac12\sum_a Q_a\otimes\dot C_{a,R}(t),
\quad
\dot C_{a,R}(t)=\operatorname{Tr}_{L,G}
 [(A_a\otimes I_R)\xi_{LGR}(t)].
\]

For any Hermitian reference contraction $B_R$, two-sided support gives

\[
|\operatorname{Tr}(A_a\otimes B_R)\xi_{LGR}(t)|
\le a_a p_{\rm bad}(t).
\]

Trace-norm duality and $\|Q_a\|_1=2$ imply

\[
\tfrac12\|\dot\xi_{LR}(t)\|_1
\le\tfrac A2p_{\rm bad}(t)\le A q_t.
\]

Integrate from the exactly correct decoded state at time zero, use (2.6), and take the supremum over inputs and references. This proves (2.3). If $p=0$, faithfulness forces $P=0$, and the result is immediate. □

The only substantive entropy imports are established convexity and data processing. A proof of convexity in the first argument follows from entropy concavity, or from flagging the ensemble and tracing out the flag. The latter and the binary measurement meet exactly the hypotheses of [Müller-Hermes–Reeb, Theorem 1](https://arxiv.org/html/1512.06117v2): positive trace-preserving linear maps on separable trace-class spaces. Here all spaces are finite, the maps are CPTP, and the Gibbs reference is faithful. No trace-decreasing or postselected entropy assertion is used. Lindblad's earlier CPTP result is credited; no theorem number from an unacquired original is invented.

### 2.3 Theorem K: a sharper randomized consumer

Apply a uniformly random input Pauli before writing and the matching inverse after readout. Keep two reliable classical frame bits during storage. This twirls the **complete logical channel**; it changes no HOLD interaction. The resource and joint HOLD channel are fixed independently of this frame. Let the averaged channel be $\widetilde N_t$.

**Theorem K — PROVED.** Under the same assumptions,

\[
\boxed{
d_\diamond(\widetilde N_t,\mathrm{id}_2)
\le\min\!\left\{1,\frac{pA}{4}(2|t|+\beta)\right\}.} \tag{2.7}
\]

The bound concerns the actual randomized protocol averaged over its seed. It is not an assertion about every seed. At short times one can also use (2.3), since channel twirling contracts distance from identity, and the quadratic bound in Section 3.

**Proof.** For one logical Pauli $Q$, define

\[
Q(t)=U_t^*QU_t,\quad C_Q(t)=\operatorname{Tr}\omega QQ(t),
\quad S_Q(t)=\operatorname{Tr}\sqrt\omega Q\sqrt\omega Q(t),
\quad b_Q=\|[Q,\sqrt\omega]\|_2^2=2-2S_Q(0).
\]

Stationarity and $A_Q=PA_QP$ give

\[
|S'_Q(t)|
\le a_Q\|P\sqrt\omega Q(-t)\sqrt\omega P\|_1
\le a_Q\|P\sqrt\omega\|_2\|\sqrt\omega P\|_2
=a_Qp. \tag{2.8}
\]

No commutation of $P$ with $\omega$ was used. In an eigenbasis of $\omega$, pairing indices (i,j) and using

\[
(x-y)(\log x-\log y)\ge4(\sqrt x-\sqrt y)^2
\]

proves $2b_Q\le D(Q\omega Q\|\omega)\le\beta a_Qp$. For the scalar inequality, exchange (x,y) if necessary so $x\ge y$, set $x/y=e^u$, and use $\tanh(u/4)\le u/4$ for $u\ge0$. The same pairing of arithmetic and geometric spectral weights gives

\[
|\operatorname{Re} C_Q(t)-S_Q(t)|\le b_Q/2.
\]

Therefore

\[
e_Q(t):=\operatorname{Tr}\omega[Q(t)-Q]^2
=2-2\operatorname{Re}C_Q(t)
\le2a_Qp|t|+2b_Q
\le a_Qp(2|t|+\beta). \tag{2.9}
\]

The complete-basis channel theorem proved in Section 3 gives

\[
d_\diamond(\widetilde N_t,\mathrm{id}_2)
\le\tfrac14\sum_{Q=X,Y,Z}e_Q(t).
\]

Substitution proves (2.7). □

### 2.4 Precisely what the stronger consequence is

Suppose a separately established family has

\[
p_n\le C n^r e^{-c n^\eta},\quad A_n\le C'n^s,
\qquad c,\eta>0,
\]

and a fixed finite inverse-temperature interval. Both (2.3) and (2.7) give a vanishing complete-channel error uniformly for

\[
|t|\le e^{(c-\varepsilon)n^\eta}
\quad\text{for every fixed }\varepsilon>0,
\]

after polynomial slack. The saved Pinsker consumer retained coefficients only below (c/2). The new proof keeps the full rare-tail exponent. It does not change a stretched-exponential family into a different functional class, and it does not establish useful temperatures or device sizes.

For the displayed N1653 interface, $a_Q\le2vn$, so $A\le6vn$. The randomized bound is

\[
d_\diamond(\widetilde N_t,\mathrm{id}_2)
\le3vn p|t|+\tfrac32\beta vn p.
\]

Applying this to that construction is conditional on its separate actual-Gibbs tail/protection theorem, with its native clocks and restricted bath class. It does not transfer the guarantee to N1645.

## 3. Strongest reusable algebraic implication

### 3.1 Any resource, any joint CPTP HOLD

Let $S\simeq\mathbb C^d_L\otimes A$, $G=A\otimes B$, let $\omega$ be **any** fixed joint state on $L\otimes G$, and let $\Lambda$ be **any** fixed joint CPTP channel. No rank, thermal or stationarity assumption is made. Write by logical SWAP, giving $\rho\otimes\omega_G$, and read by tracing $G$:

\[
N(\rho)=\operatorname{Tr}_G\Lambda(\rho\otimes\omega_G).
\]

Let $\{W_a\}_{a=0}^{d^2-1}$ be the discrete Weyl projective error **group**, normalized by $\operatorname{Tr}W_a^*W_b=d\delta_{ab}$. Define

\[
e_a=2-2\operatorname{Re}\operatorname{Tr}
 [\omega W_a^*\Lambda^*(W_a)],\qquad
\bar e=d^{-2}\sum_a e_a.
\]

**Theorem B — PROVED.** The complete-channel Weyl twirl satisfies

\[
\boxed{d_\diamond(\widetilde N,\mathrm{id}_d)
=1-F_e(N)\le\min\{1,\bar e\}.} \tag{3.1}
\]

**Proof.** On a logical reference $R\simeq\mathbb C^d$, let

\[
P_\Phi=\Phi_{RL}\otimes I_G,\qquad
\Xi=I_R/d\otimes\omega.
\]

Direct matrix-unit multiplication gives the exact identity

\[
d^2P_\Phi\Xi P_\Phi=\Phi_{RL}\otimes\omega_G. \tag{3.2}
\]

For Kraus operators $K_j$ of $\Lambda$, extended trivially to $R$, entanglement failure is

\[
\begin{aligned}
1-F_e(N)
&=d^2\sum_j\|(I-P_\Phi)K_jP_\Phi\Xi^{1/2}\|_2^2\\
&\le d^2\sum_j\|[K_j,P_\Phi]\Xi^{1/2}\|_2^2\\
&=d^{-2}\sum_{a,j}\operatorname{Tr}
 \omega[K_j,W_a]^*[K_j,W_a].
\end{aligned}
\]

The last equality uses $P_\Phi=d^{-2}\sum_a\overline W_a\otimes W_a$ and reference orthogonality. Expanding the Kraus commutators and using $\sum K_j^*K_j=I$ gives exactly $\bar e$, proving nonnegativity as well. Weyl twirling makes the logical Choi state diagonal in the orthogonal Weyl–Bell basis, with identity probability $F_e(N)$. A mixture of nonidentity Weyl errors has half diamond distance exactly its total nonidentity probability: the triangle inequality gives the upper bound and a Bell input attains it. This proves (3.1). □

For $d=2^k$, tensor-Pauli randomization needs (2k) retained classical frame bits. The group qualification matters: an arbitrary orthogonal unitary basis need not diagonalize a channel by the same twirl.

This is a mathematical implication, not free access to a subsystem. The logical identification, resource, physical control and frame remain part of the protocol. The bath may keep arbitrary memory; the theorem never replaces it after a time step.

### 3.2 Exact dynamics, stationary states, and infinite baths

For $\Lambda=\operatorname{Ad}U_t$,

\[
e_a(t)=\operatorname{Tr}\omega
 [U_t^*W_aU_t-W_a]^*[U_t^*W_aU_t-W_a].
\]

If $\omega$ is stationary, Duhamel's identity in the $\omega$-weighted Hilbert–Schmidt norm gives

\[
\bar e(t)\le t^2q,\qquad
q=d^{-2}\sum_a\operatorname{Tr}\omega[H,W_a]^*[H,W_a]. \tag{3.3}
\]

The absence of a dimension factor refers to the randomized protocol. With (2.1), (3.3) gives $q\le p\sum_a a_a^2/4$ for a qubit; the KMS argument improves its long-time consequence from $p^{-1/2}$ to $p^{-1}$.

**Infinite-bath form — PROVED.** Let a unital C*-algebra $\mathcal A$ contain a specified accessible unital $M_d$ subalgebra, let $\omega$ be any state, and let $T:\mathcal A\to\mathcal A$ be unital CP. Matrix units identify $\mathcal A=M_d\otimes\mathcal B$. The encoded product state uses the restriction $\omega_{\mathcal B}$; (3.1) holds with $\omega(W_a^*T(W_a))$. The proof replaces Kraus operators with the explicitly constructed Stinespring isometry in the GNS representation. If an invariant automorphism group has a strongly continuous GNS unitary $e^{itK}$ and each $W_a\Omega_\omega\in\mathrm{Dom}(K)$, then $q=d^{-2}\sum_a\|K W_a\Omega_\omega\|^2$ gives (3.3) by the spectral theorem. The full proof, including the dilation construction, is [in the record](QUANTUM_MEMORY_RESEARCH_RECORD/followup/auditor_cross_challenge.md).

This formulation makes no nonexistent infinite-volume Gibbs density matrix or global trace-distance comparison. An infinite bath is a mathematical state/dynamics interface, not a prepared laboratory resource. Passing a particular finite-volume thermal family to it still requires consistent interactions, an equilibrium limit and uniform estimates.

### 3.3 Exact obstruction tests

**Stationarity cannot be removed from (3.3).** For two qubits, take

\[
H=I_L\otimes X_G+Z_L\otimes|1\rangle\langle1|_G,
\quad\omega=(I_L/2)\otimes|0\rangle\langle0|_G.
\]

Every initial weighted logical commutator is zero, so $q=0$. Yet this state is not stationary; at $t=2\pi/\sqrt5$ its reset memory is a nontrivial logical $Z$-rotation with randomized error $\sin^2(\pi/\sqrt5)>0.97$. The direct time-dependent correlation theorem still holds.

**Two generators do not suffice for an arbitrary correlated resource.** Take $\omega=\Phi^+_{LG}$ and $H=\mathrm{SWAP}_{LG}$. The $X$ and $Z$ autocorrelation defects vanish for every time because they preserve the symmetric Bell subspace. The $Y$ defect is $4\sin^2t$. At $t=\pi/2$, logical SWAP writing followed by HOLD yields the completely depolarizing channel. A Gibbs-specific two-generator repair exists in the supporting [thermal addendum](QUANTUM_MEMORY_RESEARCH_RECORD/literature/constructor/two_generator_addendum.md); its modular hypothesis cannot be omitted.

**Randomization matters if logical dimension grows.** With $\omega=I/d$ and $U=I-2|0\rangle\langle0|$, untwirled half diamond distance is one, while $1-F_e=4/d-4/d^2$ and $\bar e=8/d-8/d^2$. The dimension-free conclusion is for the randomized mean channel.

**No per-operator non-Hermitian KMS shortcut.** A single non-Hermitian Weyl need not obey the qubit thermal-filter identity $\|[W,\sqrt\omega]\|_2^2=\int\beta^{-1}\operatorname{sech}(\pi s/\beta)e_W(s)ds$. Pairing $W,W^*$, or averaging an adjoint-closed Weyl basis, repairs it. An explicit qutrit counterexample and exact calculations are retained in the cross-challenge record. The main Theorem B needs no such filter.

## 4. Noisy writing: the wrong interface and a constructive replacement

### 4.1 Global thermal CP domination is too strong

Consider the sufficient condition

\[
W=W_{\rm good}+W_{\rm bad},\qquad
W_{\rm good}\le_{\rm CP}\kappa E_\gamma,
\quad\|W_{\rm bad}^*(I)\|\le\delta,
\quad E_\gamma(\rho)=\rho\otimes\gamma.
\]

Choi support proves that $W_{\rm good}(\rho)=\rho\otimes\sigma$ with $0\le\sigma\le\kappa\gamma$. Thus the good branch must be **exactly logically neutral**. A nonscalar arbitrarily small coherent logical rotation has a different rank-one Bell support and admits no nonzero such good branch: this interface assigns bad probability one even when operational error is tiny.

**Theorem D — PROVED, with local independent faults.** Let an exactly noiseless logical qubit and $m$ gauge spins have bounded onsite Hamiltonian

\[
H=I_L\otimes\Delta\sum_{i=1}^m|1\rangle\langle1|_i.
\]

At fixed $\beta\Delta>0$, gauge equilibrium is Bernoulli $q=(1+e^{\beta\Delta})^{-1}<1/2$. Independent gauge bit flips of any fixed rate $0<f<1/2$ produce Bernoulli $r=q+f(1-2q)>q$. The logical input is unchanged and stores perfectly forever. Nevertheless, for any fixed $q<\theta<r$, every preceding CP decomposition satisfies

\[
\boxed{
\kappa\ge
 [1-\delta-e^{-m d(\theta\|r)}]
 e^{m d(\theta\|q)}.} \tag{4.1}
\]

**Proof.** The gauge event $B_m=\{|g|\ge\theta m\}$ has equilibrium probability at most $e^{-md(\theta\|q)}$ and noisy probability at least $1-e^{-md(\theta\|r)}$, by exponential Markov bounds optimized over the Bernoulli moment-generating function. Evaluate its positive effect on the CP decomposition. The good mass is at most $\kappa\Pr_q(B_m)$; the bad mass is at most $\delta$. Rearrangement proves (4.1), with harmless integer-threshold rounding. □

This is a bounded-strength, bounded-density, geometrically local counterexample to the proposed **interface**, not to memory operation. It proves that extensive changes in harmless gauge weights must not automatically count as logical failure. The same example has extensive relative entropy, so the entropy admission below is sufficient, not necessary.

### 4.2 Rarity alone also does not prove noisy operation

A second construction uses

\[
H_m=\Delta\sum_i n_i+g\,1_{\{|g|\ge\theta m\}}\otimes\mathrm{SWAP}_{LB}.
\]

The bath spin $B$ is inaccessible. Its actual equilibrium bad sector is exponentially rare; the commutators have exact two-sided bad support, and ideal thermal writing protects at every time. Independent gauge flips move almost all probability into the hot sector. At $t=\pi/(2g)$, the hot branch swaps the input into the inaccessible bath. Every accessible reader then has half diamond error at least $3/4-o(1)$, despite exactly correct input at release; the natural logical reader attains the limiting value $3/4$.

This Hamiltonian contains a growing-support threshold term. It is **not** a bounded-body 3D counterexample, and does not refute N1653. It disproves a black-box inference from equilibrium rarity plus exact logical neutrality of gauge faults at release to a general noisy-writer theorem. The full equilibrium law, Chernoff calculation and reader-independent proof are in the [admission record](QUANTUM_MEMORY_RESEARCH_RECORD/literature/constructor/noisy_admission_obstruction_and_sector_repair.md).

### 4.3 Two proved sufficient repairs, with unearned applicability stated

**Entropy admission theorem — PROVED.** Retain $H,\omega,P,A$ from Section 2, but allow any CPTP writer $\Gamma$. Set $\sigma=\Gamma(I/2)$. If

\[
D(\sigma\|\omega)\le Kp,
\qquad d_\diamond(\operatorname{Tr}_G\Gamma,\mathrm{id})\le\varepsilon_0,
\]

then

\[
d_\diamond(\operatorname{Tr}_G\operatorname{Ad}U_t\Gamma,\mathrm{id})
\le\min\{1,\varepsilon_0+A pF(K)|t|\}. \tag{4.2}
\]

**Proof.** Apply the binary entropy estimate to $U_t\sigma U_t^*$. Positivity gives $\Gamma(\rho_L)\le2\sigma$. The reference-safe Pauli derivative calculation in Theorem E then applies unchanged, starting from the charged error $\varepsilon_0$. □

This admits coherent write errors that the rank-one CP-order interface rejects. It does not prove $D=O(p)$ for a fixed-rate noisy circuit. For exponentially rare $p$, that condition can be very demanding.

**Normalized-sector admission theorem — PROVED.** Let normalized gauge–bath references $\gamma_s$ and actual CP writing branches satisfy

\[
W=W_{\rm bad}+\sum_s W_s,\quad
W_s(\rho)=\rho\otimes\sigma_s,\quad
\operatorname{Tr}\sigma_s=w_s,\quad
\sigma_s\le\kappa_s w_s\gamma_s,
\quad\|W_{\rm bad}^*(I)\|\le\delta.
\]

If the same HOLD/reader on $\rho\otimes\gamma_s$ has entanglement failure $\varepsilon_s(t)$, complete-channel Weyl randomization gives

\[
d_\diamond(\widetilde N_t,\mathrm{id})
\le\min\left\{1,\delta+\sum_s w_s\kappa_s\varepsilon_s(t)\right\}. \tag{4.3}
\]

**Proof.** Entanglement failure is a positive linear functional of the written Choi operator. Apply CP domination to each branch, bound the bad trace by $\delta$, and use the exact Weyl-channel diamond identity. □

There is no charge for changed equilibrium **sector weights**. In Theorem D, conditioning on Hamming weight gives identical normalized gauge states before and after faults, so $\kappa_s=1$ and every conditional storage error is zero. The hot-sector example instead has unsafe conditional sectors, correctly exposing a real obstruction.

A concrete stochastic geometry interface is available: suppose background defects obey $\Pr(R\subset T)\le q^{|R|}$, faults obey $\Pr(R\subset F\mid T)\le f^{|R|}$, and a bounded-degree-$D$ geometric lemma proves that **every entire configuration whose union components all have size below $\ell$** is dynamically safe with trivial logical cofactor. Then

\[
\Pr(R\subset T\cup F)\le(q+f)^{|R|},\quad
\delta\le nD^{2(\ell-1)}(q+f)^\ell.
\]

The proof assigns each occupied site to defects or faults, then counts rooted connected sets by depth-first walks. This can handle extensive faults when $D^2(q+f)<1$. The actual interacting Gibbs witness law and its syndrome coherences have **not** been shown to meet this stochastic interface. Coherent good/bad amplitudes do not automatically form a CP instrument. Those are decisive operations, not minor technical qualifications.

## 5. An independent collective-field route and its obstruction

### 5.1 Exact full-support obstruction

For $n$ spin-half particles, collective SU(2) has decomposition $\bigoplus_j V_j\otimes M_j$. The maximal-spin irrep has multiplicity one. Restricting the commutant to it gives a scalar character, so the commutant cannot contain a unital $M_2$: composing such an embedding with the character would give an impossible nonzero homomorphism $M_2\to\mathbb C$. A finite-temperature finite-Hamiltonian Gibbs state is faithful. Thus zero Gibbs-weighted commutator means zero operator commutator; a finite penalty cannot delete that obstructing irrep.

This rules out a naive **exact** full-support collective noiseless factor. It does not rule out approximate access, flagged selection, or common final error recovery.

### 5.2 Constructive thermal repair, and what it costs

Four-spin cells have a rank-two singlet space and rank-fourteen complement. Let $P_b$ project onto the singlet, $Q_b=I-P_b$, and

\[
H=H_B+\Delta\sum_bQ_b+\sum_b F_b+H_{\rm int},
\]

where $H_B$ acts on the bath alone, all terms preserve all flags, and each $F_b$ is supported on **cell $b$ and the bath only**, collective on that cell, with $F_bP_b=0$ and $\|F_b\|\le M$. The sum of norms of $H_{\rm int}$ terms incident to any cell is at most $J$. The $F_b$ may use shared quantum-bath coefficients. Conditional on all other flags, partition-function bounds give

\[
\frac{\Pr(Q_b)}{\Pr(P_b)}\le
r=7e^{-\beta(\Delta-M-2J)}.
\]

**Proof.** Remove the terms incident to cell $b$. Its good sector has dimension two, zero penalty/field, and residual perturbation norm at most $J$; its partition function is at least $2e^{-\beta J}Z_{\rm rest}$. Its bad sector has dimension fourteen, penalty $\Delta$, and perturbation norm at most $M+J$; its partition function is at most $14e^{-\beta\Delta+\beta(M+J)}Z_{\rm rest}$. Divide. Scalar eigenvalue bounds justify these trace inequalities even when the remaining operators do not commute. □

Every conditional bad probability is at most $u=r/(1+r)$, so sequential conditional sampling couples the flags below independent Bernoulli-$u$ flags. No FKG assumption is needed. For $H_{\rm int}=0$, route $k\le(1-u-\eta)N$ inputs into singlet cells, using a declared failure branch otherwise. Exactly collective fields act trivially on successful singlets for every time, so failure is bounded by a binomial large-deviation tail, exponentially small in $N$.

A full-space system-only SWAP formulation is also possible: each fixed-flag sector has dimension $2^g14^{N-g}=2^N7^{N-g}$, hence admits $k\le N$ logical qubits. Identify them with the first $k$ singlet factors whenever available, and choose any factorization on failure sectors. The direct sum gives one exact full-support subsystem identification. Flags belong to its gauge factor and survive SWAP. No conditional success postselection is claimed. Its coherent control/routing can be expensive.

With a separately supplied outer thermal memory, the sector-preserving lift has error at most $\varepsilon_{\rm outer}(t)+Nu$. Making the latter at most $\delta$ by

\[
\Delta\ge M+2J+\beta^{-1}\log(7N/\delta)
\]

pays a growing energy penalty. Fixed penalties instead require a proved dilution-tolerant outer code or extra candidate cells and routing. For fixed-dimensional clock/qudit lifts, choose a rank-$d_b$ subspace of a sufficiently large singlet multiplicity in an $n_b$-spin cell and replace $7$ throughout by $R=\max_b(2^{n_b}-d_b)/d_b$. A rank-seven factor in eight spins has $R=249/7$; the displayed $7$ applies only to four-spin/qubit cells. This changes the penalty bound accordingly and does not remove the outer theorem's own bath restrictions.

An energy gap alone does not control generic nonsymmetric residuals: a local Pauli takes a singlet $s$ to an orthogonal state $v$. A bath level resonant with the penalty and interaction $\lambda\sigma_i^z\otimes X_B$ produces an invariant two-level resonant block with leakage $\sin^2(\lambda t)$, reaching one independently of the gap. The exact construction and all costs are in the [collective-field proof](QUANTUM_MEMORY_RESEARCH_RECORD/literature/machinery/collective_thermal_hybrid.md).

These repairs use established collective noiseless-subsystem theory, not a new discovery of symmetry protection. They earn a complete restricted construction and a transfer obstruction; they do not earn generic-disorder self-correction.

## 6. Exact existing machinery and historical priority

The detailed [import and priority ledger](QUANTUM_MEMORY_RESEARCH_RECORD/literature/machinery/imports_and_priority.md) records source versions, checked theorem numbers, full relevant hypotheses, failed applicability steps, DOI chronology and artifact hashes. Only the entropy and elementary channel tools are imported into the central new consumer proofs; the following code/phase theorems are comparators, not silently assumed dependencies.

| Primary predecessor | Exact relevant machinery | Applicability and priority conclusion |
|---|---|---|
| [Alicki–Fannes, 0809.4180v1](https://arxiv.org/abs/0809.4180v1), 24 September 2008; PRA 79, 012316 (2009) | Sections 2–4, equations (11)–(14) and assignment-map remark: encoded matrix algebra, correlated reference, exact/CP dynamics and logical replacement leaving the syndrome marginal fixed | The access/correlation framework is established. Its equation (23) is an upper fidelity-decay bound involving a preparation norm; it is not the particular lower channel bound derived here. |
| [Chesi–Loss–Bravyi–Terhal, 0907.2807v2](https://arxiv.org/abs/0907.2807v2), 2009; NJP 12, 025013 (2010) | Theorem 1: protected logical algebra and good projector commuting with the Hamiltonian, Gibbs-stationary Lindbladian; error at most $8\|\mathcal L\|_1tp$ | Inverse-rarity storage is already known in that semigroup scope. It does not directly apply to the perturbed exact joint Hamiltonian used here. |
| [Balasubramanian–Davydova–Lin, 2605.10943v1](https://arxiv.org/abs/2605.10943v1), 11 May 2026 | Theorem 3.16, Theorem 5.13 and Corollary 5.14: bounded-density local 3D CSS construction and thermal-memory chain; local Gibbs-stationary Lindbladians | A direct predecessor to unqualified 3D passive-memory existence. It assumes thermal syndrome encoding; preparation is separate. It is not a generic exact spin-bath theorem. |
| [Bergamaschi–Gheissari–Liu, 2507.10976v1](https://arxiv.org/abs/2507.10976v1), 15 July 2025 | Theorem 1.7 / formal 7.8: rapid convergence from a ground state to a thermal logical sector under connectedness/metacheck/correction hypotheses; efficient 4D block realization in 1.8 / 8.2 | Strong preparation comparator. Ground-state input and structural conditions are substantive; the checked 3D recursive code does not automatically meet the required metacheck contract. |
| [Ma–Khemani–Sang, 2509.15204v3](https://arxiv.org/abs/2509.15204v3), v1 September 2025, v3 16 October 2026 | Theorem 1: locally reversible transport along stable-clustering paths; Theorems 2–3: thermal-phase memory with quasi-local, termwise frustration-free Gibbs-stationary Lindbladians | Ordinary two-point clustering and total stationarity do not supply these hypotheses. For $H=X+Z$, its Gibbs state is stationary for the sum but not each commutator term. No exact-bath substitution is justified. |
| [Rakovszky–Placke–Breuckmann–Khemani, 2412.09598v2](https://arxiv.org/abs/2412.09598v2), v1 December 2024, v2 October 2026 | Quantum bottleneck Theorem 2 and supplementary local/quasilocal forms; off-diagonal Gibbs boundary weight; supplementary extensive-barrier perturbation theorem | Slow mixing alone is not coherent qubit storage. Extensive barrier, incidence and energy assumptions do not automatically hold for a subextensive 3D barrier and arbitrary bath volume. |
| [Merkli, 2105.00023v2](https://arxiv.org/abs/2105.00023v2), Quantum 6, 616 (2022), Theorem 1.1 | Uniform-in-time Davies approximation for a finite system and regular free bosonic reservoir | A finite-system theorem with spectral, regularity and initialization hypotheses. No size-uniform arbitrary-spin-bath approximation is supplied. |
| [Aharonov–Kitaev–Preskill, quant-ph/0510231](https://arxiv.org/abs/quant-ph/0510231) | Active threshold with sufficiently small local interaction-norm sum, non-Markovian bath and summable correlated interactions | Exact-Hamiltonian/non-Markovian fault tolerance is not new as a broad phrase. Its gates, ancillas, resets and continuing correction are charged in a fair comparator. |

The collective construction belongs to the established noiseless-subsystem lineage, including [Knill–Laflamme–Viola](https://doi.org/10.1103/PhysRevLett.84.2525) and [Kempe–Bacon–Lidar–Whaley](https://doi.org/10.1103/PhysRevA.63.042307). Its representation and finite thermal estimates are supplied explicitly above; no unverified theorem is used to grant a generic noise threshold.

The search also checked symmetry-protected exact/prethermal memory, growing-local-dimension 3D proposals, partial self-correction and rapid-mixing obstructions at their own noise and temperature quantifiers. Their exact scope notes are in the ledger. Neither a logarithmic energy barrier nor ground-state stability alone proves generic finite-temperature operational memory.

## 7. Recent 2026 Zenodo work: actual artifacts, not titles alone

### 7.1 Substantial comparator: Soryun IV

[Soryun IV: Erasure-Optimal Quantum Memory under Noncommuting Spatial Fields and Non-Markovian Quantum Baths](https://zenodo.org/records/23859937), metadata creators Maciej Nowicki and Artificial Hyperintelligence Eve, was publicly created **1 November 2026**, version DOI `10.5281/zenodo.23859937`, concept DOI `10.5281/zenodo.23859936`. Its 103-page PDF and source ZIP were obtained and its central proof chain was read. The internal “IV” label does not establish earlier public versions; the inspected version endpoint listed one public record.

Theorems 3.3 and 4.2 and Corollary 4.3 construct a common encoder and loss-flag-dependent recovery over a declared family of noncommuting spatial fields and arbitrary bath histories. A uniform integrated operator-norm continuity envelope on one fixed compact spatial domain is essential; leading independent-erasure rate is $(1-2f)_+$. The guarantee concerns entanglement transmission and averaged entanglement infidelity, not worst-case diamond error of each code. General efficient decoding is separate. This is meaningful common-recovery machinery and a genuine priority comparator, not merely a broad claim in metadata.

Its operator-norm regularity fails for independent microscopic bath coefficients $B(x_j)=gZ_j$: distinct sites have norm difference (2g), even when packed arbitrarily close. A fixed-spacing 3D lattice instead grows its domain and does not supply the same sublinear cell-cover argument. Its isometric code and independently supplied bath also differ from the present full-rank joint-Gibbs overwrite resource. Thus no generic-local thermal-memory theorem is imported. This comparison leaves both results intact.

The detailed hypotheses, finite common-envelope bound, proof checks, spatial horizon and DOI chronology are in the [priority ledger](QUANTUM_MEMORY_RESEARCH_RECORD/literature/machinery/imports_and_priority.md). No full-paper correctness certification or historical absence theorem is inferred from this focused reading.

### 7.2 Other checked deposits

| Record | Live public chronology / actual-file finding |
|---|---|
| [18858059](https://zenodo.org/records/18858059), Limsuwan | 4 March 2026. The actual 92-page document's Appendix X leaves 3D existence conditional; its stated bath dynamics is Davies/Markovian. No matching exact-Hamiltonian theorem was obtained. |
| [20778451](https://zenodo.org/records/20778451), Aksman | Created 20 June, publication field 21 June 2026. The inspected memory mechanism assumes instantaneous projection/infinite penalty and cites the May 3D predecessor. That does not supply a finite-energy local physical implementation. |
| [23428551](https://zenodo.org/records/23428551), Aksman | 17 October 2026. A small-angle continuous approximation is identified exactly with a finite-qubit code/Hodge model; the inspected Hilbert-space dimensions disagree. The exact equivalence and consequent lifetime inference are not justified by that derivation. |
| [21356498](https://zenodo.org/records/21356498), Caldin | 14 July 2026. The actual 2671-byte text has no code/Hamiltonian/bath/lifetime scaling proof. Its internal file date is not the public deposit date. |
| [23972523](https://zenodo.org/records/23972523), Caldin | 5 November 2026. The actual 2680-byte text likewise does not supply the theorem suggested by its self-correcting-memory title. This is a finding about this file, not every work by the author. |

A separate May Aksman deposit was metadata-screened only and is explicitly not assigned a proof judgment. Software and experimental-memory datasets found in broader searches were not treated as passive-self-correction theorems. Biological content in multi-topic deposits was not used.

### 7.3 Coverage and limits of priority checking

Searches included exact phrases, title fields and variants of self-correcting/passive/thermal/exact quantum memory, disorder, Hamiltonian, initialization, autocorrelation and non-Markovian baths. Zenodo's public API, complete relevant records, available concept/version endpoints and primary files were used. Anonymous size-100 queries were rejected; size-25 pagination succeeded. Focused thermal-memory and exact-memory queries had all their returned pages retained; broad noisy multi-topic searches were bounded rather than claimed exhaustive. Dates were checked record by record because search filters sometimes returned older results.

Version DOI, concept DOI, public creation date, self-reported publication date and internal manuscript date were kept distinct. A DOI deposit, a year in a title, or an author's internal version number is not a mathematical proof or evidence of firstness. Historical novelty of the exact new consumer remains **NOT ESTABLISHED**. A paper should not claim the first passive 3D quantum memory, the first logical thermal overwrite, or the first quantum-memory/correlation bridge.

## 8. Novelty and status ledger

| Item | Status | Dependency / scientific accounting |
|---|---|---|
| N1645's reported 3D theorem | REPORTED; theorem unavailable | Original scope retained; not reproved, disproved, or upgraded |
| N1653 static native-memory theorem | Existing capital at its stated scope | Distinct native clocks/bath/temperature class; not rederived here |
| Logical replacement retaining the gauge marginal | KNOWN | Alicki–Fannes and earlier internal N1653 |
| General Bell/Weyl implication, including C* bath | PROVED formulation | Elementary complete-channel/noiseless-algebra synthesis; historical novelty unknown |
| Entropy and KMS inverse-rarity exact-H consumers | PROVED conditional upgrade | Same actual-static/protection premises; full rare-tail exponent; no new code or noise threshold |
| Arbitrary-writer entropy admission | PROVED sufficient interface | Does not construct a writer meeting its stringent average-state entropy bound |
| Exponential global CP-domination cost under harmless independent faults | PROVED obstruction | Bounded onsite geometric model; disproves necessity of that interface |
| Hot-sector noisy storage failure | PROVED finite counterexample | Growing-support Hamiltonian; explicitly not a local 3D no-go |
| Normalized-sector/cluster repair | PROVED conditional theorem | Actual quantum Gibbs and noisy-writer admission remain open |
| Collective full-support exact-commutant obstruction and thermal repair | PROVED restricted model | Established symmetry mechanism; exact invariance, access and cost assumptions retained |
| Generic noisy operational 3D memory and matched practical benefit | OPEN / NOT ACHIEVED | Needs same-model preparation, fault containment, long HOLD and readout, plus a full-cost comparator |
| Historical firstness | NOT ESTABLISHED | Concrete predecessors excluded; bounded searches cannot prove absence |

The new full-exponent consumer is a material theoretical sharpening, not a demonstrated new memory device. The strongest counterexample changes the intended next operation: a single global equilibrium domination constant is an unsuitable universal target. A successful noisy-access theorem should preserve the logical subsystem while allowing large, dynamically harmless gauge changes.

## 9. Remaining decisive operations and constructive attacks

### A. Noisy release into a long-lived basin — highest priority

For one fixed physical model, construct the complete CPTP writer from an unknown reference-entangled input, under a declared many-location fault model. Prove a decomposition into admitted conditional gauge–bath ensembles with small bad mass and suppressed conditional logical drift over the whole HOLD interval. Neither a marginal-state estimate nor a short-time handoff is enough.

The concrete target is (4.3) with physically derived $w_s,\kappa_s,\varepsilon_s(t)$, or a different reference-safe certificate that permits harmless extensive gauge changes. A quantum cluster version must control syndrome coherences, fault propagation through auxiliaries, and real-time bath correlations. The existing scalar equilibrium witness law is not already that theorem.

An alternative certificate is a constructed positive operator $F\ge P$ with $i[H,F]\le\epsilon I$ and small actual writer expectation $\sup_\rho\operatorname{Tr}F\Gamma(\rho)\le\eta$. For forward times $t\ge0$, it gives $p_{\rm bad}(t)\le\eta+\epsilon t$ and, for correct initial logical input, deterministic error at most $\tfrac A2(\eta t+\epsilon t^2/2)$. The proof integrates the Heisenberg inequality and the same Pauli derivative bound. Constructing such an observable with the required suppressed parameters is the hard operation; defining it using an unknown future trajectory does not solve it.

### B. Actual interacting resource acquisition

Prepare the required gauge–bath marginal or a proven admissible substitute with finite local controls. An ideal isolated loader is not automatically a loader with the actual inaccessible bath. Ground-to-sector samplers, Gibbs transport and Petz/common-envelope recovery should be tested against their exact interfaces before rebuilding bespoke machinery. Account for the supplied ground state, coupling knowledge, bath access, gate complexity, mixing time, intrinsic floors and refrigeration.

### C. Robust collective-field hybrid

At fixed cell size, strength, density and temperature, prove stability of the actual sector-conditioned outer code under a positive density of thermal flagged defects and small generic nonsymmetric residuals. The conditional thermal flag estimate supplies a useful input. The multiplicity-one obstruction and resonant bath example show why exact symmetry plus a penalty does not already prove the result.

### D. Full-resource comparator

Compare with active fault-tolerant encoding/storage using the same controls, bath access, cooling, connectivity, classical hardware, calibration precision and timing. Include writing, HOLD, readout, reset and total space–time/energy resources. A lifetime theorem with prohibitive sufficient constants, a finite calculation or a successful archive deposit does not establish an advantage. No such advantage is established in this dossier.

## 10. Independent investigation, checks, and preserved record

Exactly three independent GPT-6.1 Sol researchers at maximum reasoning were used alongside the principal. The initial questions were existing machinery/priority, independent operational construction, and hostile mathematical audit. Each initial report was preserved before substantive construction exchange; subsequent challenges and corrections are separate files. The machinery initial notes the timing of a constructor message arriving during its save after its derivation was formulated. No further researchers were spawned.

Initial hashes and source pins are recorded in the supporting manifest. The strongest final theorems were then checked against the competing independent constructions, the old consumer, explicit counterexamples and primary sources. The full-exponent proof was independently accepted by all three researchers at its stated hypotheses.

Finite diagnostics include:

- 120 principal stationary-SWAP normalization/inequality cases and explicit marginal/coherent-writer obstructions;
- 144 constructor Bell/Weyl cases across logical dimensions 2–5, plus the non-Hermitian filter correction;
- 180 auditor stationary cases and 60 arbitrary-resource nonunitary CPTP cases;
- 405 structured Gibbs cases testing the support, entropy, thermal-sandwich, spectral and linear-$p$ inequalities;
- finite product-gauge smooth-domination, hot-sector and binomial-tail checks.

Residuals are recorded in the actual check files. These scripts verify finite algebra and normalization only. The proofs above establish the implication theorems; the scripts do not prove an infinite-volume static tail, historical priority, a hardware threshold or practical advantage.

Final supporting record: [index](QUANTUM_MEMORY_RESEARCH_RECORD/INDEX.md). Complete raw retrieval/search caches remain under `work/quantum-memory-20261106/`; their coverage and hashes are indexed. Earlier published manuscripts, website assets and Zenodo records were not modified by this research round.
