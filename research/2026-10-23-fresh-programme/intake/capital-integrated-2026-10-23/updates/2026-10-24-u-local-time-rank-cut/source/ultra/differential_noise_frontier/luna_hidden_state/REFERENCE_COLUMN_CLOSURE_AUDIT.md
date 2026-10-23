# Passive reference-column closure and risk bound audit

## First challenge frozen

24 October 2026. I read only `work/next_unit/differential_noise_frontier/PASSIVE_REFERENCE_DISSIPATION_OPENING.txt` before freezing this challenge. My first candidate gap was the mixed-state/ancilla factor in (B): the sensing-reference column is not a normalized conditional state, so the claimed comparison of its excited norm with physical excited population needs a positivity argument with the exact reference weight. I also checked whether projecting the column off the reference commutes with its evolution and whether the final coefficient in (C) survives both Cauchy--Schwarz steps. The closure, (B), and (C) all check under the stated inactive-reference contract.

## Exact column equation

Let \(|r\rangle=|b,0_A\rangle\), \(R=|r\rangle\langle r|\), and \(Q=I-R\). The full Lindblad equation is
\[
\dot\rho=-i[H_g(t),\rho]
+\kappa\left(Z\rho Z-\tfrac12\{Z^2,\rho\}\right)
+\gamma\left(J\rho J^\dagger-\tfrac12\{P_e,\rho\}\right),
\qquad J=|\mathrm{dead}\rangle\langle e|,
\]
where ancilla identities are implicit, \(Z|r\rangle=-|r\rangle\), \(P_e|r\rangle=0\), \(H_g(t)|r\rangle=0\), and there are no controls coupling into or out of \(|r\rangle\). The last condition and Hermiticity imply \([Q,H_g(t)]=0\). The differential-noise and loss terms also preserve the reference block, so \(Q\) commutes with the column evolution.

For \(u=2\rho|r\rangle\), the Hamiltonian term is \(-iH_g u\). The dephasing term obeys
\[
Z\rho Z|r\rangle=-Z\rho|r\rangle,
\qquad
\rho Z^2|r\rangle=\rho|r\rangle,
\]
and hence equals \(-\tfrac\kappa2(Z+I)^2u\). The loss jump term is zero on this column because \(J^\dagger|r\rangle=0\); the anticommutator contributes \(-\tfrac\gamma2P_eu\). Consequently, for the projected sensing-reference coherence column \(v=Qu=2Q\rho|r\rangle\),
\[
\dot v=(-iH_g(t)-D)v,
\qquad D=\tfrac\kappa2(Z+I)^2+\tfrac\gamma2P_e.
\]
The initial state \((|r\rangle+|\psi_b\rangle)/\sqrt2\), with unit \(|\psi_b\rangle\perp|r\rangle\), gives \(v(0)=|\psi_b\rangle\), so \(\|v(0)\|=1\). The reference population stays exactly \(\rho_{rr}=1/2\): it is uncoupled, has fixed charge, and is annihilated by the loss projector.

This is a column of the bath-traced physical density operator, not a selected no-loss trajectory. It applies to any finite number of independent noiseless ancillary/storage modes because \(Z\), \(P_e\), and \(V\) carry identity on those labels. The sensing Hamiltonian may be any common parameter-independent Hermitian control satisfying the inactive-reference condition; its strength/bandwidth is not used in the column norm estimates.

## Dissipation ledger and actual-risk charge

The operator \(D\) is positive and diagonal in the sample-charge sectors. On \(a\), it has eigenvalue \(2\kappa\); on \(e\), it has eigenvalue \((\kappa+\gamma)/2\); on \(b\) it vanishes. On sample-vacuum storage or dead sectors it is nonnegative. Thus, as a quadratic-form inequality on the full accessible Hilbert space,
\[
D\succeq 2\kappa P_a+\frac{\kappa+\gamma}{2}P_e.
\]
Since \(H_g(t)\) is Hermitian,
\[
\frac d{dt}\|v\|^2=-2\langle v,Dv\rangle.
\]
Integrating and using \(\|v(0)\|^2=1\) gives
\[
\int_0^T\|P_av(t)\|^2dt\le\frac1{4\kappa}.
\]

