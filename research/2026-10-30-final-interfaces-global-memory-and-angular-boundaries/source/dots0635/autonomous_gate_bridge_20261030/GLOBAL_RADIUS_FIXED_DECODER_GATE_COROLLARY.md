# One actual asynchronous logical CNOT with the SAME ordinary DATA decoder
2026-10-30. Governing COROLLARY CANDIDATE combining the newly reviewed global-radius native memory with the separately reviewed actual program-clock construction. It is not claimed accepted until this composition is reviewed. The older covariant-decoder gate result and all its source bytes remain unchanged.

## 1. Exact inputs and one physical instance
Use the global-exponential memory apparatus and code hypotheses at:
- `global_energy_memory_root_20261030/GLOBAL_EXPONENTIAL_COMPILER.md`, SHA-256 `0af0dc529eb96a359f9f5d0f9f00972ec90f1817dc2cb4753d95f196bd3f4f18`;
- `GLOBAL_EXPONENTIAL_CONTROLLER_INTERFACE_CANDIDATE.md`, SHA-256 `59c71b1c154457a0092b07610637eeb9a4f660c506f5277b43dbdd63d7b07155`.
Both whole global reviews are indexed in `GLOBAL_REPRESENTATION_REVIEW_INDEX.md`.

Use TWO identical CSS blocks and one joint logical/reference channel. N denotes the common size parameter; express the two block distances as d_N>=delta_d N and the number of paired resource columns as M_col<=C_col N. All constants absorb this fixed two-block convention. The global proof uses the four sector energies with one common safe radius. Choose its energy cutoff sufficiently small that the deterministic canonical DATA-weight bound in its killed basin is

    wt(E_s)<=r(s)<=alpha N,   alpha=e_cut/h<delta_d/4.

All actual native payloads, monitors, complete resets, new Ai aborts and fixed positive memory rates are retained. Declare the paired resource columns as NEW fixed-dimensional physical sites with actual joint DATA_A/DATA_B/program capability. This is not a remote LOCC regrouping or an assertion of elementary-qubit two-body locality.

Add one actual three-state program register per column with H_prog=Omega(|e><0|+h.c.), J_prog=sqrt(kappa)|1><e|, fixed Omega,kappa>0. Let U_i be the column DATA CNOT, U_*=product_i U_i, and

    G_i=P0+U_i(Pe+P1),   G=product_i G_i.

The actual nominal generator is EXACTLY Ad_G(L_mem+sum_i L_prog,i)Ad_Gdagger. Every memory term is conjugated. Program hopping is Omega(U_i|e><0|+U_i^dagger|0><e|), while e->1 remains CLOCK-ONLY. Onsite conjugation preserves hub/column two-site Hamiltonian support and onsite reset support in the declared grouped hardware.

The physical program registers remain part of the SAME bounded-body/per-site incident joint-cb noise decomposition as DATA/controllers. The external retained bath is separate. Arbitrary bounded-body partners may vary in time as in the new global memory theorem; there is no unconstrained program bath substitution. G preserves support and joint norm. Extra fixed local dimensions only change finite constants in the memory/noise proof. Choose ONE noise budget below both the adjusted global-memory margin and the clock-tail margin below. The nominal program generators commute the memory proof observable and its basin in the G frame, so they do not alter the memory drift.

Assume normal joint CPTP interval propagators and CP/TNI killed compression. Initialize exact encoded DATA, native ready clocks/workspace/locks, program clocks all0, and ONE fixed logical-independent monitor/bath state. Arbitrary logical/reference inputs are retained. No warm-start or physical encoding interface is silently added.

## 2. The SAME global killed state supplies both inputs
Let P be the reviewed radius-plus-energy basin of the global memory, independent of program registers in the G frame. It has

    r(s)<=alpha N

on EVERY retained source sector, not just with high probability. The complete-loss killed evolution is positive and factors as identity on the joint canonical logical subsystem times an auxiliary trace-decreasing map. Nominal programs are DATA identity in this frame; bounded-body noisy DATA edges remain canonical identities by the SAME global-distance argument.

The reviewed full-versus-killed joint channel bound is

    epsilon_mem(u)<=C N u exp(-b_mem N),
    1-Tr rho_P(u)<=epsilon_mem(u).

For the program clocks use `FINITE_PROGRAM_CLOCK_MOMENTS.md`, SHA-256 `e1fbaeea41d6052b37b86d8b8453c371316323d6e57a6494861e18d3f9b82d9b`. Its actual coherent Gramian gives, for every set S,

    Tr rho_P(u) product_(i in S)(P0_i+Pe_i)<=p_tail^|S|,
    u>=tau.

This is valid for the SAME UNNORMALIZED rho_P because P commutes the clock tests and complete-loss compression subtracts positive outgoing test gains. It does not condition on survival or assume reduced-clock Markovianity. The common bath and arbitrary stored-error/program correlations are retained.

For any fixed p_tail>0 choose a fixed finite tau and then a sufficiently small positive joint-noise budget using the explicit Gramian law p(u)^q=e^(-qr u)+(eta/r)(1-e^(-qr u)). No rate or latency depends on N. Programs need not all finish, and the late-time estimate is uniform under continuous reinfection noise.

