# Root generalization: independent exposure thresholds of bounded scaling dimension

The root researcher proposed the following extension.  I checked its
derivation independently and implemented its Weibull case separately from
the already-preserved exponential compiler.

## Model

Each component i has an independent threshold E_i with a known density
f_i on the positive half-line.  It fails when

    H_i(t) = integral_0^t a_i(X(s)) ds

first reaches E_i.  Local exposure rates a_i depend on the discrete failed
set and are nonnegative and attractive.  They do not explicitly depend on
time or on unobserved external inputs.  Thresholds are drawn once; the
system is generally non-Markov in X alone.  At most n components fail.

Assume, for known kappa_i>=1,

    f_i(c x) >= c^(kappa_i-1) f_i(x),  x>0, 0<c<=1.          (A1)

The inequality form is preferable to a ratio, because it also has a
meaning where densities vanish.  Define D=sum_i kappa_i.  Equivalently,
f_i(x)/x^(kappa_i-1) is nonincreasing wherever defined.  Gamma density of
shape alpha>=1 satisfies (A1) with kappa=alpha.  Weibull density of shape
k>=1 satisfies it with kappa=k.  Exponential thresholds have kappa=1.
These are mathematical examples, not statements that an experimental
system has these laws or that their parameters were acquired.

A Gamma or Weibull shape below one also satisfies (A1) with kappa=1,
since its density is decreasing; the implementation below retains the
original shape>=1 scope.  This is an optional mathematical observation,
not a claim that all threshold families satisfy (A1).

There is a sharp obstruction when the condition fails.  Let a single
node have threshold E=1+Exp(1), constant exposure rate a=1, and deadline
T=1+eta.  Its failure probability is positive.  A lower rate a_minus<1/T,
arbitrarily close to a as eta tends to zero, makes that probability zero.
The density vanishes below the positive threshold one, so no finite
global kappa can satisfy (A1).  A shifted deterministic minimum exposure
therefore cannot be silently included in the relative-law theorem.

## Deadline elasticity

For any fixed vector of thresholds, scaling all thresholds by c scales
all failure times by exactly c.  This follows inductively through the
ordered failures: between them exposure accumulates linearly at constant
state-dependent rates.  Thus tau_i(cE)=c tau_i(E), including infinite times.

For an upward-closed deadline event, let A_T be its threshold set.  Then
A_{cT}=c A_T.  A change of variables and (A1) give

    p(cT) = c^n integral_{A_T} product_i f_i(c e_i) de
           >= c^D integral_{A_T} product_i f_i(e_i) de
           = c^D p(T).                                    (A2)

The previous exponential proof using mixtures of holding times is no
longer needed.  The time-homogeneous exposure assumption is necessary for
the exact homothety.  A general age-dependent calendar-time rate does not
automatically satisfy it.

## Learned-rate domination of fine-time path laws

Suppose the acquired attractive rates obey

    exp(-rho) a_i(x) <= a_minus_i(x) <= a_i(x)

at every state.  For a particular path through T, write H_i and H_minus_i
for its cumulative exposures in the two models, evaluated on that same
path.  Then exp(-rho) H_i<=H_minus_i<=H_i.

On a fixed failure-order cone, the map from failed coordinates' times to
their exposure thresholds is triangular: exposure up to a node's failure
uses only failures earlier in the order.  Its diagonal derivative is
a_i(X(tau_i-)).  Integrating the independent thresholds of surviving nodes
therefore gives path density

    product_failed_i a_i(X(tau_i-)) f_i(H_i(tau_i))
       * product_surviving_i [1-F_i(H_i(T))].                (A3)

This is a density with respect to the natural disjoint union of
Lebesgue-measure failure-time cones and the discrete failure-set labels.
It is not a claimed Markov likelihood for the state process.

For a failed i, (A1) and kappa_i>=1 imply

    f_i(H_minus_i)/f_i(H_i)
       >= (H_minus_i/H_i)^(kappa_i-1)
       >= exp[-rho(kappa_i-1)].

The diagonal Jacobian ratio contributes another exp(-rho).  For a
surviving node, the survival-function ratio is at least one.  Hence the
acquired path measure minorizes the true path measure:

    P_minus >= exp(-rho D) P.                              (A4)

If a density vanishes, use the pointwise inequality rather than divide by
zero; P_minus may contain extra support, which does not invalidate the
minorization.  The common-threshold monotone coupling also gives
P_minus(E_T)<=P(E_T).  Consequently

    exp(-rho D) p <= p_minus <= p,
    TV(P_minus(.|E_T),P(.|E_T)) <= 1-exp(-rho D).            (A5)

The full-law bound is independent of event rarity.  Independence of the
thresholds and the learned uniform multiplicative bracket are essential
premises.  No claim about unknown arbitrary threshold laws is made.

## Held process and factorization

The pathwise delay proof only used fixed thresholds and attractive rates,
not exponential distributions.  It remains unchanged:

    tau_i <= tau_i^Delta <= tau_i+n Delta.

