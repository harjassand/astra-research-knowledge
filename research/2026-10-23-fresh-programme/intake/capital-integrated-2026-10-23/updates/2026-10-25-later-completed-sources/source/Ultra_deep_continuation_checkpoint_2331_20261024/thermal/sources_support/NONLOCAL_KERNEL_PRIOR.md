# Positive long-range spring kernels: closest primary comparisons

Scope: bounded comparison for the finite positive Fejer-kernel lattice in `NONLOCAL_KERNEL_CONSTRUCTION.md`. This checks whether its interaction operation and physical link implementation are already present in primary sources. It is not a novelty or priority determination.

## Dispersion shaping by inverse Fourier coefficients is established

Kazemi et al., “Drawing Dispersion Curves: Band Structure Customization via Nonlocal Phononic Crystals,” *Phys. Rev. Lett.* 131, 176101 (2023), [DOI 10.1103/PhysRevLett.131.176101](https://doi.org/10.1103/PhysRevLett.131.176101), formulates a monoatomic chain with symmetric springs to neighbours at each range n. Its equations of motion and dispersion are Eqs. (1)–(2):

\[
m\ddot u_j=\sum_n k_n(u_{j+n}-2u_j+u_{j-n}),\qquad
\omega^2(q)=\frac{2}{m}\sum_n k_n[1-\cos(nqa)].
\]

Eqs. (4)–(5) map cosine coefficients of a target \(\Omega^2(q)\) to the nonlocal spring constants by Fourier integration. The paper states admissibility conditions on the target curve (smoothness, \(\Omega(0)=0\), finite positive acoustic slope and zero slope at the zone edge) and gives numerical full-curve designs with multiple neighbour orders. The current Fejer construction is a particularly simple member of this inverse-design class: since

\[
D_N(q)^2=N+2\sum_{n=1}^{N-1}(N-n)\cos(nq),
\]

the target \(\omega_N^2=(c_N/M)(N^2-D_N^2)\) has exact cosine coefficients corresponding to \(k_n=c_N(N-n)>0\), \(n=1,\ldots,N-1\). Thus inverse-Fourier synthesis of such a positive spring sequence is an established operation; I did not find the exact Fejer family stated in these sources. That leaves its all-crossings thermal asymptotic as a separate claim. The 2023 work is a design/model paper, not a fixed-resource thermal-transport result or a report of a fabricated arbitrary-range Fejer lattice. Its accepted manuscript is available from [APS/CHORUS](https://link.aps.org/accepted/10.1103/PhysRevLett.131.176101).

Rouhi and Droz, “Tailoring dispersion and evanescent modes in multimodal nonlocal lattices using positive-only interactions,” *Phys. Rev. Applied* 25, 064066 (2026), [DOI 10.1103/l4jf-426m](https://doi.org/10.1103/l4jf-426m), generalize the operation to uniform multimodal lattices with nonlocal order \(p\) and up to \(P\) neighbour ranges (Secs. 2.1–2.2, Eqs. (2.1)–(2.6)). For the monoatomic spring special case, Appendix A.2, Eqs. (A.6)–(A.10), gives the same finite cosine-spring form and a linear coefficient solve. Appendix A.4.1 enforces nonnegative/positive stiffnesses; Sec. A.4.2 explicitly revisits the 2023 target curves and reports that positive-stiffness constraints can prevent globally accurate reconstruction, though local-region fits can improve it. That is a relevant feasibility caveat, not an obstruction to this particular target whose coefficients are analytically positive. Their contribution is general interpolation/control of selected points, branches and beam-lattice behavior, not the Fejer-family conductance bound.

## What physical implementations use to connect distant cells

Chen, Kadic and Wegener, “Roton-like acoustical dispersion relations in 3D metamaterials,” *Nature Communications* 12, 3278 (2021), [DOI 10.1038/s41467-021-23574-2](https://doi.org/10.1038/s41467-021-23574-2), starts from an idealized 1D chain (Eq. (1)) with nearest and Nth-neighbour springs. In its toy-model comparison, the authors hold the low-wavenumber phase velocity \(a\sqrt{(K_1+N^2K_N)/m}\) fixed while varying \(K_N/K_1\); thus fixed long-wavelength \(K_{\rm eff}/m\) dispersion shaping is already explicit for this family. For N=3, the physical proposal replaces the distant spring by a 3D structure. The direct experimental follow-up, Iglesias Martínez et al., “Experimental observation of roton-like dispersion relations in metamaterials,” *Science Advances* 7, eabm2189 (2021), [DOI 10.1126/sciadv.abm2189](https://doi.org/10.1126/sciadv.abm2189), demonstrates the actual operation: additively printed polymer cubes act as effective masses, cylindrical rods as nearest- and third-neighbour elastic links, and an auxiliary frame routes the beyond-nearest connection. A second, macroscopic air-channel implementation represents effective masses by cavities and links by tubes. The paper measures local elastic displacement in the microstructure and pressure in the air-channel sample and compares the dispersion with finite-element calculations.

These experiments establish that a third-neighbour path can be built and measured. They do not demonstrate a sequence of all positive couplings through range \(N-1\) as \(N\) grows, nor report a matched total point-mass and static-\(K_{\rm eff}\) comparison for the thermal objective. In the ideal toy-chain equations the links are Hooke springs; the physical geometry and continuum finite-element treatment include rods/frame or channels, so connector mass and internal motion are present there. The papers do not provide a separate connector-mode or connector-mass budget under the fixed-resource scaling in the present construction. They measure/design dispersion, not Bose-weighted total Landauer conductance.

**Bounded conclusion:** inverse Fourier spring design, positive-only nonlocal parameterization, and an experimental third-neighbour routing architecture are primary-source-established. The open question for the current mathematical result is narrower: its exact all-crossings Bose conductance scaling at fixed point mass and long-wavelength stiffness, together with the physical cost of realizing the increasing range and distributed connectors. None of these compared papers is a direct matched fixed-resource thermal-transport theorem; this limited check is not a novelty claim.

**Source-access note:** the Kazemi accepted manuscript and Rouhi–Droz arXiv full text were read directly. Nature/PMC primary article text was available in the native reader's indexed source passages; opening the SciAdv PMC landing page returned a browser-verification page, and no supplementary files were acquired for this bounded check.
