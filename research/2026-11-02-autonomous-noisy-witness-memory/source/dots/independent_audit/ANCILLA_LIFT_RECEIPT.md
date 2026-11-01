# Independent receipt: exact finite-rate ancilla-current lift

2026-11-01. Audited `ANCILLA_CURRENT_HYPOCOERCIVE_LIFT.md`, SHA256 1e7e17b0d4b55649cc2e9b4553b47f02c649eac925f821a4daee3197a198c204. This receipt independently derives the current inequalities, explicit local-exponential constants, and reflected-component interface. It does not certify native few-body synthesis, a physical reset reservoir, useful costs, or novelty.

## Judgment

**Conditional mathematical PASS.** No sign/algebraic counterexample was found. The proposed exponential mechanism is an exact statement about the finite-parameter joint Lindbladian, not an adiabatic-elimination approximation accumulated over time. The hypotheses and boundary/initialization qualifications below are necessary parts of the acceptance.

## 1. Activity for the actual Tanner branch list

Use only genuinely downhill selected branches; the earlier no-update dephasing branches need not be dilated. At most j compatibility branches are enabled. An enabled mismatch move must meet a nonzero mismatch coordinate; each coordinate occurs in four candidate views, so at most 4z mismatch branches are enabled. Thus, in each sector and then in their sum,

    W/K <= sum_alpha J_alpha†J_alpha <= j+4z <=4W.

The lower bound remains restricted to the received Tanner basin; the upper bound holds on all joint labels. This gives c=1/K and C0=4 for unit-norm branch operators. Splitting a selected branch into exact-drop pieces uses orthogonal local condition projectors, so it does not multiply the activity sum. It DOES multiply the channel/ancilla count by a fixed possibly enormous constant, and overlap incidence must use that actual list.

The exact-drop projectors can be local: the change of a commuting local W under a bounded-support correction is determined by the bounded neighborhood of W terms touched by that correction. Each J_alpha is a single correction Pauli times its local enabled/exact-drop projector. No condition is inferred from a global syndrome measurement.

## 2. Current algebra and mean drift

With A_alpha=J_alpha sigma_alpha^+, [W,J_alpha]=-d_alpha J_alpha and Q=W+sum d_alpha n_alpha, [Q,A_alpha]=0 exactly. Hence [Q,H]=[Q,C]=0 and L*Q=-gamma sum d_alpha n_alpha.

The expectation identity <J_alpha sigma_alpha^+>=<sigma_alpha^- psi,J_alpha psi> and Cauchy–Schwarz over alpha give

    |<C>|<=2 sqrt(<sum J_alpha†J_alpha><N>)
          <=2sqrt(C0<W><N>)<=sqrt(C0)<Q>.

No independence or factorization is used. The global Tanner upper activity bound makes this comparability global, not only a classical-state estimate.

Direct commutation gives i[H,C]=2g[A,A†], with the NEGATIVE vacuum activity term -sum J_alpha†J_alpha. The self terms contribute at most 2j_*^2 N in the unfavorable direction. An ordered overlapping pair contributes at most j_*^2(<n_alpha>+<n_beta>), because the system commutator norm is <=2j_*^2. Each channel overlaps at most z others, so summing ordered pairs gives <=2zj_*^2 N. Thus C1=2(1+z)j_*^2 is safe. Reset contributes exactly -(gamma/2)C.

For V=Q+epsilon C, eta=epsilon sqrt(C0)<=1/2 gives (1-eta)Q<=V<=(1+eta)Q and [Q,V]=0. The reset-current contribution is bounded above by epsilon gamma sqrt(C0<W><N>). Young's inequality with coefficient epsilon g c yields precisely

    L*V <=-epsilon g c W
          +[-gamma d_min+2epsilon g C1
             +epsilon gamma^2 C0/(4gc)]N.

The stated choice of epsilon therefore gives L*V<=-c_V Q, with c_V=min(epsilon gc,gamma d_min/(2d_max)). All signs and constants in A2–A5 check. The statement holds in the safe sector for the lower activity premise, for arbitrary joint quantum states supported there.

The independent exact script `check_current_signs.py` passed rational/imaginary matrix checks of conservation, current sign, comparability and mean drift for one lowering channel and its reset ancilla. This is a finite algebra sanity check, not the general proof.

