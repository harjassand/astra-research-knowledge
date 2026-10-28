# Small actual-record pilot: noncommuting spectator noise and acquired inverse search

28 October 2026. **Author pilot complete; independent audit pending.** This is a floating numerical experiment, not a received finite-control or statistical-acceptance theorem.

## What was actually executed

One fixed physical source maps ONE prepared logical qubit to TWO physical output qubits. A hidden equal mixture applies amplitude damping of rate .36 about either z or (3/5,0,4/5), correlated respectively with gauge states |0> and |+>. Those spectator states do not commute. A fixed dense entangling output unitary V is hidden from the learner. The native source has the positive operator-block representation, but not the scalar common-factor or commuting-sector whitening contracts.

Twelve independent banks used N=4,096,16,384,65,536 blocks, four replicates each: **344,064 individually RNG-drawn actual source blocks**, each with one uniformly random XYZ logical preparation/sign and two independently random physical Pauli readouts. Thus there were 344,064 logical preparations and 688,128 individual output readouts. A setting integer is drawn uniformly over the full Cartesian setting space, followed by an independent outcome uniform passed through the actual Born probabilities. This is not a known-mean Gaussian perturbation or a batch of model-predicted counts.

The complete integer count tensor and exact seeds are saved in ordinary_counts.npz. Each N is a fresh bank, not a prefix of a larger bank. No unknown payload or time-evolving retained-memory trajectory was sampled. The source has a noncommuting emitted gauge; that must not be relabeled as a demonstrated arbitrary-memory run.

Learner functions receive empirical signed contrasts from the counts and their own optimization seed, never V, true contrasts, actual damping axes, gauge states or error labels. Source parameters enter only the physical generator and post hoc scoring. Known-mean/noiseless diagnostics are explicitly separated from sampled banks.

## Candidate mechanisms and the equally informed ordinary comparison

1. Raw matrix signs, the earlier aligned-direction mechanism, are applied as a diagnostic outside their contract.
2. Scalar Hilbert–Schmidt Gram whitening is also outside its common-factor contract here.
3. Operator anticommutator Gram whitening is outside its commuting-sector contract here; a nonpositive empirical block causes rejection.
4. A four-start physical patch-unitary search maximizes the observable native recovery objective, then computes the own-commutant symmetric coefficient block and residual. No global-optimum assumption enters a certificate.
5. An equally informed ordinary full-CPTP decoder SDP is fitted to the SAME three signed contrasts. Numerical primal and dual solutions, Choi positivity repair, trace-preservation residual and primal–dual gap are checked. No full environment reconstruction is needed by this comparator either.
6. The SDP adjoint images are separately rounded by X=sign(A_X), Zodd=(A_Z-X A_Z X)/2, Z=sign(Zodd), Y=iXZ. The same saved banks are reused, with ZERO additional acquisition. Actual three-controlled-reflection extraction is scored, rather than assuming arbitrary unital images are unitary controls.

All methods see the same actual record bank. The comparison does not establish a new optimizer or an advantage over ordinary adaptive recovery SDPs. The useful point is that a standard convex recovery fit can propose an algebra whose complete inverse/gauge behavior can then be examined and separately certified.

## Findings, including unsuccessful routes

The exact-extraction native Bell loss is .19. In the noiseless diagnostics:

- Physical-unitary variational search gives .190000000000 (generator Frobenius error 1.7e-8).
- Full-CPTP SDP gives .190000000007, numerical primal–dual gap 1.14e-11. Rounded SDP extraction gives .190000000000.
- Raw signs give .1970314, scalar whitening .1924253, and operator whitening .1961256. Their biases persist with exact contrasts because their respective source hypotheses fail.
- Their worst-gauge virtual inverse losses are respectively .0185158, .0034130 and .0086230. The operator Gram happens to be positive here, so positivity alone does not repair missing commutativity.

Sampled rounded-SDP mean native losses and mean worst-gauge virtual inverse losses were:

- N=4,096: .2004556 / .0424562.
- N=16,384: .1918385 / .0090962.
- N=65,536: .1906742 / .0033140.

The four-start unitary search and ordinary full-CPTP SDP have nearly identical native scores on this fixture. At N=65,536 the raw-sign/scalar-whitening mean native losses are .2009721/.1965446, while their mean worst-gauge inverse losses are .0431644/.0269938. These are mechanism comparisons on one fixed source, not a broad practical advantage or optimal rate.

Operator whitening rejects all four N=4,096 banks and three of four N=16,384 banks because its empirical operator Gram is not positive. At N=65,536 it accepts its numerical matrix-function step but its mean native loss is .2050961. These failures are preserved, not removed as outliers.

All rounded SDP triples satisfy numerical square/anticommutation errors below 1.8e-15. Numerical SDP primal–dual gaps are at most 1.52e-7 in sampled banks. These are floating residual checks, not directed-rounding exact SDP or gate certificates.

## The honest certification failure

The same-block positive-fit gaps are numerically positive, but the conservative theorem-wide simultaneous confidence radius remains far too large. With the deliberately safe fixed logarithm L=16, a=sqrt(16*9*16/N), and provisional kappa=half the fitted block minimum, the acquired inverse bound 2(residual+sqrt(12)*a)/kappa ranges from roughly 55 to 602. **Every sampled bank fails the target delta=.1 acceptance test.** In particular the N=65,536 bounds are 55–68 despite small post hoc scored errors.

This demonstrates promising candidate search and an unresolved acquisition/certification budget, not a physically accepted accurate decoder. Numerical fitted gaps/residuals are not substituted for exact rational physicality, interval arithmetic or an acquired confidence certificate. No hardware, rational compiler or useful fault-tolerance threshold was executed.

## Reproduction and versioning

- run_pilot_before_sdp_rounding.py is the original completed acquisition/search/SDP program that results.json binds.
- run_pilot.py has only the added optional returned Choi matrix for reuse; it preserves the original acquisition logic.
- analyze_convex_rounding.py reuses ordinary_counts.npz and writes convex_rounding_results.json, with no new source draws.
- Both logs, all adverse runs and noiseless diagnostics are retained.

Run the original pilot with OPENBLAS_NUM_THREADS=1 to reproduce raw counts and initial results. Run the convex-rounding analyzer afterward. Python NumPy/SciPy floating linear algebra may produce tiny optimizer-dependent last-digit differences; the integer bank replay is exact for the stated NumPy RNG implementation. An independent audit will bind its own verified versions and actual scope.
