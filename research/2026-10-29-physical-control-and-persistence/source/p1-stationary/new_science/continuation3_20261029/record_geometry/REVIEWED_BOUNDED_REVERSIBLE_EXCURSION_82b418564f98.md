# Bounded physical excursions that program an invariant law

29 October 2026. Astra P1, root construction. Same continuing role.

## 1. Question and consequence

The earlier finite-data receiver controls stable observables by acquiring
pointwise transition accuracy. That route loses force near phase coexistence,
and complete long records can distinguish small errors. The present question
is different: can actual operations preserve a desired invariant distribution
exactly without learning the hidden kinetics or making the visible process
Markovian?

The construction below answers yes at a specified interface. One physically
executable reversible Markov operation, a noninvasive binary label, and causal
endpoint stopping suffice to multiply the invariant weight of one label by
an integer N, using between one and N calls. The output is the current physical
state, including whatever hidden state the actual trajectory has produced.
Neither a microscopic copy nor restoration of the initial microstate is used.
Hidden memory may evolve, and need not mix. The proof is a pairing of actual
forward and reversed excursions, including the same-label trajectories.

The first-passage/uniform-residual pair was supplied constructively by the
existing record-geometry helper in the unknown binary iid model. Root extends
it here to arbitrary reversible microscopic kernels, proves the complete
kernel and occupation identities, and composes it into interacting programs.
The initial low-mobility two-flip construction is retained as a failed route.
Trace kernels, path reversal, Metropolis sampling and stationary-time theory
are established mathematics. Priority for this particular physical assembly
is not established by the literature search.

An important qualification is part of the result: the programmed invariant
law is sampled at **operation-completion indices**. The theorem does not turn
the raw physical-time occupation into that law. With only one native operation
run back-to-back, the underlying native path is unchanged; the compiler
selects its physical endpoints. A network with different addressed operations
does change the subsequent actuation schedule, but still has a separate clock
law. No autonomous thermal equilibrium, free preparation, erasure, energy
advantage, rapid low-temperature mixing, or fixed-time reset follows.

## 2. Actual interface

Let X be a standard Borel microscopic state space, with a probability measure
mu and an actual Markov kernel P satisfying ordinary detailed balance

    mu(dx) P(x,dy) = mu(dy) P(y,dx).                 (1)

The state need not be finite or observable. A measurable noninvasive label
partitions it into A and B. An endpoint call applies exactly the same P;
conditional on the present microscopic state, it is the stated Markov
operation. Apparatus/bath memory that changes the next-call law must be
included in X, or the premise is false. No independence of successive visible
increments, visible lumpability, spectral gap or ergodicity is assumed.

The controller can read the label after each call, retain the starting label,
count calls, and use independent supplied randomness. Switching and sensing
must either be noninvasive at the modeled boundaries or be incorporated in
the actual P and controller timing. There is no granted zero-call branch,
physical hold, microscopic rollback, copy, or hypothetical paired future.

P is a genuine available operation, not a matrix inferred from equilibrium
weights. Detailed balance in (1) is an exact structural premise. Finite
measurements do not prove that identity or supply a missing actuator.

The two sets may contain arbitrarily many hidden states. A_mu=mu(A) and
B_mu=mu(B) are assumed positive for the conditional cost statements. The
kernel construction itself is defined at every physical state. Bounded
stopping means no recurrence assumption is required.

## 3. Literal integer protocol

Fix integer N>=1. Call A the lower-weight label and B the label to be weighted
N times as much relative to mu.

Starting in A: repeatedly execute P, stopping at the first endpoint in B or
after N calls, whichever comes first.

Starting in B: execute P once. If the endpoint remains in B, stop. If it is
in A, select L uniformly from {0,...,N-1}. Execute at most L further calls,
stopping at the first return to B or when those L calls are exhausted.
L=0 means stop at the current A state after the already completed first call.

Every branch executes between one and N native calls. No unsuccessful branch
is discarded. The labels on intermediate calls, chosen L, completion count
and controller record can all be retained. The invariant-law assertion is
about the microscopic endpoint marginal, not independence from those records.