Together with (A2), for Delta=T/N and N>n,

    (1-n/N)^D p(T) <= p_held(T) <= p(T).                    (A6)

Since D>=1, Bernoulli's inequality gives

    1-(1-n/N)^D <= Dn/N.

The same computable two-deadline enclosure also remains valid.

For a bin assignment z, let H_i(z) be the exposure accumulated before i's
failure bin and let r_i(z) be the local rate in that bin.  Replace the
exponential factors by

    f_i(z_i,z_Pi) = F_i(H_i+Delta*r_i)-F_i(H_i),  z_i<N,
    f_i(z_i,z_Pi) = 1-F_i(H_i),                  z_i=N.      (A7)

For a fixed assignment the compatible thresholds form a Cartesian
product of these intervals.  The factors are therefore exactly
normalized, even for a cyclic dependence graph.  Their scopes are the
same as in the exponential construction; ordinary variable elimination
has the same width bound, with N of order Dn/epsilon.

For completeness, the rectangle assertion is constructive.  Induct over
bins.  If earlier bins agree with z, the beginning state and all exposure
increments in the current bin agree.  A node assigned to this bin has its
threshold between the exposure at its beginning and end, so it fails in
this bin.  A node assigned to a later bin has a threshold above the
exposure through this bin, so it survives.  Thus every threshold vector
in the rectangle realizes z.  Conversely, realization of z imposes these
same inequalities.  The rectangles partition threshold space apart from
boundary sets of zero measure.  No directed-acyclic-graph assumption is
used.

After a conditional bin draw, sample each independent threshold from its
known density truncated to the corresponding interval, then replay the
undelayed exposure process.  The threshold event for the held process is
a subset of the original event.  Its lost relative probability bounds
the total variation of the conditioned driver laws and hence of the
returned fine-time paths.  Combining with (A5),

    TV(returned path law,true law given E_T)
       <= 1-exp(-rho D) + 1-(1-n/N)^D
       <= rho D + Dn/N.                                   (A8)

The ideal-law versus finite-bit output distinction in PROOF.md remains
necessary.  A floating-point program cannot be given total-variation
distance below one from a nonatomic continuous law without specifying a
rounded-output or lazy-real representation contract.

## Executed Weibull implementation

The files aging_event_time_compiler.py and check_aging_compiler.py use
Weibull thresholds.  Under Y=(E/scale)^shape, Y is exponential, so
truncation can be sampled stably by transforming an exponential interval.
The base simulator already consumes thresholds and therefore requires no
Markov approximation.  The results are in aging_results.json.

The checked cyclic three-node example has shapes (1.5,2,2.5), D=6,
deadline 0.01, and N=160.  Width-two elimination gives probability
4.797129723006482e-12.  An independent positive quadrature over all six
failure-order cones gives 4.883037552497370e-12; refinement from order 64 to
96 changes that reference by 3.15e-7 relative.  The compiler's relative
bias is approximately 1.7593%, within the analytic 10.7357% bound.  The
two-deadline held calculation supplies an upper value
5.364406020974478e-12 without a true-process solver.

Three hundred conditional threshold-pullback paths all met the deadline.
One thousand completed-path density checks for state-dependent lowered
rates satisfied the lower density bound exp(-rho D), with rho=0.04.  These
are numerical checks of the analytic construction, not empirical
certificates of total variation or physical model acquisition.

## Established model and inference antecedents

Threshold representations, cumulative exposure, Weibull load-sharing
models, and statistical estimation of monotone load-share rules are not
claimed as new.  Relevant primary research includes:

- "A threshold representation for the strength distribution of a complex
  load sharing system", Journal of Statistical Planning and Inference
  (2000), https://doi.org/10.1016/S0378-3758(99)00094-4 .
- Kim and Kvam, "Reliability estimation based on system data with an
  unknown load share rule" (2004),
  https://pubmed.ncbi.nlm.nih.gov/15130052/ .  The described setting includes
  unknown load-share parameters and a monotone restriction.
- Kvam and Peña, "Estimating Load-Sharing Properties in a Dynamic
  Reliability System" (2005),
  https://pmc.ncbi.nlm.nih.gov/articles/PMC2762212/ .
- "Reliability analysis of load-sharing systems with memory" (2018),
  https://pubmed.ncbi.nlm.nih.gov/29470697/ .

The unresolved historical comparison concerns the complete acquired
small-scope, bounded-width, relative-probability and conditional-path
operation proved here, not the existence of these physical models or
their conventional statistical inference methods.

Useful numerical failure retained: a first 24-versus-40 Gauss comparison
differed by 6.38e-6, exceeding the selected 2e-6 reference tolerance.  The
noninteger shape causes fractional-power behavior at a simplex boundary.
Refining to orders 64 and 96 resolved the specific reference-accuracy
risk; no stronger quadrature accuracy or rigorous interval enclosure is
claimed.
