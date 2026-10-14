# Decision-theory line: live response closure

15 October 2026, Australia/Brisbane. **Status: scoped exact theorem and obstruction; no established new capability.** This report concerns one live substrate, an adaptive probe protocol followed by one terminal control choice. It does not assert that arbitrary scientific control problems have been closed. The proposed operation is to measure the *joint* response of a probe and a subsequent control, including probe-induced loss of the substrate, and synthesize the control directly from that response. Mechanism identification is unnecessary **if** the relevant world-conditioned response experiments can actually be acquired. That access is the central unproved physical assumption.

## Exact response theorem

Let the possible mechanisms or prepared conditions be a finite set `Theta`, the probe transcript a finite set `Y`, and terminal controls a finite set `C`. Fix an admissible, possibly adaptive probe protocol `sigma` that acts on a physical substrate before the terminal control. For every `theta in Theta`, `y in Y`, `c in C`, define the **interventional response mass**

```
p[theta,y,c] = P_theta{probe transcript is y AND verified goal is reached
                       without forbidden failure when c is applied after y}.
```

The probability includes all effects of the probe on the substrate. If the probe destroys the only viable object, its mass is zero for every terminal control on that outcome. A terminal rule is a stochastic kernel `d(c|y)` chosen only from the observed transcript. Its worst-world success probability is

```
V_sigma = max_d min_theta sum_y sum_c d(c|y) p[theta,y,c]
          = min_{lambda in Delta(Theta)} sum_y max_c
                sum_theta lambda(theta) p[theta,y,c].                 (1)
```

Thus a target success threshold `tau` is achievable in this two-phase interface under a resource constraint `C(sigma) <= B` exactly when some admissible `sigma` with that cost has `V_sigma >= tau`. The response tensor is task-relative: it need not specify latent states, reaction pathways, or the probability of observations that cannot lead to success. This is an *exact characterization given the tensor*, not an efficient way to discover the tensor or `sigma`.

**Proof.** Condition on the probe transcript. Causal ordering gives success in world `theta` as the first linear expression in (1). Maximizing its minimum over finite stochastic terminal rules is a finite linear program. Replace the minimum over `theta` by a minimum over distributions `lambda` on `Theta`. The rule and `lambda` range over compact convex simplexes, so finite minimax swaps max and min. For fixed `lambda`, the optimizing rule independently chooses, at each `y`, a control attaining the displayed maximum. This proves (1), including randomized terminal choices and unequal world-specific probe survival. No Markov or stationarity assumption is used; all earlier adaptive probe actions are bundled into `sigma`.

For two symmetric worlds with terminal controls `c0,c1` that succeed only when their indices match the world, let `mu_theta(y)=P_theta{Y=y AND substrate survives the probe}`. Equation (1) reduces to equal-prior success

```
V_sigma = (1/2) sum_y max{mu_0(y), mu_1(y)}
        = (s_0+s_1+||mu_0-mu_1||_1)/4,                         (2)
```

provided the symmetry makes equal prior least favorable; otherwise the minimization in (1), not (2), gives the minimax value. Here `s_theta=sum_y mu_theta(y)`. Formula (2) is a **live-information** measure: a perfectly informative observation can be worthless when the probe has removed the ability to act.

## Decisive counterexample and redesign

Two worlds `theta=0,1` have indistinguishable starting observations. On a live object, `c_theta` achieves the goal and the other control irreversibly fails. Without probing, randomized commitment has exact uniform success `1/2`. A proposed probe reveals `theta` perfectly, but consumes the unique object with probability `3/5`, independently of `theta`; the readout is still available when the object is lost. Its surviving response masses are `p[theta,theta,c_theta]=2/5`, all other success masses zero. Equation (1) gives `V_probe=2/5`: *perfect mechanism identification makes control worse* than acting without the probe. The failure is physical viability, not information access.

A substantive redesign is a protected probe that preserves the object with probability `9/10` and, conditional on survival, reports the wrong world with probability `1/10`. The matching-control rule then has exact uniform success `(9/10)(9/10)=81/100`; (1) certifies this value. The redesigned probe beats the `1/2` no-probe policy only when `s(1-e)>1/2` in this symmetric binary fixture. This threshold includes both information quality and material survival. **These are constructed probabilities, not measured properties of a device.** A useful physical instantiation would need a readout that actually achieves the claimed `s,e` and leaves the actuator compatible with the object.

