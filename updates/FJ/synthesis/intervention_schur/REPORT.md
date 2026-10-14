# Shunt-intervention Schur certificate for hidden fluid–electrical mediation

**Status:** a scoped mathematical result and an experiment-design candidate, not a demonstrated device or a novelty claim. The formula is a direct consequence of the Sherman–Morrison identity. The useful contribution here is its exact input/output interpretation for the supplied hydraulic–electrical composition, its identifiability boundary, its noise conditioning, and a falsifiable control protocol. Historical priority for this exact operational package is **UNKNOWN**.

## Strongest task selected

The physical source already supplies a reciprocal wet-interface law and eliminates electrical variables by a Schur complement. It also names changing electrical loading as a consequential check, while emphasizing that the wet work-conversion coefficient is still unmeasured. I derive a load-intervention protocol that can isolate the electrically mediated part of the measured hydraulic multiport response without separately reconstructing the hidden circuit or wet-interface matrices.

The operation is: hold the wet specimen and hydraulic apparatus fixed; measure the steady small-signal hydraulic response matrix $H(0)$; add a calibrated, passive electrical shunt $tuu^T$ along one exposed electrical direction $u$; measure $H(t)$ at two distinct positive shunt strengths. The difference cancels every shunt-invariant direct hydraulic response. If the linear reciprocal wet-interface model is valid, then

\[
\Delta H(t):=H(t)-H(0)=\frac{t}{1+tq}\,F,
\qquad F=vw^T,
\]

where $q=u^T(G+Y)^{-1}u>0$, $v=C(G+Y)^{-1}u$, and $w=C(G+Y)^{-T}u$. Thus a one-direction electrical intervention produces a rank-at-most-one hydraulic signature, even when the electrical mediator is nonreciprocal. If the signature is nonzero, two distinct shunt levels identify $q$ and the full matrix $F$, but leave the hidden factors $v,w$ and the circuit itself unidentified. A third, held-out shunt level gives a direct fractional-law falsifier.

This is a mechanism-specific commissioning test for the source's proposed remote, chemically isolated fluidic interconnection. In particular, with an invariant reciprocal wet law, a nonzero change in the antisymmetric part of $H$ certifies that the shunt-controlled electrical path contributes visible nonreciprocal hydraulic response. If the wet law is unchanged by magnetic-field reversal and $Y(-B)=Y(B)^T$, then the intervention fingerprint transposes, $F(-B)=F(B)^T$, and $\Delta H(-B,t)=\Delta H(B,t)^T$. It does not identify quantum friction or any other microscopic mechanism.

## Main result and limits

The exact theorem, necessity counterexamples, finite-noise bounds, and acquisition contract are in [PROOF.md](PROOF.md). An exact-arithmetic verifier and output are in [verify_schur_intervention.py](verify_schur_intervention.py) and [verification.log](verification.log).

The result is useful only when the following experimental conditions are met: (i) the electrical load is physically isolated from the liquid and is accurately set; (ii) changing the load does not change the wet matrices $K,C,G$, temperature, gate, geometry, or hydraulic boundary conditions; (iii) the same steady, near-equilibrium linear regime is acquired at each load; (iv) all relevant hydraulic input directions are excited and all outputs measured; and (v) the response errors and correlations are bounded. A shunt-dependent thermal, electrostatic, vibrational, or chemical change can counterfeit the differential response. The exact theorem does not certify those controls.

There is no generic acquisition advantage over full component calibration: for $n_h$ hydraulic ports, a complete $H(t)$ requires $n_h$ independent pressure patterns per load condition. The intervention method asks for fewer kinds of hidden quantities, not automatically fewer measurements or less energy. Under the explicit independent-Gaussian trial model in PROOF.md, a conservative confidence budget is given as a function of sensor noise, pressure amplitude, requested matrix error, number of ports, and error probability. Physical run time, pump work, shunt switching, thermal control, field generation, calibration, reset, and instrumentation remain additional costs; no values were measured here.

## Why this is the strongest consequential use

The producer's own physical source says to test electrical loading and distinguish a flow sensor from a work-transmitting interface, but its current model test first measures $K,C,G,Y$ separately and predicts the assembly response. The differential protocol is complementary: it can show that an electrically controlled pathway actually changes a complete hydraulic response in situ while cancelling a fixed direct hydraulic background. This is a sharper causal falsifier than seeing receiver motion or voltage alone, and it does not assume access to the hidden circuit internals. It is not a substitute for the source's prior wet-device reciprocity gate or its full energy and efficiency accounting.

I rejected composition with two apparently related information routes. Capital N713 intervenes on microscopic CTMC transition rates and uses observed stationary path responses to identify a hidden lumpability residual; its action, state, response object, and kinetic calibration are different from an electrical shunt acting on a steady admittance. N804/N801 recover a finite binary model's kinetic clocks through context-preserving downhill-rate queries and use those to certify a complete-source lifetime; those data are not hydraulic multiport responses. The supplied nonlinear PDE sampler requires a verified forward model and pointwise residual access, while the quartic contact work requires compatible gradient fields and Hessian/cubic quantities; neither source supplies a shunt intervention or the port law above. No transfer is claimed.

