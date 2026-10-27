# Cartan-power completion of the full rank-two projection problem

This is the strongest live auxiliary object from the continuation. It does not decide the all-copy inequality. It uses an established coherent-state approximation theorem; neither that theorem nor the general coherent-state hierarchy method is claimed as invented here. The application, constants, and explicit opposition are given completely below.

## 1. The object, without an unknown positivity premise

Let H=(C^3)^{tensor n}, D=3^n. A unit decomposable bivector

\[
z=u\wedge v=(u\otimes v-v\otimes u)/\sqrt2,
\qquad u\perp v,\quad\|u\|=\|v\|=1,
\]

has one-replica marginal P/2, where P=uu*+vv* is a rank-two projection. Define the **Cartan power**

\[
\mathcal C_k(H)=\operatorname{span}\{z^{\otimes k}:z\text{ decomposable}\}
\subset\operatorname{Sym}^k(\wedge^2H),\qquad k\ge2.
\]

This is the irreducible U(D) representation with highest weight (k,k). It is constructible by the rectangular two-row Young symmetrizer: antisymmetrize each of the k columns and symmetrize the two rows, taking the corresponding image. Thus defining the space does not require a solution of Werner positivity. Its dimension is

\[
d_D(k)=\frac{(D+k-1)!(D+k-2)!}
{(D-1)!(D-2)!\,k!\,(k+1)!}.\tag{1}
\]

Grouping the first two bivector columns gives the canonical inclusion

\[
\mathcal C_k(H)\subset\mathcal C_2(H)\otimes\mathcal C_{k-2}(H).
\]

For k=2 the second factor is scalar. This inclusion is already evident on the spanning coherent powers, and is the highest-weight-sum inclusion needed by the cited approximation theorem.

Each bivector column consists of two H replicas, called a,b in the first column and c,d in the second. Let

\[
B_n=A_n^{(a,c)}\otimes I_{b,d},
\qquad A_n=\prod_{i=1}^n(F_{ac,i}-I/2).
\]

For R a density matrix on \(\mathcal C_k(H)\), let R^(2) be its first two-column marginal and set

\[
\alpha_{n,k}=\min_R\operatorname{Tr}(R^{(2)}B_n).\tag{2}
\]

This is a finite smallest-eigenvalue/PSD problem on an explicit linear representation space. For a coherent density matrix \(|z\rangle\langle z|^{\otimes k}\), tracing b,d gives (P/2) tensor (P/2), so the value is q_n(P)/4. Every rank-two projection occurs. In particular

\[
\alpha_{n,k}\le g_n/4.\tag{3}
\]

Partial trace maps degree k+1 into degree k, so the minima are nondecreasing in k. No product-ray, local-support, normality, reality, or graph restriction is placed on P.

## 2. Explicit convergence and full-target reduction

Theorem II.2 of Christandl--König--Mitchison--Renner, applied with highest weights (2,2) and (k-2,k-2), implies that every two-column marginal above is within

\[
4\left(1-\frac{d_D(k-2)}{d_D(k)}\right)
\]

in the **full trace norm** of a mixture of coherent states \(|z\rangle\langle z|^{\otimes2}\). The theorem is stated for a pure input; decomposing R into pure inputs and mixing their measures proves the same assertion for mixed R. Its published norm convention is half the trace norm, accounting for the factor four.

Since \(\|B_n\|\le(3/2)^n\), (3) therefore strengthens to

\[
0\le g_n/4-\alpha_{n,k}
\le4\left(1-\frac{d_D(k-2)}{d_D(k)}\right)(3/2)^n
\le\frac{16D}{k}(3/2)^n.\tag{4}
\]

Here the ratio is exactly

\[
\frac{d_D(k-2)}{d_D(k)}
=\frac{k^2(k^2-1)}{(k+D-1)(k+D-2)^2(k+D-3)}.\tag{5}
\]

To verify the last bound in (4), pair the four numerator factors with the denominator factors as

\[
\frac{k+1}{k+D-1}
\left(\frac{k}{k+D-2}\right)^2
\frac{k-1}{k+D-3}.
\]

Each is \(1-(D-2)/(k+D-j)\) with j=1,2,2,3. The union bound on one minus a product bounds (5)'s deficit by \(4(D-2)/(k+D-3)\le4D/k\). This proves (4) for D>=3 and k>=2.

