# Constructor challenge: deterministic sweep, complete errors and powered two-body compilation

7 November 2026, after freezing `initial/constructor.md` (SHA256 `12075ea25306425ae494831807d83ecddc739c8970d261bc4166810c2eade69d`). Reviewed `principal/COHERENT_SWEEP_BRIDGE.md` and the frozen auditor initial. The deterministic sweep is strictly simpler and stronger than the random-activation construction in my initial. Keep the initial unchanged as scientific accounting.

## 1. Verdict on the mathematical bridge

The principal's finite-stroke support proof closes the main coherent-noise operation at the declared accepted DATA premises, provided the finite-depth circuit and joint fresh-source contract are stated explicitly. It avoids both a global Lindblad approximation and my more delicate relative-observable erasure estimate. The result is a direct local-contraction compiler: ideal local cooling contracts a syndrome Lyapunov function; finite-depth cones and sparse thermal/low-order coherent-error support leave enough contraction margin to restore the operating basin.

The source/no-return assumption is a real physical input. Neither perfect one-spin thermal marginals nor reduced-state reset convergence implies it. A finite one-use product thermal-spin reserve supplies it literally, and costs a number of spins proportional to service duration. A cyclic finite refrigerator must separately establish and pay for renewal.

### 1.1 Deterministic contraction

For a syndrome of energy u, let A>=kappa u be the number of initially active lowering labels. At the visit of such a label, it either lowers U or an earlier successful lowering changed a predicate it reads. If a successful update can spoil at most R-1 initially active labels, charge an initially active label to its own success or its first spoiler. Then A<=R S, where S is the total number of successful updates. Every success decreases integer U by at least one, so

    U_end <=u-S <=(1-kappa/R)u.

Using the principal's conservative a=min(1/2,kappa/(2R)) is valid. An unsuccessful ground-collision label cannot spoil a classical syndrome: its off-projector leaves that eigen-syndrome unchanged. Density is essential; a single available decreasing move would not yield a constant-fraction sweep contraction.

At full exchange angle pi/2, the ground-source collision has Kraus I-Pi_high and -iL. A syndrome basis vector follows one definite syndrome path, with the collision record retained in its spin. A coherent input is a linear combination of those paths; every output energy is <=(1-a) times its input energy. During a partial collision, a high/ground source vector is a superposition of high/ground and lower/excited vectors, never a higher DATA energy. Thus every partial ideal path stays in the safe energy/radius module. The canonical logical factor is identity throughout, including syndrome off-diagonals and bath/reference coefficients.

### 1.2 Finite physical cones

Let G=JU+sum_a Jd_a n_a over the current sweep's source spins. Every exchange V_a obeys [G,V_a]=0. It follows that the whole ideal propagator is the commuting free evolution exp(-iGt) times the finite scheduled product of exchange unitaries. The free evolution is a product of bounded-incidence commuting local gates; support colouring gives fixed depth. The exchange schedule has a fixed number of full-support colours. Therefore every suffix, including one beginning partway through a collision, has a uniform finite DATA-plus-current-source cone. The constant can be computed from the explicit patch supports and fixed schedule.

This remains true with arbitrary B-only CPTP propagation. To pull a perturbation insertion to the output, conjugate only its finite-system legs by ideal system/source suffix unitaries; commute the B-only propagators past those unitaries and leave them in chronological order. No inverse of a bath channel is used. Its norm is one and its DATA support is empty. A product of r transformed insertions consequently acts on the union of at most q_eff r finite-system sites, with arbitrary B coefficients. Its complete norm is still bounded by the product of the insertion norms. A Pauli/matrix-unit expansion may establish support and canonical neutrality, but the complete-norm estimate must be taken before that expansion, avoiding a coefficient-count or bath-dimension penalty.

### 1.3 Thermal-source pull-through and exact endpoint support

For each fresh thermal source, tau_d=(1-p_d)|0><0|+p_d X|0><0|X, with p_d<exp(-beta J). Expand the product source exactly. Pull each input X through the ideal full sweep; it has one bounded output cone, even though the sweep is not Clifford. If F excited sources and r perturbation insertions are retained, the resulting system leg acts after the ideal ground sweep on at most q_eff(F+r) sites. Hence a hard input energy cutoff vN gives

    U_out <=[(1-a)v +D_E q_eff(alpha+zeta)]N

