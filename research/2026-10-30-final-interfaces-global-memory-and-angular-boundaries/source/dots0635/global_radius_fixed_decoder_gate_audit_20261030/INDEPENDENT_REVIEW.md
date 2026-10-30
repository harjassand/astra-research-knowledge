# Independent composition review: asynchronous CNOT with the same ordinary DATA decoder
2026-10-30. Reviewer: audit_topology_free_noise.

## 0. Verdict and exact frozen source
**PASS for this stronger one-layer physical-gate corollary**, under the stated accepted linear-radius code/native-controller hypotheses and the explicit paired-column, initialization, noise and ideal-output assumptions.

Governing source: `autonomous_gate_bridge_20261030/GLOBAL_RADIUS_FIXED_DECODER_GATE_COROLLARY.md`, SHA-256 `fbf970ab41b550f83e074f95a8cc80e6e5fa98ddb1d97c33476bc83b5db3b1c7`.

The actual output uses the SAME ordinary product DATA syndrome decoder as storage. It contains no logical U_L supplied as a recovery operation. The target-dependent native forest inverse remains explicit and ideal; the entire physical readout circuit is not claimed target-independent or product across the two blocks.

The earned bound is

    ||Out_u-Ad_(U_L)||_diamond
       <=min{2,C N(1+u) exp(-bN)},   u>=tau, N>=N0.

All constants and the finite latency tau are independent of N and elapsed time. No load-bearing defect was found. This is a NEW corollary of the global-radius theorem; it does not silently expand the earlier fixed-support covariant-decoder gate receipt. No full-animal tail/connector argument or squared-memory-moment oracle is used.

## 1. One instance and a noncircular parameter choice
Take two identical CSS blocks as ONE joint logical/reference system. Express both code distances as d_N>=delta_d N and paired-column count as M_col<=C_col N. The global proof uses the sum of all four sector energies and all native history defects. Its common radius lies below every imported confinement/active-density radius. Constants may absorb the fixed distinction between single-block and combined DATA sizes; one convention is retained in every displayed inequality.

Before selecting the final memory parameters choose the global energy cutoff so

    alpha=e_cut/h<delta_d/4.

This is compatible with the accepted basin conditions e_cut<h r0/2 and 2r0<delta_d, and can be made smaller. The global proof's parameter order permits any such fixed positive cutoff. Its physical rates are then chosen once to satisfy its moment/barrier margins. This is not an assertion that an arbitrarily prebuilt device automatically satisfies a newly selected cutoff.

The native forest gate list and its bounded-depth structural cones are fixed by the code/payload/controller architecture, not by proof interpolation strengths or elapsed time. Let r_gate be the DATA support bound of a dressed missing local CNOT, counting both blocks. Choose a fixed beta>0 with

    alpha+r_gate beta<delta_d/4

and a strict slack. The program rates Omega,kappa may be any fixed positive rates; their finite Gramian gives fixed positive constants. Select the desired unfinished tail, then latency, then ONE sustained noise budget below both memory and clock requirements. Extra program dimension and paired grouping change finite local constants, not an N-dependent limit.

There is therefore one apparatus, one perturbation decomposition and one initialization. No rates are separately favorable for mutually incompatible memory and program processes.

## 2. Actual physical gauge and resource accounting
Each paired column must physically contain the two resource qudits and program register, with the declared joint DATA_A/DATA_B/program Hamiltonian capability. This is a new fixed-dimensional grouped site; regrouping remote LOCC-separated systems would not supply the coupling.

In the reference program frame the nominal generator is L_mem+sum L_prog,i, with finite three-state clock Hamiltonian and e-to-1 jump. Conjugate the ENTIRE generator by

    G=product_i [P0_i+U_i(Pe_i+P1_i)].

This produces the actual program hopping Omega(U_i|e><0|+U_i dagger|0><e|), while the e-to-1 reset remains clock-only. Every memory term is conjugated too. Hub/resource Hamiltonians remain hub/column two-site terms and onsite resets remain onsite in this grouped hardware. A construction conjugating only the program drive would not establish the corollary.

