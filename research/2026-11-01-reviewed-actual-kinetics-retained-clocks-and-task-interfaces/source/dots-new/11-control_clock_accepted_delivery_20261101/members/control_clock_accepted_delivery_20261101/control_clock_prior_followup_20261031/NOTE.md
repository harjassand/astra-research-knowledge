# Post-freeze ordinary-RL comparison — not part of the clock receipt scope

Read 2026-10-31 after the 23:48 clock freeze. No frozen source was edited. This note strengthens the ordinary baseline, not the clock claim.

## Full-range ordinary model-based planning

Li, Wei, Chi, Chen, *Breaking the Sample Size Barrier in Model-Based Reinforcement Learning with a Generative Model*, [pinned arXiv v8](https://arxiv.org/pdf/2005.12900v8), Theorems 1–2, allow unnormalized tolerance a up to 1/(1-gamma), with O-tilde(nm/[(1-gamma)^3 a^2]) transition samples. Their empirical model and ordinary planners are retaining comparators. Setting a=epsilon/(1-gamma) gives O-tilde(nm/[(1-gamma)epsilon^2]) for our normalized fixed-goal task. Thus inverse-linear discount scaling is already ordinary, not a distinguishing clock capability. Theorem 1 also bounds value/policy iteration work; this is not a unit-cost planning oracle.

The older Azar–Munos–Kappen [2012 primary version](https://arxiv.org/pdf/1206.6461), Theorem 1, states a restricted a in (0,1); blindly substituting fixed normalized epsilon as gamma approaches one would exceed that version's stated range. The full-range later theorem avoids that comparison error.

## A standard finite-net all-goal retention extension (our deduction)

Fix the same received partition independently of the new transition data. A block/action reward table has d=mr entries. For normalized values, both a fixed policy's value and the optimal value are 1-Lipschitz in the sup-norm reward difference. Take a sup-norm epsilon/8 net of [0,1]^d with M<= (1+8/epsilon)^d points. Give each net task normalized error epsilon/2 and failure probability delta/M in the primary fixed-task theorem. Use the SAME empirical transition data and the same independently drawn reward-perturbation array for every net task; union bounds need no task independence, and the perturbation magnitude is common because all target accuracies coincide.

On the simultaneous event, a future adaptively chosen reward is rounded to its nearest net table. Planning for that net table gives regret at most epsilon/2+2(epsilon/8)<=epsilon. The net is an analysis device: rounding takes O(d) operations, no exponential enumeration or stored policy cover is required. The sample logarithm gains log M=O(d log(1/epsilon)), while the retained empirical-model planner remains n-state. This is a paper-level ordinary baseline, not an executed or new all-goal theorem. Exact planner arithmetic/perturbation realization or a separately paid finite-bit approximation must still be supplied; the clock prototype does not certify that backend. Repeating one global acquired event supports adaptive goals, unlike pretending a fixed-goal bound is automatically uniform.

Consequently, many-task flexibility by itself is not enough. The possible remaining distinction is a small, nonpredictive decision representation and its consumer cost, plus an instance-sensitive response/accuracy-tail tradeoff. Whether that saves enough total work remains unestablished.

## Current span/mixing theory: keep additive costs and assumptions

Wang, Blanchet, Glynn, [*Optimal Sample Complexity of Stable Discounted Markov Decision Processes*, arXiv:2302.07477v4](https://arxiv.org/pdf/2302.07477v4), Corollary 1.1, has a span-sensitive leading term, but its displayed policy bound also contains an epsilon-independent (1-gamma)^(-5) term. Remark 1's procedure for learning the span upper bound pays an additional inverse-cubic pilot. Corollary 2.1/Remark 2 retain additional costs and a supplied all-policy mixing upper bound. These details prevent promoting an abstract's leading term to a free acquired clock. They do not make the method weak: it remains a strong ordinary component under its actual assumptions.

Zurek and Chen, [*Span-Based Optimal Sample Complexity for Average Reward MDPs*, arXiv:2311.13469v2](https://arxiv.org/pdf/2311.13469v2), Theorem 1, improves discounted planning under weak communication and a bias-span parameter, with explicit H<=1/(1-gamma) and a<=H conditions. It does not require all-policy mixing. Those task/parameter regimes differ from our reducible, action-initialized pair certificate; neither theorem should be claimed to dominate the other without receiving the assumptions and full costs.

No historical novelty or practical superiority follows from the remaining distinction. These are useful controls on the next scientific question, not grounds to make another toy workload harder.
