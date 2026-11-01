# Independent receipt: resonant finite-qudit source admission

2026-11-01. **Qualified PASS for the specified autonomous GKSL source and its all-state cache/activity service.** This is not a whole-controller memory theorem or an atomic implementation claim.

Frozen reviewed source files, all under `producer-workspace/independent_syndrome_sensor_20261101`:
- `TWO_BODY_STAGE_COMPLETION_OBSERVABILITY.md`: `aeba76b86eed67f55a49622a000bdf483c3286279ae762dcaf423f23a88c5528`.
- `UNIFORM_FINITE_TIME_CACHE_REFRESH.md`: `b92183c61fb508841f62fe2db0cd4810a70208761399a4757befb5efb77eddb8`.
- `EXPLICIT_TWO_BODY_QUDIT_SOURCE.md`: `2f9c719452704a9774cfd5bb423fb5e9731d622bbbe3b1982bd541f13a667795`.

## 1. Stage observability checked

After gauging the excited block by its unitary U and removing common environmental motion, the no-target-completion amplitudes obey a'=-ig b and b'=-ig a-iD(t)b-gamma b/2, with ||D||<=B. Eliminating a gives the stated Volterra formula. The convolution kernels have L1 norms bounded by T and T²/2, so the displayed L2 estimate is valid also for vector-valued amplitudes and arbitrary initial entanglement.

The Gram matrix for b0-igt a0 has trace T+g²T³/3 and determinant g²T⁴/12. Its smallest eigenvalue is at least determinant/trace. At T=1/(g+B+gamma), the total denominator is at most 12(4/3)(5/2)²=100. Therefore

 P(completion by T)>=gamma g²/[100(g+B+gamma)³]

holds for every normalized live-stage state, including ground/excited coherence. Reconditioning after a past no-completion event is allowed because the bound is uniform over the resulting joint state. Future neighbor-record postselection would not be allowed and is not needed.

Other apparatus channels commute with U and become identical environmental channels in both blocks. One rigorous reading of the dilation step is a repeated-interaction/Trotter approximation: dilate these channels by fresh ancillas with unitaries commuting with U, apply the amplitude argument between the kicks, and take the finite-dimensional channel limit. The estimate is uniform in the dilation size and uses only the bounded incident Hamiltonian difference B. It does not assume a bounded norm for an infinite bath Hamiltonian. Noncommuting data-noise channels do not meet this ideal argument and must remain perturbations.

The geometric-block survival and moment generating function follow by stochastic domination by T times a geometric random variable. Conditional tower bounds multiply the stage factors without independence. An arbitrary partial cycle requires at most w live completions and one final exponential response. The stated C, S(t)=min(1,C exp(-theta t)), and tau<=(log C+1)/theta are valid.

## 2. Actual Hilbert space and all-state closure

The count 2+8w+4=8w+6 is correct. There is no unused binary-string or particle-number sector. Every basis state lies in idle, one live g/e pair, or final readout. Distinct-stage coherences are not assumed absent physically: the measured observable algebra is block diagonal and is preserved by the specified generator. Thus such coherences do not affect the quantities bounded. Coherence within a live pair is retained in the stage proof.

Preparation has hazard r Pi_idle; each stage's collective b-preserving decay has the specified gamma excited hazard; final X-basis readout has total hazard gamma Pi_final. Cache is not written before the final readout jump. The response estimate therefore includes the actual final response channel rather than an unspecified detector.

The decay must indeed be a single coherent sum over b for each j,c. Resolving b in the environment is a different source; nothing in this receipt licenses replacing that collective reservoir by separate transitions. Separate channels across different stages are also part of the supplied model.

## 3. Exact invariants and corrector algebras

For O commuting with every full check, the apparatus dressing is diagonal and independent of cache c. On a stage transition, the change of prefix commutation sign equals the sign from commuting O through P_j^b. The two signs cancel. All other apparatus factors commute with this local transition. Decay endpoints have identical prefixes; preparation endpoints have identity prefixes; final and idle have trivial dressing because [O,S]=0. Therefore EACH H_j and EACH specified jump commutes with dressed O, as does its adjoint. This verifies termwise invariance, not just a cancellation in the total generator.

