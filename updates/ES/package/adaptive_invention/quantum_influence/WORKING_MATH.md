# Quantum influence: boundary cancellation that preserves future returns

Date: 2026-10-13. Independent cell; no old campaign mathematics or sibling files used. Nothing is committed or published.

The unrestricted polynomial-cost target is not achieved. Its worst-case form would imply BQP = BPP. Two explicit operations survive as mathematical primitives: a product-boundary moment quotient with a certified or unbiased remainder, and a conservative register for return phases. The second operation is substantially established projection/Krylov machinery; the first is a candidate way to use finite response certificates in signed-history compression. No novelty or interacting-system speedup is established for either combination.

The most useful negative finding is that compactness of a scalar observable signal is a weak criterion: a polynomial-size conservative phase approximation exists for every bounded local-Hamiltonian signal on a polynomial time interval. Acquiring it can still be BQP-hard.

## 1. Exact target and complexity gate

Let a bounded-degree geometrically local lattice have N sites of constant local dimension q, and let

\[
H=\sum_a h_a,\qquad |\operatorname{supp} h_a|\le k_0,
\qquad \|h_a\|\le J.
\]

Each site is in at most \(\nu\) terms. The input specifies every local term and a product initial density operator \(\rho=\bigotimes_i\rho_i\). The query is

\[
f_A(t)=\operatorname{Tr}\rho\,e^{itH}Ae^{-itH},
\qquad \|A\|\le1,
\]

to additive error epsilon, with local A and possibly \(t=\operatorname{poly}(N)\).

A uniform randomized classical algorithm polynomial in N, t and 1/epsilon would simulate local output measurements of autonomous one-dimensional Hamiltonian quantum computers. These have explicit nearest-neighbor Hamiltonians, constant-dimensional sites, product computational-basis initial states, polynomial evolution times, and local readout. Thus the algorithm would imply BQP is contained in BPP, and hence BQP = BPP. This is a conditional complexity obstruction, not an unconditional lower bound. It already applies to much less general data than the target allows. See the primary constructions and the short-time algorithm in [BASELINES.md](BASELINES.md).

## 2. Operation A: replace a history pack by its boundary response jet and a remainder

Set \(\mathcal G X=i[H,X]\), and define the continuation functional

\[
F_\tau(X)=\operatorname{Tr}\rho\,e^{\tau\mathcal G}X,
\qquad
j_r(X)=\operatorname{Tr}\rho\,\mathcal G^rX.
\]

For a signed or complex history pack \(R=\sum_{a=1}^K c_aP_a\), where the \(P_a\) are Pauli strings, compute the finite response column

\[
J_m(P_a)=(j_0(P_a),\ldots,j_{m-1}(P_a))^\top.
\]

Different Pauli strings can have the same response column. This differs from combining identical Pauli endpoints: it cancels words according to their future scalar response to this particular product boundary. Use linear relations between columns to choose representatives; the discarded combination R must satisfy

\[
J_m(R)=0. \tag{A1}
\]

The operation has two permitted outputs: a deterministic remainder interval proved below, or a local unbiased tail sampler proved below. Treating a finite jet collision as exact for arbitrary future time is forbidden by the counterexamples in Sections 4 and 5.

### 2.1 Local certificate; no full evolution oracle

Suppose X has support on at most s sites. After r nested commutators, a contributing word has support on at most \(s+r(k_0-1)\) sites. At step l it intersects at most \(\nu[s+l(k_0-1)]\) Hamiltonian terms. Consequently

\[
\|\mathcal G^rX\|
\le \|X\|(2J\nu)^r\prod_{l=0}^{r-1}[s+l(k_0-1)]. \tag{A2}
\]

For \(k_0\ge2\), put

\[
g=2J\nu(k_0-1),\qquad \alpha=s/(k_0-1),
\]

so (A2) is \(\|X\|g^r(\alpha)_r\). A Hamiltonian of only one-site terms also obeys the bound after harmlessly setting \(k_0=2\).

If every Pauli endpoint has support at most s, let \(\Gamma=\sum_a|c_a|\). From (A1), for \(x=g|\tau|<1\),

