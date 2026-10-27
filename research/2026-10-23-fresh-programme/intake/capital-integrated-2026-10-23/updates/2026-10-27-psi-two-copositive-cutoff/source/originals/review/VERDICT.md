# Exact composition bound under two-copositivity

**Verdict: TRUE.** Fix \(d\ge2\). If each complex-linear map
\(\Phi_i:M_d\to M_d\) is completely positive (CP) and
\(t\circ\Phi_i\) is two-positive, then
\[
\Phi_{2(d-1)}\circ\cdots\circ\Phi_1
\]
is entanglement breaking (EB). The maps can differ and need not preserve trace. Full complete copositivity is not required. The argument below checks the weaker hypotheses directly in the supplied block proof; it is a mathematical source audit, not a new Lean verification or a priority claim.

## 1. What two-copositivity supplies

Write \(P_v=|v\rangle\langle v|\), allowing unnormalized vectors, and \(\mathcal C_2=\{\Phi:\Phi\text{ CP},\ t\circ\Phi\text{ two-positive}\}\). For any \(\Phi\in\mathcal C_2\) and positive \(X\in M_2\otimes M_d\),
\[
\rho=(\operatorname{id}_2\otimes\Phi)(X)\ge0,
\qquad
\rho^{\Gamma_B}=(\operatorname{id}_2\otimes(t\circ\Phi))(X)\ge0.
\]
Here \(\Gamma_B\) transposes the system, while \(\Gamma_R\) transposes the reference. Since
\(\rho^{\Gamma_R}=(\rho^{\Gamma_B})^T\), full matrix transposition also gives \(\rho^{\Gamma_R}\ge0\). This uses exactly a two-dimensional reference, not positivity of \(\operatorname{id}_k\otimes(t\circ\Phi)\) for arbitrary \(k\).

We next prove that every \(\Psi\in\mathcal C_2\) sends every such qubit PPT operator \(\rho\) to a separable operator.

## 2. The pair lemma, including singular blocks

For a positive block matrix \(\begin{psmallmatrix}A&B\\B^\dagger&C\end{psmallmatrix}\), the generalized Schur complement gives
\[
C\ge0,\quad B\ker C=0,\quad A\ge BC^+B^\dagger.
\]
The last assertion follows by evaluating its quadratic form at
\((x,-C^+B^\dagger x)\), after using the kernel condition. Applying this also to
\[
\rho^{\Gamma_R}=\begin{pmatrix}A&B^\dagger\\B&C\end{pmatrix}\ge0
\]
gives \(B^\dagger\ker C=0\) and
\[
R=A-\tfrac12(BC^+B^\dagger+B^\dagger C^+B)\ge0.
\]
Both sides of \(B\) are therefore supported on \(\operatorname{Ran}C\). If \(C=0\), then \(B=0\), and the result is immediate.

Otherwise take an SVD, on \(\operatorname{Ran}C\),
\[
C^{+1/2}BC^{+1/2}=\sum_j s_j u_jv_j^\dagger,
\quad p_j=C^{1/2}u_j,\quad q_j=C^{1/2}v_j,
\quad D_j=\tfrac12(P_{p_j}+P_{q_j}).
\]
The two singular-vector families are complete orthonormal bases of that support, including zero singular values. Hence
\[
\sum_jD_j=C,\quad \sum_js_jp_jq_j^\dagger=B,
\quad\sum_js_j^2D_j=\tfrac12(BC^+B^\dagger+B^\dagger C^+B).
\]
Consequently
\[
\rho=P_0\otimes R+\sum_jM_j,
\quad M_j=\begin{pmatrix}s_j^2D_j&s_jp_jq_j^\dagger\\s_jq_jp_j^\dagger&D_j\end{pmatrix}.
\]
The pieces \(M_j\) are **not assumed positive**; only their images will be proved separable.

