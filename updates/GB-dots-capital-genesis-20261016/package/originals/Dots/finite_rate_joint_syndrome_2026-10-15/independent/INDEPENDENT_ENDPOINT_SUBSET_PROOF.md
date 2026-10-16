# Independent check: simultaneous endpoint-subset effect theorem

Date: 2026-10-15. The proposed construction independently checked and proved below. This is an exact finite-rate, positive endpoint-effect theorem. It does not yet give a chronological fault history or a common-decoder memory theorem.

## 1. Statement

Let Z_1,...,Z_n be commuting Hermitian involutions on memory, extended by identity to an arbitrary finite persistent bath and reference. Consider

 L(t)rho=-i[H_0(t)+sum_i V_i(t),rho]
           +sum_i gamma_i(Z_i rho Z_i-rho),

where gamma_i>0, all Hamiltonians are Hermitian and generate well-defined finite-dimensional propagators, and

 [H_0(t),Z_i]=0,
 {V_i(t),Z_i}=0,
 [V_i(t),Z_j]=0 for j!=i,
 ||V_i(t)||<=J_i.                                         (A)

No bath commutation, weak-coupling approximation, gamma/J separation, or bath reset is assumed. The terms V_i may share arbitrary bath operators and need not commute with each other. H_0 may have arbitrary bath dynamics and syndrome-dependent bath Hamiltonians.

Let Pi_s be any nonempty joint initial parity sector, and let S be a selected subset of indices. Let F_{s,S} project onto states whose final parity differs from s_i for every i in S, with all other final parities unrestricted. For the actual channel Phi_t and genuine endpoint effect E_{s,S}=Phi_t^*(F_{s,S}),

 Pi_s E_{s,S} Pi_s <= [product_{i in S} min(1,B_i(t))] Pi_s, (1)

where, with d_i=sqrt(gamma_i^2+4J_i^2),

 B_i(t)=1/2 {exp(-gamma_i t)
            [cosh(d_i t)+(gamma_i/d_i)sinh(d_i t)]-1}.     (2)

The simpler sufficient bound is

 B_i(t)<=1/2 [exp(2J_i^2 t/gamma_i)-1].                    (3)

For J_i=0 set B_i=0. At small t, B_i=J_i^2 t^2+O(t^3); at weak J_i and fixed t its leading term is

 J_i^2[t/gamma_i-(1-exp(-2gamma_i t))/(2gamma_i^2)].

The formula has continuous gamma_i=0 limit B_i=sinh^2(J_i t), although (3) then does not apply. All inequalities are uniform over arbitrary initial states in Pi_s, including bath/reference entanglement. They are operator effect inequalities, not just estimates for a chosen bath state.

## 2. Exact telegraph representation

Unravel the dephaser with independent rate-gamma_i Z_i jumps. Its cumulative frame G(t)=product_i Z_i^{N_i(t)} conjugates V_i into xi_i(t)V_i, xi_i(t)=(-1)^{N_i(t)}, while leaving H_0 unchanged. The frame commutes with all endpoint parity projectors, so it cancels in the endpoint probability.

For the chosen subset S, first condition on the trajectories of all unselected randomizers. Absorb their modulated terms into H_0. By (A), they commute with every retained Z_i, and their trajectories are independent of the selected processes. The resulting H_0 can be arbitrary time dependent, and the following estimate is uniform in it. Thus it suffices to prove the theorem with all remaining species selected.

Pass to the H_0 interaction picture. W_i(u)=U_0(u,0)^dagger V_i(u)U_0(u,0) retains the same parity signature and norm bound, and is independent of the selected telegraph paths. For a pure joint input psi in Pi_s, expand

 U_xi(t)=T exp[-i integral_0^t sum_i xi_i(u)W_i(u)du].

Mixed states follow by purification or convexity. Bounded finite-dimensional Dyson series converge absolutely for each finite horizon, so the rearrangements and expectations below are legitimate. No bath factors are commuted or factored.

## 3. Parity selection and the double Dyson sum

A word contributes to F_{s,S}U_xi psi only if its number of W_i insertions is odd for every selected i. Expand the squared norm. Therefore both ket and bra insertion counts of each species i are odd; their combined count is 2m_i with m_i>=1.

For fixed combined ordered times

 0<u_{i,1}<...<u_{i,2m_i}<t,

the telegraph expectation is exactly

 exp[-2gamma_i sum_{r=1}^{m_i}(u_{i,2r}-u_{i,2r-1})].      (4)

Identity-start processes suffice. Since the combined count is even, there is no initial-sign factor and no stationarity assumption. Different species factor independently. The kernel is nonnegative; phases and operator matrix elements may have either sign, and are bounded in absolute value.