on every retained left and right operator leg when F<=zeta N and r<=alpha N. This is a support statement, not a first-moment estimate. All local CPTP noise need not be stochastic: low-order HP Duhamel terms are signed but have the same finite support property.

The target canonical representative is valid because the endpoint energy stays below the accepted low-energy cutoff; the zero-syndrome coefficient comparing it to the ideal output has weight <=2C0 u_c N+q_eff(alpha+zeta)N<d_N. It is a stabilizer up to scalar. The retained signed map therefore factors id_L tensor C_signed on the *whole* promised logical/gauge/B module. This directly rules out a barrier crossing and return concealed by a low final energy.

The thermal tail is a positive mass tail from an actual independent source expansion; the coherent high-order tail is a complete-norm bound from the physical interval expansion. They must not be interchanged, normalized or described as one stochastic history.

### 1.4 Positive repair constant is exactly the stated 2delta

Let T=id_L tensor C_signed be Q-output-supported and ||Gamma-T||_diamond<=delta on the promised input module. Define complete contractions

    J(theta)=I_L/d_L tensor theta,
    A(X)=Tr_L[Q X Q]

in the canonical output frame, and C_good=A Gamma J. Then A T J=C_signed, so

    ||C_good-C_signed||_diamond<=delta,
    ||Gamma-id_L tensor C_good||_diamond<=2delta.

No additional Gamma-versus-compression penalty is needed. The direct triangle already compares the full actual channel with the embedded Q-output comparison. C_good is CP/TNI, acts on the same actual gauge/B algebra, and is never normalized. Because Gamma is TP and T is Q-supported, Gamma's output mass outside Q is at most delta on the maximally mixed-logical input, giving I-C_good^*(I)<=delta I. These estimates retain arbitrary references and initial logical/B correlations.

### 1.5 What the bridge does not prove

The model needs local complete error budgets during all gates, idles, switching and routing, plus physical full CPTP evolution. A simultaneous global timing or reset failure of probability p can apply an entire logical Pauli; local marginal fault rates do not exclude it. Likewise a future source tape already correlated with B is outside the literal product-source proof. These are exact applicability limits, not hypothetical requests for extra approval.

## 2. Powered two-body implementation with a fixed accuracy budget

Dropping the physical JU term is mathematically legitimate. Retain U solely as a stabilizer-syndrome Lyapunov observable. The ideal reference sweep consists of fixed-patch unitaries U_a on at most q_* DATA-plus-source qubits, followed by discarding each source spin. Every U_a is now a *driven* gate rather than an energy-conserving thermal operation. The same ground-source contraction and finite-cone proof apply to these reference gates. The physical implementation may use one- and two-qubit driven Hamiltonians.

For an explicit conservative compilation bound, put D_*=2^q_*. QR decomposition uses at most D_*(D_*-1)/2 two-level rotations and D_* phases. Gray-code/multiple-control decompositions give an ancilla-free elementary-gate bound

    m_*(q_*) <=C q_*^3 4^q_*

over arbitrary one-qubit rotations and CNOT. Barenco et al., *Elementary gates for quantum computation*, Phys. Rev. A 52, 3457 (1995), DOI 10.1103/PhysRevA.52.3457 / arXiv:quant-ph/9503016, is the primary predecessor. This is deliberately loose; q_* is a fixed locality constant, so the cost is independent of N,K. Ancilla-free synthesis avoids adding uncharged pure work qubits.

If the hardware library is finite and approximately universal, compile each one-qubit rotation to operator error <=delta_syn/(4m_*). A standard Solovay--Kitaev bound supplies

    m_syn <=C_SK m_* log^c_SK(4m_*/delta_syn)

elementary gates, for a fixed inverse-closed universal library and fixed c_SK. Dawson--Nielsen, arXiv:quant-ph/0505030, is the appropriate primary algorithmic source. One must verify the exact library/universality hypotheses; an arbitrary pair of physical controls is not automatically universal. For a continuous rotation library this extra approximation is unnecessary.

