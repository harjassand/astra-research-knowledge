# Independent receiving: finite coherent coarse spectral acquisition
2026-10-29. Reviewer `producer-workspace/review_finite_quantum_sampler`.

## Decision and contract
PASS finite measurement-interface construction, with mandatory `FINITE_INTEGER_SCHEDULE_CLARIFICATION.md`. This is separate from the already received mathematical coarse-disturbance lemma and does not receive approximate-central recovery. Source originals remain immutable.

B is a fixed Hermitian norm-at-most-one signed Jordan-program Hamiltonian with the four-pair W=4 interface. The ordinary same-source outputs must be fresh independent programs throughout target storage. Trusted whole-register permutations, clean coherent work, finite known rotations and protected storage remain paid. Neither the source nor its preparation is inverted.

## QPE and coherent measurement comparison
For phase phi, the geometric-series QPE distribution has p_k<=1/(4 M^2 dist(phi,k/M)^2), using |sin(pi x)|>=2|x| on the circular half interval. Summing the two inverse-square tails gives the displayed conservative 1/[2(M delta-2)] bound. With delta=g/4 and M>=4096/g, one-run failure is much less than 1/16. True phases lie in [-1/4,1/4], so converting circular estimates to signed values introduces no additional failure outside this event. Conditional on each eigenvalue, coherent repeated QPE registers have product outcome probabilities. The odd-median union bound is valid even though the registers have not been measured.

For a fixed eigenvalue b, write U_b for all coherent QPE plus median computation. Copying its bin to a clean register and applying U_b^dagger gives overlap with the clean-work/correct-bin ideal vector equal to the probability of the correct bin, not its square root. The equality follows by summing |alpha_y|^2 over all work outcomes assigned to that bin. On an eigenvalue farther than g from boundaries this overlap is real and at least 1-beta, so the isometry vector distance is at most sqrt(2beta). On the remaining subspace it is at most two. The construction must uncompute all phase registers: measuring a fine phase and merely forgetting it does not preserve same-bin coherence.

For any eigenvalue, the discrete fraction of offsets within distance g of a boundary is at most 2g/w+1/L. This includes ties and is the grid-counting bound for a single circular arc. The width restrictions w<=1 and spectrum [-1,1] prevent a physical wrap ambiguity: cyclic bin names are just relabelings of the ordinary bins on this spectrum.

For each offset, split an arbitrary target-reference vector into its good and boundary spectral components. The isometry difference is at most sqrt(2beta)+2 sqrt(p_boundary). After averaging independent exposed offsets, Jensen and the uniform per-eigenvalue boundary probability imply
half-diamond <= sqrt(2beta)+2sqrt(2g/w+1/L)
<=nu/4+sqrt(3)nu/8<nu/2.
This bound holds for every reference purification and therefore for the full channel. Reading the copied bin and discarding work only contract trace distance. It is a comparison of complete unnormalized instruments, not a conditional-bin fidelity estimate. Direct sums, degeneracies and arbitrary source-independent background are allowed.

## Actual source simulation and finite arithmetic
The accepted quadratic collision receipt supplies full-reference controlled Jordan simulation with full diamond <=4W^2 t^2/n; using 64t^2/n as a half-diamond allowance is conservative at W=4. Each cycle has four signed fresh-pair collisions and consumes eight ordinary source outputs. Each selector is newly prepared and discarded. The same source state label used twice still requires distinct independent copies.

For forward QPE and its inverse there are 2sm evolutions. The additive rational schedule uses u_l=2^(l+1)>=pi 2^l/2 and U=4sM, with sum u_l=4s(M-1)<U. Choose n_l=ceil(16u_l)+ceil(64u_l U/tau). Then n_l>=16|t_l| enforces the small-angle condition, and
sum 64 t_l^2/n_l <= tau sum u_l/U < tau.
The count is at most 16U+64U^2/tau+4sm cycles, hence eight times that many source preparations. All ceilings are exact rational operations. This clarification removes any implicit exact comparison of a pi-dependent expression against an integer. Negative-time evolutions are simulated with fresh forward programs and negative known rotation coefficients, not by reversing previous noisy collision channels.

The whole ideal algorithm has a public polynomial number of known gates; approximating each relevant controlled rotation to the stated operator norm allocation gives total half-diamond <=nu/4 by a circuit hybrid. Finite QFT phases are included. Median and dyadic-bin comparisons are reversible finite arithmetic, not real-number oracle calls. They admit polynomial gates and O(s log M) workspace by retaining the estimates and using reversible comparisons/counters with uncomputation. The simulation hybrid is valid even with those work registers entangled and with previous programs discarded, because the collision comparison is global with all references.

Summing ideal coarse comparison <nu/2, collision budget nu/4 and synthesis budget nu/4 gives <nu. M=O(nu^-2 w^-1), s=O(log(1/nu)), so the conservative source count O(nu^-5 w^-2 polylog(1/(nu w))) is consistent. Three D-carriers suffice while coherent phase space is O(s log M), NOT the earlier O(log M) classical-median workspace. Small input bit height and canonical dyadic nu,J are part of this finite schedule; arbitrary requested numerical encodings must first be paid to convert.

## Composition and what remains open
Apply the mathematical random-coarse disturbance lemma to the ideal stages. The new stagewise complete-instrument errors hybrid through subsequent record-dependent channels and add to at most sum nu_j. Any fixed optimal decoder of the ideal record channel loses at most that much entanglement fidelity, proving the claimed existential retained Fopt bound for the actual record channel.

Nothing supplies that optimal decoder, proves nearby small-dimensional response blocks, constructs consistent approximate Clifford axes, or removes the rank/disturbance tradeoff. No source-memory extension, historical novelty, hardware/practical advantage or efficient approximate-central decoder is received.

## Diagnostics
Independent `check_independent.py` explicitly builds small coherent QPE matrices, copies median bins and uncomputes for 72 configurations, including s=3 coherent instances. The predicted correct-bin overlap and squared isometry-distance identities agree within 8.3e-15. Nine public rational schedules check total collision error, counts and ideal instrument constants; these schedules are enormous and were not executed. The author 36 small instrument diagnostics replayed, including same-bin coherence 0.989459 versus 0.047350 after incorrect full-phase measurement. None of these tests is a native collision/QPE hardware execution.
