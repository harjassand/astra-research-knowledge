# Uniformly interior block mixtures and local-noise precompensation for one-dimensional Gibbs states

## Status and scope

This note gives the completed mathematical construction, incorporating the separate **Independent audit and finite-precision closure for the robust 1D block mixture**, in ../noncommuting/robust_1d_independent_audit.md. That audit checked the algebra, source geometry, condition-number bounds, sampler interface and finite-precision closure against the primary full texts. The constants below include additional slack for numerical implementation.

The starting theorem is due to Pilatowsky-Cameo, Styliaris, Bakshi and Malz: every fixed-temperature one-dimensional Gibbs state is an efficiently sampled mixture of bounded contiguous pure blocks. Its ideal constant-depth preparation and classical sampler are established prior work. The new construction retains a uniform spectral floor in every sampled block. It then gives a size-independent inverse-noise radius, including for heterogeneous nonunital single-site channels.

The mathematical conclusions are distinct from an implemented physical interface. The accepted fault-tolerant preparation and independent product-Pauli boundary provide one compatible physical route, with their existing acquisition, routing and noise assumptions. No independent-cell hardware claim or total-resource advantage is made here.

## 1. Main theorem with explicit constants

Let \(r\ge1\) be fixed and let

\[
H_N=\sum_j h_j,\qquad \|h_j\|_\infty\le1,
\]

be a qubit-chain or qubit-ring Hamiltonian, with at most one term anchored at each site and each term supported on at most \(r\) consecutive sites. Terms may be noncommuting, nonuniform and sign-indefinite. A bounded total interaction strength per anchor can be absorbed into the inverse temperature. Fix \(0\le\beta<\infty\), and write

\[
\rho_{\beta,N}=\frac{e^{-\beta H_N}}{\operatorname{tr}e^{-\beta H_N}}.
\]

Define the following conservative constants:

\[
\begin{aligned}
R&=\max(2,r), &\bar\beta&=\max(1,\beta),\\
m_0&=\text{least odd integer at least }
 \exp\!\left[R\bar\beta\,2240^{\,2R}\right],&
m&=2m_0,\\
a&=\tfrac12e^{-7m},&
s&=a/2,\\
L&=\left\lceil 1+\frac2a
  \left[\log\frac4a+m\log8\right]\right\rceil,&
B&=4mL,\\
\Lambda&=\exp(2R\bar\beta\,m_0),&
\kappa_g&=64^m e^{2\beta m},\\
K_0&=\frac{2^{m+1}\kappa_g}{s},&
\eta&=\min\!\left\{
 e^{-2\beta B},\ (K_0\Lambda^4)^{-B}
 \right\}.
\end{aligned}                                                     \tag{1}
\]

In particular, \(B<\infty\) and \(0<\eta\le1\) depend only on \(\beta,r\).

**Theorem 1 — Uniformly interior block mixture.** There is a probability distribution over partitions \(\mathcal P_\mu\) into contiguous blocks and normalized density matrices \(\tau_{\mu,A}\) such that

\[
\rho_{\beta,N}
=
\mathbb E_\mu\!
 \left[\bigotimes_{A\in\mathcal P_\mu}\tau_{\mu,A}\right],
\qquad
|A|\le B,
\qquad
\tau_{\mu,A}\succeq
\eta\,\frac{I_A}{2^{|A|}}.                                        \tag{2}
\]

For fixed \(\beta,r\), the construction gives a classical algorithm polynomial in \(N\) and \(1/\epsilon\) that samples finite descriptions of block states whose averaged product is within \(\epsilon\) in trace norm of \(\rho_{\beta,N}\). The numerical leaves can all be required to satisfy the certified bound

\[
\widetilde\tau_{\mu,A}\succeq
\frac{\eta}{2}\,\frac{I_A}{2^{|A|}}.                              \tag{3}
\]

The hidden constants are exceptionally large. The theorem is a uniform constructive statement, not a useful laboratory threshold estimate.

For the algorithmic statement, the local terms and temperature are supplied digitally, with their representation and requested-precision evaluation costs charged. This is a target-state specification, not learning of a fabricated holding Hamiltonian. Denote the input description length by \(\ell_{\rm in}\). If the target specification itself is rounded from \(H\) to \(H+\Delta H\), the additional trace error is at most \(2\beta\|\Delta H\|_\infty\), by differentiating the normalized Gibbs exponential and applying Schatten Hölder. That error has its own budget.

