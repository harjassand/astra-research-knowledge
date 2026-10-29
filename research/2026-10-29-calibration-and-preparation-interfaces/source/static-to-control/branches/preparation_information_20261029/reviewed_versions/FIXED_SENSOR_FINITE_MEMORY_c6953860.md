# Controlled prediction with explicitly acquired finite memory

29 October 2026. New root theorem extending bounded Markov intervention
closure. Ordinary proof below; new load-bearing uses await independent review.
The purpose is to specify the information entering a controller's memory,
rather than declaring every memoryless controller sufficient or every
controller with memory outside the theory.

## 1. The experimental interface

Keep the native kinetic source class, fixed bath, force ceilings A,B, complete
coordinates and finite T of BOUNDED_MARKOV_FORCE_INTERVENTIONS.md. Fix:

* a finite schedule 0<t_1<...<t_m<T;
* finite report alphabets A_1,...,A_m;
* at each scheduled time and each preceding report history h, a specified
  noninvasive sensor kernel K_(ell,h)(a|omega_[0,t_ell]);
* identical controller initialization, independent of the physical source.

The kernels are bounded measurable probabilities, nonanticipating and FIXED
as source and candidate vary. They may use the complete past path in their
mathematical specification; their actual sensing/computation must be warranted.
This theorem does not implement an ideal kernel. A fixed finite catalog
selected by report history also qualifies. Variable increasingly resolving
sensor kernels do not belong to this interface merely because their output
alphabet is finite. Unreported acquisition apparatus memory must be included
if it changes future kernels or actuation.

Let t_0=0,t_(m+1)=T. On [t_ell,t_(ell+1)), a program applies an arbitrary
Borel force u_h(t,q,p), bounded by B, where h is the report history available
at that time. Each u_h acts through the directly noisy momentum force port.
Programs can vary over ALL such branch fields. The same selected program
and sensor kernels are used on source and candidate. Exact actuation command
values, if reported, need their own fixed observation-resolution contract.

Let J_F^program be the joint law of physical path and all sensor reports,
starting from the source's baseline stationary state. Let J_U^program be
the corresponding law starting from the candidate's baseline Gibbs state.

## 2. One explanation for the whole finite-memory interface

There is one smooth Gibbs potential U, with |grad U|<=A, such that

    sup_(F: sigma(F)<=s, |F|<=A)
       inf_U sup_program d_BL(J_F^program,J_U^program) ->0,
                                                  s->0.        (1)

Here joint-path distance combines the bounded uniform physical path metric
with the discrete distance on the finite report transcript. The same U works
for every admitted branch-control program. The conclusion also holds for
each finite Wasserstein order of physical paths and in TV for the COMPLETE
finite sensor transcript. Further fixed record kernels satisfying the bounded-
density or countable-output conditions inherit output TV convergence.

The static-information selection corollary persists: ANY sequence of
bounded-gradient Gibbs candidates whose complete baseline position laws
fit low-entropy source position laws weakly works uniformly across this
same interface. No new candidate is fitted after each report.

## 3. A common reference includes the actual sensor randomness

Let R_0 be the joint law obtained by running stationary FREE Kramers motion
and applying exactly the fixed kernels at the specified times. Independent
auxiliary random variables can implement each kernel at its scheduled time.
The reference's physical-path marginal is the free path law P_0. The
Brownian motion remains Brownian in the causal filtration enlarged by these
independent sensor draws and the reports already produced.

For a varying sequence of source forces and branch fields, use the preceding
baseline proof's approximately stationary L2 densities r_j relative to mu_0.
The joint controlled law from r_j mu_0 has density relative to R_0

    R_j=r_j(Z_0) exp{int theta_j dW-(1/2)int |theta_j|^2 dt},
    theta_j=[F_j(q)+u_(j,H_t)(t,Z_t)]/sqrt(2gamma tau).           (2)

