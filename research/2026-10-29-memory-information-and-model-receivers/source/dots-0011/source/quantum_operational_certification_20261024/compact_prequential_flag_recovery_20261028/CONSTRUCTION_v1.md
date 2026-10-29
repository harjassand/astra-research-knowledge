# Compact prequential quantum-flag recovery: private terminal service
2026-10-28. New candidate, pending independent review. This is a representation-specific construction, not an unrestricted decoder or process-learning theorem. It extends the private-terminal-time argument of ordinary_prequential_terminal_memory_recovery_20261028.md (N1161) with a different, entangled acquisition instrument and hence a DIFFERENT actual source-memory occupation. N1162/N1163 multiple-payload/selector conclusions are not imported.

## 1. Interface and objective
At each complete call the same causal CPTP source maps a fresh n-qubit logical input and arbitrary retained source memory to n data qubits, a named accessible r=2^g dimensional flag, and updated memory. Current roles, learner coins, receiver controls and terminal time are private; public scheduling is padded. Fresh payload plus its arbitrary reference initially factor from all source memory/acquisition randomness and is held in trusted storage. The delivered output is isolated; there is only ONE payload and no later service. Source memory is not reset or identified.

Define the length-N all-probe experiment below. At its actual history h before t, E_th is the conditional fresh-input channel. Let sigma_th,x be the unnormalized flag block obtained by projecting its normalized Choi state onto Bell label x in the full A=4^n Pauli alphabet. The blocks are positive and sum_x Tr sigma_th,x=1 even for coherent channels. A flag POVM M=(M_x) followed by Pauli P_x correction has Bell reward

 f_th(M)=sum_x Tr(M_x sigma_th,x).

The comparator is one FIXED POVM on this experiment's EXPECTED visited histories: max_M N^-1 sum_t E_h f_th(M). It is not the hindsight optimizer of each path, a future frozen-noise oracle, or a controller changing memory occupation. For arbitrary coherent channels it is a restricted correction-class oracle. For Pauli+flag channels at every visited history this class includes each full-CPTP recovery optimum, but the best fixed decoder need not attain the sum of individually varying optima.

## 2. Actual sparse gradient and pathwise learning
Each probe uses n trusted Bell pairs: send one half of each through the source and retain n reference halves. Measure data/reference pairs in the Bell basis to obtain full x, leaving the flag. Independently choose a flag Pauli W uniformly among r^2 labels and measure its parity b. For W=I set b=1. Define the tuple G_t with only one nonzero block

 (G_t)_x = r b W.

Conditionally on the actual past, E G_t=(sigma_th,x)_x. Its squared tuple Frobenius norm is exactly r^3. This conditional statement uses the actual flag/Bell measurement instrument, not imaginary samples from a frozen memory channel.

The POVM set K={M_x>=0, sum_x M_x=I_r} has squared diameter at most 2r, since sum_x Tr M_x^2<=r and cross inner products are nonnegative. Start M_1,x=I_r/A; its squared distance from any comparator is at most r. With N a square (take power of4), step a=1/(r sqrt N), update by Euclidean projection of M_t+a G_t onto K. For exact projection the usual distance expansion gives PATHWISE

 sum_t <G_t,M_*-M_t> <= r/(2a)+a N r^3/2 = r^2 sqrt N.

Conditional unbiasedness and taking infimum only over fixed comparators give expected mean reward regret <=r^2/sqrt N. No iid or uniform confidence event is used.

A finite implementation may return an exactly feasible iterate whose squared distance objective is within xi=1/(256 N^2) of the exact minimum. Strong convexity gives weighted tuple distance <=sqrt xi. Both iterates and comparator lie in K; the extra squared-distance comparison is <=2 sqrt(2r) sqrt xi+xi <=4r sqrt xi. Summing adds at most r/(8a), so regret <=(9/8)r^2 sqrt N. This deliberately loose bound covers all r,N>=1.

## 3. Exact compressed representation and finite projection
At time t all never-observed labels have the SAME effect B, by initial symmetry and permutation-invariant Euclidean projection. Store each observed label's effect and the default, with K0=A-s unseen labels, s<=t-1. When a new x appears, split its old B off from the default before updating. This requires no alphabet enumeration.

For K0>0 store the AGGREGATE C=K0 B. Given the corresponding projected center blocks Y_i and Y_C, solve the known finite convex problem

 min sum_observed ||M_i-Y_i||F^2 + ||C-Y_C||F^2/K0,
 subject to M_i,C>=0 and sum_i M_i+C=I.

