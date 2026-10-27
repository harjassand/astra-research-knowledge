# A complete replica hierarchy and an exact failure at four replicas

27 October 2026. This continuation does not prove or refute the all-copy qutrit Werner inequality. There is no admissible negative endpoint witness here. The new object below is a convex completion of the full projection problem, with an explicit convergence bound and an exact obstruction to stopping at four replicas. Historical novelty and external review are unestablished.

## 1. Fixed target and imported completeness

Retain the frozen first-stage definitions

\[
b_n(A,B)=\sum_{S\subset[n]}(-1/2)^{|S|}\langle\operatorname{Tr}_S A,\operatorname{Tr}_S B\rangle,
\qquad q_n(C)=b_n(C,C).
\]

The target is positivity for **all complex matrices of rank at most two, at every finite n**. The first-stage full-frame Cauchy growth invariant remains valid but unclosed: proving its subexponential growth still requires new information. An absolute norm bound cannot establish that relative statement.

Use the exact prior N525, whose complete source proof was reread at pinned Astra revision `65aae508a61d02e4a6ba5b368a94779ae6d744cf`. It proves that any negative complex rank-two matrix lifts, with finitely many qutrit flags, to a negative rank-two orthogonal projection. It also proves the following dichotomy for

\[
g_n=\min_{P=P^*=P^2,\ \operatorname{Tr}P=2}q_n(P):
\]

either the full target holds and every \(g_n=0\), or it fails and \(\limsup_n g_n<0\). These prior results are used at their actual scope; the projection reduction and gap dichotomy are not new results of this continuation.

## 2. The new auxiliary completion

Let \(H=({\mathbb C}^3)^{\otimes n}\), \(D=3^n\), and let \(U_\pi\) permute **whole replicas** of H. On two replicas put

\[
A_n=\prod_{i=1}^n(F_{12,i}-I/2).
\]

The ordinary swap contraction, valid for every Hermitian matrix \(\rho\), gives

\[
\operatorname{Tr}(\rho^{\otimes2}A_n)=q_n(\rho),\qquad \|A_n\|_{op}=(3/2)^n.\tag{1}
\]

For \(m\ge3\), define \(\ell_{n,m}\) to be the minimum of \(\operatorname{Tr}(R_2A_n)\) over density matrices R on \(H^{\otimes m}\) such that

\[
U_\pi R U_\pi^*=R,\qquad
\operatorname{Tr}(R U_\pi)=2^{c(\pi)-m}\quad(\pi\in S_m),\tag{2}
\]

where c is the number of cycles, including fixed points, and \(R_2\) is the two-replica marginal. This is an ordinary finite SDP with explicitly specified rational matrices. Invariance reduces the moment constraints to conjugacy classes. It is not assumed that a feasible R is a mixture of product powers.

For every rank-two projection P, \(R=(P/2)^{\otimes m}\) is feasible, because a permutation has expectation \(\prod_{\text{cycles }a}\operatorname{Tr}((P/2)^{|a|})=2^{c(\pi)-m}\). Thus

\[
\ell_{n,m}\le g_n/4.\tag{3}
\]

Partial trace maps level m+1 into level m: extending a permutation by one fixed point preserves its required moment. Consequently \(\ell_{n,m}\) is nondecreasing in m. No rank-two support plane has been excluded in (3).

### Spectral rigidity lemma

For a density matrix \(\rho\) in any dimension at least two, define

\[
d(\rho)=\operatorname{Tr}\rho^3-\operatorname{Tr}\rho^2+\tfrac14
=\sum_j\lambda_j(\lambda_j-\tfrac12)^2\ge0.\tag{4}
\]

Equality holds exactly for \(\rho=P/2\) with P a rank-two orthogonal projection. Moreover there is such a P with

\[
\|\rho-P/2\|_1\le16\sqrt{d(\rho)}.\tag{5}
\]

**Proof.** Round each eigenvalue at the threshold 1/4 to 0 or 1/2, obtaining \(\sigma=P_h/2\). For every eigenvalue,

\[
|\lambda-\mathrm{round}(\lambda)|\le4\lambda|\lambda-1/2|.
\]

