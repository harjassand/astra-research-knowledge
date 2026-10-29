# Directed transport without reconstructing hidden kinetics: completed alternative

29 October 2026. Same Astra P1 physical-mechanism role and allocation.

## Finding and scientific disposition

I constructed a finite-rate controller that turns an actual menu of reversible
pair modes into sustained directed transport, with a current direction and
stall determined by a prescribed cycle affinity rather than hidden kinetic
prefactors. Hidden state can evolve on every native transition and need not
reset. The record includes physical time, all observed native crossings, and
controller switches.

**The strong ordinary comparison defeats a broad novelty claim.** Tightly
coupled motors already supply the thermodynamic principle. On the same native
pair menu, ordinary fixed-pulse visible feedback already supplies an oriented
sequence of endpoint steps without learning kinetics. The constructed finite-
rate gate gives a concrete autonomous timing/energy contract; it is not a new
geometric pump, a new general directionality principle, or a demonstrated
improvement over the ordinary controller. I recommend preserving this as a
completed distinct construction and boundary, rather than selecting it as the
central foundational advance in its present form.

## The concrete operation

For visible stations i on a cycle, actual mode e_i permits only motion between
stations i and i+1, with arbitrary reversible hidden dynamics for a common mu.
The controller retains an active incident edge. At station i it changes the
incoming edge to the outgoing edge at rate gamma_i r_i and changes back at
rate gamma_i. The common factor gamma_i may itself be unknown. No infinitely
fast mode averaging or native holding operation is used.

For the full joint stationary process, all native-cut and controller-gate net
currents equal J and

    sigma = J log(prod_i r_i) >= 0.

If the actual microscopic graph admits a nonzero-winding closed walk, J has
the strict sign of log(prod r_i). Pair-mode irreducibility is one sufficient
supplier. An actual tightly coupled load that subtracts work W per turn has
stall W=sum_i Delta mu_i, provided the load's local detailed-balance interface
is independently supplied. Static equilibrium weights do not establish that
new load interface.

From an available baseline X~mu and a fresh fair incident-mode bit, the complete
observed record has an exact fixed-time reversal likelihood ratio equal to
the exponential of its recorded gate affinity. With a single driven gate of
ratio R this yields P(C=n)=R^n P(C=-n). It does not make first-passage cycle
times independent, and does not apply conditionally to arbitrary old records
that invalidate the initial baseline. Speed, fluctuations and full record
laws retain their hidden kinetic dependence.

## Two substantive obstructions found during construction

**A visible cycle need not close microscopically.** Four specimen states
a,1,2,b have visible labels 0,1,2,0. Reversible native modes connect only
a<->1, 1<->2, and 2<->b. With the same positive controller gates the full
eight-state graph is a connected tree. Its stationary law is unique, every
visible edge can be traversed, and every stationary current is exactly zero.
A single apparent visible turn has written its displacement into hidden
memory. Full joint irreducibility alone is insufficient for strict transport.

**An arbitrarily small leak can reverse the intended current.** On four states,
one fuel edge has rates k_01=R>1, k_10=1. All other rates are symmetric:
k_12=k_30=eta, k_13=k_20=epsilon, k_23=1. The useful cycle and a leaked cycle
traverse edge 2->3 in opposite directions through the same fuel edge. Exactly,

    J_23=(eta-epsilon)(p_1-p_0)/(eta+epsilon+2),
    p_1-p_0>0.

Thus any fixed positive leakage defeats direction when an unknown useful
bottleneck is slower. One chemical affinity alone does not ensure tight
coupling to the chosen physical current. A relative kinetic margin or a
structural exclusion of the adverse cycle is necessary.

The governing note proves a general version: with a fixed microscopic graph
and rate-ratio forces, the desired stationary current is nonnegative for every
choice of positive symmetric conductances exactly when every simple cycle's
affinity and desired-current increment have nonnegative product. The proof
uses established positive cycle-flow decomposition and a retained bad-unicycle
construction. It is not claimed as a new network-theory principle.

## Strong ordinary comparator and actual costs

Read station i, run its forward pair mode for a fixed Delta, and read again.
The physical net crossing during that pulse is exactly 0 or +1. Repeat on 0;
advance to the next forward edge on +1. Finite pair irreducibility gives a
positive per-device success floor, hence finite expected waiting, even with
persistent evolving hidden memory. No rate reconstruction or microscopic
rollback is needed. The boundary measurement/switching contract, or a real
hold that implements it, remains charged. A delayed unmodeled switch is not
silently granted.

For both constructions, uniform slowing of all native rates makes throughput
arbitrarily small without changing equilibrium laws, winding topology or gate
affinities. The finite-rate controller can incur arbitrarily many control/
record events per unit transport. Fuel, clocks, sensing, storage, actual gate
couplings and load mechanics all retain their real costs. No physical apparatus,
universal power bound, same-resource speedup or hidden-state preparation follows.

## Evidence preserved

* `FINITE_RATE_TRANSPORT_WITH_UNKNOWN_MEMORY.md`: governing construction,
  full proofs, complete record/energy scope, both exact obstructions, and the
  strong ordinary comparator.
* `PRIMARY_PREDECESSORS_AND_FAILED_ATTACKS.md`: exact primary links and actual
  read scopes, including no-pumping, quantized pumps, positive cycle theory,
  fluctuation relations, feedback ratchets and Haldane timing qualifications.
* `check_transport_supplier.py` and `TRANSPORT_SUPPLIER_CHECKS.json`: executed
  exact rational population checks. Ten twelve-state hidden-motor cases verify
  current equality, direction, stall and nonlumpability; seven uniformization
  depths verify the transient count identity; the hidden tree and three
  leakage cases preserve the failure mechanisms. These checks are not acquired
  kinetic data or experiments.

One checked hidden motor has J=0.02622783961281308 and sigma=J log 2. Scaling
only native rates by 1/100000 reduces J to 0.000001198906254212695. A leakage
1/1000 against useful rate 1/1000000 gives target current
-0.0000831806134494938 while the fuel current remains positive. The same
reversal persists at leakage 1/1000000 against useful rate 1/10^12. These
figures instantiate the proofs; they are not performance forecasts.

The primary searches changed the candidate before a novelty claim was made.
The remaining consequential opening would be an actual way to certify or
enforce microscopic winding/tight coupling with weaker controls and without
learning the hidden dynamics. That supplier has not been constructed here.