\[
|F_\tau(R)|
\le W_m(\tau):=
\Gamma\sum_{r=m}^\infty \frac{(\alpha)_r}{r!}x^r. \tag{A3}
\]

In particular \(W_0=\Gamma(1-x)^{-\alpha}\). Individual support sizes can be retained instead of using their maximum. If the actual norm and support of R can be certified more cheaply than its Pauli variation, (A2) can be applied directly to R. Computing that norm is a charged step, not a free improvement.

Proof of (A3): expand \(F_\tau(R)\) in its convergent finite-dimensional Taylor series. The first m scalar coefficients vanish by (A1). Bound each remaining nested commutator of each endpoint using (A2), then sum the positive majorant. The geometric-radius condition applies to this majorant, not to the entire finite-system signal, which is entire.

All jet entries can be acquired from the explicit local Hamiltonian by nested local Pauli commutators. Product-state boundary evaluation is

\[
\operatorname{Tr}\rho P=\prod_i\operatorname{Tr}\rho_iP_i.
\]

For constant initial support and bounded-degree interactions, the set of rooted connected supports of r commutators, and their Pauli labels, has size at most exponential in r. Exact coefficient bit lengths also increase and must be charged. No scalar jet is supplied as an oracle. The runnable tilted-Ising example records acquisition growth rather than claiming an asymptotic lower bound from finite counts.

### 2.2 Unbiased replacement by a tail-path sample

For an explicit Pauli Hamiltonian \(H=\sum_b h_bP_b\), with \(|h_b|\le J\), a nonzero application of \(\mathcal G\) maps a Pauli string to another Pauli string with a real multiplier \(\sigma_l2h_b\), \(\sigma_l\in\{-1,1\}\). Commuting choices contribute zero.

Let

\[
a_r=\frac{(\alpha)_r}{r!}x^r,
\qquad A_m=\sum_{r\ge m}a_r,
\qquad p_r=a_r/A_m,
\qquad q_a=|c_a|/\Gamma.
\]

Draw endpoint a with probability \(q_a\), draw order \(r\ge m\) with probability \(p_r\), and draw a nested commutator path by uniformly choosing a Hamiltonian term intersecting the current support at each step. If a chosen term commutes, output zero. If no term intersects, output zero. Let \(p(\omega\mid a,r)\) be the product of these explicitly known conditional probabilities. Output

\[
Z=\frac{c_a}{q_a}\frac{\tau^r}{r!p_r}
\frac{\prod_{l=1}^r(\sigma_l2h_{b_l})}{p(\omega\mid a,r)}
\operatorname{Tr}\rho P_\omega. \tag{A4}
\]

The signed path sum is the exact Taylor coefficient, hence

\[
\mathbb EZ=F_\tau(R),\qquad |Z|\le\Gamma A_m=W_m,
\qquad \mathbb E|Z-\mathbb EZ|^2\le W_m^2. \tag{A5}
\]

The envelope inequality follows from the same per-step support count as (A2). Thus O(\(W_m^2\epsilon^{-2}\log(1/\delta)\)) independent samples suffice for additive error epsilon with failure probability delta, up to fixed constants for real or complex outputs. The order distribution is an explicitly computable negative-binomial tail, not a quantum oracle. Its unbounded support must be sampled correctly; an implementation with an order cutoff must report its tail bias.

`derive_and_test.py` checks (A4) for \(R=Z_0-Z_1\), \(H=X_0/2\), \(\rho=|00\rangle\langle00|\), m=2 and tau=0.2. It records sampling error and the finite-order bias bound. This is a finite mechanism test, not a long-time speedup experiment.

### 2.3 The all-future quotient and why finite jets do not certify it

The exact null space is

\[
\mathcal N_\rho=\{X:F_\tau(X)=0\text{ for every real }\tau\}
=\bigcap_{r=0}^{D^2-1}\ker j_r, \qquad D=q^N. \tag{A6}
\]

The first equality with finitely many derivatives follows from Cayley–Hamilton for the D-squared dimensional Liouvillian. This null space is \(\mathcal G\)-invariant. Quotienting by it is exact, but constructing it generically requires exponentially many constraints. This is an observability quotient in linear-system language; that general concept is not claimed as new.