For a ring, contiguous means a cyclic interval. For an open chain, one may append \(2B\) uncoupled maximally mixed dummy qubits mathematically, apply the ring construction and trace them out. No block of length at most \(B\) can cross this entire dummy interval, so all surviving blocks are contiguous in the original open chain. Partial trace preserves the floor in (2). The additional \(2B\) sites are a constant at fixed \(\beta,r\); their partial traces are computed on the classical block descriptions, so physical dummy output qubits are unnecessary. Chains shorter than \(B\) may instead be treated directly as a single block.

## 2. Source inputs

The proof uses the following primary results, with their original scope.

1. **Pilatowsky-Cameo, Styliaris, Bakshi and Malz**, *One-dimensional quantum Gibbs states in constant circuit depth*, arXiv:2609.35973v1, 28 September 2026: https://arxiv.org/pdf/2609.35973 . Appendix A, Lemma A1 and Corollary A1 give a positive decomposition of a staircase of quasilocal perturbations; equation (A6) gives a midpoint-cut operator; Appendix B gives a constructive sampler with nearest-neighbor classical trace weights. Theorems 1–2 supply the prior pure-block and sampling theorems.

2. **Bakshi, Choi and Pilatowsky-Cameo**, *Entanglement in quantum spin chains is strictly finite at any temperature*, arXiv:2602.13386v2, updated 2 November 2026: https://arxiv.org/pdf/2602.13386 . Lemma 8.4 writes the finite-support Araki dressing matrix as a product of finite-volume Gibbs exponentials and bounds both its norm and its inverse.

The source construction supplies

\[
\rho_{\beta,N}\ \propto\
M\left[\sum_\nu w_\nu
 \bigotimes_jG_j^{(\nu)}\right]M^\dagger,
\quad
G_j=e^{-\beta H_{B_j}/2}\omega_j e^{-\beta H_{B_j}/2},
\quad
\omega_j\succeq64^{-m}I,\quad \operatorname{tr}\omega_j=1.           \tag{4}
\]

Here the elementary-block lengths can be chosen in \([m_0,2m_0]\), and \(M\) is a product of local matrices \(M_j\) near their boundaries. The source allows arbitrary anchor positions before selecting uniform spacing for convenience. At the midpoint cut of an elementary block, **no dressing operator crosses the cut**. It is unnecessary, and in some equal-spacing cases incorrect, to require a midpoint site outside all dressing supports.

For each block there is a full-rank positive operator \(G'_j\), product across that midpoint cut, with

\[
G'_j\preceq G_j\preceq e^{7m}G'_j.                               \tag{5}
\]

Using the upper block-length bound \(m\) in the prefactor of the source's \(G'_j\) preserves this conservative sandwich. The midpoint identity factor in the finite-volume cut Hamiltonian is implicit.

The local dressing is invertible. After the source's folding and normalization, its finite-volume exponentials involve at most \(m_0\) bounded terms and absorbed inverse temperature at most \(R\bar\beta\). Consequently, the crude explicit choice in (1) gives

\[
\|M_j\|_\infty,\ \|M_j^{-1}\|_\infty\le\Lambda.                    \tag{6}
\]

The exact first-stage distribution over \(\nu\) includes the trace weight of (4); it is the source's equation (B2), not the unnormalized coefficient \(w_\nu\) alone.

## 3. Keep the cut remainder strictly positive

Set

\[
F_j=G'_j/2,\qquad \Delta_j=G_j-F_j.
\]

Equation (5) gives

\[
aG_j\preceq F_j\preceq G_j/2,\qquad
G_j/2\preceq\Delta_j\preceq(1-a)G_j.                             \tag{7}
\]

Halving the cut factor prevents \(\Delta_j\) from acquiring zero eigenvalues while preserving the exact cut.

Group consecutive elementary blocks into superblocks containing between \(L\) and \(2L\) blocks. In a superblock of \(\ell\ge L\) blocks, number them \(0,\ldots,\ell-1\). The exact first-cut expansion is

