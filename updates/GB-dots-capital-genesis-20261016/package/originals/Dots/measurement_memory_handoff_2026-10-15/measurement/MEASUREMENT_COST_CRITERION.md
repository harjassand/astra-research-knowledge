# Finite-cost criterion for repeated exact-measurement cells

2026-10-15. An algebraic sufficient-condition optimization, not a device prediction. No measured quantities are fitted or substituted.

## 1. Accounting and scope
Fix weak-noise exposure tau≥0, perturbation norm bound J≥0, scheduling rate kappa>0, and uniform nonnegative scheduled-memory constants A,B,C,delta_ideal,nu. Fix the target R=q_star^Q. These constants, the footprint and conflict assumptions must remain valid uniformly over the candidate measurement counts; if changing M changes Q, geometry or the constants, the formulas below cannot simply hold them fixed.

Use M≥1 equal weak-noise cells and M+1 exact measurements: one initial acquisition plus M cell-end acquisitions. Charge

  theta(M)=tau+(M+1)t_meas,
  p(M)≤J² tau²/M.

Measurements are actual exact instruments, possibly unread by the controller; “unread” does not mean imaginary intermediate projections. The applicable measured-cell theorem must still supply its actual-record/common-dilation interface and full support conditions. Treating measurement duration as noiseless is an explicit ideal-resource assumption: any perturbation acting during readout must be charged in a model that justifies the resulting bound.

At fixed kappa, insert these quantities into the stated sufficient condition

  delta_ideal + A nu/kappa + B kappa theta(M) + C p(M) ≤ R.

Define

  K=delta_ideal+A nu/kappa+B kappa tau,
  c=C J² tau²,
  d=B kappa t_meas.

A valid conservative objective is therefore

  Phi(M)=K+d(M+1)+c/M.                                      (1)

A fixed correction/reset overhead theta_0 adds B kappa theta_0 to K. If the initial sector acquisition is already paid outside this reservation, consistently use theta=tau+M t_meas instead: replace d(M+1) by dM. The integer optimizer and comparison against M=1 are unchanged, while absolute feasibility shifts by d. Do not give only the repeated-measurement arm a free initial measurement or compare different conventions.

## 2. Exact positive-cost integer optimum
Assume d>0 and c≥0. The adjacent difference is

  Phi(M+1)−Phi(M)=d−c/[M(M+1)].                             (2)

It increases with M, so the complete set of integer minimizers is characterized by

  M(M−1) ≤ c/d ≤ M(M+1),  M≥1,                             (3)

where the lower condition is automatic for M=1. The smallest minimizer is

  M_* = max{1, ceil[(sqrt(1+4c/d)−1)/2]}.                   (4)

If c/d=M_*(M_*+1), M_* and M_*+1 tie; otherwise the minimizer is unique. This is the exact integer answer, not “round sqrt(c/d)” without tie checking. The provided script computes it using rational comparisons and integer square roots, avoiding numerical rounding at ties.

For any M>1,

  Phi(M)−Phi(1)=(M−1)(d−c/M).                             (5)

Thus a particular M improves the conservative objective iff M<c/d, and **any strict improvement over M=1 exists iff c>2d**. At c=2d, M=1 and M=2 tie; at c<2d no subdivision improves this objective. In physical symbols the strict-improvement condition is

  C J² tau² > 2 B kappa t_meas.                            (6)

This compares sufficient upper objectives under identical accounting. Failure of (6) is an obstruction to improvement of this certificate, not proof that actual physical error cannot improve. Satisfaction does not prove actual error decreases with M.

## 3. Exact feasibility and an immediate no-go test
Set L=R−K. Feasibility of the conservative condition is exactly the existence of an integer M≥1 satisfying

  d M²+(d−L)M+c≤0.                                        (7)

For d>0, this is equivalent to Phi(M_*)≤R. Alternatively, require L>d, discriminant D=(L−d)²−4dc≥0, and an integer in

  [max{1,ceil((L−d−sqrt(D))/(2d))},
   floor((L−d+sqrt(D))/(2d))].                            (8)

The lower endpoint must not exceed the upper. Exact arithmetic or a certified root calculation is appropriate on boundary cases. This includes c=0: M=1 is best and feasibility is L≥2d.

A quick necessary condition from AM–GM is

  R ≥ K+d+2sqrt(cd).                                      (9)

If it fails, no integer M can satisfy the conservative target. It is not sufficient because M≥1 and integrality may cost more. A genuine “certificate rescue” of an infeasible M=1 baseline occurs exactly when

  Phi(M_*)≤R<Phi(1).

