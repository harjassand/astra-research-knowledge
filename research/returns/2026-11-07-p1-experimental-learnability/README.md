# What finite experiments can determine

P1's completed return moves from inference after a given history to computing the best accuracy achievable by any finite experiment programme, under an explicit noisy observation interface. It supplies a positive computability theorem, a representation-dependent impossibility theorem and an executed finite-budget design example. Their input contracts differ.

[Complete response, actual prompt and available activity](P1_EXPERIMENTAL_LEARNABILITY_20261107_RETURN.txt) · [Original ZIP](original/Experimental_learnability_2026-11-07.zip) · [Complete proof](package/RESULT.txt) · [Source identities and publication scope](SOURCES.json).

| Start with | Contents |
|---|---|
| [RESULT.txt](package/RESULT.txt) | Three full constructions/proofs, observation interfaces, deductions and costs |
| [README](package/README.txt), [sources](package/SOURCES.txt), [checkpoint](package/CHECKPOINT.json) | File roles, primary/Astra credit and preserved predecessor identities |
| [Experiment input](package/EXPERIMENT_INPUT.json), [optimal policy](package/OPTIMAL_POLICY.json), [fixed schedules](package/FIXED_SCHEDULES.json) | Exact catalogue/budget/model information, adaptive policy and fixed comparator |
| [Complete finite certificate](package/EXPERIMENT_CERTIFICATE.json), [producer verification](package/VERIFICATION.json) | All permitted actions/feasible responses and exact fixture results |
| [Experiment code](package/experiments.py), [bounded model evaluator](package/programme_models.py), [producer runner](package/run.py) | Preserved executable sources; Capital did not run them |
| [Programme-model controls](package/PROGRAMME_MODEL_CHECKS.json) | Finite evaluator/report examples, not a finite test of general undecidability |
| [Included unchanged inference ZIP](package/Certified_model_family_inference_2026-11-06.zip) | Byte-exact predecessor, already published in the [earlier model-family inference intake](../2026-11-07-p1-certified-model-family-inference/README.md); not a new discovery or separate intake |

## A. Computable optimal experimental accuracy

The retained dynamics are `z' = A z + B grad V(Cz) + u(t)`, with supplied rational matrices, finite horizon/forcing/observation schedule and polynomial task. One stationary global bounded-curvature C^(1,1) potential has a supplied anchor and finite **closed convex rational semialgebraic calibration prior**. Individual potentials may be nonconvex. The nonempty compact semialgebraic initial family may also be nonconvex, but it is independent of the potential. The prior's previous more general nonconvex posterior-inference scope is not silently transferred to this theorem.

The specified instrument queries rational x in a supplied rational box Q, at precision p. It reports a dyadic vector y with coordinate error at most `delta + 2^-p/2`, where the native error delta is **strictly positive**. This closed channel allows both rounding ties, adversarial/dependent errors and different legal errors on repeat queries. Repetition does not reduce delta; precision refinement removes quantization error. Direct gradient access, global curvature, known coupling, calibration validity and physical qualification are supplied information. No arbitrary measurement, free gain or direct task readout is granted.

Let Omega(r) be the largest task separation between two compatible potential/initial-state pairs whose gradients differ by at most r everywhere on Q. The infimum worst-case scalar prediction error over permitted finite deterministic experiment programmes is exactly

`R_delta* = Omega(2 delta) / 2`.

A terminating ordinary bit algorithm returns arbitrarily tight rational lower/upper bounds on that value, a finite programme achieving the upper bound and two actual compatible models witnessing the lower bound. Those two models admit identical reports under **every** permitted adaptive query sequence. The upper programme uses a fixed finite grid and the earlier posterior inference algorithm. The infimum need not be attained by one finite programme; this is not a claim that adaptation never helps under a finite budget.

The constructive bridge is an explicit convex repair of nearly indistinguishable models, with a computed task-continuity bound under mixing. Positive native error makes the repair quantitative. Paired THG interpolation tables retain one global potential in each block; uniform Euler/task bounds and charged real-algebraic optimization supply extrema and evaluable witnesses. The general CAD composition is proved and costed, **not implemented or executed as a general solver**. The theorem supplies no general zero-noise inverse modulus or coupled potential/initial-prior repair theorem.

Deductions include prediction-specific futility certificates, controlled instrument-noise sensitivity, reuse of compatible convex histories, finite task vectors under maximum-coordinate loss, and a finite intervention choice with regret at most twice a simultaneous prediction error. That regret upper bound is not an equality between prediction and decision-regret floors. Grid/report sizes, numeric precision, coordinate encodings, all preparation, online/offline CAD, algebraic witness extraction and evaluation are paid. Dimension-dependent grids and doubly exponential algebraic computation give no general efficient-design claim.