\[
\begin{aligned}
\bigotimes_{j=0}^{\ell-1}G_j
={}&
\sum_{b=1}^{\ell-1}
 \left(\bigotimes_{j<b}\Delta_j\right)\otimes F_b
 \otimes\left(\bigotimes_{j>b}G_j\right)\\
&+F_0\otimes\left(\bigotimes_{j>0}G_j\right)
 +\bigotimes_j\Delta_j . 
\end{aligned}                                                    \tag{8}
\]

The product \(j<b\) includes \(j=0\). Every term in the first sum already has a midpoint cut and full-rank factors. The last two terms must be handled jointly.

## 4. Replace spectral projectors by full-rank factors

For \(j>0\), diagonalize

\[
A_j=G_j^{-1/2}\Delta_jG_j^{-1/2}
=\sum_t\lambda_{j,t}P_{j,t},
\qquad \lambda_{j,t}\in[1/2,1-a],
\]

using rank-one orthogonal projectors; any orthonormal basis within a degenerate eigenspace is valid. With \(d_j\) the elementary-block dimension, put

\[
Q_{j,t}=(1-s)P_{j,t}+sI/d_j,
\quad
\bar\lambda_j=\operatorname{tr}(A_j)/d_j,
\quad
b_{j,t}=\frac{\lambda_{j,t}-s\bar\lambda_j}{1-s}.                  \tag{9}
\]

Directly collecting the identity and spectral coefficients gives

\[
\sum_tQ_{j,t}=I,\qquad
\sum_tb_{j,t}Q_{j,t}=A_j,\qquad
Q_{j,t}\succeq sI/d_j.                                         \tag{10}
\]

Moreover,

\[
0\le b_{j,t}
\le\frac{1-a}{1-a/2}
\le1-a/2.                                                      \tag{11}
\]

The lower bound follows from \(\lambda_{j,t}\ge1/2\), \(\bar\lambda_j\le1\) and \(s\le1/4\); the upper bound follows by dropping the nonnegative subtraction in (9).

Thus the positive matrices

\[
E_{j,t}=G_j^{1/2}Q_{j,t}G_j^{1/2}
\]

satisfy

\[
G_j=\sum_tE_{j,t},\qquad
\Delta_j=\sum_tb_{j,t}E_{j,t},\qquad
E_{j,t}\succeq(s/d_j)G_j.                                     \tag{12}
\]

This is the replacement for the rank-deficient spectral factors in the source's equation (A10).

## 5. Resolve the exceptional term with mixed Pauli products

Substituting (12) into the last two terms of (8) yields a positive sum over \(\mathbf t=(t_1,\ldots,t_{\ell-1})\) of

\[
F_0^{1/2}(I+K_{\mathbf t})F_0^{1/2}
 \otimes\bigotimes_{j>0}E_{j,t_j},
\]

where

\[
K_{\mathbf t}
=
\left(\prod_{j>0}b_{j,t_j}\right)
F_0^{-1/2}\Delta_0F_0^{-1/2}.
\]

Equations (7) and (11), and the choice of \(L\), give

\[
\|K_{\mathbf t}\|_\infty
\le a^{-1}(1-a/2)^{\ell-1}
\le a^{-1}e^{-a(L-1)/2}
\le\frac14\,8^{-m}.                                            \tag{13}
\]

For a Hermitian \(K\) on \(k\le m\) qubits, expand \(K=\sum_P\alpha_PP\) in the Pauli basis. Let \(c=1+\alpha_I\), \(u=1/2\), and

\[
w_P=|\alpha_P|u^{-\operatorname{wt}(P)} \quad (P\ne I).
\]

Since \(|\alpha_P|\le\|K\|_\infty\) and
\(\sum_Pu^{-\operatorname{wt}(P)}=7^k\le8^m\),

\[
\sum_{P\ne I}w_P\le1/4,
\qquad c\ge1-\|K\|_\infty>3/4.
\]

Hence

\[
I+K=
\left(c-\sum_{P\ne I}w_P\right)I+
\sum_{P\ne I}w_P
 \left[I+\operatorname{sgn}(\alpha_P)u^{\operatorname{wt}(P)}P\right]
                                                                  \tag{14}
\]

is a positive sum with slack. The bracket divided by \(2^k\) is the uniform mixture, with the required parity of signs, of products of the states

\[
\frac{I\pm u\sigma}{2}.
\]