Fix one pair \(p,q\) and let \(v=|0\rangle p+|1\rangle q\). CP of \(\Psi\) gives
\[
H=(\operatorname{id}_2\otimes\Psi)(P_v)
=\begin{pmatrix}\Psi(P_p)&\Psi(pq^\dagger)\\\Psi(qp^\dagger)&\Psi(P_q)\end{pmatrix}\ge0.
\]
Two-positivity of \(t\circ\Psi\), followed by full transposition, gives \(H^{\Gamma_R}\ge0\). If \(S\) swaps the two reference basis vectors, then
\[
F=\tfrac12\bigl(H+(S\otimes I)H^{\Gamma_R}(S\otimes I)\bigr)
=\begin{pmatrix}\Psi(D)&\Psi(pq^\dagger)\\\Psi(qp^\dagger)&\Psi(D)\end{pmatrix}\ge0.
\]

Every positive equal-diagonal block matrix \(\begin{psmallmatrix}D&Y\\Y^\dagger&D\end{psmallmatrix}\) is separable. Indeed, both \(Y\) and \(Y^\dagger\) vanish on \(\ker D\); restrict to \(\operatorname{Ran}D\) and filter by \(D^{-1/2}\). The result has diagonal blocks \(I\), and \(Y\) is a contraction. Its SVD expresses \(Y=(W_++W_-)/2\) as an average of two unitaries. Spectral decomposition of each unitary expresses \(\begin{psmallmatrix}I&W\\W^\dagger&I\end{psmallmatrix}\) as a sum of positive product operators. Filtering back preserves separability. The zero-support case is zero.

Thus \(F\) is separable. The image of \(M_j\) is its local reference filter by \(\operatorname{diag}(s_j,1)\), so is separable even when that filter is singular. The remainder becomes \(P_0\otimes\Psi(R)\ge0\), also separable. This proves
\[
(\operatorname{id}_2\otimes(\Psi\circ\Phi))(X)\in\operatorname{Sep}_{2,d}
\quad(X\ge0;\ \Phi,\Psi\in\mathcal C_2).
\]
Each pair is therefore a CP, two-entanglement-breaking map.

## 3. Why this proves EB for every reference

The necessary lifting fact is: if \(\Sigma\ge0\) on \(\mathbb C^r\otimes\mathbb C^d\), \(r\ge2\), has a separable compression to one two-dimensional reference subspace, then \(\operatorname{SN}(\Sigma)\le r-1\). For completeness, write
\[
\Sigma=\begin{pmatrix}D&K\\K^\dagger&T\end{pmatrix},
\qquad D=\sum_\alpha P_{f_\alpha},\quad f_\alpha\text{ product on }\mathbb C^2\otimes\mathbb C^d.
\]
The Schur complement in reverse block order yields \(DD^+K=K\) and \(T-K^\dagger D^+K\ge0\). With \(g_\alpha=K^\dagger D^+f_\alpha\),
\[
\Sigma=\sum_\alpha P_{f_\alpha\oplus g_\alpha}
+\begin{pmatrix}0&0\\0&T-K^\dagger D^+K\end{pmatrix}.
\]
Each appended vector has Schmidt rank at most \(1+(r-2)=r-1\); the residual is supported on \(r-2\) reference dimensions. This also handles singular \(D\), including \(D=0\). For \(r=2\), separability of the whole compression is the assertion.

Now take a pure input vector of Schmidt rank \(r\). Its output under a pair \(\Theta=\Psi\circ\Phi\) is positive because \(\Theta\) is CP, and lives on its original \(r\)-dimensional reference support. Every two-dimensional compression is the pair's output on a positive qubit input, hence separable by Section 2. The lifting fact gives Schmidt number at most \(r-1\) for \(r\ge2\). A product input has separable output. Summing a Schmidt-number decomposition therefore proves
\[
\operatorname{SN}((\operatorname{id}\otimes\Theta)(X))
\le\max\{\operatorname{SN}(X)-1,1\}.
\]
For arbitrary finite reference size \(k\), initially \(\operatorname{SN}(X)\le d\). After \(d-1\) consecutive pairs the output is separable. The composite is CP, so this is precisely EB.

