# Finite work and precision for the repaired fixed-action sampler

> Release-copy note: this historical proof/review snapshot has presentation-only edits recorded in SOURCE_PROVENANCE.json. Mathematical content is unchanged. Current status and superseded steps are identified in START_HERE.md and DEPENDENCY_MAP.md at the package root.

8 November 2026. Independent review checked this finite enumeration, precision and sampling reduction. The repaired two-body spatial theorem in FIRST_DISCOVERY_PROOF.md and activity assembly in SPATIAL_RESPONSE_CANDIDATE.md have now also passed the first end-to-end audit. No all-time polynomial or practical advantage is claimed.

## Target and numerical input

Take a finite square-lattice system with static nearest-neighbor two-qubit Hamiltonian terms and on-site terms, every-site replacement rate gamma, rational product input, and computational-basis output. Terms, positive time T, gamma and accuracy0<epsilon<=1 have paid rational encodings. Let h upper-bound each grouped physical local term and Delta be a valid fixed physical path-branching bound. The spatial contract is checked at this actual T; increasing T changes the physical experiment and is not an allowed algorithmic substitute.

The theorem applies when a positive integer r satisfies the scalar conditions in the activity proof for b=8,c=2400. All physical Hamiltonian terms can be strong and noncommuting, with a fully connected two-dimensional interaction graph. The hypothesis is sufficient accumulated physical noise/time and the stated representation of the input, not the earlier weak-boundary feedback condition.

At every fixed dimensionless action gamma T, fixed h/gamma and fixed locality, r is independent of n and epsilon. Equivalently, fix numerical h, gamma and T. Fixing T and h/gamma alone is insufficient when h and gamma may grow with n. The exponent below depends on r. This is a restricted time regime within the general spatial model, not a solution for all times.

## Logarithmic cluster cutoff

For a requested partial output x_S, compute isolated normalized block marginals z_v. The activity theorem establishes z_v>=1/2 and activity magnitude |w(C)|<=exp(-8|V(C)|), uniformly in S and x_S. The connected-edge polymer count containing a chosen block is at most64^v. Hence the Kotecky-Preiss sum for modified weights |w(C)|exp(v), with size function a(C)=v, is bounded by

    |V(C')| sum_(v>=2)(64e^{-6})^v < |V(C')|.

The standard cluster-expansion tail then bounds omission of incompatibility clusters of total vertex multiplicity greater than m by at most n exp(-m). For an additive log-marginal error delta_log, use

    m=ceil(log(10n/delta_log)).

The physical log marginal is

    -|S|log2 + sum_v log z_v + sum_(clusters total size<=m) cluster contribution.

The logarithmic branch is fixed continuously from zero activities. The real physical marginal is positive; the convergent expansion gives its real log. No evaluation step divides by that global marginal.

## Explicit finite enumeration

There is an exponential-in-m procedure, rather than enumeration of all graphs on m objects:

1. Enumerate connected coarse vertex sets U of size at most m, rooted in the physical block graph, by depth-first encodings. Their number is at most n16^m up to a polynomial factor. Duplicate sets may be removed with a paid dictionary.
2. Within each U enumerate all connected edge polymers of vertex size at most m. There are at most |U|64^k polymers of size k, a safe bound inherited from the same animal count.
3. Enumerate multisets of these polymers whose total vertex multiplicity is at most m; retain those with union exactly U and connected incompatibility graph. The number of multisets is exp(O(m)): its generating product is bounded at z=1/128 by

       product_(polymers C subset U)(1-z^{|C|})^{-1}
          <= exp(O(|U|)),

   because sum_(k>=2)|U|64^k z^k is O(|U|). The coefficient/cumulative bound is therefore exp(O(m)). An ordered-type recursion with a remaining-size budget enumerates these finite multisets with polynomial delay; no operation proportional to n^m is needed.