Identity slots use \(I/2\). These local mixed states have eigenvalues \(1/4,3/4\). Every normalized product factor therefore has minimum eigenvalue at least \(4^{-m}\), and condition number at most \(3^m\).

Because \(F_0\) is product across the midpoint cut, conjugation by \(F_0^{1/2}\) preserves the cut and strict positivity. Thus every term of (8) has a cut in its superblock and all resulting factors are full rank.

## 6. Uniform floor after dressing

The first and last superblocks can be grouped so each contains between \(L\) and \(2L\) elementary blocks. Consecutive selected cuts are therefore separated by at most \(B=4mL\) qubits. No \(M_j\) crosses any selected cut, so conjugation by \(M\) preserves the final block product.

Using \(\|H_{B_j}\|_\infty\le m\), the elementary condition-number estimates are

\[
\begin{aligned}
\kappa(G_j)&\le\kappa_g,\\
\kappa(\Delta_j)&\le2\kappa_g,\\
\kappa(E_{j,t})&\le2^m\kappa_g/s,\\
\kappa(F_j^{1/2}P_{\rm mix}F_j^{1/2})
 &\le e^{2\beta m}3^m.
\end{aligned}                                                    \tag{15}
\]

Here \(P_{\rm mix}\) denotes one mixed Pauli product from (14). Each is bounded by \(K_0\) in (1). Splitting a positive tensor product across its cut cannot increase either factor's condition number beyond that of the product.

A final block contains at most \(B\) elementary factors and at most \(B\) dressing matrices. Each congruence multiplies its condition-number bound by at most \(\Lambda^4\). Its normalized state therefore satisfies

\[
\lambda_{\min}(\tau_A)
\ge\frac1{2^{|A|}(K_0\Lambda^4)^B}
\ge\frac{\eta}{2^{|A|}}.                                       \tag{16}
\]

For \(N<B\), the direct single-block Gibbs estimate is
\(\rho_{\beta,N}\succeq e^{-2\beta N}I/2^N
\succeq e^{-2\beta B}I/2^N\).
This proves (2), including the small-chain branch.

## 7. Constructive finite-precision sampling

The source's first-stage distribution \(\pi_\nu\) is unchanged: for every \(\nu\), the modified decomposition sums to exactly the same tensor product of \(G_j\). Conditional on \(\nu\), each superblock has a finite label alphabet depending only on \(\beta,r\). Its labels specify a cut and the positive factors on its sides. The trace weights after dressing still factor into nearest-neighbor functions of consecutive superblock labels, as in the source's equation (B5). The same finite-state forward-backward sampler applies. The final refinement into pure block states is omitted.

Keep the inherited source work as \(P_{\beta,r}(N,1/\epsilon,\ell_{\rm in})\), an opaque polynomial under its supplied-input computation convention. It is not replaced by the linear cost of the final forward-backward phase. The source's first stage uses a logarithmic QPI-shell cutoff, polynomially many candidate terms, distortion estimates and matrix-product trace calculations; its paper does not display a separate tight Turing bit-complexity bound. The precision statement below concerns the new finite-block calculations and is not a claim of logarithmic precision or near-linear work for the entire inherited sampler. See the companion targeted_prior_art_and_runtime.md for the exact source check.

Here is an explicit sufficient numerical rule for \(0<\epsilon\le1\). Let \(N_*=N+2B\) when padding an open chain, and \(N_*=N\) otherwise.

1. Sample the source first-stage law to total-variation error at most \(\epsilon/32\).

2. Put
   \[
   \zeta=\frac{\epsilon}{256N_*}.
   \]
   For each fixed-size superblock, construct positive cut factors whose sum \(\widetilde T_s\) obeys
   \[
   (1-\zeta)T_s\preceq\widetilde T_s
   \preceq(1+\zeta)T_s,
   \qquad T_s=\bigotimes_{j\in S_s}G_j.                       \tag{17}
   \]
   It suffices to certify
   \(\|\widetilde T_s-T_s\|_\infty
       \le\zeta\lambda_{\min}(T_s)\).
   A uniform available lower bound is
   \[
   \lambda_{\min}(T_s)
   \ge (64^{-m}e^{-\beta m})^{2L}.
   \]
   This quantity depends only on \(\beta,r\).

