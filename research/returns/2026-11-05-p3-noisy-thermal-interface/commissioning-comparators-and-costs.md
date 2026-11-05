# Commissioning, raw ports, common-bath separation and complete costs

The [main interface result](README.md) supplies a fixed-noise circuit operation under a concrete commissioned model. It does not establish a hardware implementation or a total-resource advantage over ordinary active error correction.

## Acquisition uses the same noisy templates

One unknown homogeneous Pauli channel determines all known preparation/gate/reset/measurement/capture templates. Opposite-sign preparations cancel a fixed affine capture offset: half the recorded polarization difference has form `m_t=A lambda_axis^t`, so `lambda_axis=m_1/m_0`. Three axes determine the channel within this parameterized model. This is not separate inference of arbitrary unknown preparation and measurement maps.

Protected simulation of the explicit finite endpoint circuit computes its effective channel, retaining the **unconditional** decoded resource syndrome marginal. A known Bell pair inside that calibration computation is not an ideal physical operation on the unknown incoming qubit. Large fixed decoder tables and simulation accuracy/cost are charged.

For thermal coefficients, the chosen hardware can selectively isolate an actual bounded-support check coupler. Its excitation `r_a=(1+e^(beta J_a))^(-1)` is recorded through calibrated affine coefficients and debiased. Per-check trials sufficient for parameter error `eta_lambda` scale as `O(e^(2lambda_max) eta_lambda^(-2) log(m/delta))`; choosing `eta_lambda=O(epsilon/m)` is polynomial but potentially severe. Waiting, reset, capture and arithmetic count. Physical fidelity stays fixed while statistical precision improves through work.

Selective coupler isolation and stable switching are substantial access premises. Finite commissioning cannot certify stationary independent noise or the holding bath against unrestricted future drift.

## Raw input/output has a sharp irreducible floor

For depolarizing cuts `D_a(rho)=(1-a)rho+a I Tr(rho)/2`, the source gives

\[
\inf_{\mathcal R}\tfrac12\|
\mathcal D_b\circ\mathcal R\circ\mathcal D_a-id
\|_\diamond=\tfrac34(a+b-ab).
\]

The intermediate operation can include arbitrary encoding/decoding; a Bell input proves the lower bound and identity between cuts attains it. Thus a fixed number of noisy raw crossings leaves `O(p)+epsilon`, while arbitrary interior accuracy or encoded handoff has a different paid endpoint. The same limitation applies to an active competitor with identical input access.

## A common bath defeats noninteracting passive storage

The return chooses unobserved independent isotropic local X/Y/Z bath couplings with Davies coefficients

\[
g_\beta(\omega)=2\nu/(1+e^{-\beta\omega}).
\]

They obey detailed balance and the accepted interacting holding contract. For any noninteracting holding Hamiltonian `H=sum_i H_i`, arbitrary individual gaps and cooling, the one-site channel up to a known unitary is

\[
\mathcal E_{i,t}(\rho)=\lambda\rho+(1-\lambda)\tau_i Tr\rho,
\qquad\lambda=e^{-4\nu t}.
\]

When `lambda<=1/2`, a symmetric two-output extension sends the input to either branch with weight `lambda` and otherwise outputs two Gibbs states. Tensoring extensions and copying classical records retains identical decoded marginals for any encoder/decoder. The two reference-output Bell projectors sum to operator norm `3/2`, so each marginal has Bell fidelity at most `3/4`. The source's diamond-error distance is therefore at least `1/4` for `t>=log(2)/(4nu)`, independent of qubit count, individual gaps and temperature. Zero holding Hamiltonian gives the stronger entanglement-breaking boundary after `log(3)/(4nu)`.

All information-carrying quantum systems must undergo that bath; no protected external quantum helper or bath-jump record is provided. The interacting construction can achieve error below `1/4` for a longer interval without active quantum correction. This is a specified common-bath passive-storage separation, not a no-go for active correction or a universal power-outage claim. Monitoring the bath, changing its spectral law or adding interacting autonomous recovery changes the hypotheses. Static interactions, cooling and classical record maintenance remain present.

## Strong competitors receive the same access and full bill

Ordinary active fault tolerance already supplies fixed-noise storage, computation and noisy I/O. Modern qLDPC interfaces improve their stated preparation/space workloads. Autonomous correction is a strong incumbent when the goal is removal of an external clock. They receive the same control links, cooling, switching, routing, metrology and raw access. A competitor given the same passive hardware can adopt this completed interface.

The source accounts for fabrication, acquisition, commissioning, access, reset and the integral of static/cooling/record/active power, plus quantum/classical occupied spacetime, critical-path duration, interconnect use and fresh resource pools. Regeneration costs polynomial inverse-accuracy overhead. Gate-count efficiency does not price these resources.

BDL's displayed random-embedding scale around `5.4e24`, density bound around `6.6e10` and witness exponent about `.01` make sufficient certificate sizes extremely unfavorable. These are certificate parameters, not physical lower bounds. The nonlocal active fabric has no derived finite-speed bounded-density 3D deployment here. The low-temperature threshold and conservative base code add costs. No universal energy crossover follows from long passive lifetime; actual acquisition and holding-power prices must satisfy it.

Two additional supplied deductions remain distinct: maximally mixing the logical subsystem gives full Gibbs preparation, and a bound `D(mu||pi)<=128 w d N q^2 e^(w lambda_max)` gives excess prepared-state free energy `beta^(-1)D(mu||pi)`. It does not prove reversible work for the sampler/control algorithm.

## Source-reported checks and preserved originals

The return reports five passing finite suites, including inverse/prefix TV `3.58e-16`, soft-chain detailed-balance/stationarity residuals `2.71e-20/1.21e-16`, a five-qubit reference-entangled loading error `3.04e-6` below a `5e-6` comparison bound, native-voter symmetry and common-bath broadcasting checks. These are finite algebra/algorithm results, not a simulated growing-family lifetime or a measured threshold. The [check receipt](package/noisy_interface_work/finite_check_receipt.json), [blackout result](package/noisy_interface_work/blackout_boundary_checks.json), [interface identities](package/noisy_interface_work/endpoint_route/interface_identity_checks.json), [acquisition proof](package/noisy_interface_work/passive_route/noisy_acquisition_and_control.md), [full report](package/Astra_Noisy_Thermal_Interface.pdf), original code and nested predecessor archive are included unchanged. Capital executes none of those suites.

The earlier register/loader, coherent TFD, central-sector and named sampler-obstruction results retain their actual scopes. The separate continuous-time autonomous quantum frontier theorem remains open. Capital performs no new audit, reproduction, model acquisition or physical validation to publish this supplied result.