If N=2^b, exactly b fresh fair bits supply L (they may be drawn in advance).
Counter storage needs O(b) bits. Their generation, reads, arithmetic and
decision latency are real costs. A hard cap on native calls is a hard
physical-time cap only with actual bounded-duration calls and a compatible
bounded-time controller. No unmodeled evolution during decisions is allowed.
For other N, exact uniform selection may use a supplied selector or rejection
sampling; rejection sampling has unbounded randomizer time and must not be
called a deterministic physical deadline.

## 4. Full microscopic kernel and reversibility theorem

Use the block kernels of P on A and B. Put M=P_AA and

    S_N = I_A + M + ... + M^(N-1).

Directly enumerating the actual stopped trajectories gives

    K_AA = M^N,
    K_AB = S_N P_AB,
    K_BA = P_BA S_N / N,
    K_BB = P_BB + (1/N) sum_{j=0}^{N-2}
                         (N-1-j) P_BA M^j P_AB.     (2)

For N=1 the sum is empty and K=P. All products are genuine chronological
kernel compositions. The I_A in S_N represents a zero-length part of a
longer path whose total length is at least one; it is not an identity actuator.

The first two rows of (2) follow by the first-hit decomposition. In the third,
a terminal A path has first step B->A and then L further A->A steps. Each
L is chosen with probability 1/N. For the final row, a B->A excursion with
j internal A->A steps returns to B in j+2 calls. It is permitted by exactly
N-1-j choices of L. Same-label one-step paths account for P_BB. This derivation
also proves positivity and row sums one; no matrix repair is involved.

**Theorem.** K is reversible with respect to

    nu(dx) = [1_A(x)+N 1_B(x)] mu(dx) / Z,
    Z = A_mu + N B_mu.                              (3)

Proof. Regard the block kernels as operators between L2(mu restricted to A)
and L2(mu restricted to B). Detailed balance says M and P_BB are self-adjoint
and P_AB^*=P_BA. Thus M^N and S_N are self-adjoint. The cross-block identity is

    K_AB^* = P_BA S_N = N K_BA.

Each term P_BA M^j P_AB in K_BB is self-adjoint, so K_BB is self-adjoint as
well. Multiplying the B inner product by N makes all four blocks adjoint in
the required directions. This is detailed balance for (3). Equivalently,
reverse every finite path: an A->B first-hit path of length ell has a unique
B->A partner with residual budget L=ell-1, and weight 1/N. Returning paths
within a label reverse with the same coefficient. The proof uses at most N
steps, so it applies to general hidden spaces without an infinite-series or
return-time convergence assumption. QED.

This is not the earlier signed-continuation theorem's forbidden constant
transition. The entire K can depend on the hidden kinetics. Only its invariant
weight ratio is fixed. The earlier exact/approximate operation-language
distinctions remain unchanged.

## 5. General weight ratio and the residual-horizon identity

More generally choose a positive integer random horizon H<=N with mean r.
Write t_j=Pr(H>j) for j=0,...,N-1, so t_0=1 and sum_j t_j=r.
Starting in A, use the first-hit rule with horizon H. Starting in B, after
one step into A choose L with Pr(L=j)=t_j/r and use the return rule above.

Then (2) becomes

    K_AA = E M^H,
    K_AB = S P_AB,             S=sum_j t_j M^j,
    K_BA = P_BA S/r,
    K_BB = P_BB + (1/r) sum_{j=0}^{N-2} v_j P_BA M^j P_AB,
                              v_j=sum_{ell=j+1}^{N-1} t_ell. (4)

The identical adjoint proof gives nu proportional to mu(1_A+r1_B).
Every real 1<=r<=N admits H on floor(r),ceil(r). An exact implementation
requires the stated horizon and residual selectors; known real numbers do
not automatically give finite-bit or bounded-latency randomness. Integer
powers of two in Section 3 give the clean literal bounded-random-bit family.

## 6. Exact cost and physical-time occupation