In the G frame, adding nominal clocks changes neither the memory proof observable nor its basin drift because both act as identity on program registers. The dirty coefficients, isolated useful coefficients and activity witnesses are the same native ones tensored with program identity. Thus no old dirty matrix is improperly reused after a changed native channel list: the native generator in this frame is exactly unchanged.

Physical program registers remain counted system factors in the SAME bounded-body/per-site incident joint-cb norm model as DATA and controllers. They are not moved into an unconstrained bath. G is onsite and preserves physical support and joint cb norm. The native forest and proof dilation enlarge supports only through fixed cones. Arbitrary time-varying/dense bounded-body partners are permitted because the NEW global-memory theorem and the clock hierarchy both use actual norm incidence, not a fixed conflict graph.

The external common bath is separate and may correlate all these registers dynamically. Normal joint CPTP interval propagators and CP/TNI basin compression remain hypotheses. Exact encoded DATA, native-ready labels, programs all0 and a fixed logical-independent auxiliary/bath state are required. The other arbitrary logical block is never treated as a fixed bath.

## 3. One killed state supplies memory radius and correlated clock tail
The global basin is the same radius-plus-energy projector P throughout. It is independent of program registers in the G frame. Every retained source syndrome has canonical total sectorwise weight

    r(s)<=U(s)/h<=e_cut N/h=alpha N.

Consequently the physical canonical DATA Pauli E_s has weight at most alpha N deterministically. There is NO memory-weight-tail event to union-bound.

The global full-versus-killed comparison applies to the extended native-plus-program system. Program-only nominal terms have no basin leakage; the already bounded physical local terms have total norm O(N). The proof gives epsilon_mem(u)<=C N u exp(-b_mem N), reference-stably, and survival deficit at most epsilon_mem.

The exact coherent clock Gramian yields A with a(P0+Pe)<=A<=P0+Pe and L_prog*A<=-r A. The local joint-noise subset hierarchy closes against

    p(u)^q=exp(-qr u)+(eta/r)(1-exp(-qr u)),
    Pr(all S unfinished)<= [p(u)/a]^|S|.

The factors a and r are fixed actual-clock constants, not service-rate assumptions. Choose tau and eta so p(u)/a<=p_tail for every u>=tau.

The SAME hierarchy applies to the unnormalized killed state. For each positive program test M, [P,M]=0, and

    L_P*(PMP)=P L*(PMP)P<=P L*(M)P.

The omitted contribution is positive outgoing gain for the FULL physical generator. No survival renormalization, reduced-clock Markov assumption, CP domination of killed by unmeasured evolution, or independence from stored errors is used.

## 4. Exact target frame and every final DATA coefficient
Let F_mem be the native forest unitary and F_*=U_*F_mem U_* dagger the fixed target forest. Direct multiplication gives

    F_* dagger G F_mem=U_* E_prog,
    E_z=F_mem dagger [product_(i:z_i=0)U_i dagger] F_mem.

Only label0 is missing; counting 0/e as unfinished is conservative. Each dressed factor is supported on a fixed whole structural cone. If H is the unfinished set, every DATA-Pauli coefficient P in E_z has

    wt(P)<=r_gate |H|.

This follows from support of the product, not cancellation in the exact unitary. Coefficients retain all native-controller/program/bath correlations. No raw occupation envelope or prefix-basin condition is needed for this global final-distance argument.

On a source canonical branch E_s, the DATA action is

    U_* P E_s Enc
       =(U_*P E_s U_* dagger) Enc U_L.

Transversal CNOT is Clifford and spreads any one-qubit Pauli to at most two DATA qubits. Therefore the final Pauli Q relative to the physical target logical code obeys

    wt(Q)<=2(alpha+r_gate beta)N

whenever |H|<=beta N. By the strict parameter slack and sufficiently large N0 this is at most t_N=floor((d_N-1)/2), indeed strictly smaller as written in the source. Its weight in EACH block is bounded by the same aggregate quantity. All rounding constants are harmless after N0 is enlarged.

## 5. The fixed ordinary decoder corrects the coherent span
Fix each block's ordinary minimum-weight Pauli syndrome recovery once, with deterministic ties and identity zero-syndrome correction, then its fixed code-basis decoding isometry. D_prod is their product. It is independent of U_*, program labels, readout time and noise. It is also used for storage.

