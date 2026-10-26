# Q17 stage 1 research notes

Started 2026-10-26 08:26 UTC. Read only the own-trial assignment and public starting evidence locally. No Astra archive retrieval was needed. This record preserves route development rather than presenting a retrospectively predetermined success.

## Initial question and first attempt

Can passive ordinary heat conductors and heat capacities implement a sharply timed heat-pulse release, without a powered switch or a selective detector/actuator? This could matter for passive thermal sequencing and time-domain heat routing. A useful operation must release a substantial fraction of the initially stored energy; a delayed tiny temperature feature is insufficient.

The first construction was an equal-rate one-way cascade. Such a cascade has an Erlang release density and CV squared 1/n, but thermal conductance is reciprocal. Treating its one-way transfers as free would supply the missing operation by assumption. Moreover, the phase-type optimum 1/n is established by Aldous and Shepp (1987), DOI 10.1080/15326348708807067, accessible primary manuscript https://escholarship.org/content/qt7w51x4rb/qt7w51x4rb.pdf . This is not an invention.

## Stronger compatible route

Replace the one-way cascade with a reciprocal Cauer thermal ladder, using positive conductances and positive heat capacities, with all initial energy in its first lump and one final sink at fixed bath temperature. Its normalized output flux is mathematically an absorption-time density. Node energy, not temperature, gives the Markov probability coordinates.

Candidate discovery: the exact minimum pulse CV squared at fixed node count n, initial heat capacity C1, total heat capacity R*C1, and mean release time is

    [1+(n-1)*tanh(log(R)/(2(n-1)))]^(-1).

The extremizer has geometrically spaced cumulative heat capacities. Ordinary optimization may obtain the same optimum; any claim of an algorithmic advantage must be rejected if so. The potentially useful object is the governing sharp resource law, not beating an artificially weak uniform ladder.

For a ladder, the variance quadratic form appears to be K_ij=min(S_i,S_j)/max(S_i,S_j), with S cumulative capacities and variables a_i=r_i*S_i. The inverse exponential kernel makes the optimization solvable. Need independently verify against matrix moments and prove extension to trees by collapsing off-path branches, which adds nonnegative variance at fixed mean.

## Primary prior-art checks

* Stout and Billings, onsemi AND8218/D (April 2006): experimentally calibrated thermal RC networks and Cauer refinement, https://www.onsemi.com/pub/Collateral/AND8218-D.PDF . Supports the ordinary modeling operations, not a demonstrated device here.
* Chiclana, arXiv:2605.17513v1 (17 May 2026), https://arxiv.org/html/2605.17513v1 . Appendix A gives a reversible-chain hitting-time variance bound depending on effective resistance and terminal conductance. Closely adjacent and must be compared directly. Its published inequality is not the same as the proposed heat-capacity-constrained finite-node optimum. No novelty inference is warranted from keyword absence.
* Dutta Roy and Sah (1971), DOI 10.1016/0026-2714(71)90302-7, https://www.sciencedirect.com/science/article/pii/0026271471903027 . Existing RC delay-line work includes active compensation; not a free passive thermal primitive.

All later numerical evidence will be local simulation, not measured heat transport. No fabricated material, no equipment operation, no externally published result.

## Construction and stress outcome

The exact ladder formula agrees with independent backward matrix moments. The inverse exponential kernel gives an attaining design with all positive capacities/resistances. The branch-collapse second-moment identity supplies a full tree extension, now proved in PROOF.md. A subsequent full-graph numerical search converged to near-path optima, but no proof for loops was found; it remains open in this result.

The continuum limit is a source reservoir plus exponential-area Fourier conductor and two contact resistances. Primary RC/RLC delay synthesis and exponential shaping antecedents were found (Kandic et al. 2013; El-Moursy and Friedman 2007), so the geometry and moment method are not claimed novel. Priority of the sharp finite heat-capacity-ratio/tree optimum remains unresolved.

The ordinary multistart optimizer matches the construction to numerical tolerance. This eliminates any observed performance advantage over ordinary RC design while leaving the proposed governing theorem as the substantive mathematical object. The law proves exponential capacity demand for low RMS width within its actual class.

An out-of-class switch route was considered after this blocker. Primary work already demonstrates mechanical heat pulses, passive bimetal regulators, and active counter-flow release. A source-supported operation is available in those architectures, but no calibrated whole passive timer/storage integration was constructed here. Assuming a free independently clocked instantaneous thermal gate would not complete the missing bridge. No ideal switch simulation is offered as a physical invention.

An initial code run failed JSON serialization because randomly generated tree labels were NumPy int64; labels were explicitly converted to Python int. The bundled BLAS also emitted floating-point status warnings during tiny matmul contractions despite finite, mutually consistent results. The kernel check now uses an explicit elementwise contraction, reran cleanly, and all independent identities agree to about 1e-13. These implementation fixes are not scientific validation by themselves.

The continuum transform was independently checked against tridiagonal finite-network solves at six real/complex frequencies, converging over 8,32,128,512 nodes and four resource ratios. A plotted comparison visually confirms the overlap between analytic and ordinary optimized designs. No unsupported physical advantage was promoted.
