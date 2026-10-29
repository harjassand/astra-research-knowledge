# Replacing causal quantum retention by a bounded complete instrument error

Root construction, 29 October 2026 Australia/Brisbane. Status: authored theorem; independent review pending. This proof uses the accepted exact passive compiler in `p2_mediator/` and the new, separately reviewed-if-accepted noise-path construction in `measurement_frontier/NOISE_MEMORY_PATH_THEOREM.md`. It does not change the status of either dependency.

## 1. Consequence and contract

The exact receiver stores the noncommuting part of an emitted field until later arrivals cancel it. The noise-path construction instead permits some of that incompatibility to be supplied by independent detector vacuum. Here we lift the resulting *measurement construction* to a bound on the corrected source/reference/**entire actual raw record** instrument. No input-energy cap on the original field is required for this ideal comparison.

The physical operation is a supplied controlled-Weyl dilation

    U_f = G_S sum_z |z><z| tensor W(F_z),
    F_z = direct_sum_t sum_i z_i f_(i,t), z_i in {+1,-1}.

The diagonal source unitary G_S is fixed and must be preserved. Any retained mediator is closed or explicitly included in the accessible field. Emitted batches do not return to the source after their declared retirement. Local source phase feedback is deferred until it commutes with the actual microscopic schedule. The receiver needs calibrated mode access, passive interferometers, ideal homodyne, counted retained modes and independent fresh detector vacua.

Let `Omega_t=Im Gram(f_t)`. Choose a noise path from the new synthesis theorem:

    S_0=S_T=0, rank S_t<=2q_t,
    Gamma_t=S_t-S_(t-1)-Omega_t,
    H_t=N_t+i Gamma_t >= 0.

Factor H_t as the Gram matrix of fresh auxiliary feature columns g_(i,t), and set N=sum_t N_t. These g are **measurement coefficients**, not physically delivered source couplings or actual injected coherent amplitudes. They determine a passive receiver for the enlarged features h=(f,g). Its prefix commutator is S_t, so the accepted exact compiler applies. The raw homodyne record may be larger than the reported n-vector; all of it remains in the comparison below.

Let R be this actual raw-record receiver, and let C_y be the product local Z feedback prescribed by the enlarged feature reconstruction. Define the common comparison instrument as G_S followed by R acting on the original input field and the same independent detector vacua, with no controlled displacement. If the original source and field were correlated, this baseline record can also be correlated with the source. Its assemblage is preserved in the comparison; independence is not asserted.

## 2. Complete conversion theorem

Put

    d^2 = max_(z in {+1,-1}^n) ||G_z||^2
        = max_z z^T N z,
    G_z = direct_sum_t sum_i z_i g_(i,t).

For every normal joint source/original-field/reference input rho, tensored with the stipulated independent vacuum detector supply, the actual corrected instrument and the common comparison instrument obey

    (1/2)||I_actual(rho)-I_common(rho)||_1
        <= sqrt(1-exp(-d^2)).                                  (1)

The trace norm includes the source, arbitrary reference and **all raw outcomes actually retained by R**. The supremum over such inputs satisfies the same bound. Equation (1) is therefore a complete state-uniform instrument bound for this supplied dilation and detector-supply contract, not merely a covariance bound, a reduced-source estimate, or a statement about Gaussian inputs. The original field may have unbounded mean energy.

### Proof

Introduce only as a comparison the unitary

    U_+ = G_S sum_z |z><z| tensor W(F_z direct_sum G_z).

Original and detector-ancilla one-particle sectors are orthogonal. Hence there is no Weyl cocycle in

    W(F_z direct_sum G_z)=W(F_z) tensor W(G_z).

The receiver R and feedback C_y exactly erase U_+ by the accepted full-record intertwining theorem. Its output is I_common, including any initial source/field/reference correlations. This is an algebraic comparison unitary; no physical source-to-detector-ancilla interaction is performed or assumed available.

Purify the actual allowed input and write it as sum_z |z> psi_z, with branch probabilities p_z=||psi_z||^2. The inner product of the purifications after U_f and U_+ is

    sum_z p_z <0|W(G_z)|0>
      = sum_z p_z exp(-||G_z||^2/2)
      >= exp(-d^2/2).

All terms are real and nonnegative. No independence between source, original field and reference was used. Pure-state half trace distance is sqrt(1-|overlap|^2), yielding (1) before detection. Applying the same receiver and record-controlled feedback is a common CPTP channel and contracts trace distance. Purification handles mixed states. This proves the complete raw-record claim.

The construction also permits a globally nonisotropic original F: the auxiliary imaginary Gram sums to minus its total commutator, making h isotropic. The earlier all-input commutator obstruction remains applicable to the achieved nonzero error; this construction does not contradict it or produce an exact eraser for a forbidden relative-unitary family.

## 3. What changed relative to a feature-cutoff comparison

Projecting actual field features onto fewer measured quadratures requires controlling the displacement of the unknown original field. That comparison naturally needs an input number moment. Here the original field feature is unchanged. The comparison displacement acts only on a known independent detector supply, whose vacuum characteristic function is exact. This is why the ideal bound is state-uniform on the original field.

The measurement POVM marginal alone has no analogous uniform approximation guarantee to a sharp quadrature measurement: an arbitrarily narrow input distribution can distinguish nonzero convolution noise. Equation (1) concerns a different operation, source correction with the actual record retained. Its proof uses the known auxiliary state and an exact erasing comparison, rather than inferring trace distance from a covariance.

Neither theorem makes physical controls automatically state-uniform. A small error in a passive phase or a feature coefficient need not have a small unrestricted diamond norm on arbitrarily energetic input fields. Acquisition and finite delivery errors require their own matched energy/resource contract, for which the preceding number-moment and finite-energy machinery can be reused. The ideal comparison and the physical error budget remain distinct.

## 4. Optimize the operation, not an unrelated noise scalar

The path theorem minimizes weighted covariance trace for a fixed path. The quantity in (1) is instead the maximum quadratic form on the actual finite source alphabet. The exact multi-cut example saved by the path author reverses the rankings: after a common rational Hadamard rotation of feature coordinates, one feasible path has Tr N=6 and d^2=12, while another has Tr N=8 and d^2=8. A smaller measurement-MSE cost need not give the better complete-error allowance. This compares sufficient bounds, not actual channel-error lower bounds.

Exact sign maximization is not presumed cheap. A reusable upper certificate is

    Diag(lambda)-N >= 0,
    D=sum_i lambda_i.

Then z^T N z<=D for every sign vector, so (1) is at most sqrt(1-exp(-D)). Minimizing D is the dual of the usual positive-semidefinite relaxation

    maximize Tr(N X), X>=0, diag X=1.

This relaxation is an optional computational instrument, not an assertion of a free exact optimizer. A simpler certificate is D=n lambda_max(N). For diagonal N the sign value is exactly Tr N. The exact rational tests in this tranche supply explicit matrices and witnesses rather than relying on an unchecked numerical SDP result.

For a fixed chosen S path, the complete-bound design problem admits the convex sufficient program

    minimize sum_i lambda_i
    subject to N_t+i Gamma_t>=0 for all t,
               Diag(lambda)-sum_t N_t>=0.

Allowing S_t to vary retains the causal rank constraints and can make optimization nonconvex. The theorem is a construction from a feasible certificate, not a fast global algorithm. Floating solver residuals require separate enclosure before they become certified inequalities.

## 5. Two-batch endpoints and admitted-input dependence

For two source features with local commutators kappa J and -kappa J, one retained mode gives S_1=kappa J and N=0: the exact receiver is recovered. With no retained modes, the trace-optimal isotropic local noises give

    N=2|kappa| I_2, d^2=4|kappa|,
    epsilon_complete<=sqrt(1-exp(-4|kappa|)).

This is attained as a covariance/no-memory design within the stated receiver class, while the displayed error remains a sufficient bound. It should not be treated as a sharp minimum corrected-instrument error.

For the prior two-bin small-feature example a=1/4, b=1/10000, |kappa|=ab, this state-uniform construction gives a sufficient error below 1/100. The earlier vacuum-input projection construction gives the much stronger sufficient allowance sqrt(2)/10000<1/7000. Both are useful at their actual scopes: the latter uses its input-moment promise, while the present bound tolerates arbitrary original field states. A wider promise is not automatically a better engineering choice. At a fixed interaction-generated gate angle, the coupling/loss costs remain in the physical ledger; this is no rescue of the failed accumulator.

## 6. General independent detector states and preparation error

The same proof applies to any specified independent detector state sigma with characteristic values chi_sigma(G_z)=Tr[sigma W(G_z)]. Let

    m=dist(0, convex_hull{chi_sigma(G_z): z in {+1,-1}^n}).

Using a purification of sigma, the overlap is a convex combination of those values. The complete error is at most sqrt(1-m^2). For centered Gaussian detector states the characteristic values are positive exponentials, giving the corresponding largest quadratic-form variance. This observation changes the supply contract and must not silently replace the independent-vacuum synthesis assumptions or its resource costs.

If the actual joint input is within half trace distance delta of the stipulated original input tensored with the specified detector supply, a common physical channel adds at most delta to a comparison with that stipulated ideal-supply baseline. If both endpoints are defined using an imperfect supply, the appropriate two endpoint allowances must be charged explicitly. Correlated preparation is not made free by knowing detector marginal states.

## 7. Resource and novelty boundary

The physical detector uses passive mixing, freshly prepared independent vacuum modes, ideal homodyne and local phase feedback. It introduces no extra coherent source coupling. Fresh ancillary count is rank(H_t) per batch; live width and retained count are those in the path theorem. Classical gains, readout precision, record processing, source coherence until feedback, mode capture, collection and reuse must all be supplied. Tr N is a quadrature-noise quantity in the feature convention; it is not actual injected photon energy or a pump budget. Passive processing can concentrate existing input energy into the retained register.

Storage loss and inaccessible ports are separate channels. The loss-aware two-bin operation in `noise_challenge/` is a further explicit test; its reported two-vector and full raw record are not conflated. The previous conventional returning-bus advantage remains unchanged.

Gaussian observable dilation, simultaneous-quadrature uncertainty, Stinespring/purification comparison, and environment-assisted feedback are established constituents. The claimed construction here is the compatible causal resource path combined with a complete-record erasure conversion that charges only known detector-supply displacements in the ideal comparison. Historical priority and physical advantage are not established by this authored proof.
