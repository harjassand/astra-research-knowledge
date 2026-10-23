# Compressible material-slab balance check

## Result and limits

The proposed staggered compressible equations have the correct signs, mass accounting and global energy ledger, subject to the qualifications below. Equal constant exterior pressures conserve

    I = sum_j mu_j e_j + 1/2 sum_k m_k u_k^2 + P0 (x_N - x_0).

They do not conserve total enthalpy. Viscosity transfers staggered kinetic energy into internal energy with nonnegative entropy production. Fixed cell masses remain valid with species diffusion because the diffusive fluxes have zero total mass.

`verify_compressible_balance.py` proves the mechanical cancellation with exact rational arithmetic, including unequal exterior loads and nonzero boundary heat flux. It also checks one four-cell, nonuniform-pressure RHS state using the actual pinned six-species thermochemistry, chemistry and binary diffusivities. There is no integrated compressible trajectory here and no bound on the 1700 K decision. The arithmetic-face/full-cross trajectory in the receiving code is not certified by the separate logarithmic-face entropy test.

The earlier estimated Mach number 0.089 is not a temperature-error bound. In particular, a roughly 6 K margin does not license calling the compressibility error negligible. M squared is about 0.0079; its size alone supplies neither the coefficient, sign nor a bound on the maximum-temperature discrepancy. An actual converged compressible comparison or a rigorous perturbation bound remains necessary.

## 1. State, units and equations

Use cells j=0,...,N-1 and nodes k=0,...,N. All extensive quantities are per transverse area. Let

    mu_j > 0                     cell mass [kg/m2], fixed
    l_j = x_(j+1) - x_j > 0      cell width [m]
    rho_j = mu_j/l_j             density [kg/m3]
    u_k = dx_k/dt                node velocity [m/s]
    m_0 = mu_0/2
    m_N = mu_(N-1)/2
    m_k = (mu_(k-1)+mu_k)/2      internal node mass [kg/m2].

The equation of state is cell-local:

    R_j = sum_i Y_ij Ru/W_i,
    P_j = rho_j R_j T_j.

Do not retain the low-Mach scalar pressure closure in this system. Pressure is no longer a single spatially uniform algebraic variable.

With positive shear viscosity eta_j and bulk viscosity zeta_j >= 0, define

    du_j = u_(j+1) - u_j,
    tau_j = (4 eta_j/3 + zeta_j) du_j/l_j,
    pstar_j = P_j - tau_j.

Thus tau is positive for expansion and negative for compression. The proposed 4 eta/3 law sets bulk viscosity to zero: it is the Stokes assumption, not a measured demonstration that nitrogen vibrational/bulk-viscous relaxation is negligible. Pressure and tau have units Pa. The force per area on an internal node is pstar_(k-1)-pstar_k.

For exterior compressive tractions P_L and P_R,

    m_0 udot_0 = P_L - pstar_0,
    m_k udot_k = pstar_(k-1) - pstar_k, 0 < k < N,
    m_N udot_N = pstar_(N-1) - P_R.

The equal-load case is P_L=P_R=P0. Do not also prescribe endpoint velocity or the pressure of the adjacent whole cell to equal P0. Those would be additional conditions. The traction is P-tau, not P alone.

Let J_if denote species diffusive mass flux to the right [kg/(m2 s)], and Q_f the total nonadvective energy flux to the right [W/m2]. Then

    Ydot_ij = -(J_i,j+1 - J_i,j)/mu_j + omega_ij/rho_j,
    mu_j edot_j = -pstar_j du_j - (Q_j+1 - Q_j).

Here omega has units kg/(m3 s). No factor l or rho is missing: mu=rho l. The heat/species flux must be

    Q = q_reduced + sum_i hbar_i J_i,

with full formation-containing species enthalpies, even though the evolved thermodynamic variable is internal energy. Using species internal energy in this diffusive flux omits the diffusion-associated partial-pressure work. In the continuum hbar tends to h_i(T); the receiving NASA secant is suitable for the discrete entropy construction below.

With e_i(T)=h_i(T)-Ri T and cv=sum_i Y_i(cp_i-Ri),

    cv_j Tdot_j = edot_j - sum_i e_i(T_j) Ydot_ij.

This follows by differentiating e=sum_i Y_i e_i(T). It has neither a v Pdot term nor an extra reaction heat. The formation energies already include reaction heat. A separate chemical heat source would count it twice.

Boundary insulation and impermeability mean J_i,0=J_i,N=0 for every species and q_reduced,0=q_reduced,N=0, hence Q_0=Q_N=0. Q=0 alone would not prohibit compensating species-energy exchange.

This is a standard single-barycentric-velocity compressible Navier–Stokes–Fourier/multicomponent-diffusion approximation. It does not retain finite diffusion-velocity inertia, higher-order kinetic transport or a state-resolved internal-mode nonequilibrium model.

