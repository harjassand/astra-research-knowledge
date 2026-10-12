# Order-optimal imaginary-to-real-time prediction from quantum snapshots

**ASTRA THEORETICAL — research note, 12 October 2026**

**Status.** This note gives a self-contained mathematical derivation and finite diagnostic checks. It has not received independent proof review or formal verification. Historical novelty is unresolved. The binomial/perfect-transfer mechanism and standard approximation and quantum-information ingredients are not claimed as new. The possible contribution is their combination into an order-optimal inverse-information theorem for *full quantum snapshots*, including adaptive collective measurements, a one-boundary-parameter local realization, and a finite-bit variant. No theorem from the earlier near-convex Hamiltonian construction, the Astra archive, or the OpenAI mathematical manuscript collection is a premise.

## 1. Exact access and output contract

Let \(\mathcal K\) be a known finite-dimensional Hilbert space, let \(v\in\mathcal K\) be a known unit vector, and adjoin a known unit reference \(\Omega\perp\mathcal K\). The unknown Hermitian matrix \(A\) satisfies

\[
I\preceq A\preceq 2I.
\]

We use energy units in which this spectral band is fixed and \(\hbar=1\). For any classically chosen imaginary time \(0\le\tau\le\beta\), the data source returns a fresh copy of

\[
\Psi_A(\tau)=\frac{\Omega+e^{-\tau A/2}v}{\sqrt{1+F_A(\tau)}},
\qquad F_A(z)=\langle v,e^{-zA}v\rangle.
\tag{1}
\]

Here \(\beta\in(0,\infty]\). With \(H=0\oplus A\), this is the normalized imaginary-time evolution of \((\Omega+v)/\sqrt2\). It is **not a Gibbs state**. Applying the ideal contraction to that initial state has squared norm \((1+F_A(\tau))/2\in[1/2,1]\), so the construction does not hide an exponentially rare overall normalization event. The implementation cost of that contraction is a separate resource.

The learner may choose times adaptively using classical measurement outcomes, preserve quantum memory, and perform arbitrary joint quantum operations and measurements. Computation is unrestricted. Each returned snapshot counts as one copy; all copies requested, including discarded or postselected copies, count. The copy budget is a worst-case cap, not only an expected count.

The source does not also supply a classical description of \(A\), arbitrary-input access to \(e^{-\tau A/2}\), or access to physical real-time evolution. Section 10 treats a separate coherent state-preparation query model; it must not be confused with the copy model.

The target is the complex return amplitude

\[
g_A(t)=F_A(it)=\langle v,e^{-itA}v\rangle.
\tag{2}
\]

Let \(Q(t,\beta)\) be the least worst-case copy budget for estimating (2) to additive error \(1/4\), with success probability at least \(2/3\), uniformly over finite dimensions, known seeds, and allowed matrices. An algorithm may depend on the dimension and seed; its stated copy bound is uniform in dimension.

## 2. Main theorem

**Theorem 1 (minimax prediction law).** There are universal constants \(c,C,t_0>0\) such that, for every \(t\ge t_0\) and \(\beta\in(0,\infty]\),

\[
\exp\!\left(c\,t\log(2+t/\beta)\right)
\le Q(t,\beta)
\le
\exp\!\left(C\,t\log(2+t/\beta)\right),
\tag{3}
\]

where \(t/\infty=0\). In particular,

\[
\log Q(t,\beta)=\Theta\!\left(t\log(2+t/\beta)\right).
\]

The lower bound holds already for one-dimensional, nearest-neighbor, bounded-coupling, stoquastic free-spin chains with a unique product ground state and a constant spectral gap. The two alternatives can differ in only the final onsite coefficient. The seed can be a product state and every trajectory state has Schmidt rank at most two across each spatial cut.

For fixed \(\beta>0\), this gives

\[
Q(t,\beta)=\exp(\Theta_\beta(t\log t)),
\qquad t_{\max}(N)=\Theta_\beta(\log N/\log\log N).
\tag{4}
\]

Allowing all imaginary times instead gives

\[
Q(t,\infty)=\exp(\Theta(t)),
\qquad t_{\max}(N)=\Theta(\log N).
\tag{5}
\]

“Order-optimal” refers to universal constants in the exponent, not an exact leading minimax constant. The upper bound is constructive but exponentially costly; it is not an efficient prediction algorithm.

