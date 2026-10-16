# Independent CP measurement-fault coins: a bounded detector-fault escape route

Date: 2026-10-15. Verdict: **the proposed parent product bound is valid under the explicit independent CP-coin and reservation hypotheses below.** The construction is a standard stochastic mixture/conditioning argument, not a novelty claim. It is substantially stronger as an assumption than small measurement infidelity or small diamond error.

## 1. Actual model and scope
For every prescribed measurement slot j in parent i, the actual operation is selected by a fresh classical Bernoulli coin F_j with probability epsilon_j. Coins are mutually independent across all slots and parents, and independent of the input, memory/bath state, random seeds and perturbation interpolations. On F_j=0 the operation is the exact bath-independent unread stabilizer pinching D_(G_i); on F_j=1 it is an arbitrary specified CPTP operation on that parent's full declared reservation D_i and the persistent shared bath.

A CPTP faulty operation may be arbitrarily damaging on its reservation and may change the bath. It is linear and trace preserving, not a state-dependent choice of epsilon or a normalized postselected map. The evolution has a common realization with fixed, exogenous slots and reservations. Each conditional fault-pattern evolution has a fixed dilation independent of the weak-Hamiltonian interpolation variables. Finite-dimensional CPTP maps admit such dilations; fresh auxiliary environments can be included with the persistent bath.

For a geometrically clean parent:
- all active parent reservations are disjoint on **full data/check/ancilla resources**, although they may share bath degrees of freedom;
- weak perturbations of this parent are confined to the original certified footprint A_i, with cell actions a_(i,l);
- a deleted weak cell has no remaining operation that changes its measured stabilizer sector;
- initial-sector acquisition, all ideal boundary operations, comparison truth tables and intended correction obey the earlier exact-measurement theorem;
- completed ideal outcome records, or their retained dilation equivalents, are not later corrupted by another parent's faulty map.

“Unread” means the exact physical channel really is D_G. It can be refined as the genuine projective instrument sum_s P_s rho P_s, retaining fresh outcome registers in a dilation and tracing them out at the end. No controller must read them. The theorem is a CP refinement of the stated channel, not permission to insert fictional measurements into a different evolution. The latent fault coins are also part of this actual assumed realization.

Disjoint data qubits alone are not enough if a faulty slot can touch another active parent's check data, extraction ancilla, control registers, or protected completed evidence. If such interactions occur, the affected parents must be placed in the original external-dirty/intersection envelope. The product bound below concerns the otherwise-clean parents; their geometric dirtiness still needs its own scheduled-memory accounting.

## 2. Parent event and theorem
Let

  f_i = 1−product_(j in slots(i)) (1−epsilon_j),
  p_i = min{1, sum_l a_(i,l)^2}.

A parent is bad if it has any faulty measurement slot, OR if all its slots are ideal and at least one consecutive actual boundary syndrome changes during its weak cells. Include the initial-sector slot in slots(i) when it is acquired by the same possibly faulty mechanism.

For every selected set R of otherwise-clean parents, the actual joint bad-effect operator on the entire allowed input space satisfies

  F_R ≤ product_(i in R) [f_i+(1−f_i)p_i] I.                (1)

No input bath state, bath reset, commuting bath dynamics, independent physical noise, small completion-order conditional probability, or private frame assumption is required. The factors automatically lie in [0,1].

## 3. Proof by fault-pattern conditioning
Condition on the complete finite coin pattern omega, including unselected parents' slots. Because the selectors are state independent, its scalar probability w_omega is fixed and the conditional map is CPTP on every input. Its environment and measurement operations may depend on omega, but not on the weak interpolation parameters.

Let R_0(omega)⊆R be the selected parents with no faulty slot. The other selected parents are automatically bad, so their constraints are dropped. For every parent in R_0, deleting one of its weak cell interactions leaves that cell's entering stabilizer sector unchanged until its ideal next measurement. Arbitrary faulty operations on other disjoint reservations can modify the shared bath but cannot change this sector or its protected record. Their fixed dilations are simply intervening operations in the deletion-null proof. Shared boundary outcomes within this parent still compare their own consecutive actual labels.

