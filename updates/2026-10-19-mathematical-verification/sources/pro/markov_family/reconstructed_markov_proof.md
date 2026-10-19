# Reconstructed and independently proved Markov result

Research reconstruction, 19 October 2026. This is a fresh derivation from the pasted progress log, not a recovered original manuscript. The numerical minimum agrees with the log to its stated digits.

## 1. Conventions and family

Matrices act on row probability vectors. A generator has zero row sums and nonnegative off-diagonal entries. The observation interval is one. Stationary entropy production is

\[
\sigma(Q)=\sum_{i<j}(\pi_iq_{ij}-\pi_jq_{ji})\log\frac{\pi_iq_{ij}}{\pi_jq_{ji}}.
\]

Both rates zero contribute zero; exactly one zero and the other positive contributes infinity. Natural logarithms are used. This is pathwise Markov entropy production in nats per observation interval; a thermodynamic interpretation needs the usual additional physical assumptions.

Let \(a,b>0\), \(\lambda=e^{-a}\), \(\mu=e^{-b}\), \(\Pi=\mathbf1\mathbf1^T/4\), and

\[
v=(1,-1,0,0)^T/\sqrt2,\qquad
u=(1,1,-1,-1)^T/2,\qquad
w=(0,0,1,-1)^T/\sqrt2.
\]

Define

\[
P(a,b)=\Pi+\lambda vv^T+\mu(uu^T+ww^T)
=\frac14\begin{pmatrix}
1+\mu+2\lambda&1+\mu-2\lambda&1-\mu&1-\mu\\
1+\mu-2\lambda&1+\mu+2\lambda&1-\mu&1-\mu\\
1-\mu&1-\mu&1+3\mu&1-\mu\\
1-\mu&1-\mu&1-\mu&1+3\mu
\end{pmatrix}.
\]

It is symmetric, has row sums one, and is entrywise nonnegative exactly when \(2e^{-a}\le1+e^{-b}\). Its spectrum is \(1,e^{-a},e^{-b},e^{-b}\). Whenever it is a Markov matrix, it is irreducible (the cross entries are positive) and its unique stationary distribution is uniform. Its principal logarithm is

\[
L=-avv^T-b(uu^T+ww^T),\qquad L_{12}=L_{21}=(2a-b)/4;
\]

all its other off-diagonal entries equal \(b/4\).

### Theorem 1 (sharp embedding boundary)

For the family above, reversible embeddability is equivalent to \(b\le2a\). In the regime \(b>2a\), ordinary embeddability is equivalent to both

\[
\boxed{\quad b\ge\frac{10\pi}{\sqrt7},\qquad
a\ge b-\sqrt{\frac{b^2-4\pi^2}{2}}.\quad}
\]

The inequalities themselves guarantee that the displayed matrix is stochastic; one may alternatively assume stochasticity at the outset.

## 2. Exhaustive real logarithms

Assume \(b>2a\), so the three distinct eigenvalues of \(P\) are \(1,e^{-a},e^{-b}\), with multiplicities \(1,1,2\). Every logarithm \(Q\) commutes with \(P=e^Q\); hence it preserves these three real eigenspaces. Its real action on the one-dimensional eigenspaces is necessarily \(0\) and \(-a\). The two-dimensional block has exponential \(e^{-b}I_2\).

If a matrix has diagonalizable exponential, it is diagonalizable over \(\mathbb C\): a nontrivial Jordan block \(\zeta I+N\) would exponentiate to a nontrivial Jordan block since \(e^N-I=N\,h(N)\), where \(h(0)=1\), so \(h(N)\) is invertible. Consequently the real two-dimensional block is either \(-bI_2\), or has eigenvalues \(-b\pm2\pi ki\), \(k\ge1\). Subtracting \(-bI_2\), every nonprincipal block is

