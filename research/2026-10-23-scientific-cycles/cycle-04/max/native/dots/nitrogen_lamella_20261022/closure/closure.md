# A conservative molecular lamella with explicit mechanical boundary conditions

## Outcome

The proposed closed-rigid pressure closure is correct for an ideal-gas mixture in a low-Mach material slab. It conserves internal energy, not enthalpy. Its pressure denominator is strictly positive whenever the mixture is thermodynamically stable, because it equals the width-weighted `cv/cp` sum. A spatially uniform pressure does not mean a temporally fixed pressure.

There is also a clean constant-pressure material-slab construction. It conserves enthalpy and has a moving outer material boundary. The two boundary conditions are alternatives, not different discretizations of the same process. A small executable counterexample makes their scientific consequence explicit: the 1700 K acceptance decision reverses between them, without changing transport or introducing chemistry.

An entropy-compatible Maxwell–Stefan face construction is supplied below. It resolves the specific finite-volume problem that a locally entropy-positive differential transport law need not remain entropy-positive after arbitrary midpoint interpolation.

No experiment, literature coefficient, injection geometry, flowing-device realization, surface response, or long chemical trajectory is claimed here. `verify_closure.py` is an algebraic certificate only. Initial project context was `nitrogen_admissibility_20261022/DECISION.txt` and `nitrogen_admissibility_20261022/recycle_quench/finite_mixing.py`; the latter's shorter requested path did not exist. At the parent's subsequent explicit request, the small actual-source endpoint bound and its thermochemistry were independently checked below.

## 1. State and coordinate

Let `mu_j` be fixed cell mass per transverse area, in kg/m², and let `m` be the corresponding material mass coordinate. Interfaces move with the barycentric gas velocity. Species diffuse through those material interfaces; total diffusive mass flux is zero. Define

- `R_j = Σ_i Y_ij R_i`, with `R_i = Ru/W_i`;
- `h_j = Σ_i Y_ij h_i(T_j)`;
- `cp_j = Σ_i Y_ij cp_i(T_j)` and `cv_j = cp_j − R_j`;
- `v_j = R_j T_j/P`, `rho_j = 1/v_j`, and `Δx_j = mu_j v_j`;
- `u_j = h_j − P v_j = h_j − R_j T_j`.

All thermochemical quantities must use the same formation-energy and entropy references. The species vector sums to one. Species source `omega_i` has units kg/(m³ s), so the material source is `omega_i/rho`. Include reaction formation enthalpy in `h_i`; adding a separate reaction heat would double-count it.

Fluxes point from the left cell to the right cell. Let `ΔF_j = F_(j+1/2) − F_(j−1/2)`. The conservative balances are

    Ydot_ij = −Δj_ij / mu_j + omega_ij/rho_j
    hdot_j = v_j Pdot − ΔQe_j / mu_j
    Qe_f = q_f + Σ_i hbar_if j_if.

The energy equation is the ideal low-Mach enthalpy balance, obtained from `udot = −P vdot − div_mass(Qe)`. It neglects kinetic energy and viscous dissipation at the order of the low-Mach approximation. Uniform thermodynamic pressure is compatible with small dynamic pressure gradients at the next order; it is not an exact solution of full compressible momentum for arbitrary rapid transients.

Define

    A_j = −ΔQe_j/mu_j − Σ_i h_i(T_j) Ydot_ij.

Then

    Tdot_j = (v_j Pdot + A_j)/cp_j.

Here the cell `h_i(T_j)` in `A_j` and the face `hbar_if` in `Qe_f` perform different jobs. They must not be interchanged.

## 2. Closed, rigid boundary

The total physical width is fixed:

    L = Σ_j mu_j v_j,
    P = [Σ_j mu_j R_j T_j]/L.

Differentiating the latter and inserting the temperature equation gives exactly

    Pdot = Σ_j mu_j [R_j A_j/cp_j + T_j Rdot_j]
           / [L − Σ_j mu_j R_j v_j/cp_j],
    Rdot_j = Σ_i R_i Ydot_ij.

The denominator has the useful equivalent form

    D = Σ_j mu_j v_j cv_j/cp_j.

