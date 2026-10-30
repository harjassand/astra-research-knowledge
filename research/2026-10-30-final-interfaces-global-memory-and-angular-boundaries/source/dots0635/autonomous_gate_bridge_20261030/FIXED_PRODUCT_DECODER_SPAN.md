# Stronger endpoint: one fixed ordinary product-code DATA recovery
2026-10-30. NEW derivation, preserving the separately accepted covariant-target-decoder theorem. This note proves the endpoint conditional on an exponentially small TOTAL canonical-weight tail and the already earned unfinished-clock moments. The new full-animal tail/connector argument is supplied separately by root and is not assumed proved here.

## 1. Exact code/decoder convention
Let each identical block have N DATA qubits, stabilizer code distance d_N>=delta_d N, and t_N=floor((d_N-1)/2). Fix its logical basis and encoded isometry Enc ONCE. Choose the ordinary minimum-weight Pauli syndrome recovery R: measure the block stabilizer syndrome s; apply a fixed minimum-weight Pauli representative R_s^dagger (with R_0=I); then apply the fixed code decoding isometry. Ties are resolved once, independent of the target gate, program labels, elapsed time and noise. A full deterministic completion on every syndrome makes this a CPTP map. No efficiency claim is made for its implementation.

Use D_prod=R_A tensor R_B for BOTH ordinary storage and the entangling-layer output. It is an ideal product DATA recovery, with no joint U_L operation inserted at readout. It is identity on the fixed product code. It need not agree with the earlier component-canonical decoder on arbitrary high-weight error states; the new total-weight estimate makes those exceptional readout states exponentially rare.

Native controller frames remain explicit. Storage uses its fixed F_mem inverse; the programmed layer uses the fixed TARGET native forest inverse F_*=U_* F_mem U_*^dagger, exactly as before. Thus the DATA decoder is the SAME map, but the entire native-frame readout circuit is not asserted unchanged. Neither frame depends on the ACTUAL program phases. Physical/noisy retrieval remains outside this note.

## 2. Full coherent distance-t correctable span
For any two block Pauli errors P,Q with wt(P),wt(Q)<=t_N, equal syndromes imply P^dagger Q is in the stabilizer up to phase, since it has weight <=2t_N<d_N and cannot be a nontrivial logical Pauli. Different syndromes are orthogonal. Therefore ordinary syndrome recovery satisfies

    R[P Enc rho Enc^dagger Q^dagger]=c_(P,Q) rho,

where c_(P,Q) is zero for different syndromes and a scalar phase for equal syndromes. This is a linear identity on all operators rho, including logical/reference operators.

For two blocks, D_prod has the same property for the entire linear span of errors whose weight in EACH block is <=t_N. Coefficients can be arbitrary operators on native controllers, program clocks and a common retained bath. Summing coherent error branches is therefore legitimate and incurs NO Pauli-count factor. Positivity/trace preservation of the actual recovery determine the ancillary channel; no norm bound on each unnormalized coefficient is needed.

## 3. Source canonical weight and dressed missing-gate support
In the base native forest/canonical representation, each raw source syndrome s has a fixed canonical DATA Pauli E_s. Let

    w_can(s)=sum of the reduced X/Z representative weights in the four sectors.

This upper-bounds the total physical Pauli weight of E_s across both blocks; overlaps of X and Z are merely overcounted. History flags are auxiliary and need not be clean for this final distance argument.

Let H be the conservative unfinished set (program labels 0 or e). The exact missing set is a subset (labels 0). As in the accepted physical gauge,

    F_*^dagger G F_mem=U_* E_prog,
    E_z=F_mem^dagger [product_(i:z_i=0) U_i^dagger] F_mem.

Each dressed factor has a fixed structural support. Let r_gate bound the number of DATA qubits in that support, counting both blocks. The entire E_z is supported on the union of those cones, so in its DATA-Pauli expansion

    E_z=sum_P P tensor C_(P,z),
    wt(P)<=r_gate |H|.

This is a support bound on every coefficient, regardless of cancellation, controller coherences or overlap between cones. Controller/workspace/history changes remain in the coefficients. No raw occupation footprint pruning and no prefix-basin assumption enter this global distance argument.

On the source projector w_can(s)<=alpha N and |H|<=beta N, every Pauli coefficient of the actual final framed output has DATA error

    Q_(P,s)=U_* P E_s U_*^dagger

