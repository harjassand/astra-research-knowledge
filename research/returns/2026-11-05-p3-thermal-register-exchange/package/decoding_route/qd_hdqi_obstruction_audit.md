# Independent audit: QD-HDQI on the actual BDL physical checks

## Conclusion

At every sufficiently large even depth of the actual fixed-refinement BDL random-embedding family, the relation code of the physical Hamiltonian checks contains \(L\ge a_\ell N\) nonzero, pairwise disjoint relations of weight at most \(w_\ell\). The constants depend on the fixed block parameter, not on depth or coupling values.

For every fixed \(\beta>0\) and \(J_i\ge J_{\min}>0\), the full-codeword decoder required by QD-HDQI consequently has optimal success probability

\[
1-p_{\rm fail}\le
\left[\frac{1+\sqrt{1-t_*^{2w_\ell}}}{2}\right]^{L}
\le \exp[-L t_*^{2w_\ell}/4],
\qquad t_*=\tanh(\beta J_{\min}/2)>0.
\tag{A}
\]

This is an information-theoretic statement about that specified decoding operation, including collective quantum measurements. Its ordinary repeat-until-success cost is exponential; amplitude amplification would still be exponential. It is not a lower bound on Gibbs preparation generally, and does not obstruct the accepted history sampler.

## 1. Exact paper interface: code, channel, prior and postselection