## 3. Explicit dimension-independent imaginary-time estimate

Write V=sum_X v_X with support size <=s, maximum term incidence <=zeta per site, and ||v_X||<=v_*. Let r bound the supports of every local Hamiltonian term h, reset/noise jump l, and l†l used in the estimate. Take

    C=2 zeta v_* (r+s),   0<a<=1/(2C),   x=Ca/2<=1/4.

For any such O, expand nested commutators into sequences of local terms. At the j-th commutation a nonzero sequence has support at most r+j(s-1), and at most zeta times that many choices for the next term. Each commutation costs at most 2v_*. Since r+j(s-1)<=(r+s)(j+1),

    ||ad_V^k(O)|| <=||O|| C^k k!.

Consequently T_t(O)=exp(tV)Oexp(-tV) has a uniformly convergent expansion for C|t|<1, with remainder after order m bounded by ||O||(C|t|)^(m+1)/(1-C|t|). This counts branchwise supports of the nested expansion, not the potentially extensive support of their sum. It applies on the full finite system before any nonlocal reflection.

For a Hamiltonian term h the exact weighted contribution is i(T_-a/2(h)-T_a/2(h)). Its linear term is ia[h,V]. Bounding its remaining terms by the geometric series gives the conservative remainder

    <=C^2 a^2 ||h||.

For a dissipator use A=T_a/2(l), B=T_-a/2(l†l). Its weighted contribution is A†A-(B+B†)/2. The linear term is exactly a D[l]*V. The remainder of A†A is at most ||l||^2 x^2[2/(1-x)+1/(1-x)^2], and the symmetric B remainder is at most ||l||^2 x^2/(1-x). For x<=1/4 their sum is <6x^2||l||^2, hence certainly

    <=2C^2 a^2 ||l||^2.

If the actual ideal local list obeys sum||h||<=H0 n and sum||l||^2<=R0 n, then

    F^-1/2 L*F F^-1/2=a L*V+R_a,
    ||R_a||<=C2 a^2 n,   C2=C^2(H0+2R0).

This proves A6 with explicit safe constants. For the dilation H0 may be bounded using 2g j_* times the number of channels per n, and R0 using gamma times the same number. Those large fixed constants cannot be discarded.

## 4. Foster inequality and exponent margin

Combining the exact expansion with mean drift gives the claimed weighted bound -a c_V Q+C2 a^2 n I. If a<=c_V theta/(2C2), its high-Q part is <=-a c_V Q/2; its low-Q part is <=C2a^2 n. Since Q COMMUTES with V, congruence by F^1/2 and spectral splitting at Q=theta n give

    L*F <=-k n F+D n exp[a(1+eta)theta n] I,
    k=a c_V theta/2, D=k+C2a^2.

The commutation is essential: this is not an unproved operator-monotonicity claim for exponentials of noncommuting observables. On the low sector F<=exp[a(1+eta)theta n]I by joint spectral calculus.

Boundary decay requires (1-eta)beta>(1+eta)theta. In particular, the old theta=beta/2 together with only eta<=1/2 is NOT sufficient. Safe choices include eta<=1/4 with theta=beta/2, or eta<=1/2 with theta=beta/4. The author note explicitly requires the correct margin; subsequent joins must preserve it.

## 5. Reflection without applying locality to a nonlocal projector

Choose the below-Q-cutoff component using all admitted full-system Pauli components, including ancillary flips and projections of full coupling/noise supports. Its projection onto the original system/witness labels lies in the earlier below-W safe component because W<=Q along every path. The same original Tanner activity lower bound therefore holds there.

Every ACTUAL nonzero C edge conserves Q exactly. Its endpoints belong to the same admitted below-cutoff component, so [P_good,C]=0 and hence [P_good,V]=0. Individual terms in a Pauli expansion need not conserve Q; what is used here is conservation by the actual exact-drop coupling together with inclusion of its transition edges in the component alphabet.

Ideal H preserves the component. A reset lowers Q and its adjoint product is the diagonal ancillary number operator, so its original and reflected generator actions agree on component-supported states. Therefore one may prove the local identity on the full system, then compress it; F restricted to the component is precisely exp(aV_restricted). It would NOT be valid to declare P_good l P_good local and rerun the locality count on those compressed jumps.

