# Full unitary orbits: a sharp finite-horizon memory exponent

**Status:** Derived after the spherical note in the same session. Complete analytical argument below; separate finite algebraic/numerical checks are supplied. Not independently audited, formally verified, or priority-certified. The fixed-alphabet problem remains unresolved in this investigation.

This extension strengthens the one-qubit example to arbitrary fixed Hilbert-space dimension. It does **not** infer that a conditional mean of pure states is still pure. The uniform spectral-orbit estimate in Section 3 is needed precisely to avoid that invalid shortcut.

## 1. Process and result

Fix D>=2, write n=D^2-1 and r_0=sqrt((D-1)/D), and let H_0(D) be the n-dimensional real Hilbert space of traceless Hermitian D-by-D matrices with Hilbert-Schmidt inner product Tr(AB). Let

\[
K_D=\{A_\rho=(\rho-I/D)/r_0:\ \rho\succeq0,\ \operatorname{Tr}\rho=1\}.
\]

It is a compact convex subset of the unit Hilbert-Schmidt ball; its pure-state extreme points have norm one. Given A in K_D, a sequence U_1,...,U_t of supplied unitaries, V_t=U_t...U_1, and B in the unit ball of H_0(D), define

\[
p_*(+\mid A,U_1,\ldots,U_t,B)
=\tfrac12\bigl(1+\delta\operatorname{Tr}(B V_t A V_t^*)\bigr).
\tag{1.1}
\]

Assume 0<delta<=1/n. This is an actual quantum process on C^D: prepare rho=I/D+r_0 A, apply the unitaries, and measure the binary effect

\[
E_B=\tfrac12(I+\delta B/r_0).
\]

Since ||B||_op<=||B||_HS<=1 and delta<=r_0, the effect lies between zero and identity. Its Born probability is (1.1).

A classical simulator has the same charged Markov-memory contract as the main note, now with P_t(U) arbitrary measurable stochastic matrices. Preparations, all terminal queries and all gate words of length at most T must be approximated uniformly.

**Theorem Q.** For fixed D>=2, 0<delta<=1/(D^2-1), and

\[
0<\epsilon<\frac{\delta}{2(D^2-1)},
\]

the least number of classical states satisfies

\[
\boxed{m_*(T;D,\delta,\epsilon)=\Theta_{D,\delta,\epsilon}(T^{D-1}).}
\tag{1.2}
\]

The static preparation/readout family has minimum positive factorization size exactly D^2. The quantum realization has fixed Hilbert-space dimension D.

Consequently the minimal classical bit count satisfies

\[
\lceil\log_2m_*\rceil=(D-1)\log_2T+O_{D,\delta,\epsilon}(1).
\tag{1.3}
\]

This is a fixed-D asymptotic statement. It is not a uniform joint bound in D,T,delta,epsilon, not a gate-compilation complexity result, and not a general computational quantum speedup.

## 2. Representation-compatible coefficient

Define

\[
\kappa_{m,D}=\sup_{\substack{A\in H_0(D)\\\|A\|_{HS}=1}}
\sup_{\substack{B_1,\ldots,B_m\in H_0(D)\\\|B_j\|_{HS}=1}}
\int_{U(D)}\max_j\operatorname{Tr}(B_j UAU^*)\,dU.
\tag{2.1}
\]

The supremum is attained. As in the spherical note, allowing norm-at-most-one B_j does not increase it. The same conditional-mean proof applies to the orthogonal representation A -> UAU^*. For independent Haar unitaries and unnormalized conditional means

\[
b_i(t)=\mathbb E[V_t A V_t^*\mathbf1_{\{S_t=i\}}],\quad
R_t=\sum_i\|b_i(t)\|_{HS},
\]

one has

\[
R_t\le\kappa_{m,D}R_{t-1}.
\tag{2.2}
\]

Indeed b_j(t)=sum_i integral U b_i(t-1) U^* P_t(U)(i,j)dU. Align unit B_j with the integrals for each fixed i, then bound their sum by the maximum in (2.1), exactly as in Theorem 4.1 of the main note. This covers every spectrum of every conditional mean.

The corresponding adjoint transfer is

\[
(\mathcal A_P z)_i=\int U^*\Bigl(\sum_jP_U(i,j)z_j\Bigr)U\,dU.
\]

The identity of this operator with a representation transform is not a novelty claim. In contrast with the spherical case, equality R_T=kappa^T for all T is **not** asserted.

## 3. Uniform spectral-orbit geometry

**Lemma Q1 (Grassmann small balls).** For each fixed D and k=1,...,D-1, let Q be the orthogonal projection onto a uniformly distributed complex k-dimensional subspace of C^D. For any fixed rank-k projection P,

\[
\Pr(\|Q-P\|_{HS}\le s)\asymp_{D,k}s^{2k(D-k)}
\tag{3.1}
\]

for sufficiently small positive s. The constants are independent of P.

**Proof.** Unitary invariance reduces to P=diag(I_k,0). Subspaces near P are uniquely the graphs of complex matrices Z:C^k -> C^(D-k). The corresponding orthogonal projection is

