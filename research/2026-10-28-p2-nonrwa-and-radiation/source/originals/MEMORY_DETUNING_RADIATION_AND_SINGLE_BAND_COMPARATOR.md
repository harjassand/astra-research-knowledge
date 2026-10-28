# Memory-detuning radiation and the single-band comparator

27 October 2026. Derived from the supplied symmetry-filtered ladder. Units are hbar=B=1. This result concerns static memory-frequency imbalance, not external electromagnetic loss, rail disorder, or a full noisy gate.

## Exact interacting odd-sector formula

Let c_+,c_- denote the parity endpoint couplings; the preserved calibration is c_+=sqrt(2)g, c_-=g. Perturb the Hamiltonian by epsilon D, where D=n_L-n_R. The memory frequencies become 3+epsilon and 3-epsilon. This breaks the simultaneous memory/rail exchange but annihilates the bare pair: D|LR>=0.

The odd two-particle sector is the tensor product of the two one-particle parity channels with one forbidden contact q_o=|e_+e_->=(|LL>-|RR>)/sqrt(2). Put K_o=h_+ tensor I + I tensor h_-, R_o(z)=(K_o-z)^(-1), and M(z)=<q_o,R_o(z)q_o>. Its physical hard-core resolvent is exactly

\[
R_{o,\mathrm{hc}}(z)=P_o\left[R_o(z)-R_o(z)|q_o\rangle M(z)^{-1}\langle q_o|R_o(z)\right]P_o. \tag{1}
\]

This contact subtraction is essential; free final photons miss the leading answer.

For the ideal even pair, let q_e=(|e_+e_+>+|e_-e_->)/sqrt(2). At E=E_p, the supplied root L_+(E)+L_-(E)=0 gives

\[
\psi=C(K_e-E)^{-1}q_e,\qquad C=[(L_+'(E)+L_-'(E))/2]^{-1/2}. \tag{2}
\]

This phase convention has psi approaching -|LR>. The source v=D psi already lies in the physical odd space, since <q_o,D psi>=2<q_e,psi>=0.

Let mu_s be the complete memory spectral measure of h_s and r_s(z)=integral dmu_s(x)/(x-z). In the free product spectral representation the source is exactly

\[
v(x,y)=C\sqrt{d\mu_+(x)d\mu_-(y)}[r_+(E-x)+r_-(E-y)]. \tag{3}
\]

The square roots denote spectral wavefunctions; continuous components use densities and atomic components use weights. Define K(z)=<q_o,R_o(z)v> and Q=K(E+i0)/M(E+i0). At this energy only the upper-plus-lower continuum is open. Its source spectral density in the interacting odd sector is

\[
\boxed{J_D(E)=\int_{[4,6]\cap[E-2,E]}\rho_+(x)\rho_-(E-x)
\left|C[r_+(E-x)+r_-(x)]-Q\right|^2dx.} \tag{4}
\]

Here rho_s is the complete channel's MEMORY continuum density, not the uncoupled bath endpoint density. All bound atoms remain in M,K,C,E.

The Fermi-golden-rule amplitude linewidth coefficient is

\[
\gamma_{\rm amp}=\pi\epsilon^2J_D(E)+o(\epsilon^2), \tag{5}
\]

and the corresponding probability decay rate is twice this. Equation (4) establishes the spectral coefficient. A resonance expansion or a finite-time error law additionally needs its limiting-absorption/analytic-continuation and remainder hypotheses. For fixed small nonzero g, E_p lies away from the odd convolution's interior threshold at 6; local continuation is available as the relevant analytic route, but is not proved here. Long-time branch-cut tails are not excluded.

## Leading detuning coefficient

Set c_+=alpha g, c_-=beta g for fixed nonzero alpha,beta with unequal squared magnitudes, and

\[
a=4-2\sqrt3,\quad b=4/\sqrt3-2,\quad A=c_+^2,\quad B=c_-^2,\quad P=A+B,\quad\Delta=A-B.
\]

Ordinary one-body expansions give

\[
E_+=3-aA+abA^2+O(g^6),\quad E_-=3+aB-abB^2+O(g^6),
\]

\[
Z_+=1-bA+O(g^4),\quad Z_-=1-bB+O(g^4).
\]

Combining these with the supplied fourth-order connected shift gives

\[
E_p=6-a\Delta+O(g^6),\quad\chi=-abP\Delta+O(g^6),\quad C=aP+O(g^4). \tag{6}
\]

Let |B_+B_-> be the harmonic odd bound-bound product. The source overlap is

\[
\langle B_+B_-|D\psi\rangle=-b\Delta+O(g^4). \tag{7}
\]

To see (7), expand both states to first order in the endpoint couplings. The even pair has opposite signs in its upper-memory-plus-photon and lower-memory-plus-photon amplitudes. The dressing of the odd harmonic bound product has the same signs. Their overlap is the difference of the two endpoint inverse-square forms, -b(A-B) in the phase convention (2). The bare term vanishes because D|LR>=0.