## 3. A folded local chain

Take an odd integer \(n=2m-1\), and initially allow parameters \(a,W>0\). On \(n+1\) sites define the real symmetric Jacobi matrix

\[
B_{jj}=a+W/2,\qquad
B_{j,j+1}=B_{j+1,j}=-\frac{W}{2n}\sqrt{(j+1)(n-j)}.
\tag{6}
\]

Reflection \(R e_j=e_{n-j}\) commutes with \(B\). Restrict to the reflection-even and reflection-odd subspaces, in bases

\[
e_{j,\pm}=(e_j\pm e_{n-j})/\sqrt2,
\qquad 0\le j<m.
\]

The resulting \(m\times m\) matrices \(A_\pm\) have

\[
(A_\pm)_{jj}=a+W/2\quad (j<m-1),
\qquad
(A_\pm)_{m-1,m-1}=a+W/2\mp\frac{Wm}{2n},
\tag{7}
\]

and identical off-diagonals inherited from (6). Thus the two matrices differ in exactly one diagonal entry. In both folded spaces use the same known coordinate seed \(v=e_0\).

To diagonalize (6), identify it with the permutation-symmetric subspace of \(n\) spins:

\[
B=a+W/2-\frac{W}{2n}\sum_{r=1}^n X_r.
\]

The symmetric state with \(k\) spins in the negative \(X\)-eigenstate has energy \(a+Wk/n\) and reflection parity \((-1)^k\). Its endpoint weight is \(2^{-n}\binom nk\). Conditioning on reflection parity doubles this weight. Hence

\[
\mu_+=2^{1-n}\sum_{k\ \mathrm{even}}\binom nk\delta_{a+Wk/n},
\qquad
\mu_-=2^{1-n}\sum_{k\ \mathrm{odd}}\binom nk\delta_{a+Wk/n}.
\tag{8}
\]

These are probability measures; even and odd binomial sums are both \(2^{n-1}\). In particular, both spectra lie in \([a,a+W]\).

The binomial theorem gives

\[
F_\pm(\tau)=e^{-a\tau}2^{-n}
\left[(1+e^{-W\tau/n})^n\pm(1-e^{-W\tau/n})^n\right],
\tag{9}
\]

so their difference is

\[
\Delta(\tau)=F_+(\tau)-F_-(\tau)
=2e^{-a\tau}\left(\frac{1-e^{-W\tau/n}}2\right)^n.
\tag{10}
\]

At real time \(t_n=\pi n/W\), all even-sector eigenphases agree, and all odd-sector eigenphases have the opposite sign:

\[
e^{-it_nA_\pm}=\pm e^{-iat_n}I,
\qquad g_\pm(t_n)=\pm e^{-iat_n}.
\tag{11}
\]

Thus the target values have distance exactly two.

For the canonical choice \(a=W=1\), the active spectral band is \([1,2]\), \(t_n=\pi n\), and, since \(n\) is odd,

\[
g_+(t_n)=-1,\qquad g_-(t_n)=1.
\]

The scalar functions already show an obstruction, but scalar indistinguishability alone does not control all information in the quantum states. The next section supplies that missing step.

## 4. Full-state distinguishability, not merely correlators

Put

\[
y=e^{-W\tau/(2n)},\quad \alpha=(1+y)/2,\quad\gamma=(1-y)/2.
\]

The coordinates of the full-chain vector \(e^{-\tau B/2}e_0\) are

\[
f_j=e^{-a\tau/2}\sqrt{\binom nj}\,\alpha^{n-j}\gamma^j.
\tag{12}
\]

This follows by exponentiating the commuting single-spin \(X_r\) terms. The folded vectors have coordinates

\[
x_{\pm,j}:=(e^{-\tau A_\pm/2}v)_j=f_j\pm f_{n-j}.
\tag{13}
\]

Since \(\alpha\ge\gamma\ge0\), one has \(f_j\ge f_{n-j}\ge0\) for \(j<m\). Define

\[
S=\sum_{j<m}f_j^2,\quad T=\sum_{j\ge m}f_j^2,
\quad U=\sum_{j<m}f_jf_{n-j}.
\tag{14}
\]

Then