Choose a fixed per-patch synthesis error delta_syn and per-microgate actual complete error delta_phys. For c_cat N catalogue gates, each entire sweep has a discrete insertion budget bounded by

    mu_sweep <=c_cat [delta_syn+m_syn delta_phys]
       +mu_idle+mu_reset+mu_switch+mu_route.

Choose that fixed quantity below the bridge's alpha/(8e) margin. All choices are independent of N,K. No whole-sweep diamond approximation is promised: its distance may be O(N delta_syn); only the local insertion budget is small. This is precisely why exponential global simulation accuracy is unnecessary. The bounded-depth schedule uses at most chi m_syn microgate layers, duration

    tau_sweep <=tau_source+chi m_syn tau_micro+tau_route.

The output cone constant depends on the fixed sequence of catalogue patches; each microgate fault remains inside its patch until that patch completes. A coarse q_*^(chi+O(1)) bound suffices, regardless of m_syn. Peak local drive is a fixed O(1/tau_micro); finite systematic calibration errors and timing jitter enter delta_phys or the integrated local-generator budget. A finite max drive and nonzero noise rate may fail the displayed inequality on real hardware; no useful numerical threshold is inferred.

The source spin can be a thermal qubit of a fixed gap Delta_src at the fixed ambient temperature, with p_src=(1+exp(beta Delta_src))^(-1) below the source-count threshold. It need not have a gap matched to U, because U is not physical energy in this powered representation. Any source preparation/disposal remains charged. Future source spins must be isolated from old B until their turn.

### Thermodynamic and capability accounting

The simplified device is measurement-free active quantum error correction with thermal polarized ancillas and time-dependent two-body drive. It is not a two-body passive self-correcting material, an equilibrium quantum memory or a zero-work refrigerator. Its finite source reserve is O(NK), source/reset/transport events O(NK), elementary control locations O(m_syn NK), and elapsed cooling time K tau_sweep. For smooth local pulses of norm <=Omega and total variation <=C_var Omega per pulse,

    |W_drive| <=C_var Omega m_syn c_cat N K

is a conservative system-Hamiltonian work bound. Actual controller/refrigerator inefficiency is not determined by that bound. Source reserve preparation, transport apparatus and cyclic renewal costs must not be renamed zero simply because U is diagnostic.

This representation closes a finite-body implementation theorem with fixed local accuracy. It does not enable a capability unavailable to the strongest matched active FT machine, which receives the same cooling spins, two-body controls, clock/drive, routing and ports. Hong--Guo--Lucas already construct measurement-free finite-depth Gibbs-sampling circuits in Section 4 and Appendix E of arXiv:2403.10599v3. The generic two-body compilation is established circuit synthesis. Any novelty claim must be confined to a separately established local-contraction/coherent-bath/compiler theorem, not to powered thermal-ancilla QEC itself.

## 3. Noiseless classical processing: principled replacement boundary

The prior CFG port proof cannot erase its explicit noiseless classical assumption merely because its *outer* decoder was coherently compiled. Its internal FT gadgets also use classical processing.

A stronger primary predecessor is Aharonov--Ben-Or, *Fault-Tolerant Quantum Computation with Constant Error Rate*, SIAM J. Comput. 38 (2008), DOI 10.1137/S0097539799359385; full preliminary text arXiv:quant-ph/9906129. It explicitly uses only unitary gates, add-qubit and discard-qubit operations during computation and does not require intermediate measurements or classical operations. Its abstract is insufficient for the needed complete encoded-port statement, so the remaining source check must inspect its sparse-fault operator-state proof and interface implementation. A complete wrapper can either (i) verify this scheme meets CFG's scheme/interface hypotheses, or (ii) reconstruct its encoded-input/output correctness directly, keeping all auxiliary systems and references. Preparing every newly added qubit from the fixed-temperature polarized source gives a local preparation error p_src, not an ideal pure reset. Noise in the classical programme can be handled by a fixed compiled coherent circuit with encoded programme bits; the physical schedule still requires the explicitly local timing-error contract.

That replacement would be inherited general FT machinery with polynomial overhead for exp(-cN) target error and exponential service length. It would supply universality in the active staging layer, not prove that the collision memory's CNOT/selected-CCZ gate set alone is universal. Full source-specific checking is being continued separately; this review does not promote an abstract-only import.