Cauchy--Schwarz therefore gives \(\|\rho-\sigma\|_1\le4\sqrt d\). If \(d<1/64\), then \(|1-h/2|<1/2\), which forces h=2. If \(d\ge1/64\), any rank-two P has trace distance in the full trace norm at most 2, and \(2\le16\sqrt d\). Equation (4) proves the equality statement as well. □

This lemma supplies a stable flat-rank constraint. It is a polynomial equation in spectral moments, rather than an imported positivity assertion about q.

### Quantitative convergence theorem

Set

\[
\delta=\min\{2,12D^2/m\}.
\]

Then

\[
0\le g_n/4-\ell_{n,m}
\le32\sqrt{2\delta}+\delta(3/2)^n.\tag{6}
\]

**Proof.** The finite quantum de Finetti theorem of Christandl--König--Mitchison--Renner, Theorem II.7, supplies a measure \(\mu\) on density matrices such that

\[
\left\|R_3-\int\rho^{\otimes3}\,d\mu(\rho)\right\|_1\le\delta.
\]

Their distance convention is **half** the trace norm: their bound \(2D^2k/m\), at k=3, becomes \(12D^2/m\) in the full norm used here. The primary theorem, convention, and its symmetric-purification proof were checked in the versioned primary PDF.

The constraints (2) fix the transposition moment to 1/2 and the real three-cycle moment to 1/4. A transposition and the Hermitian average of the two three-cycles each have norm one. Hence

\[
\int d(\rho)d\mu\le2\delta.\tag{7}
\]

Let \(L(X)=X-\operatorname{Tr}(X)I_3/2\). Its Hilbert--Schmidt eigenvalues are 1 and -1/2; thus \(\|L^{\otimes n}\|_{HS\to HS}=1\). For density matrices \(\rho,\sigma\),

\[
|q_n(\rho)-q_n(\sigma)|
\le(\|\rho\|_F+\|\sigma\|_F)\|\rho-\sigma\|_F.
\]

With \(\sigma=P/2\), (5) bounds this by \(32\sqrt{d(\rho)}\). Pointwise comparison with the minimum \(g_n/4\), followed by Cauchy--Schwarz in \(\mu\), yields

\[
\int q_n(\rho)d\mu\ge g_n/4-32\sqrt{2\delta}.
\]

Partial trace is contractive in trace norm, so (1) bounds the difference between this integral and the SDP objective by \(\delta(3/2)^n\). This proves (6), together with (3). □

In particular the hierarchy converges to \(g_n/4\) for **each fixed n**, with no hypothesis of Werner positivity.

One explicit joint scaling is

\[
m(n)=\lceil12\,18^n\rceil,
\quad
0\le g_n/4-\ell_{n,m(n)}
\le32\sqrt2\,2^{-n/2}+(3/4)^n\longrightarrow0.\tag{8}
\]

Combining (8) with the prior N525 gap dichotomy gives an exact full-target alternative:

* if the full all-copy target holds, \(\ell_{n,m(n)}\to0\);
* if it fails, \(\limsup_n\ell_{n,m(n)}<0\).

Thus proving the first alternative for these **explicit convex objects** would suffice. It is not proved here. The original Cauchy growth rate is zero exactly in that same first alternative. This is a complete reduction, not an acquired bound on the SDP values.

**Costs.** The uncompressed PSD matrix has dimension \(D^m\). The explicit diagonal scaling (8) uses exponentially many replicas and doubly exponential matrix dimension in n. The convergence theorem does not give an efficient decision algorithm, a finite cutoff, or an all-copy certificate. General finite de Finetti theory is established machinery; no invention of that machinery is claimed.

## 3. Strong opposition: even all four-replica permutation moments are insufficient

Here is an exact feasible relaxed state at n=3, m=4 with objective

\[
\boxed{\operatorname{Tr}(R_2A_3)=-13/32.}\tag{9}
\]

It is supported on **binary physical sites**. On this binary subspace the original quadratic form is \(\|\Pi^{\otimes3}(C)\|_F^2\ge0\) for every matrix C, where \(\Pi(X)=X-\operatorname{Tr}(X)I_2/2\). Therefore (9) cannot be an admissible witness or a mixture of identical density-matrix powers. It is an exact counterexample to sufficiency of the finite replica completion.

