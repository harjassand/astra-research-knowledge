# Full-rank noise forbids finite exact heralded frame recovery

2026-10-29. Root derivation; independent review pending. This is a boundary for the newly acquired quantum frame programs, not a claimed novel general no-programming theorem.

## 1. Same-support program lemma
Let rho_a and rho_b be finite-dimensional positive program states with the same support. Then there are finite positive constants l,u with l rho_b <= rho_a <= u rho_b. For a fixed trace-nonincreasing completely positive processor, supply a maximally entangled payload-reference input. Positivity gives l J_b <= J_a <= u J_b for the successful output Choi operators. Therefore they have exactly the same support (including simultaneous zero). They cannot be nonzero multiples of two distinct pure unitary Choi states. This permits arbitrary finite-dimensional ancillas, known controls and heralds. It does not prohibit pure, distinct, nonorthogonal programs: their one-dimensional supports differ.

## 2. Finite adaptive source-query version
Let N_a,N_b be memoryless channels with positive definite Choi matrices. There are l,u>0 such that l N_b <=CP N_a <=CP u N_b. Fix any N-slot adaptive known quantum circuit, with arbitrary protected coherent memory, intermediate measurements and a final success flag. Feeding the same channel into each slot and telescoping the multilinear CP order yields
 l^N E_b <=CP E_a <=CP u^N E_b.
The inequality also holds on each fixed classical outcome branch and after summing success branches. Hence the output successful channels have identical Choi support. They cannot implement distinct exact unitary channels with positive success probabilities. The processor may receive the unknown payload after acquisition, or before/throughout the queries: the CP-order argument covers both.

A protocol stopping after a finite but unbounded random number of calls is a countable sum of finite-depth successful subinstruments. If its total success for a is p_a U_a, every positive finite-depth contribution has Choi support contained in the U_a ray. A nonzero contribution for a has the same nonzero support for b, while every b contribution must lie in U_b. Thus two distinct exact target unitaries remain impossible. Infinite protected memory or genuinely infinite-depth outputs are not covered by this finite-dimensional finite-halting formulation.

## 3. Arbitrarily small full-rank contamination
For any finite-dimensional same-input/output channel family N_R and 0<eta<=1, define N_R^eta=(1-eta)N_R+eta D, where D(X)=Tr(X) I/d. Its Choi is positive definite. Therefore an exact heralded gate varying with R cannot be acquired from finitely many calls for all R at any eta>0, even with arbitrary trusted coherent processing. This is a noise-robustness discontinuity in the EXACT gate objective, not a prohibition on approximate recovery, quantum error correction, useful storage, or asymptotic learning.

The exact dark-support constructions operate at eta=0 and are consistent with this result. Common dark support, even without an occupation gap, is not interchangeable with approximately dark support. A correct next architecture should target a quantitative approximate gate, rather than silently extending exact heralding to generic contamination.

## 4. A quantitative finite-query consequence
For the depolarizing-contaminated d-dimensional channels above, J(N_R^eta) >= eta I/d and J(N_R^eta) <= [d(1-eta)+eta/d] I. Thus pairwise N_a^eta >=CP r N_b^eta with r=eta/[d^2(1-eta)+eta]. For N calls set c=r^N. On maximally entangled payload input, successful subnormalized outputs satisfy J_a >= c J_b. Use NORMALIZED Choi states here, so Tr J_x=p_x.

Let P_a,P_b be the unit target Choi projectors and s=Tr(P_a P_b). If normalized accepted output for b obeys trace distance D(J_b/p_b,P_b)<=epsilon_b, its mass outside P_a is at least 1-s-epsilon_b. Therefore the trace-distance error of a obeys
 epsilon_a >= (c p_b/p_a) max(0,1-s-epsilon_b).
In particular with comparable p_b>=p_a and epsilon_a,epsilon_b<=epsilon, epsilon >= c(1-s)/(1+c). This bound can be exponentially weak; it establishes a finite error floor, not an optimal resource law or practical lower bound. If p_a=0, no normalized accuracy is asserted.

## 5. Positive continuity fallback, not a useful precision promise
If two N-use physical source instruments differ by at most epsilon per use in half diamond norm uniformly over the admitted histories, hybrid composition bounds the JOINT output-instrument distance by N epsilon. This requires a genuine full-interface bound, not matching a reduced marginal. If one is the ideal exact successful gate with probability p0 and the actual accepted probability is p>0, triangle and normalization give conditional output/reference distance <= 2N epsilon/p (capped at1); corresponding success probabilities differ by <=N epsilon. Known-control errors add through the same hybrid bound. This is only a sufficient accounting rule and can be vacuous at rare heralds.

## Sources and priority
This elementary support/CP-order argument is built from standard quantum programming and channel positivity. Primary predecessor context being checked: Nielsen--Chuang no-programming; probabilistic programmable processors; Pavlicko--Ziman, robustness of probabilistic unitary storage/retrieval, PRA106052416 (2022). No historical novelty is claimed. Exact source passages and finite examples will be appended before acceptance.

Primary source actually read: Pavlicko--Ziman PRA106052416, https://www.quantum.physics.sk/rcqi/research/publications/2022/rcqi2022pavlicko_PhysRevA.106.052416.pdf , pages1--2, introduction and quantum-network/PSAR setup. Their task starts from noisy uses of the target phase gate and studies noisy retrieved channels. Our frame source need not supply even one use of the unknown frame unitary, so direct storage/retrieval machinery is a comparator but cannot be inserted as a free oracle. The present proof remains elementary and makes no historical-priority claim.