Thus `D>0` for positive widths and `cp_j>R_j>0`. A singular or negative denominator in an accepted physical state is a failed EOS/heat-capacity/state condition, not an adjustable mixing parameter. Trace-negative Jacobian probes are not accepted physical states.

Cell volume rates and interface velocities can be reconstructed:

    vdot_j = [R_j Tdot_j + T_j Rdot_j − v_j Pdot]/P,
    U_face,0 = 0,
    U_face,k = Σ_(j<=k) mu_j vdot_j.

The closure makes `U_face,N=0` up to arithmetic error. This is a testable velocity field, and its Mach number is part of checking the low-Mach approximation.

### Exact semidiscrete balances

With impermeable insulated endpoints, `j_i=Qe=0` there:

- `Σ_i Ydot_ij=0` if `Σ_i j_if=Σ_i omega_ij=0`.
- Species mass changes only by its chemical source; elemental totals are conserved if the reaction source conserves atoms.
- `Hdot = Pdot L`, where `H=Σ_j mu_j h_j`.
- `U = H − P L`, so `Udot=0` at fixed `L`.
- `Σ_j mu_j vdot_j=0` exactly in the semidiscrete algebra.

For a boundary energy flux, `Udot=Qe_left−Qe_right`; the same sign convention applies in the other mode. An impermeable insulated boundary has both species flux and reduced heat flux zero. Setting only `Qe=0` does not prohibit compensating species exchange.

Implement the algebraic `P(Y,T)` directly in each RHS evaluation, then compute its derivative from the closure. If pressure is separately integrated, track the algebraic EOS discrepancy rather than silently overwriting it. The semidiscrete conservation identities do not guarantee that a stiff ODE solver conserves them exactly in time.

## 3. Prescribed pressure with a moving material boundary

For `P=P0`, set

    Pdot=0,
    Tdot_j=A_j/cp_j,
    L(t)=Σ_j mu_j R_j T_j/P0.

With the same no-flux species/thermal boundaries,

    Hdot=0,
    Udot=−P0 Ldot,
    U(t)−U(0)+P0[L(t)−L(0)]=0.

The signed work done by the gas is `P0 ΔL` per unit transverse area. This is ordinary pressure/flow-work accounting, not an extra recoverable-power credit. A formal moving material boundary is not a fabricated mechanical work port, a demonstrated piston, or a proven injector. A fixed-area flowing apparatus must satisfy its own axial continuity, momentum and total-energy budgets before it can realize this history.

This is the appropriate thermodynamic alternative to retain when comparing to the earlier constant-pressure homogeneous entrainment calculation. Its different geometry and distributed molecular transport still require new qualification. In particular, it begins with a fixed mass of both streams in contact; it does not reproduce a parcel whose total mass grows by prescribed entrainment.

The common generalized identity is `Udot=Qe_left−Qe_right−P Ldot`. Constant `P` and constant `L` are not both freely selectable; imposing both generally overconstrains the closed adiabatic model.

## 4. Initial hot and cold inventory

For hot mass per area `mu_h`, return mass `mu_c=Rrec mu_h`, `Rrec=.85`, initial equal `P0=101325 Pa`, `Th=2700 K`, `Tc=300 K`, and initially uniform compositions in each layer,

    mu_h = P0 L0/[R_h Th + Rrec R_c Tc],
    mu_c = Rrec mu_h.

For equal gas constants, the hot fraction of the physical width is `2700/(2700+.85*300)=0.9137056`; the two cold layers together occupy `0.0862944 L0`. Their cold thickness is not proportional to cold mass fraction. Splitting the cold inventory equally on each side gives a cold/hot/cold stack.

Symmetry/no-flux boundaries can represent the centers of repeated cold sheets; they need not be solid walls. The corresponding periodic repeating stack must actually be the intended geometry. A rigid representative width still assumes confinement or a prescribed repeated-cell average, while a constant-pressure representative width may vary in time.