## 2. Exact mechanical identity and no mass double counting

Write U=sum mu e and K=1/2 sum m u squared. Since nodal masses are fixed,

    Kdot = sum_k u_k (m_k udot_k)
         = sum_j pstar_j du_j + P_L u_0 - P_R u_N.

The pressure/stress sum cancels the entire mechanical part of Udot, including viscous work. Therefore

    (U+K)dot = P_L u_0 - P_R u_N + Q_0 - Q_N.

For equal constant exterior pressure and insulated endpoints this is

    (U+K+P0 L)dot = 0, L=x_N-x_0.

The gas does signed work P0 dL on the external load. For time-varying common Pext, the derivative of U+K+Pext L equals L Pextdot; the constant-P0 invariant cannot be reused unchanged.

Momentum obeys

    d(sum_k m_k u_k)/dt = P_L - P_R.

Equal exterior loads therefore conserve total momentum as well as the energy/work invariant.

The nodal masses satisfy sum m=sum mu exactly. Each cell allocates half its mass to each end, not its entire mass to both ends. Using the same physical mass in internal and kinetic energy is not double counting: they are distinct energy modes. The kinetic quadrature is nevertheless mass-lumped. For a piecewise-linear velocity in one cell,

    K_lumped,j = mu_j (u_j^2 + u_(j+1)^2)/4,
    K_exact_linear,j = mu_j (u_j^2 + u_j u_(j+1) + u_(j+1)^2)/6,
    difference = mu_j (u_(j+1)-u_j)^2/12 >= 0.

The invariant is exactly the lumped K, not the latter continuum quadrature. Mesh refinement must resolve that difference. A real piston or membrane with additional inertia would require its own mass and kinetic-energy budget; endpoint gas half-masses do not represent it.

## 3. Entropy and the nonuniform-pressure transport drive

For ideal-gas chemical potentials g_i,

    T ds = de + P dv - sum_i g_i dY_i.

Since mu_j vdot_j=du_j, the mechanical entropy production is

    sigma_visc,j = tau_j du_j/T_j
                 = (4 eta_j/3+zeta_j) du_j^2/(l_j T_j) >= 0.

The complete semidiscrete entropy identity is

    Sdot = sum_j sigma_visc,j
           + sum_internal_faces [Q_f Delta(1/T) - sum_i J_if Delta(g_i/T)]
           - sum_j mu_j sum_i (g_ij/T_j) omega_ij/rho_j.

The chemical term is nonnegative for this detailed-balance-consistent source at physical positive states; signed Newton extensions are not physical entropy certificates. The mechanical identity itself holds regardless of the transport closure.

For ideal gases without differential body forces, the continuum Maxwell–Stefan drive is

    d_i = grad X_i + (X_i-Y_i) grad ln P,
    sum_i d_i=0.

Use this d, rather than grad X alone, on the RHS of the existing Maxwell–Stefan solve. The solver accepts an arbitrary zero-sum vector despite its argument name `grad_X`. Use face-local positive pressure to evaluate rho and binary diffusion coefficients.

The derivation of the pressure projection follows from

    a_i = Ri [grad ln X_i + grad ln P],
    Ri d_i/X_i = a_i - Rmix grad ln P.

The final term is species-independent, so its contraction with any zero-total-mass flux vanishes. This is why Xi-Yi, rather than Xi alone, is the correct pressure contribution.

If DT_i denotes a thermal diffusion coefficient in kg/(m s), with sum DT_i=0, the receiving continuum thermal-cross convention is

    J_i,Soret = -DT_i grad T/T,
    q_Dufour = -T sum_i DT_i Ri d_i/X_i.

Both the sign and units of this reciprocal Dufour term are correct: the result has units W/m2. Replacing d_i by grad X_i only in Dufour would omit the pressure cross effect and break reciprocity with the complete species driving force. The zero-total-mass gauge term also drops out of its DT contraction. Treat absent species with a justified limiting formula; dividing by Xi=0 is not a physical prescription.

