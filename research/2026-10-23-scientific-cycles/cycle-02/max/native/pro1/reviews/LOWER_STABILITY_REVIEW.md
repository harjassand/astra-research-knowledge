# Independent challenge: coherent inner/outer coding lower stability

Reviewer: `/root/stopping_converse`  
Date: 21 October 2026  
Verdict: **qualified internal mathematical acceptance** of the lower-stability construction below. The proof is valid when the ideal inner block has its inherited operator identity on the entire bath space, the outer code corrects the full indicated Pauli error space, and the tail normalization is performed coherently. This is not external certification or historical-priority acceptance.

The load-bearing question reviewed here is whether a persistent coherent bath invalidates sparse-history correction. It does not: the exact bath-independent inner identity prevents a bad block's bath disturbance from spreading through any good block. The proof below makes that statement at operator level, without assuming independence of errors or separability of intermediate states.

## 1. Inherited premise and exact inner isometries

Let the original fixed edge-reversal unitary be \(U\) on \(\mathbb C^3\otimes E\). Fix \(L=2m\) and let

\[
D=2^\ell\le C_m2^m,
\qquad \ell=\lfloor\log_2(C_m2^m)\rfloor.
\]

Choose any \(D\)-dimensional subspace of the inherited colored-Dyck code. Its encoding isometry \(C_{\rm in}:\mathbb C^D\to(\mathbb C^3)^{\otimes L}\) and its ideal output isometry \(C_{\rm out}\) satisfy the **operator identity**

\[
W_0^{(L)}(C_{\rm in}\otimes I_E)=C_{\rm out}\otimes I_E.
\]

This holds on the whole Hilbert space \(E\), not just on the reference initializer's support or on its density marginal. That stronger premise is present in the original source's equation for every vertex and then linearity/continuity.

There is a finite-dimensional ancillary output \(F\) and an isometry

\[
D_{\rm in}:(\mathbb C^3)^{\otimes L}\longrightarrow\mathbb C^D\otimes F
\]

whose action on the ideal output code is
\(D_{\rm in}C_{\rm out}|x\rangle=|x\rangle\otimes|0\rangle_F\). To construct it, extend an orthonormal basis of the output code to one of the physical output space and embed the remaining basis vectors orthogonally into a sufficiently large \(\mathbb C^D\otimes F\). This isometry must retain the syndrome/output register \(F\) in the joint proof; one cannot pretend the noisy output remains in the ideal code subspace.

For a fixed perturbed unitary \(V\) on the same port/bath space, define

\[
G_V=(D_{\rm in}\otimes I_E)W_V^{(L)}(C_{\rm in}\otimes I_E).
\]

Both \(G_V\) and \(G_0\) are isometries from packet \(\otimes E\) to packet \(\otimes F\otimes E\), and

\[
G_0=I_{\rm packet}\otimes|0\rangle_F\otimes I_E.
\]

Telescoping the \(L\) unitary interactions gives, uniformly over all bath states and references,

\[
\|G_V-G_0\|\le L\|V-U\|=:\epsilon.
\]

For the root family \(V_s=\cos(s)U+i\sin(s)I\), \(U^2=I\) implies

\[
\|V_s-U\|=2|\sin(s/2)|,
\qquad \epsilon=2L|\sin(s/2)|.
\]

The exact norm follows by squaring the difference (or using the two eigenvalues of \(U\)); the cross terms cancel. Only sufficiently small \(\epsilon\) is used below.

## 2. Sparse histories remain supported on sparse logical packets

Run \(N\) encoded inner blocks in chronological order on the **same** bath \(E\). Alice can prepare all logical packets jointly using the outer encoder and emit the physical ports in order. Bob applies the inner output isometry to each received block, retaining its packet and its own \(F_i\). No feedback is needed. No bath reset or fresh internal bath subsystem is introduced.

Write

\[
G_V=G_0+B,\qquad \|B\|\le\epsilon.
\]

Expanding the ordered product over all subsets \(S\subseteq\{1,\ldots,N\}\) gives a sum of histories. For a history with \(B\) in precisely the positions \(S\),

\[
\|H_S\|\le\epsilon^{|S|}.
\]

Every good factor \(G_0\) is identity on its packet and on the bath, and appends only a fixed local \(|0\rangle_{F_i}\). Therefore the history acts as identity on every packet outside \(S\). The bath and all ancillary outputs may retain arbitrary coherent correlations, but they are operator-valued coefficients on the error supported on \(S\). They cannot acquire an action on another packet through a good block.

This argument concerns the supports of fixed linear operators. An outer codeword may entangle all packets; a bath disturbed by an earlier bad block may be entangled with those packets. Neither fact invalidates an operator identity or enlarges the support of an operator on a good packet. No assumption of independent stochastic errors has entered.

