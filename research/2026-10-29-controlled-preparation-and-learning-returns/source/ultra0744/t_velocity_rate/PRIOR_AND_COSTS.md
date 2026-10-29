# Prior, source fit, actual execution and remaining costs

## Closest established operations

**Fournier, hard-potential recursive output.** The governing primary is
https://arxiv.org/html/1703.10874v1, published in Kinetic and Related Models
12 (2019), 483--505, DOI 10.3934/krm.2019020. Sections 2--3 supply the exact
weighted recursion and its nonexplosion proof. The counter/clock argument is
adopted explicitly in PROOF.md, not claimed new. The source's multiplicative
mass changes even at null collisions; hard_sphere.py preserves this crucial
rule in the ordinary comparator. The source expressly leaves the mass second
moment unresolved. It does not say that moment is proved infinite. Its own
practical-efficiency caveat applies; we do not substitute an easier Maxwell
recursion and call it the hard-sphere comparator.

**Energy-based particles.** Peraud--Hadjiconstantinou, 2011,
https://arxiv.org/html/1109.3910v1, Section 2.2, constructs fixed-energy
computational packets for phonon transport in the relaxation-time approximation.
Thus tilting a distribution by a conserved quantity and conserving packets are
established ideas. That source is not a proof of this nonlinear elastic-gas
partner recursion. Historical priority of the present composition is UNKNOWN;
the result is not presented as the invention of energy weighting or recursion.

**Serious practical nonlinear alternatives.** Pareschi--Trazzi--Wennberg,
https://arxiv.org/html/1009.2768v1, Section 4.2, handles variable hard-sphere-type
rates using dummy collisions and a velocity maximum for the supplied finite
particle set. That finite maximum is not a global envelope for the infinite
nonlinear law. The same source develops recursive/time-relaxed methods, reuse
of paired collision outputs and adaptive thermalization; these are stronger
ordinary alternatives than an unqualified naive time grid. Matheis--Wagner,
SIAM J. Sci. Comput. 24 (2003), DOI 10.1137/S1064827502406014, is also primary
prior for weighted-particle convergence and variance reduction. Its abstract
was screened; its full proof was not consumed as a theorem premise here.

The executed ordinary population is a continuous-time finite-N Kac process.
Each unordered pair has collision rate |v_i-v_j|/(N-1). A lazy maximum heap
maintains a valid current speed envelope; no fixed evolved-velocity cap is
assumed. It has no time-step bias. Its finite-N error is NOT certified away,
and particles in a single population are not treated as iid nonlinear outputs.

## Astra source fit

Selective operation retrieval was served current at the recorded check times:
input 2f94a3c6ae0d729c91e936b58b84af96f66c9850525b447602b8acb884d86015,
revision 3882c05cc803ff107b4d89f4010090ed41c3a392, 29 October 2026,
06:39:32--06:59:14 UTC. This is a snapshot statement, not a perpetual freshness
claim. The complete response/packet/source wrappers are saved under sources/.

N58 was fetched through its complete conditions and governing report and
**rejected as a premise**: its three-gain rank mechanism addresses a kinetic
nonuniqueness/regularization interface, not an iid hard-sphere sampler. The
previous T finite-mark/rotation operation remains restricted to Maxwell rates.
No archive-wide loading, interface repair, new simulation oracle or transferred
Gaussian-convolution identity was used.

## Fixed executed comparison

All source velocities are the six signed coordinate unit vectors with equal
probability, angular measure has mass one, and a=e0=1. This source does not
grant that the evolved velocities remain bounded; the recursive tree permits
arbitrarily many bounded-source leaves. The plan was fixed in run_acquisition.py
before execution: 12,000 independent outputs per recursive method at t=0,1/4,1;
16 independently initialized N=5,000 ordinary populations at t=1. No seeds or
times were retried after inspecting statistics.

| Method | t=0 | t=1/4 | t=1 |
|---|---:|---:|---:|
| Normalized currency, seconds | 0.07653 | 0.24733 | 5.54106 |
| Matched Fournier weighted, seconds | 0.02336 | 0.07707 | 1.55956 |
| Currency total partner calls | 0 | 41,113 | 1,342,201 |
| Weighted total partner calls | 0 | 20,225 | 595,763 |

The finite-N ordinary comparison used 147,201 pair proposals over all 16
populations and took 0.36635 seconds. All acquisition, summary and population
work took 8.02433 seconds after imports. These are literal implementation
times, not optimized complexity comparisons. In particular the currency
source weights are recomputed in each literal finite-table draw; a precompiled
categorical source would remove that avoidable O(J) arithmetic. No optimized
timing or universal practical superiority is inferred.

At t=1 the currency algorithm used 24,060 complete g attempts for 12,000 f
outputs, success 0.498753 versus the exact 1/2. Counts include 1,366,261 source
draws, 2,708,462 exponentials, 437,246 real collisions and outgoing choices,
all failed final proposals and all null-event partner subtrees. Maximum live
stack depth was 18. Every physical output had weight one.

The same-time weighted comparator had sample mass range approximately
[1.49e-5,289.95]. Its observed empirical mass standard error was 0.02853;
this finite sample neither establishes nor refutes finiteness of the true
mass second moment. For the bounded radial test 1/(1+|v|^2), currency mean
0.5335332 has empirical SE 0.0012963; weighted mean 0.5321664 has empirical
SE 0.0143386. The finite-N population mean is 0.5330137 with independent-
population empirical SE 0.0002028. All three declared bounded test differences
were retained. The largest absolute currency/population difference divided
by their combined empirical SE was about 1.33. This is a diagnostic, not a
proof of the law or a population-bias certificate.

## Proof/code controls and scientific limits

certify_generator.py does not import the sampler. It checks the generic
exchange/selection identity, manifest positive probability/drift polynomials,
six literal rational tests, exact nonflat-source tilting/rejection, and the
six-axis initial fourth-moment derivative 2sqrt(2)/9. Its final exact-algebra
receipt took 0.02006 seconds, excluding imports. This consumer is not a test
of the infinite recursive termination theorem; that is an analytic argument.

The theorem's first work bound is double-exponential in t; an independent
elementary fourth-moment estimate sharpens it to exponential in t for bounded
source inputs. At the executed source L=5.8888437389, so the guaranteed
per-output mean number of partner calls is at most 2(exp(Lt)-1). It is not
uniform in time and can be useless at late kinetic times. The ordinary
finite-N method wins literal runtime, and can be given existing approximation
analysis when its constants/task warrant are supplied. No global incumbent
performance claim survives this comparison.

Output-law and Hoeffding statements are ideal-real/iid-source theorems.
Executed arithmetic/PRNG is binary64 and does not supply exact continuous-law
or finite-bit output. Quantization, high-confidence runtime optimization,
spatial transport, non-cutoff kernels, actual collision-kernel/material
calibration and practical late-time acceleration are not acquired. No
physical, paid, external-write or outreach action was taken.