\[
R=\begin{pmatrix}A&B\\C&-A\end{pmatrix},\qquad
BC=-(A^2+\omega^2),\quad\omega=2\pi k,\quad k\in\mathbb N.
\]

Conversely, every such block satisfies \(R^2=-\omega^2I_2\), hence \(e^R=I_2\). Thus every real logarithm is exactly either \(L\), or

\[
Q=L+A(uu^T-ww^T)+Buw^T+Cwu^T
\tag{1}
\]

with the constraint above. This accounts for *all* real logarithms, not just a prescribed symmetry class. All have row and column sums zero, since \(u,v,w\perp\mathbf1\).

This logarithm machinery is already known: see Baake--Sumner (2024), Fact 2.10, Corollary 2.11 and Lemma 4.5, and the earlier Casanellas--Fernández-Sánchez--Roca-Lacostena treatment. Its specialization here is independently derived for completeness, and is not claimed as a new general logarithm theorem.

## 3. Generator constraints and exact feasibility

Put \(c=(b-A)/4\), \(d=(b+3A)/4\). The off-diagonal entries of (1) are

\[
\begin{aligned}
q_{12}=q_{21}&=(2a-b+A)/4,\\
q_{13}=q_{23}&=c+B/(2\sqrt2),&q_{14}=q_{24}&=c-B/(2\sqrt2),\\
q_{31}=q_{32}&=c+C/(2\sqrt2),&q_{41}=q_{42}&=c-C/(2\sqrt2),\\
q_{34}&=d+(B-C)/(2\sqrt2),&q_{43}&=d-(B-C)/(2\sqrt2).
\end{aligned}
\tag{2}
\]

Since \(BC<0\), writing \(p=|B|\), \(q=|C|\) gives \(pq=A^2+\omega^2\), and \(|B-C|=p+q\). Therefore the necessary and sufficient rate constraints are

\[
A\ge b-2a,\quad
\max(p,q)\le\frac{b-A}{\sqrt2},\quad
p+q\le\frac{b+3A}{\sqrt2}.
\]

For fixed \(A,\omega\), both the maximum and sum on the left are minimized by
\(p=q=r:=\sqrt{A^2+\omega^2}\). Thus a generator exists at \(A,\omega\) if and only if

\[
A\ge b-2a,\qquad
b\ge A+\sqrt2\sqrt{A^2+\omega^2},\qquad
b\ge-3A+2\sqrt2\sqrt{A^2+\omega^2}.
\tag{3}
\]

Here \(A>0\). The first right-hand function in the last two inequalities is strictly increasing in \(A\ge0\); the second is strictly decreasing there, since its derivative is \(-3+2\sqrt2A/\sqrt{A^2+\omega^2}<0\). They meet at

\[
A_0=\omega/\sqrt7,\qquad b_0=5\omega/\sqrt7.
\]

Equivalently, for \(b\ge b_0\), the feasible values of \(A\) form

\[
\left[\max\{b-2a,A_-(b,\omega)\},\,A_+(b,\omega)\right],
\]

where

\[
A_-=-3b+2\sqrt2\sqrt{b^2+\omega^2},\qquad
A_+=-b+\sqrt2\sqrt{b^2-\omega^2}.
\]

This interval is nonempty exactly when \(b\ge b_0\) and \(b-2a\le A_+\). For existence it suffices to use \(k=1\): decreasing \(\omega\) weakens every constraint in (3). Substitution of \(\omega=2\pi\) proves the stated boundary. A convenient explicit feasible choice is

\[
A=\max\{b-2a,2\pi/\sqrt7\},\quad
B=-C=\sqrt{A^2+4\pi^2}.
\]

If \(b\le2a\), \(L\) is a symmetric generator. Conversely, a reversible generator for irreducible \(P\) must be reversible for its unique uniform stationary distribution, hence symmetric. A symmetric matrix has only real eigenvalues, so a symmetric logarithm of positive definite \(P\) is uniquely \(L\). This proves the reversible claim.