The hierarchy is therefore complete for every fixed n, with a quantitative error. More significantly, an explicit joint scaling is

\[
k(n)=\lceil16\,9^n\rceil,
\qquad 0\le g_n/4-\alpha_{n,k(n)}\le2^{-n}.\tag{6}
\]

The prior N525 projection-completeness and persistent-gap theorem then gives the exact alternative

\[
\begin{array}{ll}
\text{full all-copy rank-two positivity}&\Longrightarrow\alpha_{n,k(n)}\longrightarrow0,\\
\text{a negative complex rank-two witness exists}&\Longrightarrow\limsup_n\alpha_{n,k(n)}<0.
\end{array}\tag{7}
\]

Conversely convergence to zero in (7) excludes the second alternative and proves the full target. Thus (7) is an exact reduction of the same scientific mission. **Convergence to zero has not been proved.** Computing finite levels or invoking coherent-state approximation alone does not prove it.

The explicit degree in (6) is exponential. Equation (1) has degree 2D-4 in k, and \(\log d_D(k(n))=O(n3^n)\). The matrix dimension is still doubly exponential in n. This is an exact mathematical completion, not a feasible all-copy algorithm or an advantage claim.

## 3. Strong opposition at the first Cartan level

The exact vector w_0 in PROOF.md (13), with its local physical singlet-pairing basis W, lies in \(\mathcal C_2(H)\) at n=3. Its normalized expectation is

\[
\frac{\langle w_0,B_3w_0\rangle}{\|w_0\|^2}=-3/8.\tag{8}
\]

This is also binary-supported. Consequently \(\alpha_{3,2}\le-3/8\), even though the original binary quadratic form is nonnegative on **every matrix**. It is a rigorous failure of the first Cartan relaxation, not a Werner witness.

For completeness, the representation tests establishing membership and (8) are explicit. On the two-dimensional global [22] sector spanned by w_0,w_1, the whole-replica transpositions 12 and 34 both act as

\[
\begin{pmatrix}-1&-1\\0&1\end{pmatrix}.
\]

Thus w_0 is antisymmetric in both columns. The whole-column exchange (13)(24) acts as +I on [22]. The fully antisymmetric four-replica component is absent, since this is [22], not [1111]. The decomposition

\[
\operatorname{Sym}^2(\wedge^2H)=\mathcal C_2(H)\oplus\wedge^4H
\]

then proves membership in \(\mathcal C_2(H)\). Alternatively the verifier checks the column symmetries and vanishing total antisymmetrizer directly.

To compute (8), use the local transposition B in PROOF.md's displayed two-by-two representation for 13. On the three sites the observable is \((B-I/2)^{\otimes3}\); the physical metric is \((W^TW)^{\otimes3}\). With w_0's exact coefficient column (3,-1,-1,1,-1,1,1,0)^T, multiplication gives (8). Appending binary all-zero physical sites preserves Cartan membership and multiplies (8) by 1/2 per added site. Hence fixed degree k=2 fails for every n>=3.

This supplies the strongest opposition test of the live object, beyond the weaker whole-permutation completion in PROOF.md. The Cartan support enforces actual Plücker structure across columns, but a finite level still contains noncoherent states. More degree, or another valid structural estimate, is necessary. There is no inference that degree two, four-replica moments, or a positive crossed operator settles the full rank-two problem.

## 4. Stronger obstruction: no finite Cartan degree is positive

There is an exact obstruction beyond (8):

\[
\boxed{\alpha_{n,k}<0\quad\text{for every }n\ge3\text{ and every finite }k\ge2.}\tag{9}
\]

These negative minima are relaxed states. Equation (9) is compatible with the complete convergence theorem and is not a negative rank-two Werner witness.

**Proof on three binary physical sites.** Write H_0=(C^2)^{tensor 3}, let

\[
J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}^{\otimes3},\qquad
\Theta u=J\bar u.
\]

Then Theta is antiunitary and Theta^2=-I. The linear spin flip on matrices is theta(C)=J C^T J^{-1}. On each qubit, theta fixes scalar matrices and negates traceless matrices. Consequently

\[
\Pi^{\otimes3}\theta=-\Pi^{\otimes3}.
\]

