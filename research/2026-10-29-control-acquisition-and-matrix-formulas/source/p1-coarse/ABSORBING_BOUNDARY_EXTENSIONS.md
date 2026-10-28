# Complete cost and sensor precision after removing the global gap

28 October 2026. These are new consequences of the absorption-boundary
construction. The frozen main compiler and its reviewed results are unchanged.

## 1. Observable performance conditions replace a hidden spectral promise

Consider the rank-one case and a scale g tending to zero. For each of q
primitives, suppose the following population conditions hold at a chosen
finite censor time H:

- boundary departure lies between c g and C g;
- absorption before the boundary return or censor is at least c_a g;
- return-or-live-censored probability is at most C_u g^2;
- expected trial length is bounded by a class constant.

These are performance conditions, not additional inputs needed to make the
certificate sound. The finite gate checks its own confidence inequalities
and can reject an unproductive source. There is no strict source norm cap.

Use N=O(g^-3 log(q/delta)) fixed trials per primitive. Variance-aware
first-step estimation gives |p_hat-p|=O(g^2). Binomial upper confidence bounds
on the rare return-or-censored event give u_U=O(g^2); the absorption lower
bound is Omega(g). Hence the acquired local inverse form satisfies

    M=O(1/g),  Q_true=O(g^2),
    Q_proposed <= [sqrt(Q_true)+O(g^2)sqrt(M)]^2=O(g^2).

Computational dissipation 1-p_hat^2=Theta(g), so theta^2=O(g) and the
normalized weak-defect uncertainty is zeta=O(g). The all-word error is O(g).

The complete expected cost is O(q g^-3 log(q/delta)) primitive applications
and observations. Exact boundary-state continuation requires a new
preparation only after a departure that has not returned; expected
preparations are O(q g^-2 log(q/delta)), plus initialization. A general
finite H does not give the same deterministic worst-case cost bound. A
high-probability cost bound requires the corresponding length/departure
control, which the concrete logarithmic-censor family below supplies.

The full-state one-live-state survival pair in
branches/scalar/CALIBRATION_COST_THEOREM_REVIEW.md belongs to this observable
class: zero return residual, departure Theta(g), immediate visible loss,
one-step trials. Therefore the established Omega(g^-3) source-action lower
bound still applies to uniform O(g) accuracy, with its accuracy constant
matched as in that review. Ordinary variance-aware survival calibration
matches it. This is no new statistical principle and no preparation lower
bound; it proves that removing the global spectral premise need not worsen
the complete slow-scale acquisition rate.

## 2. A reachable norm-one family where the weighted certificate matters

For 0<g<=1/4, let boundary holding probability be p=1-g. Couple the boundary
to a fast hidden state by g/2, with fast diagonal 1/4. Add countably many slow
states, with total entry mass S=g^3/16 and

    w_n=S 2^(-n-1),  eta_n=4S 2^(-n), n>=0.

A slow state stays with probability 1-eta_n, returns with probability w_n,
and is absorbed with probability eta_n-w_n. The boundary has direct loss
g/2-S>0. All slow states are reachable. As in the main example, the symmetric
substochastic operator has norm exactly one and no nonzero fixed live vector.

The eventual excursion return mass is exactly

    r_infinity = g^2/3 + S/8.

Choose H minimally so (1/4)^(H-1)<=g/8. The unresolved fast probability is
at most g^2/16; the entire unresolved slow probability is at most S. Thus

    u <= g^2/3+S/8+g^2/16+S <= g^2/2,
    a_H = g-u >= 7g/8.

The local negative-sector margin is at least 2(1-g)+7g/8>=55/32. Therefore

    m <= 4/(7g)+16/55 <= 248/(385g),
    Q_upper <= g^2/2 + m g^4/4 <= (208/385)g^2.

Since 1-p^2>=7g/4, the weighted all-word dynamic certificate is at most
(1664/2695)g<g. The expected source applications per trial obey

    E[length] <= 1+2g/3+S(H-1) < 2.