The full sharp criterion can be stated without separately imposing entrywise nonnegativity: in the principal regime, \(e^{-a}\le e^{-b/2}\) and \(2e^{-b/2}\le1+e^{-b}\). In the nonprincipal regime, the boundary has \(a\ge4\pi/\sqrt7>\log2\), so \(2e^{-a}<1\).

## 4. Entropy optimization over all generators

Stay in the embeddable regime \(b>2a\). For fixed \(A,\omega\), transpose the generator if necessary to take \(B=p>0\), \(C=-q<0\). This leaves entropy production unchanged. Set \(D=p+q\), \(r^2=pq=A^2+\omega^2\). Direct substitution of (2) into the entropy-production definition gives

\[
\sigma(Q)=\frac{D}{4\sqrt2}\left[
\log\frac{(c+p/(2\sqrt2))(c+q/(2\sqrt2))}{(c-p/(2\sqrt2))(c-q/(2\sqrt2))}
+\log\frac{d+D/(2\sqrt2)}{d-D/(2\sqrt2)}\right].
\tag{4}
\]

The first ratio in (4) is

\[
\frac{c^2+cD/(2\sqrt2)+r^2/8}{c^2-cD/(2\sqrt2)+r^2/8}.
\]

On the finite-entropy domain, both logarithms in (4) are nonnegative and strictly increasing in \(D>0\). Thus (4) is strictly increasing in \(D\), for fixed \(A,r\). Since \(D\ge2r\), the unique minimizing magnitudes are \(p=q=r\), i.e. \(B=-C=\pm r\). The same conclusion extends to boundaries by lower semicontinuity; a one-way positive edge has infinite entropy production.

For this balanced choice let \(s=\sqrt2\sqrt{A^2+\omega^2}\). The entropy is

\[
F_{b,\omega}(A)=\frac{s}{4}\left[
2\log\frac{b-A+s}{b-A-s}
+\log\frac{b+3A+2s}{b+3A-2s}\right].
\tag{5}
\]

For fixed \(A\), (5) is strictly increasing in \(s\), hence in \(\omega>0\). Every feasible generator with winding \(k>1\) therefore has entropy strictly above a feasible \(k=1\) generator at the same \(A\). Hence the global minimum has \(\omega=2\pi\).

### Strict convexity and unique minimizer

Set \(\omega=2\pi\) and \(F_b=F_{b,\omega}\). The function

\[
h(c,j)=j\log\frac{c+j}{c-j},\qquad c>j>0,
\]

is jointly convex: it is the perspective \(c f(j/c)\) of \(f(z)=z\log((1+z)/(1-z))\), and \(f''(z)=4/(1-z^2)^2>0\). Write (5) as

\[
G_b(A,s)=\tfrac12h(b-A,s)+\tfrac18h(b+3A,2s).
\]

This is jointly convex in \((A,s)\), and is strictly increasing in \(s>0\). Since \(s(A)=\sqrt2\sqrt{A^2+\omega^2}\) is strictly convex, the composition \(F_b(A)=G_b(A,s(A))\) is strictly convex on its feasible open interval: for two distinct values of \(A\), first apply strict convexity of \(s\), then strict monotonicity of \(G_b\), then convexity of \(G_b\).

For \(b>5\omega/\sqrt7\), \(F_b\) tends to infinity at both finite-entropy endpoints \(A_-\) and \(A_+\). It consequently has a unique critical point \(A_*(b)\in(A_-,A_+)\), which is its global minimum. Moreover \(A_*(b)>0\): this is immediate if \(A_-\ge0\), while if \(0\) is inside the domain, direct differentiation gives

\[
F_b'(0)=s(0)^2\left[\frac1{b^2-s(0)^2}-\frac3{b^2-4s(0)^2}\right]<0.
\]

On the strict embedding interior, namely \(b>10\pi/\sqrt7\) and \(a>b-\sqrt{(b^2-4\pi^2)/2}\), the exact answer is