A useful exact certificate is any explicitly generated invariant subspace on which all the j_r vanish; a finite jet list without invariant closure is weaker. For example, exchange symmetry of H and rho can make \(Z_i-Z_j\) belong to \(\mathcal N_\rho\), although it is a nonzero operator. A small symmetry-breaking defect can accumulate for a long time, so approximate equality still needs a horizon and error budget.

The missing long-time theorem is quantitative and operational: from H and the product boundary alone, construct history packs for all required time slices whose support cost, variation Gamma, certificate cost and total remainder variance stay polynomial. Neither the rank-m jet matrix nor the existence of the null space proves this. Intermediate history supports and Gamma can grow with time. Repeated short-time bounds do not provide the missing cancellation for free.

## 3. Operation B: eliminate excursions but retain their phases

This is a reconstruction of established projection/continued-fraction/Krylov machinery, retained as the strongest safe alternative to deleting apparently forgotten history. Its use here is to expose both a useful representation and its acquisition barrier.

Use the unnormalized Hilbert–Schmidt inner product \((X|Y)=\operatorname{Tr}X^\dagger Y\). The Liouvillian \(\mathcal L=[H,\cdot]\) is self-adjoint, and \(\rho(t)=e^{-it\mathcal L}\rho\). Choose an orthogonal projection P whose range contains both rho and A; rank r at most two suffices. Let Q=I-P and write

\[
\mathcal L=\begin{pmatrix}B&C^\dagger\\C&D_Q\end{pmatrix},
\quad B=P\mathcal LP,\ C=Q\mathcal LP,\ D_Q=Q\mathcal LQ.
\]

Let \(x=P\rho(t)\), \(y=Q\rho(t)\). Since y(0)=0,

\[
\dot x(t)=-iBx(t)-\int_0^tK(s)x(t-s)ds,
\quad K(s)=C^\dagger e^{-isD_Q}C,
\quad f_A(t)=(A|x(t)). \tag{B1}
\]

This sums every excursion out of P and back, retaining interference among its histories. It does not assume excursions decay.

### 3.1 Positive matrix-valued spectral measure

Because \(D_Q\) is Hermitian,

\[
K(s)=\int e^{-i\omega s}\,dM(\omega),
\qquad M(S)=C^\dagger E_{D_Q}(S)C\succeq0. \tag{B2}
\]

Replace the measure by finite positive atoms, \(K_m(s)=\sum_jW_je^{-i\omega_js}\), \(W_j\succeq0\). Factoring \(W_j=G_j^\dagger G_j\), introduce auxiliary phase registers

\[
\dot x=-iBx-i\sum_jG_j^\dagger z_j,
\qquad \dot z_j=-i\omega_jz_j-iG_jx,
\qquad z_j(0)=0. \tag{B3}
\]

The lifted generator is Hermitian. It preserves total norm and delayed returns; no damping is introduced merely because a signal is small. Register dimension is a phase description, not spatial state entanglement or an assumed tensor-network rank.

An orthogonal P is essential for this positive-measure derivation. The frequently used product-reset projection \(P\sigma=\operatorname{Tr}_E\sigma\otimes\rho_E\) is generally oblique in the Hilbert–Schmidt metric. It cannot simply be substituted into (B2). Conversely, an orthogonal projection onto only local observables, omitting the initial state, has a nonzero initial Q component and an additional inhomogeneous term. The two-seed choice above avoids silently discarding that term.

### 3.2 Explicit acquisition, moment matching and error

Let V have orthonormal columns spanning

\[
\operatorname{span}\{C,D_QC,\ldots,D_Q^{m-1}C\}.
\]

Set \(D_m=V^\dagger D_QV\), \(C_m=V^\dagger C\), and \(K_m(s)=C_m^\dagger e^{-isD_m}C_m\). The register has dimension at most mr, and

\[
C^\dagger D_Q^lC=C_m^\dagger D_m^lC_m,
\qquad 0\le l\le2m-1. \tag{B4}
\]

For l at most 2m-2, split l into two exponents at most m-1 and use the Krylov span on both sides. For l=2m-1, the remaining single D_Q application is sandwiched between vectors already in that span, so its projection does not change the scalar block moment.

If \(\|D_Q\|\le\Lambda\), Taylor approximation on the real interval [-Lambda,Lambda], (B4), and the positive spectral norm bound give

