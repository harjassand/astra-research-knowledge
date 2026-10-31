# Independent review: energy flow received as expected adaptive work

## Scope

I read the complete root `EXPECTED_WORK_RECEIVING_CANDIDATE.md`, initially SHA-256 `b04c1dcf343be8395680f475797ed347945b5f3c3f0dd4d64227f0805caca27a`, and checked the energy estimates, physical counter interface, and deterministic-window accounting against the accepted native and energy-resolved receivers. This review presently binds that exact 8,909-byte source together with the explicit receiving qualifications below; source amendments have not yet been read or promoted.

Verdict: qualified mathematical PASS, requiring the stated receiving qualifications, as a resource-accounting corollary of an already acquired complete first-event algorithm, with the explicit cap, port normalization, and per-call acquisition conventions in this receipt. An expected Lindblad jump count alone is not an algorithm, and this result does not remove coherent virtual-word padding or provide a practical comparison.

## 1. The elementary all-rate estimate

For a purification of the joint source/system/reference state, the commutator expectation is twice the imaginary part of the inner product between sqrt(H)V acting on the purification and sqrt(H) acting on it. Thus its absolute value is at most 2C sqrt(E), with C a certified bound on ||sqrt(H)V||. This does not require the state to be pure on the visible registers. The Hamiltonian terms declared to commute with H contribute zero.

The dissipative hypothesis gives E'<=-lambda*kappa*E+2sqrt(lambda)*C*sqrt(E). Young's inequality yields the displayed -(lambda*kappa/2)E+2C^2/kappa. Integrating interval by interval, adding the paid positive control-energy changes, and discarding final nonnegative energy proves

E N(T)<=4(E0+D_ctrl)/kappa+8C^2*T/kappa^2.

The jump compensator is exactly 2lambda E for the specified jump stack. At lambda=0 its count vanishes. No high-rate assumption, normalized tilted-state Jensen inequality, or physical thermodynamic interpretation is involved. An expected-energy injection bound suffices for this first-moment argument. Uniform operator injection certificates are a stronger convenient way to acquire it. All d_j are taken nonnegative. System-only trace-preserving instruments, with their records retained, have zero source-energy injection; rare-outcome postselection does not inherit that statement for free.

The count bound itself does not require centering. The downstream high-rate coherent receiver still requires its separately acquired centered interaction/ports and all of its other hypotheses. The resource corollary does not delete those premises.

## 2. Energy-limited tilted activity

Under the accepted high-rate energy-form condition, the initial tilted moment is at most 1+4uE0/kappa. A control with C_j^dagger(H)<=H+d_j I gives C_j^dagger(W)<=W+(4u d_j/kappa)I<=(1+4u d_j/kappa)W. This operator inequality is valid with arbitrary references and permitted retained records. It is stronger than merely bounding an unconditional mean injection and is the appropriate premise for the MGF statement.

Multiplying these factors and using 1+x<=exp(x) proves the stated Lambda_E. The inequality holds near theta=0 with equality of both sides at zero, so right differentiation gives E N<=Lambda_E. The finite bounded-source setting has finite exponential count moments. Separately, absorbing the QQ contribution at sqrt(lambda)>=2a_E/kappa and applying Young to the cross term gives

E'<=-(lambda*kappa/4)E+4r_E^2/kappa,

hence the stated direct bound 8(E0+D_ctrl)/kappa+32r_E^2*T/kappa^2. It has a weaker rate threshold but different constants. Neither certificate uniformly dominates the global C estimate. Both E0 and control charges must be actually acquired for the claimed input/control class; arbitrary source inputs revert to the corresponding worst-case bound.

## 3. Fixing the cap and using only the integer counter

Choose the physical count guard first, with its failure probability at most epsilon/8. If the exact comparison process freezes completely at its Mth jump, that guard must cover N(T)>=M, not merely N(T)>M. An equivalent one-integer adjustment is harmless but must be explicit. The final counter is min(N,M), with expectation at most the certified Xi.

Fixing the window schedule then fixes S=M+W+2. Only afterward instantiate the entire counter-augmented numerical simulation with delta_sim=min(epsilon/4,1/[4(1+S)]). The physical MGF is not asserted for the approximate simulator, and the physical cap is not redefined using the tightened numerical error. The dependency is noncircular.