In particular dressed stabilizers commute, and e_s=(I-Z_cache,s Sbar_s)/2 is a projector. Neighbor evolution preserves its dressed check even during collisions. Only the target's final cache write can change its cache mismatch.

Every jump has definite input/output cache blocks and the Hamiltonians preserve them. The full joint cache-block-diagonal observable algebra is invariant, even for observables correlated with data and other apparatus. Each truncated source generator retains this property. Hence both mismatch and activity finite-patch correctors are cache-block diagonal.

A controlled read sum_c Pi_c tensor V_c on a separate Boolean register commutes with these correctors. The corresponding read jump's dissipator annihilates them when its complete input/output register operators also commute with the corrector. This conclusion covers genuine input reads, not cache overwrites, cache rotations, or arbitrary data updates. If a Boolean gate also reads witness/flag variables, their commutation with the corrector must separately be checked; cache diagonality alone does not establish it.

## 4. Clean instruments and last-window service

During a collision-free freshly prepared cycle all overlapping apparatus are idle until target completion. Other source dynamics acts on disjoint data. In the gauge frame each live stage is a scalar driven-decay problem tensored with the data identity. Each completed stage consequently contributes its intended controlled P_j, up to a state-independent waiting amplitude. Final X readout gives the usual parity projector for a good prepared probe; the bad probe-preparation branch flips the report. Coherent extraction dwell does not itself introduce a measurement error.

The activity bound follows by charging the initially active cycle S(t), then integrating subsequent birth intensity <=r against the uniform conditional survival envelope. It gives the OPERATOR inequality exp(tG)A<= [S(t)+r tau]I, since it holds for every initial joint state.

The refresh proof's clean word is sound without future postselection:
1. Over the first F, union-bound failures of no attempts and of flushing initially active cycles. These are unconditional failures from the block-start state, not a completion theorem conditioned on future absence of starts.
2. Conditional on the resulting past event, all relevant apparatus are idle. The first neighborhood attempt is a target attempt within F with probability at least rF/2.
3. At that stopping time, a good preparation has probability >=3/4. From its resulting arbitrary joint state, separately bound completion failure by S(F) and future neighbor-start probability by Delta rF. Their union is at most 1/4. No independence of these events is asserted.
The product exceeds rF/8 and all stages finish by 3F. Iteration uses only conditional lower bounds from past block endpoints.

The bad-report bound correctly includes a target cycle already active at the last-window start; it also counts every later collision incidence and bad preparation. Thus a good report earlier in the window is not mistaken for a permanently correct cache. On the event of at least one clean report and no bad reports, the final mismatch observable has zero contribution by the CP-instrument identity and subsequent invariant source evolution. All remaining contributions are bounded by their probabilities. This establishes the displayed full-state operator service bound, not merely a stationary mean.

Independent rate-r attempt streams are a valid uniformization ONLY on the invariant active/stage/cache observable algebra. Null attempts while active need not reproduce off-block coherences. The proof uses precisely that algebra, and does not claim a full-channel Poisson-clock equivalence.

## 5. One explicit asymptotic correction

Section 7 of the reviewed cache note defines z=Delta r tau+p. Its displayed bound also contains r tau from the pre-window cycle. When Delta=0 and p=0, z vanishes identically and cannot control that term. Use

 z=(Delta+1)r tau+p,

or explicitly assume Delta>=1. This does not change small-floor attainability: take r tau and p small, then finite B and L of order r^-1 log(1/z). This receipt accepts the exact displayed service inequality and the corrected asymptotic convention; it does not silently validate the isolated-check shorthand.

## 6. Remaining whole-join obligations

The independently accepted finite-patch compiler can now consume this explicit source's e_s and A_s service, with autonomous local-generator norms and encoded coefficients charged. It yields source-generator drift only. The following are not supplied by this receipt: full actuator/Boolean perturbations of correctors, their patch-incidence constants, a positive final barrier margin, protected factorization under all actual expanded J†J terms, or native noisy readout.

The Hamiltonian source interactions are two-body qudit/data terms and the source jumps are onsite. The full Boolean controller may still use three-body GKSL primitives. Collective reservoir engineering, phase references, directed pumping, all 8w+6 levels, noise after rates are fixed, and geometry are real resources. No laboratory realization, practical parameter regime, or novelty conclusion is certified here. This was an ordinary independent mathematical audit, not a physical or numerical end-to-end experiment.