\[
Q(Z)=\begin{bmatrix}I\\Z\end{bmatrix}
(I+Z^*Z)^{-1}
\begin{bmatrix}I&Z^*\end{bmatrix}.
\]

At Z=0, its derivative sends H to the block matrix [[0,H^*],[H,0]], whose Hilbert-Schmidt norm is sqrt(2)||H||_HS. Thus in a sufficiently small fixed neighborhood this smooth chart and its inverse are bi-Lipschitz. Every sufficiently close subspace is in this chart: if ||Q-P||_op<1, projection onto C^k is invertible on the range of Q.

The Grassmannian carries the smooth Riemannian volume induced by the Hilbert-Schmidt metric on projections. That volume is unitary invariant; after normalization it is the unique invariant probability measure on this compact transitive space, hence is the law of Q. In the graph chart its density is smooth and strictly positive, and is bounded above and below on a smaller compact neighborhood. The real dimension of the chart is 2k(D-k). Comparison with Euclidean balls proves (3.1). Homogeneity makes the constants independent of P. QED.

**Lemma Q2 (uniform orbit small balls).** There is a finite constant C_D such that, for every A in H_0(D) of Hilbert-Schmidt norm one, every center B in H_0(D), and every 0<s<=1,

\[
\Pr(\|UAU^*-B\|_{HS}\le s)\le C_D s^{2(D-1)}.
\tag{3.2}
\]

**Proof.** Write the ordered eigenvalues of A as lambda_1>=...>=lambda_D. Their sum is zero and the sum of their squares is one. Hence max_i |lambda_i|>=1/sqrt(D), and their total range is at least 1/sqrt(D). At least one consecutive eigenvalue gap, say the k-th, is therefore at least

\[
g_D=\frac1{\sqrt D(D-1)}.
\]

Let P be the projection onto the top k eigenspaces. If A'=WAW^* and P'=WPW^*, diagonalization gives the exact identity

\[
\|A-A'\|_{HS}^2
=\sum_{i,j}(\lambda_i-\lambda_j)^2
|\langle e_i,We_j\rangle|^2
\ge g_D^2\|P-P'\|_{HS}^2.
\tag{3.3}
\]

The last step retains the terms crossing the top-k/lower-(D-k) split. Their weights sum to ||P-P'||_HS^2. This identity is valid with eigenvalue multiplicities inside either cluster; the selected positive gap separates the clusters.

If the ball about B misses the orbit, (3.2) is trivial. Otherwise choose one point A_0 on the orbit inside that ball. Every other point in the ball lies within 2s of A_0. Haar invariance, (3.3), and Lemma Q1 bound its probability by a constant times

\[
(s/g_D)^{2k(D-k)}.
\]

Since k(D-k)>=(D-1), this is at most a dimension-dependent constant times s^{2(D-1)} for sufficiently small s. There are finitely many k, so choose constants uniformly over them. Enlarging the constant handles all remaining s in (0,1]. QED.

This is the indispensable additional argument: no premise about pure conditional means was used.

**Proposition Q3.** For constants c_D,C_D'>0,

\[
c_Dm^{-1/(D-1)}\le1-\kappa_{m,D}
\le C_D'm^{-1/(D-1)}.
\tag{3.4}
\]

**Proof of the lower bound.** For fixed A and any unit code B_j, use (3.2) and choose s=(2C_Dm)^(-1/(2(D-1))), reducing the constant if necessary. With probability at least 1/2 the orbit point is farther than s from every B_j. Since both have norm one,

\[
1-\max_j\operatorname{Tr}(B_jUAU^*)
=\tfrac12\min_j\|UAU^*-B_j\|_{HS}^2.
\]

Averaging gives a deficit at least s^2/4, uniformly in A and the code. Taking their supremum proves the first inequality.

**Proof of the upper bound.** Choose A=(|psi><psi|-I/D)/r_0, a normalized pure-state center. Its orbit is the rank-one complex Grassmannian. Lemma Q1, or a maximal separated set using its lower small-ball bound, gives a radius-s covering with at most C_D s^(-2(D-1)) orbit points. Taking these as B_j yields squared approximation error at most s^2. Choosing s of order m^(-1/(2(D-1))) proves the second inequality, after adjusting constants for small m. QED.

The exponent comes from the least dimension of a nonconstant conjugation orbit, not from the ambient matrix-space dimension D^2-1. No exact optimal code or sharp leading geometric constant is claimed.

## 4. Observable lower bound

Choose A=(|psi><psi|-I/D)/r_0 and B=(|phi><phi|-I/D)/r_0 for fixed unit psi,phi. Both have Hilbert-Schmidt norm one. Under Haar V the scalar

\[
f=\operatorname{Tr}(B V A V^*)
=\frac{|\langle\phi,V\psi\rangle|^2-1/D}{r_0^2}
\]

has E f=0 and E f^2=1/(D^2-1).

For completeness, a uniform complex unit vector is a standard complex Gaussian vector divided by its norm. Its squared first coordinate is the ratio of one exponential variable to the sum of D independent exponential variables. It therefore has density (D-1)(1-s)^(D-2) on [0,1]. Direct integration gives E s=1/D and E s^2=2/[D(D+1)], from which the stated variance follows.

