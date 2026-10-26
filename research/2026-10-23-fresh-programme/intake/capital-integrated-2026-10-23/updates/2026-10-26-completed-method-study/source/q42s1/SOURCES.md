# Exact primary sources and the claims they do and do not supply

Read on 2026-10-26. No Astra archive was preloaded or needed. Searches were
direct public web retrieval; no paid research service or model API was used.
The mathematical proof and local calculations in this folder are not source
measurements.

1. Florian Dorfler and Francesco Bullo, *Kron Reduction of Graphs with
   Applications to Electrical Networks*, arXiv:1102.2950, subsequently IEEE
   Transactions on Circuits and Systems I 60, 150-163 (2013).
   Primary preprint: https://arxiv.org/abs/1102.2950 .
   DOI: https://doi.org/10.1109/TCSI.2012.2215780 .
   This establishes the static Schur-complement graph operation used as the
   incumbent. Kron reduction is not an invention in this trial. The abstract
   and primary metadata were inspected; the static formula is also derived
   directly in PROOF.md.

2. Jiaxin Li et al., *Reciprocity of thermal diffusion in time-modulated
   systems*, Nature Communications 13, 167 (2022).
   https://doi.org/10.1038/s41467-021-27903-3 .
   Exact preprint version: https://arxiv.org/abs/2103.11164v1 .
   The primary abstract and indexed article text were inspected. It stresses
   conservation-law problems when density/capacity modulation is treated as a
   free material parameter. This trial does not vary capacity or density, and
   does not assert that a physical actuator implementing the ideal contacts is
   free. The paper's broad introductory wording is not taken as a theorem
   forbidding every externally switched multi-terminal lumped network.

3. Ying Li et al., *Diffusive non-reciprocity and thermal diode*, Physical
   Review B 103, 014307 (2021).
   https://doi.org/10.1103/PhysRevB.103.014307 .
   Version inspected: https://arxiv.org/abs/1912.10252v3 .
   The primary abstract distinguishes internal Green-function reciprocity,
   terminal reciprocity and diode operation. In this trial, the measured
   mathematical object is a period-averaged three-or-more-terminal admittance.
   It is not a two-terminal heat diode.

4. Ran Ju et al., *Nonreciprocal Heat Circulation Metadevices*, Advanced
   Materials 36, e2309835 (2024; online 2023).
   https://doi.org/10.1002/adma.202309835 .
   Primary journal abstract indexed at https://pubmed.ncbi.nlm.nih.gov/38010625/ .
   It reports a convection-based three-port device and experimental thermal
   circulation. Thus thermal circulation itself is established and cannot be
   claimed as the invention here. Its abstract does not provide a matched
   quantitative actuator/resource budget for the present contact model. No
   performance superiority over that physical device is claimed.

5. Jiaxin Li, *Diffusive circulation via spatiotemporal modulation*,
   International Journal of Heat and Mass Transfer 260, 128474 (2026).
   https://doi.org/10.1016/j.ijheatmasstransfer.2026.128474 .
   Primary publisher abstract inspected at
   https://www.sciencedirect.com/science/article/pii/S001793102600150X .
   It proposes circulation by traveling modulation of conductivity and capacity
   without material motion. The full article was not accessible in this run;
   no uninspected equations or experimental implementation are inferred.
   This independently establishes close prior art for the broad operation.

6. Morgan Almanza, Lucas Depreux, Fabien Parrain and Martino Lobue,
   *Electrostatically actuated thermal switch device for caloric film*,
   Applied Physics Letters 112, 083901 (2018).
   https://doi.org/10.1063/1.5009618 .
   Authors' laboratory record inspected:
   https://satie.ens-paris-saclay.fr/fr/publications/electrostatically-actuated-thermal-switch-device-caloric-film .
   Author manuscript identifier: https://hal.science/hal-01706363 .
   The laboratory abstract reports deduced on/off conductance ratio 1000 from
   measurements and a diffusion model. This motivates the **sensitivity value**
   g_off/g_on=.001. It does not validate three independently switched contacts
   on one constant-capacity body. The refrigeration performance in that abstract
   is a finite-time model estimate, not a measured refrigerator demonstration.
   No switching energy, latency, extra heat capacity or endurance value is
   imported without evidence. HAL's document endpoint was access-denied.

7. Siyi Deng et al., *Autonomous Thermal Switching Outperforms the Frozen
   Optimum with Vanishing Correlations*, arXiv:2610.24589v1 (2026).
   Primary full HTML inspected:
   https://arxiv.org/html/2610.24589v1 .
   This preprint studies autonomous reversible Markov relaxation at fixed
   barrier-lowering budget, with rates exponential in lowerings. Its admissible
   frozen set need not contain the averaged conductance vector, and its
   objective is a spectral relaxation gap. It explicitly exploits this resource
   distinction. It is not contradicted by the convex-contact, constant-terminal
   DC comparison proved here, and it prevents conflating mean conductance with
   mean barrier budget.

8. The primary circuit paper *A Generalized Model for
   Linear-Periodically-Time-Variant Circulators*, Scientific Reports (2019),
   https://doi.org/10.1038/s41598-019-45013-5 , was inspected through indexed
   publisher text. Sequential switching and other time-varying circulator
   architectures are established in circuits. The electrical analogy alone
   does not supply a compatible thermal implementation.

## Novelty boundary

The search included heat-contact switching, thermal shuttles, diffusive
circulation, time-periodic resistor networks, variational effective conductivity
and periodic Dirichlet-to-Neumann maps. It found strong prior art for the
operation and standard static network mathematics. It did not establish whether
the exact identities (3)-(6) or finite-leakage n-port formula, in this precise
form, already appear in the circuit/homogenization literature. Their correctness
is addressed by proof; their novelty remains unestablished. A missing keyword
match is not evidence of novelty.
