## ASTRA — A two-photon resonance theorem

The strongest continuation is a route past the previous fourth-order obstruction. The open two-photon continuum does produce decay, but the exact resolvent shows that the decay occurs on a parametrically longer timescale than the connected two-qubit interaction.

For the specified infinite, reciprocal, gapless SSH waveguide, with two hard-core memories coupled to adjacent bond-gradient ports, the leading scales are:

\\[ \boxed{ \Delta E\_{\mathrm{interaction}} =-\frac{g^4}{12}+o(g^4) } \\]

and

\\[ \boxed{ \Gamma\_{\mathrm{two-photon}} \sim\frac{43}{5184\pi}g^8 \approx0.002640302\\,g^8. } \\]

The second coefficient is not inferred from a finite-ring lifetime fit. It comes from the full two-photon spectral density, including both propagating SSH bands.

### Exact reduction

If \\(L\_+(z)\\) and \\(L\_-(z)\\) are the complete two-boson Green functions associated with the symmetric and antisymmetric one-particle parity modes, then the physical hard-core pair has the exact Green function

\\[ \boxed{ G\_{\rm pair}(z)=\frac{2L\_+(z)L\_-(z)}{L\_+(z)+L\_-(z)}. } \\]

This incorporates the entire continuum and both forbidden double-occupation states. It reduces the interacting two-particle problem to a scalar resolvent equation without projecting photons out.

The calculated linewidth coefficient is independently supported by two routes: the previously derived fourth-order radiative source and a new convolution of the exact one-particle spectral measures. Direct finite-Fock Green-function calculations reproduce the rank-two identity to numerical precision.

### A broader interaction–radiation principle

The calculation extends beyond the SSH lattice.

For two reflection-symmetric impurities with transition energy inside a one-photon bath gap, define the symmetric and antisymmetric bath responses \\(F\_+(E)\\) and \\(F\_-(E)\\). Put

\\[ \Delta F=F\_+(\varepsilon)-F\_-(\varepsilon),\qquad \Delta F'=F\_+'(\varepsilon)-F\_-'(\varepsilon). \\]

Under the stated spectral regularity assumptions, the leading connected interaction is

\\[ \boxed{\chi_g=-g^4\Delta F\\,\Delta F'+o(g^4).} \\]

The radiative width is instead governed by a positive convolution of the two-photon continuum, at order \\(g^8\\).

This separates two physical properties: the dispersive response determines the coherent interaction, while the on-shell continuum spectral weight determines its eventual decay.

I tested the general interaction formula on two independently constructed finite-bath Hamiltonians. One gives a positive connected interaction and the other a negative one, with both numerical coefficients converging to the predicted expressions.

### 2. A controlled phase before substantial two-photon decay

The stronger consequence is a weak-coupling, full-state controlled-Z construction.

The exact pair spectral measure, centered at its resonance energy and rescaled by \\(g^8\\), approaches a Cauchy distribution with half-width

\\[ \gamma=\frac{43}{10368\pi}. \\]

This implies that, at the shorter interaction time \\(t=O(g^{-4})\\), the bare two-excitation state returns to itself up to its connected phase, with complete-state error tending to zero as \\(g\to0\\).

Apply two local \\(Z\\) echo pulses to cancel the faster one-particle exchange, then correct the known individual memory phases. At

\\[ \boxed{T_g=\frac{12\pi}{g^4},} \\]

the resulting operation obeys the asymptotic relation

\\[ \boxed{ \\|U\_{\mathrm{echo}}(g)P-P\\,\mathrm{CZ}\\| \longrightarrow0 \quad(g\to0). } \\]

Here \\(P\\) embeds the complete two-qubit computational code with bath vacuum. The limit includes all escaping photon states and arbitrary untouched quantum references.

The qualification matters: this is an asymptotic model theorem, not a certified 1% gate at a specified experimental coupling. Moreover, the same SSH model already supports a much faster \\(g^{-2}\\)-scale iSWAP operation, so the slow controlled-Z construction is not evidence of a practical gate advantage. Its scientific value is showing that a coherent fourth-order interaction can be accumulated despite a genuinely open two-photon decay channel.

### Independent computational checks

The newly executed calculations support the theoretical scaling:

| Coupling \\(g\\) | Connected shift divided by \\(g^4\\) | Inferred amplitude linewidth divided by \\(g^8\\) |
| ---------------- | ------------------------------------ | ------------------------------------------------- |
| 0.25             | −0.079973                            | 0.00137918                                        |
| 0.18             | −0.081564                            | 0.00136248                                        |
| 0.12             | −0.082539                            | 0.00134345                                        |
| 0.08             | −0.082979                            | 0.00133174                                        |
| Predicted limit  | −0.083333                            | 0.00132015                                        |

The numerical checks retain the upper positive-energy bound pole, which would otherwise introduce an error in the spectral calculation. Separate full-Hamiltonian simulations confirm the one-particle echo's expected \\(O(g)\\) error scaling.

### Preserved research

Complete mathematical derivation

Exact resolvent reduction, general interaction law, continuum spectral limit, controlled-phase construction, limitations and proof details.

Full continuum resolvent calculation · Results

Spectral scaling test · Results

General interaction-law test · One-particle echo audit

Remaining research frontier: Turn the weak-coupling convergence theorem into an explicit finite-\\(g\\) error certificate, including finite-duration control pulses and independent memory decoherence. A stronger alternative is to change the emitter geometry so the on-shell two-photon radiation coefficient vanishes while the connected interaction remains nonzero.

The relevant Green-function and embedded-resonance methods have substantial existing literature.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://journals.aps.org\&sz=32)

Phys. Rev. Research

+1

&#x20;The new contribution is the model-specific spectral reduction and interaction–radiation separation; historical novelty and experimental advantage remain unverified.