\[
\|K(s)-K_m(s)\|
\le2\|C\|^2\frac{(\Lambda|s|)^{2m}}{(2m)!}. \tag{B5}
\]

There is no exponential \(e^{\Lambda |s|}\) factor here: the real-line integral remainder of \(e^{-i\omega s}\) has derivatives of magnitude \(|s|^{2m}\). Polynomial moment matching is used before bounding the two remaining functional-calculus errors.

The exact reduced propagator \(G(t)=Pe^{-it\mathcal L}P\) has norm at most one. Both the exact and approximating lifts are conservative. The Volterra resolvent identity therefore gives

\[
\|x(t)-x_m(t)\|
\le\|x(0)\|\int_0^t(t-s)\|K(s)-K_m(s)\|ds. \tag{B6}
\]

For a uniform kernel error delta on [0,T], physical readout error is at most

\[
|f_A(t)-f_{A,m}(t)|
\le\kappa\,T^2\delta/2,
\qquad \kappa=\|A\|_{\rm HS}\|\rho\|_{\rm HS}. \tag{B7}
\]

This explicit conditioning factor matters: for a local norm-one operator and a pure product input it can be order \(q^{N/2}\). It cannot be omitted by normalizing vectorized operators. Its logarithm is only O(N), which is enough for the representation-existence result below but not for free coefficient acquisition.

Since \(\Lambda\le2\|H\|=O(N)\), \(\|C\|\le\Lambda\), and \(\kappa\le q^{N/2}\), (B5)-(B7) show that

\[
m=O(NT+N+\log(T+1)+\log(1/\epsilon)) \tag{B8}
\]

suffices for a polynomial-size phase approximation on [0,T]. This is not a polynomial classical algorithm: every acquired Krylov vector can have \(q^{2N}\) coordinates, and constructing its coefficients/readout may be the original hard computation. Product input and local H make the first few entries easy but do not make the full m-step acquisition polynomial. The same distinction defeats a proposed universal scalar interpolation algorithm.

## 4. Decisive retained obstruction: a quiet local signal with an order-one return

On an N-site chain, take

\[
H=\sum_{j=1}^{N-1}b_j(\sigma_j^+\sigma_{j+1}^-+
\sigma_j^-\sigma_{j+1}^+),
\qquad b_j=\frac{2\sqrt{j(N-j)}}{N}\le1. \tag{E1}
\]

This is time-independent, nearest-neighbor, and each bond term has norm at most one. Its one-excitation restriction is \(h=(4/N)J_x\), for spin \(J=(N-1)/2\). For product input \(|10\cdots0\rangle\) and the local occupation query n_1,

\[
f_{n_1}(t)=\left|\cos\frac{2t}{N}\right|^{2(N-1)}. \tag{E2}
\]

Put \(T=\pi N/2\). Then

\[
f_{n_1}(T)=1,
\qquad \sup_{t\in[T/4,3T/4]}f_{n_1}(t)\le2^{-(N-1)}. \tag{E3}
\]

For N=64, the quiet-window bound is \(1.0842021724855044\times10^{-19}\), while the final revival is one. A finite small local signal, a long quiet interval, or apparent local equilibration does not certify loss of future influence. This counterexample is exactly solvable and need not itself be computationally hard; it disproves the proposed deletion inference within the requested autonomous local-Hamiltonian interface.

The same H also supplies a matched entanglement test. Start from the alternating product occupation pattern \(\nu_j\in\{0,1\}\). With \(U(t)=e^{-ith}\), the covariance evolves as

\[
C(t)=U(t)\operatorname{diag}(\nu_j)U(t)^\dagger,
\qquad \langle n_1(t)\rangle=
\tfrac12\left[1+\cos\left(\frac{4t}{N}\right)^{N-1}\right]. \tag{E4}
\]

For even N at T/4, the restriction of C to the left half is \(I/2\). One way to see this is to write \(\operatorname{diag}(\nu_j)=(I+D)/2\), where the alternating diagonal sign D anticommutes with h. Thus \(U D U^\dagger=e^{-2ith}D\). At T/4, \(e^{-2ith}\) is a pi rotation of the spin and maps each site to its mirror in the opposite half. Its same-half block vanishes. The pure Slater state's bipartite entropy is therefore exactly N/2 bits. At N=64 the test obtains 32 bits.

