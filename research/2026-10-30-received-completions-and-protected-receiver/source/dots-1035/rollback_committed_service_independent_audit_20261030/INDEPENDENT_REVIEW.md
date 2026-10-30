# Independent review: rollback-aware committed credit and one weak Bob LOAD

2026-10-30. Reviewer: `producer-workspace/audit_topology_free_noise`. Final exact-source review.

## Finding and boundary

**SCOPED PASS** for (i) the clean, true-program, fully owned C-sector analytical credit with actual rollback exits and (ii) an actual one-SUCCESS instrument lower effect proportional to a single weak Bob LOAD rate when Alice LOAD and the other selected service rates stay fixed positive.

Neither assertion is a full-Hilbert guarded-credit composition, useful acquisition/FIFO drift, correct output from every dirty terminal, a scalar effective DATA generator, or a logical-memory theorem. Prior accepted stochastic, raw, debt and weighted-debt results are unchanged.

## Frozen sources

- `ACTUAL_ROLLBACK_COMMITTED_CREDIT.md`: `ba6773186f7007587d28c08b0ba35643a2d4bbfd1ce623f5c0c0e8d3defa9a05`.
- `BOB_ONLY_WEAK_LOAD_ACTUAL_SUCCESS_RATE.md`: `b8be8342586e869a1071f808bf05d453741f3cbf42056cc2e68de47648e7e0be`.
- Correctly relabeled author test: `8c2b82f95a24af61f8263488882b06468e358f52690bc6afce41425d3dd0a060`; receipt `767da6b2a1a22e56acdff41792bc2b943d5b30270e5783a2bbf55158ef490e49`.

The two governing manuscripts and all dependencies are inventoried in `SOURCE_MANIFEST.json` and `SOURCE_SHA256.txt`. Exact bytes, including the prior diagnostic labeling, are preserved under `reviewed_sources/`. The normalized weak-gain precision and final diagnostic diff were read before this receipt. No author or prior accepted source was edited.

## 1. Actual clean committed guard

The source guard is clock C, full ownership of the entire raw-read/write resource footprint, forest workspace W=0, and combined semantic/Alice-parent debt Q_h=0. On this guard P is a true current Alice value. All C labels have the same P-validity convention, and the mechanical and semantic conditions are independent of C clock position and its monitor timer. The finite C coefficient matrices therefore commute this guard, P, the raw potential restricted to C, and the virtual DATA channel.

The virtual clean GPT channel is controlled by the already retained P. It neither reads Alice again nor changes any controller register. Bob-only DATA action preserves the truth guard; mechanical flags are DATA-independent in the forest frame. Its Kraus completeness holds on the full DATA space for each program. Thus `d=V-Phi^*V` is positive and raw-syndrome/program diagonal on the guarded sector, by the actual strict ordinary GPT energy property. No idempotent replacement is made.

Inside full-ownership clean C the exact forest Hamiltonian is the scalar clock path. Needed raw-syndrome and program observables commute it. Resource labels cannot be released while C claims them. The actual hub reset-monitor timer must remain in the finite clock generator; independent monitors on fixed owned tags can be spectators. Other generator terms are not silently included in the own-hub drift calculation.

## 2. Both exits belong in the killed clock

SUCCESS at C_L and every prefix watchdog C_j to B_(j,j) leave the credited C family. Delete both gains, keeping both complete losses, to obtain the actual finite CP killed clock/monitor generator K_C. The watchdog is not an identity DATA attempt attributed to success; it is an exit to the inverse rail, on which this credit is identity.

A finite monitored path from every C clock/timer state to the terminal, with no watchdog before success, has a fixed positive effect. This is the existing finite-rate monitor argument, including arbitrary initial timer coherence, not a classical clock hypothesis. The complete exit tail is finite; in the actual machine the positive watchdog rate at every C label already supplies a uniform exit loss. Hence the positive integrals P_s and R exist, P_s has a strictly positive minimum eigenvalue p, and R has finite upper bound r_max and strictly positive lower bound.

Integrating the exact killed semigroup gives `K_C^*P_s=-Gamma_s` and `K_C^*R=-I`. Choose `0<beta<p/(2r_max)` and set `A=P_s-beta R`. Then `pI/2<=A<=P_s<=I` and

`K_C^*A=beta I-Gamma_s`.

No commutation of P_s with R, or of A with Gamma_s, is needed. Equal watchdog rates give the optional absorption identity `P_s+mu R=I`, but the construction does not depend on it.

## 3. Analytical CP map and exact own drift

Extend A by zero outside the clean committed guard. The Kraus family consisting of `sqrt(I-tA)` and `sqrt(t) K_j sqrt(A)` is exactly unital for `0<t<1/2`. The no-jump factor retains off-sector coherences; no pinching is inserted. Because A commutes V and the virtual channel coefficients on its source sector,

`T(V)=V-t A d<=V`.

Here d is understood with its clean-sector support; no positivity assertion is made for the same DATA channel on an arbitrary false-program source. The map is analytical and may depend coherently on the semantic guard; it is not an added physical interparty operation.

At actual SUCCESS, T is identity in the Q0 target and the raw gain is Phi^*V. At actual watchdog exit, T is identity in B and the raw DATA gain is V. W/P are retained at the watchdog, so it is a genuine clean rollback prefix; any discarded WANT is true under Q_h=0 and changes no false-token energy. The complete loss at either exit is exactly the one retained in K_C. Therefore

`L_h^*T(V)|_D=-Gamma_s d-t(K_C^*A)d`

`=-t beta d-(1-t)Gamma_s d`.

