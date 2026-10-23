# Strong ordinary comparisons and actual cost contract

Pure proposal-start independence Metropolis-Hastings G is available under the
same positive pi,q and supplied population D(pi||q)<=K. Its general leading
minimax error amplitude is K/log n. The accepted proof and dependencies remain
in selected_cycle5/COMPARATOR.md and the unchanged predecessor chain.

The enlarged reciprocal-proposal critical amplitudes are maxima with K. They
never demonstrate a better leading minimax error than pure G; in the adverse
transport regime they are worse. No finite-time ordering is inferred from
off-diagonal comparisons, reversibility or Dirichlet ordering.

For the new mismatched-power families, with root/leaf/core masses in
MATCHED_POWERS_THEOREM.md and fixed b<1-exp(-K), the actual hybrid law satisfies

    TV(q C^n,pi) -> b beta/[alpha(1-b)+beta] > 0.

On exactly the same native inputs, the correctly matched full-flow screen
has TV=O(n^-1+n^(-4 eta)) for fixed eta>0. Pure G satisfies

    p-(j+1)e <= TV(q G^j,pi)
                <= p+t+e/(1-b)+b^(j+1),

where p=n^-1,t=n^-3,e=b/n^4. Consequently TV(q G^j,pi)~1/n whenever j/n
tends to a fixed positive constant, including j=floor(alpha n/2). The latter
comparison matches the expected number of global attempts in the lazy hybrid,
not its target calls, cache behavior or wall time. The statements follow from
the full native laws and exact block structure; no optional count substitutes
for a deterministic horizon.

If the explicit analytic block description of these examples is available,
direct target sampling by block and uniform label is allowed. Hiding that
description would make an artificial practical comparator. The native class
theorem itself assumes target evaluations, not a free revealed target table.

All implementations must pay for proposal generation, forward and reverse Q
evaluation, target and q evaluations, acceptance uniforms, index length,
arithmetic precision and full caching. On the new examples the multiplicity
m is approximately n^(4 eta/abs(eta-kappa)), so log m scales as
eta log n/abs(eta-kappa). A graph may have a compact algebraic description,
but labels and exact probabilities still have representation costs. The
18-state diagnostic is not an execution of those enormous asymptotic graphs.

No normalizer, population-KL certificate, full target table or auxiliary
absorbed sampler is free. The absorbed process is a proof counter only. No
native-call, hardware, precision or wall-time advantage has been measured.
This checkpoint establishes a sharp robustness boundary for a stated kernel
class and a structural failure of differently matched powers.