Expand each supported packet operator in its Pauli basis. A history with \(|S|=j\) then lies in the span of Pauli errors of qubit weight at most \(\ell j\), with bounded operator-valued coefficients acting from \(E\) into \(E\otimes F_1\otimes\cdots\otimes F_N\). The number of coefficients is finite for fixed \(N\). The bath itself can be infinite-dimensional; no bound on the coefficient count in a bath basis is needed.

## 3. The inherited coding lemma corrects the whole coherent low-history space

Choose a fixed \(\delta\in(0,1/2)\), set \(t=\lfloor\delta N\rfloor\), and let \(b=\ell N\) be the number of outer physical qubits. Define the Pauli set

\[
\mathcal P_t=\{P:\operatorname{wt}(P)\le\ell t\},
\qquad
k_N=\sum_{j=0}^{\ell t}\binom{b}{j}3^j.
\]

Apply the inherited owner lemma to the CPTP channel which is the uniform mixture of these \(k_N\) Pauli conjugations. It supplies a subspace code of dimension

\[
K_N\ge\left\lceil\frac{2^{\ell N}}{k_N^4}\right\rceil.
\]

This auxiliary channel is used only to obtain Knill--Laflamme conditions for the whole error set. It is **not** a replacement model for the actual reservoir, and no Pauli independence assumption is imposed on the physical errors. The conditions correct arbitrary linear combinations of the specified errors, including combinations with environment-valued coefficients.

For completeness, let \(C\) be the outer encoder and write the conditions as

\[
C^\dagger P_a^\dagger P_b C=\lambda_{ab}I_{K_N}.
\]

Choose syndrome vectors \(|s_a\rangle\) with Gram matrix \(\langle s_a|s_b\rangle=\lambda_{ab}\). The map

\[
P_aC|\psi\rangle\longmapsto|\psi\rangle\otimes|s_a\rangle
\]

is well defined and isometric on the span of the correctable error images, because it preserves every pairwise inner product. Extend it to a recovery isometry on the whole packet space by allowing a sufficiently large syndrome space. Consequently, **simultaneously for all low histories**,

\[
(R\otimes I)H_{\rm low}(C\otimes I_E)=I_{\rm logical}\otimes Z
\]

for one bounded map \(Z:E\to E\otimes F_1\otimes\cdots\otimes F_N\otimes\mathrm{Syndrome}\). Here

\[
H_{\rm low}=\sum_{|S|\le t}H_S.
\]

The map \(Z\) is independent of the logical state. It need not be an isometry, and its norm is not assumed to be one. This exact factorization is the coherent correction statement required by the construction; proving only a correction of a mixture of histories would be insufficient.

## 4. Tail estimate and normalization without an initializer-dependent shortcut

The omitted history sum has norm at most

\[
T_N:=\sum_{j>t}\binom Nj\epsilon^j.
\]

The actual globally recovered map

\[
H=(R\otimes I)H_{\rm actual}(C\otimes I_E)
\]

is an isometry because all physical gates, encoders, and retained-environment decoders were represented isometrically. Hence

\[
\|H-I_{\rm logical}\otimes Z\|\le T_N.
\]

The root's fixed-bath-vector normalization is valid, but a polar-decomposition argument gives a uniform operator statement. If \(T_N<1\), testing on any unit logical vector and any bath vector gives

\[
(1-T_N)\|\xi\|\le\|Z\xi\|\le(1+T_N)\|\xi\|.
\]

Therefore \(Z\) is bounded below. Its polar decomposition \(Z=W|Z|\) has an isometry \(W\), and the spectrum of \(|Z|\) is contained in \([1-T_N,1+T_N]\). Thus

\[
\|Z-W\|\le T_N,
\qquad
\boxed{\|H-I_{\rm logical}\otimes W\|\le2T_N.}
\]

This avoids assuming a normalized low-history amplitude or a probability distribution over coherent histories. It is valid for infinite-dimensional \(E\), because a bounded-below operator has an isometric polar part on all of its domain.

For any initial bath state, pure or mixed, retain a purification and then trace the nonlogical output systems. If two isometries differ by norm at most \(\eta\), their induced channels differ in **full** diamond norm by at most \(2\eta\): apply the isometries to an arbitrary purified input, use the pure-state trace-distance bound, and then contract under partial trace. Consequently,

\[
\boxed{\|\Lambda_{N,V,\tau}-\mathrm{id}_{K_N}\|_\diamond\le4T_N.}
\]

The corresponding half-diamond error is at most \(2T_N\). The estimate is uniform over all bath states and arbitrary logical references. No bath-state truncation, finite entropy, or uniformity in a normal-state tail is required for this lower bound.

## 5. Exponential tail and rate

For \(\delta>\epsilon/(1+\epsilon)\), the same Chernoff argument used in the scalar history review gives the stronger estimate

\[
T_N\le2^{N\varphi_\epsilon(\delta)},
\qquad
\varphi_\epsilon(\delta)=h_2(\delta)+\delta\log_2\epsilon.
\]

