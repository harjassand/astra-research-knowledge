# Passive clamp uncertainty and a target-task lifetime certificate

Date: 2026-10-15. Independent reconstruction of `sources/transport/astra_kardashev_transport_checkpoint_2026-10-15.md`; no other current worker scratch was read for these deductions. This is a conditional mathematical analysis, not a material prediction, experimentally acquired capability, external certification, or historical novelty claim.

## 1. What the incoming equations establish

Source lines 37–107 specify stable host coordinates, common K≻0 and masses, classical harmonic ensembles, a physically accessible common clamp, and fixed constrained state meanings. Completing the square and applying the rank-one inverse and determinant identities gives

    ΔF_s=χR_s+(kBT/2)log(1+κc),
    ΔB_s=χ(R_s−R_A),
    c=bᵀK⁻¹b, R_s=(bᵀK⁻¹f_s)²/(2c), χ=κc/(1+κc).

The determinant term cancels only because K is common. The source's R_U<R_A<R_H criterion correctly lowers the useful barrier and raises the harmful barrier under one control. Unchanged kinetic prefactors, entry transition states, recrossing, dividing surfaces and equilibration separation are additional model premises. Mere passivity of the added spring establishes none of the state-overlap ordering.

With rates a_L,a_R for entry, b_L,b_R for exit, let A=a_L+a_R, B=b_L+b_R and Δ=a_Lb_R−a_Rb_L. The two-state occupancy calculation gives J=Δ/(A+B). Under the source's shared entry/exit transition assumption,

    a′=αa, b′=qb,
    α=exp(−βχR_U), q=exp[βχ(R_A−R_U)],
    J′/J=αq(A+B)/(αA+qB),

provided J≠0. The affinity is unchanged. For q>1 and α<1 the current gain condition is exactly the source's loading threshold A/B>q(1−α)/[α(q−1)]. An enhanced escape rate is therefore insufficient for current gain.

## 2. Exact yield cancellation under occupied-only damage

Assume all rates are time-homogeneous, the pore is empty initially, a destructive absorbing transition of rate h>0 occurs only while occupied, and N counts right exits minus right entries up to failure. Solve the backward first-step equations. If π_R=a_R/A, then

    E T=(A+B+h)/(Ah),
    E N=Δ/(Ah)−π_R.

With h′=q_Hh and q_H=exp[βχ(R_A−R_H)], substitution gives the exact identity

    E N′+π_R=(q/q_H)(E N+π_R),
    q/q_H=exp[βχ(R_H−R_U)].

Thus the initial trap overlap R_A and entry suppression α cancel from this particular expected lifetime transfer. If Δ>0, its gain is decided by R_H−R_U alone, which is weaker than R_U<R_A<R_H. If Δ<0 the inequality reverses; if Δ=0 there is no gain. The correction −π_R is retained, so E N′/E N need not equal q/q_H. Current, elapsed lifetime, throughput per calendar time, and net energy remain different tasks.

This cancellation does **not** extend automatically to empty-state damage, multiple occupancy, hidden aging, failure of other device components, control-dependent entry asymmetry, changing prefactors, or finite-horizon targets. It is a useful target reduction within the declared source model.

## 3. An observable certificate without transition-state observation

At one fixed clamp setting, prepare the occupied state and observe its next event. Let r_L,r_R,r_H be the probabilities of left exit, right exit and failure; r_H>0. Prepare an empty state and observe which reservoir supplies its next entry, giving π_R. Under the same Markov and same-regime assumptions,

    r_L=b_L/(B+h), r_R=b_R/(B+h), r_H=h/(B+h),
    E N=(1−π_R)r_R/r_H−π_R r_L/r_H−π_R.

The formula follows either from the rates or the geometric number of occupied visits until failure. It needs event identities and the complete first-event distribution, not direct transition-state coordinates or a harmonic free-energy fit. If elapsed lifetime matters too, measure the mean empty waiting time τ₀ and occupied waiting time τ₁; then E T=(τ₀+τ₁)/r_H. Absolute waiting times, not just branching fractions, are needed for a time or power claim.

For a simple rigorous uncertainty certificate, let simultaneous intervals contain π_R,r_R,r_H, with r_L=1−r_R−r_H, r_H≥l_H>0. The expression simplifies to

    E N=(r_R−π_R)/r_H.

Indeed the −π_R endpoint correction cancels the +π_Rr_H term after substitution. For a forward-positive range l_R−u_π≥0, a valid box lower bound is (l_R−u_π)/u_H and upper bound is (u_R−l_π)/l_H. The bound remains valid if the intervals include impossible simplex tuples; enforcing their joint simplex/likelihood constraints can tighten it. When the numerator crosses zero, use all four endpoint ratios rather than assuming monotonicity in r_H. Compare the certified intervals for the actual finite actions and subtract their complete expected costs.

