# Reusable closure, local coherent faults, and causal normalization

Author `producer-workspace/protected_algebra`, 29 October 2026. New work in `p2_reuse`; all `p2_protection` predecessors remain frozen. This is an authored theorem package, not its independent review or a hardware threshold certificate.

## 1. Consequence and interface

A mediator can retain arbitrary quantum memory between completed operations without becoming an uncontrolled broadcast path for an old fault. The decisive condition is that every *good completed operation*, on its entire admitted returning-memory input, acts as the intended data operation tensor a memory operation. Every later transfer of the bath's stored information back to new data must then pay another local fault factor. No bath reset, short correlation time, commuting bath coefficients, or small bath-only Hamiltonian is required **between those boundaries**.

This statement concerns a declared network of ports. A boundary is not created merely by naming a pulse sequence a gate. It must include all returning carriers, coherently selected controls, actual records and continuation after leakage/loss. A retained classical record that later controls the intended computation is a computational control rail: its corruption is a charged control fault, not unrestricted bath-only evolution. Internal interfaces exposed to outside intervention must be additional declared boundaries, each with its own theorem. A small completed-call channel distance supplies no arbitrary-intervention guarantee inside the call.

Three constructions are proved here:

1. A finite observable-algebra test acquires an approximate product dilation on all returning-memory states, with no bath-dimension factor. For an actual unitary, a uniform reduced-data channel certificate also gives a **linear** conversion. The stronger uniform input promise is essential.
2. Product closure plus physical support gives the usual selected-location coherent-noise condition, even under arbitrary noncommuting bath evolution between macros. Unselected operations are resummed as actual contractions; no factor exponential in computation volume is incurred.
3. A deterministic causal projection normalizes a signed good *comb* without changing its record timing. This replaces an endpoint polar normalization when a reusable multitime interface is required. It does not manufacture missing comb factorization from an endpoint statement.

The local-noise receiver and threshold consequences are established fault-tolerance machinery. The added instrument is the explicit acquisition and causality bridge from algebraic mediator closure to that machinery. No historical priority is claimed for these mathematical ingredients.

## 2. An algebraic certificate for approximate closure

Let A be r data/control qubits touched by a macro, M the complete returning memory, and M' the complete memory output. Reference systems are arbitrary. The physical macro is an isometry

\[
V:A\otimes M\longrightarrow A\otimes M',\qquad V^\dagger V=I.
\]

Fresh supplies and retained measurement-copy environments, when present, have already been included in this actual isometry. Remove the specified data unitary G by replacing V with (G^dagger tensor I)V. All statements below are then about the identity data target.

For each of the 2r Hermitian Pauli generators P=X_i,Z_i define the *intertwining defect*

