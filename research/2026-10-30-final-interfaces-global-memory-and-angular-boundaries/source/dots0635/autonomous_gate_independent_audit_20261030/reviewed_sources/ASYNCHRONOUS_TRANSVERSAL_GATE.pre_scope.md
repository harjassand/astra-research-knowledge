# A protected entangling gate with unsynchronized local completion clocks
2026-10-30. Root construction candidate. This is the next scientific attack after accepted native memory; it is NOT yet an accepted gate theorem or a universal processor.

## 1. Useful target and actual physical construction
Take two identical CSS Tanner memory blocks. Pair corresponding DATA resource sites into fixed-dimensional columns, retaining their tags/monitors and both private hub families. Transversal CNOT is U_*=product_i U_i, onsite on each paired column, and implements a known nontrivial logical CNOT on corresponding logical coordinates. It normalizes the two-block code. This is not an arbitrary addressable logical gate or an arbitrary unknown-state encoder.

Add a three-state program clock 0,e,1 at each column. In a reference frame its generator has H_prog=Omega(|e><0|+|0><e|) and clock-only jump sqrt(kappa)|1><e|. State1 is absorbing. Define the onsite unitary

    G_i=I_DATA tensor |0><0|+U_i tensor (|e><e|+|1><1|),
    G=product_i G_i.

Define the actual physical generator by conjugating L_mem+sum_i L_prog,i by G. This is an EXACT model, not adiabatic elimination. Its program Hamiltonian is Omega(U_i|e><0|+U_i^dagger|0><e|), while e->1 remains CLOCK-ONLY because both endpoints have the same U_i frame. Conjugation by onsite G_i preserves every two-site hub/column Hamiltonian and every onsite reset. Local dimensions increase by fixed factors, not by N. Pairwise qudit interactions are not claimed to be elementary two-qubit interactions. Pairing requires actual colocation and joint DATA_A/DATA_B/program control in the declared column hardware; renaming distant sites does not supply a coupler or an LOCC operation.

Treat the two blocks as ONE product-code channel with an arbitrary joint logical/reference input and all four CSS-sector observables. Cross-block column noise is a bounded local term; the other logical block is not a fixed bath. Enlarge the fixed component/support geometry before selecting constants.

Initially program clocks are0, so G is identity on the supplied encoded input. In the G frame the accepted memory generator runs unchanged alongside independent finite-rate program clocks. Bounded local physical noise keeps its joint norm and support under this onsite change of frame. All program/controller noise remains present.

## 2. Why actual program phases must NOT be undone at output
Let F_mem be the native memory forest unitary. Physical state has the frame order G F_mem rho_frame F_mem^dagger G^dagger. A program-blind output uses the FIXED target forest frame

    F_target=U_* F_mem U_*^dagger,

not the actual G-dependent inverse. Then

    F_target^dagger G F_mem
      =U_* E_prog,
    E_prog=F_mem^dagger(U_*^dagger G)F_mem.

For a program-basis label z, E_prog is a product of missing U_i^dagger gates for the z_i=0 columns, dressed by F_mem. Each dressed factor has bounded structural support; include its fixed footprint in the nominal proof geometry. Labels e already carry U_i, but may conservatively be counted unfinished.

Tracing the program after this output makes its basis labels a positive classical mixture even if they were coherently entangled with DATA/bath before the trace. No physical program measurement is assumed.

Choose the ideal target-code decoder covariantly, D_target=Ad_(U_L) D_base Ad_(U_*^dagger), where U_L is the known logical action and D_base is a fixed code decoder. Since U_* Enc=Enc U_L, D_target Enc=Id. This identity is essential: the decoder is NOT allowed to create the desired gate on an unchanged code state. At time zero all native clocks are ready and F_target=I there, so the output is identity, not a fictitious CNOT.

An operational live-controller handoff and noisy physical decoder remain separate from this mathematical encoded-gate criterion.

## 3. Actual unfinished-clock inclusion bound, with memory/bath correlations
Let Q_i=|0><0|+|e><e|. The finite nominal clock has a uniform survival bound ||exp(t L_prog,i^*)Q_i||<=C0 exp(-r t), with r>0: its two-dimensional no-jump generator has no dark subspace because Omega,kappa>0.

For any selected clock set S, fixed horizon tau, and u in (0,1), use the backwards positive test

    M_s=product_(i in S)[uI+(1-u)exp((tau-s)L_prog,i^*)Q_i].

Factors are positive, onsite and between uI and I. In the program frame, nominal memory acts trivially on them and partial_s M_s+L_nom^*M_s=0. The incident-norm local-noise inequality gives N_s^*M_s<=C(u,q)eta |S| M_s. Thus, from ANY joint starting state,

    Pr(all selected clocks unfinished at tau)
      <=p_prog^|S|,
    p_prog=exp(C eta tau)[u+(1-u)C0 exp(-r tau)].      (1)