For d>0, Phi(M) tends to infinity as M tends to infinity. The physical-duration price defeats the formal 1/M limit. Roughly M_* scales as sqrt(c/d), with the exact discrete thresholds above. Increasing M also can worsen reservation conflicts and support size; ignoring those changes would be optimistic, not an additional benefit of this calculation.

Degenerate case d=0: if c>0, Phi decreases toward K but has no finite optimizer; a finite feasible M exists iff R>K, and M≥max{1,ceil(c/(R−K))} suffices. If c=0, every M has objective K. The d=0 case assumes no counted marginal duration price (or B=0), not a physical demonstration that measurements are free. Constraints on maximum available M must be imposed separately; for a fixed integer interval the positive-cost optimizer is clipped to its permitted endpoints.

## 4. Optional use of the probability cap
The preceding optimizer is exact for the requested **conservative uncapped** majorant. A tighter valid objective can use p≤min{1,a/M}, a=J²tau²:

  Phi_cap(M)=K+d(M+1)+C min{1,a/M}.                        (10)

Do not claim (4) always optimizes this capped objective. Its saturated segment M≤a is increasing when d>0, so its best saturated candidate is M=1. On the unsaturated segment M>a it is the same convex discrete objective with c=Ca. Let m_0=max{1,floor(a)+1}; restrict the minimizers from (3) to M≥m_0, clamping to m_0 if necessary. Compare that tail candidate (including an adjacent tie) with M=1. These are all global minimizers. Feasibility follows by evaluating them.

When a≤1, the uncapped formula applies unchanged. When a>1, (6) alone is not the correct cap-aware improvement criterion. For any M>a, strict improvement over M=1 is instead exactly

  d(M−1) < C(1−a/M).                                     (11)

The finite candidate comparison just described decides whether such an improvement exists. The script checks this cap-aware rule as well. Both capped and uncapped objectives still diverge for positive d.

## 5. Measurement-fault cost: only with a joint CP qualification
The ideal-measurement theorem supplies no scalar measurement-fault epsilon. Average infidelity, a marginal failure frequency, or an arbitrary diamond-norm discrepancy does not by itself produce the mixed joint subset bound required by the scheduled-memory proof. Independent measurement-fault marginals alone also do not establish joint products with coherent-noise flags.

A sufficient additional hypothesis would be an actual common CP-instrument decomposition into exact-measurement branches and marked faulty-operation branches, with uniform **mixed** subset effects bounded by the product of the noise-parent factors and epsilon for each distinct marked measurement slot. Each faulty slot must be assigned to its parent's full bad envelope; an initial acquisition fault is included. Explicit independent classical Bernoulli selection between ideal and local faulty instruments can furnish the measurement factors only when the required uniform mixed/noise/support argument is also proved. No such device qualification is inferred here.

Under that extra mixed CP hypothesis, a commuting-event union over noise failure and the M+1 faulty measurement opportunities gives a valid conservative parent factor

  p_total ≤ J²tau²/M+(M+1)epsilon,

and the corresponding product over parents follows from the mixed subset assumption. Then the same integer formulas apply with

  c=CJ²tau²,   d=B kappa t_meas+C epsilon.                 (12)

The duration and fault prices add. Optional overall caps may tighten the answer but must be optimized piecewise rather than silently inserted into (4). Without the joint qualification, omit epsilon entirely and label the calculation an exact-measurement-resource criterion.

## 6. Relation to the acquired Zeno evidence
The final measured_zeno_response README and report were inspected for scope only. Slichter's continuous transmon readout and Kalb's discrete nonselective joint-spin projections establish different measured Zeno responses. Neither provides the arbitrary-bath full-error norm J, exact instrument/record guarantee, mixed CP measurement-fault epsilon, or uniform scheduled-memory constants required here. The digitized Slichter figure is a published-summary extraction, not raw fault histories. No drive rate, fitted coherence time, measurement infidelity or cross-device number was substituted into (1). The experiments are not combined and no new fit was performed.

## 7. Auditable check
Own standard-library script check_measurement_cost_criterion.py verifies 1,240 rational uncapped cases and 738 rational capped cases against exhaustive integers M=1,...,200. It checks ties, the improvement threshold, the exact quadratic feasibility equivalence, and the cap-aware candidate rule. Results: measurement_cost_criterion_check.json, PASS. The examples are explicitly dimensionless algebra tests, not invented device inputs. All checks were rerun after the final script edit.
