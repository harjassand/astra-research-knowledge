# Reusable ordinary trace-cost certificate

30 October 2026. Abstraction of the coupled-face construction, not a novelty claim for censoring, trace chains, or Schur complements.

Let a CTMC be stopped at K and partition the remaining states as A union B. Suppose a state b in B makes one exponential hold of rate q_b>0 and then jumps to A or K (no B-to-B jump). For a nonnegative running reward v define h(b)=v(b)/q_b. If

    sum_{b in B} q(x,b) h(b) <= C v(x),    x in A,

then from A inputs

    E integral_before_stop 1_B v(X_t)dt
       <= C E integral_before_stop 1_A v(X_t)dt.

Proof: at each actual A-to-B entrance, the conditional expected B reward before its next exit is h(b), or no larger if an additional stopping event truncates it. Sum actual entrances and apply their compensators. Localize first; monotone convergence gives the inequality without assuming the desired full hitting-time integrability in advance. An initial B hold contributes its explicit h(b) separately.

The trace on A deletes these holds and has effective generator given by the standard elimination expression

    Q_trace = Q_AA + Q_AB diag(q_b^-1) Q_BA,

with absorption retained and return-to-the-same-A-state terms interpreted in the generator, not counted as new state changes. No condition that the A->B->A transition norm be small is required. The displayed cost certificate is what restores physical time after censoring.

For the deficiency-two module, B is D=0,CE>0. Its exit rate includes gamma CE plus the seed/clear clock. The two ingress terms are beta C and kappa a at D=1; their actual output denominators give the uniform bound. Fixed A-power rewards survive because A changes by at most1 at entrance. This is why the non-small mixed return can be eliminated, while the same treatment would fail for a genuinely absorbing non-A-birth face with zero exit rate.

At the initial state a=E=0,C=c,D=1, ignoring connectors until the first productive C->E conversion, the beta jump followed by its gamma reverse is an exact self-return. Direct renewal gives expected time to that productive conversion

    (1+beta/gamma)/(lambda c).

This simple instance exposes the distinction: return probability need not vanish with c, but its entire holding cost is a finite multiplier of the productive clock. The later pooled-tag proof, not this ordinary trace lemma alone, earns the reset and signed-cycle interfaces.