Let c(x) be the expected number of native calls in one macro starting at x.
For the general horizon, c_A=S1_A. For B,

    c_B = 1_B + P_BA V1_A/r,
    V=sum_{j=0}^{N-2} v_j M^j.

Stationarity of mu gives mu_B P_BA=mu_A(I-M), as measures on A.
The polynomial identity (I-M)V=rI-S therefore yields

    integral_B c_B dmu
       = B_mu + A_mu - (1/r) integral_A c_A dmu.

Consequently the exact target-equilibrium mean is

    E_nu[number of native calls]
       = r(A_mu+B_mu)/(A_mu+r B_mu).                (5)

Since A and B partition X, the numerator is r; the unsimplified form is
useful inside an isolated local context. If the baseline label masses are
equal, (5) is 2r/(1+r)<2 (equal to1 at r=1). This is a **stationary mean**,
not a pointwise or arbitrary-initial-state cost bound; individual starting
microstates can cost nearly N. The unconditional hard native-call cap is N.
The same formula holds separately in every closed component with positive
baseline mass, using that component's A and B masses.

For a single native kernel run back-to-back, all intermediate steps are
still the original P chain. If macro starts have law nu, the expected
occupation measure of pre-call states during one macro is

    E_nu[sum_{j=0}^{tau-1} 1_{X_j in dx}] = (r/Z) mu(dx). (6)

Proof: the A-start contribution to A is mu_A S/Z. The B-start contribution
to A is mu_B P_BA V/Z=mu_A(rI-S)/Z. The B pre-call states occur only as the
initial B state, of mass r mu_B/Z; after a return the macro stops. Sum these
to obtain (6). Thus the native-time occupation is mu after normalization,
not nu. This exact clock cancellation prevents interpreting the endpoint
reweighting as a new physical energy potential or free stationary holding.
In continuous time, call interiors require their actual occupation kernels;
endpoint identity (6) alone does not specify them.

## 7. Consequential receiver: local interacting programs without kinetic learning

Supply a finite visible bit vector y and actual local kernels P_i on a common
microscopic space. Each P_i is reversible for the same baseline mu and really
preserves every visible bit other than i. This is the addressability/isolation
premise; it is not inferred from the mathematics. Hidden coordinates can
change and can be shared between sites, provided the complete P_i obey these
conditions. Readout and switching must be compatible with the actual kernels.

Choose a positive visible weight W(y). In each fixed neighbour/context value
c=y_-i, let A be the bit value with smaller W and B the other. Apply Section 5
with ratio r=W(B,c)/W(A,c), using that same P_i throughout the macro. Since
P_i never leaves context c, the block proof applies independently there.
The resulting K_i preserves, and is reversible for,

    nu_W(dx)=W(Y(x))mu(dx)/mu(W).                   (7)

The magnitudes W(A,c), not only their ratios, cause no problem: multiply
the local detailed-balance identity by that context's common constant.
Any prescribed scan, or independent state-independent random scan, of these
K_i preserves (7). Arbitrary history-selected schedules or changing the
kernel during an excursion are not justified by individual invariance.
After calibration D, kernels may be selected and frozen for deployment
provided every selected actual P_i (or context-dependent choice) has the
same reversibility and isolation contract, and the same choice is used in
both directions of each local edge. Pointwise algebra then holds for every D;
there is no concentration error in the target ratio under that structural
premise. This does not make the conditional initial distribution given D equal
to nu_W, or supply convergence from it.

If W(y)=2^{-E(y)} with integer-valued energy E and bounded local differences,
each local ratio is N=2^{|Delta_i E|}. The literal protocol needs at most
2^{max |Delta_i E|} native calls per local update and max |Delta_i E| fair
bits. For a bounded-degree finite-range energy, these resources depend on
the local energy range, not the number of sites. A random-scan selector and
all sensing and energy computation are additional costs.

