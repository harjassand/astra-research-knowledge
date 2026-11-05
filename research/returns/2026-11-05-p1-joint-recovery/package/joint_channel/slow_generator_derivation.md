# The physical matched cascade: an exact fourth-order limiting generator

5 November 2026. This is a source-specific construction and asymptotic theorem for a permitted receiver. Collective-rotation twirling and its relational multiplicity algebra are established reference-frame machinery; the ordered-collision generator and the explicit two-qubit example below are deductions for the present emitter. They do not establish the full optimal memory law.

## 1. Physical operation, orientation, and theorem

Keep k receiver qubits M_1,...,M_k in any independently prepared state sigma_M. A fresh carrier first undergoes the prescribed emitter collision with S. The receiver then applies the SAME positive-angle partial SWAP to M_1,E, then M_2,E, through M_k,E, and discards E. Repeat. No bath purifier, source interaction by the receiver, preparation key, or future carrier is used. There are k retained qubits, k+1 receiver qubits while the carrier is present, and exactly k receiver partial-SWAP gates per carrier before final decoding.

Put n=k+1 and number S,M_1,...,M_k as sites 1,...,n. Auxiliary site 0 is the carrier. Define

\[
P_j=\operatorname{SWAP}_{0j},\quad
W_n(\theta)=e^{i\theta P_n}\cdots e^{i\theta P_1},\quad
\mathcal T_{n,\theta}(X)=\tfrac12\operatorname{Tr}_0 W_n(\theta)(I_0\otimes X)W_n(\theta)^\dagger.
\]

This is the **Schrödinger map on the actual source and retained receiver**, with the earliest source collision at the right of W. Its Hilbert-Schmidt adjoint reverses the limiting Hamiltonian sign. The source is included only in the mathematical channel and remains inaccessible to the receiver.

Let

\[
J^a=\sum_j\sigma_j^a,\quad
Y^a=\sum_{i<j}(\sigma_i\times\sigma_j)^a,\quad
C_n=\sum_{i<j<l}\sigma_i\cdot(\sigma_j\times\sigma_l).
\]

Let P_inv be collective SU(2) twirling, with range A_n={X:[J^a,X]=0 for every a}. This is the full multiplicity algebra.

**Theorem (fixed n).** On A_n,

\[
\mathcal T_{n,\theta}=I+\theta^4\mathcal G_n+O_n(|\theta|^5),\qquad
\boxed{\mathcal G_n(X)=-\frac1{32}\sum_a[Y^a,[Y^a,X]]+\frac{i}{8}[C_n,X].}
\tag{1}
\]

With D[L](X)=LXL^dagger-(L^dagger LX+XL^dagger L)/2, equivalently

\[
\mathcal G_n=-i[-C_n/8,\,\cdot\,]+\sum_a\mathcal D[Y^a/4].
\tag{2}
\]

Thus G_n is a CPTP Markov generator and preserves A_n. For each fixed n and t>0,

\[
\boxed{\lim_{\theta\downarrow0}\mathcal T_{n,\theta}^{\lfloor t/\theta^4\rfloor}
=e^{t\mathcal G_n}P_{\rm inv}.}
\tag{3}
\]

Convergence is in diamond norm in this fixed finite dimension, uniform on compact t intervals bounded away from zero. It therefore preserves arbitrary inaccessible reference systems and is uniform over initial states at fixed n, including pure and mixed receiver initializations.

This does **not** exchange n→infinity with theta→0. The remainder and finite-angle threshold depend on n. A high-fidelity family with k=k(epsilon) still needs quantitative bounds and an actual recovery analysis.

## 2. All-n BCH proof and the chiral sign

Use the local analytic logarithm

\[
\log W_n(\theta)=i\sum_{r\ge1}\theta^r H_r,
\]

with Hermitian H_r. Denote normalized carrier trace by E_0. Second-order BCH gives

\[
H_1=\frac n2I+\frac12\sum_a\sigma_0^aJ^a,\qquad
H_2=\frac14\sum_a\sigma_0^aY^a.
\tag{4}
\]

Indeed, [P_j,P_i]=-(i/2) sigma_0·(sigma_i×sigma_j) for i<j, and the second BCH term in log W is -theta^2[P_j,P_i]/2. The sign in (4) is positive for the stated chronological order.

The needed third- and fourth-order carrier traces are

\[
E_0(H_3)=\frac16\sum_{i<j}\sigma_i\cdot\sigma_j
=\frac{J^2-3nI}{12},\qquad
\boxed{E_0(H_4)=C_n/8.}
\tag{5}
\]

Here is an all-n reduction of (5). Strip I/2 from each P_j; this affects only H_1. Every r-th order BCH term is a homogeneous Lie polynomial of degree r in (sigma_0·sigma_j)/2 and has support on at most r bath sites. Time reversal flips every Pauli and complex conjugates i. Since local SWAP generators are time-reversal even, H_r has parity (-1)^(r+1).

