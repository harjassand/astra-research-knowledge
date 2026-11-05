# Exact carrier-erasure law and its restricted optimal resource scale

The [complete theorem](package/root_analysis/erasure_theorem.txt) extends the accepted weak-stream acquisition calculation to carriers **lost before receiver processing**, with the loss pattern supplied as a classical flag. Arbitrary final collective decoding of all untouched retained carriers is allowed. This is not interchangeable with general causal instruments that coherently process a carrier before discarding it.

Write `b=sin(theta)^4`, `d=cos(theta)^4` and initialize `a_0=0,q_0=1`. The exact ordered recurrence is

```text
retained: a_j=a_(j-1)+b q_(j-1), q_j=(1-b)q_(j-1);
lost:     a_j=a_(j-1),           q_j=d q_(j-1).
```

An output-only physical reverse decoder achieves `epsilon_Petz=3(1-a_N)/4`. It uses an initialized tracial dummy, inverse encounters with the retained outputs in reverse schedule order, and a dummy depolarizing operation at each erased position. Every decoder obeys `epsilon_opt>=3(1-sqrt(a_N))/4`. The factor-two small-error gap and all preparation, routing, inverse-control and memory-protection costs remain explicit.

The later [coherent energy-window compressor](../2026-11-05-p1-joint-recovery/README.md) attains a strict logical memory saving after processing actual carriers,with its own accuracy/service bill. This does not contradict the pre-access erasure law here. The continuation preserves these original files unchanged.

## Independent flagged loss

For loss probability ell independent across carriers and of the input, put `f=(1-ell)(1-b)+ell d`. The unconditional flagged-channel coefficient and limiting value are

```text
a_bar_N=(1-ell)b(1-f^N)/(1-f),
a_bar_inf=(1-ell)b/[(1-ell)b+ell(1-d)].
```

The same achieved and all-decoder formulas apply with a_bar_N. Acquisition is quartic, while a lost carrier damages residual signal at quadratic order. When `ell=kappa theta^2`, the limiting coefficient tends to `1/(1+2kappa)`. Necessary and sufficient-order small-angle high-accuracy loss tolerances scale as `ell=Theta(epsilon theta^2)`; the source gives exact inequalities and strict margins for finite N. This does not mean every constant at that scale suffices.

At `.1`, N=43,462, loss probability `1e-4` gives achieved error about `.0236813` and arbitrary-decoder lower bound `.0119356`. At `1e-3`, even infinite count leaves a lower bound about `.0653091`, ruling out one-percent error for this erased stream. These large-count values evaluate exact formulas, not a 43,462-qubit density-matrix simulation.

## Untouched-carrier budget

Among subsets with at most m intact retained carriers, keeping the **first m** maximizes a_N by an adjacent exchange argument. Thus `a_N<=1-(1-sin(theta)^4)^m`. Combined with the decoder pair, the necessary and achievable retained-carrier scale is `Theta(theta^-4 log(1/epsilon))` in this restricted class. Input-independent random subset selection cannot improve that bound; coherent compression/state-dependent instruments are outside it.

The reverse circuit can be linear in addressed operations with a suitable LIFO/direct-address interface; a FIFO fixed-junction layout can pay quadratic routing. Neither hardware access pattern is free or a universal lower bound. Replacement preparations, calibration, gate errors, address/routing and protection require a whole-channel error budget; no fault-tolerant factory or scalable physical reader was built.

The supplied [186-case receipt](package/root_analysis/erasure_results.json) covers all retained subsets through N=5 at three angles with maximum Gram discrepancy `4.44e-16`. It corroborates the analytic recurrence. [Accepted governing acquisition source](package/root_analysis/inputs/partial_swap_theory.txt), [source attribution](package/source_manifest.json). No new Capital calculation, experimental validation or audit occurred. The [general causal compression endpoint](README.md) remains unresolved.
