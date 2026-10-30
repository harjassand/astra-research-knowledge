# Quantum renewal through a symmetry-preserving physical port

Working derivation, 30 October 2026. Earlier accepted results and the previous neutral-block construction are unchanged. These are new root-working results. The central construction is an interacting Hubbard star whose real central source can act irreducibly on auxiliary degrees of freedom while acting identically on a logical qubit. Electrostatic screening and a passive spectral filter supply two useful physical interfaces. This is not a completed device threshold or an established experimental advantage.

## 1. What changed the attack

The preceding construction protected total-spin-zero logical states while making finite charge excursions. Its remaining difficulty was the full exposure to charge disturbances, particularly beside a neighbor with changed particle number. A correct code-endpoint argument could not remove those interactions during capture, return, sensing or renewal.

The first investigation here supplied an exact orbital permutation on the entire dimer Fock space. For odd q>=3, effective repulsion U>0 and zero detuning,

\[
g/U={q\over2(q^2-1)},\qquad
\tau={\pi(q^2-1)\over U},\qquad
e^{-iH\tau}=e^{iq\pi N/2}P_{\rm orbital}.
\]

This is verified for all particle numbers 0 through 4, with fermionic permutation signs retained. It makes charge sign reversal meaningful even on leakage states. An intradimer capacitance adds a known N-dependent phase without changing the occupation interchange. Hubbard double-occupancy revival gates themselves are established physics; the all-sector permutation is the specific useful identity checked here.

The direct-refocusing route did not produce a persuasive physical operating region. Dilution weakens the desired dipole interaction faster than some leakage-sensitive fields. Finite swap pulses accumulate spectator interactions, and a new charge fault during an echo leaves a partial-area phase. With m sign changes, some jump time has remaining signed area at least T/[2(m+1)]. An echo that refocuses an initially leaked neighbor therefore does not automatically localize faults occurring during the cycle. Nor does finite-pulse identity cancellation automatically give a dynamically corrected entangling gate.

The stronger opening is to protect the information against a useful source itself, including its charge motion, and give unwanted direct interactions a physically derived locality bound.

## 2. The physical star and its exact protected factor

Take four spinful orbitals: center 0 and three identical outer orbitals 1,2,3. Equal central-to-outer hopping, equal outer potentials and charging parameters, equal center-outer capacitance V_c and equal outer-outer capacitance V_o give

\[
H_\star=U_cD_c+U_o\sum_jD_j+epsilon n_c
-t\sum_{j,\sigma}(c_{c\sigma}^\dagger c_{j\sigma}+\mathrm{h.c.})
+V_c n_cN_o+V_o\sum_{j<k}n_jn_k.
\]

Here D_i=n_{i\uparrow}n_{i\downarrow}, N_o=sum_j n_j, and the sums run over the three outer sites. A real equilateral geometry and symmetric electrostatic boundary conditions can supply these equalities. A T-shaped graph with equal exchange is not by itself an electrostatic S3 symmetry.

Let Gamma(pi) be the fermionic second-quantized permutation of the outer sites. It includes signs from permuting occupied fermion modes. Every displayed term commutes with every Gamma(pi).

In the N=4,S=0 sector, the representation decomposes as

\[
\mathcal H_{4,0}\cong A_1^{\oplus5}\oplus A_2\oplus
(\mathbb C^2_L\otimes\mathbb C^7_G).
\]

The familiar two four-spin singlets lie in the standard representation E=\mathbb C^2_L. Their charge excitations supply seven copies, which form the gauge factor G. Schur's lemma gives, on this entire 14-dimensional component,

\[
H_{\rm invariant}=I_L\otimes H_G.
\]

This is exact in the one-orbital Hubbard model. It does not use a small-t/U exchange expansion, a cold gauge, a fixed central occupation, or a classical bath.

### Extension across particle and spin sectors

The complete four-orbital Fock space has dimension 256. Its S3 characters on identity, transposition and three-cycle are (256,0,16), obtained from the fermionic trace det(I+P) for each spin. Therefore

