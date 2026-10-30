# Separate audit: global aggregate-comparability corollary

Reviewer: finite_phase_drift_challenge, 2026-10-30. Internal mathematical review. Scope: appended Section 6 of ROBUST_PHASE_INFINITE_FIBER_LIFT.md.

## Verdict and necessary precision

The global corollary passes for a TIME-HOMOGENEOUS physical CTMC with finite per-state total jump rates, finitely many species, a genuinely finite closed phase alphabet, the fixed finite weakly reversible projected graph, and the stated global aggregate comparability outside a finite total-count set. These standard CTMC/species assumptions should be explicit. Earlier sections permit time-dependent coefficients for a pointwise generator inequality; stationary distributions and positive recurrence in the present sense do not follow for arbitrary time-inhomogeneous coefficients.

This is a genuine restricted global theorem. Source-completeness is a substantial sufficient condition, not a consequence of weak reversibility and not a solution of general chemical recurrence.

## 1. Norm-likeness and nonexplosion

On a nonneutral projected component, the previously audited function has

    V(N,j)=Gamma(N+beta_j+1)^alpha v_j(N+beta_j),

where v_j has positive polynomial/Puiseux upper and lower growth. After a positive finite-head extension, V tends to infinity with N. Because N is the total count of all finitely many unbounded species and the phase alphabet is finite, every bounded-N physical set is finite. Thus V is genuinely norm-like on the physical state space, not merely on its projection.

Invisible internal transitions contribute zero. The earned generator inequality holds outside a finite physical set, and the generator is finite on that set under the finite-rate, finite-channel/projected-jump assumptions. Hence LV is bounded above globally. The stopped norm-like Foster argument proves nonexplosion of the minimal CTMC. There is no hidden assumption that internal fibers mix; their finiteness and the norm-like bound are the relevant facts.

## 2. Closed-class recurrence and moments

On every closed irreducible infinite physical class in a nonneutral projected component, the drift is bounded above by a negative constant outside a finite set. The standard stopped hitting/regeneration argument gives positive recurrence. A closed class cannot avoid the finite set indefinitely: stopping the negative-drift inequality would otherwise bound an infinite expected elapsed time by a finite initial V value.

The stronger integrand is

    f(N,j)=Gamma(N+beta_j+1)^alpha.

Stopped Dynkin along return cycles bounds the expected integral of f by the initial finite V value plus a finite-head occupation contribution. Positive recurrence makes that occupation contribution integrable. Regenerative normalization then gives stationary pi(f)<infinity. This does not presume pi(V)<infinity or illegitimately integrate an unbounded generator against pi.

For every fixed s>0, exp(sN) is eventually bounded by a constant times f, uniformly over finitely many phases. Thus all exponential N moments are finite. In fact the same comparison yields exp[t N log(N+2)] moments for every t<alpha, though the appended claim needs only exponential moments. Closed finite classes have all these moments trivially.

## 3. Neutral projected components

If every residual increment is zero, r=N+beta_j is conserved by every projected transition and also by every invisible transition. Since j ranges over a finite alphabet, fixing r bounds N. The corresponding physical set is finite. Consequently each closed irreducible physical class in it is a finite-state chain and is positive recurrent, without using the Hurwitz resolvent theorem.

The union over r can be infinite; no assertion that this union is a finite exception set is needed. Nonexplosion within each such class follows from finiteness and finite per-state rates. If desired, a positive norm-like function of conserved r gives zero drift on all neutral components at once. Weak reversibility of the PHYSICAL network makes every communicating class closed, via enabled reaction-graph return paths; physical weak reversibility is not silently supplied by projected weak reversibility.

## 4. Source-completeness earns the rate bounds

For source total order a and projected channel e, aggregate all channels with source composition y, |y|=a, and the prescribed projected target (total order/phase). Their generator contribution to V is the sum of their rates times ONE common projected V increment. Target composition does not otherwise enter that calculation.

If the aggregate coefficient at each y is between c_e a!/product y_i! and C_e a!/product y_i!, summing against the nonnegative mass-action factors gives

    c_e (N)_a ≤ actual projected aggregate rate ≤ C_e (N)_a

by the stated multivariate falling-factorial identity. This remains true on population boundaries. When N<a, both sides and every term are zero; an arbitrary effective coefficient inside the interval can be assigned without altering the rate. When N≥a, division defines a coefficient inside the fixed positive interval. Different source compositions may have different coefficients, so the projected total rate need not depend only on N. Exact lumpability is not assumed.

The condition is phase-specific where applicable; fixed bounded-phase factorial coefficients must be included in the stated aggregate coefficient bounds. All nontrivial projected channels still belong to the finite weakly reversible projected graph required by the robust theorem. Source-completeness alone does not establish that graph property.

## Scope retained

The global conclusion relies on globally positive projected coefficient lower bounds, finite closed phases, and a total count including every unbounded population. It does not apply merely from cone-local comparability, from a truncated halo, or when missing source compositions allow boundary rates to vanish. Removing those restrictions remains open.

Reviewed source hash:
3bc3a26972df748e95180d545383a9ab26fc1faca3b3440cc89e77cc33cbd4cc  producer-workspace/ROBUST_PHASE_INFINITE_FIBER_LIFT.md