## Prior art and novelty boundary

The Schur elimination is standard Kron reduction. Dörfler and Bullo describe eliminating interior nodes while preserving terminal behavior by a Schur complement, with applications including electrical impedance tomography (network tomography) ([2013 paper](https://doi.org/10.1109/TCSI.2012.2215780); [open arXiv version](https://arxiv.org/abs/1102.2950)). The single-shunt update is the Sherman–Morrison/Woodbury identity, not a new matrix identity. Boundary-response inverse problems can sometimes recover internal conductances under strong graph assumptions: Curtis, Ingerman, and Morrow prove recovery for critical circular-planar resistor networks ([1998 paper](https://doi.org/10.1016/S0024-3795(98)10087-3)). Classical realization theory reconstructs minimal controllable/observable dynamical realizations from input/output data, up to coordinate transformations; see Ho–Kalman ([1966 DOI](https://doi.org/10.1524/auto.1966.14.112.545)) and Kalman ([1963 paper](https://people.duke.edu/~hpgavin/SystemID/References/Kalman-JSIAM-1963.pdf)).

Causal mediation theory already defines direct and path-specific effects and establishes identification under assumptions such as sequential ignorability; Pearl's path-specific framework and Imai, Keele, and Tingley's counterfactual formulation are direct causal prior art ([Pearl, “Direct and Indirect Effects”](https://arxiv.org/abs/1301.2300); [Imai et al., “A General Approach to Causal Mediation Analysis”](https://doi.org/10.1037/a0020761)). This proposal does not estimate natural or population mediation effects from mediator/outcome distributions. It applies a calibrated intervention to a physical mediator network and uses a mechanistic multiport identity to identify a restricted, intervention-accessible response fingerprint. Its causal reading still depends on the no-direct-effect and invariant-wet-law controls; the algebra alone cannot certify them.

Those works establish close mathematical neighbors and block any claim that Schur elimination, low-rank updates, hidden-mode visibility, or input/output realization are new. The scoped distinction is only the proposed use of a calibrated electrical-only shunt as a paired intervention in the source's reciprocal hydraulic–electronic multiport: it yields an in-situ, load-invariant-background-canceling mediation witness and, with two levels, a partial quotient $(q,F)$. I did not find a primary paper in the targeted searches that establishes this exact coupled-fluidic operational package; that limited search is not priority clearance. Novelty and practical significance remain **UNKNOWN**.

## Decisive experiment

First satisfy the source's separate wet-interface gate by measuring both cross-coefficients at zero electrical bias in the same steady, near-equilibrium regime and bounding leakage, thermal gradients, electrode chemistry, vibration, and displacement current. Then, on the same assembled device and without changing hydraulic boundary conditions, acquire the complete hydraulic response for baseline plus three calibrated passive electrical shunts ($0<t_1<t_2<t_3$) along one known terminal direction. Use $t_1,t_2$ to estimate $(q,F)$; reserve $t_3$ to test the predicted scale factor and rank-one matrix shape. Repeat at reversed magnetic field, with the electrical path open, and with a reciprocal substitute. Measure all hydraulic and electrical powers and temperature channels throughout.

Pass at the bounded model scope requires: each measured $\Delta H$ is rank one within the predeclared noise budget; all $\Delta H(t_i)$ share a common rank-one direction; the estimated $q$ is positive and the third-load prediction lies inside its propagated interval; and any claimed nonreciprocal shunt-mediated transfer has a differential skew signal above calibrated uncertainty that obeys $\Delta H(-B,t)=\Delta H(B,t)^T$ under magnetic-field reversal when the wet law is field invariant. A result below the skew-detection threshold is inconclusive about path reciprocity. Failure rejects this particular linear, load-invariant composition or its claimed accessible path; it does not refute liquid–electron coupling generally. A pass certifies only the acquired effective multiport law, not microscopic origin, useful efficiency, scale-up, or technology readiness.

## Scope ledger

| Item | Result |
|---|---|
| Unknowns identified from baseline + two shunt levels | $q=u^T(G+Y)^{-1}u$ and $F=[C(G+Y)^{-1}u][C(G+Y)^{-T}u]^T$, if $F\ne0$ |
| Hidden quantities not identified | $K,C,G,Y$, internal topology, the individual factors of $F$, and modes invisible to the chosen shunt/ports |
| Necessary intervention for this target | Baseline plus two distinct positive shunt strengths; one active level cannot separate $q$ from $F$ |
| Model falsifier | Rank greater than one, non-collinear changes across load strengths, nonpositive inferred $q$, or held-out-load prediction outside its uncertainty interval |
| Conditioning | Vanishes with weak interface coupling; $q$ inversion becomes ill-conditioned when both shunts greatly exceed $1/q$ or are too close |
| Physical status | No measurements, material coefficients, actual shunt calibration, or device run were acquired |
| Priority / broad technological significance | UNKNOWN |

