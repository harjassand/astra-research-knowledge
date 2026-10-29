# History-uniform noisy frame programs: finite timeout changes availability, not quality
2026-10-29. Author draft. This strengthens the previous expectation/coupling treatment for one explicit IID family, not arbitrary source memory. Generic growth and recursive SWAP purification are established prior methods.

## Assumed physical family
Use the separately derived memoryless two-qubit channel N_eta=(1-eta) collective-twirl+eta D4, with fixed unknown local frame and 0<=eta<1. Coherent acquisition yields independent minus records sigma=x Pc+a PW, x=eta/(8+eta), a=1/(8+eta), and flag probability p_minus=(8+eta)/18. Here dim W=8, c=vecR/sqrt3. Known-control and protected-memory assumptions remain paid. A known upper bound eta_U<1 suffices for the following schedule.

## Uniform growth-history invariant
Condition on ALL classical acquisition/growth outcomes so far, including waiting times, but not on any eigenbasis label measurement (none is performed). Symmetry under U(W) implies the maintained wedge^k state is a mixture of the two irreducible occupation sectors: dark label absent or present. Let r be the dark-present weight. Fresh records are independent despite conditioning on this past. The two unnormalized transition matrices on [absent,present] are
 S=[[ (8-k)a/(k+1), 0 ],[ x/(k+1), (9-k)a/(k+1) ]],
 F=[[1-colsum(S)_0-kx/(k+1)^2, (9-k)a/(k+1)^2],
    [kx/(k+1)^2,1-colsum(S)_1-(9-k)a/(k+1)^2]].
These follow from the exact Lüders instrument and tracing only the newest record on failure. Define b_k=kx/[(9-k)a+kx]. For k=1, b_1=x. The success map sends b_k to b_(k+1). The failure residual at b_k is
 (F[1-b_k,b_k])_present - b_k Tr(F[1-b_k,b_k])
 =k(9-k)a x(x-a)/[(k+1)((9-k)a+kx)^2] <=0.
Both normalized two-class maps are nondecreasing in r; this is equivalent to their nonnegative determinants, verified symbolically for k1,...,7 and 0<=x<=1/9. Therefore EVERY retained public history satisfies r<=b_k. At completion the Hodge program is isotropic and has infidelity at most
 v_bar= b_8=8eta/(1+8eta)<=8eta_U/(1+8eta_U)<8/9.
This includes conditioning on a finite cap or on a particular completion time. The bound is larger than the exact eventual-average error but eliminates the invalid inference that time conditioning preserves that average law.

## Uniform expected base cost
For any old wedge state, its one-body occupation has total k and dark occupation r, so the next-record growth probability is [1-ka+(a-x)r]/(k+1)>=(1-k/8)/(k+1). Since p_minus>=4/9, a completed base program has expected ordinary-call cost at most
 M_0=(9/4)[1+sum_(k=1)^7 8(k+1)/(8-k)]=41481/140.
This conditional hazard bound is uniform over all classical past histories. It counts plus flags and all failed growth operations. A completed fresh batch resets the growth registers; independent future source uses allow the next batch to be generated independently conditional on its own classical history.

## Heterogeneous-input purification
Two independent, history-conditioned isotropic d-dimensional states with errors u,v have symmetric-SWAP success probability
 p(u,v)=[1+(1-u)(1-v)+uv/(d-1)]/2,
 and retained error
 f(u,v)=[u+v+2uv/(d-1)]/[4-2(u+v)+2d uv/(d-1)].
For 0<=u,v< (d-1)/d, f increases in each argument and p decreases. Thus if both errors are at most e, the retained error is at most
 e'=e(1+e/(d-1))/D_d(e), D_d(e)=2-2e+d e^2/(d-1),
 and success is at least D_d(e)/2. Failure discards both; each retry starts independent fresh subroutines. Inductively each complete public recursive history has error at most e_j, where e_0=v_bar,d=9. Uniform expected call cost obeys M_(j+1)<=4M_j/D_9(e_j). This uses conditional cost and success bounds, not independence of completion cost and output quality. The recursion reaches every positive target, with O(1/target) expected calls for fixed eta_U<1 as in the earlier elementary proof.

## Finite deterministic public call cap
Run a complete j-level subroutine with cap L=ceil(2M_j). Markov bounds its abort probability by1/2. If it aborts, discard all partial program/work states, reset known controller registers and try a fresh attempt. With r independent-memoryless attempts the failure probability is at most2^-r, and total ordinary calls are at most rL. Every successful attempt still has the history-uniform error bound e_j, even conditioned on its completion time, attempt number and cap. Thus timeout affects AVAILABILITY ONLY, not a hidden quality correction. For N separate output batches, choose r>=ceil(log2(N/delta)); the union abort probability is at most delta, at fixed total call cap NrL. Approximate preparation circuits and source-family violation are separate errors, not covered here.

## Scope
This is not an arbitrary-memory result: fresh batches and their histories must factor conditional on the fixed unknown frame. With correlated source memory, a small marginal error does not imply these scalar recurrences. No unknown-noise model identification, universal positive rate, hardware clock implementation, or quantum advantage over fixed-dimensional calibration is claimed. The concrete advance over the earlier cap argument is an operational quality bound stable under all public stopping histories in this specified full-rank noisy family.

## Checks, dependencies, and prior work
`check_history_bounds.py` establishes the success/failure identities symbolically, gives positive rational Bernstein coefficients for each determinant on x∈[0,1/9], and checks14524 exact rational public histories. `check_dense_transitions.py` reconstructs the actual Lüders maps on small d=3,4 spaces and compares both two-class transition matrices (maximum residual4.45e-16). These are mathematical/CPU checks, not native quantum executions.

The two sectors above are inequivalent representations of U(1) on c and U(8) on W; their initial invariant mixture stays invariant under every recorded growth branch. There is no hidden measurement of an unknown eigenbasis. For purification, independent subroutine batches remain product conditioned on their separate complete classical histories; the fixed unknown frame is a parameter, not an uncharged latent source correlation.

Dependencies: accepted coherent commutator acquisition, accepted exact Lüders growth interface, root's physical-twirl label derivation in robust_frame_program_boundary_20261029, and the earlier elementary inverse-error cost proof in noisy_frame_program_purification_20261029. Primary methods: Watts et al., arXiv:2610.06737 (growth); Childs et al., arXiv:2309.16387v3 (recursive SWAP purification). This packet claims neither as new. Its new load-bearing obligation is the history-uniform envelope and consequent safe bounded retry composition for this specific noisy frame-acquisition family.
