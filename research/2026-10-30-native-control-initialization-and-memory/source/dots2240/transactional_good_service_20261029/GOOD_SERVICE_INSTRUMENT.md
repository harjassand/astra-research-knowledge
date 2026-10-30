# Genuinely fresh recovery opportunities: exact latched instrument and joint tails
2026-10-29. Uses the transactional forest gauge and the finite-rate reset-tail certificate in `producer-workspace/transactional_regeneration_20261029`. No SSF decoder-correctness theorem is asserted.

## Simpler lead certificate
`TWO_HALF_GOOD_SERVICE.md` proves the needed joint physical-window missed-service law directly from existing joint no-reset tails, without any latch or new Lyapunov witness. The present latch construction is an optional alternative, not a prerequisite.

## Useful result
A **second actual terminal-or-abort reset** of owner h in a noise-free interval certifies a genuinely fresh intended recovery terminal: the first reset regenerated h to a good Q_0 state; good history cannot be destroyed by clean evolution; a good abort has zero support; and the only route from Q_0 to another terminal passes through a new complete A_k→C_0 commit.

Therefore the full-state single-reset probability p in time T gives a full-instrument probability at least p² of one witnessed fresh recovery by 2T. A two-state local record latch converts this into an actual CP killed semigroup. The finite-support Lyapunov construction then gives exponentially small **joint missed-good-service** events for many separated candidate owners, not merely marginal reset probabilities.

## 1. Good service means the intended DATA channel, not just clock progress
After any complete h terminal/abort reset, h has phase Q_0 and workspace zero. This is good for every lock configuration, and the full-Hilbert no-creation theorem preserves that owner's good sector during clean evolution even if other owners and data are initially arbitrary.

A subsequent abort jump is identically zero on this good sector. Any subsequent terminal source is consistent, all-owned, and has clean history. Since Q_0 has no direct route to C, this terminal must be preceded by a new ready/acquisition/complete-commit sequence. In the forest-gauge frame its DATA instrument is exactly Phi_h (or its actual syndrome-resolved subinstrument), tensor a controller source/reset map, even for data/controller entanglement.

This does not say the incoming data are error-free or that Phi_h necessarily fixes an arbitrary corrupted codeword. It says an actual fresh instance of the intended local recovery channel occurred.

## 2. The two-reset latch is record postprocessing
Attach a mathematical classical latch q_h∈{0,1,success} to the existing reset record. Initialize q_h=0 at the candidate window's start. On each actual designated h reset (terminal OR abort), increment 0→1→success. Success is absorbing. No other clean event changes it.

This is not an additional physical clock monitor or a phase projection. It only computes a function of actual separately recorded reset events. With clean evolution, entry into success is precisely a witness of a fresh terminal after regeneration and a new commit. A first terminal might already be a good recovery; the latch deliberately demands the stronger two-reset certificate.

Let J_h be the sum of the actual designated reset gains, and A_h=J_h*(I), 0≤A_h≤nu I. On alive latch states {0,1}, define the killed generator Khat_h by:

* retain every ordinary physical Hamiltonian, jump, and complete loss;
* route each designated reset gain from q=0 into q=1;
* delete each designated reset gain from q=1, retaining its original loss.

Then exp(t Khat_h) is exactly the CP trace-nonincreasing instrument for fewer than two designated resets. It is not an evolution projected onto a history-defect subspace. Its adjoint obeys

   Khat_h*(I)=−|1><1|_q tensor A_h ≥−nu I.

Classical direct-sum latch states suffice. If a Hilbert-space dilation is preferred, use separate source-labeled jump operators; the observable bounds below are block diagonal and extend to arbitrary latch coherences.

## 3. Uniform contraction on the entire alive space
The existing full-alphabet certificate states that, from EVERY physical/reference state, at least one designated h reset occurs in time T with probability ≥p.

From latch0, request at least one reset in [0,T] and at least one in [T,2T]. By the complete-positive Markov composition and the uniform full-state bound, this event has probability ≥p². It is a subset of two resets by 2T; extra or early resets only help. From latch1, one reset by T suffices, with probability ≥p≥p². Thus on the entire alive augmented space,

   exp(2T Khat_h*) I ≤(1−p²)I.

No conditional state has been normalized to claim an event-independent channel. Equivalently, the joint success event is evaluated by composing its unnormalized CP instruments; each uniform operator bound supplies the factor p.

The artificially allowed initial latch1/dirty-physical states need not have genuine-good-service semantics, but the contraction still holds there. Actual candidate windows start latch0, and every physically reached latch1 state has the required good certificate. This distinction permits a full-space Lyapunov argument without asserting a false certificate for arbitrary latch1 input.

## 4. Local Lyapunov witness and simultaneous joint miss bound
Apply the anchored local-polynomial construction in `JOINT_LOCAL_LYAPUNOV_TAIL.md` to Khat_h, with

   T_g=2T, p_g=p²,
   a_g=(1−exp(−nu T_g))/nu,
   alpha_g=a_g/(3T_g), r_g=p_g/(3T_g).