For a permutation-invariant R, the objective can be written

\[
K=\frac16\sum_{1\le a<b\le4}\bigotimes_{i=1}^3(F_{ab,i}-I/2),\qquad
\operatorname{Tr}(RK)=\operatorname{Tr}(R_2A_3).\tag{10}
\]

Construct three mutually orthogonal invariant sectors, all in four replicas of three physical qubits embedded in qutrits.

**Sector [4].** Use the one-dimensional all-zero vector. K equals 1/8 there; every whole-replica permutation acts as 1.

**Sector [31].** At each physical site use the three-dimensional standard S4 representation inside the one-excitation subspace of four qubits. In the basis \(f_j=e_j-e_3\), j=0,1,2, its Gram matrix is \(G=I+\mathbf1\mathbf1^T\). Each transposition is obtained by permuting the four coordinates. On the three-site tensor product, let V be the span of

\[
\begin{split}
v_0={}&4f_0^{\otimes3}-\mathrm{Sym}(f_0^2f_1)-\mathrm{Sym}(f_0^2f_2)
       +\mathrm{Sym}(f_0f_1^2)+\mathrm{Sym}(f_0f_2^2),\\
v_1={}&4f_1^{\otimes3}-\mathrm{Sym}(f_1^2f_0)-\mathrm{Sym}(f_1^2f_2)
       +\mathrm{Sym}(f_1f_0^2)+\mathrm{Sym}(f_1f_2^2),\\
v_2={}&f_0^{\otimes3}+f_1^{\otimes3}+f_2^{\otimes3}.
\end{split}\tag{11}
\]

Sym here is the sum of the three distinct placements. The vectors are independent. Direct substitution of the six coordinate transpositions gives

\[
KV=-13V/24,
\quad TV=V/3,
\quad T=\tfrac16\sum_{a<b}F_{ab}^{\mathrm{whole}}.
\tag{12}
\]

The span is invariant and is one copy of [31]. Its normalized orthogonal projector is denoted \(\sigma_{31}\). The verifier checks invariance and the full character, not just the T eigenvalue.

**Sector [22].** At a physical site use the two-dimensional spin-zero subspace spanned by unnormalized singlet pairings

\[
f_0=s_{12}s_{34},\qquad f_1=s_{13}s_{24},\qquad s_{ab}=|01\rangle_{ab}-|10\rangle_{ab}.
\]

In the ordered weight-two binary words 0011,0101,0110,1001,1010,1100, the two columns are

\[
W=\begin{pmatrix}0&1\\1&0\\-1&-1\\-1&-1\\1&0\\0&1\end{pmatrix},
\qquad W^TW=\begin{pmatrix}4&2\\2&4\end{pmatrix}.
\]

The six transpositions, in order 12,13,14,23,24,34, act as

\[
A,B,C,C,B,A,
\quad A=\begin{pmatrix}-1&-1\\0&1\end{pmatrix},
\quad B=\begin{pmatrix}1&0\\-1&-1\end{pmatrix},
\quad C=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]

On three such sites take the span of the independent vectors

\[
w_0=3f_0^{\otimes3}-\mathrm{Sym}(f_0^2f_1)+\mathrm{Sym}(f_0f_1^2),
\qquad w_1=f_0^{\otimes3}+f_1^{\otimes3}.
\tag{13}
\]

Substitution gives \(Kw_j=-9w_j/8\). The span is invariant and carries [22]; denote its normalized orthogonal projector by \(\sigma_{22}\). All normalizations and projectors use the displayed physical Gram matrices, so the nonorthogonal coordinates introduce no PSD assumption.

Now set

\[
R=\frac5{16}\sigma_4+\frac9{16}\sigma_{31}+\frac2{16}\sigma_{22}.\tag{14}
\]

This is a positive density matrix invariant under all whole-replica permutations. For the five S4 conjugacy classes, the normalized characters are