For example, W(s)=2^{sum_{edges} s_i s_j}, s_i in{-1,+1}, on a degree-four
regular graph has local ratios in {1,16,256}. It has the usual ferromagnetic Ising
weight at dimensionless coupling log2, including the strongly ordered
square-lattice regime. Each local update has native-call cap256, needs at
most8 fair bits for its residual horizon, and has target-stationary mean
below2 native calls whenever the baseline conditional bit masses are equal.
This example identifies an interacting family; the paper does not substitute
a larger easy numerical ring for the theorem or claim to solve its slow
mixing. Phase coexistence and computational barriers remain in the target.

The endpoint law in (7) is the microscopic invariant law. Its visible
marginal is proportional to W(y)mu(Y=y). A specified Gibbs target therefore
requires a known baseline visible measure (uniform is a useful supplied
case), or explicit compensation for a warranted nonuniform baseline.

## 8. Conserved sectors and preparation are separate

If all physical operations preserve a hidden component C, the initial weights
of C cannot change. The global normalized law (7) generally reweights these
components by mu(W|C); merely showing that (7) is invariant does not prepare
those new component weights.

A sufficient condition for visible preparation from arbitrary conserved-sector
weights is that every accessible component has the same baseline visible law
pi_0 and that the compiled dynamics converges within each component to its
normalized W tilt. Then each component has the same visible target
pi_W(y)=W(y)pi_0(y)/pi_0(W). Sector mixing is unnecessary. Convergence rates,
uniformity over initial hidden information, and actual preparation costs
still need their own supplier; no finite-time guarantee follows merely from
invariance. Correct preexisting nu_W sector weights are another legitimate
route. Neither route is silently supplied by baseline calibration.

For a concrete obstruction, let two frozen equal-weight sectors have baseline
Pr(Y=1|C)=1/4 and3/4. Their aggregate baseline is uniform. With W(1)/W(0)=3,
the global tilt has visible mean3/4, but preserving the original sector
weights and equilibrating each produces (1/2+9/10)/2=7/10. The global tilt
would need sector weights3/8 and5/8. This failure is retained explicitly.

Old histories and calibration records can be retained; they may change the
conditional sector weights and initial hidden law. Claiming joint preparation
with those records requires the corresponding conditional convergence premise.
The earlier finite-error preparation theorem remains available only at its
own actually acquired operation/adjoint/information interface.

## 9. Unknown binary source: exact Metropolis mobility and sharp cap

For the restricted symmetric two-state primitive with unknown iid flip
probability p, the integer protocol has

    K(A,B)=a_N(p)=1-(1-p)^N,
    K(B,A)=a_N(p)/N.                                (8)

Thus the ordinary two-state Metropolis kernel for ratio N is multiplied by
the unknown common mobility a_N. The expected calls are

    E_A tau=a_N/p,
    E_B tau=2-a_N/(Np).                             (9)

If p>=p_min>0, both are at most max(1/p_min,2), even though the hard cap N
may be large. A rare large budget is not the same as a typical long run.
For source B mode3, the supplied model gives p in[1/4,9/20], hence bound4.
In a network of frozen such sources, each local edge has a common unknown
mobility and the target Gibbs law is exactly invariant in every hidden vector.
No kinetic calibration is needed for that target law. The visible trajectories
remain hidden-dependent, so no exact predictive closure or full-record
independence is being asserted.

This separation can be exact and infinite dimensional. Draw a frozen p from
a distribution with positive density on a nontrivial interval inside(0,1),
and start the bit at its common invariant law Pr(B)=N/(N+1). The centered
label covariance after n compiled calls is its nonzero variance times

    integral lambda(p)^n dgamma(p),
    lambda(p)=(1+1/N)(1-p)^N-1/N.

lambda is strictly monotone. Every finite Hankel moment matrix of this
covariance sequence is positive definite: its quadratic form is the integral
of a nonzero polynomial in lambda squared, which cannot vanish on that
interval. Hence the compiled visible process has unbounded linear predictive
rank while the target invariant law is exact. The operation controls the
chosen equilibrium objective without eliminating predictive hidden memory.

