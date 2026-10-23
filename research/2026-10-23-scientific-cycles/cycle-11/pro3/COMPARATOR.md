# Strong ordinary comparator

Under the same supplied population D(pi||q)<=K, q initialization, proposal
and target-ratio information, ordinary independence Metropolis-Hastings
retains the accepted minimax amplitude K. It does not use the extra Q
proposal, reverse-Q evaluations or screen.

On the SAME admitted native families used for the critical phase lower,
the preserved estimate is

    TV(q G^j,pi)<=p_T/(1-n^-2)
      +b_n z/[(1-b_n)(1-z)]+b_n^(j+1)
      =O((log n)^-4), when j/n->t0>0.

This includes j=floor(alpha n/2). The hybrid has order 1/log n on these
families. Comparing these transition laws does not establish equality of
wall-time or target-call budgets; the extra local/global operations,
rejections, preparation, target evaluations, reverse probabilities,
indexing, caching and arithmetic precision all have their actual costs.

Analytic direct sampling or complete enumeration remains legitimate when
the recipient is actually given the analytic target or table. No ordinary
method is denied information it naturally possesses. The proof's
normalized pi notation does not make a normalizer available to the sampler.

Cycle11 is a sharp robustness theorem with an adverse comparison for the
hybrid. No useful-sampler, implementation, acquisition, target-call or
wall-time gain is claimed. The larger antisymmetric-screen class is an
exact-real mathematical extension; it is not a precision implementation.

The relevant primary delayed-acceptance comparison is Sherlock and Lee,
"Variance bounding of delayed-acceptance kernels," arXiv:1706.02142v4.
It distinguishes per-step asymptotic variance from computational efficiency
and proves inheritance/failure results under its own assumptions. Our
supplied-K proposal-start critical minimax TV law has a different contract.