Despite this maximal volume law, all local occupations are acquired from the explicit quadratic Hamiltonian in polynomial time by covariance evolution. This is the established free-fermion baseline, not an interacting-system discovery. It demonstrates the required distinction: full entanglement growth can be bypassed when an efficiently acquired observable algebra closes. The missing target is generic interacting closure or cancellation, not another demonstration that entanglement alone is insufficient.

## 5. Finite-moment indistinguishability

For an endpoint of a tridiagonal chain with nonzero hoppings \(b_1,b_2,\ldots\), compare the full chain with its truncation to the first m sites. An endpoint-return path must cross the deleted edge and return before it sees the difference. Hence

\[
\langle1|h^r|1\rangle=
\langle1|h_m^r|1\rangle\quad(0\le r\le2m-1),
\]

and the first difference is

\[
\langle1|h^{2m}|1\rangle-
\langle1|h_m^{2m}|1\rangle
=\prod_{j=1}^m b_j^2. \tag{E5}
\]

Thus finite jet or return-moment data do not determine arbitrary later response. In the runnable unit-hopping example m=7, all 14 moments r=0,...,13 agree exactly, the order-14 difference is one, and a sampled time interval [0,28] contains a return-amplitude discrepancy greater than 1.51. The mathematical indistinguishability statement (E5) is exact; the quoted maximum is only a sampled finite numerical result.

An even smaller test exposes false cross-string cancellation. With \(H=X_0/2\), \(\rho=|00\rangle\langle00|\), and \(R=Z_0-Z_1\),

\[
j_0(R)=j_1(R)=0,
\qquad F_t(R)=\cos t-1,
\qquad F_\pi(R)=-2. \tag{E6}
\]

The finite jet quotient is useful only with its explicit remainder or a true invariant-null certificate.

## 6. Surviving exploratory gate

The distinct candidate is operation A with certificate-guided signed tail sampling: choose cancellation packs using product-boundary response jets; replace only the certified remainder; retain oscillatory return registers rather than asserting memory loss. It changes the equivalence relation among histories, rather than postulating a small tensor-network rank.

The next mathematical gate is to prove a bound, for an explicitly stated interacting lattice class, on the total acquired certificate cost and squared tail envelopes across the entire computation:

\[
\sum_{\text{packs }p} C_{\rm acquire}(p)
+\epsilon^{-2}\left(\sum_p W_{m_p}(\tau_p)\right)^2
\le\operatorname{poly}(N,T,1/\epsilon). \tag{G1}
\]

The displayed variance allocation assumes independently sampled pack corrections; the sum-of-envelopes bound is conservative. It can be improved only by a proved covariance/cancellation argument with computable sampling probabilities. A supplied list of small W values, quantum-measured moments, a thermalization oracle, or a low-rank influence tensor would change the interface and does not close this gate.

Ergodic diffusive transport is a possible physical test class, but the existing operator-backflow work already studies exponentially small high-weight corrections and gives a quasipolynomial-memory conjecture. A new theorem must improve that acquisition-inclusive benchmark, preserve conserved slow modes and echoes, and state its randomness and Hamiltonian promises. No such theorem is asserted here.

## 7. Reproduction and scope

Run `python3 derive_and_test.py` in this directory. It uses only NumPy and writes `RESULTS.json`. The retained checks cover exact integer Pauli jets, a bias-accounted signed tail sampler, autonomous recurrence, maximal half-chain entanglement in a known solvable model, exact endpoint-moment indistinguishability, and finite positive-residue phase-register moment matching. Mathematical proofs above carry the general identities; finite tests do not certify a frontier speedup.

Status: `UNRESTRICTED_POLYNOMIAL_TARGET_NOT_ACHIEVED`; `BOUNDARY_JET_PRIMITIVE_DERIVED`; `UNBIASED_TAIL_SAMPLER_DERIVED`; `RETURN_PHASE_OPERATION_RECONSTRUCTED`; `NOVELTY_UNESTABLISHED`; `INTERACTING_ACQUISITION_GATE_OPEN`.
