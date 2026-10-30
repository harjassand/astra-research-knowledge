# Carried launch faces remove the initial mixed-clock requirement

30 October 2026. New candidate; not yet independently reviewed. Preserve the reviewed raw compiler unchanged. This construction uses its exact trace, terminal, pooling, seed, activity and weak-reversibility hypotheses, but DROPS only `1+n <= C_init L_B`. No arbitrary-network conclusion is asserted.

## 1. The missing clock is real, but it belongs to a different row

At a=0,C=E=1,D=0,X=N in the hidden-clock rejection, the initial mixed wait has order-one operational mean. It cannot obey a population-decaying reset. Keep this obstruction. Do not insert this input into a uniform-reset row.

Instead use a carried launch row L at each connector boundary whenever D=0 (both mixed and true dormant states). Its hidden vector is frozen until a seed or restoring event. The restoring aggregate hazard is

    h(hidden) (A)_a0 (B)_q,

where h is constant on this launch path and is allowed to be arbitrarily small or large across metadata. Restoring changes the hidden vector, preserves A,N,B, and enters positive D. Seeds likewise enter positive D, retaining their actual products and phase.

A positive-D input starts a traced row R. Within this row, all mixed D=0 holds remain INTERNAL, exactly as in the accepted trace proof. Stop R only at a connector/clearing, or entry to true F. Thus no non-small all-D=0 ingress kernel is inverted. At a connector output choose the next launch/traced mode from its actual D; at a true-F output enter L immediately. The mode is a deterministic stopping-protocol flag, not a change to physical reaction rates. Initial-phase-left and rare-degree flags remain part of the state.

## 2. A uniform arbitrary-killing extension of the dormant Green

Let W_s=exp(theta r+lambda B)(1+A)^(-s), with the finite list of exponents and lambda already admissible in the accepted graded dormant construction. Let Y be the actual seed-free dormant connector path, stopped at its true seed or designated section/degree stop. Its accepted block proof also yields the stronger jump envelope

    J_s(y)=E_y[ W_s(Y_0) + sum_{connector jump times t<tau} W_s(Y_t)
                    + W_s(actual seed/terminal output) ] <= C_s W_s(y).  (1)

Here only connector jumps are counted; there are no unobserved restoring jumps in this reference path. This is a completion, not an inference from occupation alone. In the large-A regime, the number of clearing blocks is geometrically summable because of the fixed seed marking probability; births within a block have the same summable high-birth series, and each low approach contains at most q events. Each block therefore pays all of its jump rewards with the same profile cost. In the bounded-A/high-B regime, each leading step has at most three jumps, while every error ends a step with bounded weight multiplier; the accepted leading Green and small error perturbation pay their sum. In the fixed finite corner, jump reward is bounded by polynomial-intensity occupation with a polynomial-exponential envelope, whose finite-input values were earned independently using the enhanced complex-balanced connector. These are precisely the three regions of the accepted Green proof. Finite shell values, not an invalid rescaling, supply the corner constants. Initial low phases are included. Marked versions retain their actual counter: truncating the path never creates a rare mark or spends an unearned degree.

Now add an independent exponential mark with cumulative rate h(A)_a0(B)_q and stop at its first mark sigma. Couple until sigma to Y. Between connector jumps W_s is constant. Hence, PATHWISE,

    W_s(Y_sigma) 1_{sigma<tau} <= W_s(Y_0)+sum_{t<tau} W_s(Y_t).

The restoring output has exactly the same W_s, since A,N,B are unchanged. Therefore its actual exit kernel H_h obeys

    H_h W_s <= C_s W_s,

uniformly in h>=0, including h tending to infinity. Running cost, seed rewards, and section rewards before sigma are dominated by those of the reference path. This proves the enlarged launch Green and its TOTAL seed-plus-restore exit bound uniformly in the carried hidden metadata. It is incorrect to justify the exit estimate solely by occupation domination; (1) supplies the missing bound. Fixed polynomial residual weights and marked finite-degree versions follow by the same jump-envelope proof used for the accepted residual-power Green.

## 3. The genuinely small feedback is unchanged

The positive-D-start R proof never needed an initial mixed holding bound: every mixed interval there has an actual ingress, paid by the exact entrance compensator. All accepted R conclusions consequently remain valid from positive D: every finite profile/grade, polynomial time moments, uniform positive-power time/occupation and terminal-profile resets, and small true-F return

    R_F f_s <= C_s n^(-eta_s) f_s.