## 3. Fixed target native frame, no program-phase inversion
Let F_mem be the full-Hilbert native forest unitary. Its target counterpart is the FIXED program-blind

    F_*=U_* F_mem U_*^dagger.

For the actual physical state frame G F_mem,

    F_*^dagger G F_mem=U_* E_prog,
    E_z=F_mem^dagger[product_(i:z_i=0)U_i^dagger]F_mem.

Label e already carries the target U_i, but may be conservatively included in the unfinished set H={i:z_i=0 or e}. Each dressed factor has a fixed full structural DATA support. Let r_gate bound its number of DATA qubits in BOTH blocks. Every DATA-Pauli times auxiliary coefficient of E_z has weight <=r_gate |H|, without a cancellation-based footprint reduction or a Pauli-count factor.

This fixed target frame does not undo actual program phases. It remains an explicitly IDEAL controller-frame operation, potentially using paired-column capability. The stronger claim below concerns the DATA recovery map; it does not make the entire physical readout circuit independent of the target frame or product/LOCC across blocks.

## 4. ONE ordinary product DATA recovery
Fix D_prod=R_A tensor R_B once from the codes: measure each block's syndrome, apply a deterministically chosen minimum-weight Pauli correction, then decode its fixed logical code basis. Choose the zero-syndrome correction identity. This map is independent of U_*, program labels, time and noise, and satisfies D_prod Enc=Id. No U_L is inserted in it.

Choose beta>0 so

    2(alpha+r_gate beta)<delta_d/2

with strict margin and enlarge N0 for integer radii. If |H|<=beta N, a final DATA coefficient relative to the physically transformed logical code is

    Q_(P,s)=U_* P E_s U_*^dagger,
    wt(Q_(P,s))<=2(alpha+r_gate beta)N<t_N,
    t_N=floor((d_N-1)/2).

The factor two is the maximum Pauli spread of transversal CNOT. This aggregate weight bound in particular bounds each block's weight.

Ordinary distance-t recovery corrects the ENTIRE linear span of these coefficients. For Pauli errors Q,Q' of weight <=t_N, different syndromes are orthogonal; equal syndromes make Q^dagger Q' a stabilizer up to phase because its weight is <d_N. Recovery is therefore scalar times logical identity on every cross term, including arbitrary controller/program/bath coefficients and reference operators. No stochastic-Pauli or independence assumption occurs. `FIXED_PRODUCT_DECODER_SPAN.md`, SHA-256 `c57c7c1a43bb267ae3a333ea600a0915ca3456a1aaca129f8d3234b2bad20677`, gives this algebra in detail.

Let Pi project onto |H|<=beta N inside P. Its canonical action is identity on logical information. The exact good decoded map after U_* E_prog is b_u Ad_(U_L), b_u=Tr Pi rho_P Pi, because U_* Enc=Enc U_L. U_L here comes from the ACTUAL physical transversal layer, not from recovery. No prefix-basin envelope is required for this global correctable-span step.

At time zero, native controllers are ready so F_mem and F_* are identity there, programs are all0 and G is identity. The SAME D_prod then returns the input unchanged, not CNOT(input). At fully completed program labels E_prog=I and the physical U_* gives the logical target. The fixed decoder cannot manufacture the gate on an unchanged code state.

## 5. Uniform aggregate tail and quantitative endpoint
For m=ceil(beta N), use the unfinished inclusion bound and M_col<=C_col N:

    Tr rho_P 1_(|H|>=m)
       <=binom(M_col,m)p_tail^m
       <=[(e C_col/beta)p_tail]^m.

If m>M_col the bad event is empty. Otherwise choose p_tail<beta/(e C_col), giving delta_prog(N)<=exp(-b_prog N) after fixed constants/rounding. No memory/program independence is used. There is NO memory-weight-tail term here, since P already has the deterministic alpha N bound.

Gentle projection for the positive subnormalized killed state costs at most 2sqrt(delta_prog). Unitary frames/suffix and fixed CPTP recovery are contractive. Comparing the full channel to the killed one and using 1-Tr rho_P<=epsilon_mem gives

    ||Out_u-Ad_(U_L)||_diamond
       <=2 epsilon_mem(u)+2sqrt(delta_prog)+delta_prog
       <=min{2,C N(1+u)exp(-bN)},
       u>=tau, N>=N0.

The actual output is

    Out_u=D_prod Tr_aux Ad_(F_*^dagger) E_phys,u Enc_init,

where auxiliary traces include native controllers, program registers and the retained bath; no bath access/reconstruction occurs. The bound is uniform for arbitrary logical/reference inputs with the specified fixed initialization.

## 6. Scope of this stronger endpoint
This improves the covariant-decoder result to the SAME ordinary product DATA decoder for storage and one fixed entangling layer. It is conditional on the reviewed linear-radius code/native-controller hypotheses and the actual paired-column program hardware. The constant latency and local parameters may be enormously unfavorable.

It does not implement noisy retrieval, guarantee an unchanged entire native-frame readout circuit, provide remote LOCC coupling, selected logical-pair addressability, a repeated reusable gate sequence, live handoff, non-Clifford universality, passive protection or a practical threshold. The older fixed-support covariant gate theorem is not silently broadened: this is a NEW corollary using the separately reviewed global topology-free memory class and the SAME explicitly local physical program-noise model.
