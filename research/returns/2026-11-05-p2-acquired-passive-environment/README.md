# Acquiring a finite-horizon predictor of an unknown positive relaxation environment

The supplied construction joins finite noisy mechanical observations, positive-kernel fitting, retained-state initialization, finite release and an actual residual-certified numerical trajectory. It allows unknown hidden dimension, arbitrarily slow/fast rates and frozen modes **within a declared scalar positive relaxation class**. It does not infer that class from short observations or establish an economical acquisition advantage.

Read the complete [report](package/acquired_passive_environment.md), [16-page PDF](package/acquired_passive_environment.pdf), [full acquisition proof](package/forward/passive_FULL_PROOF.md), [finite-release proof](package/forward/RELEASE_HANDOFF.md), [join review](package/backward/JOIN_REVIEW.md), [model/execution and cost page](model-and-execution.md), and [independent constructions](alternative-constructions.md). The [original ZIP](original/acquired_passive_environment_research_package.zip), [complete captured return](P2_ACQUIRED_PASSIVE_ENVIRONMENT_20261105_RETURN.txt) and [source metadata](SOURCES.json) preserve all supplied material.

The capture records that the download was unavailable when collected; the ZIP subsequently appeared and is included unchanged. The full accessibility rendering/activity and truncated native prefix remain verbatim. No absent native text is reconstructed.

## Physical class and acquired operation

The observed coordinate obeys

```text
x'=-V'(x)-integral(x-y_lambda)nu(dlambda)+f,
y_lambda'=lambda(x-y_lambda),
K(t)=integral exp(-lambda t)nu(dlambda).
```

V is known with V' strongly monotone by mu>0; nu is a positive measure of mass at most B and hidden initial elastic energy is bounded by E0. Local drag is calibrated to one, and finite evaluation/variation bounds for V' are supplied. No mode count, positive rate floor, rate ceiling or finite rate moment is assumed. Maxwell branches realize positive rates; a zero-rate branch is a spring to a fixed possibly displaced anchor.

The experiment uses a calibrated moving trap, finite position/force averages and declared meter noise/bias. Trap position, speed, acceleration, force, timing and readout range are paid. Deployment additionally needs stiffness to reach zero with finite slew and an **independently movable local viscous support** delivering the later force. Those capabilities do not follow from merely having a moving trap. The hidden modes and visible potential retain their laboratory frame.

For the actual emitted path q, the acquired kernel L1 error zeta, retained-force uncertainty gamma, post-release coordinate error delta_in, complete numerical residual rho and delivered-force error xi_f give

```text
||x-q||_infinity,[0,T] <= max{delta_in,
 (zeta||q'||_infinity+gamma+||rho||_infinity+xi_f)/mu}.
```

A positive Volterra maximum principle provides stability without an exponentially growing generic perturbation bound. One successful calibration/initialization event supports every later admissible force programme on the chosen horizon, including queries chosen after calibration. Repeated counterfactual calculations do not consume fresh confidence; repeated **physical** trials would need a separately supplied reset/preparation. General discontinuous feedback is not granted; the stated small-gain/Lipschitz extension has its own premises.

## Reports, retained force and release

A smooth finite ramp plus triangular finite-time readout estimates a filtered positive kernel K*. Two position-box averages supply the integrated derivative; no specimen-velocity oracle or differentiation of noisy point measurements is used. White meter-noise variance includes `2v_f/(3w)+2v_x/w^3`, so narrow windows can be costly. Positivity preserves the kernel class and gives `||K-K*||_L1<=B(h/2+w)`, directly paying unresolved fast modes without deconvolution.

A bounded observed history gives an old-force envelope G. Its derivative is bounded by `G/(e t)` at positive age. A quiet hold and final finite force measurement therefore estimate the surviving force as a constant over the forecast. Frozen modes need not decay; their remaining force is retained. Long-hold cost for this strategy and an alternative using aged measurements/greater precision are explicit.

Finite trap release contributes coordinate and old-force errors; ramp regularity/slew, support startup acceleration, travel, reaction force and work are charged. The [release proof](package/forward/RELEASE_HANDOFF.md) distinguishes the hidden-state envelope at the start of the hold from that at release, and keeps the actual actuator assumptions. The [join review](package/backward/JOIN_REVIEW.md) credits the scalar join at its reviewed version and states fixture adapter/receipt limits.

Unknown oscillatory/active/nonlinear hidden branches, uncertain drag, general matrix-valued kernels, nonconvex instabilities and thermal stochastic path laws are not covered automatically. The same-scalar isotropic vector corollary requires full transverse trapping, rather than identifying an arbitrary matrix bath through one port. Existing exponential approximation/GLE methods and the accepted retained-device thermal simulator remain credited at their different interfaces. No scientific programme, solver, experiment, new audit or large retrieval build ran for publication.
