# Independent result: what sustained physical-law control costs

29 October 2026. Same Astra P1 allocation; no additional workers or branch.

## Question chosen before root's preferred mechanism was disclosed

Can unknown baseline-stationary local operations maintain a desired physical
law at every ordinary clock boundary, rather than only at selected completion
epochs, without a protected hold or microscopic rollback?

## Constructive answer

For a uniform visible baseline and actual pair-preserving native operations,
the answer is controlled by the visible move graph G. For target visible law pi,

    delta_G(pi)=max_S [pi(S)-pi(N(S))].

There is a fully kinetic-independent controller with no extra preserving
operation exactly when delta=0. With an actual baseline-stationary operation
R preserving the visible label, delta is the exact minimum worst-case stationary
expected fraction of R use across the declared universal menu class. Particular
calibrated devices can do better. R need not freeze the full microscopic state.

A maximum flow in a bipartite double cover supplies symmetric edge allocations
f. Selecting edge e at label y with probability f_e/pi(y) makes the selected
full-state measure invariant under its unknown native operation. The remaining
selector mass goes to R. This proves the target on the complete microscopic
state, even with evolving hidden memory and nonreversible native kernels.

The lower bound uses a common-rate native witness and applies to all causal
feedback controllers, retained histories, internal memories and calibration.
For any independent set I, the finite-horizon preserving duty is at least
rho_T(I)-rho_T(N(I))-1/(pT). Thus a controller cannot evade the obstruction
merely by learning kinetics or using a nonreversible history policy.

There are two physical-time suppliers. Native invariant semigroups preserve
the target between fixed boundaries when the selection interface is compatible.
A complete finite-rate joint generator instead changes controller mode i to j
at rate gamma q_j(Y), while native mode i remains active. Its joint invariant
law is nu(dx)q_i(Y(x)). This avoids an instantaneous decision idealization as
mathematics; actual state-dependent rates and coupling remain a physical task.

## Consequence and scalable family

For any minimum-distance-two binary code given desired valid-code mass at least
1-epsilon, individual-bit actuation requires preserving duty at least
1-2epsilon in the common-rate witness. For every perfect Hamming code of length
d=2^r-1, weighting codewords by B>=d and other labels by one attains that bound:

    valid-code mass=B/(B+d),   preserving duty=(B-d)/(B+d).

The controller uses a syndrome read rather than an exponential flow table.
When B is a power of two its selector uses a bounded number of fair bits.
No new code is claimed. The construction does not protect against uncontrolled
errors on inactive bits, and an actual R could simply be applied continually.
The rigorous consequence is a physical activity-budget theorem, not an improved
memory device or a preparation theorem.

## Strong incumbents and novelty limit

Ordinary prechoice Metropolis with a real R is already a valid unknown-kinetics
controller. Conventional flow optimization can achieve the exact same optimum.
Suwa–Todo's 2010 probability-flow construction gives the complete-graph minimum
rejection max(0,2 max pi-1); directed-loop equations and Edwards–Sokal auxiliary
models are further close predecessors. Flow allocation, rejection minimization,
and data augmentation are established machinery.

The surviving contribution is the complete-state physical-interface reduction,
the arbitrary-history lower bound, and a finite-rate supplier specifying what
must be physically available. This is a substantive independent intermediate;
it has not established a major foundational advance or practical superiority.
The root's exact-preparation direction remains the stronger candidate for the
next central consequence.

## Saved proof and executed checks

- `FIXED_CLOCK_ACTUATION_COMPATIBILITY.md`: governing construction, proofs,
  all-time supplier, code family, costs and limitations.
- `PRIMARY_COMPARISON_AND_FAILURES.md`: exact primary links, actual read scopes,
  strong incumbents and failed stronger interpretations.
- `check_actuation_compatibility.py`: exact standard-library population checker.
- `ACTUATION_COMPATIBILITY_CHECKS.json`: successful execution.

Six graph cases agree with exhaustive cut deficiency. Two full hidden-kernel
cases verify microscopic stationarity/reversibility and a 64-state finite-rate
controller. Perfect-code formulas are executed at lengths 3 and 7. For the
three-bit code with weight 16, ordinary prechoice Metropolis has preserving
duty 15/19 and the conventional graph optimum 13/19. These are mathematical
checks, not acquired transition data or apparatus measurements.
