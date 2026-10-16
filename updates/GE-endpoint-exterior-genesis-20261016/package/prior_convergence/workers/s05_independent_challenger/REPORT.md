# S05 independent challenger: branch-scoped response through an acquired port

16 October 2026. **Decision: NOT_ACHIEVED as a new enabling capability.** I constructed and proved a restricted operation for predicting a finite control response of a local subsystem coupled to an unknown, metastable exterior. The mathematical result is exact and the synthetic discriminator passes its bounds. The central reduction is already adjacent to nonlinear Kron reduction, Schur complements, and measured multiport equivalents. An equally informed incumbent can use the same acquired port curve to make the identical prediction. There is no physical acquisition, demonstrated advantage, historical-priority claim, or exceptional foundational result.

## Mechanisms screened before selection

1. **Ordered-pulse commutator spectroscopy.** Apply two nonlinear controls in both orders to expose a hidden interaction from endpoint differences. The Lie-bracket mechanism and signal-separating phase cycles have substantial primary precedent, including [Dürr et al. on Lie-bracket approximation](https://arxiv.org/abs/1109.6129) and an [implemented four-pulse phase-cycling spectroscopy protocol](https://arxiv.org/abs/2412.07492). I stopped before producing an incremental commutator identity or calling pulse-order subtraction an invention.
2. **Nonlinear boundary defect localization.** Use paired elliptic boundary loads and adjoint products to detect a sign-definite internal anomaly without reconstructing the whole coefficient. Nonlinear monotonicity and boundary support methods are already substantial, including [Corbo Esposito et al.'s nonlinear conductivity monotonicity principle](https://arxiv.org/abs/2007.15431) and [Salo–Tzou's single-point semilinear boundary uniqueness](https://arxiv.org/abs/2202.05290). I stopped this direction before claiming ordinary nonlinear EIT as new.

The selected mechanism addresses a harder regime: a selected stable response branch can have *negative* differential port response, so global contraction and strongly monotone resistor laws do not apply. The operation is nevertheless limited to that branch and remains close to existing network reduction.

## Target and interface

The scientific target is a finite response \(x_h-x_0\) of a small modeled local circuit, material subassembly, or network region when a drive \(h\) is changed. The remainder of the network can have many hidden states and multiple stable branches. A physical clamp sets the accessible interface state \(z\), and a sensor measures exterior port current \(j(z)\) after branch-preserving settling. The local law \(U_h(x,z)\) is supplied or independently calibrated. The exterior microscopic law and states are not supplied to the predictor.

For a full energy \(E_h=U_h(x,z)+V(y,z)\), a smooth selected exterior branch \(V_y(y(z),z)=0\) has port relation \(j(z)=V_z(y(z),z)\). Its equilibria are exactly the roots of \(U_{h,x}=0, U_{h,z}+j(z)=0\), irrespective of exterior dimension. If the reduced equation is strongly monotone with modulus \(\mu\) over the stated drive corridor and an acquired port approximation has uniform error at most \(\epsilon\), the predicted state error is at most \(\epsilon/\mu\). A target with Lipschitz constant \(L\) has error at most \(L\epsilon/\mu\). [PROOF.md](PROOF.md) gives all hypotheses, the Schur-complement stability condition, and the branch-failure construction.

The key acquisition caveat is consequential: the sample grid and instrument resolution do not by themselves supply a *uniform* port error, curvature bound, or branch guarantee between samples. Those quantities must be independently bounded or the certificate returns `UNKNOWN`.

## Exact synthetic discriminator

The hidden exterior is the nonconvex quartic \(V(y,z)=(y^2-1)^2/4+0.8(y-z)^2/2\). A linear two-node local region has a stabilizing leak. On the selected positive branch at \(z=0\), the exterior port slope is \(j'(0)=-0.8\), while the entire coupled system has a positive reduced Hessian with least eigenvalue at least \(1.433809621\) throughout the tested drive corridor. Thus the negative differential exterior response is compatible with a stable full operating branch. This explicitly leaves the global convex resistor regime while preserving a tractable target.

For \(h=1\), [port_branch.py](port_branch.py) gives the full selected-branch target \(x=0.5747166330\). A 21-point port table on \([0,0.2]\), with deterministic \(\pm10^{-4}\) error injected into each simulated measurement, predicts \(x=0.5747037161\). The actual target error is \(1.29\times10^{-5}\). A supplied analytic curvature bound gives a rigorous table error at most \(3.6833\times10^{-4}\), hence a target error at most \(6.8209\times10^{-5}\). A one-point tangent extrapolation predicts \(x=0.5925925926\) and errs by \(0.017876\); it is only a weak diagnostic, **not** the fair incumbent. All exact values, assertions, and resources are in [RESULTS.json](RESULTS.json).

The branch test matters more than the small interpolation error. At identical port state \(z=0\), positive and negative prepared branches produce currents differing by \(0.715541753\). A descending and ascending quasistatic sweep jumps near \(z=\mp0.0430331483\), respectively. A branch-blind one-valued current table would silently conflate two different physical response laws. Repeated preparation, direction, dwell time, jump incidence, and noise-driven transitions must be measured before an experimental prediction can be certified.

## Strongest same-information incumbent and prior art

The fair incumbent is an empirical nonlinear multiport or I–V lookup obtained from the *same* 21 port clamps, followed by an ordinary local circuit solve. It can use the same piecewise-linear interpolation and obtain exactly the same \(x\) and error certificate. If the exterior model is known, a full nonlinear solver is stronger still, though it has more supplied information. The tangent extrapolation does not establish an advantage over either. No reduced method here uses fewer port acquisitions than the best equally informed predictor.

[Van der Schaft, Besselink, and Huijzer, *Kron reduction of nonlinear networks* (2024)](https://arxiv.org/abs/2403.00400) already derive nonlinear boundary response maps by eliminating internal nodes, with Hessian Schur complements and strongly convex edge laws. My restricted branch calculation permits a negative port derivative because the hidden exterior is nonconvex, but the algebra is an implicit-function/Schur argument, not an established priority claim. [Johnson, *Circular Planar Resistor Networks with Nonlinear and Signed Conductors* (2012)](https://arxiv.org/abs/1203.4045) also shows that nonlinear and signed boundary recovery has deep earlier theory. These sources make any broad “nonlinear black-box exterior compression” claim untenable. Historical novelty of a particular branch-aware error package is `UNKNOWN`, and the fair empirical I–V incumbent already matches its output.

The double-well plus stabilizing positive quadratic is also physically adjacent to ferroelectric negative-capacitance research, including the [measured double-well landscape in a dielectric heterostructure](https://www.nature.com/articles/s41586-018-0854-z) and [earlier series-dielectric stabilization experiments](https://pubs.acs.org/doi/10.1021/nl5017255). Those papers do not validate this synthetic resistive circuit or its branch certificate; they rule out treating stabilized negative response itself as a new physical principle.

## Physical discriminator and full resource gate

An attainable but unperformed electrical test would connect a programmable cubic current element at hidden node \(y\) to a one-port resistor, with a two-node stabilized local circuit. Before test, specify voltage/current units, a preparation and reset protocol selecting one stable branch, the drive corridor, an independently validated port-current uncertainty bound, and a curvature/stability lower bound. Clamp 21 port voltages over the corridor; measure settled currents with repeats, drift controls, and bidirectional sweeps. Release the clamp, apply held-out drives \(h=0.25,0.5,1\), and measure \(x,z\) and jump incidence. Compare three predictors that all receive the same clamp data: branch-aware table plus theorem, standard empirical I–V lookup plus local solve, and a full-model fit only if its fitting data/cost are charged. The decisive superiority gate would be strictly less total acquisition/computation for equal target coverage and error at held-out drives. The present analysis predicts no superiority over the empirical lookup.

The complete cost must include cubic-element fabrication/programming and supply power, branch resets and failed attempts, clamp and current-sensor calibration, each settling time, sample repeats, reverse sweeps, temperature/drift control, local-law identification, numerical solves, and error-bound validation. The replay used 21 simulated clamps plus 1,602 simulated sweep states, not physical measurements. It measured no wall time advantage, monetary cost, or energy. Finite samples alone cannot rule out an unobserved fold between sample points. A fold or branch switch inside the target corridor makes the current single-branch certificate inapplicable and returns `UNKNOWN`.

## Status

| Claim | Status |
|---|---|
| Branch-scoped reduction and \(\epsilon/\mu\) state bound | Internally proved under stated smoothness, existence, branch, and monotonicity assumptions |
| Nonconvex fixture with negative port slope and stable coupled branch | Exact algebra plus executable numerical replay |
| Finite table predicts the synthetic held-out response within its bound | Executed; simulator-generated samples only |
| Branch-label/hysteresis discriminator | Exact fold analysis and finite simulated sweeps |
| Experimental device or measured scientific output | Not performed |
| Better than strongest same-information nonlinear port lookup | **No; matched baseline ties exactly** |
| Novel foundational operation, practical or mission-scale capability | **NOT_ACHIEVED** |

This result may serve as a useful negative control for any Convergence Genesis claim that treats boundary compression or a local tangent as newly enabling. A genuine next advance would need a new mechanism that acquires a certified branch response at materially lower cost than an equally informed nonlinear port model, or proves an output inaccessible to that model under the same interface.
