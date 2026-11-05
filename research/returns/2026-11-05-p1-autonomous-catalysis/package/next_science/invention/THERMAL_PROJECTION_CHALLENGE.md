# Independent challenge of the thermal-projection turnover bound

No counterexample was found to root's equations (1)–(4) under finite irreducibility, positive bath links, resolved-channel bookkeeping and correct target reward. The Poisson identity has the right sign. The thermal projection is a mathematical same-architecture infinite-bath-rate comparator, not automatically a realizable catalyst or the capture-off material.

## Exact sharpness construction

Four states are (A,0),(A,1),(B,0),(B,1). At either chemical configuration the thermal rates are 0→1: gamma q and 1→0: gamma. Chemical channels (A,0)↔(B,1) and (B,0)↔(A,1) both have rates c+,c−, forward product count +1 and reverse count −1. Impose c+/c−=q exp(A). Thus the gate free-energy gap is −kBT log q, there is one chemical affinity A, and sigma=A J. All reverse channels and work supplies are paid.

Write t=q/(1+q), B=gamma(1+q), s=c++c− and u=c+/s. Symmetry gives chemical marginals one half. Exactly,

\[
p=(su+Bt)/(s+B),\quad\delta=p-t={s\over s+B}(u-t),
\]

\[
J=B\delta,\quad J_{th}=s(u-t),\quad J-J_{th}=-s\delta,
\quad w_A=w_B=-s.
\]

For the sharp binary coefficient c(t), V=c(t)s²/B, hence

\[
{(J-J_{th})^2\over\sigma V}
={s\over s+B}{u-t\over[\operatorname{logit}u-\operatorname{logit}t]c(t)}.
\]

Choose u at the maximizer defining c(t). The second factor is one. Every finite s gives a fully reversible finite-rate model, and the ratio is s/(s+B). Reaching 1−epsilon requires s/B≥(1−epsilon)/epsilon. Thus c(t), including the V_mu→Vmax step when contrasts are constant, cannot be improved uniformly over the rate-unbounded class.

At t=1/2 take c±=Lambda exp(±A/2). The original Pinsker ratio is [2 tanh(A/2)/A]s/(s+2gamma), tending to one as A→0 and s/gamma→infinity. This checks all factors of two independently.

**Important limitation:** the sharpness family is a slowdown, J/Jth=B/(s+B)<1. It does not attain the positive-gain upper bound. Near-saturation also requires large gross reversible chemical activity compared with the bath rate. Mathematical sharpness of an absolute bound is not a useful catalytic capability.

## Stronger exact-entropy envelope

For supplied chemical weights mu_i, contrasts w_i and B_i=gamma_i(1+q_i), set t_i=q_i/(1+q_i) and phi_i(p)=(p−t_i)[logit(p)−logit(t_i)]. The sharpest upper bound using only these local quantities and exact bath entropy budget S is

\[
\max_{0<p_i<1}\sum_i\mu_i w_i(p_i-t_i)
\quad\text{subject to}\quad\sum_i\mu_iB_i\phi_i(p_i)\le S.
\]

Use −w for the lower direction. It is at least as strong as Pinsker or the global c(t) bound. It retains the small-budget curvature phi_i(p)≈(p−t_i)²/[t_i(1−t_i)], which can be much stronger for a rare thermal mode. Strict convexity follows from phi_i''(p)=[p+t_i−2pt_i]/[p²(1−p)²]>0.

For positive multiplier lambda, each coordinate solves

\[
B_i\left[\operatorname{logit}p_i-\operatorname{logit}t_i
 +{p_i-t_i\over p_i(1-p_i)}\right]=w_i/\lambda.
\]

The left side increases strictly from −infinity to infinity, so its scalar root is unique. A second monotone scalar search enforces the total budget. This supplies a constructive numerical operation, not a new physical mechanism. Unacquired mu_i cannot be assumed known; actual chemical stationarity further restricts feasible occupancies.

## Primary comparison

