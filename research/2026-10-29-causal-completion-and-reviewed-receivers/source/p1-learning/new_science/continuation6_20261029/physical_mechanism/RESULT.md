# Response design from visible trajectories: completed constructive alternative

29 October 2026. Existing Astra P1 physical-mechanism role; no added branch,
worker pool or transfer. All prior continuations remain unchanged.

## Question and completed construction

Can one optimize the physical dynamics of a sensor without reconstructing
its inaccessible microscopic state? The concrete task chosen here is to
minimize stationary readout noise by changing the time shares of actual
reversible operations that preserve the same equilibrium law. The sampling
clock and exponential readout filter are fixed, so the objective is not won
by silently observing for longer or increasing every native rate.

Let P_w=sum_j w_j P_j, where all actual native kernels are reversible for the
same mu and each complete native round takes the same actual duration tau.
For |f|<=1, rho in (0,1), q=1-rho, define

    F(w)=q <f,(I-rho P_w)^(-1)f>.

The stationary exponentially filtered sensor Z_k=q sum_r rho^r f(X_(k-r))
has variance

    Var Z_k=[2F(w)-q ||f||_2^2]/(1+rho)-mu(f)^2.

Thus minimizing F exactly optimizes this declared physical readout. The
objective is convex, and its first-order simplex gap gives a global
suboptimality certificate. It needs no finite hidden-state model, no hidden
mixing gap, and no microscopic reset within an experiment.

The proposed acquisition is a chronological intervention experiment: execute
two independently geometrically distributed random-operation prefixes with
one forced P_j call between them, and correlate the initial and final sensor
readings. With c=rho/q, its bounded output c f_0 f_end is an exact gradient
estimate. It runs on one persistent specimen and never copies a microscopic
state. Its expected cost is 2c+1 native calls plus preparation, sensing,
controller and clock costs. Conditional Hoeffding bounds provide an acquired
global certificate. A conservative finite stopping optimizer with all-round
confidence is also proved.

## The strong ordinary method changed the conclusion

The strongest ordinary comparator can already acquire the needed derivatives.
In one geometrically stopped word, retain the selector counts N_j and the
endpoint product Y. Its simplex tangent score is

    Y[N_j/w_j-N],

whose expectation is g_j-w dot g and whose variance is at most
c(1/w_j-1). For two controls, S=N_1/w-N_2/(1-w) has
E S^2=c/[w(1-w)]. The subtraction of N is essential: using a raw-count
variance with an additional c^2 term would artificially weaken the comparator.

One ordinary trajectory estimates all tangent coordinates simultaneously and
costs only c expected native calls. An independently learned reward baseline
reduces variance further. A finite-variance median-of-means construction gives
the ordinary route its own finite confidence global certificate; no hidden
model or asymptotic CLT is required.

Forced insertion retains a genuine boundary advantage because it tests an
action whose current mixture weight is zero. But a competent ordinary
optimizer can use forced exploration or combine score and weak-derivative
estimators. The two-prefix experiment is itself a size-biased / marked-word
representation of the ordinary product derivative. No exclusive new physical
gradient operation or general resource advantage survives this comparison.

## Executed acquisition and matched comparison

The declared population supplier has 32 microscopic states, one visible bit,
and 16 hidden states. Mode 1 flips the visible bit with a hidden-dependent
dyadic probability. Mode 2 executes a lazy hidden hypercube move while leaving
the bit fixed. Both kernels are exactly symmetric rational matrices with a
common uniform stationary law; they do not commute. The sampler executes
every native call, retaining the hidden state within each trajectory. The
learner receives only visible endpoints and its own operation counts.

The readout parameter is rho=7/8, so a geometric word costs seven native calls
on average. A conventional score-based pilot selected w=47/64 for mode 1.
Independent validation then gave:

