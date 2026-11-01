# Root join: self-stabilizing source allocation without accuracy dilution

2026-11-01. Draft for independent whole-theorem review. This supersedes the dilute-start source for the proposed architecture, while preserving its received proof as reusable capital. It does not assert laboratory performance or historical novelty for mutual exclusion/CSMA.

## 1. Why the mechanism changed

The exact two-probe comparator won. On identical augmented source hardware including a physical token and DONE/handoff stage, token flips at rate .001g give retained cache error .000659917 and per-check flux .0668601g. Random starts at .1g give .0639995 and .0603015g; at .01g they give .00998576 and .00938853g. With preparation impurity .001, the token error is .00165860. These are finite-device calculations under the specified noise model, not a complete logical channel or network threshold.

The right continuation is the physical allocator, not polishing the losing collision-dilution design. The network mechanism was independently originated as abort-on-contention locks, then reconciled with the proved resonant source completion and positive-corrector consumer.

## 2. Actual finite-dimensional network

Use a conflict edge for every pair of checks whose simultaneous partial operations can spoil a report. Maximum degree D and check weight w remain fixed. Each edge has one physical qutrit (free, owner-left, owner-right). Each check has one fused apparatus of dimension 8w+4D+10, explicitly enumerated in FUSED_GRAPH_PROTOCOL_REFRESH_THEOREM.md.

Its classical phases release only their own locks in a full sweep, wait for an actual local attempt event, then collect incident locks one at a time. A busy lock causes immediate abort and cleanup, never waiting while holding resources. After all locks are collected, the apparatus prepares and runs its resonant quantum probe. No lock event pauses or resets a partial probe. Completed readout writes the cache and enters full cleanup. Collection/release jumps are two-apparatus classical GKSL primitives; quantum gate Hamiltonians remain apparatus-data two-body; native phase baths remain onsite.

All apparatus levels and lock states are physical. No perfect ownership metadata, scheduler, global token, or common runtime clock is supplied. Initial arbitrary control phases can cause an unvalidated first job. The allocator must—and does, under its cited proof—repair that situation rather than assume it absent. The fused representation prevents a cleanup controller from coexisting with a partial native probe as separate inconsistent registers.

## 3. Actual all-state source service

The quantum source supplies a uniform conditional active-cycle exponential moment M_A(theta), from its bounded-incident-commutator stage theorem. Busy collection aborts and cleanup always advances, so reaching a full CLEAN_0 scan and completing it has moment

 M_R(theta) <= [g/(g-theta)]^[3(D+1)]
                 [nu g/(nu g-theta)] M_A(theta).

Once a vertex has completed that full scan, all its new launches have genuinely acquired every incident edge. Neighbors cannot steal those locks: they acquire only free/their own values and release only their own values. This local invariant is preserved even while distant vertices remain malformed. A global n-vertex cleanup event is unnecessary.

Cache correctness requires more than control stabilization. An already-contaminated active job may still finish later. For a target and its D neighbors, the cited burn bound is

 S_burn(B)<=min{1,(D+1)S_R(B/2)+S_A(B/2)}.

After this burn succeeds, current/future target jobs are fresh isolated cycles. A fixed-length quiet-neighborhood service word has positive conditional success q at fixed attempt rate nu g, so at T=B+k Delta_word,

 exp(T L_src^*) e_s <=[S_burn(B)+(1-q)^k+p nu g(T-B)] I.

The last term prices actual bad preparation marks on post-B attempts. Earlier pending cycles must finish before the fresh post-B cycle and are overwritten. There is no assumption that a good report can never be followed by an incorrect one.

Separately, for the positive imminent-wrong-report observable

 d_s=F_s (I-X_probe,s Sbar_s)/2,

where F_s projects onto the final readout phase,

 exp(t L_src^*) d_s <=[S_burn(t)+p g tau_A] I,
 tau_A=integral S_A.

This follows from conditional active-survival integration of bad preparation births, not a stationary sampling or last-report independence assumption. It is the key readiness contract needed for the high-rate controller coupling.

All these are operator inequalities for arbitrary initial coherent states. Classical control/lock blocks can be analytically dephased because their observable algebra is invariant; within-stage quantum coherence is retained. Physical coherent perturbations are admitted later through their generator action, not converted to fictitious independent stochastic fault sets.

## 4. A fixed degree-aware attempt rate

The constructor's general q formula allows a useful rate choice that is independent of accuracy. Let m=D+1. Choose theta0 below g and the native moment radius, independently of nu. Define drain/fresh moments M_Q(theta0), M_F(theta0) as in the source proof. Choose

 F>=max{log(2m M_Q(theta0))/theta0,
        log(2 M_F(theta0))/theta0}.

Set the attempt window h=F, attempt rate nu g=1/(6mF), and word length Delta_word=3F. Then

 q>=exp(-1/2)/(24m),
 q/Delta_word>=exp(-1/2)/(72mF).

Regeneration uses theta_R=min(theta0,nu g/2), separately. This avoids circular selection of a moment exponent below an as-yet unchosen attempt rate. This design may be slower than the empirically useful nu=1, but its certified service cost is not exponential in degree solely because every neighbor was forbidden to start for a whole own mean waiting time. Native M_A and F still carry their actual costs. Nu depends on fixed graph/hardware parameters, not on target error or preparation impurity. No claim of arbitrarily small error at fixed p is made.