The complete primary PDF [Piveteau–Quek–Franco Garrido, arXiv:2610.03566v1](https://arxiv.org/pdf/2610.03566) was checked directly.

* Definition 2.1, equation (38), defines the Pauli-label matrix \(B\) by putting the **physical Hamiltonian Pauli terms in its columns**. Its symplectic code is explicitly \(C_H=\ker B\). Its dual \(C_H^\perp=\operatorname{im}B^T\) is used in the Fourier/codeword-to-syndrome transformation; it is not the codeword-decoding target.
* Definition 2.2, equation (44), defines
  \[
  \operatorname{PSC}[p](x)=\sqrt{1-p}|x\rangle+\sqrt p|1-x\rangle.
  \]
* Lemma 4.1, equation (77), and Theorem 4.1, equation (120), set \(p_i=(1-\operatorname{sech}(\beta v_i))/2\) for \(H=\sum_i(-1)^{y_i}v_iP_i\). Equations (86)–(87) remove known phases by unitary basis changes, giving precisely these product channels, up to physically irrelevant codeword phases.
* Section 2.2 explicitly declares uniformly distributed transmitted codewords. Section 3.3, equation (59), defines the decoder's success as \(|C_H|^{-1}\sum_c\langle\Psi_c|\Lambda_c|\Psi_c\rangle\). The coherent algorithm also prepares the uniform superposition of the entire relation code, equations (54)–(56).
* Algorithm 2, step 4, postselects the zero difference between the original codeword register and the decoder output. Its success probability is **exactly** \(1-p_{\rm fail}\). Theorem 3.1 expressly requires \((1-p_{\rm fail})^{-1}=\operatorname{poly}(m)\).

For P1's energy convention,

\[
H_{\rm BDL}=\sum_i\frac{J_i}{2}(I-S_i)
=\frac12\sum_iJ_iI-\sum_i\frac{J_i}{2}S_i.
\]

The scalar shift cancels from normalized Gibbs states, so the paper's coefficients are \(v_i=J_i/2\). The overlap of the two PSC outputs is

\[
2\sqrt{p_i(1-p_i)}
=\sqrt{1-\operatorname{sech}^2(\beta v_i)}
=\tanh(\beta v_i)
=\tanh(\beta J_i/2).
\]

There is no extra factor of two or replacement of a relation code by a rowspace in (A).

## 2. Uniform-prior genie proof, including collective measurements

Let \(c_1,\ldots,c_L\in C_H\) have disjoint nonempty supports of size at most \(w\). They are independent. Write

\[
C_H=\operatorname{span}\{c_1,\ldots,c_L\}\oplus C_1.
\]

A uniform codeword is \(c=v+\sum_j u_jc_j\), where \(v\) is uniform in \(C_1\) and the \(u_j\) are independent unbiased bits. Give \(v\) to the decoder. This cannot reduce its optimal probability of correctly recovering the entire codeword. Applying the known tensor-product bit flip \(X^v\) leaves independent binary pure-state ensembles, one on each support \(\operatorname{supp}(c_j)\), and a message-independent state outside those supports.

The two block states have overlap

\[
a_j=\prod_{i\in\operatorname{supp}(c_j)}t_i\ge t_*^w.
\]

Their equiprobable Helstrom success is

\[
s_j=\frac{1+\sqrt{1-a_j^2}}2.
\]

The optimal probability of getting **every** independent block bit right is \(\prod_js_j\), even with a joint entangled measurement. Here is a direct proof rather than an independence assumption about the measurement. For a block, the minimum-error-discrimination dual minimizes \(\operatorname{Tr}Y_j\) subject to \(Y_j\ge\rho_{j,0}/2\) and \(Y_j\ge\rho_{j,1}/2\). Such \(Y_j\) is positive. Tensoring optimal feasible operators gives

\[
\bigotimes_jY_j\ge2^{-L}\bigotimes_j\rho_{j,u_j}
\quad\text{for every }u\in\{0,1\}^L,
\]

so the full dual objective is at most \(\prod_js_j\). Product Helstrom measurements attain that value. This proves multiplicativity and then (A), using \(\sqrt{1-x}\le1-x/2\).

The argument concerns the decoder receiving the noisy codeword system, exactly the interface used in Algorithm 2. It does not claim that arbitrary new Gibbs algorithms with other operations or source states must perform this decoding.

## 3. Actual physical-check relations at every large even depth

This construction uses only the physical check columns of [BDL arXiv:2605.10943v1](https://arxiv.org/html/2605.10943v1), Section 3.2.2, equations (61)–(73), its Lemma 3.8, and the dual construction in Section 3.2.5. No identity columns from an augmented matroid occur here.

The physical Z boundary matrix of an RX step has block form

\[
B_Z=\begin{pmatrix}D_X&G_1&0\\0&D_Q&P\end{pmatrix},
\]

where columns are x-local faces, q-local edges, and doubled old-Z points. Rows are x-local edges and q-local vertices.

Choose an old qubit \(q\) with at least two old Z neighbors. Its \(Y_q\) graph consists of two subdivided stars joined at the old-Z leaves. Choose two leaves and let \(e_q\) be the cycle using their two bridges and four arms. If \(s=(\ell-1)/2\), this cycle has \(4s+2=2\ell\) edges. Thus \(D_Qe_q=0\).

For every old X neighbor \(x\), the inclusion of this cycle into \(Y_x\) is a cycle. BDL proves \(H_1(Y_x)=0\), so there exists a face chain \(f_x\) with

\[
D_X f_x=(G_1e_q)|_{Y_x}.
\]

Put \(f=\sum_{x\sim q}f_x\). The physical check-coordinate vector

\[
r_q=(f,e_q,0)
\]

is nonzero and satisfies \(B_Zr_q=0\). The only possible signs are positive: these are Z-type stabilizers and a zero boundary is a product equal to \(+I\). Every involved block has bounded size at fixed \(\ell\). If \(D\) bounds old check incidence and \(F_\ell\) bounds one x-block's number of faces, one may take

\[
|r_q|\le2\ell+D F_\ell.
\]

Two chosen old qubits give disjoint physical relation supports whenever their old X-neighbor sets are disjoint: the face chains occupy different x-blocks and their edge chains occupy different q-blocks. Sharing an old Z neighbor is harmless, because the old-Z point component is zero. A bounded-degree conflict graph therefore loses only a constant factor when packing such relations.

There are \(\Omega(N)\) eligible old qubits just before the final RX step. At a preceding RZ step, every local edge qubit inside a \(Y_z\) layer grid is incident to exactly its two endpoint physical Z-check vertices. Thus it has Z degree two. Each old Tanner square supplies a fixed-size layer-grid patch. The base has no isolated qubit in either check sector; RX and RZ preserve this because local edge qubits lie on faces and have endpoint checks, while local vertex qubits have local edge checks and old-neighbor restriction incidences. The prescribed Tanner pairing then gives

\[
2|T(2)|=\sum_q\deg_X(q)\deg_Z(q)=\Theta(N).
\]

Consequently local grid-edge qubits form a positive fraction at fixed \(\ell\), and bounded-overlap packing supplies a linear number of \(r_q\).

The final RZ step preserves these relations as **physical** relations. Its Z checks are vertices of connected \(Y_z\) blocks. Assign the old check coefficient constantly to every new vertex in that block. Each internal edge row sees two equal coefficients, and each root-vertex row sees the old relation equation. Hence the lifted coefficient vector is a new physical dependence. Different old check supports lift into disjoint blocks, and weights increase by only the fixed maximum vertex-block size.

Since two replacement steps change system size by only fixed factors, the final even-depth family has \(L\ge a_\ell N\) pairwise disjoint physical relations, all of weight at most a fixed \(w_\ell\). This proves the premise used in (A) at the actual family and operating scale.

## 4. USD/rejection and the separate fixed-sign issue

For the classical rejection sampler of Section 5, independently select each physical check with probability \(t_i=\tanh(\beta J_i/2)\). Selecting every coordinate of any \(r_q\) makes the subset dependent. For disjoint relations these events are independent, so

\[
\Pr(\text{accepted})\le(1-t_*^{w_\ell})^L
\le e^{-L t_*^{w_\ell}}.
\tag{B}
\]

Thus its explicit Gaussian-elimination/rejection implementation also has exponential expected repetitions.

Separately, Theorem 4.1's error guarantee is averaged over **all** uniformly random Hamiltonian sign strings. BDL fixes its frustration-free signs. For its centered Hamiltonian \(-\sum_i v_iS_i\), the paper's normalization factor is exactly

\[
Z'_\beta=\frac{Z_\beta}{2^n\prod_i\cosh(\beta v_i)}
=\sum_{c\in C_H}\prod_{i:c_i=1}t_i.
\]

Every relation product is \(+I\), because the stabilizers have a common \(+1\) sector. Restricting this positive sum to the span of the disjoint relations gives

\[
Z'_\beta\ge\prod_{j=1}^{L}(1+a_j)
\ge(1+t_*^{w_\ell})^L.
\tag{C}
\]

It is therefore exponentially far from one. This directly shows why the paper's sign-averaged near-normalization argument cannot be specialized to BDL's fixed sign choice. Pauli conjugation does not fix this: it changes signs only by a vector in \(C_H^\perp\), which has zero pairing with every relation, preserving the frustration sector and the normalization factor. It cannot turn a uniform average over all sign strings into a bound for the fixed frustration-free sector.

The runtime obstruction (A) is stronger than merely noting the sign restriction: decoder success is unchanged by the known sign-removing unitaries, so (A) applies independently of the sign choice. The fixed-sign normalization calculation (C) is an additional explicit failed premise, not the sole basis of the comparison.
