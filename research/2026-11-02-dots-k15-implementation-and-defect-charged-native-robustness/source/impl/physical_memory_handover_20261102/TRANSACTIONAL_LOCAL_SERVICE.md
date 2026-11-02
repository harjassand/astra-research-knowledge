# Protected waiting and finite transactional service: a concrete partial compiler

2 November 2026. This supplies finite physical-time lemmas, not a completed autonomous-QCA threshold. It is the harder continuation after the native Gibbs-loading approach remained open.

## 1. Two tests any synchronizer reduction must pass

### Shared stalls are not independent local faults

Let k payloads share one service delay T~Exp(1), and let independent noise clocks of rate p run on each payload. The event that each payload faults before service has probability

  E[(1-exp(-pT))^k] = k! p^k / product_(j=1)^k(1+j p).

For fixed p and large k this has a polynomial, not exponential-in-k, tail. A uniform marginal service-time bound therefore does not yield a uniform successful-gate fault-set bound. Bounded service neighborhoods only help if the number of payloads sharing a delay remains bounded at the *same protection level*.

### Finite patches do not by themselves remove clock winding

On a ring of length divisible by q, the field kappa_i=i mod q has locally valid nearest-neighbor differences. Every site nevertheless waits on its predecessor if advancing may not create lag 2. Every patch smaller than q/2 admits a valid integer lift. Thus separate local liftability is not an inter-patch liveness proof. A finite fault island from a correct initial state is a different question; this example is not a threshold counterexample.

## 2. Quantum-safe protected waiting

Use encoded gate teleportation, not a destructive global release. A prepared encoded Choi resource supplies a requested gate. Endpoint Bell measurements commute across subblocks, so they need not finish simultaneously.

- Before input consumption, a resource timeout may discard/reset the known-state factory without touching the input.
- Once an input subblock has been Bell-measured, the unknown information has moved to an output-resource subblock. Never roll this back by discarding the resource. Commit forward.
- Both unconsumed source subblocks and transferred output subblocks keep their *own inner EC* running. The outer encoded wire temporarily spans both locations.
- Store each consumed/ownership bit and each Pauli result with the same protection level as the corresponding payload. An unencoded flag is not allowed to trigger a logical gate or overwrite an output.
- A slow outer peer may prevent an outer logical operation from completing; it must not suspend an inner correction cycle.

This is a genuine quantum operation: no unknown state is copied. The ideal Bell identities hold reference-safely. The remaining controller problem is reliable execution and reconciliation of the encoded records, not preservation of a bare qubit while waiting.

## 3. Finite transactional local module

Fix once and for all a module support of at most b neighboring cells and a finite primitive channel. Its ideal Stinespring implementation is a known finite sequence U_1,...,U_d on payload plus local workspace; all discards, measurements with forgotten outcomes, and destructive resets can be postponed to commit. Workspace initialization may occur at acquisition, since it does not overwrite payload. b,d, workspace dimension and interaction radius are constants, possibly very large.

The module has finite classical registers: request/epoch, acquired flag, a prefix index j in {0,...,d}, forward/abort mode, and output/consumed record. **Durable last-commit epoch, consumed flag, and output/measurement record are payload-level state, not resettable workspace.** An abort or clearing word never changes these durable registers. Acquisition requires a present request whose epoch is not already durably committed; commit updates the durable epoch and output atomically. A completed transaction is never reversed merely because a damaged volatile prefix index is nonzero. Resource locks have owner labels drawn only from the fixed finite set of neighboring modules eligible to touch that resource.

Ideal attempted updates are local CPTP maps, driven by independent Poisson clocks with rates bounded above and below by positive constants:

