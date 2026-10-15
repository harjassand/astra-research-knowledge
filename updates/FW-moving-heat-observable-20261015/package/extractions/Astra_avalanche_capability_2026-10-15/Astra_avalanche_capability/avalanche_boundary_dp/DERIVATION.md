# Fixed-strength avalanche lifetime mean by a shared boundary transfer

This is an independent computation for the thermal equal-load-sharing model in https://arxiv.org/abs/2508.13367. It uses the independently established common-clock representation. No downloaded author code is imported or executed here. The verification imports only our own previously written reachable-state generator.

## Exact fixed-time PMF in quadratic arithmetic cost

Sort strengths s_1 >= ... >= s_n. At internal time u, let X_j be independent Bernoulli(p_j), p_j=exp(-exp(-s_j/T)u), and N_j=sum_{i<=j} X_i. Let K be the largest feasible surviving count, zero if none. A count c is feasible whenever its cth present fiber has strength greater than F/c. Mechanical equality breaks.

Put j_m=#{j:s_j>F/m}, m>=1, and j_0=0. The crucial decomposition is

    {K=m} = {N_(j_m)=m} intersect {N_j s_j <= F for every j>j_m},

with zero count always permitted. If j_m<m the event is empty.

Proof: K=m requires at least m present fibers in A_m. If there were c>m, those c fibers all have strength greater than F/m>=F/c, making c feasible, a contradiction. Thus exactly m are present in this prefix. Beyond the prefix, strengths are <=F/m. A later feasible count c>m would contradict maximality. Conversely, exactly m present in A_m makes m feasible, and the suffix restrictions exclude all larger feasible counts. A restriction at an absent fiber causes no spurious exclusion: its count was first attained at a present fiber with at least as large a strength, so feasibility there would already have been detected. For m=0 the suffix restrictions simply prohibit any feasible positive count. The argument accommodates repeated strengths and exact equality.

Forward Poisson-binomial recursion:

    a_0(0)=1,
    a_j(c)=(1-p_j)a_(j-1)(c)+p_j a_(j-1)(c-1).

Save a_(j_m)(m) for each feasible m. Define H_j(c) as the probability that all FUTURE prefix counts stay below their mechanical boundary, given current count c at index j. Crucially the current index j is not itself checked. With d_j(c)=1 when c=0 or s_j<=F/c,

    H_n(c)=1,
    H_j(c)=(1-p_(j+1)) d_(j+1)(c) H_(j+1)(c)
              +p_(j+1) d_(j+1)(c+1) H_(j+1)(c+1).

Then P(K=m)=a_(j_m)(m) H_(j_m)(m). One forward and one backward pass give every PMF entry simultaneously. Bucket the queries by j_m; only O(n) working memory is needed. Sorting costs O(n log n); each probability evaluation uses O(n^2) arithmetic operations. This is an arithmetic-operation statement, not a polynomial-bit-complexity theorem for unbounded rational thermal inputs. The basic recurrence is positive, avoiding alternating-sign cancellation. Ordinary binary floating-point code does not supply certified rounding bounds.

## Deterministic mean and geometric quadrature

Let psi(0)=0 and psi(k)=exp(-F/(kT)). The common-clock identity gives

    E[tau] = integral_0^infinity g(u) du,
    g(u)=sum_m psi(m) P(K(u)=m).

Coupling the same clocks proves g is nonnegative and decreasing. Thus on each grid interval [u_j,u_(j+1)] the integral lies between its width times g at the right and left endpoints. On [0,u_0], use [u_0 g(u_0), u_0 psi(n)]. For the remaining tail,

    integral_U^infinity g(u)du
      <= psi(n) sum_i exp(-lambda_i U)/lambda_i.

This follows from K(u)>0 implying at least one E_i>u and the union bound. For an exact geometric ratio r, interior upper rectangle sum <= r times lower rectangle sum plus (r-1)u_0 g(u_0). Consequently the node count depends logarithmically on the time range and inversely on requested relative gap, rather than linearly on the largest lifetime scale.

The interval prototype uses exact rational strengths (the exact binary64 values produced by the author's seed), F=5/8, T=1/20, exact rational grid u_0=1/1000, U=100000000, r=101/100, and installed mpmath.iv 1.3.0 with 40 decimal digits for exp and every arithmetic operation. Mechanical decisions use Python Fraction comparisons, independent of transcendental rounding. It propagates full intervals through both positive recurrences, including p and 1-p. Its enclosure is conditional on the interval library's arithmetic/exp contract, not a formally machine-checked theorem. This rational T model is intentionally distinguished from exact evaluation of the author's binary64 T constant.

Result: the mean is enclosed by

    [2047.20828390170767745710890750743951085656756,
     2067.6803667407343312452555783530127476636895].

The tail bound is below 2.982e-22. There are 2,547 grid evaluations, taking 1.98 seconds in this run. Both endpoint-sum intervals and exact input fractions are recorded in certified_fixture.json. The numerical quadrature implementation, which is NOT an interval certificate, gives 2057.410374767016.

## Scope and prior art

At fixed u this is static reliability of a bundle with independent two-point random strengths Y_i in {0,s_i}. Classical static bundle reliability and boundary-crossing recurrences are therefore the correct prior-art family, rather than only exponential-state thermal CTMC implementations. We make no priority claim for the PMF recurrence. The useful transfer demonstrated here is a shared prefix/suffix computation for this heterogeneous thinning problem, composed with the common-clock integral to compute a conditional thermal-avalanche mean deterministically.

Primary source leads:

- Daniels (1945), The statistical theory of the strength of bundles of threads. I, DOI https://doi.org/10.1098/rspa.1945.0011. An accessible author thesis precursor is https://era.ed.ac.uk/items/c210a8d9-93a9-4514-9093-de38354d2a75. These establish that static bundle strength distributions and their asymptotics are classical.
- McCartney and Smith (1983), Statistical Theory of the Strength of Fiber Bundles, DOI https://doi.org/10.1115/1.3167097. Search metadata identifies accurate finite-bundle recurrence calculations. The publisher text was inaccessible in this pass, so its exact overlap with our heterogeneous-thinning recurrence remains to be checked before a novelty claim.
- Moscovich and Nadler, Fast calculation of boundary crossing probabilities for Poisson processes, https://arxiv.org/abs/1503.04363 (Statistics & Probability Letters 123, 2017). Its O(n^2 log n) result concerns Poisson-process boundary crossing, not this exact heterogeneous Bernoulli PMF, but is relevant prior art for the algorithmic family.
- Zhang, Hong and Balakrishnan, An Algorithm for Computing the Distribution Function of the Generalized Poisson-Binomial Distribution, https://arxiv.org/abs/1702.01326. It treats independent nonidentical Bernoulli sums via characteristic-function/FFT computation. It does not by its abstract establish the present suffix-boundary result.

This does not compute the physical lifetime PDF, a rare-tail probability, variance, disorder-averaged moments, or physical material validation. The fixed-u marginal distributions alone do not give two-time covariances needed for lifetime variance. It should not be advertised as universally faster than Monte Carlo. A deterministic enclosure and a stochastic confidence interval have different guarantees, and matched runtime/accuracy comparisons are still required.