Horowitz, Zhou and England, *Minimum energetic cost to maintain a target nonequilibrium state*, PRE95,042102 (2017), [arXiv1703.04722](https://arxiv.org/abs/1703.04722), derives the undriven-edge dissipation maintenance cost and its attainment by fast driven channels. Equations (1)–(4) and the general argument were read. The entropy half and fast-control sharpness idea have exact prior art.

Dechant and Sasa, *Fluctuation-response inequality out of equilibrium*, PNAS117,6430–6436 (2020), [DOI10.1073/pnas.1918386117](https://doi.org/10.1073/pnas.1918386117), full text PMC7104339, gives |E_Pf−E_Qf|≤inf_{h>0}[log E_Q exp(h sign(Delta)(f−E_Qf))+D(P||Q)]/h. Root's Poisson-corrected observable and conditional thermal reference fit this general response framework, while still requiring the correct distributions and entropy accounting.

Hilder and Sharma, *Quantitative coarse-graining of Markov chains*, SIAM J Math Anal56,913–954 (2024), [DOI10.1137/22M1473996](https://doi.org/10.1137/22M1473996), [arXiv2201.10256](https://arxiv.org/abs/2201.10256), uses conditional-expectation generators, entropy and functional inequalities without scale separation. Theorem3.1 was read. Its reference uses the full-chain stationary conditional distribution, whereas root uses bath-only equilibrium. Its zero stationary marginal error is therefore not root's current comparison; that theorem does not directly replace root's claim.

Downloaded sources and hashes are in `primary/projection_prior_manifest.json`. The comparisons do not support calling entropy-controlled coarse-graining or response bounds new machinery. An identical statement with root's specific stationary-current comparator was not established in the sources checked.

## Consequence and limit

The theorem closes a real loophole in naive per-turnover pulse estimates: rapid reversible donor traffic is permitted but its maintained conditional gate distortion is paid by full entropy production. This is a useful conditional deduction. If w is unrestricted, slow traps and large reversible traffic can make Vmax arbitrarily large. Neither a universal bound on the observed catalyst nor a new microscopic mechanism follows. A nonvacuous physical conclusion requires the bath generator, complete-cycle contrasts and architecture, or independent material constraints on them.

## Completed finite checks

`FINITE_GATE_COEFFICIENT.md` derives an explicit general finite-bath coefficient from one conditional Poisson solve, avoiding an unspecified functional-inequality oracle. It is a standard entropy/current Cauchy–Schwarz construction and reduces to the sharp binary secant coefficient.

`projection_exact_witnesses.py` checks selected synthetic six-state models using exact rational arithmetic for local detailed balance, stationary probabilities, the thermal projection, its Poisson equation and the corrected-current identity. One model gives positive gain 3.51517409078, but the maximum-based bound is 4479.83123. Another gives positive gain 1.01986877632 with the nonvacuous upper bound 1.60205835604. Entropy uses the exactly specified affinity log(100), numerically evaluated only after all rational identities are checked.

The first model was reduced to an exactly soluble two-cycle mechanism in `POSITIVE_GAIN_TOPOLOGY.md` and `projection_two_cycle_witness.py`: J=61105/87342, Jth=60330/303697, gain=3.52176840226. Thermal equilibration overpopulates a slow branch; finite gate memory favors the other productive cycle. All reverse rates and one chemical affinity are paid. Its zero gate splitting, rate span and bath timescale are explicit, so it is not evidence for the source's 0.126 eV/41 ns mechanism. A simple single ring is monotone in every symmetric bath-edge rate and cannot show this positive deviation; the two-cycle construction evades that topology restriction.

These checks establish consistency, possible positive response, conditional nonvacuity and absolute-bound sharpness. They do not establish novelty, empirical identification, sharpness of the positive-gain bound, or a civilisation-changing endpoint.

## Independent check of the transfer constructor's causal-comparator counterexample

The complete four-state model in `../transfer/THERMAL_RECYCLING_COUNTEREXAMPLE.txt` was independently read. Its positive paired rates, local detailed balance, distinct parallel capture/product channels, stationary probabilities, equal thermal projections and excitation-lineage definition are consistent. It supplies real internally relayed mode energy and causal capture benefit while the capture-on conditional gate distribution is exactly thermal and its bath entropy production is zero. The capture-off model lies below the common thermal projection. This is not a counterexample to root's mathematical bound; it is a counterexample to interpreting that bound as an upper limit on the whole causal benefit of energy routing.

For two models sharing a positive Jth, define `g(kappa)=1+kappa/2+sqrt(kappa+kappa^2/4)`. The two-sided individual inequality gives `1/g(kappa_m) <= J_m/Jth <= g(kappa_m)`. Therefore

\[
{J_{on}\over J_{off}}\le g(\kappa_{on})g(\kappa_{off}).
\]

If ON is known to be exactly at Jth, its factor is one. Acquiring both complete-cycle coefficients remains necessary. A zero conditional gate entropy in ON alone cannot exclude trajectory-level retained-energy routing or causal improvement over OFF.