3. Sample the resulting finite-state nearest-neighbor label law to total-variation error at most \(\epsilon/32\). Compute positive normalized edge weights to relative accuracy \(O(\epsilon/N_*)\), with rescaling or log-domain transfer arithmetic. Handle scalar coefficients separately: coefficients below the chosen additive local-error threshold can be omitted within (17), so no relative accuracy is required at a zero weight.

4. Compute each normalized numerical block to trace error at most \(\epsilon/(16N_*)\), and certify its trace, positivity and floor (3). Refine the arithmetic until both the error certificate and floor hold.

The matrix calculations involve fixed dimensions. Compute any approximate unitary diagonalization with a certified residual, clip the eigenvalues into \([1/2,1-a]\), and form \(Q_t\) by the positive formula (9). Degenerate eigenspaces cause no difficulty. The stronger \(1/4\) slack in (13) allows the central Pauli decomposition to be rounded while remaining positive. Matrix exponentials, square roots and inverses are uniformly continuous on the compact positive spectral ranges used here. The arithmetic precision is \(O(\log(N_*/\epsilon))\) bits plus a potentially enormous \(\beta,r\)-dependent constant for these finite-block steps. The source's first-stage algorithm has its separate polynomial cost.

To see why a global condition number does not enter, tensor (17) over \(q\le N_*\) superblocks:

\[
(1-\zeta)^q\bigotimes_sT_s
\preceq\bigotimes_s\widetilde T_s
\preceq(1+\zeta)^q\bigotimes_sT_s.
\]

Congruence by the exact analytical \(M\) preserves this Loewner sandwich, regardless of its global condition number. After trace normalization, its trace-norm error is at most

\[
2\left[
  \left(\frac{1+\zeta}{1-\zeta}\right)^q-1
 \right]\le16q\zeta\le\epsilon/16.                            \tag{18}
\]

The last inequality uses the chosen small \(\zeta\). Numerical evaluation of local \(M_j\) is charged through the edge-weight and final-block budgets, rather than through a global matrix-inversion bound. First-stage and label-law errors contribute at most \(\epsilon/16\) each, and block-state rounding contributes at most \(\epsilon/16\) by product telescoping. The combined trace error is at most \(\epsilon/4\), leaving ample room within the requested \(\epsilon\).

This is a constructive sampling statement. It does not require enumerating exponentially many global labels, exact eigenvectors, exact nonzero-weight tests, or a global rejection step.

## 8. Corollary: heterogeneous nonunital local channels

Define the explicit positive radius

\[
\delta_0
=
1-
\left(1+\frac{\eta}{2^{B+2}}\right)^{-1/B}.
                                                                  \tag{19}
\]

Let \(\mathcal E_i\) be any single-site CPTP maps, possibly different at every site and possibly nonunital, satisfying

\[
\|\mathcal E_i-\mathrm{id}\|_\diamond\le\delta_0.
\]

Since \(\delta_0<1\), the Neumann series gives linear inverses that preserve trace and Hermiticity, with

\[
\|\mathcal E_i^{-1}\|_\diamond\le(1-\delta_0)^{-1}.
\]

For \(A\) of size at most \(B\),

\[
\left\|
 \mathcal E_A^{-1}-\mathrm{id}
\right\|_\diamond
\le(1-\delta_0)^{-|A|}-1
\le\frac{\eta}{2^{B+2}},
\qquad
\mathcal E_A=\bigotimes_{i\in A}\mathcal E_i.                  \tag{20}
\]

For an exact leaf \(\tau_A\) from (2), its preimage
\(\sigma_A=\mathcal E_A^{-1}(\tau_A)\) is therefore positive.
More strongly, for an actual numerical leaf satisfying (3),

\[
\widetilde\sigma_A
=\mathcal E_A^{-1}(\widetilde\tau_A)
\succeq\frac{\eta}{4}\frac{I_A}{2^{|A|}},
\qquad
\operatorname{tr}\widetilde\sigma_A=1.                         \tag{21}
\]

Indeed, the inverse correction has operator norm at most its trace norm, bounded by \(\eta/2^{B+2}\). This is at most one half of the floor in (3).

Thus the exact ensemble has an exact positive preimage

\[
\sigma_{\beta,N}
=
\mathbb E_\mu\bigotimes_A\mathcal E_A^{-1}(\tau_{\mu,A}),
\qquad
\left(\bigotimes_i\mathcal E_i\right)(\sigma_{\beta,N})
=\rho_{\beta,N}.                                               \tag{22}
\]