| Validation route | Baseline preparations | Actual native calls | Global F-regret upper bound |
| --- | ---: | ---: | ---: |
| Forced chronological insertion | 1,000,000 | 15,004,431 | 0.0841069875 |
| Ordinary selector score, median of means | 2,142,858 | 14,996,976 | 0.0175822056 |

Each certificate has at least 99.5% confidence under the declared sampling
model; the simultaneous guarantee is at least 99%. The score comparison pays
for its 50,000-sample reward-baseline pilot. Its rigorous certificate uses raw
scores with the proved variance bound, while its separately reported corrected
mean uses the learned baseline.

After design selection, independent population calculations found the optimum
weight 0.7727424755 and actual selected F-regret 0.0005404766. The selected
filtered variance is 0.6076278567; uniform scheduling gives 0.6367498476 and
the better individual native operation gives 0.6307235533. These modest fixture
improvements are not the destination or evidence of a foundational speedup.
They demonstrate the complete design-and-certificate interface.

At the selected weight, the insertion estimator's population variance per
expected native-call budget is about 11.98 times the optimal constant-baseline
score value. The actually learned baseline gives empirical score variance
28.6054, close to the population optimum 28.5551. This is a strong ordinary
comparison, not a model-fitting strawman. Near some boundary weights the
ranking reverses. Baseline preparation is also more frequent for the shorter
score trajectories, so no full-cost winner is inferred from native calls alone.

The complete run used 3,542,858 baseline preparations, 7,085,716 endpoint
readings, and 32,794,335 native calls including the design pilot. The explicit
ideal discrete random-bit ledger is 520,354,992 bits. Raw observable/control
records and their hashes are saved, rather than replacing acquisition with
population matrix products. These are synthetic native-operation samples and
population checks, not a laboratory result, interval certificate, or acquired
physical implementation precision budget.

## Obstructions and exact physical limits

Common stationarity alone does not give convexity: opposite deterministic
rotations on a three-cycle have a response objective with a strict interior
maximum. Reversibility is load-bearing for the global design certificate.
The ordinary score identity itself survives that failure, but a first-order
stationary point then need not be globally good.

The clock premise is equally load-bearing. Call-level response does not become
fixed-physical-time response when native durations differ. No free holding or
padding operation is inferred. Common equilibrium preserves a DC sensor mean;
it does not certify the gain for a changing external signal.

Fresh baseline preparation must be valid conditional on the complete retained
calibration record. A specimen trapped in one frozen hidden class cannot
learn an unknown population of such classes from repeated visible starts.
Deployment on the old uncharacterized specimen does not inherit stationary
noise merely because the selected weight has a confidence certificate.

Finally, a rare hidden mode can have an arbitrarily large undiscounted
integrated response while contributing negligibly to any fixed discounted
record. The theorem certifies the specified filter. A zero-frequency or
arbitrarily long-time claim needs an additional tail contract and pays the
real horizon-dependent acquisition costs.

## Sources, disposition and files

Primary predecessors were read early: Boyd–Diaconis–Xiao convex mixing design,
Ghosh–Boyd–Saberi effective-resistance optimization and its gradient/duality
formulas, Williams's episodic REINFORCE and reward baselines, random-scan Gibbs
adaptation, and primary abstracts of measure-valued derivative estimators.
Their exact URLs and actual read scope are in
`ORDINARY_SCORE_COMPARATOR_AND_SOURCES.md`. Preserved Astra mission and
scientific-acceptance sources governed the comparison; N675 was not reopened.

This is a useful positive unit: an exact stationary sensing objective can be
optimized and globally certified using visible trajectories without learning
the hidden dynamics. The strongest ordinary route already provides the core
capability and is substantially better in the executed interior comparison.
Historical novelty, an apparatus supplier, and substantial practical advantage
remain unestablished. The unit should be retained as constructive capital and
as a demanding ordinary comparator, rather than promoted to the central new
physical principle.

The governing proof, comparator proof/source record, executable sampler,
checks, raw observations and a hash manifest are all in this directory.