The same algebra admits a probe that reveals nothing but improves the object: if an observation-independent preparation increases the success mass of a universal terminal control from `2/5` to `4/5` in both worlds, operational value doubles while statistical informativeness is unchanged. That is why the joint probe/control response, rather than a sensor-only order, is the quantity to acquire.

## How a direct certificate could be acquired, and its limits

Suppose each `theta` can be *independently prepared or unambiguously stratified* into fresh, exchangeable specimens, the probe `sigma` and every `c` can be executed on each specimen, and goal/failure can be verified. For each `(theta,c)`, perform `n` independent runs of `sigma` followed by `c` regardless of `y`; record each transcript and success. The empirical frequency of `{Y=y AND success}` estimates `p[theta,y,c]`. With `M=|Theta|`, `K=|C|`, `J=|Y|`, Hoeffding plus a union bound gives simultaneous cell error at most

```
r = sqrt(log(2 M K J / delta)/(2 n))
```

with probability at least `1-delta`. Solve (1) with lower masses `L[theta,y,c]=max(0,p_hat[theta,y,c]-r)`. The attained rule then has true worst-world success at least `V(L)` on that confidence event. Also `V(L) >= V(p)-2 J r`; hence `n >= 2 J^2 log(2 M K J/delta)/epsilon^2` suffices to lose at most `epsilon` in certified value relative to the best terminal rule for *this fixed probe*. These bounds are elementary and conservative. They charge `M K n` complete sacrificial trials, including preparation, probing, terminal actuation, and verification; the formula does not price energy, duration, disposal, or creating known-`theta` specimens. Search over probe protocols is an additional cost and can be exponential in horizon and branching.

If there is only one irreplaceable substrate, if `theta` cannot be prepared/stratified, or if repeated trials alter the response law, the finite-sample certificate is unavailable. Testing only the deployment mixture certifies its mixture success, not a uniform guarantee over worlds. One can instead evaluate complete closed-loop policies directly on independently reset copies; an equally informed comparator can do that and may be cheaper than tensor estimation. The theorem creates no free experimental access.

## Prior art and comparator boundary

This report's proof and examples are original derivations for the stated fixture, but the minimax LP is classical decision theory; **novelty is UNKNOWN and should not be claimed**. Blackwell's experiment comparison concerns information available for a decision under a fixed downstream decision problem. Here the probe changes the physical opportunity for that decision, so the response masses must include survival and post-probe control effects. That observation is consistent with established dual control, not a displacement of it. [Blackwell, *Equivalent Comparisons of Experiments* (1953), DOI](https://doi.org/10.1214/aoms/1177729032) was checked at the journal landing page/metadata; the full original PDF was not accessible in this browse. [Feldbaum, *On a class of dual control learning systems* (1964)](https://www.mathnet.ru/eng/at11622) explicitly describes trial actions of cognitive nature combined with actions that bring a plant to the required state; the archive abstract was inspected, not the Russian full text.

Most importantly, merely stopping when all surviving mechanisms share a successful decision is already [Javdani et al., *Near Optimal Bayesian Active Learning for Decision Making* (AISTATS 2014)](https://proceedings.mlr.press/v33/javdani14.pdf): its Section 2 states the version-space-in-one-overlapping-decision-region criterion and Section 3 gives hyperedge cutting. Dynamic belief-support reach-avoid synthesis and antichains are also established; [Chatterjee et al., *Games with Imperfect Information: Theory and Algorithms*](https://lsv.ens-paris-saclay.fr/~doyen/papers/Games_with_Imperfect_Information_Theory_Algorithms.pdf), Sections 3.1–3.4, gives knowledge-set updates, winning constructions, and rank/strategy issues. [Junges, Jansen and Seshia, *Enforcing Almost-Sure Reachability in POMDPs*](https://arxiv.org/abs/2007.00085) explicitly targets safe winning regions. These are the strongest equally informed planning comparators; given the same acquired response data or a full model, they can represent the same decision problem. No computation, sample, energy, or reliability advantage is demonstrated here.

The next decisive test is on a real, single-use control substrate with two or more plausible hidden conditions. Specify goal/failure and the best no-probe and POMDP/dual-control policies **before** testing. Measure the world-stratified joint success tensor of a genuinely viability-preserving probe and terminal actions on matched specimens, with preparation and attrition fully charged; then prospectively deploy the LP rule on fresh blinded specimens. The probe has value only if the lower confidence bound on its worst-world success exceeds the matched comparator after total resource accounting. No such substrate or experiment was available in this investigation.