For any unit u, the two vectors u,Theta u are orthogonal. The projection P_u onto their span is theta-invariant. Hence Pi^{tensor 3}(P_u)=0 and q_3(P_u)=0. This is the binary spin-flip zero mechanism already present in the supplied CT source; it is not claimed as new.

The family of these quaternionic two-planes is **Zariski dense** in the complex Grassmannian Gr(2,H_0). Here is the local argument needed for that assertion. Fix one invariant plane with basis e_0,Theta e_0 and split off its Theta-invariant orthogonal complement W. A general nearby complex plane is the graph of two independent columns (x,y) in W. Its Theta-invariant real locus is exactly

\[
(x,y)=(x,\Theta x).
\]

In a fixed complex basis of W, write Theta x=M bar x with M invertible. If a holomorphic polynomial in (x,y) vanishes on this locus, put x=a+ib with a,b real. It then vanishes after substitution (x,y)=(a+ib,M(a-ib)) for all real a,b in an open set. The resulting polynomial in a,b is identically zero. The substitution is an invertible complex-linear transformation of (a,b), so the original polynomial is zero. This proves density on the Grassmannian chart, and hence on the connected Grassmannian.

It follows that the vectors z_u^{tensor k}, for the decomposable bivectors of these zero planes, span the entire Cartan power C_k(H_0). Indeed any linear functional annihilating them restricts to a holomorphic polynomial section in Pluecker coordinates; on the graph chart it is a polynomial vanishing on the real locus just considered, and therefore vanishes on all coherent powers. Those powers define C_k by their span.

Suppose the compressed observable defining alpha were PSD at some finite k. Its zero coherent expectations at every P_u would imply that it annihilates every z_u^{tensor k}. The spanning result would force the compressed observable to be zero. But the plane spanned by the binary words 000 and 011 has

\[
q_3(P)=2(1/8)+2(1/8)=1/2>0.
\]

Its coherent expectation is 1/8, a contradiction. Therefore the finite Hermitian compression has a strictly negative eigenvalue for every k.

**Embedding into every qutrit n>=3.** Embed H_0 into the first three qutrit sites and append n-3 fixed pure zero letters. This is an isometry into H_n and sends C_k(H_0) into C_k(H_n). Every appended site's observable has expectation 1/2, so the compressed objective on the embedded subspace is multiplied by 2^{-(n-3)}. The negative eigenvalue persists, proving (9). The same argument proves the finite-degree obstruction on every odd binary copy number at least three.

This rules out an entire finite-degree positivity strategy. Degree cannot simply be increased until the compressed operator becomes PSD, even in the binary problem where positivity is already known. The obstruction is constructive in finite linear algebra: enumerate Gaussian-rational u, retain independent zero coherent powers until they span C_k(H_0), and use an exact Hermitian factorization to recover a negative relaxed vector. Zariski density proves termination of the spanning step; no polynomial acquisition bound is asserted. The viable remaining use is an **asymptotic negative-floor estimate**, exactly as in (6)--(7). No finite-degree PSD stopping certificate is available from this hierarchy.

## 5. Remaining obligation and provenance

The hard remaining claim is now

\[
\alpha_{n,k(n)}\ge-o(1)
\]

on an unbounded sequence of n, or a valid alternative bound of the same consequence. That is not established by the convergence theorem: (4) compares alpha to the still unknown global minimum. The first-stage growth invariant has not gained an upper bound from this construction. The exact obstruction (9) means that replacing the vanishing bound with finite-level nonnegativity would be false.

Primary import: [Christandl--König--Mitchison--Renner, arXiv:quant-ph/0602130v4](https://arxiv.org/pdf/quant-ph/0602130), Theorem II.2, its proof, and Example II.4's rectangular-representation interpretation. The theorem and trace-norm convention were checked from the primary PDF. N525's exact projection and persistent-gap proof is identified in PROOF.md. No all-copy positivity assertion is imported from either source.

The exact degree-two opposition and two non-real quaternionic zero controls are checked by verify.py using physical permutations and independent partial traces. The all-degree spanning argument is the analytic proof above, not an extrapolation from these controls. A numerical compression probe suggested the negative value before the rational vector check; that probe is exploratory and is not a proof. The rational formula (8) and its exact Cartan membership are the retained result.