| sector | identity | transposition | double transposition | three-cycle | four-cycle |
|---|---:|---:|---:|---:|---:|
| [4] | 1 | 1 | 1 | 1 | 1 |
| [31] | 1 | 1/3 | -1/3 | 0 | -1/3 |
| [22] | 1 | 0 | 1 | -1/2 | 0 |

The weights in (14) consequently give moments

\[
1,\quad1/2,\quad1/4,\quad1/4,\quad1/8,
\]

exactly \(2^{c(\pi)-4}\) in every class. Thus **every** constraint (2) holds. Equations (12)--(14) give

\[
\frac5{16}\frac18-\frac9{16}\frac{13}{24}-\frac2{16}\frac98=-\frac{13}{32},
\]

proving (9). These are rational identities, not rounded optimizer output.

Appending n-3 all-zero physical sites preserves all permutation moments and multiplies the objective by \(2^{-(n-3)}\). Thus the four-replica relaxation admits a negative point for every n>=3, even on binary physical support.

### Exact consequence for scalar/global-permutation certificates

No correction Z in the algebra of whole-replica S4 permutations can both

1. have zero expectation on every \((P/2)^{\otimes4}\) for rank-two projections P, and
2. make \(K+Z\) positive semidefinite,

at any n>=3. Indeed (14) matches the complete whole-permutation moment functional of every such P, so \(\operatorname{Tr}(RZ)=0\); then (9), with padding, contradicts positivity. No centrality restriction is needed for Z. This rules out a complete class of finite replica certificates, not the full target and not more general corrections involving physical structure or higher replica consistency.

## 4. What remains open

The hierarchy is complete when m grows, but the required nonnegative asymptotic floor is not known. The exact four-replica object (14) shows that correct global characters and PSD alone leave substantial nonphysical freedom. Even the rank-two flat spectrum at the scalar moment level does not supply the missing consistency.

A useful next obligation is therefore precise: exploit consistency between larger replica levels, or a valid additional physical inequality, to prove \(\ell_{n,m(n)}\ge-o(1)\) on an unbounded sequence of n. The prior gap dichotomy would then prove the full target. Proving that inequality is still the hard scientific task. No oracle, unproved positivity, finite-search sign, or entangled-reference co-Choi domination is used as a premise here.

## 5. Sources and verification boundaries

* Frozen B first-stage PROOF.md and HANDOFF.md: full-domain Gamma reduction, inadequate exponential bound, absolute-versus-relative opposition, and failure of Hamming-ball coverage retained.
* Pinned Astra N525 and complete `updates/BQ/package/supplied/werner_projection_research/RESEARCH_PROOF.md`, source SHA256 `9b15f562766a5622fd971730a05d056cc5f5ae12c7729f186fcca33d26d905a3`: exact projection completeness and persistent gap. This source was reread completely.
* Pinned Astra N525 `shadow_lp.py` and `shadow_lp_receipt.json`: prior finite two-replica weight-enumerator/shadow outer relaxation already has negative nonphysical optima. The present obstruction imposes **all four-replica whole-permutation characters** and constructs an exact PSD state, rather than claiming that prior diagnostic is a new result.
* The supplied AV, BC, BD and CT scientific texts were consulted for the crossed-versus-ordinary swap distinction, product/support restrictions, entangled-reference certificate failure, and rank/zero-manifold obstructions. They furnish no all-copy premise.
* Christandl, König, Mitchison, Renner, *One-and-a-half quantum de Finetti theorems*, [arXiv:quant-ph/0602130v4](https://arxiv.org/pdf/quant-ph/0602130), Theorem II.7 and its proof through symmetric purification; the full-trace-norm convention was independently accounted for above. Only this established finite approximation is imported from the paper.

`verify.py` reconstructs the local physical representations, exact Gram metrics, both invariant subspaces, every one of the 24 permutation characters, and the negative relaxed objective using SymPy rational arithmetic. It also checks the spectral rigidity rounding inequality algebraically and the exact hierarchy scaling. `verification.json` records the results. These checks validate the displayed finite construction; the complete mathematical arguments are above. The small numerical S4 probe was exploratory; its output is not a positivity certificate or an endpoint witness.