Protected flatness is inherited from the original safe system component, while ancillary flips and phases are unprotected syndrome operations. The joint ground subsystem is the old protected/gauge ground tensor ancillary vacuum. Reflected coupling and reset terms therefore act as identity on protected information, including coherent gauge states.

## 6. Local noise and the boundary consumer

The same conjugation series gives, for x<=1/4, a weighted local Hamiltonian bound <=2Ca||h_noise||. For a jump, use the exact identity (A†B+B†A)/2 with A=T_a/2(l) and B=T_a/2(l)-T_-a/2(l). Its norm is <=2Ca||l||^2. Thus local noise budgets sum||h_noise||<=h n and sum||l_noise||^2<=gamma_noise n imply a weighted perturbation bound

    u_noise(a)n <=2Ca(h+gamma_noise)n.

For bath-coupled Pauli terms, replace each coefficient by its bounded bath operator norm; the system-support commutator count is unchanged. Take r and C large enough to cover the ACTUAL admitted noise supports. The earlier diagonal exp(aW) hyperbolic constants are not automatically reused.

For example h+gamma_noise<=c_V theta/(8C) ensures u_noise<=k/2. These are fixed positive ratios independent of n, although potentially unusably small. Finite-temperature upward resets are included as actual local noise jumps; their total rate sums over ALL ancillary channels.

The repaired boundary comparison still uses a TWO-step shell, now for Q and its maximum admitted Pauli increment b_Q. Ideal terms agree under reflection; only noise contributes. Since V commutes with Q and V>=(1-eta)Q,

    p_shell(t)<=tr(F rho_ref(t))
                 exp[-a(1-eta)(beta n-2b_Q)].

The preceding trace-norm Duhamel bound applies with n(2h+4gamma_noise) times the time integral of sqrt(p_shell), using the actual Pauli/norm budgets. Together with the Foster estimate and a positive exponent margin this gives an exponentially long decoded-memory interval. No finite-time channel approximation and no epsilon*T elimination error is introduced.

## 7. Initialization and physical counting qualifications

Pure ancillary vacuum and encoded W=0 input lie in the good component and have F moment exactly one. This clean initialization is sufficient for the accepted mechanism.

For independent thermal ancillary populations, the product upper bound in the author note follows from V<=(1+eta)Q and [V,Q]=0. But the thermal state also has support outside the cutoff component. A separate tail/truncation cost is REQUIRED before actual/reflected comparison. On system ground, every ancillary occupation pattern with Q<beta n is reachable from vacuum by monotone ancillary flips, so belongs to the good component. Chernoff bounds its excluded probability using the stated moment; normalized projection costs at most twice its square root in trace norm (twice the probability for the independent diagonal thermal case). The conditioned initial F moment is at most the original moment divided by the retained probability. Choose the thermal exponent strictly below a(1-eta)beta and the Foster exponent with a strict margin. For independent ancillary preparation this conditioning does not alter protected logical input. Arbitrary correlated preparations need their own logical-admission argument; a small energy moment alone is not enough.

There is one two-level ancilla per actual exact-drop channel. If their number is L0 n, total physical qubits are (5+L0)n, NOT 5n. L0 may be enormous because the local truth tables have many patterns. Physical noise budgets, initialization entropy, local incidence, H0/R0, and protected-rate overhead all include this factor. A fixed small excitation density must also pay L0. No assumed multilevel bundling is used.

## Acceptance limits and closure

Accepted: exact finite-rate current correction, dimension-independent mean drift, explicit local exponential expansion, fixed-parameter Foster/noise admission, and reflected boundary interface under the stated safe-component and initialization conditions. No algebraic blocker remains in this bounded audit.

This earns a mathematical finite-ancilla dilation at fixed rates within the stipulated Markov-reset model, including suitably small nonzero upward/reset/data/ancilla noise. It does not replace the reset reservoir by a closed finite quantum system, justify a microscopic Markov approximation for exponential time, compile high-body conditional couplings into native few-body interactions, or establish useful geometry/cost. Those resource limits remain real and are not repaired by this proof.