Only R_F enters the internal feedback equation. Let E_h be the combined seed/restoring launch exit into positive D; Section2 supplies its uniform profile bound. The internal loop is E_h R_F, NOT E_h times the all-D=0 hitting kernel. Its norm is small after the usual exterior cutoff for each finite requested list. The exact dormant launch Green is preconditioned first. This constructs fixed-b kernels and the actual unbounded-phase processor without any bound on h/n and without a small mixed-return assumption.

Connector outputs of R may themselves have D=0 and be mixed. They are actual phase outputs, not an omitted internal R_F event. Their inverse-profile rewards are included in the R terminal reset and first-connector compensator. The following launch row retains their actual phase, hidden state, residual and counter. A restoring mark spends degree zero, changes no connector algebra, and immediately supplies an R input. All pre-existing rare connector degrees are unchanged.

## 4. Complete section rows and signed forcing

At section B=q, partition bad inputs into L={D=0} and R={D>0}. Assign

    g_L=w f_m(A),       g_R=w(1+r)^(-eta).

The L row is deliberately NON-small even for arbitrarily large hidden mass. Its pure connector part is controlled by the enlarged Green. Its seed/restoring exits enter R; their bounded profile costs followed by R reset give the small cross product. Internal R-to-L true-F returns are small. Connector-mediated L outputs are paid by the phase processor, not silently classified as rare fast returns.

For the constructed complete cycle, the same first-connector identity gives

    E[(w_next-w)_+] <= C w T,
    E[w_next f_m(A_next)] <= C w T.

Indeed ordinary clearing spends f_m; activation at B=2q-1 still needs one additional inverse-power degree and A f_1(A+m-1)<=1; immigration costs iT. A restoring event is not a connector and is priced by Section2 plus the R kernel. For actual bad-R outputs, g_R <= epsilon0 w f_m with epsilon0=sup_{u>=r0} C log(2+u)^(2m)u^(-eta) tending to zero. Thus the old output-sensitive small-gain argument applies with this larger, carried L row; it does not assert a pointwise small reset on L.

Good L inputs have A>=K(r). Before the first connector A can only increase until a seed/restoring exit; seeds lose at most two, restoring loses none. Direct holding thus has T/U<=C/K; after exit the good-input R ratio and its same-episode return compensator apply. A finite negative activation/clearing word either stays in the launch path, losing only bounded A at each of its finitely many clearings, or enters R, whose clearing outputs reset. Extra restoring marks cannot create positive residual jumps. Qualification and low-race failures are bounded by the same finite-grade errors; the accepted word has probability >=cU after enlarging K's constant. Combining with the complete positive part gives Pw-w<=-c_theta wU+CwT. The enlarged bad correction is <=Cwf_m, with good leakage O(wT).

## 5. Complementary clock and endpoint of the proposed transfer

Actual activity has NOT changed: positive D, enabled restoration, or a>=2 inside the physical gate. Fast activity preservation is exactly the original raw terminal/pool check, independent of the new row labels. An active D=0 mixed state is not relabeled physically inactive.

In large-N complementary trials, a launch segment either follows the accepted dormant attempt or exits by a restoring mark to R. The mass removed from the old attempt by this extra mark is the mass handed to R; the uniform positive-D clearing/reset estimates give its ensuing prescribed continuation the same asymptotic success bound. One must not claim killing alone increases the old event probability. Conditioning on the actual mark time/output supplies the replacement continuation. On the finite N head an enabled restoring jump followed by the acquired finite path to 2a/clearing has positive probability and finite scaled time; finitely many head states give uniform constants. Thus the existing down/up trial estimates and physical-time two-direction patch have the same inputs with L handled as a launch row, not a uniform-reset row.

This proposes the same classwise recurrence/exponential-moment conclusion as the accepted compiler for inputs satisfying all its conditions EXCEPT initial mixed growth. The sole new probabilistic interface is the arbitrary-killing jump-envelope lemma and the carried launch/traced protocol. The full transfer remains subject to independent review; a local Green bound alone is not claimed to establish recurrence.

## 6. Constructive significance and limits

The raw finder may omit the initial-growth guard and output a MODE-DEPENDENT decomposition: D=0 is a launch boundary at connector starts, while enabled-restoration D=0 holds are internal to a positive-D trace. This is an algorithmically determined stopping protocol, not a set partition pretending every physical state has one role. The hidden-clock example now fits without changing a reaction. This is stronger than attaching one more named species: arbitrary carried hidden mass is allowed subject to all the same exact coefficient, pool and terminal checks.

This is an instance of standard stopped-time/Filonov reasoning using a richer stopping state; no historical novelty is asserted. Multi-step face dynamics, A-dependent restoring products, adverse pooled transfers and nonconservative/nonbinary residual networks remain outside this certificate. Exact trace compensation and the non-small raw-immigration obstruction are preserved. No physical operations or external actions are involved.