The root's version with an additional \(N+1\) prefactor is also sufficient. The floor in \(t\) causes no loss: for integer \(j\), \(j>\lfloor\delta N\rfloor\) means exactly \(j>\delta N\).

With \(\delta=\sqrt\epsilon\), for \(0<\epsilon<1\) one has \(\delta>\epsilon/(1+\epsilon)\), and

\[
\varphi_\epsilon(\delta)
\le\delta\log_2(e\delta)<0
\quad\text{when }\delta<1/e.
\]

The error therefore decays exponentially in \(N\) for each fixed sufficiently small perturbation and chosen fixed inner block.

For the outer code, \(j/(\ell N)\le t/N\le\delta\), and the function \(h_2(x)+x\log_2 3\) is increasing on \(x<3/4\). Thus

\[
k_N\le(\ell N+1)2^{\ell N[h_2(\delta)+\delta\log_2 3]},
\]

so

\[
\log_2K_N\ge
\ell N\{1-4[h_2(\delta)+\delta\log_2 3]\}
-4\log_2(\ell N+1).
\]

If desired, restricting to a power-of-two logical subspace loses less than one qubit. The total physical forward cost is exactly \(LN\). Hence the construction achieves any rate below

\[
\boxed{
\frac\ell L\{1-4[h_2(\delta)+\delta\log_2 3]\}
\quad\text{qubits per forward use}
}
\]

provided the braces are positive and the tail exponent is negative. Both conditions hold for all sufficiently small \(\epsilon\). The bound is intentionally loose; no improved coding constant is needed for the continuity conclusion.

## 6. Order of limits and actual conclusion

Given any target \(r<3/2\), first choose a finite Dyck block length \(L\) large enough that \(\ell/L>r\), using the inherited Catalan growth. Then choose a sufficiently small **fixed** unitary perturbation so that \(\epsilon=L\|V-U\|\), \(\delta=\sqrt\epsilon\), and the displayed achievable rate remain above \(r\). Finally let the number of inner blocks \(N\to\infty\). The bath initializer is fixed throughout; the number or state of bath registers is not changed with \(N\).

For the coherent family this proves

\[
\boxed{\liminf_{s\to0}Q_{\rm unassisted}(V_s,\tau)\ge3/2.}
\]

Combined with the separately established upper bound
\(\limsup_{s\to0}Q_{\leftarrow}(V_s,\tau)\le3/2\) and the inclusion of unassisted codes among feedback codes, it yields

\[
\lim_{s\to0}Q_{\rm unassisted}(V_s,\tau)
=\lim_{s\to0}Q_{\leftarrow}(V_s,\tau)=3/2.
\]

The lower construction itself is more general than this one-parameter family: it uses only unitarity on the same port/bath space and operator-norm proximity to \(U\). Therefore it proves lower semicontinuity at \(U\) against arbitrary fixed unitary perturbations in that norm, uniformly over bath initializers. The upper-stability construction still depends on the special coherent family and is not promoted to generic upper continuity.

## 7. Scope, resource accounting, and failed shortcuts

- All \(LN\) forward qutrit calls are counted. The scheme is fixed horizon, not expected-cost stopping.
- The same bath is used throughout. All \(F_i\) registers and recovery syndromes are external decoder systems, explicitly retained in the isometric proof. They are not fresh internal bath cells or hidden resets.
- No classical feedback, preshared entanglement, bath access, or postselection is used by the lower construction.
- Exact ideal bath return is used as an **operator identity on all of E**. Mere return of one density marginal would not prevent error propagation and is insufficient for this argument.
- The perturbed scheme promises approximate logical transmission. It does **not** promise terminal or all-use bath return. The polar isometry \(W\) can change the bath and attach it to external syndrome systems.
- Coherent low-history amplitudes are corrected jointly. Treating them as independent probabilities, or normalizing each history, would be incorrect.
- The exact outer code is an existence result from the already documented Knill--Laflamme/Tverberg lemma. No efficient encoder/decoder synthesis, practical blocklength, or hardware-resource advantage is established. Ancilla dimensions and local computational work can grow rapidly with \(N\).
- The convergence rate is not uniform as the perturbation tends to zero: the chosen block length and tail exponent depend on the target rate and perturbation. The nested order of limits is explicit.
- The construction establishes continuity at the unperturbed point after combining upper and lower bounds. It gives no exact capacity formula or proof of feedback equality at individual nonzero angles.

## Review record

I read the inherited coding lemma and exact tree-block premise, challenged the support of coherent histories, reconstructed the joint Knill--Laflamme recovery, and supplied the uniform polar-normalization proof. No old finite capacity audit was rerun, and no numerical experiment is used to establish this infinite-bath claim. No external person or compute service was used. Inference and total tool costs are not independently metered.