A mathematically sharp temperature/composition jump gives singular early-time gradients in the continuum. A finite mesh implicitly smooths it. Check mesh refinement and either prescribe an initial smooth interfacial thickness or demonstrate that the omitted acoustic initial layer is irrelevant to the claimed observation time. In particular require the acoustic equilibration time to be short compared with the relevant transport time, and induced interface velocities small compared with sound speed. Shrinking a lamella arbitrarily is not a license to violate these conditions.

## 5. Entropy balance and a constructive face law

For an ideal mixture let `g_i(T,P,X)` denote the mass-specific chemical potential,

    g_i/T = h_i(T)/T − s_i^0(T) + R_i ln(X_i P/Pstd).

The Gibbs identity is

    T ds = dh − v dP − Σ_i g_i dY_i.

For one internal face, the exact semidiscrete contribution to global entropy production is

    sigma_f = Qe_f Δ(1/T) − Σ_i j_if Δ(g_i/T),

where every jump is right minus left. No physical-width factor is missing: this is the entropy rate per area assigned to the face. The reaction contribution in a cell is

    sigma_chem,j = −mu_j Σ_i g_ij omega_ij/(rho_j T_j).

For a thermodynamically consistent reversible mechanism this is nonnegative. In molar reaction notation it becomes a sum of `Ru(r_forward−r_reverse) ln(r_forward/r_reverse)` times cell volume. Reversible labels alone do not prove this: the forward/reverse ratio must match the same chemical potentials. A signed extension used for solver trials does not certify entropy or physical admissibility of accepted negative compositions.

### Gibbs–Helmholtz enthalpy secant

Define `beta=1/T`, `z_i=g_i/T`, and

    hbar_i = Δ[h_i(T)/T − s_i^0(T)] / Δbeta.

For equal temperatures use `hbar_i=h_i(T)`. This is the beta-averaged enthalpy, not generally the arithmetic mean of endpoint enthalpies. It satisfies

    a_i := Δz_i − hbar_i Δbeta = R_i Δln X_i

at spatially uniform pressure. For near-equal temperatures evaluate the secant stably, using an analytic expression or controlled quadrature of `h_i(1/beta)`; naive subtraction may lose precision.

Then `Qe=q+hbar·j` yields

    sigma_f = q Δbeta − j·a.

A generic constructive class is `q=Lambda Δbeta`, `j=−M a`, with `Lambda>=0`, symmetric positive-semidefinite `M`, and `M 1=0`. It has `Σ_i j_i=0` and `sigma=Lambda(Δbeta)^2+a^T M a>=0`. For Fourier heat conduction choose `Lambda=kappa T_L T_R/d`, so `q=−kappa ΔT/d`. This construction certifies thermodynamic structure, not the magnitude or physical applicability of an arbitrary mobility matrix.

### An entropy-certified Maxwell–Stefan finite-volume face

This is a specific construction suited to a molecular transport core. For strictly positive endpoint mole fractions define

    ell_i = (X_i,R−X_i,L)/(ln X_i,R−ln X_i,L),
    S = Σ_i ell_i,
    X_i,* = ell_i/S,
    grad_i = (X_i,R−X_i,L)/d.

At equal endpoints use `ell_i=X_i`. Solve the ordinary Maxwell–Stefan equations at `X*`, using `grad_i` as the finite-difference mole-fraction gradient, pair diffusivities `D_ik=D_ki>0`, and the mass-average constraint. In terms of `w_i=X_i,* v_i`,

    grad_i = Σ_(k!=i) [X_i,* w_k − X_k,* w_i]/D_ik,
    Σ_i W_i w_i=0,
    j_i=W_i c* w_i,

where `c*=P/(Ru T*)>0` and the same chosen face temperature is used consistently by the transport evaluation. The normalized logarithmic mean makes

    grad_i/X_i,* = S Δln X_i/d.

Consequently

    −Σ_i j_i R_i Δln X_i
      = c* Ru d/S · Σ_(i<k) X_i,* X_k,* (v_i−v_k)^2/D_ik >=0.

