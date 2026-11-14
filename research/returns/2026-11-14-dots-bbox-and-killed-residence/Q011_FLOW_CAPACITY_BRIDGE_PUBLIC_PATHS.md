# Acquired paths to capacity: constructive bridge and remaining cost

For a distribution over source-to-target monotone paths, let phi(e) be its edge-occupancy probability. This is a unit flow. Its resistance is
E = sum_e phi(e)^2/c(e) = E_path[sum_{e in path} phi(e)/c(e)].
Thus acquired paths provide an unbiased resistance estimator IF their occupancy probabilities are computable. Upper bounds on occupancy yield upper bounds on E after expectation, or deterministic bounds if every path sum is bounded. Thomson gives C >= 1/E. Inverting a finite noisy empirical resistance mean is NOT a rigorous lower bound or an unbiased capacity estimator.

For the recovered R200 four-corner law, acquisition and native paths now run, but an efficient computable full occupancy oracle (including all path preimages and all stages) has not been established. Existing analytical overlap bounds are useful upper bounds, not such an oracle. This is the precise missing step in using that sampler directly for resistance acquisition.

## A full executable finite bridge
On the complete 3x3 torus soft-source model, choose a uniformly random spin permutation and fill its first five sites. The source reservoir injects through all-minus only; this is a valid unit flow in the full source network, not an assertion that the physical source is all-minus. Every level-j upward edge has occupancy 1/[choose(9,j)(9-j)]. All conductances, source cost, and native rates are retained.

Exact finite enumeration (floating evaluation) gives resistance 3142.4734694, hence flow lower bound C>=0.000318220666. The independently solved full-network capacity is 0.005679329890, a factor 17.847 larger. 10,000 sampled paths gave resistance mean3154.8533, standard error43.8926. A deterministic all-path resistance bound17369.847619 also follows from the sum of layer maxima.

For the cut separating states of size<=2 from larger states, let w_e=c(e). A normalized proposal mixes half conductance law with half the monotone flow's crossing law. The conductance component supplies full support, including reservoir edges that cross the cut. For a proposed oriented edge x->y, run independent native killed chains from x and y and let Hx,Hy indicate absorption at the source reservoir. Then
Y = w_e(Hx-Hy)/q_e
is unbiased for capacity. It may be negative. This construction does NOT assume that a difference of committors is available as a Bernoulli oracle, or that soft-source killing preserves monotone coupling.

Actual run of2,000 draws: mean0.0055669041, standard error0.0003729199;14,658 native jumps;6,701.0753 total simulated physical-time units;0.146 wall seconds. Exact finite reference relative variance is8.77769. Full-state enumeration and matrix solution used as reference are setup costs, not part of a claimed scalable estimator.

## Resource-normalized conclusion
This is a working finite sampler-to-flow-to-capacity bridge, not a scalable breakthrough. Flow quality certifies a lower bound and helps normalize variance, but does not make endpoint absorption cheap. General signed decisions have second moment h(x)+h(y)-2h(x)h(y), not h(x)-h(y). The earlier Bernoulli-oracle diagnostic therefore cannot be used as the variance guarantee for this implementable algorithm. An efficiency claim needs both full-support proposal acquisition and an upper bound on decision work, as well as overlap/flow control. The native-path decision burden remains open at R200.

Reproduce: OPENBLAS_NUM_THREADS=1 python flow_capacity_bridge.py. The script also reruns the earlier diagnostic because it imports its finite model through runpy. JSON records complete numerical results.
