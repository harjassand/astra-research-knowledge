# Bounded prior-art audit: Ganesh, Pillai & Narayanan (2022)

**Scope and access.** This is a source audit of Ganesh, Pillai & Narayanan, “Effect of low-frequency AC forcing on the morphological instability arising in electrodeposition,” *Journal of Engineering Mathematics* 132:16 (2022), DOI [10.1007/s10665-021-10199-z](https://doi.org/10.1007/s10665-021-10199-z). I tried the supplied primary manuscript endpoint, [NSF PAR PURL 10350049](https://par.nsf.gov/servlets/purl/10350049), and the DOI landing page with the native web reader; the PURL timed out and the publisher page could not be opened. I did not download another copy or use a secondary text service. Targeted searches against the NSF-hosted manuscript index returned substantial excerpts from the paper, including its abstract and passages identified as pages 3, 11, and 15. The findings below are limited to those exposed passages; the failed opens are not evidence about material omitted from the index.

## Forcing and flux normalization

The paper is explicitly **voltage-driven**. Its stated input is a small AC term of the form

\[
V(t)=V_0+\delta\cos(\Omega t),
\]

added to a constant DC voltage (the abstract denotes the base voltage by \(\Delta V\); the results use \(V_0\)). Thus \(\delta\) is the cosine coefficient, i.e. peak amplitude in this convention. The AC voltage has zero time mean, but the paper does not prescribe a sinusoidal Cu partial current or impose an unchanged mean deposition flux. Instead, it studies how the voltage perturbation changes the growth-rate-versus-wavenumber stability curve.

This distinction is visible in the paper's own expansion: the base electrode speed is written \(U=U_0+\delta U_1+\tfrac{1}{2}\delta^2 U_2\). Here \(U_2\) is the second-order correction (the second derivative coefficient in that expansion). The results passage says the time-averaged first-order correction vanishes, while the time-averaged second-order base-speed correction is central; depending on the curvature of the base \(U_0\)-versus-\(V_0\) relation, \(U_2\) can be negative throughout or can change sign. Hence zero-mean **voltage** forcing does not amount to retained mean electrode speed/flux. The indexed passages show no re-tuning of the DC voltage to compare cases at equal mean Cu partial flux, and no matched-retained-flux result. I phrase this as “none supplied in the inspected analysis,” not as a claim about unindexed portions of the full paper.

## Low-frequency assumption and result

The exposed results passage says the computed corrections at each order were independent of \(\Omega\), and attributes that to the assumption \(\Omega<1\): domain dynamics are assumed slaved to interface dynamics and in phase with the interface periodicity. This is a dimensionless low-frequency condition in the model passage; the indexed text supplies no dimensional frequency in hertz or mapping to a particular Cu bath/geometry. The paper reports the AC effect first at order \(\delta^2\), consistent with the zero mean of the cosine and the time-independent component of \(\cos^2(\Omega t)\). The reported stability effect depends on the base-speed-versus-DC-voltage curvature and a dimensionless parameter distinguishing diffusion-limited from reaction-kinetics-influenced regimes.

The abstract and exposed results therefore establish theoretical prior art for periodic small-amplitude voltage forcing changing morphological linear stability, including a stabilizing branch. They do not, in the inspected text, establish equal-mean-metal-flux stabilization for Cu/CuSO\(_4\) under galvanostatic control.

## Relation to the present comparator

The comparator under audit prescribes a positive sinusoidal **Cu partial flux** with unchanged mean on a fixed film and evaluates a frequency-dependent lateral Dirichlet-to-Neumann response. The 2022 paper instead adds a cosine **voltage** to a DC bias, allows the mean base speed to receive a second-order correction, treats a moving electrode base state, and—under its \(\Omega<1\) assumption—reports frequency-independent perturbative corrections. These are real modeling differences, but a change of controller alone is not a novelty argument: the shared broad phenomenon, periodic forcing affecting instability, is prior art. Any distinct claim must rest on the specific equal-mean-flux constraint and the resolved frequency-dependent response, and should be bounded to those model features unless separately validated.

## Provenance record

- Primary indexed source used for the claims above: [NSF PAR manuscript PURL](https://par.nsf.gov/servlets/purl/10350049), search-index excerpts from pages 3, 11, and 15, retrieved 24 October 2026.
- Direct reader access to that PURL: timed out. DOI landing page: unavailable to the reader. No claim is made that the whole manuscript was read.
- No new experiment protocol, source survey, or physical validation is supplied by this audit.