This calculation is valid even with noncommuting clock coefficients and Gamma_s, since d is a separate commuting DATA/program factor. No second application of Phi occurs at the physical terminal. At clean true-program COMMIT, source T is identity and target T has a negative credit, giving the additional nonpositive term with the positive C0 matrix block of A; if timers are retained, that block is an operator on the timer, not an assumed scalar.

Clean inverse B rail Hamiltonians and B0 erasure act on an observable with no credit there. Their presence cannot turn a rollback into success. Opening a semantic or mechanical guard on a dirty source is nevertheless a different full-Hilbert problem and is not controlled by this clean compression alone.

## 4. Non-idempotence comparison

For a true-program raw label, if the table chooses no move, the raw label is unchanged and both d and Phi^*d vanish there. Otherwise its integer energy decreases by at least one, so

`d(sigma)>= (1-e^{-s}) V(sigma)`.

At the next raw label the same true program is still true: Alice DATA and P have not changed. Monotonicity gives `0<=Phi^*d(sigma)<=V(sigma)`. Hence

`Phi^*d <= d/(1-e^{-s})`.

This argument uses the actual raw exponential, not a generic positive potential. Since the virtual channel preserves D and its coefficients commute A, the CP credit also obeys `T(Dd)<=C_s Dd`, with `C_s=(1-e^{-s})^{-1}`. It does not require `Phi^2=Phi`; the regression explicitly has `Phi^*d>d` on a label and is non-idempotent.

## 5. Exactly one weak actual Bob LOAD

The actual favorable word can first retire and clear Bob h and every owner blocking its full footprint without any LOAD. Park those neighbors by excluding future LOAD/I-watchdog records, retaining their losses. The Alice backlog/purge stage can contain several old native READ macros because REQUEST is persistent, but these have fixed positive Alice LOAD rates. Their footprints and finite queue capacities give a finite fixed word, with no recursive acquisition of neighboring lock sets. Then obtain a fresh measured response, hence WANT, take the single selected Bob-h LOAD, acquire/commit, and reach SUCCESS before rollback. No Bob-neighbor LOAD is selected.

The lower effect is uniform on arbitrary initial physical/monitor/queue/reference states, although earlier dirty actions can damage DATA. Actual complete reset outcomes and label-conditioned records cover those states; no syndrome outcome is assigned an assumed lower probability. The favorable event is a genuine subset of physical records.

The quantitative issue is the weak gain. An unscaled absolute monitor-approximation error cannot be compared with a success probability of order lambda. The corrected source explicitly factors the one selected gain as `lambda J_LOAD` **before** making the projected-monitor/Dyson comparison. All no-LOAD losses retain their lambda dependence. The resulting normalized coefficient kernel is not a substituted physical channel; it is the coefficient of an actual selected record. Its bounded local norms and its leading path effect are uniform for lambda in `[0,lambda_0]`. Every comparison error therefore acquires the same external lambda factor. Fixed monitor windows then give `c_0 lambda I` at fixed T_0. Without this normalization the claimed scaling would not have been earned by the old absolute-error constants.

## 6. Tail, fixed-count latch and analytic tilt

For the nominal physical process, SUCCESS channels remain actual separately recorded channels. Deleting only those gains gives a CP no-SUCCESS instrument. Iterating the full-state lower effect yields

`||N_s(t)|| <= (1-c_0 lambda)^floor(t/T_0)`.

After weakening c_0 if necessary, the exponential form has a prefactor uniform on the declared lambda interval and decay rate at least `c lambda`. This is a survival-tail rate, not an instantaneous hazard.

For a fixed count m, divide a window of length `C_m/lambda` into m long subwindows. Each has a uniformly positive conditional chance of at least one actual success; compose the full-state effect bounds, or use the passive classical success-count latch. This gives fixed positive m-success probability and the corresponding order-lambda killed tail. It does not multiply a fixed-window lambda^m path and mislabel it as a linear-rate result.

The same normalized-gain proof can be repeated in the conservative analytical tilt: the selected weak LOAD still contributes exactly one lambda, and the complete reset-effect comparison changes only fixed local constants. That analytical generator is not a physical record in the noisy process. In particular arbitrary signed continuous perturbations do not automatically preserve the actual SUCCESS instrument needed for this tail.

If Alice LOAD also tends to zero, the purge can require multiple weak Alice READ completions. No rate uniformity or linear Alice scaling is proved in that regime. Fixed weak positive rates may be used in a separate stochastic source theorem only after its actual constants are recomputed.

## 7. Independent diagnostics and remaining obligations

I reran the supplied committed fixture. Its original monitor was direct projector dephasing, not the actual reset timer, and its B exit was an absorbing identity-on-DATA label. The author has now explicitly relabeled it as an abstract resolvent/drift diagnostic, not a simulation of the full native monitor/rollback alphabet, and points to the independent supplemental test. Its non-idempotent payload difference is 0.82212 and its drift identity error is 6.32e-16.

To test the actual clock structure I independently built `check_actual_timer_and_b_rails.py`: three C positions, all six B_(j,l) positions with inverse hopping and B0 resets, Q0, and the actual two-level monitor with independent drive and label-resolved reset jumps. The 60-dimensional fixture retains an abstract three-level non-idempotent DATA map. It gives minimum success-before-rollback effect 0.09949, minimum A 0.06633, maximum A 0.52558, and the full drift identity error 8.12e-16. This verifies the timer/B mechanism while not pretending to instantiate the native Tanner GPT table.

The accepted scoped statements leave acquisition/FIFO useful drift, neighboring-owner activity, coherent guard activation, full product composition and useful DATA-energy coverage open. A terminal occurrence bound is not a correctness certificate for dirty output, and a clean committed drift is not a whole memory theorem.