For any two errors Q,Q' of weight <=t_N per block, different syndromes give orthogonal branches. If their syndromes agree, Q dagger Q' has zero syndrome and weight <=2t_N<d_N and hence acts as a stabilizer up to phase. Thus recovery has scalar logical identity action on every cross term Q Enc(rho)Q' dagger. This is a linear operator identity valid with all logical/reference operators and arbitrary auxiliary coefficients. It corrects the entire coherent span, with no sum of Pauli coefficient norms and no stochastic-Pauli-mixture assumption.

The killed joint state has identity logical factorization from the fixed initialization. Projecting onto |H|<=beta N inside P acts only on its canonical auxiliary factor. The final coefficient calculation and recovery identity therefore give exactly

    D_prod Tr_aux[Ad_(U_*E_prog)(Pi rho_P Pi)]
       =b_u Ad_(U_L)(rho_LR),
    b_u=Tr Pi rho_P Pi.

The scalar is independent of arbitrary logical/reference input. It is the ACTUAL physical transversal U_* that contributes U_L; the decoder supplies no logical CNOT.

The distinction in readout scope is essential: D_prod is unchanged, but the ideal native frame is F_* rather than the storage frame F_mem. F_* may involve paired-column operations. The corollary neither promises an unchanged entire readout circuit nor implements noisy retrieval.

## 6. Aggregate tail and exact quantitative composition
For m=ceil(beta N), subset union and the unnormalized inclusion bound give

    Tr rho_P 1_(|H|>=m)
       <=binom(M_col,m)p_tail^m
       <=[(e C_col/beta)p_tail]^m.

When m>M_col the event is empty. When beta N is an integer, the event on the left also includes the threshold itself and is merely a conservative upper bound for Pi's complement; this does not weaken the exponential conclusion. Choose p_tail<beta/(e C_col) with strict slack. Then delta_prog<=exp(-b_prog N) after fixed constants. Correlations with stored DATA and bath never enter this combinatorial inequality.

Let a_u=Tr rho_P. Gentle compression gives ||rho_P-Pi rho_P Pi||_1<=2sqrt(delta_prog), and 1-b_u<=1-a_u+delta_prog. Exact unitary frames and fixed CPTP recovery are contractions, so

    ||Out_u-Ad_(U_L)||_diamond
       <=2 epsilon_mem(u)+2sqrt(delta_prog)+delta_prog
       <=min{2,C N(1+u)exp(-bN)}.

This is uniform with references. The O(N) prefactor arises from the NEW global moment/boundary theorem, rather than the old animal estimate's N^(3/2) prefactor. No stronger output claim is inferred merely from a toy code experiment.

## 7. Time zero, tests and retained scope
At time zero native controllers are ready, so F_mem is identity on arbitrary DATA with that ready sector; F_* is also identity there. All programs are0, so G is identity. Thus the exact same D_prod returns the input, not CNOT(input). At completed program labels E_prog=I and ordinary recovery corrects errors around the actual physical U_* action. This rules out the specific free-recovery-gate artifact.

I inspected and reran the author's check_fixed_product_decoder.py in this audit directory without modifying the source. It actually calls the ordinary product syndrome decoder, with no U_* inverse or U_L operation in the recovery function. On two [[7,1,3]] Steane blocks plus a reference it checks all single-missing columns and coherent two-DATA-qubit corruption on that same column. Trace-norm discrepancies were below 4.1e-16; time-zero output is identity. The script is explicitly an ideal-code sanity test, NOT a native controller/noise/threshold simulation or a replacement for the proof above.

This closes one fixed asynchronous entangling layer with the same ordinary DATA recovery, under the accepted linear-radius native theory. It does not establish selected logical-pair addressability, arbitrary programs, non-Clifford universality, repeated reusable gates, live handoff, warm-start entry, remote LOCC, physical fault-tolerant retrieval, passive protection or practical constants. The prior covariant-decoder result and connected-animal receipts remain unchanged. No external state was mutated.