relative to Enc(U_L rho U_L^dagger). Transversal CNOT is Clifford and each one-qubit Pauli spreads to at most two DATA qubits, hence

    wt(Q_(P,s))<=2[alpha+r_gate beta] N.             (3.1)

In particular its weight in each block obeys the same upper bound. Choose fixed alpha,beta>0 with

    2(alpha+r_gate beta)<delta_d/2,

leaving a strict margin; enlarge N0 for the floor and minus-one in t_N. Then (3.1) is <=t_N. If alpha is specified PER SECTOR instead, replace alpha here by the sum of all four sector bounds. No fixed-alpha conclusion is claimed for a code family lacking a positive relative distance.

## 4. Joint good projector and correlations
Let rho_P(u) be the SAME unnormalized killed state used by native storage, with its exact joint logical/reference factorization in the canonical gauge. Define Pi to project onto BOTH source bounds in Section 3, inside P. These are commuting raw-syndrome and program tests. Pi acts as identity on the logical factor; it can filter an arbitrarily correlated auxiliary state.

Suppose the new full-animal argument proves

    Tr rho_P 1_(w_can>alpha N)<=mu_mem(N)

uniformly in u, with mu_mem exponentially small. From the accepted physical program inclusion bound Tr rho_P product_(i in S)B_i<=p_tail^|S|, choose m=ceil(beta N). A union bound over m-subsets gives, without independence or normalization,

    Tr rho_P 1_(|H|>=m)
      <=binom(N,m) p_tail^m
      <=[(e/beta)p_tail]^m.

Choose p_tail<beta/e by a fixed latency and a sufficiently small common noise budget. Thus mu_prog(N) is exponentially small. The joint bad mass obeys

    Tr rho_P (I-Pi)<=mu_mem+mu_prog=Delta_N.

No claim of locally stochastic residual DATA noise follows from the total-weight tail, and none is needed here.

## 5. Same product decoder earns the physical logical CNOT
After Pi, the stored state is a coherent canonical error expansion with the SAME logical/reference input. After the actual suffix and full transversal layer, every DATA error coefficient Q_(P,s) lies in the distance-t correctable span by Section 3. Section 2 therefore yields

    D_prod Tr_aux[Ad_(U_* E_prog)(Pi rho_P Pi)]
        =b_u Ad_(U_L)(rho_LR),

with b_u=Tr(Pi rho_P Pi), independent of the arbitrary logical/reference input. The U_L in this equation comes from the ACTUAL physical transversal U_*, not from D_prod. Off-diagonal source syndromes and program/controller/bath coherences are handled by the correctable-span identity. Tracing programs is optional for the algebra, and if done gives the exact positive program-label mixture already established.

At time zero the native ready frame is identity, programs are all0, and U_* E_prog=I on the supplied input. D_prod then returns rho, not CNOT(rho). For completed programs E_prog=I and D_prod recovers the physical U_L action. The same D_prod also gives the ordinary storage identity channel on the low-total-weight source span (set U_*=I and omit E_prog).

## 6. Quantitative comparison
Let epsilon_mem(u) be the existing joint full-versus-killed error, and a_u=Tr rho_P. Complete-loss storage gives 1-a_u<=epsilon_mem. Gentle projection for the subnormalized state gives

    ||rho_P-Pi rho_P Pi||_1<=2 sqrt(Delta_N).

The exact unitary frames/suffix and the fixed CPTP product recovery are contractive, so uniformly with reference

    ||Out_u-Ad_(U_L)||_diamond
       <=2 epsilon_mem(u)+2 sqrt(Delta_N)+Delta_N.   (6.1)

When epsilon_mem<=C N^(3/2)u exp(-b ell) and both tails are exponentially small in N, (6.1) gives the same polynomial-times-exponential gate error (with the relevant minimum exponent). No physical retrieval implementation or local stochastic residual has been inferred.

## 7. Exact remaining obligation
The only new probabilistic input in this endpoint note is the uniform exponentially small TOTAL reduced-weight tail for rho_P, with the same physical apparatus and a suitably connected ANALYTICAL animal graph. Root's full-animal/connector derivation must earn that input and its parameter compatibility. Once earned, the decoder/Pauli-span step above uses only code distance, bounded dressed DATA supports, the actual target frame and the already reviewed clock inclusion bound. It does not rely on the previous gate-dependent covariant DATA decoder.