1. **Acquire-all.** Acquire the entire required footprint atomically or acquire nothing. There is no hold-and-wait.
2. **Forward.** If all ownership labels match, apply U_(j+1) and increment j in the same update.
3. **Abort.** Enter reverse mode from the recorded j. In a clean execution, apply U_j†,...,U_1† and return the input exactly, including its reference entanglement.
4. **Ownership-loss repair.** Before any reverse action, check ownership. If it no longer matches, do not act quantumly on the foreign payload. Skip the remaining rollback and clear local bookkeeping. Only locks carrying this module's own label are released.
5. **Commit.** At j=d, perform the required local discards/resets and update the consumed/output/epoch record atomically. The completed request cannot fire again unless the caller supplies the next valid request.
6. **Repair of orphaned locks.** Every module's abort/reset path scans its fixed eligible footprint and releases locks bearing its own label, even if its local ledger says idle. No external acknowledgement is needed to finish abort.

A corrupted ledger may cause a wrong inverse or a skipped operation. That is a bounded-module quantum fault, not a benign abort. It must be charged to its initiating fault and repaired at the next protection level. Honest aborts are exactly identity/delay channels on the payload.

This specification does not claim that an arbitrary corrupt global epoch state represents a meaningful computation. Causal correctness is asserted only on valid request/ownership states. The repair guarantee from arbitrary ledger states is local availability, with possibly corrupted local payload.

## 4. Uniform private service certificate

Consider a fixed requested module whose input is ready. Include the finitely many competing owner modules that can hold one of its resources. Let K bound their number. Because abort never waits for outside resources, there is a finite word of attempted updates that:

- puts every competing module in abort mode;
- executes at most d bounded reverse/clear steps per competitor;
- releases every eligible ownership label;
- acquires the requested footprint;
- executes its d forward steps and commits.

Suppress all other attempts in the finite conflict neighborhood while this word runs. A false guard is harmless during clearing; the ownership scan handles orphaned labels. On a valid request state, the result is exactly the requested channel, with honest aborted competitors restored. On a damaged request state, this certifies eventual local availability only, not restoration of lost quantum information or validation of its epoch. An already-committed request is acknowledged as service-ready without being reissued; the clearing word cannot legitimately authorize a repeated irreversible action. Only a fresh valid request receives the requested-channel guarantee.

Let the word contain ell attempted events, let Lambda bound the total competing attempt rate, and gamma_min the smallest prescribed event rate. Divide a duration tau=ell delta into ell subintervals and require exactly the prescribed attempt in each. Its probability is at least

  v = (gamma_min delta exp(-Lambda delta))^ell > 0.

All parameters are independent of system size. Taking delta=1/Lambda gives v >= [gamma_min/(e Lambda)]^ell. Repeating m disjoint trials yields a conditional availability-failure bound (1-v)^m. This remains true despite arbitrary previous ledger/lock states because the clearing word does not rely on an unproved communicating-class assumption.

This closes a private finite-module service lemma. It does NOT establish global token causality or prove that a logical request's input is ready. Those are precisely the interfaces that must remain encoded and cannot become an unprotected master scheduler.

## 5. Physical-time fault-set lemma for imperfect local contacts

Partition physical space-time into fixed-duration bins of length tau. Assign each bounded-local generator term to a unique spatial owner. Suppose each ideal local term L_a and implemented local term L_a+Delta_a is a valid Lindblad generator and ||Delta_a||_diamond<=epsilon_a. The perturbation may include faulty correction/reset contacts, not only added unitary jumps. A coherent local V contributes Delta=-i[V, .], with norm at most 2||V||.

For a finite set F of marked bins, define the fault-set contribution by the mixed finite difference: all unmarked terms remain actual, and in each marked bin toggle its perturbation between zero and full strength. The alternating sum is the sum of fault paths having at least one perturbation insertion in every marked bin.

Interpolate independently by lambda_b in [0,1]. Each intermediate local term is a convex combination of two valid Lindblad generators, so every propagator between insertions is CPTP and has diamond norm one. Repeated Duhamel differentiation inserts one Delta_b at an arbitrary time in each marked bin. Summing the time orderings integrates the full product of the time intervals; there is no factorial or total-system-volume factor. Therefore

  ||E(F)||_diamond <= product_(b in F) integral_b ||Delta_b(t)||_diamond dt
                  <= (epsilon tau)^|F|,                       (1)

