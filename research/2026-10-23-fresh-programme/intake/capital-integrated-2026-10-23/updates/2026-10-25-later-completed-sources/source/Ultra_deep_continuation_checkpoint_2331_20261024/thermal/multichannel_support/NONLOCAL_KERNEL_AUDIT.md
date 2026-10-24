# Independent audit: positive nonlocal kernel and full channel width

Status: bounded mathematical audit of `thermal/NONLOCAL_KERNEL_CONSTRUCTION.md`. The finite-range harmonic point-mass construction and its all-crossing bound check out. Its escape from the nearest-cell range theorem is specifically unbounded interaction reach and an uncharged intercell extension range.

## 1. Kernel, stiffness and dispersion

For a scalar mass \(M\) per cell and springs
\[
\kappa_n=c_N(N-n),\quad n=1,\ldots,N-1,
\qquad c_N=\frac{12K}{N^2(N^2-1)},
\]
all springs are positive, including the nearest-neighbor spring. The exact sum
\[
\sum_{n=1}^{N-1}n^2(N-n)=\frac{N^2(N^2-1)}{12}
\]
gives \(K_{\rm eff}=\sum n^2\kappa_n=K\). The affine spring sum is
\(K_{\rm aff}=c_NN(N-1)/2=6K/[N(N+1)]\).

The finite geometric-series identity
\[
1+2\sum_{n=1}^{N-1}(1-n/N)\cos(nq)
=\frac1N\left(\frac{\sin(Nq/2)}{\sin(q/2)}\right)^2
\]
implies \(\sum_n(N-n)(1-\cos nq)=[N^2-D_N(q)^2]/2\). Hence
\[
\omega_N(q)^2=\frac{c_N}{M}\big[N^2-D_N(q)^2\big],\qquad
D_N(q)=\frac{\sin(Nq/2)}{\sin(q/2)},
\]
including the continuous value \(D_N(0)=N\). The maximum frequency is exactly
\[
\Omega_N=N\sqrt{c_N/M}=\sqrt{\frac{12K}{M(N^2-1)}}.
\]
Expanding \(D_N(q)\) at zero gives \(\omega_N(q)^2=(K/M)q^2+O(q^4)\), so the low-wave-number stiffness remains \(K\), even as \(\Omega_N\sim\sqrt{12K/M}/N\) tends to zero. For each finite \(N\), the chain is connected because \(\kappa_1>0\).

## 2. Total variation counts every crossing

For an even periodic scalar dispersion, count one right-moving channel per regular frequency crossing. The one-dimensional coarea identity gives
\[
W_N:=\int_0^\infty N_{\rm ch}(\omega)\,d\omega
=\frac12\int_{-\pi}^{\pi}|\omega_N'(q)|\,dq
=\operatorname{TV}_{[0,\pi]}\omega_N.
\]
Thus oscillatory lobes on the near-flat plateau are included; replacing them by a band union would not be justified. Since \(0<g_\theta\le1\), \(J_N\le W_N\).

Set \(u_N=D_N/N\), so \(\omega_N=\Omega_N\sqrt{1-u_N^2}\), and let \(q_0=2\pi/N\). On \((0,q_0)\), with \(x=Nq/2\),
\[
\frac{d}{dq}\log u_N=\frac{N}{2x}\left[x\cot x-\frac{x}{N}\cot(x/N)\right]<0.
\]
Indeed \((x\cot x)'=(\sin x\cos x-x)/\sin^2x<0\) on \((0,\pi)\). This first lobe therefore rises monotonically from zero frequency to \(\Omega_N\), contributing exactly \(\Omega_N\) to total variation.

For \(q\in[q_0,\pi]\), \(N\sin(q/2)\ge N\sin(\pi/N)\ge2\), so \(|u_N(q)|\le1/2\), and
\[
|\omega_N'(q)|\le2\Omega_N|u_Nu_N'|
\le2\Omega_N\left[\frac1{2N\sin^2(q/2)}+
\frac1{2N^2\sin^3(q/2)}\right].
\]
The first tail integral is exactly \(\cot(\pi/N)/N\le1/\pi\). Using \(\sin(q/2)\ge q/\pi\), the second is at most
\[
\frac{\pi^3}{2N^2}\int_{2\pi/N}^{\pi}\frac{dq}{q^3}
=\frac\pi{16}-\frac\pi{4N^2}\le\frac\pi{16}.
\]
For \(N=2\), the tail interval is empty. Therefore
\[
\Omega_N\le W_N\le
\left(1+\frac2\pi+\frac\pi8\right)\Omega_N.
\]
No propagating crossings have been dropped. At any fixed \(\theta>0\), this proves \(J_N(\theta)\to0\) as \(N\to\infty\), while the fixed \((M,K)\) rigid chain has positive conductance. If \(\theta\to0\) with \(N\theta\to\infty\), then \(J_N/J_Q\le3W_N/(\pi^2\theta)\to0\), whereas the rigid-chain ratio tends to one.

## 3. Neighbor-displacement Gibbs cost

For \(Y=x_{\ell+1}-x_\ell\), the single-branch Bloch coefficient is \(|e^{iq}-1|^2=4\sin^2(q/2)\). The per-cell quantum Gibbs variance is
\[
\operatorname{Var}(Y)=\frac1{2\pi}\int_{-\pi}^{\pi}
4\sin^2(q/2)\frac{\hbar}{2M\omega_N(q)}
\coth\!\left(\frac{\hbar\omega_N(q)}{2k_BT}\right)dq.
\]
Since \(\omega_N(q)\le\Omega_N\) and \(\coth x\ge1\), the zero-point floor is
\[
\operatorname{Var}(Y)\ge\frac{\hbar}{2M\Omega_N}
\frac1{2\pi}\int_{-\pi}^{\pi}4\sin^2(q/2)\,dq
=\frac{\hbar}{M\Omega_N}.
\]
Using \(\frac{\hbar}{2\omega}\coth(\hbar\omega/(2k_BT))\ge k_BT/\omega^2\) instead gives the classical floor
\[
\operatorname{Var}(Y)\ge\frac{2k_BT}{M\Omega_N^2}.
\]
Thus the *variance* of a nearest-neighbor extension grows at least linearly in \(N\) from zero-point motion and quadratically in \(N\) at fixed positive classical temperature. The construction has no internal coordinate within a cell, so a range cap limited to intra-cell coordinates is vacuous; it does not keep actual neighbor extension bounded.

## 4. Boundaries and interpretation

This is a valid counterexample to a conductance lower bound based only on fixed \(M\), fixed relaxed long-wave stiffness \(K_{\rm eff}\), and a cap on intra-cell relative coordinates while allowing unrestricted positive interaction range. It does not contradict the nearest-cell rail bounds: \(K_{\rm aff}\to0\) and the interaction reach \((N-1)\) cells diverges. A physical realization must count connector extension, mass distribution and extra connector modes. The note's simple axial connector mass estimate stays finite, so finite connector mass alone is not a proof that the network is impossible; the additional modes and their effect on transport remain to be modeled.

The formulas are for an infinite periodic lattice (or a ring with enough sites that distinct shifts through \(N-1\) cells do not alias). They establish an ideal point-mass harmonic result, not an acquired bounded-extension material or a finite-contact device.