For E_0(H_4), scalar terms supported on at most two bath sites are time-reversal even and vanish. A term involving four distinct sites has exactly one Pauli on each and is likewise even, so it vanishes. The only allowed odd scalar on three sites is the scalar chirality. Its coefficient depends only on the relative order of those three collisions: a fourth site cannot contribute to their three-site support. Every ordered triple therefore has the coefficient determined by three sites. At order three the same argument leaves only universal two-site dot products; a three-distinct-site scalar has the wrong parity there.

The remaining finite calculation is an exact algebraic identity. For three sites put A=P_1, B=P_2, D=P_3 and

\[
S_p=\sum_{r+s+u=p}\frac{(iD)^u(iB)^s(iA)^r}{u!s!r!}.
\]

The fourth coefficient of log W_3 is

\[
L_4=S_4-\tfrac12(S_1S_3+S_2^2+S_3S_1)
+\tfrac13(S_1^2S_2+S_1S_2S_1+S_2S_1^2)-\tfrac14S_1^4.
\]

SWAP multiplication, using sigma^a sigma^b=delta_ab I+i epsilon_abc sigma^c and chi_123=2i[P_12,P_23], gives E_0(L_4)/i=chi_123/8. The script `check_bch_exact.py` evaluates this over exact rational complex matrices and asserts equality, rather than floating-point closeness. It also certifies E_0(H_3)=sum pair dots/6. The support/parity argument then proves (5) at all n.

Now let X lie in A_n. The inner commutator [H_1,I_0⊗X] is zero. Moreover, if Z is invariant under simultaneous rotations of carrier and bath, decompose Z=I_0⊗Z_0+sum_a sigma_0^a⊗Z_a. The Z_a transform as a vector, so

\[
E_0[H_1,Z]=\tfrac12\sum_a[J^a,Z_a]=0.
\tag{6}
\]

Thus any outer ad(H_1) vanishes after carrier trace, while any inner ad(H_1) acting directly on X is zero. All relevant nested commutators preserve simultaneous invariance. At orders one and two there is no surviving term. At order three, [E_0(H_3),X]=0 because E_0(H_3) is a function of J^2. At order four the only surviving terms are

\[
i[E_0(H_4),X]-\tfrac12 E_0[H_2,[H_2,I_0\otimes X]].
\]

Using E_0(sigma_0^a sigma_0^b)=delta_ab and (4)-(5) gives exactly (1). This also proves the +i[C_n,X]/8 sign for the stated Schrödinger orientation. The usual Hamiltonian in -i[H,X] notation is therefore -C_n/8.

## 3. Why the repeated-channel limit is rigorous at fixed width

The channel is exactly SU(2)-equivariant, so P_inv commutes with T and its adjoint. The scalar sector and its orthogonal complement do not mix, even before taking the limit. On an operator-spin-l sector, l>=1, the second-order expansion is

\[
\mathcal T_{n,\theta}=I-\frac{\theta^2}{8}\sum_a\operatorname{ad}(J^a)^2+O_n(|\theta|^3)
=I-\frac{l(l+1)}2\theta^2+O_n(|\theta|^3).
\]

Consequently the norm on the nonscalar subspace is at most 1-c_n theta^2 for small enough theta, with c_n>0. After floor(t/theta^4) steps it is bounded by an exponential of order exp(-c_n t/theta^2), and disappears. On A_n, (1) and the finite-dimensional exponential-product formula give exp(tG_n). The scalar approximation error is O_n(t theta) on bounded t intervals. Finite-dimensional norm equivalence upgrades the convergence to diamond norm, proving (3).

This is a two-scale result: an initial collective twirl on the theta^-2 scale, followed by genuine scalar/multiplicity dynamics on the theta^-4 scale. It is not a claim that an individual receiver can apply the twirl jointly to the inaccessible source. The twirl emerges from the specified physical repeated collisions.

## 4. An explicit physical two-qubit counterexample to vanishing information

Take k=2 and initialize M_1,M_2 in |0>⊗|+>. Number S,M_1,M_2 as 0,1,2 in this section only. Put C_ij=sigma_i·sigma_j and chi=sigma_0·(sigma_1×sigma_2). The invariant algebra has basis I,C_01,C_02,C_12,chi, and the exact limiting generator is

\[
\begin{aligned}
G(I)&=0,\\
G(C_{01})&=-C_{01}-C_{02}+C_{12},\\
G(C_{02})&=-3C_{02}-C_{12},\\
G(C_{12})&=-C_{12},\\
G(\chi)&=-\chi.
\end{aligned}
\tag{7}
\]

The initial collective twirl sends the source Pauli images to

\[
P_{\rm inv}(\sigma_z/2\otimes|0+\rangle\langle0+|)=C_{01}/24,\quad
P_{\rm inv}(\sigma_x/2\otimes|0+\rangle\langle0+|)=C_{02}/24,\quad
P_{\rm inv}(\sigma_y/2\otimes|0+\rangle\langle0+|)=\chi/48.
\]

The average is I_8/8. Solving (7) and discarding the actual source gives the limiting accessible channel, for rho=(I+r·sigma)/2,

