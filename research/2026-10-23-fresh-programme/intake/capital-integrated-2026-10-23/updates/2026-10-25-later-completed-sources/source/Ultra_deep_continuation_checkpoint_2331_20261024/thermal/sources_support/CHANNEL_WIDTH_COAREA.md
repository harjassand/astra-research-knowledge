# Intrinsic channel width, backward waves, and the Landauer heat interpretation

Scope: check the total-variation channel-width identity used for the scalar Fejer lattice against primary energy-flow and Landauer formulas. This is a derivation/interface check, not a material-conductance claim.

## Channel count includes backward waves

Chen, Kadic and Wegener, “Roton-like acoustical dispersion relations in 3D metamaterials,” *Nature Communications* 12, 3278 (2021), [DOI 10.1038/s41467-021-23574-2](https://doi.org/10.1038/s41467-021-23574-2), write the toy-chain equation and dispersion in Eqs. (1)–(2):

\[
m\ddot u_n=K_1(u_{n+1}-2u_n+u_{n-1})+
K_N(u_{n+N}-2u_n+u_{n-N}),\qquad
\omega^2(k)=\frac{4}{m}\left[K_1\sin^2\frac{ka}{2}
+K_N\sin^2\frac{Nka}{2}\right].
\]

For one scalar periodic branch, define its right-moving channel count at regular \(\omega>0\) by
\[
N_R(\omega)=\#\{q\in[-\pi,\pi):\omega(q)=\omega,\ \omega'(q)>0\}.
\]
The sign test is group velocity, not wave-number sign. Chen et al. explicitly show a frequency range with three roots at \(k>0\): two forward modes and one backward mode with positive phase velocity but negative group velocity. Its time-reversed root at \(-k\) has positive group velocity and energy flow, so it is a right-moving channel. Across the full Brillouin zone there are three right movers in this example. Restricting “right-moving” to \(q>0\) would omit the right-moving state on the backward part of the dispersion.

The same primary source checks energy velocity directly. Its Eq. (3) is
\[
\langle p(k)\rangle=\frac{\widetilde u^2\omega}{2}
\left[K_1\sin(ka)+N K_N\sin(Nka)\right].
\]
Differentiating Eq. (2) gives
\[
\omega'(k)=\frac{a}{m\omega}\left[K_1\sin(ka)+N K_N\sin(Nka)\right],
\]
so \(\langle p\rangle=(m\widetilde u^2\omega^2/2a)\omega'\): their net energy-flow sign equals the group-velocity sign. The factor \(N\) in the long-spring contribution is essential; their Methods Eqs. (4)–(6) obtain it because \(N\) long springs cross each unit-cell cut. Their 3D calculation also plots local flux: individual rods can carry opposite partial flows, while the integrated unit-cell flux agrees in sign with group velocity. It is net flux, not the sign of one connector's local flow, that labels a channel direction.

## Coarea identity for the full scalar band

For a differentiable periodic scalar frequency \(\omega(q)\), one-dimensional coarea gives
\[
\int_0^\infty N_R(\omega)\,d\omega
=\int_{-\pi}^{\pi}\mathbf 1_{\{\omega'(q)>0\}}\omega'(q)\,dq
=\frac12\int_{-\pi}^{\pi}|\omega'(q)|\,dq.
\]
The last equality uses periodicity, \(\int_{-\pi}^{\pi}\omega'(q)dq=0\): positive and negative variation have equal magnitude. If the branch is even, as the reciprocal scalar Fejer branch is, this is also
\[
\int_0^\pi|\omega'(q)|\,dq
=\operatorname{TV}_{[0,\pi]}\omega.
\]
Every regular crossing is counted, including repeated crossings on a nearly flat oscillatory plateau. Critical values with zero group velocity are a measure-zero set for a nonconstant analytic band and do not affect the integral. A constant flat band has zero group velocity and contributes no transporting channel. For several bands, sum the total variations over bands (counting degenerate independent polarizations with multiplicity); taking the variation of only one ordered eigenvalue would miss channels. For a non-even but periodic scalar branch, the full-zone half-total-variation formula remains valid, while the half-zone identity does not follow.

## What this says about heat flow

Das and Dhar, “Landauer formula for phonon heat conduction: relation between energy transmittance and transmission coefficient,” *European Physical Journal B* 85, 372 (2012), [DOI 10.1140/epjb/e2012-30640-x](https://doi.org/10.1140/epjb/e2012-30640-x), give the contact-coupled current in Eq. (1):
\[
J=\frac{1}{2\pi}\int_{-\infty}^{\infty}d\omega\,
\hbar\omega\,\mathcal T(\omega)\,[f(\omega,T_L)-f(\omega,T_R)].
\]
For their 1D chain and ordered leads, Eq. (62) relates energy transmittance to plane-wave scattering:
\[
\mathcal T(\omega)=|\tau(\omega)|^2\frac{k_R\sin q'}{k_L\sin q}.
\]
Here k_L and k_R denote lead spring constants, while q and q' are lead wave numbers. The flux-normalization factor and \(|\tau|^2\) expose the contact/reflection dependence: a bulk propagating-channel count is not, by itself, the transmitted channel count of a finite device. With perfectly matched, lossless contacts each right-moving channel transmits one unit, so \(\mathcal T=N_R\); in general, \(\mathcal T\) is set by the full scattering problem and can be lower. The paper notes that for higher-dimensional or arbitrary-geometry reservoirs the NEGF expression remains, but the meaning of plane-wave \(\tau\) and its relation to \(\mathcal T\) is more involved (Introduction, Eqs. (1) and discussion).

Consequently the Fejer \(W=\int N_R\,d\omega\) bound is a correct ideal *intrinsic* scalar-bandwidth statement, with all crossings included. The Bose-weighted ideal conductance is no larger because its per-channel thermal weight is at most one. A finite-contact heat-conductance claim would additionally require \(\mathcal T(\omega)\); no such contact result is supplied by the total-variation proof. This distinction is already consistent with the construction's stated ideal-intrinsic scope.

Mousatov and Hartnoll's Eqs. (6)–(10), already scoped in MELTING_COMPARATOR.md, constrain a melting/sound-velocity scale and relate anharmonic scattering lifetime to high-temperature diffusivity. They do not count Bloch crossings or derive a ballistic transmission identity, so they do not change this channel/heat interpretation.