For the terminal bit Y consider Z=(2Y-1)f. The target expectation is delta/(D^2-1). The classical expectation has absolute value at most R_T<=kappa_(m,D)^T. Uniform probability error epsilon changes this expectation by at most 2epsilon. Thus

\[
\kappa_{m,D}^T\ge a:=\delta/(D^2-1)-2\epsilon>0.
\]

By Proposition Q3,

\[
a\le\exp(-c_DT m^{-1/(D-1)}),
\]

and consequently

\[
m\ge\left(\frac{c_DT}{\log(1/a)}\right)^{D-1}.
\tag{4.1}
\]

Only the output probabilities of the fixed weak-measurement family are required. The simulator need not reconstruct a density matrix.

## 5. Matching polytope construction

Choose a projective net of pure vectors phi_i such that for every unit psi some phi_i obeys

\[
1-|\langle\psi,\phi_i\rangle|^2\le r^2,
\]

with N<=C_D r^(-2(D-1)). Existence follows from Lemma Q1 and maximal separated sets. Let A_i=(|phi_i><phi_i|-I/D)/r_0 and L=conv{A_i}.

**Lemma Q4.** With alpha=1-D r^2>0,

\[
\alpha K_D\subset L\subset K_D.
\tag{5.1}
\]

**Proof.** For any nonzero traceless Hermitian B, its largest eigenvalue lambda_max is positive and lambda_min>=-(D-1)lambda_max. Choose a top eigenvector psi and a net point phi_i with infidelity at most r^2. Expanding phi_i into its component along psi and its orthogonal complement gives

\[
\langle\phi_i,B\phi_i\rangle
\ge\lambda_{max}-r^2(\lambda_{max}-\lambda_{min})
\ge(1-Dr^2)\lambda_{max}.
\]

The cross terms vanish because psi is an eigenvector. Divide by r_0. Since h_(K_D)(B)=lambda_max/r_0, every support direction of L dominates the corresponding support direction of alpha K_D. Separation proves (5.1); the second inclusion follows because its vertices belong to K_D. QED.

Let P=L/alpha and w_i=A_i/alpha. Then K_D subset P subset alpha^(-1) times the unit Hilbert-Schmidt ball. For every unitary U,

\[
\alpha U w_i U^*=UA_iU^*\in K_D\subset P.
\]

Choose barycentric coefficients as stochastic transitions on the w_i. Encode any A in K_D by its barycentric coordinates. Use terminal probabilities (1+delta Tr(Bw_i))/2. These are valid when alpha>=1/2 because delta<=1/(D^2-1)<=1/3.

After t steps the expected vertex is exactly alpha^t V_t A V_t^*. Thus the probability error is at most

\[
\frac\delta2(1-\alpha^T)\le\frac{\delta D T r^2}{2}.
\]

Choose

\[
r^2=\min\{1/(2D),\ 2\epsilon/(\delta DT)\}.
\]

Then alpha>=1/2, the error is at most epsilon, and N=O_(D,delta,epsilon)(T^(D-1)). Together with (4.1) this proves Theorem Q.

Latent vertices w_i need not be quantum states. They are abstract classical states with valid responses for the specified weak effects. Requiring them to be physical states would be an extra, unnecessary restriction.

## 6. Exact static size

Identify H_0(D) isometrically with R^n. The regular-simplex construction in Section 8 of the spherical note works for every A in K_D, since K_D is inside the unit ball and delta<=1/n. It uses n+1=D^2 states.

For the converse choose an orthonormal basis F_1,...,F_n of H_0(D). The preparations A_0=0 and A_j=cF_j lie in K_D for sufficiently small fixed c>0: I/D+r_0 cF_j is positive if r_0 c<=1/D. Choose queries B_0=0 and B_j=F_j. The resulting square probability matrix has determinant (delta c)^n/2^(n+1), which is nonzero. Hence every static factorization needs at least n+1 states. QED.

## 7. Prior art and scope

Montina's 2008 paper, Exponential complexity and ontological theories of quantum mechanics, Phys. Rev. A 77, 022104, and his later arXiv:1008.4415 discussion are important predecessors. They study the dimension of continuous-variable Markov ontological models, including regularity/trajectory hypotheses. The source abstract reports a 2D-2 variable-dimension bound. This note does not claim to invent that dimension or the general Markov-simulation obstruction.

The result here has a different explicit contract: a finite-horizon, finite-state, uniform approximation law for a specified weak-measurement family, admitting arbitrary measurable time-dependent transitions and non-affine preparations. These differences do not establish priority. Detailed comparison with the original papers and recent finite-memory work is still required.

No lower bound for a full deterministic floating-point state-vector simulator follows: its real registers or finite-precision values must be accounted for as classical states, and its running time is a separate resource. For D=2^q, the asymptotic leading coefficient D-1 in the classical bit count is exponential in q, but the constants and permitted visibility/error also depend on D. It would be misleading to state a dimension-uniform practical exponential speedup.

The quantum extension does not resolve the fixed finite gate-alphabet question identified in the main note. Nor does it establish the requested historic foundational objective.
