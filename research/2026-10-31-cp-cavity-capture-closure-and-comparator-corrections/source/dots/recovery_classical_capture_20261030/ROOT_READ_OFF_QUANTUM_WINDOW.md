# Fixed read-off seed window: a bath-volume-free support bound
30 October 2026. Root construction candidate. This supplies a finite-window safe-support route; independent review pending. It is not a whole capture/factory theorem.

## Problem and setting
During the declared fixed-duration seed/reset window of duration tau, turn off the intended quantum read/correction operations. The quantum protected subsystem S includes DATA and any native apparatus whose errors will matter on re-enabling the receiver; its size is N_S=O(N). All capture targets, raw records and other systems belong to B, which may be very large and initially entangled with S. A historical classical m may label the construction, but is not a physical control resource.

The actual joint time-dependent generator L(t) is CPTP. Its decomposition is

 L(t)=I_S tensor L_B,raw(t)+sum_(e touching S) N_e(t),

where individual centered HP N_e need not be CP generators. Each N_e acts on at most q sites of S (and its permitted bath/record legs), ||N_e||_diamond<=eta_e, and sum_e eta_e<=eta N_S. The nominal read-off dynamics acts only on B. Known onsite S unitaries can instead be removed in their onsite interaction picture. No uncounted S-entangling nominal operation may remain. The raw B generator is NOT assumed CPTP: merely deleting noise terms is not legitimate.

## A legitimate reference bath generator
Define the completely mixed embedding E(rho_B)=I_S/d_S tensor rho_B and R=Tr_S. Set

 Lbar_B(t)=R L(t) E.

This is a CPTP generator on B. One elementary verification is that R exp(h L(t)) E is CPTP and equals I+h Lbar_B(t)+O(h²); its repeated short-step limit exp(t Lbar_B(t)) is therefore CPTP. For time-dependent finite-dimensional bounded generators the same pointwise argument and ordered product limit give the CPTP propagator. Infinite reservoirs require the corresponding existence/limit assumptions; this note does not supply unbounded-generator domain theory.

Because R(I tensor L_B,raw)E=L_B,raw, the exact remainder is

 L-I tensor Lbar_B=sum_e Delta_e,
 Delta_e=N_e-I tensor (R N_e E).

Every Delta_e is centered HP, has diamond norm<=2eta_e, and its S support lies in the same at-most-q system sites as N_e. Tracing the other maximally mixed system factors changes no bath-size constant. The subtracted term is identity on S. Thus the reference propagator is completely contractive although arbitrary deletion of the original N_e would not be.

## Dyson support and quantitative tail
Expand the actual propagator around I tensor Lbar_B. Between insertions the reference acts only on B with complete trace norm1. The total norm of all order-k insertion terms is at most

 A^k/k!,    A=2 eta N_S tau,

or A=2 integral sum_e eta_e(t) dt in the varying case. Every order-k term is a linear combination of left/right S operators supported on a union of at most qk sites. This follows from the finite local operator basis expansion of each Delta_e; no probability distribution of Pauli faults is asserted.

Suppose the initial positive state is supported on a code/module enlarged by errors on at most r0 system sites, with arbitrary retained bath. Let P_r be the common operator-error span enlarged to r sites. All terms with qk<=r-r0 have zero (I-P_r) compression. Consequently for K=floor((r-r0)/q)+1,

 Tr[(I-P_r) rho(tau)] <= sum_(k>=K) A^k/k!
 <= exp(A) (e A/K)^K,     K>=A.                         (1)

The first inequality uses positivity only of the ACTUAL final state. The low-order Dyson sum need not be positive and is not called a conditional channel. A gentle projection then produces a positive state supported in P_r, at trace-distance error at most2sqrt(tail), with normalization handled explicitly if desired. An arbitrary reference may be retained throughout because all bounds are complete.

With N_S=c_S N, r-r0=delta N, fixed tau and q, the right side is exp(-c N) for sufficiently small fixed eta tau. There is no factor exp(eta times number_of_bulk_record_sites times tau). The huge capture bath affects neither the insertion budget nor the system support count.

## What this earns and does not earn
This prices the fixed read-off waiting window using actual weak joint noise, without assuming its individual HP terms can be removed while preserving positivity. It can be combined with the separately derived quantum-weighted seed effect: one supplies a positive correctable-support cut, the other supplies the joint moment. They apply to the same actual state; conditioning the moment on the good cut needs its own commuting/support estimate or must retain the unnormalized positive cut and its moment bound.

The allowed radius r must be received by the actual native memory's true-code basin and ready/dirty apparatus contract on re-enabling. A support bound alone does not imply the exact native energy/BUSY parameter without that conversion. Any source warm support r0 is an actual hypothesis from the source's good cut, not a generic arbitrary input claim. This finite constant-duration lemma does not yield exponential waiting without active memory, ideal final decoding, or an autonomous schedule. Its reduced-generator argument is elementary channel calculus; no historical novelty is claimed.