This corollary has been checked in Section 8 of the revised allocator source proof (SHA256 cd7285cf05b92a6b41d5e408c9c254cc9b8d7526b68d2b46e5e780975105825d). The general positive-q theorem does not depend on choosing this rate.

## 5. Positive local correctors and exact good-write cancellation

Apply the received finite-patch compiler to the actual allocator/source generator and observables e_s,d_s. It gives positive local H_e,s,H_d,s with

 L_src^* H_e,s<=-e_s+q_e I, 0<=H_e,s<=T_e I,
 L_src^* H_d,s<=-d_s+q_d I, 0<=H_d,s<=T_d I.

The floors include the actual source bounds, finite-patch boundary/evolution error and any numerical certificate residual. The radius is finite and independent of memory size. Every source/controller term preserves the dressed protected labels; cache-diagonal observables remain cache-diagonal. The correctors are therefore identity on witness/flag/Boolean wires and commute all cache input Z observables.

Paying EVERY cache write as an error would destroy the high-rate margin. Instead use the exact local identity at final readout. All of F_s,e_s,d_s commute. Define

 G_s=F_s e_s-e_s d_s  (wrong cache becomes correct),
 B_s^flip=(I-e_s)d_s (correct cache becomes wrong),
 chi_s=G_s+B_s^flip (the cache actually flips).

Then

 L_src^* e_s=gamma(B_s^flip-G_s),
 L_src^*(epsilon E_B)<=epsilon sum_s B_s gamma chi_s,

where B_s is the fixed Boolean-consistency sensitivity to cache s, not B_s^flip. Hence the positive local addition epsilon sum_s B_s e_s cancels the good-write cost:

 L_src^*[epsilon E_B+epsilon sum_s B_s e_s]
     <=2epsilon sum_s B_s gamma d_s.

No correct report is charged as permanent noise. Add 2epsilon B_s gamma H_d,s to pay the remaining wrong-report readiness. This cancellation is an exact Heisenberg operator statement, not a classical trajectory approximation.

## 6. Whole-controller mean drift and strict barrier margin

Keep the received virtual flag-mask actuator and noisy Boolean verifier. With actuator rate a, reference source rate g0, choose

 epsilon=a/g0, epsilon B_act<=1/2,
 alpha_s=a[(1+D_W)R_s+1],
 gamma_i>=g0[((1+D_W)R_i+w_i)/delta_i].

Define

 V=W+epsilon E_B+
       sum_s[alpha_s H_e,s+epsilon B_s e_s
                       +2epsilon B_s gamma H_d,s].

All ideal Boolean input reads/dephasing and flag actuation annihilate the source correctors and e_s. The source preserves W termwise. Combining the exact cancellation with the received verifier inequalities gives

 L_ideal^* V<=-(a c0/2)W-aE_B-a sum_s e_s+b_src n I.

For sensor density C_s, alpha_s<=C_alpha a, B_s<=B and gamma/g0<=C_gamma,

 b_src/a<=C_s[C_alpha q_e+2B C_gamma q_d],
 0<=V-W<=a K n I,
 K=C_E/g0+C_s C_alpha T_e+C_s B/g0+2C_s B C_gamma T_d.

Choose q_e,q_d<=beta c0/[64 C_s(C_alpha+2B C_gamma)], then aK<=beta/32 and a/g0<=1/(4B_act). After all rates, dimensions, lock terms and finite-patch constants are fixed, impose actual continuing-noise admission

 L_noise^* V<=u_V n I, u_V/a<=beta c0/64.

With c=a c0/2 this yields

 L*V<=-cV+[b_src+u_V+caK]n I,
 [b_src+u_V]/c+aK<=3beta/32.

Thus the same exact noncommuting exponential lift and killed-channel comparison from the received resonant join apply, after evaluating constants for the actual enlarged source. The old-frame admitted Pauli alphabet includes all actual H,J,J-dagger-J components after finite-depth dressing. Lock qutrits are free gauge apparatus; every source corrector preserves the full component labels. The required cut factorization includes FULL J-dagger-J, not just internal jumps.

For sufficiently small fixed exponent k and sufficiently large admitted n, the resulting output estimate has the same form

 2sqrt(3)n(2h_all+3Gamma_all)T_storage
           exp(k b_W)exp(-k beta n/4).

Ideal encoded input and ideal terminal decoding remain explicit. Arbitrary physical controller errors are not assumed absent: their actual norm densities and effects on the chosen local potential must lie in the post-selection admission region. This gives a positive formal region, not an engineering threshold estimate.

## 7. Consequence gate and comparison

This mechanism removes an intrinsic accuracy-versus-start-rate compromise from the quantum source, rather than only sharpening a constant. The token benchmark demonstrates that the alternative can beat the previous source on both reporting quality and speed in the same finite hardware model. The graph theorem, if received, supplies the missing noisy-control composition route.

It still does not establish practical large-code protection, physical realization of every multilevel/pairwise reservoir, cheap Tanner/Boolean constants, local 3D wiring, or a superiority claim over the strongest timed controller given the same apparatus and faults. Classical mutual exclusion is established machinery; the contribution being tested is its actual self-stabilizing quantum-service and protected-memory interface. A finite-cell numerical win is not a civilisation-level breakthrough.

The next consequential comparison must target useful physical scale and geometry. Further microscopic or proof-cost optimization alone should not become a substitute for that capability.
