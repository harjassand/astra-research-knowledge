# External radiation of the symmetry-filtered pair

27 October 2026. Derivation for the supplied number-conserving, hard-core ladder. The engineered ladder coupling is denoted by `g`; the independent weak coupling to an additional electromagnetic environment is denoted by `lambda`. All energies below use the source convention `hbar = B = 1`. This note preserves the source's exact ideal-ladder BIC and its distinctions from a physical Maxwell implementation.

## 1. A symmetric electromagnetic environment already defeats the claimed physical protection

Place two identical parallel electric dipoles at positions `r_L = -R/2` and `r_R = R/2`, with dipoles perpendicular to `R`. Reflection through the midpoint exchanges the emitters and leaves the dipole orientation unchanged. Couple the two memories to vacuum radiation through

\[
H_{\rm em}=\sum_\lambda\int c|k|a^\dagger_{k\lambda}a_{k\lambda}\,d^3k,
\qquad
V=\lambda\sum_{i=L,R}\sum_\alpha\int
\big[v_{i\alpha}(k)\sigma_i^+a_{k\alpha}+\mathrm{h.c.}\big]d^3k,
\]

where

\[
v_{i\alpha}(k)=-i\sqrt{\frac{c|k|}{2\epsilon_0(2\pi)^3}}
\,d\cdot e_{k\alpha}\,e^{ik\cdot r_i}F(k).
\]

The ultraviolet form factor `F` is included so the Hamiltonian and Lamb shift have a declared ultraviolet interface. The expression is the rotating-wave form of the dipole interaction. Its downward on-shell matrix elements also give the second-order spontaneous-emission coefficient of the full dipole interaction; this observation is not a nonperturbative derivation of the ladder from Maxwell theory.

Define

\[
S_\pm^-=(\sigma_L^-\pm\sigma_R^-)/\sqrt2.
\]

Under full geometric reflection, the electromagnetic modes also split into even and odd radiation modes. The coupling is a sum of products of equally transforming system and field operators, so it **preserves the combined reflection**. Nevertheless,

\[
S_+^-|LR\rangle=|e_+\rangle,
\qquad
S_-^-|LR\rangle=-|e_-\rangle.
\]

Both matrix elements have unit norm. An even initial pair can decay to an even residual excitation plus an even photon, or an odd residual excitation plus an odd photon. Both final total parities are even. Ordinary vacuum supplies these channels at every positive photon frequency. No asymmetric fabrication error is necessary.

Write the collective one-photon rates, with the explicit `lambda^2` factor removed, as

\[
\mathcal J_\pm(\omega)=\Gamma_0(\omega)[1\pm f_\eta(\omega R/c)],
\quad
\Gamma_0(\omega)=\frac{|d|^2\omega^3}{3\pi\epsilon_0c^3}|F(\omega/c)|^2,
\]

\[
f_\eta(u)=\frac32\left[
(1-\eta^2)\frac{\sin u}{u}
+(1-3\eta^2)\left(\frac{\cos u}{u^2}-\frac{\sin u}{u^3}\right)
\right],
\quad \eta=\widehat d\cdot\widehat R.
\]

At `g = 0`, the pair population-decay coefficient is exactly

\[
\boxed{\Gamma_{LR}=\lambda^2[\mathcal J_+(3)+\mathcal J_-(3)]
=2\lambda^2\Gamma_0(3).}
\]

This coefficient is independent of emitter spacing. Making one collective one-excitation channel subradiant makes the other bright, and the doubly excited state has a decay matrix element into each. For small nonzero `g`, continuity of the dressed bound states gives

\[
\Gamma_{P}=2\lambda^2\Gamma_0(3)+O(\lambda^2g^2)+o(\lambda^2)
\]

at fixed finite nonzero separation, when the external spectral functions are smooth near 3. The small-separation collective-bath limit is useful algebraically, but the divergent free-space dipole-dipole Lamb shift must not be omitted in a physical co-location limit. Frequency shifts and direct exchange need to be included or compensated; such compensation is a physical cost.

This does not contradict the supplied ideal-ladder theorem. That theorem omits the additional electromagnetic continuum. It corrects the narrower physical interpretation that parity breaking is required to reopen decay.