when each marked bin's assigned total perturbation strength is bounded by epsilon. Overlapping physical supports do not invalidate (1); their bounded spread is charged in the later geometric/gadget analysis. The lemma is Markovian at the declared enlarged-system level. It does not automatically cover arbitrary non-Markovian elimination errors of a microscopic bath.

This is a physical-time statement. Random service delays must not be hidden by replacing tau with an uncontrolled successful-gate waiting time.

## 6. Combining service failures and contact faults without a shared-stall fiction

There is a useful direct graphical version for a Poisson-channel implementation. Let each actual attempt channel differ from its ideal CPTP channel by at most epsilon_g in diamond norm. Add a bounded-local coherent generator of strength v. Choose a fixed time box containing m service trials.

Also declare a box bad if its finite conflict neighborhood has more than J attempted events. J is a fixed constant chosen large enough that this overflow probability is small. On a non-overflow record, the total local channel-fault weight in a box is bounded by

  a = J epsilon_g + 2 v tau,

or by exp(a)-1 when summing all nonempty fault subsets. This bound is uniform over the actual attempt record and all quantum/control states. Honest aborts are included in the ideal channels and cost no fault weight.

The event that no service certificate occurs, or that an overflow occurs, depends only on independent Poisson attempt records in a bounded neighborhood. For a family of boxes, extract a disjoint subfamily of size at least |F|/R, where R is the fixed overlap degree. Their joint schedule-failure probability is at most r^(|F|/R).

Mixed schedule/noise contributions can therefore be charged by a fixed-strength physical-box noise parameter of the form

  eta_box <= C [exp(a)-1 + r^(1/R)],                           (2)

with fixed geometry factors. One partitions each required bad box according to whether it contains a schedule failure or a contact/coherent fault; conditional contact bounds are uniform on non-overflow records. First choose finite m,J to make r small, then choose fixed contact/coherent strengths small enough to make a small. None of these choices scales with total system size.

Equation (2) is a concrete finite-time fault-set lemma for PRIVATE transactional modules. It does not say their asynchronous completion history is already the synchronous QCA of arxiv2601.20818v3. A separate causal/encoded-controller theorem must connect the boxes to valid extended rectangles or to a direct stall-cluster damage geometry.

## 7. Physical resource ledger

The ideal update channels include finite workspace resets. A finite-purity reset is a noisy local CPTP operation, not a perfect state preparation. For example, an implemented update Phi_tilde=(1-p)Phi+p Xi gives exactly

  gamma(Phi_tilde-id)
    = gamma(1-p)(Phi-id) + gamma p(Xi-id).

This admits arbitrary CPTP Xi, not only unitary error jumps. Generic coherent implementation errors are covered instead by the norm bound in (1), not by inventing a convex stochastic interpretation.

A finite-temperature reset service can have a fixed impurity below threshold using fixed local gap/temperature. It consumes ongoing entropy-removal capacity. At fixed attempt rate per cell, total service throughput and heat/work budget scale extensively with the number of active cells and with physical hold time. No autonomous scheme may label this cost zero merely because the generator is time-independent.

Constant-duration physical contacts can cause overlapping-contact errors. Their finite-rate/finite-duration collision implementation and a uniform local error bound must be supplied; an instantaneous CPTP jump is the declared effective model, not a microscopic implementation proof. Atomic acquire/commit acts on a fixed but potentially large support. Compiling it to strictly two-body finite-range hardware with noisy intermediates is another finite-gadget obligation, not a freely perfect operation.

## 8. Remaining decisive join

The private-service mechanism avoids the unconditional global-clock claim. It still needs a compositional autonomous executor with:

- encoded request, epoch, consumed and Pauli records;
- no physical flag capable of broadcasting an uncharged logical operation;
- unambiguous ownership through partial Bell transfers;
- inner EC that never waits for outer payload readiness;
- a proof that invalid records and delayed repair have bounded damage/explanation witnesses;
- a readout decoder for actual asynchronous cuts, rather than pretending every physical instant is a synchronous circuit layer.

