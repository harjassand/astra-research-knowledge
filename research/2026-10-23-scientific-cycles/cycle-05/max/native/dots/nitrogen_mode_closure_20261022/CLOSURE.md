# A thermodynamic four-temperature closure, and what it cannot identify

## Result and scope

A constructive, conservative, entropy-producing finite-volume closure exists with one pressure-bearing bath temperature T and independent vibrational temperatures Tv,N2, Tv,O2 and Tv,NO. It requires more information than equilibrium thermochemistry/chemistry and empirical VT/VV times. In particular, chemical mode-energy partition and nonequilibrium reaction affinities/rates are not determined by those inputs. Two local constitutive models below agree on the entire equal-temperature chemical-rate manifold and have the identical VT/VV operator, yet give different instantaneous mode derivatives there and different chemistry away from it. Both conserve energy and produce nonnegative entropy. They do NOT have identical full coupled linear response: the derivative of chemical affinity with respect to mode inverse temperatures depends on the selected partition.

This is a mathematical closure and non-identifiability certificate, not a fitted nitrogen model, an attainable cooling trajectory, an exclusion result, or a modification of the frozen lamella checkpoint. No ODE/PDE is run. The quantities in check_algebra.py are explicitly synthetic, not measured constants.

Source context: nitrogen_lamella_20261022/DECISION.txt, vibrational/REPORT.md and closure/closure.md. This derivation uses their low-Mach material-slab mechanical contract and their convention of right-minus-left face jumps.

## 1. Thermodynamic state and one consistent split

Let i index all chemical species; V={N2,O2,NO}. For fixed cell mass per transverse area m_j, use states (Y_i,h,z_a), with z_a=Y_a e_va(Tva) the vibrational energy per unit mixture mass. All Y_i>0 and T,Tva>0 in this derivation. Set z_i=0 for species not in V. Use a declared ideal-mixture model:

    h = sum_i Y_i h_bi(T) + sum_a z_a,
    u = h − Rmix T,        v = Rmix T/P,
    Rmix = sum_i Y_i Ri,   Ri = Ru/Wi.

The bath carries ideal-gas pressure; the internal oscillators carry none. Define positive mode heat capacities c_va=de_va/dTva and entropies ds_va=c_va dTva/Tva. A harmonic choice, if justified, is e_va=Ri theta_a/(exp(theta_a/Tva)−1), with a matching harmonic entropy. Other monotone partition-function models are possible.

To match a selected equilibrium thermochemistry exactly on Tva=T, set

    h_bi(T)=h_eq,i(T)−e_vi(T),
    s_bi^0(T)=s_eq,i^0(T)−s_vi(T)

for represented modes, and leave unrepresented species in the bath. Use identical formation and entropy references throughout. Require cp_bi=dh_bi/dT and mixture Cv_b=Cp_b−Rmix>0, where Cp_b=sum Y_i cp_bi. Subtracting energy without subtracting the matching entropy is not a thermodynamic model. A harmonic subtraction from NASA equilibrium functions is a declared surrogate split, not a demonstration of exact spectroscopic populations. Positive bath heat capacity must be checked on the accepted domain.

The specific entropy is

    s = sum_i Y_i [s_bi^0(T) − Ri ln(X_i P/Pstd)]
        + sum_a Y_a s_va(Tva).

Introduce beta=1/T, beta_a=1/Tva, alpha_a=beta_a−beta, and

    Z_bi = h_bi/T − s_bi^0 + Ri ln(X_i P/Pstd),
    psi_a = e_va/Tva − s_va,
    Z_i = Z_bi + psi_i                   (psi_i=0 outside V).

The exact generalized Gibbs identity is

    ds = beta (dh − v dP) − sum_i Z_i dY_i + sum_a alpha_a dz_a.

Equivalently replace dh−v dP by du+P dv. Z_i has units J/(kg K); it is the composition conjugate at fixed mode energy, not the ordinary single-temperature g_i/T evaluated at an invented effective temperature. At thermal equilibrium Z_i=g_eq,i/T. The mass-fraction constraint allows a common additive conjugate gauge; it cancels for mass-conserving sources and fluxes.

## 2. Conservative material-cell balances

