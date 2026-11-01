# Flag-free source repair on ALL physical clock strings

Reconciled extension, 2026-11-01 16:49 UTC. This closes the mean-level corrupted-clock contribution conditionally on the explicitly specified bounded-arity GKSL primitives. It does not derive those primitives from two-body Hamiltonians.

## 1. Extend the source potential, not the entire irreversible program

Use M clock qubits c and mode bit b, decoded x_i=c_i XOR b, rank R=sum_i x_i. Legal strings are 1^R0^(M-R). Define the computational/return phase label solely by (b,R), including the precise source correction in FLAG_FREE_SOURCE_ADMISSION.md section 6. Define the Pauli prefix, armed mask, own-clock Poisson t, readiness coefficient, and every pair Poisson h on ALL clock strings through this decoded label.

The completed Pauli prefix remains S_p during readout/return/idle and changes to I at actual preparation. The phase table must distinguish the before/after-preparation stages correctly. No inverse of a reset/readout channel is used. Only controlled-Pauli prefixes dress the true checks.

Let V_src be the entire positive source potential: sum_p[t_p e_p+T_cycle r_p] plus the shifted positive centered-pair occupation potentials. It is diagonal in all clock computational bases, though its data/probe terms need not commute.

## 2. Sorting preserves the ENTIRE source potential

Let I_p=sum_(i<j)(1-x_i)x_j. Adjacent 01->10 sorting preserves (b,R), hence preserves every source coefficient, prefix, readiness mask and pair Poisson argument. It acts trivially on probes/data. Therefore
 L_sort^* V_src=0
exactly on arbitrary quantum states, including clock coherences. This conclusion does not require that the reset/mark/readout program is unitary; it follows from rank preservation of the actual clock-diagonal observable.

Each sorting jump reduces I_p by 1; if I_p>0 there is at least one adjacent inversion. At rate nu per adjacent pair,
 L_sort^* [A sum_p I_p] = -nu A sum_p N_01,p,
 N_01,p >=1_[I_p>0].

## 3. Charge invalid physical phase moves locally

The real hardware uses local wall predicates and local mode flips, with each phase operation a TP data/probe/cache channel. On a legal clock these realize the specified independent cycle. On an invalid clock they may perform a wrong gate, premature reset/readout, or wrong mode flip. These are NOT declared correct operations.

For a rigorous comparison, define a mathematical reference phase generator that acts on the decoded (b,R) label as the ideal finite cycle, applies the proper TP phase map, and places an invalid clock in a canonical string of the next phase. One may project individual clock configurations for this proof-only map. It is not a proposed physical high-arity primitive. On valid clock strings it agrees with the physical phase generator when applied to V_src.

The reference generator obeys the already-derived source bound on all decoded labels. The difference between reference and physical phase contributions is supported on 1_[I_p>0]. Include BOTH extra/wrong physical moves and missing reference moves. A conservative bound is
 (L_phases^*-L_reference^*) V_src <= sum_p C_p 1_[I_p>0],
where C_p is finite and depends on the sum of actual rates of local phase channels (<=O(M kappa)) times the sum of norms of source-potential terms affected by that gadget. Those terms occupy a fixed neighborhood because checks/degree/clock size are bounded. Their coefficients include T_cycle and 2 kappa T_cycle span(h), so C_p is large, roughly inverse in the slow-start rate, but independent of total memory size.

Why this is an operator bound: each clock flip/mode flip is an injective partial permutation, and sums of data Kraus operators obey sum K†K=I. The potential is clock-diagonal. Source/target blocks can therefore be compared using the norm of their bounded local difference, sectorwise; arbitrary clock coherences do not introduce off-diagonal terms. For the reference's possibly noninjective canonicalization, separate Kraus operators for each source configuration make the same statement true. No operator monotonicity of exponentials is used here.

An invalid physical wall move changes I_p by at most M-1; an invalid mode flip changes it by at most M(M-1)/2. With at most M+2 physical channels of rate <=kappa, the positive clock-penalty gain is bounded by
 A (M+2) kappa [M(M-1)/2] 1_[I_p>0].
Legal forward/return/mode steps preserve I=0.

## 4. Actual global mean source Foster bound

Choose any A>0 and then finite nu such that
 nu A > max_p C_p + A(M+2)kappa M(M-1)/2 + delta
for some delta>0. Combining physical phase moves, sorting, and the exact reference source cancellation gives, on ALL physical clock/probe/data states,
 L_ideal^* [V_src+A sum_p I_p]
 <= -sum_p e_p -delta sum_p 1_[I_p>0]
    + N epsilon(1+D_eff r/kappa)
    + (# ordered neighbor pairs) 2 D_eff²(r/kappa)/(1+D_eff r/kappa).
Here D_eff=2M+1 for the supplied physical clock; heterogeneous rates use the actual finite coefficients. This pays illegal episodes by a negative repair drift, not a permanent extensive illegal-operation floor. The only ideal extensive floors shown are finite preparation purity and admitted dilute-overlap readout corruption.

## 5. Admission and protected-barrier boundary

Physical clock, detector, probe, cache and coupling noise remain perturbations. Clock noise can create inversion debt or jump between legal phases; the latter may skip a gate while leaving I=0, and is still charged as an actual perturbation acting on V_src, NOT claimed to be detected by sorting. Since each perturbation affects finitely many terms, its local price is finite, but scales with T_cycle, pair h, A and the helper count.

If helper error rates grow with engineered sorting strength nu, that dependence must enter the noise budget. It is invalid to make nu arbitrarily large while silently keeping an error-per-sort resource free. A nonempty rate/error window requires the complete noisy-device constants to satisfy the eventual domination inequality.

The source mean inequality is not by itself a protected-memory barrier theorem. V_src and inversion penalties add positive local apparatus costs with potentially large coefficients; the root must show the combined data/controller potential still has the required logical barrier, bound initial apparatus charge, and perform the local noncommuting exponential lift with the actual expanded supports. No conclusion about exponential lifetime is made here without those joins.