For any randomized causal controller with1<=tau<=N such iid native calls,
the opposite-endpoint probability F(p) is a polynomial and

    F'(0)=E[tau on an all-no-flip path] in[1,N].      (10)

Indeed only single-flip paths contribute at order p. Every first flip along
the no-flip prefix remains an opposite physical output if no further flip
occurs, regardless of subsequent stopping decisions. Integrating independent
seeds gives (10). If two controllers have F_A(p)=r F_B(p) on an open physical
interval, polynomial identity extends this to0, implying1/N<=r<=N.
The integer protocol saturates r=N. Also F_A(p)<=1-(1-p)^N for every p,
because no flip among the first N calls cannot change the physical bit;
the high-direction rule saturates that pointwise upper bound.

This sharp cap result is only for a single unknown iid symmetric primitive
and a mandatory first call. It is not an impossibility theorem for the full
source-B menu: for example its native p_1=3p_0 already gives ratio3 in one
call. A genuine zero-call hold, an added initializer, or an unbounded stopping
time changes the feasible set. With hard cap N, the universal dimensionless
weight-bias budget for this single-source interface is at most log N.
Because this two-state family is a member of the general reversible class,
the same example proves sharpness of N for any proposed UNIVERSAL reweighting
compiler at the one-unknown-kernel interface with mandatory1..N calls. The
construction in Sections3--5 attains every r in[1,N] with the stated selectors.

## 10. What physical errors and finite acquisition can support

Unknown kinetics that preserve actual mu-reversibility and the selected local
support leave (7) exact. This permits calibration to optimize throughput among
structurally valid operations rather than to estimate every row to an error
that shrinks with service length. Exact structure is a premise, not something
the finite data has magically verified.

Sensing errors, missed transitions at the sampled endpoints, incompatible
latency, nonreversible native dynamics, drift during an excursion and crosstalk
can violate the construction. If an independent implementation contract gives
per-call coupling error e and the literal controller has at most N calls, a
first-error coupling bounds one compiled endpoint error by min(1,N e), plus
any separately budgeted selector/controller error. This finite-record bound
does not give a gap-independent stationary-observable guarantee. Small
nonconservative errors can select different phases; the complementary note
gives an exact example. There is no unacquired apparatus precision number.

If the implementation instead exactly realizes a coherent rounded energy
E_tilde with |E_tilde(y)-E(y)|<=epsilon*d (dimensionless), then

    |log Z_tilde-log Z|/d <= epsilon,
    D_KL(pi_tilde||pi)+D_KL(pi||pi_tilde) <= 2 epsilon*d. (11)

The first inequality follows by bounding exp[-(E_tilde-E)] pointwise. The
second is the difference of its expectations under the two Gibbs laws and
is bounded by the oscillation2epsilon*d. These are free-energy-density and
relative-entropy-density statements, not uniform magnetization accuracy at
phase coexistence, and not a claim that arbitrary row errors are energy errors.

## 11. Ordinary routes and scope of the candidate addition

A real protected hold plus state-dependent native calls gives standard
Metropolis/time-change control without this excursion construction. An extra
isolated spectator device can sometimes supply the logical hold by executing
operations on that spectator; it is a real extra device and isolation contract,
not forbidden by definition. Added initialization/replacement is likewise a
legitimate alternative at its actual cost.

In the binary frozen source, ordinary proposal/acceptance followed on rejection
by first return gives exact Metropolis mobility p, expected at most2 native
calls, and unbounded worst-case length. In the two-label reversible hidden
model, rejected excursions can also preserve detailed balance without restoring
the starting microstate. Trace/censored-chain theory explains that fact.
It is a strong incumbent and can be preferable to the bounded compiler.

The candidate addition is therefore specific: a positive, physically executed,
bounded-native-call reweighting kernel from a coarse reversible interface,
including arbitrary hidden memory, complete diagonal-block balance, exact
occupation/cost identities, local composition and a sharp single-source cap.
It separates target invariant-law control from predictive completeness and
from physical-time stationary holding. It establishes a mathematical capability,
not a demonstrated hardware advantage or an achieved civilisation-scale result.