Let j_i be the species diffusive mass flux (sum_i j_i=0); F_a the total flux of mode-a energy; F_E the nonconvective total enthalpy flux. Let w_i be the chemical mass source per volume and S_a the mode source per mixture mass per time. Then

    Ydot_ij = −Delta j_ij/m_j + w_ij/rho_j,
    zdot_aj = −Delta F_aj/m_j + S_aj,
    hdot_j  = v_j Pdot − Delta F_Ej/m_j.

There is no separate chemical heat or internal-exchange source in the last equation: formation energies and all represented internal modes are already in h. Chemical reactions conserve total energy locally; external radiation, laser absorption or wall exchange would require an explicitly signed external energy source. Local mode exchange must be compensated in bath energy.

For transport it is essential to use

    F_a = ebar_va j_a + q_a,
    F_E = q_b + sum_i hbar_bi j_i + sum_a F_a.

Here q_a is conductive/cross-coupled mode energy flux relative to species convection, not its species-carried contribution. Thus actual internal energy travels with diffusing molecules and is accounted for in both the mode equation and total energy. It is not legitimate to use equilibrium h_eq(T) in total diffusive enthalpy while carrying e_va(Tva) in a separate mode equation unless the missing difference is explicitly restored. Omitting a term from both balances can leave global energy formally conserved but gives the wrong internal-energy transport and in general loses the entropy proof; adding a mode flux to total energy twice instead creates double counting.

Define

    B_j = −Delta F_Ej/m_j − sum_i h_bi(T_j) Ydot_ij − sum_a zdot_aj.
    Tdot_j = (v_j Pdot+B_j)/Cp_bj.

The term −sum zdot includes species transport and chemical mode production. Since z_a=Y_a e_va, recovering Tva requires

    Tvdot_a = [zdot_a − e_va Ydot_a]/(Y_a c_va).

Ignoring the second term treats production/destruction of vibrational carriers incorrectly.

### Mechanical alternatives

For constant pressure, Pdot=0; insulated impermeable boundaries give Hdot=0 and Udot=−P Ldot. For a closed rigid material slab, L=sum m_j v_j fixed:

    Pdot = sum_j m_j [Rmix_j B_j/Cp_bj + T_j Rdotmix_j]
           / sum_j m_j v_j (Cp_bj−Rmix_j)/Cp_bj.

This is the previous closure with the explicit bath heat capacity and mode derivatives, not total equilibrium cp. Its denominator is positive on stable states. Then U=H−PL is conserved at zero external flux. Low-Mach and acoustic/geometry admissibility remain separate obligations.

## 3. Exact finite-volume entropy production

One internal face contributes

    sigma_face = F_E Delta beta − sum_i j_i Delta Z_i
                 + sum_a F_a Delta alpha_a.

A cell source contributes m_j[-sum_i Z_i w_i/rho + sum_a alpha_a S_a]. These follow by differentiating the cell entropy, not by midpoint approximation of a continuum entropy law.

For uniform thermodynamic pressure choose the Gibbs secants

    hbar_bi = Delta[h_bi(T)/T − s_bi^0(T)] / Delta beta,
    ebar_va = Delta[e_va(Tva)/Tva − s_va(Tva)] / Delta beta_a.

Use h_bi or e_va at equal temperatures and stable divided-difference implementations near equality. These are beta-averaged energies, generally not arithmetic means. Since d(h_b/T−s_b)/d beta=h_b and d(e_v/Tv−s_v)/d beta_v=e_v,

    sigma_face = q_b Delta beta + sum_a q_a Delta beta_a
                 − sum_i j_i Ri Delta ln X_i.

This proves the necessary cancellation of species-carried internal energy at finite face jumps. A constructive class is

    a_i=Ri Delta ln X_i,
    j=−M a,       M=M^T positive semidefinite, M 1=0,
    q_b=Lambda_b Delta beta,
    q_a=Lambda_a Delta beta_a,              all Lambda>=0.

It gives sigma_face=Lambda_b(Delta beta)^2+sum Lambda_a(Delta beta_a)^2+a^T M a>=0. Fourier q_b=−k_b Delta T/d corresponds to Lambda_b=k_b T_L T_R/d; likewise for each mode. A full symmetric positive-semidefinite Onsager matrix on the force vector (Delta beta,Delta beta_a,−a_i), preserving zero total diffusive mass, permits reciprocal cross terms. Setting cross terms to zero is a mathematically allowed restriction, not measured negligibility.

