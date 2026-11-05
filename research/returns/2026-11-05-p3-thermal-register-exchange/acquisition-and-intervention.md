# Priced acquisition and a finite harmonic reset-and-mark operation

These are completed companions to the [reusable register theorem](README.md), with their own access and calibration premises. The original proof notes and audits govern; neither operation grants a free apparatus or an unmeasured real-world capability.

## Ramsey calibration on constrained checks

For known commuting Pauli supports, prepare a ground eigenstate, apply physical Pauli frame `R` and use a one-site probe `P`. The signed gap is

\[
\Delta_P(R)=\sum_{a\in B(P)}J_a\chi_a(R),\qquad
J_a=E_R[\chi_a(R)\Delta_P(R)].
\]

A controlled-P / natural-evolution / controlled-P Ramsey sequence measures the gap without controlled-Hamiltonian access. Orthogonality is over actual Pauli characters, even when stabilizer relations constrain attainable signs. It does not assume independent arbitrary sign assignments. Combine exact duplicate terms instead of claiming separate identifiability.

The [operation](package/calibration_operation.md) and [completed audit](package/calibration_audit.md) give conservative total shots `O(m^3 epsilon_cal^(-2) log(m/alpha_conf))` at fixed overlap, coupling and temperature bounds, for coefficient error `O(epsilon_cal/m)`. Every shot pays state preparation, routing, interrogation, control precision, readout and reset. Timing/control bias enters the gap error. Temperature needs a priced thermometer; a bath-rate upper bound does not establish fast thermometer equilibration.

The constrained syndrome law obeys `TV(p_lambda,p_lambdahat)<=sum|lambda_a-lambdahat_a|/4`. Once acquired and initialized, that distributional error is paid once through a fixed adaptive channel. New backgrounds, changed Hamiltonians or calibration-dependent faulty gates have separate budgets. No rare lifetime measurement is required for these coefficient identities; the physical model still needs its own validation.

## Finite meter with endpoint-independent error

The [finite reset-and-mark theorem](package/intervention_route/FINITE_RESET_AND_MARK.md) treats the calibrated harmonic Langevin source with `S=(x,p)`, `B=e_p`, constant hidden force `fZ`, and

\[
A=\begin{pmatrix}0&1/M\\-k&-\gamma\end{pmatrix},\qquad
k/M=\lambda(\gamma-\lambda),\quad \nu=\gamma-\lambda.
\]

The old `(x_0,p_0,Z,R)` law may be arbitrary. A degree-13 Hermite polynomial supplies smooth finite pulse kernels

\[
h=D(D+\lambda)(D+\nu)\phi,\qquad
g=M D(D^2-\lambda^2)(D^2-\nu^2)\phi.
\]

Endpoint/moment identities cancel initial position and hidden force, including the repeated-root critical case. Canonical pointer coupling `-G g(t)xP`, followed by a detached quadrature operation removing known self-backaction, gives

\[
Y=p_0+E,\quad E\sim N(0,v),\qquad
v=2\gamma\sigma^2\int h^2+v_Q/G^2.
\]

Crucially `E` is independent of the complete old system and both components of the later source innovation. An ordinary unbiased noisy derivative estimate would not supply that independence. Source backaction is retained as an explicit loaded Gaussian channel rather than discarded.

If `v<sigma^2`, take fresh `xi~N(0,tau^2)`, `tau^2=sigma^2-v`, and use a smooth controllability-Gramian force to add `e^(AT)B(xi-Y)` at the endpoint. Then `zeta=xi-E` is thermal and independent of the old system: the exact endpoint is the loaded channel `K_T C`.

Choose the arm from the fresh actuator coordinate with

\[
b(\xi)=\tfrac12[1+\eta e^{v/(2\tau^2)}\sin(\sigma\xi/\tau^2)].
\]

It yields the full joint source/hidden/reference/arm law exactly when

\[
v\le\frac{2\log(1/\eta)}{1+2\log(1/\eta)}\sigma^2.
\]

This sharp threshold concerns that Gaussian interface, even allowing postprocessing of both `(Y,xi)`. It is not an obstruction to all devices with extra observations or actuators. A finite harmonic quadrature rotation and two mechanical couplings implement analog feedback without a free exact ADC. Only bounded arm-probability coin logic needs final digitization.

## Useful output, costs and campaign scope

The exact momentum-arm contrast is `2 eta sigma exp(-1/2)[exp(AT)]_pp`, with `[exp(AT)]_pp>=exp(-gamma T/2)(1-gamma T/2)` for `0<=T<=2/gamma`. A fixed fast execution can retain useful contrast while hidden-force relaxation time diverges; the force has not been learned.

The [supplied 65-digit receipt](package/intervention_route/finite_reset_results.json) includes soft, critical and ordinary examples. The normalized `T=0.2` fixture has variance about `0.1897204`, corrected sine amplitude `0.5620996`, contrast `0.494886` and force-action coefficient `561.617` per unit `E[p_0^2]+sigma^2`. Its coupling peak is about `1.05e5` and slew about `2.83e7`. The `T=0.75` fixture lowers that coefficient to about `38.0529`, with contrast `0.269813`. These large finite resource values and numerical residuals are analytic implementation checks, not hardware trials or optimal designs.

Pointer/actuator preparation, smooth switching and trap rotation, range, coupling energy, force, slew, mechanical work, heat disposal, calibration, retained records and useful response measurement all count. Smooth saturation gives bounded interaction Hamiltonians on a finite operating box, with exit probability charged by coupling until first exit. Arbitrary second-moment laws need their actual larger tail bounds; Gaussian apertures cannot be assumed. Position range and potentially energy capacity still grow as `lambda^(-1/2)`. Quantum uncertainty constrains pointer choices and classical validity.

The ideal calibrated per-use kernel is exact conditional on past history, so it adds no fixed `n v` marking-discrepancy term. Kinetic moment costs still need a per-trial ledger. Finite reset/saturation/control errors compose: a conservative allocation `O(epsilon/n)` gives serial pointer bath-reset contact time `O(n log(n/epsilon))` under uniformly bounded post-use energy moments. Binary-only coin errors with a strict probability margin admit squared-error composition and `O(epsilon/sqrt(n))` accuracy. Calibration requirements depend on the campaign length and moments and must be acquired, not assumed away.

The endpoint is explicitly loaded. Comparing it to an unmetered experiment requires charging the additional force path. This calibrated affine counterexample defeats a universal lower bound based solely on hidden-force inference time; it does not resolve the universal nonlinear campaign resource law. [P1's distinct direct-arm feedback construction](../2026-11-05-p1-burst-constructive-exchange/feedback-and-resources.md) retains its different instrument, endpoint and cost account.

All original scripts and source audits are preserved. Capital ran no scientific checker or simulation.
