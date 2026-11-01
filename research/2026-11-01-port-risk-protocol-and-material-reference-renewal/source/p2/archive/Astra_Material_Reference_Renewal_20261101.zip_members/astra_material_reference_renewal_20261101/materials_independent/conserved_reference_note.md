# Conserved or quantized reference: focused challenge

**Verdict:** A representation change can eliminate the specific repeated analog-copy random walk. It does not eliminate inventory-transfer faults or the uncertainty of converting the invariant back into length. The strongest conventional route is a protected integer register plus a freshly realized physical pitch. A closed hydraulic inventory is a useful physical alternative but conserves mass, not geometry.

## Exact distinction

Replace the recursively copied analog state by

\[
Q_{j+1}=Q_j+\delta q_j,\qquad R_j=g(Q_j,\theta_j)+\epsilon_j,
\]

where Q is a conserved inventory or corrected discrete value and theta contains the transducer's current material, temperature, pressure and calibration state. If delta q is exactly zero and theta/epsilon have a bounded stationary distribution, the output error has a bounded floor instead of accumulating the previous cycle's analog error. Linearizing gives

\[
\operatorname{Var}(R_M)\simeq g_Q^2 M\sigma_{transfer}^2+
\operatorname{Var}(g_\theta\delta\theta_M+\epsilon_M).
\]

A systematic inventory loss b produces a bias proportional to M b. If theta itself is maintained only by analog copying, the random walk has merely moved into theta.

## Strongest conventional construction

Quantize the original scalar as N=round(R0/a0), store N in a finite error-corrected integer memory, and manufacture or position the new member using N periods of a newly realized crystalline or interferometric pitch. During replacement, decode the integer, verify the replacement copy, and then retire the old copy. All storage components can turn over; no single geometric artifact must survive. The initial quantization cost is at most a0/2. The memory, majority/decoding apparatus, readout, verification, and energy are real parts, not free helpers.

Conditional on correct logical transfer,

\[
R_M=N a_M+\epsilon_M,
\quad
R_M-R_0=(N a_0-R_0)+N(a_M-a_0)+\epsilon_M.
\]

There is no inherited M sigma_copy^2 term. The remaining error is quantization, current pitch calibration and current setting error. Logical count slips reintroduce a rare failure channel: for independent per-turnover logical error probability p, probability of at least one error is at most M p. A simple uncorrected plus/minus-one count error yields a contribution of order M p a0^2. This is the familiar digital-regeneration improvement, not exact immortality.

A physical fixed-monomer or segment-count register substitutes a retained particle/bond inventory for digital memory, but must preserve the relevant chain/axis count, not merely the total number of particles in a three-dimensional body. Total atom number does not specify shape, sequence or lattice-plane count in each direction. An integer invariant can remain constant while conformation, strain, dislocations or orientation change. If actual tokens are retained, the enduring inventory must be openly counted as the reference carrier. If tokens also turn over, one-for-one exchange or verified count transfer must be physically supplied.

The crystalline unit is not a free precision helper. The BIPM's 2026 metre realization explicitly permits silicon lattice spacing as a secondary realization and requires accounting for impurities, temperature, pressure and motion-system errors. A NIST research study reports thermal and pressure corrections and variability associated with impurities and defects. These sources establish the conventional unit-realization route while also showing why it has a finite metrology budget. [1,2]

## Hydraulic realization and its exact limitation

Keep a reference fluid inventory in connected bellows or vessels and replace vessels by overlapping connection and physical transfer. This avoids measuring an old analog amount and synthesizing a noisy replacement amount. With reference fluid mass m,

\[
R=\frac{m}{\rho(T,p,c)A},
\qquad
\frac{\delta R}{R}=\frac{\delta m}{m}-\frac{\delta\rho}{\rho}-\frac{\delta A}{A}.
\]

Mass conservation is genuine, subject to inventory boundaries; volume and length are not fundamental conserved quantities. A finite-error implementation pays for leakage, permeation, fluid left in discarded dead volume or wetting films, evaporation, bubbles, changing composition, thermal expansion, compressibility, cylinder-area calibration and pressure deformation. Replacing every vessel does not remove these terms. A permanently sealed catch vessel would count as retained infrastructure, not an unexplained perfect helper.

Piston metrology actually models effective area and its pressure distortion from measured geometry and elasticity. Thus treating equal fluid volumes as equal piston strokes across replacements assumes a transducer calibration that needs its own budget. [3]

## Why paired updates alone are insufficient

If actual physical updates obey delta r1 + delta r2 = 0, their sum is indeed invariant. But two commanded opposite strokes give delta r1 + delta r2 = eta_j whenever pitch, gain, compliance, backlash or transfer differ. Then the sum executes the same random walk. A differential or rigid constraint fixes the sum relative to its carrier; a closed hydraulic link fixes a fluid balance subject to its state equation. The apparatus that enforces the equality cannot be omitted when it is replaced.

**Recommendation:** Accept a conserved/quantized reference as a valid way to defeat the particular analog-copy term. State a finite lifetime and split the error budget into invariant-transfer failures and current metric-realization error. Do not claim absolute geometric preservation from conserved mass or count alone. If only dimensionless shape ratios matter, common pitch drift can cancel, R_i/R_j=N_i/N_j; an absolute scale still needs a physical unit.

## Primary sources

1. BIPM, *Mise en pratique for the definition of the metre*, Appendix 2, version 1.2, 19 June 2026. https://www.bipm.org/documents/20126/41489670/SI-App2-metre.pdf/0e011055-9736-d293-5e56-b8b1b267fd68 . Current version and relevant content confirmed by root retrieval, browser refs turn138view0 / turn139view0; supersedes the earlier branch retrieval's version metadata.
2. *The Lattice Spacing Variability of Intrinsic Float-Zone Silicon*, Journal of Research of NIST 122, Article 24 (2017), DOI10.6028/jres.122.024. https://nvlpubs.nist.gov/nistpubs/jres/122/jres.122.024.pdf . Browser ref turn137view1.
3. *Conversion of a piston–cylinder dimensional dataset to the effective area of a mechanical pressure generator*, Metrologia (2024), DOI10.1088/1681-7575/ad77db. https://pmc.ncbi.nlm.nih.gov/articles/PMC11494611/ . Browser ref turn137view2.