\[
\boxed{\min_{Q:\ e^Q=P(a,b)}\sigma(Q)=F_b(\widehat A),\qquad
\widehat A=\max\{b-2a,A_*(b)\}.}
\tag{6}
\]

This is an exact one-variable characterization, not a claim that the root is elementary. The two minimizers are the generator (1) at \(A=\widehat A\), \(B=-C=\sqrt{\widehat A^2+4\pi^2}\), and its transpose. At the nonprincipal embedding boundary (equality in either of its defining inequalities), all feasible generators have a one-way edge and the minimum is infinity. In the reversible regime the minimum is zero, attained by \(L\).

For rigorous root evaluation, let \(s'=2A/s\), \(c_1=b-A\), \(c_2=b+3A\), and
\(\ell_1=\log((c_1+s)/(c_1-s))\), \(\ell_2=\log((c_2+2s)/(c_2-2s))\). Then

\[
F_b'(A)=\frac{s'}4(2\ell_1+\ell_2)
+s\left[\frac{c_1s'+s}{c_1^2-s^2}+\frac{c_2s'-3s}{c_2^2-4s^2}\right].
\tag{7}
\]

## 5. Exact rational observation matrix

Take \(a=8\log2\), \(b=18\log2\). Then

\[
P=\frac1{1048576}\begin{pmatrix}
264193&260097&262143&262143\\
260097&264193&262143&262143\\
262143&262143&262147&262143\\
262143&262143&262143&262147
\end{pmatrix}.
\]

It is strictly positive and symmetric, with eigenvalues \(1,2^{-8},2^{-18},2^{-18}\). Its principal logarithm has \(L_{12}=-(\log2)/2<0\), so no reversible continuous-time realization exists on these four states.

An exact all-positive generator witness uses \(A_0=2\pi/\sqrt7\). Put \(t=A_0\). The witness is

\[
Q_0=\frac14\begin{pmatrix}
-2a-b+t&2a-b+t&b+3t&b-5t\\
2a-b+t&-2a-b+t&b+3t&b-5t\\
b-5t&b-5t&-3b-t&b+11t\\
b+3t&b+3t&b-5t&-3b-t
\end{pmatrix}.
\]

Here \(b>5t\) and \(2a-b+t>0\). To check positivity without relying on floating point, use \(\log2>2/3\), \(\pi<22/7\), and \(220^2<84^2\cdot7\) to get \(b>12>10\pi/\sqrt7=5t\). Also \(\log2<1\) and \(\pi>3>\sqrt7\) imply \(t>2>2\log2=b-2a\). The spectral-block argument proves \(e^{Q_0}=P\) exactly.

The unconstrained root lies in \([2.2905478380320084,2.2905478380320091]\), above \(b-2a=2\log2\). Exact rational interval arithmetic gives

\[
26.178911678346<\min\sigma<26.178911678347.
\]

This lies strictly inside the pasted prior enclosure \([26.1789116459,26.1789117108]\). The accompanying `certify_entropy.py` uses only the Python standard library and performs exact rational interval arithmetic, with explicit series remainder bounds for logarithms and pi and integer square-root bounds, to certify the root and value without trusting floating point optimization. The output is saved in `certified_result.json`. A separate direct matrix-exponential computation agrees with the rational observation matrix to less than \(5\times10^{-16}\); direct evaluation of the pairwise entropy sum agrees with the scalar objective.

## 6. Literature and correctness/novelty separation

