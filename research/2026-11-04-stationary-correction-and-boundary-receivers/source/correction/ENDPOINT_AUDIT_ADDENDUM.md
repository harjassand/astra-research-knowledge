# Independent audit addendum: direct endpoint recovery supersedes graphic reconstruction

2026-11-04. Auditor: independent constructor. This addendum concerns the frozen PROOF.md with SHA256 fb5d4f943cf79c863019eb820f57f5c13683f1b6adc2b683f5c12fb6bab20314. It does not modify that file.

## Finding

The author's newly identified maximum-principle baseline is correct. It removes the graphic-matroid reconstruction and positivity-based state-alignment stages entirely. The original exact theorem remains true, but those stages are unnecessary for its stated observation model. Moreover, a spanning biconnected selected graph suffices for full reconstruction. This materially changes the assessment of the construction's leverage and its comparison with existing methods; it is not evidence that the original theorem is false.

## Direct proof

Use the column-generator convention, W pi=0, pi_i>0. For a nonzero response d=pi'−pi on an unknown pair {a,b}, the original finite-response identity is

W d = alpha(e_b−e_a), alpha != 0.

Set h_i=d_i/pi_i and L=W diag(pi). Because W pi=0, L has zero row sums. For each i outside {a,b},

0=(Lh)_i=sum_{j != i} W_ij pi_j (h_j−h_i).

Thus h_i is a positive weighted average of its predecessor values in the baseline graph. The division by pi is essential; extrema of d itself need not identify the pair.

Without loss of generality alpha>0. At any maximum of h, (Lh)_i<=0, so b cannot be a maximum; at any minimum, (Lh)_i>=0, so a cannot be a minimum. A nonterminal maximum propagates along predecessor edges until it reaches a terminal; irreducibility therefore places a at a maximum and b at a minimum.

Now use the spanning bidirected biconnected selected support. If a nontarget i shared the maximum with a, there is a path in this selected graph from i to b avoiding a. Along that path, at every nontarget maximum the harmonic equation forces every positive-weight neighbor also to equal that maximum. Consequently b would attain the maximum, contradiction. Therefore a is the unique maximum. Deleting b and applying the same argument proves b is the unique minimum. For alpha<0 the roles reverse.

Accordingly the unordered pair is exactly {argmax_i h_i, argmin_i h_i}. It takes a linear scan per response. Extra unperturbed directed edges merely add nonnegative averaging weights and do not invalidate the proof.

This uses only nonzero two-coordinate support of Wd, not the equality of the two physical rate multipliers. The original symmetric-barrier model is sufficient and keeps its finite-control reconstruction formulas; no broader physical calibration claim is needed.

## Generator reconstruction under the weaker graph hypothesis

Once all target pairs are known in physical state coordinates, solve the original homogeneous constraints

1^T K=0, K pi=0, and (K d_e)_i=0 outside the recovered pair.

A spanning biconnected graph has connected cycle matroid. The original cycle-rigidity argument applies directly with no permutation P: K_H W_H^{-1} preserves every incidence ray, so it is a scalar multiple of the identity on H. Hence K=cW. Choose the sign giving nonnegative off-diagonal rates, and normalize a clock convention. No graphic recognition, Whitney uniqueness, or row relabeling is required. Exact rational arithmetic remains polynomial in input length. This conclusion includes n=3 and n=4 without exceptional reconstruction cases.

Biconnectivity is sufficient, not asserted necessary. Additional unperturbed support can eliminate plateaus even when selected support is weaker. A full characterization of identifiability outside this sufficient regime is not claimed.

## Exact four-cycle verification

Let

W = [ -3,  1,  0,  2;
       2, -3,  1,  0;
       0,  2, -3,  1;
       1,  0,  2, -3 ].

Then pi=(1,1,1,1)/4. Double the two rates on pair {0,1} and update the two relevant diagonal entries. Exact rational stationary solution is

pi'=(22/105,29/105,4/15,26/105),
h=(-17,11,7,-1)/105.

The unique minimum is state 0 and unique maximum state 1. This selected cycle is biconnected but not 3-vertex-connected. Repeating separately for all four pairs gives spanning incidence responses with the single cycle dependence, so the original rigidity yields one common generator scale.

## Why some support condition is real

A triangle with a pendant state gives a concrete plateau. Let

W = [ -4,  1,  2,  1;
       2, -3,  1,  0;
       1,  2, -3,  0;
       1,  0,  0, -1 ].

Again pi=(1,1,1,1)/4. Double pair {0,1}. Then

pi'=(2/9,13/45,4/15,2/9),
h=(-5,7,3,-5)/45.

State 3 shares the minimum with target 0. An arbitrary argmin implementation can mislabel this out-of-scope response. This example concerns endpoint uniqueness, not a claim that all alternative inverse methods fail for every graph with an articulation.

## Direct noise condition

Let each measured coordinate of pi and pi' have absolute error at most eta, and pi_min>eta. Define R=max_i pi'_i/pi_i. Direct ratio estimation hhat_i=pihat'_i/pihat_i−1 obeys

||hhat−h||_infinity <= eta(1+R)/(pi_min−eta).

Proof: bound the numerator error in the quotient by eta/pi_hat plus pi'_i eta/(pi_i pi_hat), using pi_hat>=pi_min−eta.

Let g be the smaller of the true max-to-second-max and second-min-to-min gaps in h. If twice the displayed error bound is less than g, the unique extrema are recovered correctly. A common bound over all experiments supplies the multi-response condition. The later linear-system singular-value condition still governs stable recovery of W.

This replaces the much more elaborate rank-oracle margin for acquiring the endpoint labels. It is not a uniform sample guarantee: small baseline probabilities, weak perturbations, small endpoint gaps, and slow mixing can still be expensive. There is no claim that these true margins can be certified from arbitrary finite noisy data without a promise or confidence analysis.

## Prior and status

The maximum principle and Markov harmonic functions are classical. This auditor independently downloaded and inspected Hunter (2002), *Stationary Distributions and Mean First Passage Times of Perturbed Markov Chains*, Research Letters in the Information and Mathematical Sciences 3, 85–98. Corollary 4.1.2, equations (4.7)–(4.8), and the explanatory text on page 93 explicitly place the minimum and maximum relative stationary responses at the two perturbed destination states. Hunter treats changes to two entries in one row of a discrete-time transition matrix, whereas the present experiment changes two opposed rates of a continuous-time generator. Their stationary forcing has the same two-coordinate support; this is a strong direct predecessor, not a new maximum principle. The exact blind full-generator theorem is not claimed to be contained in Hunter.

Verified primary PDF:
https://mro.massey.ac.nz/server/api/core/bitstreams/8b373271-6b75-456d-84ab-1ecfd6b7cd19/content

No claim of a newly discovered general maximum principle or of previously unavailable experimental capability is warranted. A replacement proof should lead with this simpler same-data method, not retain matroid reconstruction as the missing acquisition operation.