An exact feasible joint confidence set can be substituted for intervals. A covered action whose lower net utility exceeds every competitor's upper net utility closes that declared decision. No full mechanism identification is needed. The action catalogue, preparation overhead, event misclassification, censoring/tails, specimen variation, common conditions and complete costs remain acquired inputs. This is standard direct event/decision estimation, not a claimed new operation or proven cheaper experiment.

If h is extremely small, observing failure is expensive: r_H in the denominator makes the required precision consequential. Repeated exit events are not independent virgin specimens unless the declared model or a calibrated renewal protocol supplies that relation. A finite censored experiment cannot yield a uniform exact infinite-lifetime expectation on an unrestricted hidden-tail class. A finite-horizon clipped output instead has bounded statistics, but answers a different explicit task.

## 4. Well data cannot acquire the missing overlap ordering

Here is a pair of exact common-K harmonic alternatives. Use one host coordinate, K=1, b=1, β=1 and κ=1, so c=1 and χ=1/2. Take f_A=1 and E_A⁰=1/2, giving R_A=1/2 and F_A(0)=0. Fix any positive baseline useful and harmful barriers B_U⁰,B_H⁰ and common prefactors. For every state s choose E_s⁰=B_s⁰+R_s; then F_s(0)−F_A(0)=B_s⁰ independently of R_s.

World +: f_U=0, f_H=√2, so (R_U,R_H)=(0,1).

World −: f_U=√2, f_H=0, so (R_U,R_H)=(1,0).

All occupied-well mechanical distributions and responses agree for **every** κ, because A,K,f_A are identical. Baseline useful/harmful rates agree by the chosen offsets. Empty-state parameters can also be identical. Yet at κ=1,

    world +: q=e^(1/4), q_H=e^(−1/4), α=1;
    world −: q=e^(−1/4), q_H=e^(1/4), α=e^(−1/2).

For Δ>0, expected lifetime transfer strictly increases in world + and decreases in world −. Current also increases in world + and decreases in world −. Both clamped host matrices remain positive; no unstable host or exotic negative stiffness is used. The distinguishing hidden information resides in constrained transition ensembles, or equivalently in observed action effects—not in equilibrium well compliance or baseline rates.

One can keep both transition-state overlaps in bounded physically declared intervals. If those intervals permit R_H−R_U of both signs, the lifetime-yield ordering remains ambiguous. If the acquired joint uncertainty set instead has R_H−R_U≥δ>0 and χ≥χ_min>0, it certifies the model's shifted-yield multiplier at least exp(βχ_minδ), subject to the same kinetic and cost assumptions. Marginal intervals alone may give only a conservative minimum; common correlations should be retained.

## 5. The strongest equally informed operation

For a finite fixture catalogue, randomized matched measurements of the actual accepted transfer, destruction, waiting time and total cost answer the action question directly. The event certificate above is a compact model-specific sufficient statistic; full until-failure cycles are an alternative when their expense and tails are acceptable. A transition-state acquisition route can be valuable for extrapolation or unseen fixtures, but is not logically necessary for a covered finite decision. Any claimed advantage must count the evidence required to justify extrapolation and compare against these direct methods on the same task and information boundary.

## 6. Pooled event calibration fails under persistent hidden heterogeneity

The compact certificate in Section3 requires one homogeneous Markov response or an acquired complete joint type/history model. It cannot be applied to pooled event probabilities from persistent hidden specimen types by replacing an expectation of a ratio with a ratio of expectations.

An exact countermodel uses two equally likely types, each with empty total entry rate A=1, right-entry fraction π_R=1/4, and occupied total event rate B+h=1. Thus both empty and occupied waiting times are exponential with mean1, independent of type. Only the occupied branching probabilities differ. Let r_L fill the simplex.

World + has type1 (r_H,r_R)=(1/16,7/16) and type2 (7/16,1/16); both have r_L=1/2. Their expected net transfers are3 and−3/7, so the specimen-average expected net transfer is9/7.

World − has type1 (r_H,r_R)=(1/16,1/16), r_L=7/8, and type2 (7/16,7/16), r_L=1/8. Their expected net transfers are−3 and3/7, so the specimen-average expected net transfer is−9/7.

Both worlds have exactly the same pooled first occupied-event probabilities

    (E r_H,E r_R,E r_L)=(1/4,1/4,1/2),

the same entry statistics, the same full one-event waiting-time distributions, and the same mean failure time

    E T=(1/2)[2/(1/16)+2/(7/16)]=128/7.

All entry/exit/failure rates are strictly positive. Applying the homogeneous formula to pooled probabilities would give0, while the actual expected decisions have opposite signs. The hidden correlation persists across successive visits within the same specimen. Pooling separate marginal intervals or one-event samples does not establish the renewal relation required for the formula.

A complete observed until-failure cycle directly measures the intended signed output, and repeated within-specimen events can expose type/history dependence. Either repairs the *covered* decision when its censoring, tails, specimen population and costs are calibrated. Hidden transition-state mechanism identification remains unnecessary; hidden repeated-history response cannot be ignored.