The latch is a fixed-dimensional on-site register. The modified killed term remains local and anchored at h. All ordinary local adjoints annihilate I; only the h killed term is nonunital. Thus the same locality/Taylor/telescoping proof supplies a finite-support Hermitian witness Z_h with

   alpha_g I≤Z_h≤I,
   Khat_h* Z_h≤−r_g Z_h.

Its support radius R_g is finite, uniform in volume, and may be extremely large. Include the latch and all monitor/support buffers in the range budget.

For owner sets S separated enough that no local generator term touches two witness supports, augment with one independent record latch per owner and kill any entry into success. The exact product rule gives

   ||Nhat_S(t)||diamond
      ≤ min{1, alpha_g^(−|S|) exp(−r_g |S| t)}.

This is the norm of the actual joint instrument in which EVERY h∈S misses the witnessed fresh terminal by t. There is no independence assumption and no conditioning on remote future records. Arbitrary entangled initial states are allowed; initialize all latches to zero for the stated physical meaning.

For arbitrary finite S, bounded geometry supplies a buffered subset U of size at least |S|/P_g. When b(t)=alpha_g^(-1) exp(−r_g t)≤1, the miss-all-S event implies miss-all-U, hence

   ||Nhat_S(t)||diamond ≤ b(t)^(|S|/P_g).

For all t use min{1,[alpha_g^(-1) exp(−r_g t)]^(|S|/P_g)}. This gives a genuine all-finite-specified-sets missed-opportunity parameter

   q_miss(t)=min{1,[alpha_g^(-1) exp(−r_g t)]^(1/P_g)}.

It becomes small by choosing a sufficiently long fixed physical window, independently of total system size.

## 5. Deterministic physical-time slabs
For aligned nonoverlapping slabs of fixed length Delta, initialize analysis latches to zero at each slab's start. For any prescribed finite set of owner/slab candidates, apply the preceding simultaneous bound within each slab, then compose slabs chronologically. The bound is uniform over the conditional entering physical state and reference, so

   ||instrument(all prescribed candidates miss witnessed good service)||diamond
      ≤ q_miss(Delta)^(number of prescribed candidates).

This is a physical-time missed-service law, NOT a law indexed by successful update counts. A virtual latch reset at a slab boundary only forgets prior record counts; it does not reset any physical controller or data. Selected candidate slabs must have the stated deterministic, nonoverlapping convention; arbitrary overlapping time windows require an additional packing argument.

## 6. Safe Poisson-noise extension with a validity latch
If local CPTP Poisson kicks are included, redefine the alive latch to track validity: any kick whose support intersects B_h sets q_h back to zero. A designated reset changes 0→1; any designated reset from 1 is counted as success, exactly as in the clean killed generator. On the reachable q=1 sector h is genuinely good, so an abort there has zero support and every actual success is a terminal. Retaining this same algebraic transition rule on unreachable dirty/latch1 states keeps the robustness comparison well-defined. Success stays absorbing even if a later kick occurs. This is again classical postprocessing of actual kick/reset records, not feedback.

A kick may reset only boundedly many latches. Its extended map is CPTP; its generator perturbation has norm at most twice its Poisson rate. The augmented process has the same actual separately recorded reset channels. Thus the robustness argument of the local Lyapunov certificate applies: if the incident perturbation norm budget on each witness support is eta and every noise term touches at most b witness supports, then

   (Khat_S+Nhat)* Z_S
      ≤−[r_g−eta alpha_g^(−b)] |S| Z_S.

For eta alpha_g^(−b)<r_g, the same joint good-service tail holds with this reduced positive rate. The proof counts the validity-latch reset as part of the actual kick instrument. It does not silently assume kicks cannot dirty a previously regenerated episode.

For arbitrary initial latch1 states, the extended killed generator may accept a dirty terminal as success; this is irrelevant to semantics because the theorem's real initial latch is zero. The full-space drift is used solely as an upper bound, and the reachable valid-latch sector enforces true good terminals.

This robustness condition is conservative and can be extremely weak. It applies only when the designated reset channels are genuinely present as actual record channels; an unspecified signed generator perturbation does not automatically preserve this interface.

## Scope for finite-window SSF
The result supplies the missing **missed-valid-service** term for fixed physical windows: a reset alone is insufficient, but a regenerated fresh terminal is certified by the latched event. The forest-gauge DATA identity supplies the intended recovery map at that event. Marked prior DATA damage remains charged to faults and is not erased from bookkeeping by regeneration.

A full SSF/quantum-memory threshold still requires the appropriate decoder contraction/correctness statement under the resulting asynchronous intended-recovery sequence and bounded fault clusters. Neither an arbitrary recovery map nor arbitrarily pessimistic service constants establish that theorem by themselves.