4. For R polymer occurrences in a retained multiset, compute the alternating sum over connected spanning subgraphs of its incompatibility graph by subset recurrence in O(3^R) integer work. If Z(W)=product_(edges inside W)(1-1), then the connected coefficient C(W) is obtained by subtracting C(S)Z(W\S) over proper subsets S containing a fixed root. Here Z(W) is1 for an independent set and0 otherwise. Multiply by product w(C) and divide by the factorial of each polymer multiplicity. R<=m/2, and these are explicit integers and rationals.

All combinatorial work is n exp(O(m)) times polynomial factors. The integer connected coefficient has at most O(m^2) bits, since its absolute value is at most2^{R(R-1)/2}.

## Activities and arithmetic precision

Each required activity uses at most2^e switched Hamiltonians, e<=2v, on at most r^2v nontrivial physical qubits. A matrix representation has dimension exponential in r^2v. Direct rational Taylor evaluation of the finite-time exponential can be charged as follows:

- A safe Hilbert-Schmidt generator norm action is A=O(N(h+gamma)T) for N physical sites and fixed incidence.
- A Taylor degree polynomial in A+N+log(1/eta) suffices for a scalar marginal error eta. The N term pays norm conversion between the observable, initial state and normalized Hilbert-Schmidt norm.
- Rational input and exact integer arithmetic make all intermediate bit lengths polynomial in the paid input bits, degree, action and requested precision. Equivalently, a certified stable matrix-exponential algorithm may be used with its full cost charged.
- Alternating sums have2^e terms. Local denominator products have factors at least1/2. Thus choosing the per-evolution scalar precision smaller by exp(O(v)) and computing each z_v to matching precision controls the activity error without an inverse rare-prefix factor.

If the number of retained clusters is M_cl<=n exp(O(m)), approximate each activity to

    eta_w <= delta_log / [10 M_cl m 2^{m^2+m}].

This is deliberately conservative. Product telescoping and the integer coefficient bound pay every retained term. Its required scalar bit precision is only polynomial in m+log n+log(1/delta_log), although the underlying matrices are exponentially large in r^2v. Compute each log z_v to error delta_log/(10n); z_v>=1/2 makes this stable. Certified log2 and scalar logarithms have their precision charged.

The complete log-marginal evaluator therefore has finite bit work

    poly(B,n,A,log(1/delta_log)) · exp(O(r^2 m)),

with polynomially charged integer-arithmetic factors. Constants in the exponent include the explicit enumeration and matrix algorithms. This is a large worst-case bound, not a practical implementation.

## Positive full-output sampling from certified logs

For each bit prefix, evaluate the two next-bit log marginals with delta_log=epsilon/(100n), then normalize their exponentials using a stable logistic function of their difference. Their conditional probabilities are positive and sum to one. The per-branch log error is at most2delta_log, and multiplication along n steps gives a pointwise likelihood-ratio error at most exp(2n delta_log). Its induced TV error is below epsilon/10 with the displayed slack.

Implement each conditional coin using a fixed number O(log(n/epsilon)) of unbiased random bits at additive error at most epsilon/(100n), including scalar evaluation. Sequential coupling pays their total error. The cluster-tail, activity-arithmetic and baseline-log budgets are already part of delta_log. The complete sampler therefore have bounded work and global TV error below epsilon. It produces one n-bit output, not an exponentially large table.

This sampling reduction is standard prior work, including the noisy-circuit comparator. The substantive continuous-time operation is the repaired activity bound; the reduction from certified logarithms to a sample is standard.

## Scope that remains open

The current work is polynomial at each fixed qualifying physical time, with exponent O(r^2). It is not uniformly polynomial for times scaling up to log n/gamma. The available global mixing shortcut handles sufficiently late times but does not remove the intermediate scaling interval. Early times below the accumulated-noise condition are also not covered. Arbitrary nonunital noise, uncharged correlated inputs, higher-arity terms without recomputed geometry, and an actual production speedup are not claimed.