\[
F_\pm=S+T\pm2U,\quad \Delta=4U,\quad
T\le U,\quad U^2\le ST,\quad S+T\le1.
\tag{15}
\]

The last inequality uses \(B\succeq aI\), so \(\|e^{-\tau B/2}e_0\|\le1\).

Write \(D(\rho,\sigma)=\tfrac12\|\rho-\sigma\|_1\). For pure states, \(D^2=1-|\langle\psi,\phi\rangle|^2\). Equations (13)-(15) give the exact identity

\[
D(\Psi_+,\Psi_-)^2
=\frac{4\,[T(1+S)-U^2]}{(1+S+T)^2-4U^2}.
\tag{16}
\]

Indeed, the unnormalized overlap is \(1+S-T\), while the product of squared norms is the denominator in (16).

The numerator is at least \(4T\), and the denominator is at most four. Conversely, the numerator is at most \(4T(1+S)\), while

\[
(1+S+T)^2-4U^2\ge1+2S+2T+(S-T)^2\ge1+S.
\]

Therefore

\[
\boxed{T\le D(\Psi_+,\Psi_-)^2\le4T\le\Delta(\tau).}
\tag{17}
\]

This bounds the complete quantum states, including every possible global measurement.

For \(a=W=1\), set \(z=e^{-\tau/n}\). Equation (10) becomes

\[
\Delta(\tau)=2\,[z(1-z)/2]^n.
\]

Consequently,

\[
\sup_{\tau\ge0}\Delta(\tau)=2\,8^{-n},
\qquad
\sup_{0\le\tau\le\beta}\Delta(\tau)\le2(\beta/(2n))^n.
\tag{18}
\]

The first maximum occurs at \(\tau=n\log2\); the second inequality uses \(1-e^{-x}\le x\). More generally, with \(r=a/W\),

\[
\sup_{\tau\ge0}\Delta(\tau)
=2\left[\frac{r^r}{2(1+r)^{1+r}}\right]^n.
\tag{19}
\]

## 5. Adaptive quantum-copy lower bound

**Lemma 2.** Suppose a source indexed by a classical query \(\tau\) supplies one of two pure states, and their trace distance is at most \(d\) at every allowed query. Any protocol using at most \(N\) fresh copies, adaptive classical queries, and arbitrary intervening quantum processing has final trace distance at most \(\sqrt N\,d\).

**Proof.** Use root fidelity \(\mathcal F(\rho,\sigma)=\|\sqrt\rho\sqrt\sigma\|_1\). It is nondecreasing under quantum channels, multiplicative on tensor products, and equals the absolute overlap on pure states. Immediately before a query, retain the classical outcome history. The joint states are block diagonal in that history. Their root fidelity is the sum of the block fidelities, weighted by the geometric means of the corresponding history probabilities. Appending the source state to each block multiplies that block's root fidelity by at least \(\sqrt{1-d^2}\). Subsequent processing cannot decrease the fidelity. Starting from the same state under the two hypotheses,

\[
\mathcal F_{\mathrm{final}}\ge(1-d^2)^{N/2}.
\]

The trace-distance/fidelity inequality and Bernoulli's inequality give

\[
D_{\mathrm{final}}^2\le1-\mathcal F_{\mathrm{final}}^2
\le1-(1-d^2)^N\le Nd^2.
\]

Variable stopping can be padded to the worst-case cap with hypothesis-independent operations. This proves the lemma. The fidelity ingredients are standard quantum-information results, not new claims; see [5]. \(\square\)

An estimator accurate to \(1/4\) on both values in (11) yields a binary test successful with probability at least \(2/3\) on both hypotheses, by assigning the estimate to the nearer target. Thus \(D_{\mathrm{final}}\ge1/3\). Combining the lemma with (17)-(18), the canonical pair requires

\[
\boxed{N\ge\frac1{18}\max\{8^n,(2n/\beta)^n\}.}
\tag{20}
\]

This bound permits arbitrary collective quantum measurements and adaptive time choices.

To obtain the lower bound at every sufficiently large real \(t\), choose the largest odd \(n\le t/(2\pi)\), put \(a=1\), and choose \(W=\pi n/t\). For \(t\ge6\pi\),

\[
t/(4\pi)\le n\le t/(2\pi),\qquad 1/4\le W\le1/2.
\]