The exact-measurement cell theorem therefore holds **uniformly in omega** for the retained parents. Its cell-subset bound and commuting parent union give

  F_(R|omega) ≤ product_(i in R_0(omega)) p_i I.             (2)

The uniformity is essential: a marginal calibration of a fault-free parent would not suffice. Summing the actual CP effects with their state-independent weights yields

  F_R ≤ [sum_omega w_omega product_(i in R_0(omega)) p_i] I.

The “parent has no faulty slot” indicators are independent across parents, since the slots belong to fixed separate parents and their coins are independent. Unselected pattern probabilities sum to one. Thus the scalar sum is precisely the product in (1). Fault maps and bath trajectories themselves need not factorize.

For a parent with M+1 equal-error slots, the exact factor is

  r(M)=1−(1−epsilon)^(M+1)(1−p_i).

The conservative r(M)≤p_i+(M+1)epsilon follows from the ordinary union bound. It is now justified by the explicit mixed CP model, not inferred from measurement fidelity. The earlier exact integer cost optimizer applies to that additive upper objective with d=B kappa t_meas+C epsilon; optimizing the sharper r(M) requires its own discrete calculation.

## 4. Support certificate and the footprint-closure obstruction
A parent with all ideal slots and no latent weak-cell changes can still use the original A_i-only condition

  Pauli(A_i) ∩ Centralizer(G_i) ⊆ phase × S_code.

There is no need to demand this condition for every Pauli on D_i, because arbitrary D_i measurement faults are explicitly marked as bad. Ideal projectors on the larger measured support are the specified allowed operations. Thus the model avoids the full-footprint fixed-state-factor obstruction rather than disproving it.

Every faulty parent must instead be charged over its **entire D_i reservation and causal control footprint**, including check data, ancillas, record/control effects, possible skipped or misdirected operations, and tails allowed by the underlying support theorem. Arbitrary local CPTP Kraus operators admit a memory-Pauli expansion on that enlarged footprint with chronological auxiliary coefficients. This alone does not license moving bath channels or ignoring later feedforward propagation outside D_i; the full bad-envelope and completion argument must still cover those effects.

Consequently all scheduled geometry constants, reservation durations, support radii, conflicts and dirty-parent bounds must be recomputed or uniformly bounded using D_i, not the original smaller A_i. If enlarged detector reservations intersect, those interactions cannot remain silently “clean.” Unfinished parents remain pending. Equation (1) is a quantum input to the previous support/common-decoder and subset-to-contour framework, not a replacement for its geometric and logical obligations.

## 5. Decisive limitation: small coherent error can have zero exact ideal weight
Consider the qubit pinching

  D_Z(rho)=P_0 rho P_0+P_1 rho P_1,

and the arbitrarily close channel

  E_theta=Ad_(U_theta) composed with D_Z,
  U_theta=exp(−i theta X),  0<|theta|<pi/2.

Suppose E_theta contained a positive exact D_Z CP-subchannel: E_theta−w D_Z completely positive for some w>0. A decomposition E_theta=w D_Z+(1−w)F with F CPTP would require this property.

Use the unnormalized Choi convention J(E)=sum_k |K_k>><<K_k|. The ideal Choi support is span{|0>_out|0>_in, |1>_out|1>_in}. The actual support is span{U_theta|0>_out|0>_in, U_theta|1>_out|1>_in}. For nonzero theta in the stated interval, the former is not contained in the latter.

More explicitly, with c=cos(theta), s=sin(theta), take the normalized vector

  |v> = (−i s |0>+c |1>)_out tensor |0>_in.

It lies in the kernel of J(E_theta), while <v|J(D_Z)|v>=s². Hence

  <v|[J(E_theta)−w J(D_Z)]|v> = −w sin²(theta) < 0

for **every** w>0. The only exact ideal-mixture weight is zero, i.e. epsilon=1 in this particular exact-ideal-plus-fault model.

