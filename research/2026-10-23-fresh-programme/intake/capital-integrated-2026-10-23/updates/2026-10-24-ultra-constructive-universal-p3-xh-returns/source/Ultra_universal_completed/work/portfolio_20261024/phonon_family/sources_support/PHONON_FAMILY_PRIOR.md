# Bounded prior check: interlacing spectra, Foster synthesis, and the Bose optimum

Read against [`FIRST_FAMILY_CONSTRUCTION.md`](../FIRST_FAMILY_CONSTRUCTION.md) and the explicit inverse-realization derivation in [`COMPLETE_INVERSE_REALIZATION.md`](../circuit_support/COMPLETE_INVERSE_REALIZATION.md). This is a focused comparator check, not a priority search.

## The inverse-spectrum piece is close to established theory

Nylen and Uhlig, “Inverse eigenvalue problems associated with spring-mass systems,” *Linear Algebra and its Applications* 254 (1997), 409–425, DOI [10.1016/S0024-3795(96)00316-3](https://doi.org/10.1016/S0024-3795(96)00316-3), state the classical two-spectrum Jacobi result: given ordered λ's and μ's, there is a unique Jacobi matrix with spectra \(\sigma(T)=\{\lambda_i\}\) and \(\sigma(T_1)=\{\mu_i\}\) exactly under strict interlacing \(\lambda_1<\mu_1<\lambda_2<\dots<\mu_{n-1}<\lambda_n\). Their abstract also says they prove a related theorem prescribing \(\sigma(T)\) and \(\sigma(T+E)\) for a certain rank-one \(E\), and explicitly motivate recovery of mass/spring parameters from the spectra of a system and its modification. The primary publisher record is [here](https://www.sciencedirect.com/science/article/pii/S0024379596003163). I could verify the publisher's abstract, not the full article; the abstract does not specify the precise rank-one \(E\), so exact theorem-level identity with this construction remains unverified.

The construction's own determinant relation is a rank-one two-spectrum inverse problem in this same family:
\[
\frac{\prod_j(t+y_j)}{\prod_j(t+x_j)}=1+S q(t),\qquad
q(t)=v^{\mathsf T}(tI+D_0)^{-1}v.
\]
Strict interlacing makes the residues of \(q\) positive. The further conversion \(R(t)=1/[tq(t)]=m+\sum_j k_j/(t+\nu_j^2)\), with positive \(k_j\), gives the explicit mechanical *star* parameters. Thus the broad inverse-eigenvalue principle and strict-interlacing sufficiency are established prior art; the full-periodic-band packaging, translation zero mode, inferred total-mass/backbone-mass formulas, and explicit positive star map are the construction's more specialized content. This check cannot establish that the specialized statement is historically new.

## The positive star expansion is Foster-type network synthesis

Foster, “A Reactance Theorem,” *Bell System Technical Journal* 3 (1924), 259–267, DOI [10.1002/j.1538-7305.1924.tb01358.x](https://doi.org/10.1002/j.1538-7305.1924.tb01358.x), gives the general finite lossless driving-point reactance and says that any such reactance can be physically realized by a parallel collection of series LC resonators or a series collection of parallel LC resonators; the paper says its proof uses the analogous frictionless small-oscillation problem. The [primary publisher abstract](https://onlinelibrary.wiley.com/doi/abs/10.1002/j.1538-7305.1924.tb01358.x) is accessible; its linked full text was unavailable in the page view.

For the proposed mechanical realization the direct correspondence is visible without relying on a modern restatement of Foster: set \(Z(s)=sR(s^2)\). Then
\[
Z(s)=m s+\sum_j\frac{k_j s}{s^2+\nu_j^2},
\]
which is the driving-point impedance form of a backbone inertance plus parallel branch contributions from spring-coupled side masses \(M_j=k_j/\nu_j^2\). The endpoint-to-positive-residue argument is a concise way to *construct* that Foster-type star from a desired interlacing list. Foster's result makes clear that positive rational resonator synthesis itself should not be presented as new.

## What these priors do not establish

Neither source treats the Bose/Planck-weighted ballistic thermal-conductance objective. The inverse-eigenvalue source concerns finite-system Jacobi spectra and their modification; Foster concerns a passive one-port reactance. They do not, on the material inspected, prove the two exact bulk passband moments for \(D(q)=D_0+4K\sin^2(q/2)vv^{\mathsf T}\), the sign-minimizing Bose dual, or its globally optimal one-resonator spectrum under fixed \(M,K\). Conversely, these bounded sources are not enough to claim the Bose-weighted theorem or open resource family is new. The defensible positioning is: classical interlacing and Foster synthesis are established ingredients; the candidate's possible contribution is their explicit application to the complete bulk-passband set together with the Bose-weighted global optimum and open two-parameter family. Priority and complete coverage of later literature remain UNKNOWN.

## Final challenge after the universal-family claim

The strengthened claim now under review is that, for every finite positive temperature, backbone spring constant, and total mass above the backbone lower bound, one finite one-side-resonator cell is the unique global minimizer of the full Bose conductance over every finite positive internal network and admissible backbone allocation. A bounded targeted primary search for a theorem with that same periodic scalar harmonic class, fixed total mass and backbone stiffness, and an all-network global Bose-weighted comparison did not surface a direct antecedent. This is a search result, not evidence of absence or a novelty determination.

The closest exact-source boundaries remain: (i) Nylen–Uhlig's 1997 finite Jacobi/spring-mass inverse two-spectrum theorem, with a related rank-one modification theorem whose exact matrix hypothesis is not available in the publisher abstract; and (ii) the separate acoustic sum-rule paper recorded above, whose observable and objective differ. The ordinary resonator-engineering and thermal-conductance calculations already catalogued in [`PHONON_SOURCES.md`](../../physical_opportunity/sources_support/PHONON_SOURCES.md) are examples/comparators, not the claimed universal minimax theorem.

For a stronger check of the old synthesis ingredient, a primary-search-indexed scan of Foster's original paper gives the theorem's form: the finite lossless-network driving-point impedance is an odd rational function, fixed up to a positive scale by alternating resonant/antiresonant frequencies including zero and infinity; the same passage gives its realization by parallel series-LC or series parallel-LC branches. See the [indexed original scan](https://www.worldradiohistory.com/Archive-Bell-System-Technical-Journal/20s/Bell-1924b.o.pdf), p. 267, and the [Wiley primary record](https://onlinelibrary.wiley.com/doi/abs/10.1002/j.1538-7305.1924.tb01358.x). The ordinary PDF open returned 403, so the original's full pages were not independently acquired or visually inspected. Even at that access limit, the abstract plus indexed theorem statement is enough to treat finite Foster synthesis as established; it is not evidence that Foster proved a Bose-weighted optimum.

**Bounded conclusion:** old inverse-spectrum/Foster synthesis is not a defensible novelty claim. No inspected primary theorem directly subsumes the universal finite-temperature Bose optimum; the strongest source-backed status for that part remains “no direct match found in this bounded check; priority UNKNOWN.”