The spectra lie in \([1,3/2]\), and (11) holds at precisely the requested time \(t\). The function \(r^r/[2(1+r)^{1+r}]\) is decreasing in \(r>0\), because its logarithmic derivative is \(\log(r/(1+r))<0\). Since \(r=1/W\ge1\), (19) is at most \(2\,8^{-n}\). The finite-window estimate is now

\[
\Delta(\tau)\le2(W\beta/(2n))^n=2(\pi\beta/(2t))^n.
\]

It follows that

\[
N\ge\frac1{18}\max\{8^n,(2t/(\pi\beta))^n\}.
\]

Taking logarithms, using \(n=\Theta(t)\), and absorbing fixed constants proves the lower side of (3), uniformly in \(\beta\).

## 6. Matching universal upper bound

This argument uses only the spectral band \([1,2]\), not the chain structure. By the spectral theorem,

\[
F_A(z)=\int_1^2 e^{-\omega z}\,d\mu_A(\omega)
\]

for a probability measure \(\mu_A\). In particular, for \(\operatorname{Re}z\ge0\),

\[
|F_A^{(k)}(z)|\le2^k.
\tag{21}
\]

Let \(b=\min\{\beta,t\}\), \(R_t=\sqrt{t^2+b^2}\), and \(k=\lceil4eR_t\rceil\). Use real interpolation nodes \(\tau_j=jb/k\), \(0\le j\le k\), with Lagrange basis \(\ell_j\).

The Hermite-Genocchi divided-difference identity expresses an order-\(k+1\) divided difference as the integral of \(F_A^{(k+1)}\) over a simplex of volume \(1/(k+1)!\), evaluated on convex combinations of the nodes and \(it\). The identity follows by successive applications of the fundamental theorem of calculus along complex line segments, so it applies to these complex nodes. Their convex hull lies in the closed right half-plane. Hence (21) and the interpolation remainder formula imply

\[
\left|F_A(it)-\sum_{j=0}^k\ell_j(it)F_A(\tau_j)\right|
\le\frac{(2R_t)^{k+1}}{(k+1)!}
\le2^{-(k+1)}.
\tag{22}
\]

The last step uses \(s!\ge(s/e)^s\).

The interpolation noise amplification satisfies

\[
\Lambda:=\sum_{j=0}^k|\ell_j(it)|
\le(R_tk/b)^k\sum_{j=0}^k\frac1{j!(k-j)!}
=(R_tk/b)^k\frac{2^k}{k!}
\le(2eR_t/b)^k.
\tag{23}
\]

To estimate the real-node data, measure the projector onto \(\Omega\). Its probability is

\[
p_A(\tau)=\frac1{1+F_A(\tau)}\in[1/2,1].
\tag{24}
\]

Clip the empirical probability to \([1/2,1]\), and set \(\widehat F=1/\widehat p-1\). The transformation is 4-Lipschitz on this interval. Set \(\eta=1/(16\Lambda)\). Hoeffding's inequality shows that

\[
N_j=\left\lceil8\eta^{-2}\log(6(k+1))\right\rceil
\]

copies at each node suffice for \(|\widehat F_A(\tau_j)-F_A(\tau_j)|\le\eta\) simultaneously for all nodes, with probability at least \(2/3\). Indeed each node fails with probability at most \(1/[3(k+1)]\).

Return

\[
\widehat g=\sum_{j=0}^k\ell_j(it)\widehat F_A(\tau_j).
\]

Its error is at most \(2^{-(k+1)}+\Lambda\eta<1/4\) for \(t\ge1\). The total copy count is at most a universal constant times

\[
(k+1)\Lambda^2\log(k+1).
\]

Since \(k=O(t)\) and

\[
\log(2eR_t/b)=O(\log(2+t/\beta)),
\]

taking logarithms proves the upper side of (3). \(\square\)

