# A universal native recovery oracle for one logical qubit in a positive-operator noise family

28 October 2026. **New corollary; separate independent receiving pending.** Governing dual: `convex_positive_operator_clifford_acquisition_20261028.md`, source SHA 4bb1b5ce0a9f688e8127a65651ba0059ab5f98a4d570b891c8880c82373ee439 and its separate receipt. This corollary connects that received convex dual to the actual native-channel recovery task; it is not a new recovery SDP or a collective multi-logical capacity theorem.

## 1. Native channel and exactly what the decoder can access

There is ONE logical input qubit L, its inaccessible reference R, and the FULL physical output P of dimension d=2g. Given the allowed calibration/past record h and an actual source-memory state omega, the native one-use reduced channel is N_(h,omega):L->P after discarding outgoing inaccessible source memory. The unknown logical payload/reference is initially product with that source memory, or conditionally product given the allowed classical record, so this one-use channel is well defined.

A decoder is any CPTP map D:P->L. It may be selected using the permitted prior record and knowledge of N, but it has no direct access to outgoing source memory, an additional environmental record, or an unmodeled protected copy of the input. The benchmark is entanglement fidelity of D composed with N on the normalized maximally entangled logical/reference pair.

Suppose all actual conditional channels in the declared family have signed contrasts

    C_j=N(sigma_j/2)=sum_k B_k T_kj,
    B_j=U(sigma_j tensor I_G)Udagger,
    T_kj=T_jk Hermitian, [T_kj,B_l]=0,
    [T_jk]_(j,k=X,Y,Z)>=0.                                  (1)

The same U and logical algebra B hold across the family. T and the unsigned output rho=N(I/2) may be unknown and change with past history and retained memory. T entries need not commute with each other. Native N is an ACTUAL CPTP source channel; arbitrary algebraic T,rho not realizing a physical channel are not introduced. A strictly positive T gap is needed for useful acquisition/completion, but NOT for the oracle identity below.

## 2. Exact full-CPTP oracle identity

For any CPTP decoder D, its adjoint Phi=D* is unital completely positive. Let A_j=Phi(sigma_j). The normalized Bell expansion gives exactly

    F_e(D N)=(1+sum_j Tr(A_j C_j))/4.                         (2)

The constant is one because D N is trace preserving. In particular the affine translation/unsigned rho does not enter this entanglement-fidelity objective. This is not a claim that translation is irrelevant to every operational task.

The governing convex dual proves, for every such unital CP Phi,

    sum_j Tr(A_j C_j)<=Tr(sum_j T_jj),                        (3)

with equality at the physical embedding A_j=B_j. That embedding is the adjoint of the explicit subsystem extraction

    D_star=Tr_G composed Ad_(Udagger).

Therefore

    max_(D CPTP P->L) F_e(D N)
       =F_e(D_star N)=[1+Tr(sum_j T_jj)]/4.                  (4)

This is the full CPTP oracle, not a decoder menu, a unitary-only comparator, a best fixed gauge estimate or a model-specific numerical optimizer. The positive-operator block supplies a valid dual certificate over the entire channel set. It can have noncommuting spectator blocks, so no readable classical flag or scalar common noise contraction is required.

## 3. Why the same acquired operation can survive changing unknown noise

Equation (4) applies separately to every allowed (h,omega), while D_star depends only on the fixed algebra B. Thus one reusable physical operation is pointwise optimal for the entire declared conditional family, even when a decoder allowed to know the CURRENT conditional native channel selects its best CPTP map. It is unnecessary to reconstruct every changing T or rho merely to choose the optimal one-qubit entanglement-fidelity decoder.

The finite positive-fit/convex-acquisition construction learns B from actual ordinary calibration data. If its accepted receiver Dhat is within half-diamond zeta of D_star on ALL physical inputs, then for every later native channel satisfying (1),

    loss(Dhat N)<=min_(D CPTP) loss(D N)+zeta.                 (5)

Its bad-certificate mass, calibration-record discrepancy, conditional acceptance denominator and whole-service implementation errors are retained exactly as in the governing construction. The accuracy is not asserted on arbitrary bad records. Finite true gaps/excitation, source caps and candidate/control costs remain substantive. Payload introduction follows acceptance, so no unknown input is held during calibration.

The complete-map inverse comparison still holds for arbitrary continuing-memory/reference correlations as a separate operation-norm theorem. The N-dependent oracle statement here is specifically a one-use reduced channel with the stated initial-input contract. Do not replace it by a claim of optimal complete environmental output, causal multi-time strategy, or joint multi-payload fidelity. Discarding gauge may matter for other tasks, even though it is optimal for this native single-use objective.

## 4. Scope that must not be enlarged

- If only a local output envelope is available, (4) optimizes decoders acting on THAT envelope. It is not an oracle over extra physical outputs that were discarded before forming the contrasts.
- Several logical qubits require their own joint comparison. Local one-qubit oracle facts do not establish a collective full-CPTP optimum or a channel capacity.
- Future channels must retain the same B and positive operator-block contract for the oracle claim. The acquired inverse remains close to the particular D_star even when later noise violates the oracle premise, but D_star need not then be optimal.
- Arbitrary component-specific coherent rotations do not share a positive common orientation merely because each has its own polar factor.
- A determinant-negative canonical residual from the separate handedness construction is not automatically positive operator-block noise; that wider algebra-identification result does not inherit this oracle corollary.
- A completely forgetting channel has T=0 and may satisfy the algebraic premise. Its maximal Bell fidelity is only 1/4, and it provides no inverse-learning excitation. The theorem does not recover information that the native channel has destroyed.

The sampled noncommuting-spectator pilot is consistent with (4): the full-CPTP recovery SDP and exact extraction both have native Bell loss .19 on its noiseless source, and fitted candidates approach that loss from finite ordinary data. The pilot does not independently prove the theorem, practical budget, or historical novelty.

## 5. Consequence

This gives a structural reason to learn a reusable physical information algebra rather than repeatedly fit the entire current noise channel: within the declared noncommuting positive-operator family, the same extraction is already the native single-qubit CPTP oracle. The conditional source family, acquisition costs, physical control and objective remain explicit. Historical priority, broad unknown-noise coverage, useful hardware budgets and collective quantum-computing consequences remain unresolved.
