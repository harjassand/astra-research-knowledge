# Thermal ordering, work and physical scope

[Return guide](README.md) · [Main proof](package/invention_variation/proof_and_claim_boundary.txt) · [Resource deductions](package/invention_root/resource_deductions.txt) · [Measured-source audit](package/invention_root/source_audit.txt)

## A composable covariance ordering

For a deterministic response `F`, added covariance `Q`, and `m=D/Lambda`, define `E=Q-m(I-FF^T)`. The ordinary Gaussian evolution equations yield

```
E = (2D/Lambda) integral Phi(T,t)(Lambda I-A(t))Phi(T,t)^T dt >= 0
E_21 = E_2 + F_2 E_1 F_2^T.
```

Maximum isotropic relaxation has `E=0`. Moving such a relaxation of contraction `b` from before another admissible operation to after it leaves mean map and duration unchanged and reduces covariance by `(1-b^2)E`. Every fastest program saturates the rate bound along a shortest shape, so moving all isotropic relaxation to the end proves the ordering. Shortest-shape ambiguities can rotate the covariance; they do not change radial error.

The resulting centered Gaussian error simultaneously minimizes every centered-ball tail among duration minimizers. Independent preselected random programs implementing the same target do not improve that law. For rotation targets, randomizing optimal orientations can make covariance isotropic, but the error remains a Gaussian mixture rather than an isotropic Gaussian. Generic orientation randomization need not preserve a general target matrix.

For a boundary rotation, put `L=sqrt(theta^2+2pi|theta|)`, `rho=L/(pi+|theta|)` and `f=1-exp(-2L)`. Added-noise eigenvalues are

```
q_+/- = (2D/Lambda) f [1+rho^2 +/- rho sqrt(1+rho^2)].
```

With surplus contraction `u=s-L`, each becomes `exp(-2u)q_+/- + (D/Lambda)(1-exp(-2u))`. The squared radial error is distributed as `q_+ Z_1^2+q_- Z_2^2`, with independent standard normal variables. All tabulated confidence radii are evaluations of this model.

## Work and input resources

Starting and ending at reference trap `A=Lambda I`, and including endpoint potential switches, the constructed optimal program has net expected modulation work `2 k_B T_bath d(N)` for any initial distribution of finite second moment. This is an accounting identity for the constructed control, not a minimum-work theorem. It credits recovered negative work and does not price gross supply, recovery machinery, peak power, actuator loss or work fluctuations.

Signal attenuation requires substantial stored input energy. For input radius `R`, relative error tolerance `epsilon` and success probability `p`, the source gives the necessary bound

```
E_0/(k_B T_bath)
 >= (exp(2L_theta)-1) log(1/(1-p))/epsilon^2
E_0 = gamma Lambda R^2/2.
```

The exact fastest 90-degree boundary example needs approximately `1.16e6 k_B T_bath` stored input energy for 95% probability of error below 10% of desired output radius. That is stored energy, not an assertion that preparing an unknown input costs exactly that work. Input preparation, amplification, readout and full apparatus reset remain separately unpriced.

During rotation, `||dot A||_op=Lambda^2(pi+|theta|)/(2L_theta)` diverges as the requested angle tends to zero. Endpoint changes are ideal instantaneous switches and rank-one stiffness includes a zero eigenvalue. The theorem is amplitude-limited, not a finite-bandwidth apparatus optimum.

## Existing methods and actual physical evidence

The record credits established quadratic Brownian work/covariance equations, `SL(2,R)` distance and cut-locus formulas, gradient-flow holonomy, labelled transport, positive-factor geometry and polygon inequalities. The primitive log preserves defeated novelty claims and revised constructions. Existing methods can use the optimal formulas too; no general methodological advantage is inferred.

Published controlled colloidal relaxation supports the ordinary experimental setting but does not implement this rotating rank-one unknown-input map. Measured hydrodynamic-memory resonances and negative correlations challenge the white-noise memoryless model at high speed. The producer acquired papers and their reported conditions, not the original raw time records. No new experiment or empirical validation of this control operation occurred.

The whole-response attenuation law is planar. Extra initialized coordinates change the access class; separate dimension-independent necessary bounds retain their own scope. Adaptive feedback, anisotropic noise, inertia, hydrodynamic memory, moving/nonlinear force landscapes, unknown force calibration and finite slew require different theorems.

The original [recorded verification summary](package/invention_variation/last_verification_summary.json) includes 36 general-target checks, 143 near-rotation regression cases after a repaired coordinate defect, high-precision stage checks and independent geometric/variation audits. Numerical results catch implementation mistakes and supplement the global proofs; they are neither experimental evidence nor interval certification. No script or scientific verification ran during publication.