The odd harmonic bound-bound pole lies at E_++E_-=E_p-chi and dominates both M and K. Hence

\[
Q=-b\Delta+o(g^2). \tag{8}
\]

On the outgoing continuum shell, the uncorrected term C[r_+(E-x)+r_-(x)] is O(g^4), whereas Q is O(g^2). The cancellation in the first term is the complementary-denominator cancellation of the two second-order emission time orderings. Thus the interacting contact correction supplies the leading emission.

For the uncoupled bath endpoint densities varrho_+(x)=(2/pi)sqrt(1-(x-5)^2) and varrho_-(y)=(2/pi)sqrt(1-(y-1)^2), the leading memory densities on shell are A varrho_+(x)/(x-3)^2 and B varrho_-(6-x)/(x-3)^2. Their integral is

\[
\int_4^6\frac{\varrho_+(x)\varrho_-(6-x)}{(x-3)^4}dx=\frac{16}{27\pi^2}. \tag{9}
\]

Therefore

\[
\boxed{\gamma_{\rm amp}=\frac{16b^2}{27\pi}\epsilon^2AB\Delta^2+o(\epsilon^2g^8).} \tag{10}
\]

The remainder notation denotes the coefficient of epsilon squared at fixed g followed by its weak-g asymptotic; a uniform joint-limit estimate is not supplied. Small symmetry breaking, weak coupling, and long gate time have not been freely interchanged.

For A=2g^2 and B=g^2 this becomes

\[
\boxed{\gamma_{\rm amp}=\frac{32(4/\sqrt3-2)^2}{27\pi}\epsilon^2g^8+o(\epsilon^2g^8)
=0.0361143649965\ldots\epsilon^2g^8+o(\epsilon^2g^8).} \tag{11}
\]

This coefficient belongs to a different perturbation from the preserved parity-preserving wrong-band source. It does not describe ordinary vacuum emission.

## Executed checks

`detuning_fgr.py` evaluates (4) using analytic half-line Weyl functions and adaptive continuum quadrature. Complete 220-site Jacobi spectral measures supply the gapped even state. These are convergent numerical checks, not interval arithmetic certificates.

| g | coefficient of epsilon squared in amplitude linewidth | coefficient divided by g to eighth |
|---|---:|---:|
| .4 | 6.37897675e-6 | .00973355 |
| .2 | 6.68375948e-8 | .02610844 |
| .1 | 3.33087620e-10 | .03330876 |
| .05 | 1.38252430e-12 | .03539262 |
| .035 | 8.05244682e-14 | .03575885 |
| limiting value | — | .03611436 |

`detuning_rank_one_audit.py` independently builds the complete physical connected ladder hard-core Fock matrix. For 4,6,8 bath sites per rail it verifies (1)-(3) against the direct odd-sector resolvent at nonzero imaginary spectral parameter. Resolvent errors are below 3e-16 and source norms agree at machine precision. This checks the interacting formula itself rather than refitting its asymptotic coefficient. Additional port-ratio checks appear in `general_port_detuning_results.json`.

## A stronger ordinary local-gate comparator

For the local same-end two-memory gate, global embedding itself provides no demonstrated performance resource. At fixed total squared endpoint coupling

\[
P=c_+^2+c_-^2=2(t^2+s^2),
\]

(6) yields |chi|=abP|Delta|+O(P^3)<=abP^2+O(P^3). The leading interaction is maximized by one accessible band, c_-=0 or c_+=0.

With c_-=0 (t=s), the lower band is exactly decoupled from both memories. Exchanging the two bath rails while leaving EACH memory fixed is conserved even with unequal memory frequencies. Equivalently the lower-band excitation number is conserved and remains zero from a memory-only input.

In this accessible subsystem the two-excitation continuum begins near energy 7 (one memory plus an upper-band photon); the pair remains near 6. For sufficiently small coupling and |epsilon|<1 with an adequate gap margin, the pair is an ordinary isolated bound state. Static memory imbalance cannot radiate into the lower band at any order. This requires symmetric coupling to the two rails and preserved bath bands, but does not require memory-exchange symmetry.

The preserved calibration uses P=3g^2 and has |chi|=3abg^4+O(g^6). The single-band comparator at the same P gives |chi|=9abg^4+O(g^6): three times larger at leading order, with no radiation caused by D.

Thus the two-band embedded-pair architecture has no established local-gate advantage over this equally resourced band-gap comparator. It remains a valid interacting embedded eigenstate construction. A practical advantage requires a further task or constraint genuinely demanding both bands or globally gapless accessible modes.

Neither architecture resolves rail disorder, external electromagnetic modes, thermal occupation, control noise, or finite-time loading cost.