The logarithmic-mean Maxwell–Stefan construction already proved in closure/closure.md can supply the species flux here unchanged: the remaining species force is precisely Ri Delta ln X_i. The base/mode secants replace the earlier equilibrium enthalpy secant. Temperature- and mode-dependent transport coefficients still need physical identification. This is a constructed alternative Onsager/face closure, not an identified empirical Maxwell–Stefan/Soret/Dufour law or an immediate retrofit of the old solver.

Strictly positive state support was assumed. Zero species/mode populations require justified limits and positivity-compatible flux/source definitions; this local derivation alone does not give a globally invariant numerical domain. Entropy production at the semidiscrete level also does not certify a chosen time integrator.

## 4. Internal exchange: what the signs require

### VT

A simple finite-reservoir VT law is

    S_a,VT = Y_a [e_va(T)−e_va(Tva)]/tau_a,     tau_a>0.

The bath source is minus this quantity in the split energy budget. Its entropy is alpha_a S_a,VT>=0 because e_va increases with temperature. Multiple collider rates may add only within their justified mixture/rate regime. Finite bath energy must evolve; prescribed sink temperature is a different open-system assumption.

### VV and mismatched quanta

For a forward elementary event which removes epsilon_a from mode a, adds epsilon_b to mode b, and deposits epsilon_a−epsilon_b in the bath,

    S_a=−epsilon_a J,     S_b=epsilon_b J,
    S_bath=(epsilon_a−epsilon_b) J,
    sigma_event=J A,
    A=epsilon_a(beta−beta_a)+epsilon_b(beta_b−beta).

Energy is conserved exactly. Equal quanta give A=epsilon(beta_b−beta_a); unequal quanta generally do not. A detailed-balance-consistent forward/reverse pair has Jplus/Jminus=exp(A/kB) for per-molecule energies, or exp(A/Ru) for per-mole energies, and hence J A>=0. Reduced Boltzmann mode descriptions may average over many such events; a single empirical time does not specify those channels or their reverse rates.

The algebraic counterexample takes T=1000, Tva=2000, Tvb=1500 and positive quantum energies epsilon_a=1, epsilon_b=4 in arbitrary consistent units. Although a is hotter than b, a stipulated forward event has A=−0.0008333333<0. Therefore merely transferring a population quantum from the hotter mode to the colder mode without enforcing the bath-dependent affinity can lower entropy. Depositing both quantum energies as equal would conserve neither the stipulated transition energetics nor its affinity. These numbers are a structural counterexample, not N2/NO spectroscopic data.

## 5. Chemistry: explicit non-identifiability

For reaction r with molar stoichiometry nu_ir (products positive), choose mode energy production eta_ar per mole of reaction advancement. For rate r_r in mol/(volume time), set

    w_i = sum_r Wi nu_ir r_r,
    S_a,chem = sum_r eta_ar r_r/rho,
    A_r = −sum_i Wi nu_ir Z_i + sum_a alpha_a eta_ar.

A_r is the entropy affinity in J/(mol K), not Gibbs energy. The chemical entropy production per volume is sum_r r_r A_r. Total h has no chemical source; the bath receives the energy implied by the stoichiometric formation-energy change and these selected mode sources. Atom/mass conservation requires stoichiometrically valid nu, for example N2+O <=> NO+N in the represented nitrogen mechanism.

A local thermodynamic construction is

    r_r = 2 k_r sinh[A_r/(2 Ru)],       k_r>=0,

or forward/reverse rates k_r exp[+/-A_r/(2 Ru)]. It has r_r A_r>=0. k_r has rate units; this is a permissible constitutive class, not a proposed measured mechanism. On the equal-temperature manifold alpha=0, A_r is independent of every eta_ar. Given consistent one-temperature forward/reverse rates, set k_r=sqrt(rplus_eq rminus_eq) there to reproduce them exactly; infinitely many nonnegative off-manifold extensions remain.

Take two models with identical thermodynamics, stoichiometry, transport and VT/VV laws, and the same k_r on that manifold. Choose eta=0 in one and eta=c in the other for one represented mode. At an interior equal-temperature state with nonzero reaction affinity, both models have exactly the same chemical rate and entropy production, but their mode-energy production differs by c r_r. Their bath-temperature derivatives differ correspondingly while total energy is identical. Even starting at thermal equilibrium therefore does not select the next mode-temperature derivative from equilibrium chemistry alone.