\[
\boxed{\mathcal E_t(\rho)=\frac{I_4}{4}
+\frac{C_{12}}{12}\{u_x(t)r_x+u_z(t)r_z\},}
\tag{8}
\]

where

\[
u_x(t)=-\frac{e^{-t}-e^{-3t}}2,\qquad
u_z(t)=e^{-t}\left(\frac{3t}{2}-\frac14+\frac{e^{-2t}}4\right).
\tag{9}
\]

Thus the ledger's accessible Petz visibility has the strictly positive limit

\[
\boxed{a(t)=\frac{u_x(t)^2+u_z(t)^2}{9}>0\qquad(t>0).}
\tag{10}
\]

For example a(1)=0.02759547397585118. This refutes a universal bound a_N<=C(m)theta^2 with C(m) finite and uniform in N, even with just two retained receiver qubits (m=4). Exact finite-channel powers at t=Ntheta^4=1 give 0.02884679, 0.02792807, 0.02767991 for theta=0.2,0.1,0.05, consistent with the proved limit.

There is an even simpler analytic distinguishability witness. Let P_-=(I-C_12)/4 be the receiver singlet projector. From (7),

\[
G^*(I_S\otimes P_-)=(-C_{01}+C_{02}+C_{12})/4.
\]

For the specified frame, p_-'(0)=(r_x-r_z)/4. The two source z eigenstates therefore have different receiver singlet probabilities for all sufficiently small positive slow time. This conclusion needs no numerical extrapolation.

**The information in this example is classical.** Both receiver total-spin irreps have multiplicity one, and (8) lies in the abelian algebra generated by P_-. It is entanglement breaking. Its optimum final entanglement fidelity is

\[
F_{\rm opt}(t)=\frac14+\frac{\sqrt{u_x(t)^2+u_z(t)^2}}8.
\tag{11}
\]

At t=1 this is 0.3122945706129682, far below the 1/2 entanglement-transmission threshold. A finite global Clifford twirl of the complete physical receiver/readout converts this value into a depolarizing logical channel of half-diamond error 1-F_opt. Neither the positive visibility nor the slow lifetime establishes accurate quantum recovery.

## 5. Numerical implementation and established limits

`cascade_effective.py` implements (1) on the complete Schur multiplicity algebra, including coherences within and between the relevant coupling paths. It does not replace the logical input with a classical vector. It propagates all four source Pauli images, then traces the actual source. The final receiver channel is invariant under collective physical rotations; consequently the magnetic irrep register is an input-independent maximally mixed factor *within each block* and can be discarded at final readout, while every multiplicity block is retained. The readout is optimized by a conditional-min-entropy SDP on each multiplicity block.

For the product frame cycling |0>,|+>,|+i>, completed t=1 weak-limit results are:

| retained k | a | optimum final Bell fidelity |
|---:|---:|---:|
| 2 | 0.02759547 | 0.31229457 |
| 3 | 0.04358191 | 0.35587033 |
| 4 | 0.05764122 | 0.36979913 |
| 5 | 0.07542893 | 0.39052077 |
| 6 | 0.09002023 | 0.40871910 |
| 7 | 0.10364030 | 0.42159722 |
| 8 | 0.11646837 | 0.43444168 |

These are achieved channel parameters and numerical final-decoder optima for one specified frame and one specified passive cascade. They are not optimal over frames, controls, instruments, or memory. The k=9 product scan exhausted the available dense SDP memory and produced no completed value. The root's separate arbitrary-frame optimizations supersede this product-frame table for best feasible performance; they are not asserted to find global optima either.

What remains unproved is whether any initial frame and admissible controls make the recovered error tend to zero as k grows, let alone a bound uniform jointly in k,theta,t and the target error. No all-k no-go follows from the completed scans. The present theorem gives a concrete finite physical receiver and an exact reduced limiting control problem; it does not solve the original optimal memory/processing endpoint.

## 6. Reproduction and attribution

- `check_bch_exact.py`: exact rational certificates for the three- and four-order carrier traces.
- `cascade_scalar_limit.py`: direct ordered-collision expansion and the complete n=3 generator.
- `cascade_hamiltonian.py`: independent finite-matrix checks of the chiral term for n=2,...,5.
- `pure_frame_cascade.py`: exact finite-angle repeated channel and unrestricted final-decoder SDP.
- `cascade_effective.py`: full fixed-width slow generator and Schur-multiplicity final readout.
- `effective_product_results.jsonl`: completed larger product-frame runs; the unfinished k=9 header is not a result.

The generic relational/noiseless-subsystem interpretation is existing machinery, for example S. D. Bartlett, T. Rudolph, R. W. Spekkens, *Classical and quantum communication without a shared reference frame*, Phys. Rev. Lett. 91, 027901 (2003), https://arxiv.org/abs/quant-ph/0302111 . The final-decoder SDP uses R. Koenig, R. Renner, C. Schaffner, *The operational meaning of min- and max-entropy*, IEEE Trans. Inf. Theory 55 (2009), https://doi.org/10.1109/TIT.2009.2025545 . The specific ordered Yangian/chirality generator, physical initialization, and counterexample above are source-specific deductions, not claims made by those references.