Choose u and exp(-r tau) small, then eta small. All choices are fixed independently of N. Applying this on the last tau interval gives a uniform bound at every later readout time; no growing exp(eta*time) loss is accepted.

The SAME bound holds for the unnormalized killed memory state. Its basin projection acts on memory DATA/controllers, not program clocks, so it commutes M_s. Complete-loss compression subtracts a positive outgoing M_s contribution, and the same differential inequality applies. This avoids an invalid claim that the killed process is dominated by the unmeasured process in CP order.

## 4. A stronger memory moment can be earned with the same physical hardware
The memory proof can be run for a finite collection of nearby admissible animal exponents/temperatures, choosing the physical rates and perturbation budget to satisfy the finitely many strict inequalities simultaneously. The auxiliary CP proof credits may differ; no extra hardware operation is performed.

In particular choose a_hi>a_low and theta so the killed state obeys

    Tr[sum_A f_(a_hi,theta)(A)^2 rho_killed]<=C N.     (2)

The squared summand is the raw animal weight for parameters (2a_hi,theta^2). The finite-family compatibility and its actual basin preservation are derived in SIMULTANEOUS_MOMENTS_COMMON_BASIN.md and require independent review; they are not inferred by squaring a dressed moment. Because all accepted local corrections decrease each tuned raw potential, the second proof can use the same raw component/potential basin. Rates may be extremely unfavorable.

## 5. A worst-case suffix envelope retains correlated noise and all Pauli branches
Let H be the unfinished-column set. Define Gamma_i to contain EVERY occupation projector whose FULL support intersects the entire structural support cone of the dressed missing gate, including all unary-energy vertices and complete history-token bundles. Do NOT select only projectors failing to commute with the exact unitary: Pauli-term cancellations can hide occupation changes. This conservative Gamma_i covers every individual DATA-Pauli/controller coefficient. Put Gamma(H)=union_(i in H)Gamma_i. Define the commuting envelope

    V_env(label,H)=sum_A f_(a_low,theta)(label) theta^(-|A intersect Gamma(H)|).

It bounds the raw lower potential of EVERY Pauli coefficient path and EVERY prefix of the missing-gate product, since labels outside Gamma(H) cannot change. There is no multiplication by the number of Pauli coefficients.

Let each clock affect at most k labels and each label have at most b incident clocks. Equation (1) yields

    Pr(S subset Gamma(H))<=b^|S| p_prog^(|S|/k),
    E theta^(-2|A intersect Gamma(H)|)
       <=[1+b p_prog^(1/k)(theta^(-2)-1)]^|A|
       =exp(c_prog |A|).

Memory labels and program projections commute, though their states need not be independent. With Delta=a_hi-a_low, Cauchy-Schwarz gives

    E[f_low(A) theta^(-|A intersect Gamma(H)|)]
       <=exp[-(Delta-c_prog/2)|A|] sqrt(E f_hi(A)^2).

A second Cauchy-Schwarz over ALL animals, together with (2) and the rooted count A0^m, yields E V_env<=C'N provided

    2Delta-c_prog>log A0.

Reserve a spatial exponent margin first, then make p_prog sufficiently small. This is not an assumption of independent program failures and memory errors.

## 6. Logical action and error claim to be audited
On the commuting source projector V_env<M_edge/2, with the memory's safe components, every local Pauli branch of E_prog remains below the canonical local-edge barrier at every prefix. It therefore has identity logical action in the base canonical gauge. This is a common-span statement covering coherent DATA/program/bath correlations.

The complement has killed-state mass O(N/M_edge). Gentle projection gives an exponentially small channel error, reference-stably. The memory's full-versus-killed error is already C N^(3/2)time exp(-cN). Combining these with the fixed target frame/decoder should therefore yield, for physical times time>=tau,

    ||D_target Tr_ctrl,prog Ad_(F_target^dagger) E_time Enc_init
                  -Ad_(U_L)||_diamond
       <=C N^a(1+time)exp(-c'N),                     (3)

for fixed a and positive constants, under the declared noise budget. Equation (3) is a PROPOSED conclusion pending independent review of (2), the envelope projector/common-span argument, and target-decoder covariance. It is not obtained by applying U_L freely at readout: D_target is identity on the code, and the time-zero sanity test fails to perform U_L.

## 7. Scope, comparators and remaining operations
The intended new consequence is a genuine entangling logical operation driven by independent finite-rate local clocks, while native recovery remains active. Ordinary scheduled transversal CNOT is the strong comparator; transversal CNOT itself is not new. The proposed gain is removal of synchronized completion as an operational requirement under the same continuous noisy-controller model.

This is only a fixed transversal logical layer on paired identical blocks. It does not establish selected logical-pair addressability, non-Clifford universality, an arbitrary-program autonomous computer, or a reusable live mode-switch protocol. Fixed program-clock initialization and the encoded input are explicit. Physical noisy output/transfer remains subject to its own interface proof. Grouped-site hardware and maintained reset resources retain their actual costs; no practical threshold is claimed.