Tracing out everything but the bounded INTEGER counter gives TV distance at most delta_sim/2 under the trace-norm convention. For any two distributions on [0,M], the difference in their means is at most M times TV. Thus

E N_sim <= Xi + (M/2)delta_sim <= Xi+1/8.

There is no dependence on continuity of a timestamp, skip decision, or call-history count. Exact and discretized continuous time laws need not be TV close. The previously earned counter-augmented remaining-channel hybrid is the actual required operational interface.

All implementation errors that can affect the retained counter must be included in the tightened delta_sim comparison. This includes supplied encoding/primitive errors and approximate control errors if the energy certificate describes ideal rather than executed controls. An external error budget only of order epsilon can otherwise contribute order M*epsilon to expected counter bias. Alternatively, certify the energy and injection charges for the ACTUALLY executed external instruments and compare the simulator to those same instruments; their difference from a desired ideal task then belongs only to the separate accessible-output error. There is no exemption from the counter accuracy merely because a primitive was externally supplied.

The physical cap error contributes at most twice its probability to trace norm; the finite simulation and any remaining external target-control discrepancy receive their separate output budgets. These sum within the declared epsilon budget. Keeping the private counter for analysis and then discarding it does not change accessible behavior.

## 4. Actual adaptive calls, not a padded-circuit shortcut

Each completed simulated event adds at most one call, and deterministic no-event window completions contribute at most W. The fixed slack covers the initial/final conventions. Therefore executed calls are pointwise bounded by N_sim+W+2, and their expectation is at most Xi+W+3. Short-window skips can only lower this upper bound; their discontinuous histories are never compared between two processes.

The private event/time record may be measured only after a COMPLETE first-event instrument as permitted in the received construction. Source/system memory is retained. This allows measured adaptive execution, not a replacement of a coherent inner word by its expected number of virtual insertions. Every call still pays its padded virtual cap, amplification, and actual primitive precision.

For a resource vector, c_call must be a uniform actual upper bound over all admitted remaining windows, inputs, and active branches. In particular, per-call clock/angle recompilation when the private remaining window changes is included in c_call; only genuinely one-time source/operator acquisition is outside the expected-call multiplier. Multiplying this upper bound by Xi+W+3 is sound without assuming independence between call cost and jump count. The fixed-depth implementation continues to pay its S-call upper bound. These are different execution models and cannot be interchanged in a benchmark.

## 5. Expected H0 action with worst-window charging

B_off denotes the SQUARE of the actually acquired crossing-port normalization times T/g. In the accepted slack-port convention QKP/(2rho), it is 4rho^2*T/g, not rho^2*T/g. This factor matters for the scalar envelope condition.

With D=128B_off+Xi+p+4 and a dyadic tau in [1/(2D),1/D], that envelope condition holds. From W<=ceil(1/tau)+p+1,

(Xi+W+3)tau <= 1+(Xi+p+5)tau <= 9/4.

The last constant follows from D>=Xi+p+4 and D>=4; any fixed larger constant is also valid. No concentration or full-path time-sum argument is needed.

Every binary-duration H0 slot is charged its worst physical interval T*tau. Multiplying the per-call padded number d_A(Kcap+1) of such slots by the expected call bound proves the stated O(alpha_0*T*d_A*(Kcap+1)) action. Per-piece synthesis overhead is still paid, as are all source-kernel, clock, port, stack, and arithmetic costs. The new schedule requires recomputing the actual receiver caps/precision for its windows; it does not import a numerical table from the previous M-inclusive schedule. The count guard can remain conservative, and its effects on logarithmic precision/virtual caps remain real.

## 6. Consequence and limits

For the restricted classical task, a prepared pure stationary representative can have E0=0 while giving the correct diagonal-algebra controlled statistics. That replacement requires the established matching initial law/system state, permitted controls, and output interface; it is not valid for arbitrary correlated CQ inputs or arbitrary quantum-source experiments. Preparation costs remain.

This result earns an adaptive expected-call accounting improvement from a certified energy budget AFTER the full simulator has been constructed. The all-rate elementary estimate is not by itself an all-rate fast compiler. The sharper worst-window H0 action statement is a high-rate receiving corollary, with actual access and source conditioning still paid. It supplies neither physical mean-duration shortcuts nor a practical advantage over ordinary dense/effective-model methods on the existing fixtures.