For the risk relation, positivity gives for every projector \(S\) orthogonal to \(|r\rangle\)
\[
\|S\rho|r\rangle\|^2\le \rho_{rr}\,\operatorname{Tr}(S\rho).
\]
For example, writing \(\rho=\sum_j\lambda_j|\psi_j\rangle\langle\psi_j|\), apply vector Cauchy--Schwarz to \(S\rho|r\rangle=\sum_j\lambda_j\langle\psi_j|r\rangle S|\psi_j\rangle\); the two squared factors are \(\rho_{rr}\) and \(\operatorname{Tr}(S\rho)\). Taking \(S=P_e\), using \(v=2Q\rho|r\rangle\) and \(\rho_{rr}=1/2\), yields the exact factor
\[
\|P_ev(t)\|^2=4\|P_e\rho(t)|r\rangle\|^2
\le2\operatorname{Tr}(P_e\rho(t)).
\]
The terminal jump has compensator \(\dot r_g(t)=\gamma\operatorname{Tr}(P_e\rho_g(t))\), with \(r_g(0)=0\), because the dead state is absorbing and there are no other loss channels. Therefore
\[
\int_0^T\|P_ev_g(t)\|^2dt\le\frac{2r_g(T)}\gamma.
\]
This is an actual terminal-death probability bound, not an inferred conditional survival rate.

## Two-parameter difference and coefficient in (C)

For a common control waveform, let \(v_i=v_{g_i}\), \(w=v_0-v_1\), and \(\Delta g=g_0-g_1\). The exact column equations imply
\[
\dot w=(-iH_{g_0}-D)w-i\Delta g\,Vv_1.
\]
Taking the norm derivative and dropping the nonpositive \(-2\langle w,Dw\rangle\) term,
\[
\frac d{dt}\|w\|^2
\le 2|\Delta g|\,\left|\operatorname{Im}\langle w,Vv_1\rangle\right|
=2|\Delta g|\,\left|\operatorname{Im}\langle v_0,Vv_1\rangle\right|,
\]
because \(\langle v_1,Vv_1\rangle\) is real for Hermitian \(V\). The sign may be written \(\pm\) before taking absolute values. Since \(V=|e\rangle\langle a|+|a\rangle\langle e|\),
\[
|\langle v_0,Vv_1\rangle|
\le \|P_ev_0\|\|P_av_1\|+\|P_av_0\|\|P_ev_1\|.
\]
The two time integrals are bounded separately by
\[
\int_0^T\|P_ev_0\|\|P_av_1\|dt
\le\sqrt{\frac{2r_{g_0}}\gamma\frac1{4\kappa}}
=\sqrt{\frac{r_{g_0}}{2\kappa\gamma}},
\]
and similarly with \(g_0,g_1\) exchanged. The common initial sensing branch gives \(w(0)=0\). Integrating the norm derivative therefore gives exactly
\[
\boxed{
\|v_{g_0}(T)-v_{g_1}(T)\|^2
\le |g_0-g_1|\sqrt{\frac{2}{\kappa\gamma}}
\left(\sqrt{r_{g_0}(T)}+\sqrt{r_{g_1}(T)}\right).
}
\]
No factor 2 is missing: the derivative contributes 2, each Cauchy--Schwarz term contributes \(1/\sqrt{2\kappa\gamma}\), and together these yield \(\sqrt{2/(\kappa\gamma)}\). If both risks are at most \(\rho\), this becomes \(\|v_0-v_1\|^2\le2|\Delta g|\sqrt{2\rho/(\kappa\gamma)}\). Thus a fixed-fringe separation \(d\le\|v_0-v_1\|\) entails \(\rho\ge\kappa\gamma d^4/(8|\Delta g|^2)\), with the stated trace/norm convention.

## Scope boundary

The proof is all-waveform for the sensing-reference coherence vector under a fixed inactive reference, common parameter-independent sensing Hamiltonian, independent noiseless ancillas, and the specified Markovian dephasing plus terminal loss. It does not bound information in diagonal populations, retained syndrome/environment-like records, moving or corrected references, nor every estimator/output law. An allowed controller that exports parameter dependence into a diagonal population while this column decays is not ruled out by (C); extending the result would require a separate operational argument. No all-controller frontier is claimed.