The algorithm requires high precision and exponentially many copies. No implementation or favorable runtime is asserted. Finite query-time and arithmetic precision can be allocated to keep their amplified errors below the same constant error budget. For example, \(|F_A'(\tau)|\le2\) means time errors \(O(1/\Lambda)\) suffice; their bit precision is \(O(t\log(2+t/\beta))\), in addition to the representation of the requested times. The main theorem counts copies, not the total cost of preparing them.

## 7. Sharper asymptotics for the explicit binary family

Let \(Q_{\mathrm{pair}}(n,\beta)\) be the copy complexity of deciding the canonical pair, known in advance except for its sign. Equation (17) and Lemma 2 imply

\[
Q_{\mathrm{pair}}(n,\beta)=\Theta(1/T_{\max}),
\qquad T_{\max}=\sup_{0\le\tau\le\beta}T(\tau).
\tag{25}
\]

For the upper side, choose a maximizing (or constant-factor maximizing) time, repeatedly measure the projector onto \(\Psi_+(\tau)\), and declare minus when its complement is observed. Under plus this has no error; under minus, \(O(1/D^2)\) copies make the probability of never observing the complement at most \(1/3\). Thus no computational or measurement implementation claim is hidden in (25), and the asymptotics do not require adaptive measurements.

Put

\[
b_n=2^{-n}\binom n{(n+1)/2}=\Theta(n^{-1/2}),
\qquad z=e^{-\tau/n},\quad q=(1-\sqrt z)/(1+\sqrt z).
\]

The first term in the binomial tail is

\[
T_0=f_{(n+1)/2}^2=b_nq\,[z(1-z)/2]^n.
\tag{26}
\]

The ratio of consecutive tail terms is at most \(q^2\), so

\[
T_0\le T\le T_0/(1-q^2).
\tag{27}
\]

At \(z=1/2\), \(q=3-2\sqrt2\), a positive constant, giving \(T_{\max}\ge c n^{-1/2}8^{-n}\). For the upper bound, note

\[
q/(1-q^2)=(1-z)/(4\sqrt z).
\]

Therefore

\[
T\le\frac{b_n}4\,2^{-n}z^{n-1/2}(1-z)^{n+1}
\le\frac{b_n}4\,[z^{r_n}(1-z)/2]^n,
\quad r_n=1-1/(2n).
\]

The maximum of the last bracket is \(r_n^{r_n}/[2(1+r_n)^{1+r_n}]\). On \(r\in[1/2,1]\), its logarithmic derivative has absolute value at most \(\log3\). Comparing with the value \(1/8\) at \(r=1\) gives an \(n\)-th-power ratio at most \(\sqrt3\). Hence

\[
\boxed{Q_{\mathrm{pair}}(n,\infty)=\Theta(\sqrt n\,8^n).}
\tag{28}
\]

For fixed \(\beta>0\), eventually \(\beta<n\log2\). Both \(q\) and \(z(1-z)\) increase as \(\tau\) increases in this window. Thus (26)-(27) sandwich \(T_{\max}\) between \(T_0(\beta)\) and \(T_0(\beta)/(1-q(\beta)^2)\). As \(n\to\infty\),

\[
b_n\sim\sqrt{2/(\pi n)},\quad q(\beta)\sim\beta/(4n),
\]

and

\[
[z(1-z)/2]^n\sim e^{-3\beta/2}(\beta/(2n))^n.
\]

It follows that

\[
\boxed{Q_{\mathrm{pair}}(n,\beta)
=\Theta_\beta\!\left(n^{3/2}(2n/\beta)^n\right).}
\tag{29}
\]

The exact exponential base eight is proved for this particular binary family, not as a leading constant for the unrestricted minimax problem.

## 8. Spin-chain realization and what is physically established

Let \(n_j=|1\rangle\langle1|_j\), and use the entries of (7) and positive hopping magnitudes \(J_j=-A_{j,j+1}\) to define

\[
H_\pm=\sum_j d_j^\pm n_j
-\sum_{j<m-1}J_j(\sigma_j^+\sigma_{j+1}^-+\sigma_j^-\sigma_{j+1}^+).
\tag{30}
\]

The vacuum \(\Omega=|0\cdots0\rangle\) has energy zero, and the one-excitation restriction is \(A_\pm\). The Jordan-Wigner transformation expresses (30) as \(\sum_{jk}(A_\pm)_{jk}c_j^\dagger c_k\). Diagonalizing the one-particle matrix shows that every many-particle energy is a sum of its positive one-particle energies. Consequently the vacuum is the unique ground state, and the many-body gap is at least one in the canonical case.

Every term in (30) is uniformly bounded, and every off-diagonal matrix entry in the computational basis is nonpositive. The chain is therefore stoquastic and nearest-neighbor. The full many-body bandwidth is extensive; the fixed \([1,2]\) band in Theorem 1 is the *active one-excitation band*, not the entire many-body spectrum.

The initial state

\[
(\Omega+e_0)/\sqrt2=|+\rangle_0|0\rangle_1\cdots|0\rangle_{m-1}
\]

is a product state. Under either real or imaginary evolution it remains in vacuum plus one excitation. Across any bipartition, such a vector can be written as a sum of at most two product vectors, so its Schmidt rank is at most two. This is an exact bond-dimension-two matrix-product representation, not an approximate area-law argument.

For real evolution of the initial state, the first-spin \(X\) expectation is \(\operatorname{Re}g_A(t)\), while \(Y\) gives \(\operatorname{Im}g_A(t)\) under the usual Pauli convention. At canonical \(t_n=\pi n\), the alternatives give opposite deterministic first-spin \(X\) outcomes. Thus a real-time experiment distinguishes them in evolution time \(O(n)\), whereas the restricted imaginary-time data source requires exponentially or superexponentially many copies.

This is a mathematical construction under ideal coherent dynamics. It does not demonstrate survival under fixed nonzero decoherence as \(n\to\infty\). It does not give an algorithmic separation when the Hamiltonian coefficients themselves are already known: these free chains are then directly diagonalizable.

## 9. Rational coefficients and inverse-polynomial calibration tolerance

The separation is not dependent on storing the square-root couplings to exponential precision.

Choose \(a=5/4\), \(W=1/2\), and \(t_n=2\pi n\), leaving spectral slack inside \([1,2]\). Round all bulk entries identically in the two matrices and round their final diagonal entries on a rational grid. Let the rounded matrices be \(\widetilde A_\pm\), and require

\[
\|\widetilde A_\pm-A_\pm\|\le1/(8t_n).
\tag{31}
\]

Duhamel's formula gives

\[
\|e^{-it_n\widetilde A_\pm}-e^{-it_n A_\pm}\|
\le t_n\|\widetilde A_\pm-A_\pm\|\le1/8.
\]

The real-time amplitude contrast remains at least \(2-1/4=7/4\). For all sufficiently large \(n\), the spectra remain in \([1,2]\).

Because the matrices are tridiagonal, entrywise precision \(O(1/n)\) implies (31), after reducing its constant: the operator norm is bounded by the maximum absolute row sum. A grid with denominator \(O(n)\) therefore needs \(O(\log n)\) bits per entry, and \(O(n\log n)\) bits for the complete pair.

The two rounded matrices still differ only at the last diagonal entry. Consequently

\[
\widetilde A_+^jv=\widetilde A_-^jv\qquad(0\le j<m).
\tag{32}
\]

A path starting at the first site must take at least \(m-1\) hopping steps to reach the last site and a further diagonal step to use the differing coefficient. Thus no product of length below \(m\) detects it.

For \(\|\widetilde A_\pm\|\le B\), Taylor expansion and (32) give

\[
\|e^{-\tau\widetilde A_+/2}v-e^{-\tau\widetilde A_-/2}v\|
\le2e^{B\tau/2}\frac{(B\tau/2)^m}{m!}
\le2e^{B\tau/2}\left(\frac{eB\tau}{2m}\right)^m.
\tag{33}
\]

There is also a bound uniform in all \(\tau\ge0\). Map the Bernstein ellipse of parameter two for \([-1,1]\) onto \([1,2]\). Its leftmost real coordinate is \(7/8>0\), so \(|e^{-\tau z/2}|\le1\) everywhere on the ellipse, uniformly in \(\tau\). The Chebyshev coefficient contour formula bounds the degree-\(j\) coefficient by \(2\cdot2^{-j}\). Truncation before degree \(m\) has error at most \(4\cdot2^{-m}\) on \([1,2]\). Applying the same polynomial to the two matrices and using (32) yields

\[
\|e^{-\tau\widetilde A_+/2}v-e^{-\tau\widetilde A_-/2}v\|
\le8\cdot2^{-m},\qquad\tau\ge0.
\tag{34}
\]

The map \(x\mapsto(\Omega+x)/\sqrt{1+\|x\|^2}\), for \(x\perp\Omega\), is 1-Lipschitz when the complex Hilbert space is viewed as a real Euclidean space: differentiate along a line segment and bound its differential norm by one. Pure-state trace distance is at most the norm of a chosen vector difference. Therefore (33)-(34) also bound snapshot trace distance.

Squaring these bounds and applying Lemma 2 preserves the exponential-order lower bound \(\log Q=\Omega(t\log(2+t/\beta))\) along \(t=t_n\), with different universal constants. For example, (34) covers \(\beta\) a fixed fraction of \(m\) or larger; for smaller \(\beta\), (33) supplies \(\Omega(m\log(m/\beta))\). This robustness statement does **not** preserve the exact binary-family constants (28)-(29).

The tolerance is inverse-polynomial, not constant. Bulk perturbations are matched between the alternatives. This does not establish robustness to arbitrary independent fixed-strength disorder or noise, nor does it establish a translation-invariant construction.

## 10. Coherent state-preparation queries: a separate corollary

A coherent preparation oracle is stronger than a source of fresh copies, so the \(N d^2\) copy lower bound does not automatically apply. Nevertheless an exponential-order obstruction also holds in a worst-case coherent preparation model.

For a normalized snapshot \(\psi=\Psi_A(\tau)\), let

\[
w_\psi=(\Omega+\psi)/\|\Omega+\psi\|,
\qquad U_\psi=2|w_\psi\rangle\langle w_\psi|-I.
\tag{35}
\]

Its reference overlap is real and positive, so \(U_\psi\Omega=\psi\); \(U_\psi\) is a Hermitian unitary and its own inverse. Normalization is uniformly Lipschitz here because \(\|\Omega+\psi\|\ge\sqrt2\). For the two constructed snapshots, whose mutual overlap is nonnegative,

\[
\|U_{\psi_+}-U_{\psi_-}\|\le 8D(\psi_+,\psi_-)
\tag{36}
\]

is a valid conservative bound. It follows by bounding the projector difference by the normalized-vector difference and using \(\|\psi_+-\psi_-\|\le\sqrt2D(\psi_+,\psi_-)\).

For a time-controlled direct-sum oracle, the same bound holds uniformly, with the supremum over allowed times. A hybrid argument bounds the final trace distance of any \(N\)-query algorithm by \(8Nd\), even with inverse queries and coherent time selection. Thus a successful discriminator requires \(N\ge1/(24d)\). Applying (18) gives a lower bound exponential in \(n\), or in \(n\log(n/\beta)\) for short windows. The copy-based upper procedure is also a coherent-query algorithm. Consequently the *logarithmic order* (3) survives for this coherent preparation-oracle family, although the stronger copy-count exponent constants and (28)-(29) do not transfer unchanged.

This is a worst-case statement about preparation unitaries that contain no additional promised information. A preparation oracle could otherwise reveal the unknown Hamiltonian through unspecified columns. Neither this corollary nor Theorem 1 concerns arbitrary-input access to an imaginary-time propagator or a Hamiltonian block encoding.

## 11. Interpretation, prior work, and unresolved objective

The principal logical consequence is:

> Locality, a constant gap, stoquasticity, a known product vacuum, a fixed active energy band, and bond-dimension-two trajectories do not suffice for statistically efficient conversion of imaginary-time trajectory data into later real-time predictions.

The obstruction is not a large entanglement representation, ultraviolet spectral weight, or an inefficient optimization algorithm. In this model it is distinguishability of the available data. Exact noiseless data still determine the return amplitude; finite data do not do so stably at long times.

Classical analytic-continuation ill-conditioning is established literature. Lawrence [1,2] develops positivity-based, model-free bounds for quantities compatible with Euclidean correlation data, including real-time questions. Those results are not negated here. The present lower bound has a compact active energy band, so it does not invoke unbounded high-frequency weight.

The engineered transport mechanism in (6) belongs to the perfect-state-transfer lineage of Christandl, Datta, Ekert, and Landahl [3]. Silva, Taddei, Carrazza, and Aolita [4] prove an imaginary-time no-fast-forwarding theorem in a Hamiltonian block-encoding model; their bound already contains a closely related high-order binomial kernel. Their task is implementing imaginary-time evolution from Hamiltonian queries. The present task is reconstructing real-time information from fixed-input imaginary-time states. Changing the access direction does not by itself prove originality; the potentially distinct claim is the complete minimax law and its strengthened data/physical scope.

### A decisive counterexample to broader access claims

The fixed seed is a necessary part of the result, not a harmless notation choice. If the learner may also request snapshots with the seed at the last site, the canonical boundary bit is easy to learn. Write \(w=e_{m-1}\) and \(F_\pm^{(w)}(\tau)=\langle w,e^{-\tau A_\pm}w\rangle\). Since \(d_- -d_+=m/n\ge1/2\), Taylor expansion and \(\|A_\pm\|\le2\) give

\[
F_+^{(w)}(\tau)-F_-^{(w)}(\tau)
\ge\tau/2-4\tau^2e^{2\tau}\ge\tau/4
\quad (0<\tau\le1/64).
\]

The corresponding reference-measurement probabilities differ by at least \(\tau/16\), because their denominators are at most four. For any fixed \(\beta>0\), take \(\tau=\min\{\beta,1/64\}\). Ordinary Bernoulli estimation identifies the bit using \(O(\tau^{-2})\) snapshots, independent of chain length. Once the bit is known, the two candidate Hamiltonians are known and the return amplitude can be computed. Thus these examples disprove any attempted extension of their exponential lower bound to freely selectable seeds at all sites.

The two requested repositories were consulted as research context. Astra was read at head `d11ea42bb3bfb4122eb298d3276407266afc0960` (12 October 2026); the OpenAI collection explicitly contains results at mixed stages of verification. No unverified repository theorem is imported into the proofs above. The literature checks were selective, not a comprehensive priority clearance.

The broader objective of an independently validated, historically original foundational advance is not certified by this note. The precise remaining issues are historical equivalence to prior inverse-problem/quantum-learning results, independent checking of the general arguments, and escalation beyond this data-access model. No claim is made about generic interacting matter, finite-temperature Gibbs access, supplied microscopic Hamiltonians, fault-tolerant implementation, or fixed-noise large-system experiments.

## 12. Diagnostics and preserved evidence

`check_construction.py` performs exact rational and numerical checks. Run it with Python and dependencies NumPy, SciPy, SymPy, and mpmath. It rewrites `check_results.json` next to the script.

The captured run reports:

- 252 exact rational assertions, checking characteristic polynomials and binomial endpoint moments;
- 49 floating-point checks of spectra, real-time phases, and the exact full-snapshot distance identity;
- 36 high-precision binomial-tail assertions;
- four rational-grid matched-bulk examples, with real-time contrast greater than 1.999998.

The largest recorded spectral discrepancy is approximately \(8.9\times10^{-16}\); the largest recorded real-time phase discrepancy is approximately \(1.1\times10^{-14}\). These are diagnostic observations, not error-certified statements about arbitrary size. The uniform theorem, adaptive-information argument, and interpolation upper bound are mathematical derivations, not conclusions inferred from these finite experiments. There has been no independent review or formal proof compilation.

## References

[1] Scott Lawrence, *Model-free spectral reconstruction via Lagrange duality*, arXiv:2408.11766 (2024). https://arxiv.org/abs/2408.11766

[2] Scott Lawrence, *Real-time dynamics from convex geometry*, arXiv:2502.01880 (2025). https://arxiv.org/html/2502.01880v1

[3] Matthias Christandl, Nilanjana Datta, Artur Ekert, and Andrew J. Landahl, *Perfect state transfer in quantum spin networks*, Physical Review Letters 92, 187902 (2004), arXiv:quant-ph/0309131. https://arxiv.org/abs/quant-ph/0309131

[4] Thais L. Silva, Márcio M. Taddei, Stefano Carrazza, and Leandro Aolita, *Fragmented imaginary-time evolution for early-stage quantum signal processors*, Scientific Reports 13, 18258 (2023). https://www.nature.com/articles/s41598-023-45540-2

[5] Christopher A. Fuchs and Jeroen van de Graaf, *Cryptographic Distinguishability Measures for Quantum Mechanical States*, arXiv:quant-ph/9712042; IEEE Transactions on Information Theory 45, 1216–1227 (1999). https://arxiv.org/abs/quant-ph/9712042

Research context, not proof premises: https://github.com/harjassand/astra-research-knowledge and https://github.com/openai/math