This is exactly the full-alphabet Euclidean projection by symmetry, not a relaxation. There are at most N+1 r-by-r blocks; 1/K0 has O(n) bit length. If K0=0 omit C. A rational interior center for m actual blocks is I/m. A Schur-complement quadratic epigraph has rational coefficients and polynomial bit length in n,N,r and requested precision. Ill-conditioning costs precision depending on log K0; it is not a free unit-cost operation. Require a paid polynomial-cap convex solve on a fixed dyadic grid, with independently checked exact feasibility and objective slack xi.

Explicit feasibility repair is available: if Hermitian approximate blocks H_i have lambda_min>=-delta and ||sum H_i-I||op<=delta, put H'_i=H_i+(I-sum H_i)/m, then M_i=(H'_i+2delta I)/(1+2m delta). These sum exactly to I and are PSD. Standard finite-dimensional norm bounds make repair and fixed-grid rounding cost polynomial in m,r times delta, also in the weighted norm because 1/K0<=1. Choose delta to fit xi after bounding the known objective's Lipschitz constant on the bounded near-feasible set. Fixed-grid output prevents recursive denominator growth. A run failing its exact feasibility/slack contract stays physical by fallback but does not receive the optimization guarantee. This is a paid finite solver contract, not a hidden unknown-channel oracle.

## 4. Random compact realization preserving the ENTIRE decoder
An empirical-objective-preserving deterministic pruning is inappropriate online: it need not preserve reward on the next unknown source. Instead implement an unbiased random decomposition.

First, when K0>0 sample one uniformly random actual unseen label z and replace the aggregate effect C by a single effect at z. Every unseen label then has mean effect C/K0=B; observed effects are unchanged. A rank/select operation on a trie of observed labels maps a uniform integer from 0,...,K0-1 to the corresponding unseen label in polynomial time and O(n)-bit arithmetic. Use capped exact integer rejection and charge exhaustion probability. There is no A-label loop.

For the resulting m<=N+1 effects, if m>r^2 find a nonzero REAL rational dependence sum_i v_i M_i=0. Nonzero effects force both signs in v. The allowable interval for t in M'_i=(1+t v_i)M_i has finite endpoints t_-<0<t_+. Choose t_+ with probability -t_-/(t_+-t_-), otherwise t_-. Then E[t]=0; the POVM remains positive and normalized, at least one effect vanishes, and EACH effect is preserved in conditional expectation. Repeat until <=r^2 effects. Consequently the averaged correction CP map equals the original full-alphabet POVM decoder on EVERY input, including joint source-memory/reference inputs, not just its measured reward. The randomness must remain private and unavailable to the source at that call; no future output interactions are covered.

This is conventional convex geometry. Exact rational elimination and endpoint coins give existence and a finite algorithm; polynomial bit-complexity of repeated elimination is NOT yet established here. A rigorous bounded-precision or rational polytope-decomposition implementation with a single complete operational error budget remains a live obligation. The statistical and compressed-projection theorem does not wait on claiming that unproved bit bound. A noncompact implementation of the m-outcome observed-plus-random-default POVM is already finite and polynomial-size in N,r, with at most N+1 outcomes.

For a given compact realization, use the flag Naimark isometry sum_i |i> sqrt(M_i), dimension <=r^3, and conditionally apply at most n local Paulis. Flag synthesis/control, private coin generation and classical pruning costs are paid. Compiler error and approximate coins belong in a complete implementation budget, not the statistical regret.

## 5. Private terminal time and what is gained
Choose T uniformly from1,...,N at initialization with private fair bits. Before T use the exact probe/update instrument; at T send the independently stored payload through the same complete source port and apply the precomputed decoder M_T (or its averaged exact random realization), isolate output and terminate. The prefix conditional on T=t is exactly the all-probe prefix. Therefore the actual averaged terminal channel equals the average of those history-conditioned decoded channels, even tensor arbitrary external reference. Its Bell loss is at most

 min_fixed M N^-1 sum_t E_h[1-f_th(M)] +(9/8)r^2/sqrt N + nu,

where nu is ONE declared whole-process implementation discrepancy relative to this ideal experiment. It does not silently move the comparator to the imperfect experiment's altered memory occupation. The optional private OUTER Pauli twirl preserves Bell fidelity and makes the reduced n-qubit terminal channel Pauli, hence half-diamond error equals Bell loss; pay 2n key bits and pre/post controls and retire the key.

For fixed accessible flag dimension, the acquisition excess is independent of 2^n: N=O(r^4/epsilon^2), at the cost of n protected Bell reference halves and n Bell readouts on EACH probe. This is not the ordinary-probe unrestricted decoder theorem's information interface or oracle. Worst-case N calls, mean (N+1)/2; all classical compilation time contributes to payload holding time. No high-fidelity guarantee follows when the correction-class comparator is poor. No capacity, rate, multi-payload, free gauge-compression, historical novelty or advantage over an equally informed conventional online learner is asserted.