The cited Cantera primary documentation defines DT in exactly this Soret convention: [Transport thermal diffusion coefficient reference](https://www.cantera.org/dev/cxx/d2/dfb/classCantera_1_1Transport.html). Its [one-dimensional governing equations](https://www.cantera.org/stable/reference/onedim/governing-equations.html) also state the mass-frame Soret flux. Those pages establish coefficient convention, not a certificate for the new compressible discretization.

## 4. Important finite-volume pressure correction

A continuum-consistent face is not automatically an entropy-stable face. At nonuniform pressure the thermochemical secant gives

    a_i = Delta(g_i/T) - hbar_i Delta(1/T)
        = Ri [Delta ln X_i + Delta ln P].

Let ell_i be the species logarithmic mean, S=sum_i ell_i, Xstar_i=ell_i/S and Ystar_i=Wi Xstar_i/Wstar. If keeping the existing raw composition finite difference Delta X/dx, the entropy-compatible pressure drive is

    dstar_i = Delta X_i/dx
              + S (Xstar_i-Ystar_i) Delta ln P/dx.

Then

    dstar_i/Xstar_i = S/dx [Delta ln X_i
                          + (1-Ystar_i/Xstar_i) Delta ln P],

and the mass-frame projection yields the exact positive friction identity

    -sum_i J_i a_i
      = cstar Ru dx/S sum_(i<k) Xstar_i Xstar_k (V_i-V_k)^2/D_ik >= 0.

Together with q=-k Delta T/dx and the NASA hbar secant, this certifies the no-Soret face. An alternative is to divide the composition gradient by S and keep the pressure term unscaled; this is also entropy-compatible but changes the finite-grid transport magnitude. Both approach the continuum drive as dx tends to zero.

Simply adding (Xstar-Ystar) Delta ln P/dx to the old raw logface gradient omits S. The executable two-species counterexample has XL=(.55,.45), XR=(.45,.55), W=(14,46), pressure ratio 1.45586467 and positive temperatures. The naive drive gives entropy production -3.11023e-5 W/(m2 K), despite zero total mass flux; the corrected drive gives +3.39719e-5. This is a counterexample to unconditional certification, not an estimate of the actual trajectory's entropy error. Arithmetic faces likewise have no exact general proof.

There is an additional temperature-jump issue for full cross terms. With the above hbar, positive endpoint temperatures TL,TR, arithmetic Tf and the usual finite-difference Soret flux, exact discrete reciprocal pairing would require

    q_Dufour,discrete = -TL TR/(Tf dx) sum_i DT_i a_i
                     = -TL TR/(Tf S) sum_i DT_i Ri dstar_i/Xstar_i.

The simple continuum expression -Tf sum DT_i Ri dstar_i/Xstar_i agrees only in the small-jump limit (where S tends to one and TL TR/Tf squared tends to one). Reciprocity alone also does not prove nonnegative full-cross entropy: the coupled mobility matrix must be positive semidefinite. The full actual-source Soret/Dufour operator is not certified by this diagnostic. Do not claim it is merely because the no-Soret friction identity passes.

## 5. Boundary admissibility and meaningful comparison

This boundary is a pressure-loaded, closed material slab with impermeable, insulated moving ends. It can be used as an explicit idealized mechanical contract. It is not a demonstrated free jet at one atmosphere. A real interface between miscible hot/cold/ambient gases generally permits heat and species exchange; a free jet also has axial momentum, entrainment, shear and pressure-loss balances. A physical membrane or piston, if used to impose the ideal boundary, brings new inertia, losses, materials and heat paths.

Nor may these traction conditions simply be relabeled as the old reflecting symmetry planes in a repeated cold/hot/cold array. Reflection, periodic repetition and exterior loading are distinct mechanical boundary conditions. A repeating-array embedding must specify the motion and momentum balance of its symmetry planes consistently. The local pressure-loaded result does not prove such an embedding.

For a compressible comparison, retain the same mu, initial widths, T and Y and specify u(0). At-rest initialization retains the physical acoustic initial layer of that idealized preparation. Assigning the reconstructed low-Mach velocity instead is a different, well-prepared initialization with additional initial K; include it in the inventory rather than silently treating it as free. A sharp initial thermal/composition jump is still mesh-regularized and requires refinement or an admitted finite initial thickness.

Required trajectory diagnostics include positive widths and compositions; EOS/thermochemistry domains; conservation of I and momentum; atom totals; staggered Mach numbers; mechanical/transport entropy; time-step and spatial refinement; and the actual difference in maximum temperature near its minimum. A transient static-temperature dip during expansion can rebound as acoustic kinetic energy dissipates. Track the entire required observation window, not only a favorable saved sample. None of the algebraic checks alone admits the injector, free-jet realization, thermal cap or energy advantage.

## Reproduction and obtained checks

Run:

    python nitrogen_lamella_20261022/compressible_check/verify_compressible_balance.py

Outputs are `certificate.json`, with supporting `mechanics.py`. The certificate includes source hashes. On the present source:

- Exact rational mechanical energy, general boundary power, nodal mass and equal-load net force residuals: exactly zero.
- Actual-source four-cell RHS relative energy-rate residual: 1.4570e-15.
- Maximum total species diffusive mass flux: 2.2430e-18 kg/(m2 s).
- Actual-source no-Soret face entropy/friction identity absolute error: 1.1369e-13 W/(m2 K).
- Actual-source total entropy budget absolute error: 4.5475e-13 W/(m2 K).
- Viscous entropy production: 0.0525671 W/(m2 K), positive.

The exact-rational checks are exact only for their explicitly constructed finite values. The actual-source checks are float64 pointwise tests, not outward-rounded bounds, solution-existence proofs, time-integration certificates, apparatus predictions or maximum-temperature error estimates.