## 2. Exact transition measure at finite engineered coupling

The ideal ladder permits an unusually explicit inclusive calculation. Let `h_sigma` denote either complete one-body parity Hamiltonian and let `mu_sigma` be its endpoint spectral measure, including its bound atom. Set

\[
L_\sigma(z)=\iint\frac{d\mu_\sigma(x)d\mu_\sigma(y)}{x+y-z},
\qquad
G_\sigma(z)=\int\frac{d\mu_\sigma(y)}{y-z}.
\]

Let `E_p` be the exact hard-core pair root `L_+(E_p)+L_-(E_p)=0`. In the even harmonic two-particle space the excluded normalized double-memory vector is

\[
|D\rangle=(|LL\rangle+|RR\rangle)/\sqrt2
=(|2e_+\rangle+|2e_-\rangle)/\sqrt2.
\]

The other excluded double-memory combination is odd and does not occur here. Compression to the hard-core even space implies

\[
|P\rangle=\mathcal N(H^{\rm harm}_2-E_p)^{-1}|D\rangle,
\qquad
\mathcal N^2=\frac{2}{L_+'(E_p)+L_-'(E_p)}.
\]

The sign of `mathcal N` fixes the otherwise arbitrary eigenvector phase. In the source family the sign giving positive bare-pair overlap is negative.

**Exact transition identity.** For each parity,

\[
\boxed{S_\sigma^-|P\rangle
=\mathcal N\,G_\sigma(E_p-h_\sigma)|e_\sigma\rangle.}
\]

Consequently the complete residual-state spectral measure is

\[
\boxed{dW_\sigma(x)=\mathcal N^2
\left|G_\sigma(E_p-x)\right|^2d\mu_\sigma(x).}\tag{1}
\]

This includes transitions to the residual one-particle bound state **and every scattering state**. It is not a projection onto a pair of dressed memory modes.

Proof: On the physical hard-core domain, `S_sigma^-` agrees with the harmonic annihilator `a(e_sigma)`. In the symmetric tensor representation,

\[
a(e)(d\Gamma(h)-E)^{-1}|2e\rangle
=\sqrt2\left[\int\frac{d\mu(y)}{h+y-E}\right]|e\rangle.
\]

Applying this to the two orthogonal terms of `D` gives the identity. The spectral theorem then gives (1). All inverse denominators are regular on the own-parity spectral supports because the source pair lies in a gap of the even harmonic continua and between, rather than at, the double-bound poles.

For an arbitrary mirror-preserving external environment, the second-order **population** linewidth is therefore

\[
\boxed{\Gamma_P^{(2)}=
\lambda^2\sum_{\sigma=\pm}
\int_{x<E_p}\mathcal J_\sigma(E_p-x)\,dW_\sigma(x).}\tag{2}
\]

Each integrand is nonnegative. Equation (2) is a Fermi-golden-rule/resonance coefficient: the transition measure is exact at finite `g`, while the external coupling is treated to second order. Usual limiting-absorption and spectral regularity hypotheses are required to promote a positive coefficient to a resonance statement. Equation (2) is not, on its own, a finite-time gate-error theorem.

The two bound-state contributions already give a positive lower bound whenever the corresponding external LDOS is positive. Near zero engineered coupling, their weights each approach one. This proves the leading `2 lambda^2 Gamma_0` physical obstruction without evaluating the continuum integral.

## 3. The continuum transition weight starts at sixth order

Let

\[
a=4-2\sqrt3,\quad b=4/\sqrt3-2=a/\sqrt3,
\quad\kappa_+=\sqrt2,\quad\kappa_-=1.
\]

The bare bath endpoint densities are

\[
\rho_\sigma(x)=\frac2\pi\sqrt{1-(x-c_\sigma)^2},
\quad c_+=5,\quad c_-=1,
\]

on their respective support intervals. Their dressed endpoint continuum measures obey, uniformly on those intervals,

\[
d\mu_\sigma^{\rm cont}(x)
=\kappa_\sigma^2g^2\frac{\rho_\sigma(x)}{(x-3)^2}\,dx+O(g^4)\,dx.
\]

The double-bound poles are separated by `(F_+(3)-F_-(3))g^2 = -3ag^2` at leading order. Hence