H grows only logarithmically. For example H-1<=8/g gives the coarse bound
1+2g/3+g^2/2<2. The same departure-count event used for calibration bounds
the total actual length by N+O(gN)H=O(N) with high probability.

The older unweighted second-order certificate, even supplied the exact
boundary model and exact residual norm, is

    ||D||^2/(1-p)^2
      = [(g/2)^2+S^2/3]/g^2 >= 1/4.

It cannot expose the vanishing error in this family. This is a comparison
between certificates, not a lower bound against every existing method.
An equally informed method adopting the acquired local source form obtains
the stronger guarantee too. In particular the main three-boundary example
already has a gap-free unweighted certificate; the advance here removes the
strict spectral premise from the more informative *weighted acquisition*.
It is not the first all-word theorem that avoids a hidden source gap.

core/absorbing_slow_family.py verifies seven exact source-scale receipts,
g=1/4 through 1/1024. At the last scale the weighted bound is .000356342922,
while the unweighted bound is .250000000000001. The check executes exact
algebra, not the proposed statistical budgets. Ordinary arguments above
establish the all-scale statements.

## 3. A bounded loss-sensor error can be charged explicitly

Retain exact boundary-state labels and preparation. Allow the distinction
between alive outside and absorbed to be wrong with conditional probability
at most eta at each nonboundary report, uniformly over the past. The report
remains nonintrusive. A source trial has at most H reports.
Reports are causal. A genuine preparation or valid boundary reuse restores
the source path law conditional on the complete prior experimental history,
including prior reports. This is the filtration premise used by the coupling
and conditional moment-generating-function proof. A merely marginal average
sensor error rate does not suffice; a shared persistent sensor fault can
violate the conditional bound after its past outcomes reveal it.

Couple the observed trial to the same underlying source path with ideal
reports. Unless at least one report is wrong, stopping and every recorded
indicator agree. Conditional on the history before a fresh trial, the chance
of disagreement is at most c_H=min(1,H eta). The bound uses a union bound;
it does not require independent sensor errors or an independent stopping time.
Potential ideal source trajectories beyond an erroneously early stop are
used only in this mathematical coupling.

For each ideal fixed-source event probability p, the conditional mean of
the observed Bernoulli indicator lies in [p-c_H,p+c_H], clipped to [0,1].
Iterating the Bernoulli moment-generating-function bound supplies the same
Chernoff tail inequality as independent indicators with the corresponding
extremal means. Consequently the existing confidence endpoints remain
sound after adding c_H to return-or-pending and even-return-or-pending
upper bounds, and subtracting c_H from absorption lower bounds. Initial
boundary counts are unchanged, because boundary labels remain exact.

The new bounds feed the identical finite Schur and source-form certificate.
Known-boundary reuse is still valid: an erroneous loss report can end a
trial outside the boundary, but that report never falsely supplies a known
boundary state. The next trial then receives a genuine preparation. If the
boundary label itself can be false, this proof does not apply.

core/absorbing_sensor_robustness.py executes this exact sensitivity calculation
on the saved main acquisition counts, using zero additional source queries.
It does not establish the sensor warranty or simulate new noisy instruments.

| Per-report error upper eta | Uniform point-model bound | Transport difference interval |
|---:|---:|---:|
| 0 | .0399059846 | [.1080212,.1337116] |
| 10^-8 | .0399689014 | [.1080045,.1337282] |
| 10^-7 | .0405206714 | [.1078543,.1338785] |
| 10^-6 | .0451712088 | [.1063510,.1353818] |
| 10^-5 | .0753947918 | [.0911908,.1505419] |
| 10^-4 | .3016404368 | [-.0755538,.3172865] |

The sign certificate disappears at the final tested warranty. This is a
concrete sensitivity to instrument accuracy, not a count of measurements
standing in for that accuracy. For the slow-scale family, preserving
return-or-pending upper bounds O(g^2) requires H eta=O(g^2), so this sufficient
condition asks eta=O(g^2/log(1/g)) with the chosen censor horizon. Acquiring
such a uniform sensor guarantee is an additional physical task.