The inverse acts only on bounded blocks, and the same label probabilities are retained. The local channels need not commute with the Hamiltonian, satisfy detailed balance, or preserve the maximally mixed state.

This is a mathematical theorem about known channels. It does not establish an apparatus interface for arbitrary heterogeneous nonunital channels. The already accepted independent product-Pauli boundary is one realized special case under its own noise and control model.

## 9. Corollary: invert each actual leaf, then deliver forward

For a sampled finite-precision target leaf, invert that **actual** matrix as in (21). Do not first approximate the global Gibbs matrix and then apply the global inverse channel.

With exact finite-block arithmetic,

\[
\mathcal E_A(\widetilde\sigma_A)=\widetilde\tau_A
\]

for every sample. Consequently,

\[
\left(\bigotimes_i\mathcal E_i\right)
\left[
 \mathbb E_\mu\bigotimes_A\widetilde\sigma_{\mu,A}
\right]
=
\mathbb E_\mu\bigotimes_A\widetilde\tau_{\mu,A}.                 \tag{23}
\]

The delivered error is exactly the sampler's forward target error. No exponential amplification by a global inverse norm appears.

Each inverse in (21) is a constant-size linear-system computation at fixed \(\beta,r\). A spectral decomposition gives a purification of the resulting positive density matrix, from which an explicit known-state preparation circuit can be synthesized to any requested block trace error. The matrix sizes, purification workspace and constant prefactors can be exceptionally large. This constructs the circuit description; physical execution must still use a compatible implemented compiler.

For finite synthesis, choose trace-one positive matrices
\(\widehat\sigma_{\mu,A}\) with

\[
\|\widehat\sigma_{\mu,A}-\widetilde\sigma_{\mu,A}\|_1
\le\xi_A,
\qquad
\sum_A\xi_A\le\xi.
\]

The floor in (21) permits certified finite arithmetic without approaching the positivity boundary. Contractivity of the forward channels and product telescoping bound the additional delivered error by \(\xi\). If actual channels \(\mathcal F_i\) satisfy
\(\|\mathcal F_i-\mathcal E_i\|_\diamond\le\kappa_i\), their further forward error is at most \(\sum_i\kappa_i\). A compatible physical simulation error \(\epsilon_{\rm sim}\) adds separately:

\[
\|\rho_{\rm delivered}-\rho_{\beta,N}\|_1
\le
\epsilon_{\rm sampler}+\xi+
\sum_i\kappa_i+\epsilon_{\rm sim}.                              \tag{24}
\]

This is an error-budget identity, not an assumption that acquisition, synthesis or simulation are free. Root's physical construction supplies and charges those operations.

## 10. Two boundaries and deductions

### Entangled thermal states are included

For the Heisenberg dimer
\(H=(XX+YY+ZZ)/3\),

\[
\rho_\beta
=\frac14[I-t(XX+YY+ZZ)],
\quad
t=\frac{e^{4\beta/3}-1}{e^{4\beta/3}+3}.
\]

Under identical local depolarizing channels with Bloch contraction \(\lambda>0\), the unique preimage has \(t_{\rm in}=t/\lambda^2\). It is positive exactly when \(t\le\lambda^2\). The target is entangled exactly when \(t>1/3\), as follows from its partial transpose. Hence there is an attainable entangled regime when \(\lambda^2>1/3\).

There is also an exact optimal approximation boundary, independently derived and checked in the companion boundaries/local_factory_geometry.md:

\[
\inf_\sigma\frac12
 \|\rho_t-(\mathcal D_\lambda\otimes\mathcal D_\lambda)(\sigma)\|_1
=\frac34(t-\lambda^2)_+.                                      \tag{25a}
\]

Here \(\mathcal D_\lambda\) denotes the channel with Bloch contraction \(\lambda\), rather than the replacement-probability convention used below. Twirling by \(U\otimes U\) preserves the target, commutes with this channel and contracts trace distance; it reduces the input to a Werner state with parameter \(v\in[-1/3,1]\). The output parameter is \(\lambda^2v\), and the distance between Werner parameters \(t\) and \(v'\) is \(3|t-v'|/4\). Choosing \(v=\min(t/\lambda^2,1)\) attains (25a). At \(\lambda=0\), the output is \(I/4\) and the same formula holds directly. Thus the obstruction is accompanied by an attaining preparation.

