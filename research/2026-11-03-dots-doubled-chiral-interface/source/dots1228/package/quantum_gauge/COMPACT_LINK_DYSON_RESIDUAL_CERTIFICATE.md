# Full compact quantum-link evolution from a finite residual certificate

2026-11-03. This closes a finite-time, finite-device prediction without truncating the actual electric spectrum or assuming a photon overflow bound. It uses the ACTUAL finite-charge matter Hamiltonian, including its two same-chirality charge assignments. It is a weak-coupling finite-time construction, not a volume-uniform or continuum theorem.

## 1. Solve finite-box Gauss law exactly

Use a connected finite cubic cell complex with no noncontractible1-cycles, and work in total neutral matter charge. Delete one redundant incidence row. Split incidence D=(D_t,D_c) into spanning-tree and non-tree columns. D_t is invertible over integers. Put

 L=D_t^(-1), C=D_t^(-1)D_c,
 G=I+C^T C, R=−C^T L, C_Q=L^T L.

Gauss law D E=Q solves E_t=LQ−C E_c. Tree gauge identifies the physical Hilbert space exactly with L²(T^b) of b independent cycle angles theta, tensored with the neutral finite-charge matter space. The exact electric operator is

 H_E=g²/(2a)[p_theta^T G p_theta+2p_theta^T RQ+Q^T C_Q Q],
 p_theta=−i∂_theta.

All onsite Q commute, and commute with p_theta. This retains the charge–electric cross term instead of silently deleting it by a possibly nonperiodic Coulomb dressing. Global tree coordinates are a proof/computation chart, not a claim of uniform spatial locality.

Let B be the integer plaquette/cycle matrix so U_p=exp(i(B theta)_p). Since the box has no harmonic1-cycles, K=B^T B is positive definite on these physical coordinates. The actual globally gauged matter Hamiltonian becomes a finite matrix-valued trigonometric polynomial h(theta), or a smooth finite-charge matrix function with explicitly bounded derivatives, obtained by the exact charge-transfer compiler. No gauged Choi identity is used.

## 2. Exact weak-field expansion with controlled remainders

Set theta=g x in the local chart. On R^b define

 H00=h(0)+(1/(2a))[p^T Gp+x^T Kx],
 V1=(1/a)p^T RQ+Σ_r x_r J_r,
 V2=(1/(2a))Q^T C_QQ+(1/2)Σ_rs x_r x_s K^mat_rs
       −(1/(24a))Σ_p(B_p x)^4,

where J_r=∂_r h(0), K^mat_rs=∂_r∂_s h(0), computed from ACTUAL charges. The exact compact Hamiltonian in this chart is H00+gV1+g²V2+R_g.

For a local tree-gauged term h_X, its theta dependence is conjugation by commuting path charges. Taylor's integral remainder gives an operator-on-vector bound

 ||R_matter(g)psi||
 ≤(|g|³/6)Σ_X 8||h_X|| ||(Σ_r |x_r| ||B_Xr||)^3 psi||.

For the magnetic part, the elementary global scalar Taylor inequality gives

 ||R_magnetic(g)psi||
 ≤g^4/(720a) Σ_p ||(B_p x)^6 psi||.

Thus matter costs sixth moments and magnetic remainder costs twelfth moments. These are not inferred from a second-moment estimate; they are computed directly on the finite trial space below.

Diagonalize the positive oscillator pair G,K by finite linear algebra. Let P_n project onto total oscillator occupation≤n. For any linear coordinate/momentum form Z=Σ_k(d_k b_k+d_k* b_k†), define d(Z)=Σ_k|d_k|. Then

 ||Z^m P_n||≤[2d(Z)sqrt(n+m)]^m.

For absolute coordinate sums, expand the finite multinomial and apply this bound termwise. This gives explicit numbers r_n(g) bounding ||R_g P_n||, with r_n(g)=O(|g|³)+O(g^4), and explicit L1(n)=||V1P_n||, L2(n)=||V2P_n|| bounds. The finite matter matrices enter by ordinary operator norm. No infinite gauge bandwidth is bounded or discarded.

## 3. A trial solution using only finitely many Hermite levels

Choose any normalized matter vector and oscillator vector with occupation≤n0. Let

 chi0(t)=exp(−itH00)psi0,
 chi1(t)=−i∫_0^t exp[−i(t−s)H00]V1 chi0(s)ds,
 chi2(t)=−i∫_0^t exp[−i(t−s)H00][V1chi1(s)+V2chi0(s)]ds.