H_t is the report history available at t, held constant between scheduled
observations. The integrand is adapted and bounded. Conditional exponential-
martingale estimates give

    ||R_j||_L2(R_0)^2
       <=exp[(A+B)^2 T/(2gamma tau)] ||r_j||_L2(mu_0)^2.         (3)

This is a density on JOINT path/report space, not an assumption that the
reported history is independent of the physical state. The observation
kernels keep their causal conditional laws after this adapted change of
measure. Equivalently, concatenate native transition laws and sensor draws
chronologically to construct the same joint experiment.

## 4. Identifying the limit without erasing report memory

There are finitely many history nodes. Extract a common subsequence on
which every u_(j,h) converges weak-* in L_infinity(dt mu_0), with the same
bound B, and F_j converges to the baseline Gibbs force F. Extract a weak
L2 limit of (2). It defines SETWISE convergence of the joint laws.

In a smooth compact-momentum martingale test, a moving-control error on a
single node h of level ell is

    1_{H_(t_ell)=h} int_(t_ell)^(t_(ell+1))
                  [u_(j,h)-u_h](t,Z_t).grad_p phi(Z_t) dt.      (4)

Its L2(R_0) norm is at most the L2(P_0) norm of the occupation integral
without the indicator, since the indicator is bounded by one and the
physical reference marginal is P_0. The full-state compact occupation
lemma makes that norm tend to zero. The same works on any fixed truncated
test interval. Sum over the FINITE nodes. Bounded past multipliers are
handled by Cauchy--Schwarz and (3).

All other martingale terms are fixed bounded measurable joint functionals.
The prescribed sensor conditional identities also pass to the limit: for
any bounded pre-observation test chi, each identity

    E[chi {1_(A_ell=a)-K_(ell,Hprev)(a|past_path)}]=0             (5)

has a fixed bounded measurable integrand. The limit therefore retains both
the correct controlled native generator on every branch AND the declared
sensor operations. Piecewise bounded Girsanov uniqueness, followed by each
fixed conditional sensor draw, identifies a unique joint law inductively.

Initial TV approximation propagates through this complete causal experiment.
Thus the true stationary starts have the same joint limit. For the Gibbs
candidate sequence constructed from the baseline limit, or selected by the
static position-fit corollary, apply the SAME varying branch program. The
candidate joint laws converge setwise to exactly the same limit.

If (1) failed, choose allegedly separating branch programs after the one
candidate sequence. Extract their finitely many fields as above. Common
limits contradict separation. This verifies inf_U sup_program.

Finite transcript TV follows by summing its converging probabilities.
Fixed additional records follow by the same Scheffe argument as before.
Controlled momentum moment estimates use only the force ceiling A+B and
remain valid for this adapted force, so finite Wasserstein consequences
follow by the same moment interpolation. Finite-dimensional bounded
controller memory is NOT silently assumed to have its own thermal bath.

## 5. What this says about the memory obstruction

The theorem allows actual retained information and adaptive decisions.
Its uniformity comes from a fixed FINITE sensing schedule/catalog and a
finite report tree, while each branch's force can vary arbitrarily within
the Markov amplitude bound. The proof does not cover a number of reports
that diverges as entropy decreases, a growing alphabet, changing exact-path
tests, arbitrary stopping-time acquisition, or an unmodeled apparatus state.
Those are distinct interfaces requiring additional arguments.

A single bit obtained by a sequence of progressively finer native path tests
can violate the broader replacement claim, even though its stored alphabet
is smaller than the finite trees covered here. Its acquisition operation is
not fixed. The one-bit reporter construction in causal_frontier makes that
distinction operational with a bounded later force and a noisy final readout.

For a fixed finite experiment, the number of nodes can grow exponentially
in the report depth. The theorem is qualitative and has no algorithmic
enumeration advantage or effective entropy-to-response modulus. It does not
turn arbitrary noncomputable Borel protocols into numerical simulators.
Actual sensor, preparation, actuation and solver precision remain charged.
Its content is that an equilibrium explanation selected BEFORE feedback
can remain valid for a whole explicitly acquired-memory experiment class.