A size-independent noise radius cannot also be uniform over all temperatures. Even \(H=-Z\) on one qubit requires depolarizing contraction at least \(\tanh\beta\) to reach its Gibbs state. The much smaller constants in (19) are sufficient bounds, not claims of optimality.

### A local heralding floor

Take
\(\mathcal D_p(X)=(1-p)X+p\,\operatorname{tr}(X)I/2\)
with \(p=\delta_0/2>0\).
The elementary bound
\(\|\mathcal D_p-\mathrm{id}\|_\diamond\le2p\)
allows (22), so

\[
\rho_{\beta,N}=\mathcal D_p^{\otimes N}(\sigma)
\]

for some positive \(\sigma\). Any trace-nonincreasing completely positive operation on all sites other than a selected site commutes with that selected site's \(\mathcal D_p\). For every heralding outcome of nonzero probability, the normalized conditional state at that site therefore obeys

\[
\rho_{i\mid{\rm outcome}}\succeq pI/2.                          \tag{25}
\]

Thus conditioning only on other sites cannot produce an arbitrarily pure selected-site state from the exact finite-temperature Gibbs state.

This is a deduction of the product-preimage theorem, not a priority claim for the qualitative heralding obstruction. Related uniform conditional-state floors follow from existing local Gibbs-comparability/Araki estimates, often with much better constants. The contribution here is a common constructive product-preimage representation for the entire chain. For an approximately delivered state with global trace error \(\epsilon\), conditioning on an event of probability \(q>0\) can magnify error by at most \(2\epsilon/q\); no probability-independent approximation guarantee is asserted for arbitrarily rare heralds.

## 11. Physical scope and the unsuccessful independent-cell route

Uniformly interior states in an actually isolated finite cell lie in the convex hull of a sufficiently fine, sufficiently accurate finite physical preparation menu. That geometric observation does not complete preparation on a fixed chain whose sampled block boundaries are random. Noisy scheduling, coupler selection or routing can create interactions across intended blocks. The proposal to infer independent physical cells directly from the random-block decomposition therefore remains unproved and is not used.

The compatible completed route uses the already earned global fault-tolerant preparation and independent product boundary, constructing each bounded-block inverse first. It retains the paid fabrication, links, routing, metrology, commissioning and stationary-noise assumptions of that compiler. The state-family theorem makes a target-specific holding bath or target-check isolation unnecessary; it does not by itself change the physical compiler's noise class.

A sampled ensemble label is a classical extension of the mixed state. If it remains an accessible public record, the conditional output is that ensemble member, not the Gibbs marginal. The preparation seed must be discarded or erased with its reset cost charged, or the claimed endpoint must specify the joint extension. Retained calibration and prior history records can instead be included in a uniform conditional error guarantee under the accepted compiler's model.

No unknown-input transmission theorem, indefinite storage guarantee, physical finite-cell construction, favorable numerical threshold, or lower energy/spacetime advantage is inferred from the present result.

## 12. Attribution and audit record

The following components are prior machinery: the ideal pure-block representation, source first-stage sampler, finite-state trace-weight sampler, QPI product floor, Araki dressing locality and invertibility, and general quantum error precompensation.

The new proof components are the halved cut operator, full-rank spectral replacement, mixed-product exceptional-term decomposition, their uniform final block floor, and the resulting constructive many-body local inverse-noise operation. The independent audit confirms the argument and finite-precision closure. This definitive note uses the audit's suggested geometric wording and a stronger central slack than the initial opening.

Primary sources:

- https://arxiv.org/pdf/2609.35973 — Theorems 1–2; Appendix A Lemma A1, Theorem A1, Corollary A1 and equations A6–A10; Appendix B B1–B7; Appendix C C1–C2.
- https://arxiv.org/pdf/2602.13386 — v2, Lemma 8.4 and its explicit local product of exponentials.
- https://arxiv.org/pdf/2403.16850 — product-Pauli parity decompositions and high-temperature coefficient slack.
- https://arxiv.org/pdf/2309.01434 — existing inverse-channel precompensation and semidefinite optimization.

Companion internal audit: ../noncommuting/robust_1d_independent_audit.md .
