# Weighted reachability and the onset of information loss

The strongest result of this investigation is a finite algebraic description of the onset of Astra's Choi deficit, together with a sharp comparison to an established CP-replacer coefficient. The description explains the reported cubic versus quintic amplitude-damping behavior and gives an exact algorithm in dense Hilbert-space dimension. A coding-theoretic reduction shows why the corresponding quantitative problem becomes hard for succinct many-qubit generators, even with a positive spectral gap.

These results do not establish a discovery of historic 9–10/10 significance. No major open problem is resolved. In particular, the onset mechanism has the same support condition and fixed-dimension exponent as positive quantum Doeblin minorization. Its general interpretation as an exact entropy contraction coefficient still depends on N402. The mathematical statements about the Choi objective below do not require N402. Historical novelty of the derived statements is unresolved.

The repository input is pinned to [`d40cec82e99a441ad5754e1590ca036e4e2bd237`](https://github.com/harjassand/astra-research-knowledge/tree/d40cec82e99a441ad5754e1590ca036e4e2bd237), retrieved on 10 October 2026. The relevant source seeds are [N402](https://github.com/harjassand/astra-research-knowledge/blob/d40cec82e99a441ad5754e1590ca036e4e2bd237/frontier/dossiers/N402.txt) and the [subsequent orthogonal-unitary calculation](https://github.com/harjassand/astra-research-knowledge/blob/d40cec82e99a441ad5754e1590ca036e4e2bd237/updates/CW/package/N402_foundational_extension_2026-10-10.tex). The newer weighted-filtration observation supplied in the request is treated as a clue and reconstructed below.

## The exact objects

Let \(J\geq0\) act on \(A\otimes B\), with \(d=\dim A\). For a channel, use the unnormalized Choi convention \(\operatorname{Tr}_B J=I_A\). Define

\[
 M(J)=\min_{\substack{\sigma\geq0,\ \operatorname{Tr}\sigma=1\\
 \operatorname{ran}(I_A\otimes\sigma)\subseteq\operatorname{ran}J}}
 \left\|\operatorname{Tr}_B[(I_A\otimes\sigma)J^+(I_A\otimes\sigma)]\right\|_\infty,
 \qquad \beta(J)=M(J)^{-1}.
\]

An empty feasible set means \(M=+\infty\) and \(\beta=0\). Here \(J^+\) is the Moore–Penrose inverse. Define, separately,

\[
 \alpha_+(J)=\max\{\operatorname{Tr}H:H\geq0,\ I_A\otimes H\leq J\}.
\]

For a channel, \(\alpha_+\) is exactly its largest physical replacer weight: \(\mathcal N=\alpha_+\mathcal R_\tau+(1-\alpha_+)\mathcal Q\), with \(\mathcal Q\) CPTP. The positivity requirement on \(H\) matters: the more recent Doeblin literature also defines a different coefficient using arbitrary Hermitian \(H\). Our coefficient is its \(\alpha_+\), as in [Definition 7 and equation 3.25](https://arxiv.org/html/2503.22823v2#S3.SS3).

N402 asserts that certain complete relative-entropy and conditional-information contraction coefficients equal \(1-\beta\). That assertion is not used as a premise in the linear-algebraic proofs here.

## A closed expression for the exponent and a sharp baseline comparison

Define the largest complete output subspace

\[
 E(J)=\{b\in B:A\otimes b\subseteq\operatorname{ran}J\}
 =\ker\operatorname{Tr}_A P_{\ker J}.
\]

Let \(P_E\) denote its orthogonal projection. If \(E\neq0\), put

\[
 K_E=\left.P_E(\operatorname{Tr}_A J^+)P_E\right|_E,
 \qquad h(J)=\operatorname{Tr}_E K_E^{-1}.
\]

Set \(h(J)=0\) when \(E=0\).

**Theorem 1.** For every finite positive semidefinite \(J\),

\[
 h(J)\leq\beta(J)\leq d\,h(J),
 \qquad
 \boxed{\alpha_+(J)\leq\beta(J)\leq d^2\alpha_+(J).}
\]

Consequently, \(\beta>0\), \(\alpha_+>0\), and \(E(J)\neq0\) are equivalent. For any family with fixed input dimension, \(\alpha_+\), \(\beta\), and \(h\) have the same power-law onset exponent whenever that exponent exists.

**Proof of the expression for \(E\).** For every \(b\),

\[
 \langle b,\operatorname{Tr}_A P_{\ker J}b\rangle
 =\sum_a\|P_{\ker J}(|a\rangle\otimes b)\|^2.
\]

This vanishes precisely when all \(|a\rangle\otimes b\) lie in \(\operatorname{ran}J\). Thus a density \(\sigma\) is feasible exactly when its range lies in \(E\). On that subspace, \(K_E\) is positive definite.

**Proof of the bounds using \(h\).** For every feasible \(\sigma\), define the positive operator

\[
 T_\sigma=\operatorname{Tr}_B[(I\otimes\sigma)J^+(I\otimes\sigma)].
\]

Its trace is \(\operatorname{Tr}(K_E\sigma^2)\), and
\(\operatorname{Tr}T_\sigma/d\leq\|T_\sigma\|_\infty\leq\operatorname{Tr}T_\sigma\).
Hilbert–Schmidt Cauchy–Schwarz gives

\[
 1=(\operatorname{Tr}\sigma)^2
 \leq\operatorname{Tr}K_E^{-1}\operatorname{Tr}(K_E\sigma^2).
\]

Equality holds at \(\sigma_0=K_E^{-1}/\operatorname{Tr}K_E^{-1}\). Minimizing the trace bounds therefore gives
\(1/(dh)\leq M\leq1/h\), which is the first assertion. No commutation hypothesis on the optimizing density was assumed.

**Proof that \(\alpha_+\leq\beta\).** If \(J\geq a(I\otimes\sigma)\), then the block matrix

\[
 \begin{pmatrix}J&I\otimes\sigma\\I\otimes\sigma&(I\otimes\sigma)/a\end{pmatrix}
\]

is positive: subtract \(\operatorname{diag}(J-aI\otimes\sigma,0)\), and the remaining block is a positive scalar \(2\times2\) matrix tensored with \(I\otimes\sigma\). This is a feasible certificate for \(M\leq1/a\), including singular \(J\). Optimize over \(a\).

**Proof that \(\beta\leq d^2\alpha_+\).** First assume \(J>0\), and set \(T=J^{-1}\), \(K=\operatorname{Tr}_A T\). The elementary bipartite inequality

\[
 T\leq d\,I_A\otimes\operatorname{Tr}_A T
\]

follows by decomposing \(T\) into rank-one terms and using the Schmidt rank bound \(\operatorname{SchmidtRank}(v)\leq d\) on each term. Inverting gives
\(J\geq d^{-1}I_A\otimes K^{-1}\). Thus \(\alpha_+\geq h/d\), while \(\beta\leq dh\).

For general \(J\), apply the matrix inequality to \(J+\varepsilon I\) and let \(\varepsilon\downarrow0\). The corresponding inverse marginal is
\(\varepsilon^{-1}\operatorname{Tr}_A P_{\ker J}+\operatorname{Tr}_A J^++O(\varepsilon)\).
Its inverse converges to \(P_EK_E^{-1}P_E\). Taking limits in the feasible matrix inequality gives \(J\geq d^{-1}I_A\otimes P_EK_E^{-1}P_E\), and hence \(\alpha_+(J)\geq h(J)/d\). The already proved singular harmonic bound completes the result. \(\square\)

**The factor \(d^2\) is optimal.** For an orthogonal unitary error basis with probabilities \(p_g>0\), the source calculation gives

\[
 \beta=\frac{d^4}{\sum_g p_g^{-1}},\qquad
 \alpha_+=d^2\min_g p_g.
\]

The second identity follows by testing the Choi constraint on every maximally entangled error-basis vector, and is attained by a scalar \(H\). Let one probability be \(\varepsilon\) and keep the others bounded away from zero. Then \(\beta/\alpha_+\to d^2\).

This theorem is the decisive limitation on an interpretation of row completion as an entirely new onset phenomenon: the established positive CP-replacer geometry already has exactly the same onset. The comparison is only by dimension-dependent constants. It does not identify the coefficients, and the factor is exponential in qubit count.

## An exact algorithm for a supplied rational Choi family

The expression \(h\) can be evaluated without an SDP. For \(J(t)>0\), put \(A(t)=\operatorname{Tr}_A\operatorname{adj}J(t)\). Then

\[
 h(J(t))=\frac{\det J(t)\,\operatorname{Tr}\operatorname{adj}A(t)}{\det A(t)}.
\]

Therefore

\[
 \operatorname{ord}_{t=0}\beta
 =\operatorname{ord}\det J+
 \operatorname{ord}\operatorname{Tr}\operatorname{adj}A-
 \operatorname{ord}\det A.
\]

This is an equality of exponents, not of leading coefficients. It accounts for optimizing output states that move with time.

For a possibly singular supplied polynomial or rational family, form instead

\[
 \Delta(t,\varepsilon)=\det(J(t)+\varepsilon I),\qquad
 A(t,\varepsilon)=\operatorname{Tr}_A\operatorname{adj}(J(t)+\varepsilon I).
\]

Compute \(\Delta\operatorname{Tr}\operatorname{adj}A/\det A\), cancel its lowest \(\varepsilon\) powers, and take \(\varepsilon\downarrow0\). The result is exactly \(h(J(t))\). Its numerator and denominator valuations determine the onset, or the zero function certifies \(\beta\equiv0\). These are exact determinant and polynomial operations, with polynomial bit complexity in the dense dimensions, polynomial degrees, and input coefficient sizes. Positivity is an input promise. An exponentially represented Choi matrix is not a polynomial-size input to this procedure.

For \(J(t)\) arising from a supplied Lindblad generator, an efficient algebraic alternative is the weighted construction that follows.

## The weighted row completion theorem

Consider a finite-dimensional Lindblad generator

\[
 \mathcal L(X)=GX+XG^*+\sum_{j=1}^mL_jXL_j^*,
 \qquad G=-iH-\tfrac12\sum_jL_j^*L_j.
\]

Let \(\delta(X)=[G,X]\). Starting from \(F_0=\operatorname{span}\{I\}\) and \(F_{-1}=0\), define

\[
 F_r=F_{r-1}+\sum_jL_jF_{r-1}+\delta(F_{r-2})\quad(r\geq1).
\]

Equivalently, \(F_r\) is spanned by \(I\) and products

\[
 (\delta^{k_n}L_{i_n})\cdots(\delta^{k_1}L_{i_1}),
 \qquad n+2\sum_\ell k_\ell\leq r.
\]

The equivalence follows by the derivation rule for \(\delta\); conversely, apply \(\delta\) to a product and subtract its other differentiated factors to obtain each required left factor. Thus a jump has weight one and a drift commutator has weight two.

For any matrix subspace \(F\subseteq M_d(\mathbb C)\), define its complete row subspace

\[
 S(F)=\{b\in\mathbb C^d:|b\rangle\langle x|\in F\text{ for every }x\in\mathbb C^d\}.
\]

Let \(r_*\) be the first \(r\) for which \(S(F_r)\neq0\), or \(+\infty\) if no such \(r\) exists.

**Theorem 2.** If \(d>1\), then either \(r_*=+\infty\) and
\(\beta(e^{t\mathcal L})=\alpha_+(e^{t\mathcal L})=0\) for every \(t>0\), or

\[
 \boxed{\beta(e^{t\mathcal L})=\Theta(t^{r_*}),\qquad
 \alpha_+(e^{t\mathcal L})=\Theta(t^{r_*}),\qquad
 1\leq r_*\leq2d^2-3.}
\]

The constants concern one fixed supplied generator as \(t\downarrow0\). The exponent is exactly computable in polynomial bit complexity from Gaussian-rational \(H,L_j\), in dense dimension \(d\) and their input bit lengths. This does not compute an exact leading prefactor, a uniform interval of validity, or a polynomial-in-qubit-count representation.

**Proof, trajectory expansion and the drift correction.** The \(n\)-jump trajectory with \(0<s_1<\cdots<s_n<t\) is

\[
 e^{(t-s_n)G}L_{i_n}e^{(s_n-s_{n-1})G}\cdots L_{i_1}e^{s_1G}
 =e^{tG}\prod_{\ell=n}^{1}(e^{-s_\ell\delta}L_{i_\ell}).
\]

The Choi matrix is the sum over words of the integrals of the outer products of their vectorizations, together with the no-jump term. Remove the invertible output factor \(e^{tG}\), and substitute \(s_j=tu_j\). A jump sector contributes a factor \(t^n\), while its Taylor coefficient of total degree \(k\) is a polynomial of degree \(k\) in the ordered times, with operator coefficient in \(F_{n+2k}\). Squaring amplitudes explains the weight \(n+2k\).

Put \(F=\bigcup_rF_r\), \(V_r=F_r\ominus F_{r-1}\), and let \(P_r\) project onto the vectorized \(V_r\). The drift-removed Choi matrix \(\widetilde J(t)\) satisfies, on \(F\),

\[
 c\sum_rt^rP_r\ \leq\ \widetilde J(t)\ \leq\ C\sum_rt^rP_r
 \tag{*}
\]

for sufficiently small positive \(t\), with constants \(0<c\leq C<\infty\).

To prove (*), conjugate \(\widetilde J(t)\) by \(\sum_rt^{-r/2}P_r\). In each fixed jump sector its normalized amplitude has a finite limit. Its layer \(r\) is a homogeneous polynomial of degree \((r-n)/2\), or zero if this is not a nonnegative integer. Suppose a vector annihilates the limiting Gram form. Every such polynomial must vanish on the open ordered-time simplex. Different homogeneous degrees cannot cancel there, and distinct monomials have independent coefficients. For each \(r\), the exact-weight operator coefficients span \(V_r\) after projection. Thus the vector has zero component in every \(V_r\), proving that the limiting Gram form is positive definite. Finite-dimensional convergence gives (*). The infinite jump tail tends to zero after normalization: bounded \(L_j,G\), the simplex volume \(1/n!\), and the factor \(t^{n-r_{\max}}\) dominate it. Analyticity also shows that the exact support of \(\widetilde J(t)\) is \(F\) for every \(t>0\).

This step is indispensable. Freezing a Choi eigenspace at \(t=0\) can miss leakage into a much smaller eigenvalue. Removing the trajectory drift and retaining the full weighted Gram form accounts for it.

**Proof, why the first complete row is the exponent.** Write \(D(t)=\sum_rt^rP_r\). If \(b\in S(F_{r_*})\) is a unit vector, then
\(I\otimes|b\rangle\langle b|\leq P_{F_{r_*}}\leq t^{-r_*}D(t)\) for \(0<t\leq1\). Hence \(\alpha_+(D(t))\geq t^{r_*}\).

For the reverse inequality, let \(Q\) project onto \(F_{r_*-1}^{\perp}\) in the full matrix space. Since \(S(F_{r_*-1})=0\), the matrix \(\operatorname{Tr}_A Q\) is positive definite. If \(I\otimes H\leq D(t)\), taking the trace against \(Q\) gives

\[
 c_0\operatorname{Tr}H\leq
 \operatorname{Tr}[Q(I\otimes H)]\leq\operatorname{Tr}[QD(t)]=O(t^{r_*}).
\]

This proves \(\alpha_+(D(t))=\Theta(t^{r_*})\). Comparison (*) transfers this to \(\widetilde J\). Output congruence by \(e^{tG}\) changes \(\alpha_+\) by factors between its squared smallest and largest singular values, both tending to one. Finally use Theorem 1 to transfer the exponent to \(\beta\). If no complete row exists, the support criterion in Theorem 1 gives zero for every positive time.

**Proof, the cutoff and algorithm.** Ignore weights temporarily and close \(\operatorname{span}\{I\}\) under the linear maps \(X\mapsto L_jX\) and \(X\mapsto[G,X]\). A strictly growing chain has at most \(d^2-1\) enlargements. Every nonzero operator word starts with a multiplication by some \(L_j\), since \([G,I]=0\); its first operation costs one and subsequent operations cost at most two. Thus the limiting space is reached within weighted grade \(2d^2-3\).

Compute the displayed \(F_r\) recurrence by exact linear elimination. To test \(S(F_r)\), choose a basis \(Q_\ell\) of \(F_r^\perp\) and solve the linear equations
\(\langle Q_\ell,|b\rangle\langle x|\rangle_{\rm HS}=0\) for every matrix-unit input vector \(x\). Each stage handles at most \(d^2\) basis matrices and \(O(md^2)\) candidates; there are \(O(d^2)\) stages. One may retain actual operator words as basis representatives. Their lengths and rational coefficient bit sizes are polynomially bounded; exact elimination consequently has polynomial bit complexity. \(\square\)

The unweighted commutator algebra and support formula are already present in the quantum-semigroup literature: [Fagnola and Mora, Definition 1 and Theorem 3](https://arxiv.org/html/1405.6374v2) characterize supports through products of iterated \([G,\cdot]\)-commutators. The weighted Gram proof adds the order of vanishing and the complete-row optimization. This is a derived theorem whose historical novelty is unestablished, not a claim to have invented algebraic controllability.

## Exact examples and a consequence for sparse noise

For \(H=X/2\) and \(L=|0\rangle\langle1|\), the filtration dimensions at grades \(0,1,2,3,4,5\) are \(1,2,2,3,3,4\). The corresponding complete row dimensions are \(0,0,0,1,1,2\). Therefore \(r_*=3\), although the smallest Choi eigenvalue has order five.

The exact Taylor calculation gives

\[
 \det J\sim t^9/34560,\quad
 \det(\operatorname{Tr}_A\operatorname{adj}J)\sim t^{10}/34560,\quad
 \operatorname{Tr}\operatorname{adj}(\operatorname{Tr}_A\operatorname{adj}J)\sim t^4/12.
\]

Thus \(h\sim t^3/12\), and Theorem 1 gives \(\beta=\Theta(t^3)\). The characteristic-polynomial valuations give Choi eigenvalue orders \(0,1,3,5\). These exact statements reproduce the cubic/quintic separation without assuming the numerical Choi-SDP report or N402.

For \(H=X/2\), \(L=Z\), the first complete row appears only at grade four: the successive new directions are \(I,Z,Y,X\) at weights \(0,1,3,4\). The missing direction before weight four is an invertible Pauli matrix, so no nonzero complete row is present. Here \(h\sim(2/3)t^4\), the Choi eigenvalue orders are \(0,1,3,4\), and \(\beta=\Theta(t^4)\). The displayed coefficients are coefficients of \(h\), not asserted coefficients of \(\beta\).

An immediate general restriction is that \(m<d\) Lindblad jumps force \(r_*>1\), whenever \(r_*\) is finite. Indeed, \(F_1=\operatorname{span}\{I,L_1,\ldots,L_m\}\) has dimension at most \(m+1\). A complete nonzero row has dimension \(d\), and \(I\) is independent of that row for \(d>1\); hence row completion at grade one needs \(m+1\geq d+1\). Conditional on N402, sparse noise therefore cannot give a positive uniform complete all-pairs entropy rate \(\eta(e^{t\mathcal L})\leq e^{-\kappa t}\) from time zero. A positive spectral gap alone does not change this conclusion.

More generally, linear onset is generically absent at every deficient noise rank. Fix \(m<d^2-1\) and choose a generic \(m\)-dimensional traceless jump span. Its \(F_1^\perp\) contains an invertible matrix, which annihilates every possible complete row and forces \(S(F_1)=0\). To justify genericity, the exceptional condition that every matrix in \(F_1^\perp\) is singular is algebraic and proper: choose an invertible traceless \(B\), and choose the jump span inside the \((d^2-2)\)-dimensional space orthogonal to both \(I\) and \(B\). Then \(B\in F_1^\perp\) supplies a counterexample to that exceptional condition. Full traceless noise rank \(d^2-1\) gives \(F_1=M_d\) and hence linear onset. Rank-deficient reset generators with linear onset are exceptional configurations. This statement concerns exact generic subspaces, without a uniform numerical conditioning bound.

## A computational obstruction despite locality and a positive gap

Let \(A\in\mathbb F_2^{2n\times m}\) have Pauli labels \(s_j\) as its columns, and let

\[
 \mathcal L=\sum_j\gamma_j(\operatorname{Ad}P_{s_j}-\mathrm{id}),\qquad\gamma_j>0.
\]

Pauli conjugations commute. At time \(t\), this is the random-Pauli channel with label \(AE\), where the independent bits satisfy
\(\Pr(E_j=1)=(1-e^{-2\gamma_jt})/2\).

**Theorem 3.** Strict positivity of \(\beta(e^{t\mathcal L})\) for \(t>0\) is equivalent to \(\operatorname{rank}_{\mathbb F_2}A=2n\), and is decidable in \(O(n^2m)\) binary operations. When the rank is full, its onset exponent is

\[
 r(A)=\max_{g\in\mathbb F_2^{2n}}\min_{Ax=g}|x|
 =\rho(\ker A),
\]

the covering radius of the binary linear code \(\ker A\).

There exist absolute constants \(k\) and \(c>1\) for which the following promise problem is \(\Pi_2^P\)-complete: given rate-one Pauli jumps supported on at most \(k\) qubits, including every \(X_i,Z_i\), distinguish \(r\leq K\) from \(r>cK\). Every such generator has a unique maximally mixed stationary state and spectral gap at least two. Locality here means bounded operator support; geometric locality and bounded interaction degree are not promised.

**Proof of the exponent formula.** For each label put

\[
 \ell(g)=\min_{Ax=g}|x|,\qquad
 c_g=\sum_{\substack{Ax=g\\|x|=\ell(g)}}\prod_{j:x_j=1}\gamma_j.
\]

The exact Bernoulli formula gives \(p_t(g)=c_gt^{\ell(g)}+O(t^{\ell(g)+1})\). All labels have positive probability exactly when \(A\) has full row rank. In that case the orthogonal-unitary formula yields

\[
 \beta(e^{t\mathcal L})=
 \frac{2^{4n}}{\sum_{g:\ell(g)=r}c_g^{-1}}t^r+O(t^{r+1}),\qquad r=\max_g\ell(g).
\]

Representatives of syndrome \(g\) form one coset of \(\ker A\); the minimum Hamming weight in each coset is exactly \(\ell(g)\). Taking the worst coset proves the covering-radius identity. No entropy equality is needed.

**Proof of the hardness transfer.** Membership follows from the quantified polynomial predicate

\[
 r\leq K\quad\Longleftrightarrow\quad
 \forall g\ \exists x:\ Ax=g\text{ and }|x|\leq K.
\]

The hardness premise is [Guruswami, Micciancio and Regev, Theorem 5.5](https://cims.nyu.edu/~regev/papers/crp.pdf): binary covering radius has a \(\Pi_2^P\)-hard constant-factor promise gap. Their construction on printed pages 22–24 produces a full-row-rank check matrix \(H\), contains every unit column, and has column weight at most \(B+2\), for an absolute bounded-occurrence constant \(B\). These properties follow directly from its five column groups; its output size is polynomial because \(B\) is fixed.

On \(R\) qubits, where \(R\) is the number of rows of \(H\), use the jumps \(X^{h_j}\) and \(Z^{h_j}\), with labels forming \(A=H\oplus H\). Their support is at most \(k=B+2\), and the unit columns supply all \(X_i,Z_i\). Identical columns may be deduplicated: a minimum-weight syndrome representative never needs two identical columns. For syndrome pairs,

\[
 \ell_A(u,v)=\ell_H(u)+\ell_H(v),\qquad
 r(A)=2\rho(\ker H).
\]

Map a covering-radius threshold \(D\) to \(K=2D\). The multiplicative promise gap is preserved exactly. This proves hardness without a hidden exponentially long noise list.

Finally every Pauli eigenoperator satisfies

\[
 \mathcal L(P_g)=-2\#\{j:[g,s_j]_{\rm symp}=1\}\,P_g.
\]

Each nonidentity Pauli anticommutes with at least one supplied single-qubit \(X_i\) or \(Z_i\), so all nontrivial eigenvalues are at most \(-2\). Only the identity is fixed. This proves the stationary-state and gap promises. \(\square\)

This transfers an established hardness theorem to a quantum onset problem; it does not prove a new separation of complexity classes. It rules out a general deterministic polynomial-time algorithm for the stated promise problem unless \(P=\Pi_2^P\). It also does not establish hardness of fixed-time additive estimation of \(\beta\): an order of vanishing can depend on a very small signal.

The easy rank test and hard radius sharply separate qualitative reachability from quantitative onset. Theorem 1 shows that the obstruction also applies to the positive CP-Doeblin onset. Conditional on N402 it transfers to the corresponding entropy/CMI onset.

**An exact subclass and finite example.** If the \(2n\) labels are independent, then

\[
 \beta(e^{t\mathcal L})=\prod_{j=1}^{2n}(1-e^{-4\gamma_jt}).
\]

This follows by factoring \(\sum_gp_t(g)^{-1}\) over the independent Bernoulli coordinates. For
\(H=[e_1,e_2,e_3,e_1+e_2+e_3]\), the three-qubit generator with its X and Z labels has radius \(r=4\), spectral gap four, and
\(\beta(t)=(16384/9)t^4+O(t^5)\). There are nine deepest label pairs, each with four shortest representatives, which gives the coefficient directly.

## What exact input access changes

The dense and succinct input contracts cannot be interchanged. Suppose instead that a Boolean circuit samples a Pauli label by mapping uniform random bits to \(2n\) output bits. Then \(\beta>0\) is exactly circuit surjectivity, a \(\Pi_2^P\)-complete property. A direct reduction maps \(\forall y\exists z\,\varphi(y,z)\) to
\(C(y,z,b)=(y,b\wedge\varphi(y,z))\); copy an extra free bit if needed to make the output length even. Every \((y,0)\) is reached, while \((y,1)\) is reached precisely when the existential witness exists.

Exact coefficient evaluation is already \(\#P\)-hard for a succinct single-qubit Pauli channel. If \(q=\#\mathrm{SAT}(\varphi)/2^m\), a small sampler realizes probabilities

\[
 ((2-q)/4,\ 1/4,\ 1/4,\ q/4),\qquad
 \beta=\frac{2q(2-q)}{1+q(2-q)}.
\]

An exact value determines \(q\in[0,1]\) uniquely and hence the satisfying-assignment count. The formula has polynomial-size exact rational output; recovery uses integer square root after rational rearrangement. Thus an efficient dense Choi optimization does not remove the cost of acquiring its entries from a succinct sampler.

## The stationary support criterion

The qualitative geometry admits a structural characterization beyond full Choi rank. Let
\(\mathscr A=\operatorname{alg}\{\operatorname{ad}_G^k(L_j):k\geq0\}\), including the identity.

**Theorem 4.** Positive \(\beta(T_t)\), equivalently positive \(\alpha_+(T_t)\), at one or every positive time holds exactly when the semigroup has a unique invariant density \(\rho\) and its support projection \(P\) belongs to \(\mathscr A\). In that case,

\[
 S(\mathscr A)=\operatorname{ran}\rho,
 \qquad P\mathscr A=\operatorname{Hom}(\mathbb C^d,\operatorname{ran}\rho).
\]

The feasible output densities in the Choi optimization are exactly all densities on this stationary support, at every positive time.

**Proof.** The trajectory support proof gives \(\mathscr K_t=e^{tG}\mathscr A\). Put \(R=S(\mathscr A)\). It is invariant under \(\mathscr A\) by left multiplication. It is also \(G\)-invariant because

\[
 |Gb\rangle\langle x|=[G,|b\rangle\langle x|]+|b\rangle\langle G^*x|\in\mathscr A.
\]

Thus \(e^{tG}R=R\), and the complete row space of \(\mathscr K_t\) is exactly \(R\). This proves the all-positive-time dichotomy and the claimed feasible face.

Suppose \(R\neq0\). The semigroup restricts to a CPTP semigroup on \(R\), which has an invariant density. Its support is \(R\): any stationary support is invariant under \(G,L_j\), hence under \(\mathscr A\), while \(\mathscr A|_R=\operatorname{End}(R)\). A positive replacer component at any fixed time contracts the trace norm of traceless Hermitian matrices by a factor strictly below one. It therefore makes the invariant density globally unique. Its support projection has range in \(R\) and belongs to \(\operatorname{Hom}(\mathbb C^d,R)\subseteq\mathscr A\).

Conversely, suppose \(\rho\) is unique and \(P\in\mathscr A\). Its support \(S\) is \(G,L_j\)-invariant. To see the standard support fact directly, stationarity tested on vectors orthogonal to \(S\) forces each \(L_jS\subseteq S\); the off-diagonal stationary equation then forces \(GS\subseteq S\). The restricted semigroup has a unique faithful invariant state and is irreducible, since any proper invariant subspace would support another stationary density. The established finite-dimensional transitivity theorem, followed by Burnside's theorem, gives \(P\mathscr AP=\operatorname{End}(S)\). The QMS transitivity implication is [Fagnola and Mora, Theorem 6](https://arxiv.org/html/1405.6374v2).

Let \(W=P\mathscr A\) and \(Z=\bigcap_{a\in\mathscr A}\ker(Pa)\). The subspace \(Z\) is \(\mathscr A\)-invariant. It is \(G\)-invariant as well: for \(w=Pa\), \([G,w]\in P\mathscr A\), so \(wGz=Gwz-[G,w]z=0\). If \(Z\neq0\), it supports a stationary density. But \(P\in W\) forces \(Z\subseteq\ker P\), contradicting uniqueness. Hence \(Z=0\).

The space \(W\subseteq\operatorname{Hom}(\mathbb C^d,S)\) is stable under all left matrix units in \(\operatorname{End}(S)\). It therefore equals \(S\otimes U\) for some subspace \(U\) of the input dual: matrix units isolate any row and move it to any other output row. Its common kernel is the annihilator of \(U\). Since that kernel is zero, \(U\) is the entire input dual and \(W=\operatorname{Hom}(\mathbb C^d,S)\). Thus \(S\subseteq R\), and the necessity argument identifies \(R=S\). \(\square\)

For undriven amplitude damping, \(\mathscr A=\operatorname{span}\{I,|0\rangle\langle1|\}\): its invariant state is uniquely \(|0\rangle\langle0|\), but that projector is absent from \(\mathscr A\). Accordingly \(\beta=0\) at every finite time. Adding a reset jump supplies the missing projector. This explains why unique relaxation to a pure state is insufficient for strict complete contraction of the proposed kind.

## An exact family with two jumps and arbitrarily high onset

For \(d\geq2\), let

\[
 N=\sum_{i=1}^{d-1}|i-1\rangle\langle i|,\qquad
 P_0=|0\rangle\langle0|,\qquad L_1=N,\quad L_2=P_0,\quad H=0.
\]

Then \(G=-I/2\), \(\mathcal L=\Phi-\mathrm{id}\), where
\(\Phi(X)=NXN^*+P_0XP_0\), and \(\Phi^{d-1}=\mathcal R_{P_0}\). The invariant density is uniquely \(P_0\); the only generator eigenvalues are zero and minus one, with possible growing Jordan blocks at minus one. Its spectral gap is one.

The noise algebra is

\[
 \operatorname{span}\{I,N,\ldots,N^{d-1},P_0,P_0N,\ldots,P_0N^{d-2}\},
\]

of dimension \(2d-1\), with complete row space \(\mathbb C|0\rangle\). Its first complete row appears at grade \(d-1\). More strongly, at every time,

\[
 \boxed{\beta(T_t)=\alpha_+(T_t)=q_{d-1}(t)
 =1-e^{-t}\sum_{j=0}^{d-2}\frac{t^j}{j!}.}
\]

**Proof of the exact coefficient.** Poissonization gives
\(T_t=\sum_{k=0}^{d-2}p_k\Phi^k+q_{d-1}\mathcal R_{P_0}\), with \(p_k=e^{-t}t^k/k!\). Write \(e_k=|E_{0k}\rangle\!\rangle\) and \(u_k=|N^k\rangle\!\rangle-e_k\). Orthogonal superdiagonals split the Choi matrix into blocks

\[
 p_k|e_k+u_k\rangle\langle e_k+u_k|+a_k|e_k\rangle\langle e_k|,
 \quad 0\leq k\leq d-2,\qquad
 a_k=\Pr(\operatorname{Poisson}(t)\geq k+1),
\]

and the last scalar block \(q_{d-1}|e_{d-1}\rangle\langle e_{d-1}|\). Each \(u_k\) is nonzero and orthogonal to \(e_k\). Its two-dimensional Schur complement gives \(\langle e_k,J^+e_k\rangle=1/a_k\). The sole feasible output density is \(P_0\). Its inverse form is diagonal with entries \(a_k^{-1}\), and last entry \(q_{d-1}^{-1}\); the maximum is \(q_{d-1}^{-1}\). The same Schur complements give exactly \(H\leq q_{d-1}P_0\) for positive replacer feasibility. This proves both equalities.

Consequently \(\beta(t)=t^{d-1}/(d-1)!+O(t^d)\). The unbounded onset is compatible with the fixed gap because Jordan transients grow with dimension. The family also has a classical absorbing-chain interpretation; it is an exact illustration of the principle, not a new mixing-time phenomenon.

## A classical counterexample to analytic optimized expansions

The exponent is an integer for the finite Lindblad construction. An analytic channel does not, however, force the optimized value to have an ordinary integer-power Taylor expansion.

For a strictly positive classical channel,

\[
 M(P)=\min_{\sigma\in\Delta(Y)}\max_x\sum_y\frac{\sigma_y^2}{P_{xy}},\qquad
 \beta(P)=\min_{\lambda\in\Delta(X)}\sum_y
 \left(\sum_x\frac{\lambda_x}{P_{xy}}\right)^{-1}.
\]

The dual follows by convex minimax and weighted Cauchy–Schwarz; the minimizing density for a fixed \(\lambda\) is proportional to the reciprocal denominators. Classical-input off-diagonal density entries can be removed by output dephasing, so this also is the full Choi objective for the associated classical channel.

If \(P_{xy}(t)\sim c_{xy}t^{d_{xy}}\), put \(r=\min_y\max_xd_{xy}\) and \(C=\{y:\max_xd_{xy}=r\}\). Then

\[
 \beta(P(t))=B_0t^r(1+O(\sqrt t)),\qquad
 B_0^{-1}=\min_{s\in\Delta(C)}\max_x
 \sum_{\substack{y\in C\\d_{xy}=r}}\frac{s_y^2}{c_{xy}}.
\]

Indeed a trial density on \(C\) bounds the scaled optimum. Every noncentral mass obeys \(\sigma_y=O(t^{(\max_xd_{xy}-r)/2})\), from its own worst row. Dropping these masses and renormalizing gives the matching lower bound with \(O(\sqrt t)\) error. For a Markov semigroup, \(d_{xy}\) is directed shortest-path length, so \(r\) is directed in-radius. The classical baseline is \(\alpha_+=\sum_y\min_xP_{xy}\), and \(\alpha_+\leq\beta\leq|X|\alpha_+\), so the exponent is again shared with Doeblin.

The square-root error can occur. Consider the irreducible generator

\[
 Q=\begin{pmatrix}-1&0&1\\1&-1&0\\2&1&-3\end{pmatrix}.
\]

Its unique center is output zero, with \(r=B_0=1\), yet

\[
 \boxed{\beta(e^{tQ})=t+\sqrt2\,t^{3/2}+O(t^2).}
\]

**Proof.** The relevant transition orders are

\[
 P(t)=\begin{pmatrix}
 1+O(t)&t^2(1+O(t))/2&t(1+O(t))\\
 t(1+O(t))&1+O(t)&t^2(1+O(t))/2\\
 2t(1+O(t))&t(1+O(t))&1+O(t)
 \end{pmatrix}.
\]

The primal optimizer converges to \((1,0,0)\), and its third-row objective, multiplied by \(t\), converges to \(1/2\), while the optimum converges to one. Thus the third row is inactive for small \(t\), and an optimal dual has \(\lambda=(s,1-s,0)\). Necessarily \(s\to0\). Its three reciprocal terms are, uniformly near \(s=0\),

\[
 H_0=\frac{t}{1-s}(1+O(t)),\qquad
 H_1=\frac{t^2}{2s+t^2}(1+O(t)),\qquad H_2=O(t^2).
\]

The trial \(s=\sqrt{t/2}\) gives the claimed upper bound. The lower bounds \(H_0\geq t(1+s)-O(t^2)\) and \(H_1\geq(1-O(t))t^2/(2s+t^2)\) force every optimal \(s\) to be bounded above and below by positive multiples of \(\sqrt t\). Write \(s=L\sqrt t\). Uniformly on that range,

\[
 H_0+H_1+H_2=t+t^{3/2}\left(L+\frac1{2L}\right)+O(t^2).
\]

The bracket has minimum \(\sqrt2\) at \(L=1/\sqrt2\), proving the result. The primal density has \(\sigma_1\sim\sqrt{t/2}\), \(\sigma_2\sim t/2\). A noncentral output therefore changes the first correction. \(\square\)

## What the investigation establishes

The indispensable mathematical ingredient is the weighted trajectory Gram form: homogeneous jump-time polynomials prevent cancellation between distinct weighted layers. Complete row generation, rather than the last Choi eigenvalue, selects the onset. The inverse marginal supplies a second, exact symbolic route that automatically retains moving output directions.

The strongest capabilities established are:

| Result | Actual capability | Boundary |
|---|---|---|
| Weighted row theorem | Exact onset exponent from finite matrix-space closure | Polynomial in dense Hilbert dimension |
| Stationary support criterion | Exact qualitative strictness criterion including singular invariant states | Uses the standard QMS transitivity theorem |
| Inverse marginal | SDP-free symbolic onset for supplied rational Choi families | Does not provide exact coefficient or physical acquisition |
| Pauli covering-radius reduction | Hardness despite bounded jump support and a positive gap | Transfers established coding hardness; geometric locality is open here |
| Exact cascade and qubit examples | Explicit coefficients and separations from smallest-eigenvalue order | Concrete families, not a major-open-problem solution |
| Half-power Markov example | Counterexample to analytic optimized-value expansions | Leading exponent remains the classical in-radius |

All displayed proofs concern finite matrices with supplied exact descriptions. The examples provide separate exact arithmetic evidence for their stated scope. None is a formal proof-kernel certificate or external mathematical review. The coding-hardness premise and the QMS transitivity theorem are explicitly imported; N402 is required only for the asserted entropy/CMI identification. Historical priority is unresolved.

The decisive test in the mission is **not met**. The onset clue has yielded a general theorem and a concrete computational obstruction, but its support and exponent reduce to established positive CP-Doeblin geometry. The exact coefficient can still improve constants and thresholds when dimension grows; that is where an additional capability would have to be demonstrated. It has not supplied a general algorithm that bypasses covering-radius hardness, solved a major open problem, or established transformative consequences beyond the original domain.

The remaining mathematical gaps are specific: independent resolution of N402's universal entropy equality; exact leading prefactors for general noncommuting generators; a sharp universal row-grade bound; and the complexity of the onset problem under geometric locality and bounded interaction degree. These are unresolved questions, rather than results claimed by this report.

## Reproducible files

- `weighted_onset.py` implements exact weighted closure and row-kernel extraction for supplied Gaussian-rational generators, and prints five built-in examples.
- `weighted_onset_results.json` records those results, including undriven amplitude damping's zero-deficit case.
- `exact_examples.py` and `exact_examples.json` construct the qubit Choi Taylor coefficients exactly and extract the characteristic-polynomial valuations and determinant ratios.
- `pauli_onset_checks.py` and `pauli_onset_checks.json` verify the finite code example, its gap and prefactor, exact probability factorizations, and the counting reduction at finite rational inputs.

Run `python3 weighted_onset.py` or `python3 weighted_onset.py generator.json`; SymPy is required. The input schema and exact entry format are in the script. `pauli_onset_checks.py` uses only the Python standard library. These checks support the fixtures; the universal statements rest on the proofs above.
