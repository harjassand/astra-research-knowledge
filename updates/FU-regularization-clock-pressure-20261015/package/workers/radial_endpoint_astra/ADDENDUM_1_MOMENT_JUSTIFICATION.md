# Addendum 1: fully justified Pauli moments for general noise

Date: 2026-10-15. This addendum resolves the explicit general-measure moment-justification qualification in Section 6 of `ENDPOINT_PROOF_v1.md`. It does not change any constants or the existence proof.

Suppose \(\nu\) is any scalar probability measure with all exponential moments and that a positive normalized operator measure \(M\) satisfies
\[
 \widehat M(t)=\widehat\nu(t)e^{iA(t)}.
\]
For every unit vector \(v\) in the Hilbert space and every real direction \(u\), the ordinary probability distribution of \(u\cdot X\) under \(\langle v,M(\cdot)v\rangle\) has characteristic function
\[
 \widehat\nu(tu)\langle v,e^{itA(u)}v\rangle.
\]
Uniqueness of characteristic functions identifies this one-dimensional distribution with the convolution of the \(u\)-projection of \(\nu\) and the spectral distribution of the bounded self-adjoint \(A(u)\) in the state \(v\). Both factors are positive probability measures. This is a direct consequence of the all-linear-marginal contract and does not interchange a distribution with an unbounded test function.

Therefore, for every real \(g\),
\[
 \int e^{g\cdot x}\langle v,M(dx)v\rangle
 =m_\nu(g)\langle v,e^{A(g)}v\rangle
 \le m_\nu(g)e^{R|g|}\|v\|^2.
\]
The bounded positive quadratic form on the left defines a bounded positive operator. Polarization gives the operator identity
\[
 Q(g):=\int e^{g\cdot x}M(dx)=m_\nu(g)e^{A(g)}.
 \tag{A1}
\]

Polynomial factors can also be integrated and differentiated rigorously. Fix a compact set of real tilts \(g\) and a small \(d>0\). For each nonnegative integer \(k\),
\[
 |x_j|^k e^{g\cdot x}
 \le C_{k,d}\bigl(e^{(g+de_j)\cdot x}+e^{(g-de_j)\cdot x}\bigr).
\]
On a compact neighborhood of \(g\), add finitely many coordinate signs if necessary to dominate simultaneous perturbations. Formula (A1), continuity of \(m_\nu\), and boundedness of \(A\) give a uniform bound on the resulting positive operator integrals. Dominated convergence of quadratic forms, followed by polarization, thus identifies first and second derivatives of \(Q(g)\) with the corresponding operator moments. Equivalently, the Taylor remainder is dominated by the same positive exponential envelopes, so differentiation holds in operator norm.

For the Pauli proof, set \(g=(s,0,\ldots,0)\), and conjugate by
\[
 C_s=m_\nu(g)^{-1/2}e^{-sA_1/2}.
\]
The operator measure \(e^{s x_1}C_sM(dx)C_s\) is positive and normalized. Its zeroth, first transverse, and second transverse moments are, by (A1),
\[
 I,\qquad B_1(s),\qquad \frac{K'(s)}sI+B_2(s),
\]
because radiality makes the first scalar transverse derivative zero and the second one \(K'(s)/s\). Positivity of
\[
 \int
 \begin{pmatrix}I\\x_2 I\end{pmatrix}
 e^{s x_1}C_sM(dx)C_s
 \begin{pmatrix}I&x_2 I\end{pmatrix}
\]
and its Schur complement prove the exact inequality used in Section 6, for arbitrary such input noise and weakly countably additive POVMs. The needed integrals and differentiation are now justified using positive one-dimensional marginals alone.

Thus (T5), (T6), and the sharp iterated-log obstruction in the main proof hold in their full stated noise/POVM generality, without an additional smoothness or derivative-decay hypothesis.