\[
\mathcal N^2=9a^2g^4+O(g^6),\qquad
G_\sigma(E_p-x)=\frac1{x-3}+O(g^2).
\]

Substitution into (1) yields the positive density

\[
\boxed{dW_\sigma^{\rm cont}(x)
=9a^2\kappa_\sigma^2g^6
\frac{\rho_\sigma(x)}{(x-3)^4}\,dx+O(g^8)\,dx.}\tag{3}
\]

The integral is elementary:

\[
\int\frac{\rho_\sigma(x)}{(x-3)^4}\,dx
=\frac{2}{9\sqrt3}.
\]

For example, it follows by differentiating three times the endpoint Weyl function `m_c(z)=2[(z-c)-sgn(z-c)sqrt((z-c)^2-1)]`; the integral is `-m_c'''(3)/6`. Thus

\[
\boxed{W_+^{\rm cont}=\frac{4a^2}{\sqrt3}g^6+O(g^8),
\qquad W_-^{\rm cont}=\frac{2a^2}{\sqrt3}g^6+O(g^8).}
\]

Their sum is

\[
\boxed{W_{\rm cont}=(56\sqrt3-96)g^6+O(g^8)
=0.994845223857\ldots\,g^6+O(g^8).}\tag{4}
\]

The absence of an order-`g` continuum transition amplitude has a direct explanation: applying a memory lowering operator to the pair's first-order dressing reproduces the residual one-body bound state's first-order dressing. The amplitudes cancel in the orthogonal continuum projection. Equation (1) makes the cancellation exact before expansion.

This is a new consequence derived here from the preserved source resolvent. It is not asserted to be a historically novel quantum-optics principle.

## 4. What a spectral notch does and does not buy

An external LDOS notch covering both frequencies `E_p(g)-E_sigma(g)` for the full controlled ramp removes the order-one bound-transition weights from (2). It leaves

\[
\Gamma_{P,\rm notch}^{(2)}
=9\lambda^2a^2g^6\sum_\sigma\kappa_\sigma^2
\int\frac{\rho_\sigma(x)\mathcal J_\sigma(6-x)}{(x-3)^4}\,dx
+O(\lambda^2g^8).
\]

At this perturbative order, a conditional phase taking time of order `g^-4` accumulates a radiation contribution of order `lambda^2 g^2`. This supplies a concrete LDOS design target.

**There is no fixed-lambda, g-to-zero gate theorem here.** Taking the external-coupling expansion first at fixed `g` is essential. Higher orders in `lambda`, external Lamb shifts, interaction corrections, and emission involving more external photons may dominate in a different joint limit. A uniform remainder bound or an exact combined spectral model is needed before using this scaling as an asymptotic implementation guarantee. If the external coupling itself scales as `lambda = delta g`, the displayed second-order term becomes `delta^2 g^8`, which explains why a source model whose wrong-band amplitude is proportional to `g` has a different apparent small-`g` order.

For an exact radiation-free state, a notch only around frequency 3 is insufficient. The residual continua in (1) require the following additional spectral exclusions:

* A residual odd lower-band state `x in [0,2]` needs an odd external photon at `E_p-x`, near `[4,6]`.
* A residual even upper-band state `x in [4,6]` needs an even external photon at `E_p-x`, near `[0,2]`, when this energy is positive.

The frequencies are shifted by a carrier `Omega` if every number-conserving one-particle energy is shifted by `Omega`. The required photon frequency then shifts by `Omega`, while the relative interval bookkeeping remains the same. All statements of exact suppression must be made on the full supports, not only at the undressed memory frequency.

Equivalently, the external channels must obey the same parity-resolved sumset exclusion as the engineered bath. A shielded structure with an appropriate symmetry-resolved LDOS or an actual photonic bandgap is a potential route. Ordinary three-dimensional vacuum has no such exclusion. This is an environmental design requirement, not an acquired Maxwell or circuit realization.

## 5. Other physical losses remain at lower order

The pair's bath occupation follows from its first-order dressing:

\[
\langle N_{\rm bath}\rangle=3bg^2+O(g^4),
\qquad
\langle n_L+n_R\rangle=2-3bg^2+O(g^4).
\]

