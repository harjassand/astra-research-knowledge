# Productive repair capacity, finite stock, energy and support

The independent [repair construction](package/independent/physical_repair_companion.md), [saved checks](package/independent/physical_repair_companion_results.json), and governing [main report](package/report.tex) give an attained resource boundary in a declared continuous-time machine-repair model. This companion is not a proved physical realization of the [finite-cycle control model](README.md). Classical machine interference, queueing, monotone comparison and birth-death exit formulas are credited; no new repair mechanism or historical priority is claimed.

## Useful operation and the full allocation optimum

With N modules and k failed, useful output flows at `nu(N-k)`. Each healthy module fails at hazard lambda. There are c_N repair channels of completion hazard mu, with at most one channel per failed module. Service fails at m<N failures. Single-module jumps, unchanged post-repair characteristics, exponential service and immediate dispatch are substantive premises. Setup/detection delays, aging, induced failure, shared catastrophe or degraded output cannot silently be folded into a rate.

A work-conserving policy attains downward intensity `mu min(k,c_N)`. Coupling orders its damage count below every permitted causal randomized allocation, so it stochastically maximizes both service time and completed useful work. Homogeneous components make repair labels immaterial. A history-dependent actual system inherits envelope guarantees if its failure intensity is conditionally at most `lambda(N-k)` and its realizable repair completion intensity at least `mu min(k,c_N)`. These are history-uniform conditional bounds, not empirical average rates.

## Exact finite means and the strict capacity boundary

Let `b_k=lambda(N-k)`, `w0=1` and

```text
w_k=product_(j=1)^k lambda(N-j+1)/[mu min(j,c_N)].
H_i=E_i tau_m=sum_(k=i)^(m-1) [sum_(j=0)^k w_j]/(b_k w_k),
G_i=E_i W=sum_(k=i)^(m-1) [sum_(j=0)^k w_j nu(N-j)]/(b_k w_k).
```

These give every safe-start mean in O(N) arithmetic and memory using log weights/prefix sums; numerical precision and actual service are additional costs. If R_N is the ratio of the largest safe weight to w_(m-1),

```text
R_N/b_(m-1)<=H_i<=m(m+1)R_N/[2b_(m-1)],
nu(N-m+1)H_i<=G_i<=nu N H_i.
```

Thus all safe starts have the same exponential mean scale, without a small immediate failure-risk promise adjacent to failure. A separate stationary-coupling bound certifies a finite mission from a paid all-healthy start; stationarity is an analytical comparison, not physical equilibrium preparation.

For `m/N->b in (0,1)`, `c_N/N->s>0`, fixed positive rates, rho=1-b and fluid zero `x_star` solving `lambda(1-x)=mu min(x,s)`, the mean log scale is

```text
V(b,s)=integral_(x_star)^b log[mu min(x,s)/(lambda(1-x))]dx
       if b>x_star, and zero otherwise.
log H_i=log R_N+O(log N),     log R_N=N V+o(N).
```

The general convergent capacity sequence gives o(N), not an unconditional O(1) remainder. A positive exponential useful-work scale occurs exactly when both `mu b>lambda rho` and `mu s>lambda rho`. One condition concerns per-module repair speed, the other installed capacity; buying channels cannot fix inadequate individual speed.

The closed saturated expression `V=c/lambda-rho-rho log[c/(lambda rho)]`, c=mu s, requires `b>x_star>=s`. It must not be applied outside that interval. At critical equality the exponent is zero. The proposed near-critical evidence scaling was not promoted to a theorem: startup relaxation and finite-size prefactors remain unresolved. The exact finite sums remain available. These asymptotic qualifications were corrected and checked in the final audit.

## Exponential endurance pays exponential total upkeep

Let R_T count completed repairs. For initial count k0, failure-count compensators give

```text
E W_T=(nu/lambda)[E R_T+E K_T-k0].
```

At service failure K_T=m. If at most B repairs are available before operation proceeds to failure, every policy satisfies `E W<=(nu/lambda)(B+m-k0)`. Where each completed repair actually costs energy e>0,

```text
E E_repair=(e lambda/nu)E W-e(m-k0).
```

This uses an actual cost contract rather than an invented universal reset energy. A reusable repair mechanism does not automatically consume a fresh material part each event, but still needs operating energy and lifetime accounted. Exponential mean work requires exponential expected repair throughput and, with positive actual repair costs, exponential total resources. Instantaneous hardware and power can remain linear in N. Power and total energy are distinct quantities.

For repair-energy price chi, work-conserving allocation also maximizes net expected utility when `1-chi e lambda/nu>0` at fixed installed capacity and the stated cost model. Standby costs, hard fuel and changing installed capacity require their own design problem.

An independent indispensable support failure hazard kappa gives `E tau_physical<=1/kappa` and `E W_physical<=nu N/kappa`. Constant failure risk in power, cooling, routing or dispatch destroys an exponential physical service claim. If support hazard itself has exponent gamma, the protected mean exponent is min(V,gamma) under the stated independence and sufficient-resource premises. The repair theorem does not supply that protection hardware.

## Acquisition, deployment and retained checks

Homogeneous local rate assays need order `eta^-2 log(1/delta)` paired healthy/repair dwell intervals, with expected physical exposure proportional to `1/lambda+1/mu` per pair. Tiny individual failure rates retain their waiting cost. Transfer from test modules, load dependence and future conditional envelopes require justification; heterogeneous types need coverage. All-healthy preparation requires real inspection/reset, not an equilibrium sampler.

Pooled implementation pays O(N) status/queue memory and O(N) event throughput at fixed rates, plus actual transport distance, dispatch, sensing and setup latency. Autonomous local channels remove shared scheduling only by buying their own hardware. Systematic timing/missed events do not average away. Calibration can be reused only within its declared validity interval; exponential-duration maintenance may itself require exponentially many ordinary recalibration cycles.

The supplied program checked exact Green sums against finite-generator solves, all 54 staffing policies in a finite example, finite-horizon survival and capacity examples from N=100 through 1600. These computations support finite algebra and illustrate the theorem; they do not validate a physical contract. Capital published the saved code/results without rerunning them.