Together with Fourier `q` and the enthalpy secant, this proves exact semidiscrete face entropy production. The certificate script verifies the identity numerically. An arbitrary arithmetic midpoint composition does not supply this proof. Dividing the input gradient by `S` also yields a nonnegative law but changes the coarse-grid transport magnitude; the construction here uses the actual raw finite difference `ΔX/d`.

The finite-volume law is consistent with the continuous equations as the mesh is refined. Entropy certification alone does not establish spatial convergence or the correct experimental binary coefficients, conductivity, Soret or Dufour response. A no-Soret, Fourier-reduced-heat model is a thermodynamically permissible restricted model, not a measured claim that thermal diffusion is negligible.

### Zero species and time discretization

An absent species on both sides can be removed from the face subsystem. One-sided zero abundance is a limiting case: the mole-gradient and limiting flux may be finite while `Δln X_i` and the initial entropy slope are infinite. Do not replace those facts with an unreported floor. Use a justified limit or a conservatively initialized positive trace and report its sensitivity. Disjoint endpoint supports can make this normalized-mean face undefined (`S=0`) and need a separate positive-state transition construction; silently normalizing zeros is not valid.

The semidiscrete entropy argument does not make BDF or an arbitrary explicit update positivity-preserving or entropy-stable. Monitor accepted states, total entropy, mass/atoms, the energy/work ledger, width/EOS residuals, and cell extrema. Saving only a few time samples is not a bound on the true maximum temperature or the worst entropy step.

## 6. Two explicit failure cases

### Boundary-condition failure that changes the temperature-cap decision

Use a single chemically inert ideal gas with

    cp(T)=900+0.12 T J/(kg K), Rgas=287 J/(kg K).

This is an illustrative stable caloric model, not the six-species project mechanism. It has positive `cv` throughout 300–2700 K. Start with 1 kg hot gas at 2700 K and .85 kg cold gas at 300 K, at the same pressure.

- Constant-pressure adiabatic enthalpy mixing gives `1675.584524 K`, below 1700 K.
- Closed-rigid adiabatic internal-energy mixing gives `1703.128726 K`, above 1700 K, with `Pfinal/Pinitial=1.066256563`.
- The constant-pressure final material width is `1.049012308` times its initial width.
- Applying the constant-pressure enthalpy answer inside the fixed initial width would lose `41,566.603 J/kg hot` of internal energy without an admitted heat/work path.

This is a constructive counterexample to exchanging the two boundary models. It is not a prediction that the actual six-species rigid case fails, nor an argument that prescribed pressure is inadmissible.

### Conservative corrected Fick flux can have negative entropy

For three ideal species with molecular weights `.028,.032,.014 kg/mol`, take

    YL=(.36,.50,.14), YR=(.31,.505,.185),
    relative unequal D=(.02,25,.065),
    j_raw=−D*(YR−YL),
    j=j_raw−Y_mid*sum(j_raw).

This corrected mass-fraction-gradient law has `sum(j)=0`, but at equal temperature its entropy production is `−0.535339845` in the normalization used by the certificate. The diffusivity ratios are deliberately extreme; this is not a nitrogen transport estimate. It shows precisely why zero total mass, positive individual diffusivities and a conservative energy flux are not sufficient as a generic entropy proof. It does not condemn all mixture-averaged models: a properly weighted mole-fraction-gradient formulation can have a different, valid entropy argument.

## 7. What can be mapped to a flowing sheet

The model can answer a conditional local question: given prepared hot/cold layers, an explicit initial thickness and inventory, molecular transport/chemistry, and a stated pressure/width boundary, how do transverse composition and temperature evolve?

It does not establish that a nozzle or turbulent jet prepares those layers at the stated flow, pressure loss and work. It does not include entrainment generation, strain history, interface-area production, axial diffusion, radiation, surfaces, finite downstream cooling, or actual injector hardware.

The replacement `t=z/Uaxial` is allowed only after showing a common suitable convection speed, negligible axial transport, a compatible pressure/momentum field, the correct moving or fixed transverse geometry, and consistent inlet/outlet enthalpy and kinetic-energy fluxes. A pressure rise obtained in the closed rigid time history cannot simply become a free pressure rise along a steady low-Mach duct. Likewise, constant-pressure material expansion does not prove a constant-area flowing realization. These are different balance problems.