1. E. Baake, M. Baake and J. Sumner, *Embedding of reversible Markov matrices*, arXiv:2511.22800v1, 27 November 2025: <https://arxiv.org/html/2511.22800v1>. Theorem 3.16 explicitly asserts that a reversible positive-spectrum Markov matrix is ordinarily embeddable iff it is reversibly embeddable. The matrix above contradicts implication (1) to (2) of that version. The proof's unsupported step selects a sequence of *embeddable reversible simple-spectrum matrices* approaching any embeddable reversible positive-spectrum matrix. Density of simple-spectrum matrices alone does not give this additional embeddability property. The counterexample shows such a sequence cannot exist: continuity of the principal logarithm would preserve the negative (1,2) entry near this matrix, while simple positive-spectrum matrices can only embed via their principal logarithm.

2. M. Baake and J. Sumner, *Embedding of Markov matrices for d <= 4*, Journal of Mathematical Biology 89 (2024), article 23, DOI 10.1007/s00285-024-02112-w, arXiv:2311.02596v2: <https://arxiv.org/html/2311.02596v2>, <https://link.springer.com/article/10.1007/s00285-024-02112-w>. The general two-dimensional real logarithm parameterization and four-state degree-three case are prior work. Our derivation specializes these tools and explicitly solves the inequalities and entropy optimization for this family.

3. M. Casanellas, J. Fernández-Sánchez, J. Roca-Lacostena, *The embedding problem for Markov matrices*, arXiv:2005.00818: <https://arxiv.org/abs/2005.00818>. General four-state embedding work must be credited.

4. M. Casanellas, J. Fernández-Sánchez, J. Roca-Lacostena, *An open set of 4 x 4 embeddable matrices whose principal logarithm is not a Markov generator*, Linear and Multilinear Algebra 70 (2022), 3768--3779, DOI 10.1080/03081087.2020.1854165, arXiv:2005.00821: <https://arxiv.org/pdf/2005.00821>. Their Example 3.2 provides the generator \(Q_{\rm old}=\pi H/4\), where

\[
H=\begin{pmatrix}-21&4&16&1\\7&-9&1&1\\1&1&-9&7\\1&16&4&-21\end{pmatrix}.
\]

For its sampled matrix \(M=e^{Q_{\rm old}}\), taking the fourth power yields \(P_{\rm old}=M^4=e^{\pi H}\). Exact diagonalization gives spectrum \(1,e^{-28\pi},e^{-16\pi},e^{-16\pi}\) and

\[
\log(P_{\rm old})=\pi\begin{pmatrix}-18&10&10&-2\\4&-12&4&4\\4&4&-12&4\\-2&10&10&-18\end{pmatrix}.
\]

This logarithm is reversible for \(\pi_{\rm old}=(1/7,5/14,5/14,1/7)\), hence so is \(P_{\rm old}\), yet it has a negative (1,4) entry. Thus the broad positive-spectrum reversible counterexample is already a short consequence of this older published example, even though that consequence is not the example's stated focus. We explicitly credit this precursor and make no first-counterexample claim.

The explicit sharp boundary and entropy optimization above have complete elementary proofs. They have not been proved novel by the absence of a search hit. The broad counterexample is a corollary of older published work. Any originality claim should concern only the explicit family classification and completed entropy minimization, pending specialist literature review.

## 7. Scope and limitations

The result concerns finite, time-homogeneous continuous-time chains on the *same four observed states*, sampled at one exact interval. It does not optimize over enlarged hidden state spaces or time-dependent generators. It does not assert a robust statistical estimator or provide an experimental physical invention. Exact repetition of the eigenvalue is essential to this particular mechanism: for a reversible positive matrix with distinct eigenvalues the real logarithm is unique. The example is nevertheless separated from every reversible generator because its principal logarithm has a strictly negative off-diagonal entry.

Four states are minimal for an irreducible example of this kind: in dimensions two and three a reversible positive-spectrum Markov matrix either has distinct eigenvalues, forcing the unique real logarithm, or in dimension three has spectrum \(1,\mu,\mu\). The latter matrix is \(\Pi_\pi+\mu(I-\Pi_\pi)\), whose principal logarithm \(\log\mu(I-\Pi_\pi)\) is automatically a reversible generator for \(0<\mu<1\).