Set psi_trial=chi0+gchi1+g²chi2. Occupations are bounded respectively by n0,n0+1,n0+4. These are finite vectors and integrals. Exact matter evolution is supplied by the actual finite matrix/compiled simulator, not by an assumed response oracle.

For0≤t≤T define

 A1=T L1(n0),
 A2=T L2(n0)+(T²/2)L1(n0+1)L1(n0),
 A=1+|g|A1+g²A2.

Then ||chi1||≤A1, ||chi2||≤A2. Direct substitution, with NO omitted higher photon states, gives

 ||(i∂_t−H_poly)psi_trial||
 ≤|g|³[L1(n0+4)A2+L2(n0+1)A1]
   +g^4 L2(n0+4)A2 =:D_poly.

The action H_poly psi_trial may have occupation up to n0+8. Those components are included in the residual norm, so boundary overflow is not assumed absent. Adding the exact Taylor remainder costs at most A r_(n0+4)(g).

## 4. Put the trial vector into the ACTUAL compact Hilbert space

Choose fixed smooth cutoff chi(theta), equal1 on |theta|∞≤rho and zero on |theta|∞≥2rho, where2rho<pi. Define

 (I_g f)(theta)=g^(−b/2) chi(theta) f(theta/g),

extended periodically on T^b. I_g is a contraction, not silently an isometry. Normalize the actual initial state I_gpsi0. Lift it by the exact tree-gauge inverse to satisfy every Gauss constraint. This is a true compact-link state with infinite electric support and finite kinetic energy.

Every vector in P_n is a finite Gaussian times polynomial. The oscillator covariance matrix is explicitly known. Therefore its norm outside |x|∞≤rho/g and the norms of its first derivatives there are computable Gaussian-polynomial integrals. Let tau_n(g) bound the norm tail and sigma_n(g) bound the kinetic cutoff commutator

 ||H_comp I_g f−I_g H_chart f||≤sigma_n(g)||f||, f∈P_n.

Only derivatives of chi appear in this commutator. In rescaled coordinates they have factors g and g²; the electric charge cross term adds the explicit finite Q norm. Both bounds have the form C g^(−m)exp[−c rho²/g²], with c>0 from the actual oscillator covariance. One may compute tighter bounds by incomplete Gaussian moments. They depend on box size, charge cutoff and n, and are not claimed uniform as the infrared frequency approaches zero.

Multiplication terms commute exactly with I_g on the chart. Thus the ACTUAL compact Schrödinger residual is bounded by

 D_comp≤D_poly+A r_(n0+4)(g)+A sigma_(n0+4)(g).

Let U_comp(t) be the full compact gauge evolution, with no electric cutoff. Unitarity and the inhomogeneous Schrödinger equation prove

 ||U_comp(t) psi_initial−I_g psi_trial(t)||
 ≤2tau_n0(g)+|t| D_comp,

with harmless tightening available for the initial normalization factor. This is an a posteriori error certificate for the entire quantum state. Observable errors follow from2||O|| times the state error (plus the small trial normalization correction). All constants are finite sums, Gaussian integrals, norms and finite-time matrix integrals of the actual specified model.

## 5. Physical meaning and limits

The formula predicts a nonzero-coupling, genuinely time-dependent compact quantum-gauge experiment at any chosen finite T for which the displayed error is small. Its photon dynamics has physical frequency set by1/a, not by g→0 freezing. The full gauge vacuum energy stays in H00 as a scalar phase; it is never falsely used as a small excitation budget. It includes actual current/contact vertices, electric charge cross terms, Coulomb energy and compact magnetic corrections. Combining its trial amplitudes with the subgap resolvent/SW analysis identifies virtual mirror polarization in a slow-gauge-frequency window.

This can be applied directly to the actual finite light+rest device without assuming that its separate gauged Hamiltonians inherit a zero-field Choi identity. However, calling the resulting signal purely chiral requires the separately proved rest-band/target identification and its charged-vertex transfer. The certificate predicts the ACTUAL model even if that interpretation fails.

Resources are severe: finite matter charge cutoff and dimension, cycle count b, oscillator levels through n0+8, mode covariance/IR frequency, finite-time matter simulation, and all derivative norms appear. The previous astronomical Wilson refinement remains. No fixed-coupling thermodynamic or continuum estimate follows; constants can grow with volume and the present auxiliary cutoff. This is a controlled finite-device quantum-response construction, not completion of the major foundation sought.