\[
\boxed{\mathcal F_4=A_1^{\oplus48}\oplus A_2^{\oplus48}
\oplus(\mathbb C^2_L\otimes\mathbb C^{80}_G).}
\]

In particular, c_{c\sigma}, c_{c\sigma}^\dagger, all central spin operators, central charge, total outer charge and collective outer spin commute with S3. A physical central electron lead can exchange particles and spin while preserving L. The ordinary N=4,S=0 code is a special gauge preparation inside this larger subsystem.

This protection does not assert that arbitrary charge noise is harmless. Individual outer potentials and site-resolved outer leads need not commute with S3. Equal independent noise strengths supply a permutation-covariant channel, which is weaker. The executable counterexample with equal independent outer D[n_j] dephasing has reference-infidelity derivative 0.0574198073 at t/U=.1, epsilon/U=.4; a central n_c channel and one collective N_o channel have zero derivative to numerical precision.

## 3. Full source instruments and retained histories

Suppose the total joint Hamiltonian, including arbitrary retained apparatus M, commutes with the outer-site permutations acting on the block alone. On the standard component it has the form

\[
H=I_L\otimes H_{GM}.
\]

Every source instrument obtained by evolving this Hamiltonian and reading source variables consequently has

\[
K_{r,\alpha}=I_L\otimes B_{r,\alpha}.
\]

Products for arbitrary records and time-dependent invariant controls retain this form. Several modules may share a noncommuting interacting apparatus, provided it commutes with each protected module's independent S3 action. A bad charge or irrep state in one module does not remove identity action on another protected module.

This proves preservation of the useful logical subsystem without resetting the retained environment. It includes source readout and source quantum backaction, rather than just a correct classical label.

There is a necessary conditioning qualification. If L and G were already correlated, measuring G can steer L on a selected record. Factorization does not make all record probabilities independent of L under pre-existing correlations. The trace-preserving source operation preserves rho_LR for every external reference R; successful-record-only preservation requires additional hypotheses. Fixed-deadline renewal, with every record retained or summed consistently, is the default construction here.

An invariant port cannot prepare an E resource from the vacuum, which belongs to A1. An initial asymmetric singlet preparation, its verification, and its cost remain necessary. Nor can this port repair leakage into a different S3 irrep. Existing leakage-reduction cells remain separate supplied operations; their implementation has not been silently transferred to the new bus hardware.

## 4. The difficult algebraic step: the physical port can reach the gauge

Logical blindness alone could leave inaccessible hot gauge states. Two results rule out that algebraic obstruction in the specified interacting models.

### 4.1 Central density reaches all seven charge gauges

There is a gauge basis in which

\[
D=\operatorname{diag}(0,1,1,1,1,2,2),\quad
N=\operatorname{diag}(1,0,2,1,1,0,2),\quad
H_G=UD+tT+\epsilon(N-I).
\]

The nonzero symmetric entries of T are

\[
T_{01}=\sqrt3,\ T_{02}=-\sqrt3,\ T_{13}=-\sqrt2,
\ T_{23}=1/\sqrt2,\ T_{24}=\sqrt{3/2},
\ T_{35}=1,\ T_{36}=2,\ T_{45}=\sqrt3.
\]

Every hopping edge changes N by one, so

\[
[N,[N,H_G]]=tT.
\]

For nonzero t and U, the algebra generated by H_G,N therefore contains T,D,N. Their joint spectral projectors resolve basis indices 0,1,2,5,6 and the two-dimensional space {3,4}. The operator P_34 T P_1 T P_34/2 resolves |3><3|; subtraction resolves |4><4|. Nonzero T edges then connect all seven basis vectors, generating every matrix unit. Thus