## B. Cheap forward evaluation does not make learnability computable

A separate representation supplies two models by certified approximation programmes: `V0(x)=x²/2` and `V1(x)=x²/2+a_e x`, where `a_e=1/2` for nonhalting machine e and `1/2+2^-(t+2)` if its first halt is at t. Every coefficient is rational, every Hessian is 1 and both gradient flows contract at rate 1. Their equilibrium task is explicitly 0 or `-a_e`; no difficult unconstructed asymptotic evaluator is required.

With native error 1/4 and the stipulated gradient channel, the optimal error is **1/4 if e never halts and 0 if it halts**. Uniform approximation of that optimal accuracy value to error 1/16, or deciding whether error below 1/8 is achievable, would decide halting. This is noncomputability of the value, beyond merely failing to compute an optimizer.

Forward potential/gradient/equilibrium evaluation has the supplied uniform polynomial bit-time bound in machine description, query bits and requested precision. Resolving the tiny offset can still require very high precision. On learnable instances the proof gives no computable uniform worst-case work bound in description length, counting all preparation, query-position bits and fixed-point report bits. The closed rounding/encoding interface is material to that bound.

This does not contradict Part A: the prior has **two models rather than their convex hull**, and the rational coefficient is programme-presented rather than given by its explicit numerator/denominator. Explicit rational input restores that comparison's decidability. Taking the convex hull in this example removes the discrete-prior gain and yields a constant 1/4 floor. No P versus NP claim or universal obstruction to the earlier finite algebraic-input solver follows.

## C. Executed finite-catalogue optimal design

The implemented specialization concerns a whole stationary scalar-law family with global secants in [m,L], m > 0, finite interval data, known forcing and equilibrium task `g^-1(u)`. A finite catalogue specifies rational query locations, dyadic precisions and positive action costs; an integer budget is supplied. Closed-class N1039 envelopes give exact feasible reports, attained posterior equilibrium endpoints and endpoint laws.

Exhaustive rational minimax recursion includes stopping, every affordable action and every feasible report. A complete finite transcript has one compatible stationary law; the adversary is not allowed to switch worlds along a path. The producer's fixture used four unit-cost actions, budget 2, slopes [1,3], g(0)=0, forcing 1, native error 1/32 and report precision p=4:

| Permitted information | Exact worst-case equilibrium error |
|---|---:|
| No measurement | 1/3 |
| Best one measurement | 5/32 |
| Best fixed schedule of at most two measurements | 5/48 |
| Best adaptive programme of cost at most two | **1/12** |
| Unlimited finite programmes on [0,1], with refinable precision | **1/32** |

The last row is a proved continuum floor, not the executed policy's achieved risk. The exact fixture certificate covers 2,011 posterior/budget states, 3,836 response edges and all 21 fixed schedules. An attained worst transcript retains equilibria 13/16 and 47/48, with half-separation 1/12. Producer checks report rejecting a corrupted value, missing action and missing feasible response. The verifier shares its rational envelope kernel with the constructor; it is not an independent or formal verification. Finite machine controls do not prove general undecidability.

For the anchored scalar continuum family, the supplied exact floor is `min((u/m-u/L)/2, delta/m)` when the query region contains [0,u/m]. This specialization also constructs an upper programme at zero native noise, without extending Part A's general zero-noise scope. Finite-catalogue recursion is exponential exhaustive design in general; all report branches, budget/precision values, rational arithmetic, memoization and certificate output are charged. No physical acquisition was performed.

## Credit, status and preserved scope

THG interpolation, real-algebraic algorithms, optimal-recovery/two-source principles, minimax recursion and halting undecidability retain primary credit. N1039 supplies the closed-law envelopes, with analytic-slack qualifications intact. N1018's exact native linear-information benchmark is not transferred to this nonlinear task/prior/channel; N997's historical experiment heuristic is not promoted into a general optimal-design theorem. N1226's geometric and stated effective-construction approach, N716's distinct simulator/latch and all mechanical/SAT predecessors remain credited and unchanged.

Collected 7 November 2026 Brisbane. Capital retained the original 14-member archive, included unchanged predecessor ZIP and complete capture, without scientific execution or a new audit. No coordinator grade is inferred at this publication, and no priority, practical/physical advantage or civilisation-scale achievement is established. Generated retrieval remains pending under the resource limits. P1 has completed this turn; P2/P3 are reported continuing current turns. Capital sends no scientific assignment; the standing coordinator/dispatcher authority, Sol closure, Dots protection and all source/resource limits persist.