Nevertheless

  ||E_theta−D_Z||_diamond
    ≤ ||Ad_(U_theta)−Id||_diamond
    ≤ 2||U_theta−I|| ≤ 4|sin(theta/2)| → 0.

Thus arbitrarily small coherent implementation error, even in worst-case channel distance, does not imply any positive exact D_Z CP mixture component. Average infidelity is weaker still. The obstruction is Choi support, not the size of the error. One can sometimes change the designated ideal channel, add deliberate mixing, or prove a different fault-path certificate, but none is the fixed D_Z mixture assumed here.

The same support warning applies to nearby rotated-axis pinching: its Choi support is span{|I>>,|n·sigma>>}, which does not contain span{|I>>,|Z>> when n is not parallel to z. This is another close channel without the required positive exact D_Z component.

## 6. Independent finite-dimensional check
Own script check_cp_coin_bridge.py uses two data parities Z_A,Z_C and one shared bath qubit, hence full input dimension eight. Weak time is one, with M_A=2 and M_C=3 staggered cells. Noncommuting couplings are 0.4 X_A X_B and 0.5 X_C Z_B, plus nontrivial syndrome-preserving bath dynamics. The seven actual measurement slots use independent illustrative probabilities 0.02 on A's three slots and 0.03 on C's four slots. Fault branches are nontrivial local data–bath unitaries replacing the measurement, so need not acquire a syndrome at all. These numbers are algebra-test inputs, not device estimates.

Complete Kraus enumeration gives 3^7=2,187 branches over 128 coin patterns. Full instrument normalization error is 6.78e−16. All 25 applicable conditional clean-parent subset checks pass. All three unconditional parent effects obey (1):

- A: maximum effect 0.1296892431 ≤ 0.1341033600.
- C: maximum effect 0.1852630143 ≤ 0.1884815908.
- Both: maximum effect 0.0217305767 ≤ 0.0252760146.

These are full-input operator eigenvalue checks, not selected-state probabilities. Separate Choi kernel witnesses for theta=0.1,0.01,0.001 agree with −w sin²(theta) at w=1/2. The analytic argument covers every w>0; finite numerical tests are not its proof. Results are saved in cp_coin_bridge_check_results.json. Computation uses complete finite-dimensional matrix/Kraus calculations in floating point, no experimental data, no fitting, and no author code.

## Conclusion
Independent, state-independent CP selectors plus full-reservation cleanliness supply the requested exact mixed-parent product bound and a concrete way to charge arbitrary detector faults separately. The model's principal burden is physical qualification of the selectors/exact branch and enlarged geometry. Generic small measurement error does not meet that burden. No novelty or hardware-readiness claim is made.

## 7. Same-proof extension to correction/controller/core slots
The slot set may also include the original correction-controller/core and initial acquisition, provided each has the same stipulated independent, state-independent CP selector. Its ideal branch must implement the exact intended source correction/controller operation; its faulty branch is an arbitrary CPTP operation confined to the declared full parent reservation and bath. All fixed timing, slot counts, padding and geometry remain exogenous, including on faulty branches. Faults cannot corrupt another parent's protected records or seeds, or trigger uncharged operations outside the declared causal footprint.

Define a parent faulty when any selected core/controller/acquisition/measurement slot is faulty. A parent with all slots ideal is precisely the original exact-core measured-cell model, so the same conditional deletion-null bound applies. A parent with any core fault is automatically bad and charged on the whole D_i envelope; no reliable syndrome comparison or intended-core behavior is claimed for that branch. Therefore (1) remains unchanged after extending product_(j in slots(i))(1−epsilon_j) to all these slots. A trusted acquisition paid elsewhere must either remain exact under its own assumptions or be included among the qualified slots; it cannot disappear from the fault accounting.

This removes an unconditional exact-core requirement **only within this specific qualified stochastic CP-mixture model**. The exact ideal component is still part of each slot assumption. It does not qualify generic coherent controller/correction errors, state-dependent error rates, outcome-dependent scheduling, or arbitrary small diamond/infidelity errors. The Choi-support obstruction above continues to apply to attempts to infer the requisite decomposition from small coherent error.