\[
d_P=\|(P\otimes I_{M'})V-V(P\otimes I_M)\|,
\qquad z=\tfrac12\sum_{i=1}^r(d_{X_i}+d_{Z_i}).                 \tag{1}
\]

This is an operator-norm statement on the full input, not an average over one calibrated bath state. Define the rectangular conditional expectation

\[
\mathsf E(V)=4^{-r}\sum_{P\in\mathcal P_r}
(P\otimes I_{M'})V(P\otimes I_M)=I_A\otimes A_0,
\quad A_0=2^{-r}\operatorname{Tr}_A V.                         \tag{2}
\]

The averaging map is a norm contraction. The 2r maps (I+Ad_P)/2 commute as superoperators. Telescoping their product, and keeping every other factor as a contraction, gives

\[
R=V-I\otimes A_0,\qquad \|R\|\le z.                        \tag{3}
\]

The variance identity is stronger than a plain triangle estimate:

\[
I_M-A_0^\dagger A_0=\mathsf E_A(R^\dagger R),\qquad
0\le I_M-A_0^\dagger A_0\le z^2 I_M.                         \tag{4}
\]

Here E_A denotes normalized trace over A; the cross terms vanish by E(R)=0. If z<1, polar normalization

\[
W=A_0(A_0^\dagger A_0)^{-1/2}
\]

is a memory isometry and

\[
\boxed{\ \|V-I_A\otimes W\|
\le f(z):=z+1-\sqrt{1-z^2}.\ }                              \tag{5}
\]

One may replace z in (4)-(5) by any certified tighter value of ||R||. If V is unitary on A tensor M, the analogous identity for VV^dagger shows A_0 A_0^dagger>= (1-z^2)I; W is then unitary. The proof extends to arbitrary Hilbert-space M for bounded V because the average is over a finite-dimensional data factor and the spectral lower bound makes the inverse bounded. No finite bath dimension or cutoff was used.

The full joint half-diamond distance of the actual and product channels is at most f(z), by the isometry comparison and trace contraction. This includes arbitrary initial data-memory-reference correlations. It is a product of **maps**, not an assertion that their correlated output state is a product. If the dilation copies each actual classical outcome to a measurement environment, the average (2) and input-side polar normalization preserve that outcome-copy subspace. No new latent record is measured.

### 2.1 A linear conversion from a uniform reduced-data test

Suppose now that V is an actual unitary on A tensor M. Define the channel on the *whole* input

\[
\Phi_V(\rho_{AM})=\operatorname{Tr}_M(V\rho V^\dagger),\qquad
\delta=\tfrac12\|\Phi_V-\operatorname{Tr}_M\|_\diamond.       \tag{6}
\]

Duality implies ||V^dagger(P tensor I)V-P tensor I||<=2 delta for every data unitary P. Because V is unitary, this equals ||(P tensor I)V-V(P tensor I)||. Averaging **all** Pauli conjugates directly yields ||R||<=2 delta, without a factor r. Thus, for 2 delta<1,

\[
\boxed{\ \inf_{W\ {\rm unitary}}\|V-I\otimes W\|
\le f(2\delta)=2\delta+1-\sqrt{1-4\delta^2}.\ }             \tag{7}
\]

This linear small-delta behavior is not a replacement for the general square-root continuity theorem for arbitrary channels. It uses the actual joint unitary and a diamond norm whose input includes **every state of the returning memory**, not a fixed bath preparation. Equation (1) is often the more useful microscopic acquisition route, since only local generator defects need a proof. Neither test is claimed experimentally cheap for an uncontrolled bath.

### 2.2 Two sharp scope separations

**Fixed bath calibration is insufficient.** Let V=I_A tensor |0><0|_M + Z_A tensor |1><1|_M. With M=|0>, the data channel is exactly identity. A permitted bath X between calls makes the next data operation Z. On |+> the operation error is one. The full-input test (6) detects this; a reset-state calibration does not.

**Fresh isometries generally need a square root.** For c^2+s^2=1, define V|psi>=c|psi>|0>+s Z|psi>|1>. The reduced-data half-diamond error is s^2, whereas the actual joint output on |+> has expectation 2cs for Z_A tensor X_M. Any identity-data tensor memory comparison has zero expectation for that observable. Its joint half-diamond discrepancy is therefore at least cs. No bound linear in the reduced error s^2 can hold uniformly as s tends to zero. KSW supplies the appropriate generic square-root ancestry. Direct intertwining data (1) still proves (5) for this isometry.

## 3. Why exposed intervention times matter

### 3.1 Exact endpoint equality can hide maximal comb error

Take two SWAPs between A and M, one before and one after an internal slot. With the slot empty the completed channel is exactly identity on the entire joint input. Insert X_A in that slot. The actual completed operation becomes X_M, while replacing the sequence by an identity service would put X_A on the data. On input |0>_A|0>_M the two data outputs are orthogonal. Thus even zero whole-call error does not bound an undeclared internal-intervention comb.

This is a representation failure, not a physical lower bound on computation. Seal that slot operationally, expose and certify it, or change the mechanism.

### 3.2 Arbitrary bath interventions cannot be harmless at an open entangling cut

Let a unitary macro have completed closure QP=G_A tensor W_M. P is its prefix at an internal cut. An arbitrary bath unitary R inserted there gives

\[
Q(I\otimes R)P=(G\otimes W)P^\dagger(I\otimes R)P.           \tag{8}
\]

Its data action is still exactly G for all joint inputs and every R if and only if

\[
P^\dagger(I_A\otimes\mathcal B(M))P
=I_A\otimes\mathcal B(M).                                  \tag{9}
\]

For finite tensor factors, the normalizer of this full matrix factor consists of product unitaries, so P=P_A tensor P_M. One proof uses the innerness of automorphisms of a full matrix algebra: remove the implementing M unitary; the remainder commutes with all I tensor B and hence lies in B(A) tensor I. This is the unitary no-signalling rigidity underlying Beckman et al., Theorem 7.

Therefore a prefix that entangles data with the mediator cannot be exactly insensitive to **all** bath interventions at that cut. A bus-mediated entangling gate with no direct source-source interaction cannot have such protection at every time of a differentiable implementation: if every prefix is a product, its generator is data-only plus bath-only, and the allowed one-source controls cannot generate an entangling data gate.

This no-go is deliberately strong in its adversary. It does not prohibit bounded residual noise, a correctable local error space, known commuting bath dynamics, error correction, or a changed port. It tells us why arbitrary bath-only dynamics is free at a **closed** boundary but generally must be included in the fault contract during an **open** mediated contact. Moving to an interaction picture does not make a noncommuting open-loop bath Hamiltonian harmless.

## 4. Forced-subset resummation at the certified boundaries

Consider N sequential macros on a fixed declared circuit, with arbitrary bath-only channels between them. Purify the latter and all actual records to isometries. Macro j acts only on its specified data support Q_j and complete M; spectators are untouched. Write its actual dilation as

\[
U_j=C_j+F_j,\quad C_j=G_j\otimes W_j,\quad
\|F_j\|\le\eta_j,\quad \|U_j\|=\|C_j\|=1.                 \tag{10}
\]

Equation (5), a bounded residual Hamiltonian integral, or another full-interface derivation can supply eta_j. The support premise is separate from the norm premise. Weak collective errors on spectators cannot be relabeled a one-qubit fault.

Expand the causal product multilinearly, using C_j or F_j at each macro. Let T_F be the amplitude with *exactly* fault set F. For a prescribed set S, let

\[
E(S)=\sum_{F\supseteq S}T_F.                               \tag{11}
\]

Linearity replaces every unmarked factor C_j+F_j by the **actual** U_j. Hence E(S) is the same circuit with F_j at j in S and actual U_j everywhere else. All intervening bath-only dynamics and declared strategy isometries have norm one. Therefore

\[
\boxed{\ \|E(S)\|\le\prod_{j\in S}\eta_j.\ }               \tag{12}
\]

This statement holds for every finite N with constants independent of N, bath size, bath correlation time, and bath-only strength. It includes initially correlated inputs and noncommuting bath coefficients. It also holds uniformly after arbitrary causal CPTP interventions at the **declared boundaries**, by purifying the intervention and keeping its dilation as a contraction. Postselected normalized branches are not contractions and are not licensed by this argument.

For record-adaptive controls, include the actual classical history as a direct-sum computational control register and require (10) uniformly on every past-history block, with the declared target G_j(h). Classical decision/record corruption and shared controller faults belong to the physical fault model. A record used as a trusted command cannot also be placed inside M and allowed arbitrary free corruption: flipping that record followed by a perfect controlled gate can corrupt fresh data without another F_j. Coherent control registers belong to Q_j if their quantum information is part of the computation. A classical-label test cannot certify their off-diagonal phases.

The product bound (12) is exactly the local coherent-noise condition used by Aliferis--Gottesman--Preskill, Section 11. It is not a stochastic Pauli law and eta is an amplitude. The elementary resummation proof is standard; it is included to show precisely what closure must deliver.

### 4.1 The signed-channel version can be the stronger representation

When a full actual memory/record channel is supplied directly, one need not choose a Stinespring gauge. Suppose

\[
\mathcal N_j=\mathcal C_j+\mathcal F_j,\quad
\mathcal C_j=\mathcal G_j\otimes\mathcal R_j\text{ CPTP},\quad
\|\mathcal F_j\|_\diamond\le q_j.                            \tag{13}
\]

The same expansion at ket-and-bra channel level gives

\[
\left\|\sum_{F\supseteq S}\mathcal T_F\right\|_\diamond
\le\prod_{j\in S}q_j.                                     \tag{14}
\]

The fault maps may be signed/non-CP. They are never assigned positive fault probabilities. Equation (14) follows because actual unmarked channels and all deterministic inserted channels have diamond norm one. It covers actual preparations, resets and measurement records once their full joint input/output and spatial support satisfy (13). A reduced channel obtained by discarding a returning environment is insufficient. The corresponding strategy-norm statement follows by absorbing any causal tester into these same contractions.

This version is useful when a direct joint-channel certificate avoids a square-root dilation conversion. It also agrees with the receiving interface in Astra N951. Its assumptions do not follow just from a small reduced-data error.

### 4.2 What propagation is, and is not, bounded

A source fault can remain entangled with M. At every subsequent good macro G_j tensor W_j, the bath component evolves only on M. It cannot place a new source error on another qubit. The old source/control operator propagates only through the intended quantum and classical circuit gates. Therefore a new mediated transfer to data outside that ideal light cone requires another F_j. This is the reusable fault-containment statement. The arbitrary joint testers used to establish the norm statement (12) may intentionally connect data and memory; they do not themselves satisfy a locality promise. For the containment conclusion, all such connecting operations must be declared circuit locations or included source/control faults.

It does not bound source error weight independently of the intended circuit: a CNOT fanout spreads one X fault to arbitrarily many targets even with a perfect, fully closed bus. Fault-tolerant gadgets, scheduling, syndrome extraction and a good-implies-correct proof are still required. Likewise a small per-call eta does not give a workload error independent of N; coherent Z overrotations can accumulate to an order-one logical error.

At fixed-size receiving gadgets, the standard inclusion-exclusion identity bounds the sum of paths with at least s faulty locations among a locations by

\[
B_s=\sum_{r=s}^{a}(-1)^{r-s}{r-1\choose s-1}
\sum_{|S|=r}E(S),\qquad
\|B_s\|\le {a\choose s}\eta^s(1+\eta)^{a-s}.                \tag{15}
\]

The size a is the actual gadget size, not the whole computer volume. All source idles, control, preparation, measurement, reset and actual recovery locations must be included. Overlapping extended rectangles and rejected-ancilla preparations need the established receiver's own analysis. No stochastic threshold number is transferred to eta or q.

### 4.3 Overlapping contact and source-idle windows: a separate norm adapter

A source-support compiler may move isolated spectator-idle faults past ideal mediator pulses because those ideal pulses act trivially on the spectator and external bath. With several interleaved faults sharing the same bath, that argument establishes an error **span**, not coefficientwise factorization or a bound on merged fault coefficients. In particular it does not prove the sequential product premise (10) for an arbitrarily grouped physical window.

One can instead derive the forced-set condition on the original physical Hamiltonian. Suppose

\[
H_\lambda(t)=H_0(t)+\sum_{j=1}^N\lambda_j V_j(t),\qquad
\lambda_j\in[0,1],\qquad
\eta_j=\hbar^{-1}\int\|V_j(t)\|\,dt<\infty.                 \tag{16a}
\]

Each declared V_j has its actual local source/control support, may involve the shared bath, and may overlap other windows. The independent strength parameters are proof devices, not independent stochastic causes or experimentally available switches. Their dependence is affine as displayed; a shared failure with a different support must be included honestly. H_0 includes the specified ideal bus controls and any common background, with defined unitary propagators. Bounded V_j and the interaction-picture Duhamel expansion suffice even when H_0 itself is unbounded.

Let R_j set lambda_j to zero in the propagator family and Delta_j=I-R_j, evaluated with the other parameters unchanged. The exact finite-difference expansion has terms

\[
T_F=\Bigl(\prod_{j\in F}\Delta_j\Bigr)
\Bigl(\prod_{j\notin F}R_j\Bigr)U_{\boldsymbol1},\qquad
\sum_{F\supseteq S}T_F=\Bigl(\prod_{j\in S}\Delta_j\Bigr)U_{\boldsymbol1}.
                                                                    \tag{16b}
\]

All couplings outside S remain ON in the right side. Express the selected finite difference as the integral of the mixed derivative in lambda_S. Repeated Duhamel differentiation inserts each selected V_j once. The |S|! time orderings partition the integration cube; every propagator segment at every intermediate lambda is unitary. Thus the norm is at most product eta_j, with no factorial or unmarked-volume factor. Declared boundary interventions can be included as fixed isometries. Their open slots do not license moving an uncontrolled intervention inside an otherwise sealed macro.

This is the standard microscopic local coherent-noise bound, and the same mixed-derivative mechanism is explicit in Astra N951. It is logically separate from a source-support compiler: the latter must establish that each completed T_F belongs to the claimed fault-support span, using the actual ideal controls and the specified contact/idle support. Both statements are required. Arbitrary unbounded **bath-only dynamics between closed macros** can be included in H_0; an H_0 with uncontrolled noncommuting open-loop bus dynamics need not retain the ideal closure.

## 5. Causal normalization of a good comb

The preceding local derivation supplies a multitime object with its boundary slots retained. A second issue arises after error correction: the coherent good sum need not itself be a normalized channel, much less an internally causal normalized service. The following projection solves the normalization problem **when factorization has been proved at the comb level**.

Use a finite ordered set of interface rounds. Let C be the actual deterministic comb on a data rail D and a common memory/record rail B. These rails include their input/output ports at the specified rounds; a rail can have trivial ports at some rounds. Let U be a specified deterministic data comb. Suppose a Hermiticity-preserving decomposition is established as a multilinear comb identity

\[
\mathfrak C=\mathfrak U\otimes\Lambda+\mathfrak B,
\qquad \|\mathfrak B\|_{\rm str}\le\beta.                  \tag{16}
\]

Lambda need not be positive or normalized. The norm is the complete strategy distinguishability norm: supremum of the output trace norm after compatible deterministic causal testers, arbitrary test memory and references. The factorization in (16) means equality for all insertions at the declared slots, not just for the one circuit used during an endpoint test.

Choose any fixed deterministic causal tester T closing only the data rail, with all its measurement outcomes discarded, so T(U)=1. An explicit choice prepares a fixed dummy state at each incoming data port and discards each outgoing data port, with timing respected. Define

\[
\mathfrak R=\mathsf T_D(\mathfrak C),\qquad
\mathsf P(\mathfrak X)=\mathfrak U\otimes\mathsf T_D(\mathfrak X).
                                                                    \tag{17}
\]

R is a deterministic causal memory comb: it is obtained by physically wiring a deterministic tester into a deterministic comb. All actual common record ports remain at their original rounds. P is a deterministic causal supermap, a norm contraction, and P(U tensor Lambda)=U tensor Lambda. Consequently

\[
\mathfrak C-\mathfrak U\otimes\mathfrak R
=\mathfrak B-\mathsf P(\mathfrak B),\qquad
\boxed{\ \tfrac12\|\mathfrak C-\mathfrak U\otimes\mathfrak R\|_{\rm str}
\le\beta.\ }                                                   \tag{18}
\]

The norm contraction needs no assumed multiplicativity theorem. Any final tester following P can simulate the fixed U and the dummy tester internally, so it is a valid tester for the original X. This directly proves ||P(X)||_str<=||X||_str. Idempotence follows from T(U)=1.

The actual-input reference and the returning memory can be correlated. Equation (18) is a complete norm estimate on the process, not a state-factorization assertion. R generally has a new, code- and tester-dependent record law. It is a mathematical comparison comb, not an implemented extra recovery, fresh preparation, or a new free resource.

If the ideal data operation is controlled only by **past actual classical records**, the same construction works with a causal copying wire for those records: extract the memory comb using a fixed dummy data strategy and reinsert the specified record-controlled ideal data service. The resulting P is still a deterministic idempotent supermap on the declared controlled-good family. This extension requires the record-dependent ideal control itself to be causal. Quantum controls cannot be copied in this way and must remain in the data interface or receive a separately proved construction.

### 5.1 Amplitude tails and signed channel tails are different

Equation (18) uses a **channel/comb** remainder beta. If instead, for every coherent tester dilation, an amplitude decomposition W=W_good+B_a is known with ||B_a||<=b and a comb-compatible good amplitude, then

\[
\|\operatorname{Ad}_W-\operatorname{Ad}_{W_{\rm good}}\|_{\rm str}
\le b(2+b).                                                    \tag{19}
\]

Indeed the difference is B_a(.)W^dagger+W_good(.)B_a^dagger, and ||W_good||<=1+b. The causal projection then gives half-strategy discrepancy at most b(2+b). A direct signed-channel tail can avoid this conversion. An endpoint operator bound on one W does not by itself prove the uniform tester bound or the comb-compatible good part needed in this paragraph.

### 5.2 Why endpoint polar normalization can break timing

There are two memory input qubits, at times 1 and 2, with their outputs due at those respective times. Let the actual memory unitary be I and make the valid endpoint decomposition

\[
I=A_0+B,\qquad A_0=I+\tfrac{20i}{99}{\rm SWAP},\quad
B=-\tfrac{20i}{99}{\rm SWAP}.                                \tag{20}
\]

The bad amplitude norm is 20/99. Polar normalization gives

\[
A=\frac{99I+20i\,{m SWAP}}{101}.                            \tag{21}
\]

With the first input |0>, the first output has |1> probability zero if the *future* second input is |0>, and 400/10201 if it is |1>. A is therefore not a causal two-round memory comb. Tensoring an independent logical data identity changes nothing. This counterexample concerns the general endpoint normalization lemma; it is not asserted to be a particular physical fault-path decomposition. The original lemma's endpoint channel conclusion remains correct.

Construction (17) instead returns a causal memory reference, because its normalization is a deterministic network operation. The new requirement is stronger good-part factorization at every interface that remains open.

## 6. Essential physical and control conditions

The following are scientific premises, not acquired device claims.

* **All-state admitted support.** Later ports must satisfy the closure identity on every state reachable under the admitted bath, including leakage or loss flags if those states are admitted. A Pauli action defined only on an ideal two-level subspace cannot protect a leaked mediator. A qualified replacement/continuation is an additional operation.
* **Physical source locality.** Macro j and its residual have the declared Q_j support. Crosstalk, always-on source-bath terms, control broadcast and hidden future source contacts are charged at their actual supports. A norm-small collective error is not a local error.
* **Open-contact exposure.** Arbitrary bath-only dynamics between closed macros is harmless. Noncommuting bath dynamics during open contacts belongs in eta_j or a separately proved correctable fault space. Known commuting dynamics or accurately tracked controls can change that contract, but no free interaction-picture cancellation is assumed.
* **Acquired source/control rails.** All coherent selectors used by the computation are included. Classical controls are actual retained records, with fault assumptions on their acquisition, retention, processing and delivery. A corrupt decision controlling many gates is not automatically one benign data fault.
* **Supply and readout.** Preparations, reset, measurement, syndrome extraction and data idles have their own full joint local contracts. Freshness means independence from the currently unknown data and returning memory to the specified allowance. Memory reuse does not remove entropy-supply or injection costs.
* **Timing.** Only certified boundaries are available to arbitrary external intervention. A longer held source idle has its own exposure. A single serial bus can increase circuit depth and idle error; no parallel scheduling or throughput advantage follows from its small controlled width.
* **Budgets.** Algebraic representation error, macro acquisition/solver error, physical fault strength, omitted large-support processes, recovery approximation and total workload error remain distinct. Uniform local strength supports an appropriate threshold theorem only after the full receiving circuit is supplied.

## 7. Strong conventional comparators and actual source scope

Aliferis, Gottesman and Preskill, [quant-ph/0504218v3](https://arxiv.org/abs/quant-ph/0504218), Section 11 defines exactly the forced-subset amplitude norm in (12), treats an arbitrary shared bath, gives inclusion-exclusion and the threshold receiving conditions. Their source explicitly distinguishes amplitude from stochastic probability and leaves ancilla-rejection complications outside the displayed proof. Our closure construction is an adapter to this framework, not a new non-Markovian threshold theorem. Direct local source gates satisfying the same model remain the strongest comparator and can avoid a mediator's extra contacts and serial latency.

Terhal and Burkard, [quant-ph/0402104](https://arxiv.org/abs/quant-ph/0402104), supplies earlier coherent fault-path and error-spread ancestry; the portions read concern its model and sparse-path proof. AGP explicitly relaxes the older bath-locality restrictions. Kretschmann, Schlingemann and Werner, [quant-ph/0605009](https://arxiv.org/abs/quant-ph/0605009), provides the dimension-independent general Stinespring continuity comparison. Our linear bound (7) uses an extra all-input unitary promise and does not overrule its square-root regime.

Chiribella, D'Ariano and Perinotti, [0712.1325](https://arxiv.org/abs/0712.1325), gives combs as causal channels-with-memory and their normalization constraints. Gutoski, [1008.4636v4](https://arxiv.org/abs/1008.4636), supplies the strategy distinguishability norm. Beckman et al., [quant-ph/0102043](https://arxiv.org/abs/quant-ph/0102043), Theorem 7 supplies the unitary causality ancestry. The projection proof (17)-(18) is derived here directly from causal wiring and contractivity.

Astra N951 current capsule, governing `FINITE_CONTROL_COMPILER.md` and actual `SOURCE_EXPOSURE.txt` were read. Its scope is a finite-control, shared-bath fault-path compiler; current gaps retain external correctness/physical acquisition/priority as unknown. It contains a related signed-channel selected-subset bound, unmarked-operation resummation, and a completed-channel dummy-input normalization. Its finite-key theorem is not imported as a premise here. We extend the normalization argument at the explicitly retained comb interface and supply an approximate algebraic-closure route; no source-reported internal review becomes our independent review. Exact current source/version details are in `SOURCE_READ_SCOPE.json`.

## 8. Executable evidence and remaining reach

`reusable_algebra_checks.py/json` checks exact rational-complex algebra, finite complete-record processes and the counterexamples above. It is an author check, not proof by finite sampling or an independent review. No floating-point quantity is labeled an enclosure or a device error.

The construction makes it possible to state a reusable mediated computing interface in the same local coherent-noise language as a conventional fault-tolerant circuit, while allowing the mediator's bath to retain unrestricted quantum memory between calls. It also supplies a causal normalized comparison when all retained records and intervention slots matter. It does not acquire a physical low-noise macro, a fault-tolerant source receiver, scalable supply or a favorable workload cost. Those are now separate explicit interfaces, rather than hidden consequences of a small memory register or of endpoint fidelity.
