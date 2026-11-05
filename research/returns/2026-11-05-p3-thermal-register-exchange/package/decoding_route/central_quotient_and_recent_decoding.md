# Recent decoding comparisons, coherent polymer preparation, and a central-sector bypass

## Status and scope

This note supplies three results for the constructive exchange. It accepts P1's decoder-history compiler, its BDL instantiation, its unknown-qubit loading theorem, and its specified passive bath theorem at their declared scopes.

1. The full-codeword decoder used by QD-HDQI has a concrete, information-theoretic obstruction on the actual BDL physical check coordinates: a linear packing of bounded-weight check relations makes its successful-decoding/postselection probability exponentially small at every fixed positive inverse temperature.
2. The accepted low-activity polymer compiler can be lifted constructively to an efficient **canonical thermofield double** preparer. This uses coherent Markov transitions and a uniformly gapped annealing path; an ordinary classical sampler alone is not silently treated as a coherent preparation circuit.
3. Algebraic relative transduction admits an exact **central-sector projection** implementation. It can bypass a relative decoder entirely. In particular, it gives explicit bounded-strength, bounded-degree, geometrically local two-dimensional noncommuting Hamiltonians whose canonical TFD is preparable in polynomial time at every fixed finite inverse temperature.

The third result is a useful stronger compatible method. It does not prove generic two-dimensional Gibbs sampling or passive quantum storage for the new target family. Its thermodynamics remains that of a one-dimensional source restricted to one parity sector. No reduction from the burst model or from the intervention-stream contract is used.

## 1. Exact primary-source conditions

The supplied arXiv HTML of 2610.06667v2 terminates at Theorem 4.3 because of a conversion failure. Its complete versioned PDF was retrieved and read. The complete PDF of 2610.03566 was also retrieved. Full-text retrieval copies were used for the analysis; the research package cites the primary URLs rather than redistributing those papers.

### 1.1 QD-HDQI