If every oscillator leaks through an independent, spectrally flat Markov channel with population rate `kappa`, the pair jump rate is

\[
\Gamma_{\rm rails}=\kappa\langle N_{\rm bath}\rangle
=3b\kappa g^2+O(\kappa g^4).
\]

The original connected shift is `chi = -3ab g^4+O(g^6)`. A plateau phase of `pi` therefore has a leading rail-loss exposure `pi kappa/(a g^2)`. Reducing the engineered coupling worsens this cost. A physical bath generally has frequency-dependent damping, so the flat Markov model is a declared model, not a universal microscopic rate. Suppressing direct memory emission does not suppress these oscillator losses.

Similarly, without a memory-frequency notch, direct emission contributes a phase-time exposure of order `lambda^2/g^4`. Slowing the protected ideal ramp cannot eliminate this external physical loss. Finite control duration, preparation, retrieval, pulse noise, and coherent shift compensation still require an inclusive protocol analysis.

## 6. Executed checks

`radiative_spectral_weights.py` independently constructs the connected ladder in its complete allowed two-particle Fock space, restricts the exact reflection-even subspace, diagonalizes the pair, applies the physical memory lowering operators, and decomposes the result into every one-particle eigenstate. It also evaluates (1) independently from the one-body spectral measures.

For 18 sites per rail:

| g | Total continuum transition weight / g^6 | Bound transition weight, summed |
|---:|---:|---:|
| 0.4 | 0.7182711209 | 1.8393186592 |
| 0.2 | 0.9071377336 | 1.9621407248 |
| 0.1 | 0.9713531170 | 1.9906733231 |
| 0.05 | 0.9888656059 | 1.9976767215 |
| 0.025 | 0.9933435072 | 1.9994197002 |
| analytic limit | 0.9948452239 | 2 |

The finite-Fock transition vectors and the exact-resolvent formula agree to below `2e-12` for `g = 0.1, 0.2, 0.4`. At smaller `g` the double-bound-pole subtraction becomes numerically ill-conditioned; the observed absolute vector discrepancies remain below `3.1e-9` at `g = 0.025`. The small-`g` coefficient (4) is derived analytically and does not rely on that subtraction.

At `g = 0.2`, changing the rail length from 10 to 18 to 28 changes the continuum transition weight from `5.8056814676e-5` to `5.8056814952e-5` to `5.8056814952e-5`. These are finite-volume floating-point checks, not interval-arithmetic certificates or an experimentally measured lifetime. The JSON files retain all transition weights and the specified vacuum spectral-rate diagnostics.

## Sources and ancestry

The hard-core ladder, its pair resolvent, all-sector positivity, and ideal gate are supplied in `ASTRA_SYMMETRY_FILTERED_EMBEDDED_PAIR_20261027(3).md`. The source receipt's distinction between its wrong-band model and generic physical symmetry breaking is preserved.

The microscopic radiation framework and collective dipole rates are established quantum optics:

1. R. H. Lehmberg, *Radiation from an N-Atom System. I. General Formalism*, Physical Review A **2**, 883 (1970), https://doi.org/10.1103/PhysRevA.2.883.
2. R. H. Lehmberg, *Radiation from an N-Atom System. II. Spontaneous Emission from a Pair of Atoms*, Physical Review A **2**, 889 (1970), https://doi.org/10.1103/PhysRevA.2.889.
3. D. Plankensteiner et al., *Cavity antiresonance spectroscopy of dipole coupled subradiant arrays*, Appendix A for the radiation kernel and the main text for the physical distinction between coherent coupling and free-space loss, https://arxiv.org/html/1703.06039v2. Rate conventions in that paper differ by factors of two in its linewidth/Lindblad notation; this note consistently uses population decay and defines its own rate matrix.
4. S. Filipp et al., *Preparation of Subradiant States using Local Qubit Control in Circuit QED*, https://arxiv.org/abs/1107.2078, demonstrates that dark-state preparation and access require control-field symmetry to be accounted for. It does not supply a full encoded hard-core replacement for this ladder.

The exact transition identity (1), its sixth-order integrated coefficient (4), and their application to the supplied ladder were derived in this continuation. No priority audit or physical implementation claim is made.