**Assumption boundary.** Complete positivity supplies arbitrary-reference positivity in this last step. Merely replacing CP by two-positivity is not justified by this proof. Every use of copositivity occurs at reference dimension two. No trace normalization, channel factorization, faithful state, invertible global block, or nonzero success probability is needed. A nonzero output can be normalized afterwards by positive scaling; the zero output is separable. The theorem concerns serial compositions, not tensor powers or networks with a noiseless quantum-memory bypass. No optimality of \(2(d-1)\) is asserted.

## 4. A fully explicit non-PPT channel in the input class

For every \(d\ge3\), define
\[
\Phi_d(X)=\frac{2\operatorname{tr}(X)I_d-X^T}{2d-1}.
\]
Let \(F=\sum_{ij}|i\rangle\langle j|\otimes|j\rangle\langle i|\) be the swap, and \(|\Omega_d\rangle=\sum_i|ii\rangle\) be unnormalized. The Choi matrix is
\[
J(\Phi_d)=\frac{2I-F}{2d-1}>0,
\]
with eigenvalues \(1/(2d-1)\) and \(3/(2d-1)\). Thus \(\Phi_d\) is CP. Directly, \(\operatorname{tr}\Phi_d(X)=\operatorname{tr}X\), so it is trace preserving.

Furthermore
\[
(t\circ\Phi_d)(X)=\frac{2\operatorname{tr}(X)I_d-X}{2d-1}.
\]
For any \(v\in\mathbb C^2\otimes\mathbb C^d\) of Schmidt rank \(r\le2\), with \(\rho_R=\operatorname{Tr}_B P_v\), Cauchy–Schwarz on its Schmidt expansion gives
\(P_v\le r(\rho_R\otimes I_d)\le2(\rho_R\otimes I_d)\). Hence
\[
(\operatorname{id}_2\otimes(t\circ\Phi_d))(P_v)
=\frac{2\rho_R\otimes I_d-P_v}{2d-1}\ge0.
\]
Spectral decomposition covers every positive input, proving two-positivity. But
\[
J(t\circ\Phi_d)=\frac{2I-P_{\Omega_d}}{2d-1}
\]
has eigenvalue \((2-d)/(2d-1)<0\) on \(|\Omega_d\rangle\). It is not CP, and \(\Phi_d\) is not PPT. Concretely \(d=3\) gives \(\Phi_3(X)=(2\operatorname{tr}(X)I_3-X^T)/5\), with that negative eigenvalue \(-1/5\).

The class inclusion is strict for \(d\ge3\). In \(d=2\), two-positivity of \(t\circ\Phi\) already implies its complete positivity by the Choi criterion, so strictness cannot hold there. No failed example is being omitted: the displayed family passes all three exact checks.

## 5. Explicit-statement and provenance boundary

Only the five source files authorized for this audit were read. In the supplied PSI release snapshot attributed to commit `da37af2ae174687403fbd97e9673c819edee71fd`:

- `paper/source/ppt_composition_prl_draft.tex`, lines 40–42 and Theorem 1, explicitly state CP and **complete** copositivity. The pair proof at lines 186–295 uses only the two-reference tests isolated above.
- `lean/docs/FIDELITY.md`, lines 7–18, 32–35 and 66–71, describes a full-PPT theorem and explicitly defines that hypothesis as CP plus complete copositivity. It does not certify a Lean theorem under the weaker condition.

In the authorized old published Astra snapshot:

- The package `README.md`, lines 7–25, explicitly treats arbitrary CP/two-copositive words with **approximate** EB replacement. Lines 43–47 preserve the unresolved exact-word boundary.
- `nonstationary_ppt/EXPLICIT_EB_NOISE_REPAIR.md`, Sections 3–5, gives two-EB repairs and then EB approximation/domination; Section 6 explicitly separates this from finite exact word membership.
- `nonstationary_ppt/EXACT_UNRESTRICTED_GATE_REDUCTIONS.md`, opening and Sections 2–4, contains reductions for full-PPT exact words, with a remaining conditional gate.

Thus the stronger exact statement is not explicitly stated in these inspected files. This is not a repository-wide or literature-wide absence finding, and no novelty or historical-priority conclusion is drawn. The strengthened proof reuses PSI's qubit block construction and the credited Schmidt-number iteration; the old approximation family's broader input assumption is not itself a new discovery here.