Piveteau, Quek and Franco Garrido, [*Gibbs state preparation through quantum decoding*, 2610.03566v1](https://arxiv.org/pdf/2610.03566), Theorem 4.1, considers

\[
H=\sum_{i=1}^{m}(-1)^{y_i}v_iP_i,\qquad v_i\ge0,
\]

with commuting Pauli terms. Let \(B\) have the actual indexed Pauli labels as columns. The code to decode is the **relation code** \(C=\ker B\). It is not the quantum code's physical-error decoder. The decoder receives codewords over independent pure-state channels with

\[
p_i=\tfrac12[1-\operatorname{sech}(\beta v_i)]
\]

or, for a classical decoder, the corresponding binary symmetric channels. If its failure probability is \(p_{\rm fail}\), the theorem requires efficient decoding and

\[
(1-p_{\rm fail})^{-1}=\operatorname{poly}(m).
\]

Its error guarantee is

\[
\mathbb E_{y\sim\operatorname{Unif}(\mathbb F_2^m)}
\|\widetilde\rho_y-\rho_{\beta,y}\|_1
\le6\sqrt{p_{\rm fail}}.
\]

The averaging is over all Hamiltonian sign strings. It is not automatically an error bound for a fixed frustration-free ferromagnetic sign choice. The paper's general Theorem 3.1 additionally exposes a coherent-interference term \(\alpha\); low ordinary decoding error does not alone remove that term for a fixed sign string. Its Gibbs normalization factor is

\[
Z'_\beta=\frac{Z_\beta}{2^n\prod_i\cosh(\beta v_i)},
\]

and the sign-averaged argument also controls \(|Z'_\beta-1|\).

The classical dequantization (Algorithm 3 and Theorems 5.1–5.2) samples a subset of physical checks by independent Bernoulli probabilities

\[
t_i=\tanh(\beta v_i)
\]

and rejects unless the selected columns are linearly independent. It then samples an affine stabilizer eigenspace by Gaussian elimination. If \(p_{\rm dep}\) is the probability of dependence, its mean runtime after preprocessing is

\[
O\!\left(\frac{m+n^3}{1-p_{\rm dep}}\right),
\]

and its stated trace-norm error bound, averaged over all signs, is \(2p_{\rm dep}\). This is a precise algorithmic comparator; it is not a universal efficient sampler for all commuting Hamiltonians.

For P1's convention \(H=\sum_a J_a(I-S_a)/2\), drop the scalar shift and set \(v_a=J_a/2\). Thus the quantities relevant below are \(t_a=\tanh(\beta J_a/2)\).

### 1.2 Relative decoding

Shang, Wang and Stilck França, [*Quantum Gibbs State Preparation via Relative Decoding: From Fast-Mixing Sources to Broader Target Classes*, 2610.06667v2](https://arxiv.org/pdf/2610.06667v2), requires matched indexed term magnitudes and:

\[
\Sigma_A=\Sigma_B,\quad K_A=\ker A\subseteq K_B=\ker B,
\]

together with matching signed-relation phases on \(K_A\). A coherent relative decoder recovers \(Az\) from \(Bz\) throughout its certified support. The relative distance is

\[
d_{A\to B}=\min\{|c|:c\in K_B\setminus K_A\}.
\]

Theorem 6.1 takes a supplied **canonical TFD** of the source, not merely a source Gibbs-state sampler. For \(\Lambda\ge\|H_A\|\), \(\ell=\log(1/\eta)\), a sufficient degree condition is

\[
D+1\ge\beta\Lambda+\sqrt{2\beta\Lambda\ell}+\ell/3,
\qquad D\le D_{\rm dec},\qquad 2D_{\rm dec}<d_{A\to B}.
\]

The total target TFD trace-distance error is at most

\[
\delta_{\rm src}+2\eta+\delta_{\rm circ}.
\]

The paper's explicit chain construction, Section 8/Theorem 8.1, supplies a constant inverse-temperature window. It does not establish a BDL-specific source and quotient decoder. Conversely, the theorem does not exclude another source, another approximation certificate, or the exact projection method below. A commuting BDL source alone also cannot generate a noncommuting target through this theorem, because their indexed anticommutation matrices must agree.

## 2. A concrete QD-HDQI obstruction on physical check coordinates

### Proposition 1: disjoint relations obstruct complete codeword decoding

Let \(C\subseteq\mathbb F_2^m\) contain \(L\) nonzero vectors \(c_1,\ldots,c_L\) with pairwise disjoint supports and \(|c_j|\le w\). Transmit a uniformly random codeword through independent pure-state channels

\[
|\psi_0^{(i)}\rangle=\sqrt{1-p_i}|0\rangle+\sqrt{p_i}|1\rangle,
\qquad
|\psi_1^{(i)}\rangle=\sqrt{p_i}|0\rangle+\sqrt{1-p_i}|1\rangle.
\]

Suppose their overlaps obey

\[
\langle\psi_0^{(i)}|\psi_1^{(i)}\rangle\ge t_*>0.
\]

Then every decoder, including an unbounded quantum decoder, has full-codeword success probability

\[
P_{\rm succ}^{\rm opt}(C)
\le \left[\frac{1+\sqrt{1-t_*^{2w}}}{2}\right]^L.
\tag{1}
\]

**Proof.** The disjoint vectors are independent. Choose a complementary subspace to their span and reveal its message coordinate to the decoder. This can only improve success. Undo the known codeword by bit flips. What remains is a product of \(L\) independent, equiprobable binary pure-state discrimination problems. The two states in block \(j\) have overlap

\[
a_j=\prod_{i\in\operatorname{supp}(c_j)}
\langle\psi_0^{(i)}|\psi_1^{(i)}\rangle
\ge t_*^w.
\]

Helstrom's binary optimum is \(s_j=(1+\sqrt{1-a_j^2})/2\). Optimal success for independent product ensembles multiplies: product measurements attain the product, and tensoring feasible dual operators of the minimum-error discrimination semidefinite programs proves the reverse inequality. Therefore \(P_{\rm succ}\le\prod_j s_j\), proving (1). \(\square\)

For QD-HDQI, the channel overlap is exactly \(\tanh(\beta v_i)\). Hence \(L=\Omega(N)\), bounded \(w\), fixed \(\beta>0\), and \(v_i\ge v_*>0\) imply exponentially small success. This violates its polynomial postselection requirement independently of the sign-averaging issue.

The classical rejection sampler and USD have the simpler bound

\[
\Pr(S\text{ independent})
\le\prod_{j=1}^{L}
\left(1-\prod_{i\in\operatorname{supp}(c_j)}t_i\right)
\le(1-t_*^w)^L.
\tag{2}
\]

Indeed, selecting all coordinates of any relation makes the set dependent, and these events are independent for disjoint supports.

### Actual BDL local relations

The following uses the physical RX/RZ coordinates of [BDL 2605.10943v1](https://arxiv.org/html/2605.10943v1), rather than an arbitrary new stabilizer basis.

In an RX step, choose an old qubit \(q\) adjacent to at least two old Z checks. Its local graph \(Y_q\) is two subdivided stars joined at their leaf endpoints. Two arms produce a cycle \(e_q\). Assign coefficient one to that cycle's physical q-block edge/Z-check coordinates. For each old X neighbor \(x\), the included cycle in \(Y_x\) bounds a local two-chain \(f_x\), because \(H^1(C_x)=0\). Thus \((f_x,e_q)\) has zero physical boundary and is a physical Z-check relation.

The source definitions are Section 3.2.2, equations (61)–(72), especially the \(Y_q\) construction around (66); the local vanishing first cohomology is in the proof of Lemma 3.8 around (77)–(79). The block size \(\ell\) is fixed, so the relation weight is bounded by a constant depending on \(\ell\) and bounded incidence degree. A bounded-overlap packing gives a linear number of disjoint relations. The positive density of eligible qubits can be taken from interior edges of the fixed local square grids once \(\ell\) is chosen large enough, for example \(\ell\ge5\).

The subsequent RZ step is RX on the dual complex. Its degree-zero representative sends each old coefficient to the all-ones vector in its vertex block, as in equation (82) and the dual construction in Section 3.2.5, equations (88)–(95). This lifts each relation, preserves disjointness of different coordinate supports, and multiplies its weight by only a fixed constant. The number of physical qubits changes by fixed factors at fixed \(\ell\). Thus the final alternating family has \(L=\Omega(N)\) disjoint bounded-weight physical check relations.

Equations (1)–(2) therefore apply to the recent complete relation-code decoding and USD procedures on BDL. They do **not** obstruct P1's accepted history-polymer sampler, a matroid method with separately proved hypotheses, or Gibbs sampling generally. A disjoint collection of constant-size redundant stabilizer blocks already illustrates why complete relation-code decoding can be hard while Gibbs preparation is easy.

### Proposition 2: which relations a relative source must absorb

Let

\[
K_{\le w}:=\operatorname{span}\{c\in K_B:|c|\le w\}.
\]

For every \(K_A\subseteq K_B\),

\[
d_{A\to B}>w\quad\Longrightarrow\quad K_{\le w}\subseteq K_A.
\tag{3}
\]

If \(K_{\le w}=K_B\), then \(d_{A\to B}>w\) forces \(K_A=K_B\). Under matching commutation and relation phases, equality of kernels gives a termwise Clifford equivalence after adding idle qubits if necessary.

**Proof.** If a relation of weight at most \(w\) is absent from \(K_A\), it is a candidate in the minimization defining \(d_{A\to B}\). This proves (3). When kernels are equal, \(Az\mapsto Bz\) is a well-defined isomorphism of the generated Pauli-label subspaces. Equal commutation matrices make it symplectic on those subspaces. A symplectic extension to padded full Pauli spaces gives a Clifford, while phase compatibility supplies the required Pauli sign correction. Polynomial-time symplectic elimination constructs it. \(\square\)

For actual BDL this proves that a linear-distance source must absorb the explicitly constructed local relations. **This note does not assert that all BDL relations are generated by bounded-weight relations.** That additional premise has not been established. The stronger Clifford-equivalence conclusion is stated only under the explicit spanning premise.

## 3. Coherent preparation from the accepted polymer compiler

### Proposition 3: canonical TFD preparation

Assume the accepted history compiler: unique valid histories, bounded-degree primal graph, nonzero connected components with additive energy \(E(\gamma)\ge a|\gamma|\), polynomial enumeration at logarithmic cutoff, and the accepted low-activity condition. Then the Gibbs state of the associated commuting stabilizer Hamiltonian has a canonical TFD preparable by a quantum circuit of size polynomial in \(N\) and \(1/\epsilon\), with the same supplied Hamiltonian/control premises.

This is an algorithmic corollary of the accepted polymer analysis and the coherent Markov-chain annealing machinery of [Somma, Boixo, Barnum and Knill, PRL 101, 130504 (2008), arXiv:0804.1571](https://arxiv.org/pdf/0804.1571). It does not assume a free conversion of sampled classical probabilities into amplitudes.

**Construction.** Choose a polymer cutoff making the probability of any excluded polymer at most \(\tau=O(\epsilon^2)\), and enumerate the \(K=\operatorname{poly}(N,1/\epsilon)\) retained polymers. Write configurations as compatible collections \(\Gamma\), and define

\[
\pi_u(\Gamma)=\frac{u^{|\Gamma|}\prod_{\gamma\in\Gamma}w_\gamma}{Z_u},
\qquad 0<u\le1.
\]

Every configuration contains at most \(M\) polymers, where \(M\) is the number of history variables. Scale only activities, not the constraint relation or physical Hamiltonian. The same path-coupling proof applies for every \(u\le1\): decreasing birth probabilities preserves its influence bound. The explicit heat bath therefore has spectral gap at least \(3/(4K)\), uniformly along this path. Reversibility and positivity follow because a heat-bath update is a conditional-expectation projection; the random-scan chain is their average.

The chain has at most \(K+1\) possible next configurations from any state, and their probabilities are computed from compatibility and \(uw_\gamma/(1+uw_\gamma)\). Consequently its coherent transition isometry is constructible in polynomial time, as required by the quantum-walk theorem. Its stationary quantum state is

\[
|\pi_u^{1/2}\rangle=\sum_\Gamma\sqrt{\pi_u(\Gamma)}|\Gamma\rangle.
\]

Choose \(u_0\) so \(u_0K\le c\epsilon^2\). Since \(w_\gamma\le1\),

\[
Z_{u_0}\le\prod_\gamma(1+u_0w_\gamma)\le e^{u_0K}.
\]

The empty configuration is therefore within \(O(\epsilon)\) pure-state trace distance of the initial stationary quantum state.

For an explicit conservative annealing schedule, set \(\theta=\log u\) and \(R=\log(1/u_0)\). Differentiating the normalized stationary vector gives

\[
\left\|\frac{d}{d\theta}|\pi_{e^\theta}^{1/2}\rangle\right\|
=\tfrac12\sqrt{\operatorname{Var}(|\Gamma|)}\le M/4.
\]

With \(S\) equal logarithmic steps, ideal successive stationary-state projections fail with total probability at most \(M^2R^2/(16S)\). Take \(S=O(M^2R^2/\epsilon^2)\). Quantum-walk phase filtering implements each projection with polynomial cost: the phase gap is \(\Omega(K^{-1/2})\), and allocating error \(O(\epsilon/S)\) per projection gives total error \(O(\epsilon)\). The fixed data/zero-ancilla subspace is orthogonal to the unwanted zero-phase subspace, exactly as in the cited annealing construction. Repeating a flagged failed preparation has bounded expected overhead.

Reversibly combine each collection into its unique history, and use the accepted bijection to obtain

\[
\sum_s\sqrt{\pi_\beta(s)}|s\rangle
\]

up to the chosen error. Removing probability mass \(\tau\) costs \(\sqrt\tau\) in pure-state trace distance; this explains the squared truncation accuracy.

If the code has \(k\) logical qubits, let \(V_0\) be its ground encoder and \(V_s=F_s^\dagger V_0\). Prepare a logical Bell state \(|\Phi_k\rangle\), apply \(V_s\) to its physical half and \(V_s^*\) to its reference half coherently controlled by \(s\), then erase the syndrome register by coherently computing the physical stabilizer eigenvalues. The result is

\[
\sum_s\sqrt{\pi_\beta(s)}\,2^{-k/2}
\sum_{j=1}^{2^k}|v_{s,j}\rangle|v_{s,j}^*\rangle
=|\operatorname{TFD}_{H}(\beta)\rangle.
\]

The protected frame is computable by hypothesis; the second controlled frame is the complex conjugate of the first. Basis changes within a syndrome sector cancel under \(U\otimes U^*\), so the output is the canonical purification, not merely some purification.

This construction pays for enumeration, compatibility, reversible arithmetic, transition preparation, quantum filtering, controlled encoders, and coherent syndrome extraction. Compiling its polynomial circuit to local gates has polynomial routing overhead; no efficient constant-noise implementation is claimed without an additional control-noise contract. Coupling precision is also paid. For commuting coefficients, a perturbation \(\Delta E\) of the classical energy changes the canonical state by at most \(\beta\operatorname{osc}(\Delta E)/4\), since the normalized-amplitude derivative norm is \((\beta/2)\sqrt{\operatorname{Var}(\Delta E)}\). Thus \(\sum_a|\Delta J_a|=O(\epsilon/\beta)\) suffices.

## 4. Exact central-sector transduction

### Proposition 4: replace relative decoding by sector selection

Assume the algebraic hypotheses of the relative-decoding paper: matched indexed coefficients, equal commutation matrices, kernel inclusion, and matching relation phases. Let

\[
q=\dim K_B-\dim K_A.
\]

Then there are \(q\) independent commuting **central** source Pauli operators and a joint eigenspace projector \(P\) such that restricting \(H_A\) to \(P\) is Clifford-equivalent to \(H_B\), up to idle factors. Given the canonical source TFD, project its physical half by \(P\), apply the corresponding Clifford on physical and conjugate Clifford on reference, remove the fixed sector registers, and add or remove idle Bell pairs as needed to match the target representation. Conditioned on success, the output is exactly the canonical target TFD for every \(\beta\ge0\).

The success probability is

\[
p_\beta=\frac{\operatorname{Tr}(P e^{-\beta H_A})}
{\operatorname{Tr}(e^{-\beta H_A})}.
\tag{4}
\]

Independent repeated preparation costs \(1/p_\beta\) in expectation; with coherent source preparation and its inverse, amplitude amplification gives \(O(p_\beta^{-1/2})\) query dependence. Neither statement is a lower bound on all possible target-preparation methods.

**Proof.** Proposition B.7 of the relative-decoding paper proves that the kernel of \(Az\mapsto Bz\) lies in the radical of the source Pauli space. Choose a basis \(c_j\) for \(K_B/K_A\). Its nonzero source labels \(Ac_j\) are independent and central. Their required eigenvalues are fixed by the corresponding target signed relations; the phase hypothesis ensures consistency. Clifford symplectic reduction sends these central generators to independent Z operators. In their selected eigenspace the indexed source Pauli algebra has exactly the target relations and commutation form. A second symplectic reduction identifies the target representation, with uniform idle multiplicities.

Since \([P,H_A]=0\), projection of

\[
\operatorname{vec}(e^{-\beta H_A/2})/
\sqrt{\operatorname{Tr}(e^{-\beta H_A})}
\]

onto the physical sector also selects the conjugate sector on the reference. After normalization it is the canonical purification of the restricted Gibbs operator. Clifford reduction on both copies therefore gives the claimed output. \(\square\)

For a source supplied only to trace-distance accuracy \(\delta\), conditioning can amplify error. A safe bound is \(O(\delta/p_\beta)\), rather than silently charging \(\delta\) only once. A known lower bound \(p_0\le p_\beta\) permits choosing \(\delta=O(p_0\epsilon)\). Taking \(O(p_0^{-1}\log(1/\epsilon))\) trials gives a finite failure-probability guarantee. Circuit inaccuracies and any metrology uncertainty must be included in this budget.

### Positive commuting source: temperature-independent codimension bound

Suppose both source and selected target sector are frustration-free commuting ferromagnetic systems with the same positive physical term energies. Parameterize source syndromes by a binary linear space \(C_A\); target syndromes form a codimension-\(q\) subspace \(C_B\subseteq C_A\). Then

\[
p_\beta=\pi_A(C_B)\ge2^{-q}
\quad\text{for every }\beta\ge0.
\tag{5}
\]

To prove this without a probabilistic monotonicity assumption, express source configurations as \(s=Lx\) and expand

\[
\exp\!\left(\sum_i K_i(-1)^{\ell_i\cdot x}\right)
=\prod_i\cosh K_i
\prod_i[1+\tanh K_i(-1)^{\ell_i\cdot x}],\qquad K_i\ge0.
\]

Every Fourier coefficient is nonnegative. Consequently every parity expectation is nonnegative. The indicator of \(q\) homogeneous target constraints is the average of \(2^q\) such parity characters, with its identity term equal to one. Equation (5) follows. Thus low-codimension central quotients are efficiently preparable at arbitrarily low fixed temperatures without a relative-distance decoder.

## 5. An explicit local two-dimensional noncommuting family at every fixed temperature

Let \(V\) be the \(L\times L\) square-grid vertices, \(N=L^2\). Choose a Hamiltonian path \(P\) snaking through rows and another path \(T\) snaking through columns. The source has two qubits \((q_v,c_v)\) per vertex and Hamiltonian

\[
H_A=\sum_v
\bigl(a_vX_{q_v}+b_vZ_{q_v}+d_vZ_{c_v}
+e_vZ_{c_v}Z_{q_v}\bigr)
+\sum_{(u,v)\in P} f_{uv}Z_{q_u}Z_{q_v},
\tag{6}
\]

where all coefficients are supplied and bounded in absolute value by \(J_0\). Viewed along \(P\), this is a bounded-strength nearest-neighbor chain of constant-size cells. The coefficients may have either sign. It is noncommuting whenever a nonzero X field meets a nonzero Z term.

Let \(F\in\mathbb F_2^{(N-1)\times N}\) be the edge-vertex incidence matrix of the tree \(T\). It has full row rank and

\[
\ker F=\operatorname{span}\{\mathbf1\}.
\]

Place a target qubit \(R_e\) at the midpoint of each \(T\) edge and set

\[
B_v=\prod_{e\ni v}Z_{R_e}.
\]

The target is

\[
H_B=\sum_v
\bigl(a_vX_{q_v}+b_vZ_{q_v}+d_vB_v+e_vB_vZ_{q_v}\bigr)
+\sum_{(u,v)\in P}f_{uv}Z_{q_u}Z_{q_v}.
\tag{7}
\]

Because \(T\) is a path, each \(B_v\) has weight at most two and \(B_vZ_{q_v}\) weight at most three. All interactions lie within a fixed neighborhood of a grid vertex or edge; density, degree and range are bounded. With all displayed terms present, the interaction graph contains a square-grid minor: \(P\) provides all horizontal grid edges, and \(q_u-R_{uv}-q_v\) supplies the vertical ones through \(T\). This is a genuinely two-dimensional local interaction layout, despite its source representation.

The only new central relation is

\[
\prod_vB_v=I.
\]

Prepare the source canonical TFD and measure

\[
C=\prod_vZ_{c_v}
\]

on its physical half. Keep outcome \(+1\). To compress the selected central sector, write \(c=F^Tr\). For a tree this has a unique solution \(r\) exactly when \(\sum_vc_v=0\). For a path the solution is obtained by prefix parity along the path; CNOT gates compute the edge bits and the final zero parity bit. Apply the same real Clifford on reference. The final parity registers are fixed zero and may be removed. Equations (6)–(7) are then exactly intertwined, and the output is the canonical target TFD.

### Success probability and complete preparation cost

For any vertex \(v\), \(X_{c_v}\) exchanges the two parity sectors and changes only two source terms. Hence

\[
\|X_{c_v}H_AX_{c_v}-H_A\|
\le \Delta_v:=2(|d_v|+|e_v|)\le4J_0.
\]

Weyl eigenvalue comparison on the parity-restricted blocks gives

\[
\frac{Z_-}{Z_+}\le e^{\beta\Delta_v},
\qquad
p_+\ge\frac1{1+e^{\beta\Delta_v}}
\ge\frac1{1+e^{4\beta J_0}}.
\tag{8}
\]

This does not use operator monotonicity of the exponential, which would be invalid in general. It compares eigenvalues and then traces.

Bergamaschi and Chen, [*Fast Mixing of Quantum Spin Chains at All Temperatures*, 2510.08533v2](https://arxiv.org/pdf/2510.08533v2), Corollary I.1, supplies precisely the canonical purification for (6), to trace distance \(\delta\), with circuit size \(s_{\beta,q}N\operatorname{polylog}(N/\delta)\) and depth \(d_{\beta,q}\operatorname{polylog}(N/\delta)\), using nearest-neighbor two-qubit gates and ancillas. Its constants depend on fixed temperature and fixed local dimension. Grouping each \((q_v,c_v)\) as a cell and rescaling the bounded interaction strength satisfies its hypotheses.

Let \(p_0=(1+e^{4\beta J_0})^{-1}\) and request source error \(O(p_0\epsilon)\). Parity measurement and path compression use \(O(N)\) CNOTs per copy, conservatively depth \(O(N)\), and \(O(N)\) qubits. Repetition gives expected gate cost

\[
O\!\left[p_0^{-1}\{s_{\beta,q}N\operatorname{polylog}(N/(p_0\epsilon))+N\}\right].
\]

A fixed trial cap adds a factor \(\log(1/\epsilon)\) for failure probability \(O(\epsilon)\). Storage, resets, ancillas, reference copy, local routing along the two paths, numerical precision, and control error are all explicit parts of this preparation. For every **fixed finite** \(\beta\), it is polynomial in system size and requested precision. There is no uniform-in-\(\beta\) efficiency claim as \(\beta\) grows with \(N\), and no intrinsic-bath realization of the preparation circuit is assumed.

This reaches all fixed temperatures by central-sector selection, whereas the paper's relative-decoding certificate for the same incidence-code construction has a fixed upper bound on \(\beta\). It constructs an actual stronger operation from compatible ingredients. Its Gibbs preparation does not imply fast mixing of a specified target bath. Conversely, it has not proved that any particular target bath mixes slowly.

### Validation

`verify_central_quotient.py` independently constructs a four-vertex source and target from row/column snake paths, verifies the exact matrix intertwining through \(c=F^Tr\), and compares conditioned source Gibbs matrices against directly exponentiated target Gibbs matrices. At \(\beta=0,0.2,1,3,8\), all algebraic residuals were zero and all state discrepancies were below \(7\times10^{-16}\). The sector probabilities obeyed (8). This is an implementation check; the asymptotic result is supplied by the proofs above.

## What this changes in the exchange

The recent complete-codeword QD-HDQI sampler does not supply BDL's cold loader on its actual check coordinates: its required success probability fails quantitatively. Relative decoding is more flexible but requires absorbing the local relation space and supplying a true coherent source; neither requirement is satisfied merely by naming BDL's physical-error decoder.

The accepted compiler nevertheless supplies the stronger coherent source by a completed constructive route. Once a source is available, relative decoding is not always the right missing operation. Low-rank central sector selection can replace it, and the local two-dimensional example gives an explicit cold noncommuting consequence. All these conclusions retain their preparation and access costs. None changes the accepted BDL passive bath theorem or promotes a low-rank disguised chain into a generic two-dimensional quantum memory.