In normalized units Ru=1, k=1, chemical contribution −sum Wi nu_i Zi=1, the script uses c=1. Both rates at alpha=0 are 1.0421906109874948, whereas mode sources are 0 and 1.0421906109874948. At alpha=−0.5 the rates become 1.0421906109874948 and 0.5052246336163366; both entropy productions stay positive. These normalized scalar calculations instantiate the exact channel algebra for any mass/atom-balanced channel and an interior thermodynamic state with that affinity; they are not nitrogen parameter choices.

This is a LOCAL constitutive non-uniqueness proof. Arbitrary constant eta need not preserve physical state bounds globally, and a vibrational-temperature ansatz need not correspond to the actual reaction-state distribution. The example does not claim to construct a globally admissible nitrogen kinetic mechanism. For a sufficiently small local interval at positive populations/energies, finite source derivatives have no boundary issue. Requiring microscopic state-to-state kinetics would further constrain eta and rates, but precisely that information is absent from equilibrium reaction rates and aggregate VT/VV times.

Conversely, keeping one-temperature chemical rates unchanged for every off-manifold state while independently assigning arbitrary eta generally fails: the sign of A_r can change while the inherited rate does not. A nominally reversible mechanism can then have negative entropy production. In the same normalized example, eta=3 and alpha=−0.5 makes A_r=−0.5 while the retained one-temperature rate is positive. Thus conservation alone cannot repair an arbitrary chemistry/mode partition.

## 6. What this establishes for the lamella

1. Separate Tva states can be added without double-counting NASA energies, but only with a declared energy AND entropy split, finite bath balance, generalized chemical affinities, mode-resolved species transport, and a compatible chemistry source partition.
2. Existing equilibrium chemistry and measured aggregate VT/VV times alone do not determine those terms. Entropy and conservation constrain their structure but not their physical magnitudes or the missing channel populations. No scalar relaxation filter closes the gap.
3. Rotations/electronic states are assumed equilibrated with the pressure-bearing bath in this reduced closure. Trace NO2 has been assigned to that bath, not proved instantaneously equilibrated. Mode-specific transport, state-selective chemical production/destruction, high-vibrational-tail populations, third-body effects and bath-assisted mismatched-quantum transfer all remain potential load-bearing omissions. The measured N2–O/NO/O2 information in the prior report is necessary but not sufficient.
4. The separately supplied caloric_counterexample.py uses the correct identity H=H_eq(T)−E_v,eq(T)+E_v,stored. Its Tv inversion and sign are correct: positive residual bath cp makes a larger stored vibration inventory lower bath T at fixed H and composition. It constructs 1687.597770 K bath / 1959.507539 K N2 vibration instead of 1724.578691 K equilibrium bath at the same packet H and selected composition. This is a possible caloric state in that split, not a reachable history. Preserved initial N2 vibration despite composition changes is stipulated, redistribution is assumed, other modes are equilibrated, sampled cp positivity is not an interval proof, and the dynamical path is not checked. The parent's additional scalar entropy screen uses the consistent split S=S_eq(T)−nN s_v(T)+nN s_v(Tv); its global increase from 15382.78260 to 16393.58261 J/(kg-fresh K), below the equal-temperature value 16396.74530, passes a necessary global entropy check but not kinetic reachability. These are fixed-H, prescribed-pressure states, not fixed-U, fixed-volume states. It shows why the missing physics need not worsen the transient bath cap; it does not establish useful cooling.
5. A translational cap is not the fully relaxed endpoint predicate. Stored mode energy must still be accounted for before a 300 K reset. The existing conditional >=53.995 kJ/kg-fresh endpoint export requirement is neither removed nor converted to SEC by this construction. Injector/geometry, finite export area, pressure/actuation work and closed recycle inventory remain outside this constitutive result.

## Reproduce

Run `python nitrogen_mode_closure_20261022/check_algebra.py`. It writes algebra_results.json and checks the exact finite-face entropy identity, zero total species flux, positive VT entropy, conservative exchange bookkeeping, equal-manifold/unequal-mode-source chemical non-identifiability, and the mismatched-quantum VV counterexample. This is an algebraic float64 test, not outward-rounded arithmetic or physical validation.
