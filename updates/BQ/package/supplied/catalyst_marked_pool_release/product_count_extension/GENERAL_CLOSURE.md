# Finite revealed-pool closure: theorem, proof, and scope

## Exact model class

Let there be `N` exchangeable particles with state space `S={1,...,q}`. At time
zero their states are iid with law `mu0`; the initial controller state `Z(0)`
is deterministic or independent of those particle states. While not in an
interaction, each particle evolves independently as a finite-state CTMC with
generator `Q(t)`. Let `Z(t)` be a finite-state controller. Between
interaction proposals it may have its own finite-state generator, provided
that generator does not depend on the unobserved particle states.

All interactions are driven by a state-independent, possibly inhomogeneous
Poisson proposal process of rate `Lambda(t)`, with finite mean
`A_T=integral_0^T Lambda(t) dt`. At a proposal, a rule depending only on time,
the current controller state, and retained finite bookkeeping selects at most
`r` particle labels, where `r` is fixed; selection is independent of particle
states and permutation-symmetric across exchangeable labels. The event kernel
can inspect the selected particles' states and `Z`,
then change `Z` and the states of only those selected particles; it may also
reject/no-op. Any finite memory of proposal marks is included in the controller
state. A selected label is permanently designated as revealed from
that point on, even after a no-op or if it later returns to its original
single-particle dynamics. Particles not yet revealed never affect the
controller or any other particle except by being selected at a proposal.
All event rates and kernels are known. The endpoint observation is a
probability-valued function of the controller and the aggregate particle
state counts (or a coarsening of these counts).

For simplicity this theorem uses one iid population. It also extends directly
to finitely many independently evolving exchangeable strata, each with its
own initial law, generator, and known population size; then one records one
revealed count vector per stratum. It does **not** apply to arbitrary
exchangeable-but-correlated initial laws or to an initial controller state
correlated with the pool unless that dependence is represented by a finite
latent variable and conditioned on explicitly.

State-dependent interaction hazards are included only when they admit the
specified state-independent proposal representation: sample labels first,
reveal them, and let the event kernel accept/reject based on the sampled
states. A model whose event rate or label selection depends on the uninspected
bulk without such a representation is outside the theorem.

## Theorem

Let `J_T` be the number of proposals by time `T`, so
`J_T ~ Poisson(A_T)`. Fix an integer reveal cap `K>=0`. Evolve exactly the
finite process consisting of the controller and the multiset of revealed
particle states, and kill a trajectory only when a proposal would create more
than `K` revealed labels. At time `T`, combine the revealed count vector with
an independent multinomial count vector
`Multinomial(N-m, p(T))`, where `m` is the number revealed and
`p(t)=mu0 U(0,t)` is the single-particle CTMC law. Then, for every endpoint
event `E` (including a joint event involving a controller state), the output
`L_K(E)` is a lower bound on the exact likelihood `L(E)` and

`0 <= L(E)-L_K(E) <= Pr(Poisson(A_T) >= floor(K/r)+1)`.

For `r=1`, this is the tail `Pr(Poisson(A_T)>K)`. At fixed `K,q,r` and fixed
controller-state set, the retained finite-state dimension is independent of
`N`; using a histogram of revealed states gives at most
`|Z| * binom(K+q,q)` states (before any additional exact pruning). The bound
is an absolute likelihood certificate. For a bounded endpoint weight
`g in [0,M]`, multiply the right-hand side by `M`.

If an event uses more than one particle, any selection-without-replacement
and symmetric update rule can still be represented on revealed-state
histograms, but it can create up to `r` new tags in one proposal. If particle
roles, species strata, or update kernels break the relevant permutation
symmetries, retain separate histograms/roles; finite dimension remains
independent of `N` only when the number of such classes is fixed.

## Proof

Condition on the complete proposal history, proposal marks, and the identities
and paths of all revealed labels. The rule for choosing labels is independent
of particle states. Therefore conditioning on which labels remain unrevealed
does not bias their iid initial states or independent CTMC paths. No
unrevealed particle has been updated or used in a controller transition.
Consequently, at every time `t`, the `N-m` unrevealed particles remain
conditionally iid with law `p(t)`. This law is independent of the retained
controller/revealed state once the revealed history has been fixed.

The process on the controller and revealed labels is Markov: the between-
proposal generator is finite because `Z` and `S` are finite; at a proposal,
selection probabilities for already-revealed labels are functions of their
tracked multiplicities and `N`; a newly selected label has state law `p(t)`.
Exchangeability lets us quotient label identities by a state histogram, with
the appropriate combinatorial selection weights. Killing only discards
trajectories that exceed the cap, so retained endpoint mass is a submeasure
of the exact endpoint law.

If the cap is ever exceeded, more than `K` distinct labels were revealed.
Each proposal reveals at most `r` new labels, hence this event implies
`r J_T > K`, equivalently
`J_T >= floor(K/r)+1`. Since `J_T` has the stated Poisson law, the omitted
probability is at most the theorem's tail. Any endpoint indicator is bounded
by one, so its omitted likelihood contribution is no larger than this
probability. Conditional on a retained endpoint state with `m` revealed
labels, the total endpoint count is the sum of the revealed histogram and an
independent multinomial histogram from the remaining `N-m` particles. This
gives the stated likelihood calculation and completes the proof.