\[
\boxed{\{H_G,N\}'=\mathbb C I\quad(Ut\ne0).}
\]

This is an exact source law requiring only coarse information: fine values of U,t,epsilon are not needed to know that central-density cooling has no inaccessible gauge factor. It also includes the symmetric physical capacitances: at N_total=4 their diagonal energy is (U_o−V_o)D+f(N), because D_c=N(N−1)/2 and N_o=4−N. The function f is a quadratic polynomial, already in the algebra generated by N. The same proof therefore requires only t(U_o−V_o)!=0, with arbitrary central charging and symmetric V_c,V_o. Actual rates require nonzero lower bounds and a bath spectrum. In the noninteracting example U=0,V_c=V_o=0 the calculation exhibits three dark components. Absence of a dark component does not give a uniform rate as t or U tends to zero.

The independent root code supplies an exact finite-field rank certificate: the rational commutant problem has rank 48 on 49 unknowns. The analytic argument above gives the broader nonzero-U,t statement.

### 4.2 A central particle port reaches the full 80-dimensional gauge

Consider the joint algebra of H_star and c_{c up},c_{c down}, with their adjoints. An operator in its commutant must first have form I_center tensor X_outer, because the central creation and annihilation operators generate the complete central-site matrix algebra. Commuting with the hopping then forces

\[
[X_o,C_\sigma]=[X_o,C_\sigma^\dagger]=0,
\qquad C_\sigma=\sum_{j=1}^3c_{j\sigma}.
\]

For zero mutual capacitances, H_outer=U_o sum D_j−mu N_o. Commutation with H_outer and C_sigma gives the separately summed transitions between empty and singly occupied sites, and between singly and doubly occupied sites: [sum D_j,C_sigma] isolates the latter. Their graded anticommutators generate all collective even local matrix units; all odd local matrix units are already available. For example two of the diagonal anticommutators sum to N_o, after which sum D_j is recovered explicitly.

With physical V_c !=0, the central n_c coefficient separately forces [X_o,N_o]=0. Using

\[
H_o=(U_o-V_o)\sum D_j+{V_o\over2}N_o(N_o-1)-\mu N_o,
\]

the same proof works whenever U_o−V_o !=0.

These are the collective gl(2|2) matrix units on the three local spaces {|0>,|up>,|down>,|double>}, with their fermionic grading. Super Schur-Weyl duality identifies their commutant as the signed permutation algebra. Equivalently, on the standard component their gauge action is the complete matrix algebra. A direct rational/modular calculation confirms rank 399 on the outer gauge's 400 commutant unknowns. The central factor then gives the full gauge dimension 4*20=80.

This is the specific interaction-enabled port construction. It is an application of established subsystem and representation theory, not a new claim to Schur-Weyl duality. The same reasoning extends to identical Hubbard leaves around one central orbital, with logical carriers given by the represented permutation irreps.

### What the algebra does and does not imply about cooling

For a finite-temperature Davies generator with positive forward and reverse rates over the needed transition band, detailed balance supplies a faithful restricted Gibbs state. The scalar commutant then implies uniqueness, and the self-adjoint jump structure excludes a nondecaying gauge factor. One must not apply the commutant statement to an arbitrary dissipator and conclude unique mixing: Evans irreducibility alone is insufficient without the relevant conditions.

A finite central lead still may renew slowly. In a charge plateau, low spin excitations cannot necessarily decay by a downhill sequential particle hop. Thermal activation or cotunneling may set the rate. Algebraic accessibility is not a usable cold source by itself.

For U=1,t=.1,epsilon=.2,mu=.5, the exact full-gauge calculation gives an N=4,S=0 ground state and gap .03979848745 U. The restricted thermal ground population is .620851 at beta U=40, .9989533 at 200, and .999999634 at 400. Cooling only the seven charge gauges while conserving S=0 has a much larger gap, .8071813751 U. These two renewal tasks must not be confused. The lower-energy S=1 state of the unrestricted spin star belongs to another permutation irrep and is inaccessible to the exact central port; symmetry breaking can reintroduce it.

## 5. A source spectrum supplied by an actual circuit

A central voltage electrode couples through e alpha n_c V. For a thermal linear impedance,

\[
S_{VV}(\omega)={2\hbar\omega\operatorname{Re}Z(\omega)
\over1-e^{-\beta\hbar\omega}}.
\]

An RC port fixes both its strength eta=4 pi alpha^2 R/R_K and its cutoff 1/(RC). Raising R does not independently raise all transition rates: it narrows the available band. The seven-gauge code evaluates actual matrix elements of n_c and the rates supplied by this spectrum.

For a generic-gap Davies model with population propagator P_t and Gibbs weights pi,

\[
{1\over2}\| (\mathcal R_t\otimes I)(\rho_{GR})
-\tau_G\otimes\rho_R\|_1
\le \max_j\|P_t(:,j)-\pi\|_{TV}
+{d_G-1\over2}e^{-\gamma_{\rm coh}t}.
\]

The bound holds for arbitrary initial gauge-reference correlations. Its proof separates diagonal blocks and uses ||rho_ij||_1<=sqrt(p_i p_j), so the off-diagonal sum is at most d_G−1. At d_G=7, U=1,t=.1,epsilon=.2,beta U=40, RC cutoff3U/hbar, the calculated population and coherence gaps are .01417996 eta U/hbar and .007180895 eta U/hbar. A finite renewal duration follows from an actual spectrum rather than an assigned reset rate.

### Passive spectral separation improves the source/control compromise

An always-connected renewal port can measure the logical state during an asymmetric gate. A real alternative to assuming a perfect switch is a parallel RLC cold impedance:

\[
Z(\omega)=\left[R^{-1}+i(\omega C-1/(\omega L))\right]^{-1},
\quad
{\operatorname{Re}Z\over R}=
{1\over1+Q^2(\omega/\omega_0-\omega_0/\omega)^2}.
\]

Here omega0=1/sqrt(LC), Q=R sqrt(C/L). Its low-frequency real impedance is proportional to omega^2, so quantum voltage noise is proportional to omega^3. A broad resonance near the charge transitions can retain renewal while suppressing lower-frequency logical measurement during a driven gate. RLC spectral engineering is established machinery; the new use here is on the exact logically blind central port.

An explicit component calculation uses U=.5 meV, C=10 fF, alpha=.05, beta U=200, omega0=.8U/hbar, Q=1. These imply R=164.553 ohm, L=.270777 nH, resonance96.7196 GHz. With the same R,C,alpha,T, renewal at epsilon/U=.4, the same bias as the gate, has seven-gauge reference-uniform mixing time to1e−6 of32.8201 microseconds for RC and41.4842 microseconds for RLC. The earlier epsilon/U=.2 results,21.0750 and23.1314 microseconds, are retained in renewal_filter_eps02_results.json; using them in the gate budget would require an additional bias-changing operation. The projected driven logical dephasing exponent per ideal force loop changes from1.93618e−5 to7.76490e−8. The latter comparison uses all Fourier components of a 2048-point microscopic Floquet density response; retaining only five harmonics changes the RLC exponent by about9.91e−15. It is not a total gate-error upper bound. The RLC device adds a physical inductor and spectral qualification.

A further calculation includes all20 singlet Floquet modes and their central-density transition matrix elements. At the same drive point the RLC escape action from the more susceptible active branch is about2.1e−21 in this isolated weak-coupling model, versus about1.24e−17 for the RC port; the other branch reaches the numerical floor. These tiny numbers are not rigorous bounds or physical infidelities. The zero-drive calculation reproduces directly calculated static transition rates at beta U=5 within3e−15; at beta U=200 the exact static rates fall below the numerical Fourier floor. Thus modeled driven charge escape does not undo the source-filter improvement, while the computation oscillator and its capacitance term remain outside this check. See alternatives/FLOQUET_PORT.md.

These circuit values are a model example, not a jointly established dot-orbital implementation. A finite-coupling derivation of the master equation, cold-resistor preparation, parasitic capacitance, electrode loss, bus coupling and actual symmetry errors remain qualifications. The full retained bus cannot be reset by pretending it is an untouched reference. A joint gauge-bus calculation is preserved separately; its dense Bohr spectrum prevents an automatic finite-rate secular justification. All-energy uniform finite-time oscillator renewal is impossible; an energy domain is necessary.

## 6. Electrostatic locality from a physical transverse gap

Place finite charge modules between two grounded planes at z=±h. The midplane Green interaction is

\[
v_2(r)={2K\over h}\sum_{m\ge0}K_0(q_mr),
\quad q_m={(2m+1)\pi\over2h},\quad K={e^2\over4\pi\epsilon}.
\]

There is no gapless transverse electrostatic mode. The positive integral representation of K0 gives

\[
v_2(s)\le e^{-q_0(s-r)}v_2(r),\qquad s\ge r.
\]

Assume each module contains at most N_max electrons in a real interaction region of radius R_mod. This includes its allowed charge leakage and its internal transfer paths. The complete intermodule first-quantized Coulomb operator obeys

\[
\|H_{AB}\|\le N_{\max}^2 v_2(R_{AB}-2R_{\rm mod}).
\]

No logical projection, spin neutrality, fixed charge pattern, narrow orbital or good neighbor is used. On a square module lattice with spacing d>2R_mod, summing all shells gives

\[
\boxed{\kappa_{\rm direct}\le
{8N_{\max}^2v_2(d-2R_{\rm mod})\over(1-e^{-q_0d})^2},
\qquad
\eta_{\rm direct}\le\kappa_{\rm direct}T_{\rm full}/\hbar.}
\]

For the four-orbital model N_max=8, this is the512 v2 bound. It includes interactions during asymmetric gates, particle-changing source intervals, sensing, routing and renewal as long as the real interaction region and particle bound hold. Infinite reservoirs and uncontrolled orbital tails need their own source/domain bounds.

Consequently, for a supplied finite operation duration, the spacing needed to suppress this direct-interaction action grows only logarithmically with T_full/epsilon. This has a computational consequence only if the useful gate uses a separate guided mode whose local coupling does not shrink with the screened direct interaction.

The effect is not unique to an ideal metal. A physically justified Robin boundary phi+lambda partial_n phi=0 has q0 tan(q0 h)=1/lambda and q0>0 for every finite lambda>=0. Its Green function is again a positive K0 sum. A gapless escape channel or unmodeled feed can destroy the exponential law and must be included.

### The intended mode has a real interface and a required counterterm

A circular driven patch of radius b centered over the star gives a weighting potential

\[
\alpha(r)=b\int_0^\infty {J_1(kb)J_0(kr)\over2\cosh(kh)}\,dk.
\]

Thus Q_ind=e[alpha(0)n_c+alpha(a)N_o], which is S3 invariant at every occupation. For h/a=b/a=.5, the electrostatic calculation gives alpha(0)=.254648, alpha(a)=.030506, contrast .224142, independent of module spacing.

The actual circuit energy is

\[
H_{\rm electrostatic}=H_{\rm grounded}
+{[Q-Q_{\rm ind}(n)]^2\over2C}.
\]

The linear charge-mode coupling and Q_ind^2/(2C) are linked. The latter is exactly gauge-only during symmetric idle, but must be retained during an asymmetric gate. It includes local charging and cross-module terms. A mode shared by an unbounded number of blocks cannot be assigned a fixed capacitance and voltage; fixed-degree buses or an explicit circuit-scaling model are required.

In the electrostatic fixture h/a=.5 and Gaussian onsite width ell/a=.2, U=4.94457 K/a. For a separately assumed compact module radius1.2a, d=10a and UT_full/hbar=1e5, the unsubtracted analytic incident bound gives action4.516e−4. The compact-support column is not a claim that a Gaussian has compact support. Including the calculated41.4842 microsecond renewal at the gate bias and the ideal.134880 microsecond loop gives UT/hbar≈3.1615e7. The unsubtracted action is.142787 at d=10a,.00580394 at11a, and.000237499 at12a. At12a the same direct-interaction budget allows a full duration up to175.238 microseconds for action1e−3; actual ramps, preparation, readout and routing must fit that duration. These combined component values are preserved in renewal_filter_results.json. The same law can accommodate longer computed renewal times by a logarithmic increase in d. It does not prove that the assumed t/U, U, higher orbital gap and tunnelling barriers can coexist in a fabricated dot.

## 7. How an active useful operation is supplied, and its scope

Known SAGE/exchange-only control provides the logical axes. At exchange order, with x=epsilon+v(a+a†),

\[
H_L=-\sum_{j=1}^3J_j(x)P_s^{cj},\qquad
\sum_jP_s^{cj}=3I/2,\quad
J_j(x)={4t_j^2U\over U^2-x^2}.
\]

The equal-hopping idle response is logically scalar at every order by the exact symmetry, including its physical circuit loading. To activate one axis, supply the actual squared-hopping waveform t_1^2=t^2+A cos(omega_d t). A microwave source supplies its amplitude, phase and the compensating scalar drive; these are real resources.

With an energy-qualified, renewed charge gauge, the driven block has a longitudinal force GZ(a+a†), together with a scalar force, local quasienergy, higher harmonics and dispersive corrections. The first-order bus force is obtained from the exact driven central-density Fourier coefficient, rather than assuming a static exchange formula is accurate.

At t/U=.1,A/U²=.005,epsilon/U=.4,omega_d hbar/U=.05,v/U=.005, the full20-state S=0 Floquet calculation gives

\[
G/U=-1.5330926657\,10^{-5},\quad
f_{\rm induced}/U=-1.7263629032\,10^{-5},\quad
\Omega_L/U=.000267189032.
\]

The leading exchange force would predict −2.83447e−5U, nearly1.85 times too large. The exact static Fourier value is −1.5236283e−5U, differing from the driven answer by.621%. Doubling1024 to2048 propagation steps changes G by1.85e−11U. These are floating-point finite-model checks without interval enclosures.

The ideal harmonic rotating model is

\[
H=\Delta a^\dagger a+
\left[fI+\sum_bG_bZ_b\right](a+a^\dagger)
+\sum_b\Omega_b Z_b/2.
\]

One loop T=2pi/Delta closes the oscillator and produces exp[i2pi(fI+sum G_b Z_b)^2/Delta²], with the known local quasienergy phases included. Equal G and Delta=4|G| give exp(i pi Z_AZ_B/4), up to local phases. The same loop plus a classical f supplies a one-qubit rotation; choosing different driven star edges supplies two nonparallel axes. Scalar-force and quasienergy compensation must use the acquired values. This provides actual operations behind the ideal universal gate set rather than assuming local logical rotations are free.

At the displayed Floquet point, UT/hbar=102459.32 before loading ramps and renewal. The loop duration is about135 ns if U=.5meV. The exact ideal closed-loop identity is independent of the initial harmonic-oscillator state. Its imperfect implementation is not uniformly close on all oscillator states: every nonzero residual displacement has operator distance2 from identity on the unrestricted oscillator. With mean photon number<=N, displacement error is bounded by |delta|(sqrt(N)+sqrt(N+1)). The excursion bound is A_max=2||fI+sum G_bZ_b||/|Delta|, giving mean occupation<=(sqrt(N)+A_max)^2. It is1 for the f=0 two-block loop or f=±G single-block loop in the compensated frame. Compensating the native quasienergy using the same force can increase it; phase wrapping permits |f|<=2|G| and A_max<=2 for two identical blocks. A known logical phase is not declared physically corrected for free.

The computed driven DC detuning curvature is d²Omega_L/d epsilon²≈.0030653163/U. Its adiabatic number-shift estimate is chi≈7.66329e−8U, or chi T/2≈.00392588 radians per photon. This is a static-detuning susceptibility of the driven module, not yet its full second-order response to a resonant oscillator. It is already much larger than the filtered-port dephasing component.

A separate exact harmonic-loss calculation retains the loss cost even with an initially vacuum bus. For branches Z_A+Z_B=±2, their force difference is4G. Vacuum damping at kappa=omega_r/Q produces coherence exponent kappa T+O((kappa T)^2). With omega_r=.05U/hbar and the computed G, Q=1e6 gives kappa T=.00512297 and a half-trace-distance witness about.00255. The full formula is in bus_loss.py. Source filtering does not remove this ordinary bus-loss cost. Conventional multiple-loop longitudinal gates reduce the leading loss exposure as1/sqrt(M) while increasing total duration as sqrt(M), at fixed force and target phase. Shaped-force and echo protocols are also legitimate comparators. Their active nonlinear response, imperfect closure and holding costs must be retained; the one-loop witness is not a universal lower bound on every possible gate.

The finite physical gate still needs the circuit counterterm, scalar loading, finite-frequency rectification, charge-gauge transitions, oscillator anharmonicity, loss, control noise and loading ramps. A static spectrum or a single Floquet harmonic is not a complete spin-bus instrument. The asymmetric drive also need not act identically on arbitrary gauge80 states. It is not an arbitrary-history gate just because the idle source is an arbitrary-history protected operation.

## 8. What remains reliable under imperfections and repeated use

The exact invariant apparatus can be arbitrarily strong and retained. If its violation E has a bounded integrated full-space norm, Duhamel's formula gives joint isometry error at most integral ||E(t)||dt/hbar. The corresponding channel diamond distance is at most twice that bound. For example, allocating action1e−3 to a static symmetry-breaking norm throughout the computed41.4842 microsecond renewal requires its energy divided by Planck's constant to be at most about3.84 Hz. This demanding requirement is derived from the duration; it is not assumed to be achieved. This covers arbitrary reference states and initial gauge histories in the protected component. It does not make infinitely long storage with fixed nonzero mismatch exact.

The screened Coulomb result supplies such a bound from geometry, including the full incident sum on leaked neighbors. Other error terms need their own physical bounds. A miscentered patch couples a standard outer charge mode to an oscillator quadrature. Because that quadrature is unbounded, finite geometric tolerance then requires a supplied energy/quadrature domain. Exact symmetry and finite-tolerance qualification have different scopes.

Finite-band fermionic source couplings have bounded smeared annihilation operators, with norm determined by the square-integral of the tunnelling form factor. This gives a possible state-uniform source-mismatch bound; an infinite wide-band rate approximation cannot simultaneously be used as a finite operator-norm certificate.

Outer physical permutations can be supplied by the all-Fock revival pulse if actual outer-outer tunnel links exist. Equal outer capacitances reduce to (U_o−V_o)sum D_j+(V_o/2)N_o(N_o−1), so the extra number term is gauge-only. A common pair potential cancels the known N_pair phase; the untouched outer doublon revives. A central source can remain coupled during this pulse. The full256-state check is preserved. This does not by itself supply dynamical decoupling of a rapidly moving gauge. Random group twirling also requires treatment of retained random/controller records, which can reveal the first-order conditional error.

There is therefore a concrete improvement and a concrete remaining bridge. The improvement is a source that can erase gauge information without erasing logical information, plus an all-charge locality mechanism that does not slow a separately supplied guided interaction exponentially. The missing bridge is a single physical regime certifying the complete active circuit, finite-rate renewal, symmetry mismatch, sources, orbital spectrum and correction operations together. No arbitrary tiny residual or device advantage is assigned to close that gap.

## 9. Comparison and credit

Noiseless subsystems and operator error correction already provide the abstract algebraic principle. Symmetry-protected infinite-temperature memories already show that otherwise ergodic many-body dynamics can retain quantum information. Their prethermal extension requires additional locality and code conditions; it does not automatically protect this four-site block against a local dressed logical perturbation. SAGE already provides equal-exchange four-spin degeneracy, protected spin encoding and local control axes. Hubbard revival gates, hot-oscillator geometric gates, impedance spectral engineering, screening and fault-tolerance theory are existing machinery.

The working contribution here is the particular physical combination and the proved interface laws: full-Fock S3 protection through a central particle source; interaction-enabled gauge accessibility; an exact seven-gauge cooling-algebra proof; a finite-region all-leakage electrostatic incident bound; and a source/control spectrum calculated from circuit elements. These should be evaluated as information and interface guarantees, not inferred to be a complete hardware advantage.

Equally informed conventional singlet-only controllers may use the same acquired Hamiltonian, Floquet response, spectral filters and screened geometry. Ordinary optimized exchange or capacitive gates may be faster and need fewer components. Existing cavity longitudinal gates already close an ideal hot bus; the distinct guarantee here is exact scalar idle loading throughout the protected charge sector. It is not exact active immunity.

Optical double-heralded entanglement remains a strong alternative with real emission, local rotations, detectors and renewed ports. Its success probability and waiting-time storage cost must be counted. A finite-cooperativity cavity click can also be a state-dependent filter; a good basis label or favorable conditional state fidelity is not automatically a state-uniform parity instrument. None of these comparators is denied its actual controls, calibration or filtering.

The old signed-spin handles, positive-force apparatus, charge compiler and this symmetric circuit architecture are distinct resource settings. Earlier accepted parity instruments, finite-U return, neutral-block leakage reduction and correlated-history results are retained with their original hypotheses.

## 10. Reproducible work

Root code: orbital_echo.py; star_subsystem.py; central_port.py; instrument_checks.py; renewal_filter.py; bus_loss.py. Their corresponding results.json files preserve the outputs.

Complementary physical calculations are in source_physics/STAR_RENEWAL.md, coulomb_leakage/STAR_GEOMETRY.md and alternatives/STAR_ACTIVE.md, with executable rate, electrostatic, revival and Floquet scripts. Main scripts run with Python, NumPy and SciPy, e.g. OPENBLAS_NUM_THREADS=1 python p2_physical_bridge/central_port.py.

Exact claims are distinguished from ordinary floating-point examples. The modular rank certificates do not rely on rounded nonzero singular values; the spectral, geometric and rate examples are not interval-certified parameter boxes.

## Primary sources consulted

- Knill, Laflamme, Viola, Theory of Quantum Error Correction for General Noise: https://arxiv.org/abs/quant-ph/9908066
- Wildeboer, Iadecola, Williamson, Symmetry-Protected Infinite-Temperature Quantum Memory from Subsystem Codes: https://arxiv.org/abs/2110.05710
- Foulk et al., Singlet-only Always-on Gapless Exchange Qubits with Baseband Control: https://arxiv.org/abs/2501.18589
- Borodin and Rozhkovskaya, On a super-analog of Schur-Weyl Duality: https://arxiv.org/abs/2208.07434
- Zhang and Barthel, Criteria for Davies Irreducibility of Markovian Quantum Dynamics: https://arxiv.org/abs/2310.17641
- Ruskov and Tahan, Modulated longitudinal gates on encoded spin-qubits via curvature couplings to a superconducting cavity: https://arxiv.org/abs/2010.01233
- Analog Quantum Simulation of the Dynamics of Open Quantum Systems with Quantum Dots and Microelectronic Circuits: https://arxiv.org/abs/2203.12127
- Koulakov and Shklovskii, Charging Spectrum and Configurations of a Wigner Crystal Island: https://arxiv.org/abs/cond-mat/9707204
- Spin swap vs. double occupancy in quantum gates: https://arxiv.org/abs/cond-mat/0402674
- Khodjasteh and Viola, Dynamical Quantum Error Correction of Unitary Operations with Bounded Controls: https://arxiv.org/abs/0906.0525
- Ng and Preskill, Fault-tolerant quantum computation versus Gaussian noise: https://arxiv.org/abs/0810.4953
- Nathan and Rudner, Universal Lindblad equation for open quantum systems: https://arxiv.org/abs/2004.01469

These references support the credited prior machinery. The new concrete algebra, counterexamples and component calculations are derived above and in the linked executable work.