The norm of each ket/bra operator product is bounded by product_i J_i^{2m_i}, uniformly in psi and bath dimension. This remains valid for arbitrarily noncommuting W_i(u).

For each species, color its 2m_i ordered combined times as ket or bra with an odd ket count. There are

 sum_{r odd} binomial(2m_i,r)=2^{2m_i-1}

such colorings, and the remaining bra count is also odd. Once all colors and actual times are fixed, the chronological species order on each branch is determined. Conversely every original Dyson-word pair corresponds to exactly one such coloring and time ordering, except measure-zero ties. Summing species-word interleavings therefore partitions the product of per-species ordered simplices. There is no additional factorial or multinomial penalty.

Consequently the genuine endpoint probability is bounded by

 product_i sum_{m>=1} 2^{2m-1} J_i^{2m} I_m(gamma_i,t),     (5)

where I_m is the ordered integral of (4). This is a bound on a positive actual probability; it is not a signed inclusion-exclusion channel estimate.

## 4. Kernel integral and explicit constants

Pair each odd/even insertion into a duration v_r=u_{2r}-u_{2r-1}>=0. After fixing those durations, the available ordered pair-start volume is (t-sum_r v_r)_+^m/m!. Hence exactly

 I_m(gamma,t)
 =1/m! integral_{v_r>=0, sum v_r<=t}
       (t-sum v_r)^m exp[-2gamma sum v_r] product_r dv_r
 <=t^m/[m!(2gamma)^m].                                  (6)

Substitution in (5) gives (3) and the constructed product bound.

There is also an exact closed form for the positive scalar sum. If A_t=integral_0^t xi(u)du for a single telegraph process, symmetry of the integration cube gives E A_t^{2m}=(2m)! I_m. Therefore

 sum_{m>=1}2^{2m-1}J^{2m}I_m
 =E sinh^2(J A_t)
 =1/2[E cosh(2J A_t)-1].                                 (7)

The elementary two-state telegraph generating-function equation yields F''+2gamma F'-4J^2 F=0, F(0)=1,F'(0)=0 for F=E cosh(2J A_t). Its solution gives (2). This closed form is only evaluation of a scalar positive majorant; it is not an assumption that the noncommuting quantum dynamics reduces to a scalar telegraph Hamiltonian.

The bound holds for every normalized psi in the initial sector, so the quadratic-form criterion proves the operator inequality without the min caps. To cap individual factors at one, discard indices with B_i>1, observe the all-original-flips event is contained in the retained-flips event, and reapply the theorem with discarded terms absorbed into H_0. They commute with every retained parity. This proves (1).

## 5. Exact scope and failure cases

- The hypothesis that V_i flips ONLY selected parity i is essential. H=J X_1X_2 with checks Z_1,Z_2 creates both flips with probability J^2t^2+O(t^3), violating a product of two O(J^2t^2) factors. Such a term must be charged as one multi-parity support or handled by a different theorem.
- Bounded spatial support can ensure the one-selected-parity incidence condition for sufficiently separated selected checks, but the required interaction/check incidence must be proved, not assumed from the word local. All terms of a given selected signature can be grouped with the corresponding sum-of-norms J_i.
- Terms left in H_0 must commute with EVERY selected parity. Arbitrary exact sweep jumps are stabilizer covariant but may change selected syndrome sectors. Covariance alone is insufficient for this Hamiltonian H_0 argument. Inserting such corrections into the claimed theorem without another proof is invalid.
- The theorem supplies a final CP measurement effect, not independent faults, a causal fault instrument, or a trajectory of local support births. Multiple continuous excursions can have no net endpoint flip. The common-decoder/history interface remains a separate obligation.
- The initial state is in a known joint parity sector. A genuine initial measurement can prepare such sectors, and final measurements can support serial conditioning when subsequent intervals satisfy the same hypotheses. Hypothetical intermediate measurements cannot be inserted for free.
- The reference/bath can be arbitrary and persistent. However the specified check clocks remain exogenous independent Markov processes, and V_i cannot depend directly on their private realizations beyond the displayed frame conjugation.

## 6. Numerical verification

check_endpoint_subset.py evaluates exact Lindblad endpoint EFFECT operators, maximizing over the whole initial bath subspace, rather than checking just a convenient bath state. It tests shared noncommuting bath couplings, all initial sectors, different selected subsets, rates, strengths, and times. It also verifies the simultaneous-flip counterexample after deliberately violating the one-parity-per-term hypothesis. These are algebra checks, not a lifetime experiment.

Conclusion: the proposed simultaneous endpoint subset theorem is valid under its precise parity-incidence assumptions, with the sharper finite-rate bound (2). This is stronger than the preceding channel-norm regeneration interface, but it does not resolve the original correction-interleaved space-time memory theorem.