## Important edge conditions

* If a proposal inspects a label but rejects, that label must still be
  revealed. Otherwise the rejection event can inform the algorithm about an
  untracked particle state and the untouched pool is no longer iid.
* If the controller can inspect an aggregate of all particles between
  proposals, the revealed subsystem is not closed.
* If selection is preferential by unobserved particle state, the selected
  state distribution must be explicitly captured by a valid proposal kernel;
  uniform selection is the model used in the current engine.
* If there are repeated observations on the same population, later likelihood
  factors condition the unrevealed pool. A one-terminal-count likelihood can
  be recomputed for independent/destructive snapshots, but this theorem alone
  is not a filter for repeated snapshots on one trajectory.
* A bound on the truncation tail does not certify floating-point ODE or
  matrix-exponential error. Those errors require a separate numerical
  enclosure.
* For conditional likelihoods such as `P(Y=y | B=b)`, this theorem directly
  certifies the joint numerator only. Ratio certification additionally needs
  a denominator enclosure separated from zero.

## What this establishes and what it does not

The proof provides a reusable exact closure for fixed-horizon endpoint
likelihoods when only a bounded-rate set of particle labels can influence a
finite controller. It explains why the complexity can be independent of a
large population size at fixed reveal cap, while making clear that the cap may
need to grow with interaction budget or rare-event accuracy.

This is not a priority claim. Its core pieces are standard: Poisson
uniformization / time-ordered event expansions, independent-particle
multinomial evolution, graphical constructions, and state-space truncation.
Even the likelihood interval itself is established for FSP: Fox, Neuert and
Munsky derive monotone lower and upper single-cell likelihood bounds by
reallocating the known FSP loss. The possible algorithmic contribution is
therefore the particular positive revealed-particle quotient and exact
untouched-pool endpoint marginalization for joint controller/population
observations, not a new likelihood-certificate principle. The targeted
search did not identify an exact statement of this entire combination, but
that absence is not established; a broader search of stochastic-process,
queueing, and chemical-kinetics literature could find it already known.

### Closest inspected primary literature

* N. M. van Dijk, S. P. J. van Brummelen, R. J. Boucherie, “Uniformization:
  Basics, extensions and applications,” *Performance Evaluation* 118 (2018),
  8–32. Uniformization represents finite-horizon CTMC evolution by a Poisson
  number of discrete steps and truncates the Poisson tail. DOI:
  <https://doi.org/10.1016/j.peva.2017.10.002>.
* Z. Fox, G. Neuert, B. Munsky, “Finite state projection based bounds to
  compare chemical master equation models using single-cell data,” *J. Chem.
  Phys.* 145 (2016), 074101. FSP yields monotone lower/upper data-likelihood
  bounds from its retained probability and known truncation loss; hence the
  present Poisson likelihood interval is not novel by itself. DOI:
  <https://doi.org/10.1063/1.4960505>; article:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4991991/>.
* E. Mjolsness, “Time-Ordered Product Expansions for Computational Stochastic
  Systems Biology,” *Physical Biology* 10 (2013), 035009. Uses event-ordered
  expansions for stochastic-network simulation and parameter inference. DOI:
  <https://doi.org/10.1088/1478-3975/10/3/035009>; preprint:
  <https://arxiv.org/abs/1209.5231>.
* T. Jahnke and W. Huisinga, “Solving the chemical master equation for
  monomolecular reaction systems analytically,” *J. Math. Biol.* 54 (2007),
  1–26. Independent monomolecular molecules have multinomial structure and
  arbitrary count distributions follow by convolution. DOI:
  <https://doi.org/10.1007/s00285-006-0034-x>.
* M. Reis, J. A. Kromer, E. Klipp, “General solution of the chemical master
  equation and modality of marginal distributions for hierarchic first-order
  reaction networks,” *J. Math. Biol.* 77 (2018), 377–419. It gives exact
  generating-function solutions for a hierarchic first-order class with
  deterministic/Poisson starts, including catalytic and splitting reactions.
  The present enzyme binding step `E+S -> ES` is bimolecular, not in that
  first-order hierarchy; the free-pool switching subsystem by itself is
  covered by monomolecular multinomial solutions. DOI:
  <https://doi.org/10.1007/s00285-018-1205-2>; article:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC6061068/>.
* R. Fernandez, P. A. Ferrari, N. L. Garcia, “Perfect simulation for
  interacting point processes, loss networks and Ising models,” *Stochastic
  Processes and their Applications* 102 (2002), 63–88. A marked-Poisson
  graphical construction with finite relevant ancestor sets; this is related
  conceptual prior art, although its problem is perfect stationary sampling,
  not this finite-time aggregate likelihood. DOI:
  <https://doi.org/10.1016/S0304-4149(02)00180-1>.