The proven discrete-time noisy-controller construction is the appropriate baseline to reuse. Its continuous-time outline cannot be promoted by (1) alone. A global winding/slope configuration lies outside a properly initialized finite-fault basin but disproves a state-uniform shared-clock service assertion. A direct damage/explanation-path theorem may be the correct completion rather than successful-gate local-noise domination.

A completed architecture would be a nonequilibrium autonomous fault-tolerant memory/computer, not an equilibrium native-H passive material. The active comparator gets all its local dissipators, reset power, controllers, ancilla volume and gates; autonomy can remove external scheduling, not create a free reliability or energy advantage.

## 9. Gamma-cycle moment and ownership conditions

For a q-tick private cycle with unconditional rate-gamma advancement, tau~Gamma(q,gamma). For integer R>=1 and R epsilon<gamma,

  E[(exp(epsilon tau)-1)^R]
    = sum_(j=0)^R (-1)^(R-j) binom(R,j)
                          [gamma/(gamma-j epsilon)]^q,

and the stable upper bound

  E[(exp(epsilon tau)-1)^R]
    <= epsilon^R (q)_R gamma^q/(gamma-R epsilon)^(q+R)

follows from exp(x)-1<=x exp(x). Thus its Rth root is O_(q,R)(epsilon/gamma) when R epsilon<=gamma/2.

If each service interval is a function of independent primitive clock increments and every increment is read by at most R intervals, Finner's inequality yields a product fault-moment bound with that constant. One must also forbid postselection of service intervals: selecting the longest among many revealed cycles violates the intended conclusion even with formal overlap one. Membership/ownership must be fixed or predictably committed before the relevant future increments are exposed, and unsuccessful attempts must stay in the accounting.

A candidate enforceable discipline is one outstanding transaction per fixed-degree port, rendezvous only at private-EC epoch boundaries, and preassigned leading/trailing sharing. Each primitive epoch then serves its owner plus at most one outstanding request per port. This is a local ownership construction, not a proof that an arbitrary hierarchical executor already obeys it. Adaptive recursive DAGs require an explicit predictable exposure argument, not an unqualified appeal to Finner.

## 10. Why the commit bit must already be encoded

If an unknown state has been destructively Bell-teleported but its logical outcome bit is stored only in one raw physical bit, a fault erasing that bit merges two possible outputs rho and Z rho Z. No input-independent recovery can be correct on both histories for every unknown input/reference. With equally likely outcomes the resulting unrecorded channel is (rho+Z rho Z)/2, complete phase dephasing. Preparing a protected record only afterward does not repair the loss.

Therefore the logical Bell outcome must emerge from the FT measurement as a distributed encoded classical record. Raw outcome records may be discarded only after that protected record exists. Similarly, a consumed flag must not be a bare physical switch authorizing a logical overwrite. This is a necessary operation-level condition, not mere bookkeeping preference.


## 11. Durable-record repair and finite-state check

The earlier 432-state executable check modeled only locks, mode and prefix index. It did **not** test irreversible commit retention and must not be cited for replay safety. The expanded `transaction_durable_check.py` enumerates 46,656 states including durable last-commit epochs, output records, active transaction epochs, and present/absent requests. It verifies:

- all volatile locks and prefixes become available without changing either module's durable records;
- 15,552 fresh request cases commit exactly once;
- 31,104 already-committed or absent request cases are not reissued;
- a repeated full clearing/service word cannot replay any of these requests;
- clean-prefix rollback restores the exact unitary to numerical error below 2.5e-16.

Only the local one-outstanding-port discipline is tested. Two-state alternating epochs are not a proof about global wraparound or delayed stale packets. Most importantly, the persistent record must be encoded at the payload's protection level before any raw outcome is discarded. The script does not turn that record into a trusted noiseless bit; record corruption remains a charged local fault, and its hierarchical consequences still require the protected executor.