No gain should be credited from transverse or axial kinetic energy unless that energy is explicitly carried through and recovered by a permitted physical path. A total-enthalpy reduction cannot be claimed merely from static-temperature reduction.

## 8. Small transport-independent cap test, if needed

For ideal species with positive `cv_i`, any closed-rigid state with every local `T<=Tcap` satisfies

    U <= Σ_i n_i ubar_i(Tcap).

Therefore maximize the right side over nonnegative species mole inventories, the fixed nitrogen/oxygen atom totals, an explicitly stated retained `n_NO+n_NO2` interval, and any independently justified radical bounds. This is a linear program. If its maximum is strictly below `Uinitial`, no transport law can put every parcel below the cap without energy export under those inventory restrictions.

For the constant-pressure no-flux construction, use the analogous `H <= Σ_i n_i hbar_i(Tcap)` bound and compare with initial enthalpy. Do not use the internal-energy bound to exclude that different mechanical boundary.

A relaxed maximum above initial energy does not prove attainability, kinetics, a mixing rate or a feasible apparatus. Do not forbid additional beneficial NO or assume permanent radical storage without stating and justifying the constraints. The parent subsequently evaluated this bound on the actual source inventory. An independent four-species linear program reproduces every saved closed-form ceiling to within 4.66e-10 J/kg fresh. For packet NOx no greater than initially present and no radicals, the minimum export is 56,501.455 J/kg fresh in the prescribed-pressure mode and 105,171.233 J/kg fresh in the rigid mode. Exact polynomial stationary-point evaluation verifies positive cp and cv for all six source species over 200–1700 K. These checks are float64, not outward-rounded interval arithmetic; no statement below the thermochemistry's 200 K domain is implied. See `endpoint_independent_certificate.json`.

## Reproduce

Run `python nitrogen_lamella_20261022/closure/verify_closure.py`. It writes `certificate.json` and checks:

- positive and equivalent pressure denominators;
- zero closed-rigid width derivative and internal-energy derivative;
- EOS pressure derivative and global species conservation;
- equality of direct face entropy and Maxwell–Stefan friction plus Fourier conduction;
- the boundary-sensitive 1700 K counterexample;
- the conservative negative-entropy corrected-Fick counterexample.

There is no trajectory integration in this certificate.


## 9. Receiving NASA7 secant helper

`nasa_secant.py` supplies `nasa7_h_secant(TL, TR, low_coefficients, high_coefficients, gas_constants, splice_temperature=1000.)`. Coefficient arrays have last dimension seven, ordered a0 through a6. For the actual receiving kernel, use `low=K.nasa[:,8:15]`, `high=K.nasa[:,1:8]`, and `gas_constants=K.R/K.W`.

Within one branch the expression is

    hbar/Ri = TL TR [a0 log(TR/TL)/(TR−TL) + a1/2
                  + a2(TR+TL)/6
                  + a3(TR²+TR TL+TL²)/12
                  + a4(TR³+TR² TL+TR TL²+TL³)/20] + a5.

It evaluates the logarithmic divided difference using `log1p`, uses the exact enthalpy at equal temperatures, and combines crossed branches using beta-interval weights evaluated without subtraction of near-equal reciprocals. There is no arbitrary near-equal-temperature fallback or clipping.

Branchwise integration equals the chemical-potential secant only when the receiving standard potential g0/T is continuous at the splice. `splice_diagnostics` reports the discontinuities and does not modify coefficients. The actual source has only roundoff-scale discontinuities, with max absolute g0/T jump 1.82e-12 J/(kg K). Its 300–2700 K helper secants agree with direct source potential subtraction to within 7.46e-9 J/kg. Synthetic near-equal and cross-splice tests agree with independent beta-quadrature to within 4.1e-16 relative. The tests include 1000±1e-10 K and exactly equal endpoints.

`test_nasa_secant.py` and `nasa_secant_certificate.json` are synthetic-function tests. `check_endpoint_bound.py` and `endpoint_independent_certificate.json` are actual-source checks. Neither integrates a trajectory.
