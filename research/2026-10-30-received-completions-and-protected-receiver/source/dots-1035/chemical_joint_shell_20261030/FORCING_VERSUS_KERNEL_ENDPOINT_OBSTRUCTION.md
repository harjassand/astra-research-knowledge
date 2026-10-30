# Exact endpoint obstruction: kernel transport versus aggregate forcing

Status: personally derived. This is a counterexample to a tempting uniform Green-kernel extension, not to recurrence. A second exact computation shows why forcing-sensitive aggregation is materially different.

## Reversible killed conservative shell
Take the unit-rate conservative reactions A→C and C→A, with A+C=N, and kill independently at rate1. This is an exact killed boundary piece of the weakly reversible network A⇌C, 0⇌B when restricted to B=0. No claim of one-linkage generality is needed for the kernel obstruction.

Write a for the A count. Starting from all A, the probability of A=0 at time t is [(1−e^(−2t))/2]^N. Hence

    G_N(N,0)=2^(−N−1) Beta(1/2,N+1).

The physical insertion that adds one A and leaves C fixed sends the two queried states to N+1 and1. Direct binomial transition probabilities give

    G_(N+1)(N+1,1) / G_N(N,0)
       = (N+1)(N+2)/(2N+3) ~ N/2.

Therefore NO constant-factor fixed-C Green comparison can hold uniformly to the endpoint, even for this reversible linear conservative shell. The macroscopic epsilon restriction in MAJORITY_INSERTION_UNIFORM_GREEN.md cannot simply be deleted. This is not a mixing pathology: the un-killed Ehrenfest chain has a fixed positive spectral gap.

## Uniform forcing removes this particular endpoint amplification
Let v_N=G_N^T 1, i.e. put a source of strength1 at EVERY composition state. Uniform measure on counts is the beta-binomial mixture with mixing parameter uniform on [0,1]. If u=e^(−2t), that mixing parameter at time t is uniform on [(1−u)/2,(1+u)/2]. Integrating time and interchanging positive integrals yields the exact formula

    v_N(b)=E[ |2P−1|^(−1/2) −1 ],
    P distributed Beta(b+1,N−b+1).

For fixed b and N→infinity, concentration near zero and expansion (1−2p)^(-1/2)−1=p+O(p^2) give

    v_N(b) ~ (b+1)/N.

The singularity at p=1/2 contributes only exponentially small terms for fixed b; this follows directly by bounding the beta density on a neighborhood of 1/2 and integrating its square-root singularity. Consequently

    v_(N+1)(b+1)/v_N(b) → (b+2)/(b+1),

rather than growing like N. Thus full-support forcing genuinely removes the rare backward-entry amplification in this model. It is not legitimate to infer this from a uniform bound on individual Green entries, which is false.

## What remains unproved
No forcing-sensitive endpoint theorem is claimed for the coupled nonlinear hard network. Its actual inter-shell source is not automatically uniform or comparable to uniform; that is precisely the new obligation. Arbitrary source concentration near a well can retain the bad kernel ratio. The right question is therefore whether the actual connector forcing satisfies an earned smoothing/shape condition under the joint killed-shell operator, not whether all entries admit a constant shift bound.
