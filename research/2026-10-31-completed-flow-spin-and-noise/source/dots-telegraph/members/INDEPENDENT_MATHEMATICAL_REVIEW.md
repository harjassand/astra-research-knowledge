# Independent review: finite-bit telegraph source and controlled-process simulation

Date: 31 October 2026.

## Verdict and exact source binding

Accepted at mathematical-existence level, with the binding receiving conditions below. This is not an implemented-circuit review, a gate-optimality result, or a novelty verdict.

I independently read the complete source note, “A finite-bit coherent oracle for integrated telegraph paths,” from:

`INTEGRATED_TELEGRAPH_SOURCE_COMPILER.md`

The complete UTF-8 body has 23,741 bytes. I independently computed its SHA-256 as:

`2b22ede3ded8034427a300d2d1daf81b4160b73da98b5461a1398f13eb2b71a6`.

Its frozen header correctly records its status when written; this separate later review does not edit that header. The source note alone explicitly excludes the whole Hamiltonian-simulation receiver. Whole acceptance here binds the source body together with the receiving proof's interaction-frame, fixed-time intervention, natural-scale clipping, and finite-precision receiving completions stated below.

## 1. Accepted theorem and input model

Let H0 and A be Hermitian operators supplied through controlled block encodings with known normalization bounds alpha0 and alphaA. Encodings must be exact, or available at the requested precision with that precision-dependent cost charged. A fixed unknown encoding error does not support arbitrary final accuracy.

Let lambda, gamma, and T have finite rational descriptions. The source is a stationary symmetric telegraph sign with flip rate lambda and integrated path

    W(t) = sqrt(gamma lambda) integral_0^t xi(s) ds.

The simulator receives p prescribed intervention times with finite or certified descriptions. At those times it permits arbitrary instruments, adaptive choices based on earlier outcomes, retained ancillas, and an external reference. The source seed and its work registers remain private and initially uncorrelated with the system/reference. The same source is retained throughout the experiment.

For every requested epsilon, the completed simulator can approximate the averaged controlled process in trace distance, uniformly over these strategies, with error at most epsilon. Its cost is polynomial in

    1 + alpha0 T + p + alphaA sqrt(gamma T),
    input bit lengths and register widths,
    log(2 + lambda T), and log(1/epsilon),

times the charged block-encoding costs. This is an existence statement; no optimized polynomial degree or practical resource estimate is asserted.

The theorem does not cover arbitrary adaptive intervention times, unrestricted continuous controls, arbitrary noncommuting noise modes, access to the private seed, unlimited subsequent source reuse, or normalized rare postselection. It grants neither acquisition of the block encodings nor free observable estimation.

## 2. Exact stochastic representation

Conditional on the Poisson event count, normalized chronological spacings have the uniform Dirichlet law. Grouping alternate spacings produces a Beta occupation total and independent normalized Dirichlet vectors within the two parity groups. Balanced independent Beta splits reproduce those vectors exactly before numerical discretization.

The N=0 case and zero-count children are deterministic degeneracies, not Beta distributions with zero shape. The initial sign is independent. The source note correctly distinguishes its exact continuous representation from its finite-word approximation.

Both source data structures are valid. Separate parity prefix trees followed by binary search use logarithmically squared node count. The chronological parity tree uses one descent, splitting each parity mass according to its left/right leaf counts, and requires only logarithmically many visited nodes. Neither representation materializes an arrival list.

## 3. Count and Beta sampling

The Poisson modal envelope, its geometric tails, and its constant acceptance bound check. When the left endpoint is zero, the corresponding tail is omitted. For mean below one, the envelope 2 times 2 to the power minus n is valid and has total mass four. The Poisson cutoff and bounded rejection count are explicitly priced.

For Gamma shape k at least two, the stated dyadic d lies between sqrt(k-1)/4 and sqrt(k-1)/2. The envelope area is at most 9 sqrt(k-1). On its central interval the normalized target is at least exp(-1/4), giving acceptance greater than 1/32. Shape one is handled separately. Two independent Gamma draws yield the required Beta split.

The finite-bit seam is adequately closed for a polynomial-existence theorem. Gamma tail truncation, proposal-uniform cutoffs, bounded rejection loops, and fresh acceptance uniforms support the stated coupling. On the compact accepted domain, log-density derivatives have polynomial bounds. Discontinuous mixture choices, cutoff tests, and finite Poisson integer/geometric thresholds are charged through explicit boundary-strip or uniform-threshold probabilities; they are not incorrectly treated as differentiable.

One numerical wording precision is binding: the acceptance derivative with respect to the proposal location can be O(H^7), while its composition with the proposal-uniform map can be O(H^14). The stated 500 log2(H) precision budget still has ample slack. This does not change the asymptotic theorem.

No runtime may scale by iterating H or Nmax times. Those numbers are magnitude and probability-budget parameters. Actual loops use bounded rejection count, logarithmic tree/search depth, and polynomial bit-arithmetic. The log-factorial construction shifts by O(B) steps, applies the positive-real Stirling remainder bound, and pays guard bits for cancellation; it does not multiply n factorial factors. This review establishes mathematical arithmetic feasibility, not correctness of an executed numerical library.

## 4. Uniform path coupling

The dyadic splits and their exact complements produce a consistent nonnegative spacing vector. A depth-D tree has leaf-mass l1 error at most 2(D+1) times the split error, including the parity occupation split.

Matching corresponding chronological intervals by a monotone time change bounds both breakpoint times and integrated signed occupation. The integrated sign is 1-Lipschitz. Consequently the uniform W error is bounded by

    4 sqrt(gamma lambda) T (D+1) times the split error.

Zero-length rounded intervals are harmless under a consistent endpoint convention. There is no minimum-spacing assumption, no query-time anti-concentration requirement, and no error accumulation proportional to the number of switches. Exact rational comparisons and dyadic mass products supply the coherent lookup; final output and parameter rounding receive their separate budgets.

## 5. Limited independence and the private source

The table replacement is valid only with independence order at least twice the deterministic number of primitive table calls. That count includes source computation, rejection-sampler random words, and reversible uncomputation. It is not twice the number of high-level time queries unless their internal source calls have already been included.

A quantum circuit's averaged density-matrix entries involve monomials containing at most twice that many distinct table addresses. This is a per-term statement, not a claim that a superposed computation globally accesses only a small fixed set of addresses.

The independent-table coupling is analyzed first. The finite consuming circuit is then replaced by the limited-independence table using exact equality of its averaged visible output. No assertion is needed about an all-node good event under the limited-independence family.

The finite-field construction, irreducibility verification, capped setup failure, seed length, and Horner evaluation cost are charged. A conservative quadratic total overhead in the primitive query budget is allowed. The resulting seed is suitable for the declared bounded-query experiment, not an unlimited exact random-path service.

## 6. Interaction frame and fixed-time controls

For each path,

    R(t) = exp(-i A W(t)),
    H_I(t) = R(t)^dagger H0 R(t).

This identity is exact. The transformed norm is at most alpha0. Its continuous-path Lipschitz bound is at most 2 alphaA alpha0 sqrt(gamma lambda). That derivative scale enters the logarithm of the time-grid size, rather than a linear number of source events.

For two integrated paths with uniform difference d, endpoint-frame errors and Duhamel's formula on each interval imply the uniform controlled-process bound

    4 alphaA [(p+1) + alpha0 T] d.

The interval errors telescope through arbitrary memory-bearing CPTP interventions because such maps contract trace/diamond distance. The bound is independent of the particular allowed strategy. Averaging a coupled source adds at most twice the probability of its bad event.

Digital time/value rounding is a separate uniform Hamiltonian-oracle approximation. The rounded oracle itself is not assumed differentiable. Apply Dyson regularity to the ideal continuous dyadic-spacing path, possibly clipped, and then charge oracle errors by simulation hybrids.

All Hamiltonian simulation constructions must be completed CPTP operations. Failure flags may be retained or discarded, but their contribution is charged. Normalized successful postselection is not a substitute for the required process approximation.

## 7. Binding natural-scale clipping correction

The fixed-sign tilted generator gives, for the stationary symmetric source,

    E exp(u W(t)) <= exp(gamma t u^2 / 2).

For the claimed complexity normalization, use a time grid with oscillation scale sqrt(gamma T), not a fixed unit oscillation. Put

    J = ceil(sqrt(lambda T)) + 1,
    B = sqrt(gamma T) [1 + sqrt(2 log(2J/eta))].

Including endpoints, the union bound and deterministic path Lipschitz property give sup |W| <= B except with probability eta. Zero-noise or zero-time cases are trivial. Clipping is nonexpansive and changes the true process only on this priced bad event.

This correction is necessary for the displayed norm dependence. A clip of 1 plus a fluctuation term would introduce an unlisted additive alphaA cost when gamma T is tiny. The natural-scale clip makes generic A-exponential cost polynomial in alphaA sqrt(gamma T) and logarithmic in rate/accuracy. It does not assume that A can be fast-forwarded.

## 8. Whole error and cost composition

The receiving proof's allocations, such as source failure epsilon/64 and path tolerance

    epsilon / [64 (1+alphaA)(p+1+alpha0 T)],

leave slack for source cutoff, rejection/setup failures, clipping, path rounding, block precision, and complete-CPTP synthesis. These budgets must be individually included rather than counted as a single unexamined sampler error.

Time-dependent Dyson simulation uses O(1+p+alpha0 T) segments and logarithmic truncation order. Its time-grid register depends logarithmically on the derivative scale and requested accuracy. Each interaction-frame block computes the path, implements the bounded variable A-exponential, applies the H0 encoding, and uncomputes. Packed node words and a predetermined query budget prevent a circular dependence of the independence order on its own implementation.

With these conventions, the stated constructive polynomial theorem follows. No remaining load-bearing mathematical gap was found in this source-plus-receiver chain.

## 9. Ordinary comparators and limits of this review

The components have substantial established precedents:

- Dirichlet-tree factorization: https://tminka.github.io/papers/dirichlet/minka-dirtree.pdf
- Virtual Brownian trees and repeatable arbitrary-time path access: https://proceedings.mlr.press/v108/li20i/li20i.pdf
- Single-seed Brownian paths and integrals, with its stated query-separation qualification: https://arxiv.org/abs/2405.06464
- Quantum polynomial and limited-independence methods: Beals and coauthors; Zhandry.
- Interaction-picture Hamiltonian simulation: https://arxiv.org/abs/1805.00675
- Time-dependent L1-norm simulation: https://arxiv.org/abs/1906.07115
- Quantum spectral stochastic-process representations: https://arxiv.org/abs/2303.06719
- OU coarse-bridge noise simulation: https://arxiv.org/abs/2502.12296

The spectral stochastic-process comparator stores values in amplitudes and explicitly distinguishes that interface from direct individual-time readout. It prevents any broad claim of being the first exponentially succinct quantum stochastic representation, but does not by itself supply the digital oracle required here.

Borras and Marvian's trajectory algorithm applies directly to the telegraph sign-register dilation: its jump sqrt(lambda) X has scalar total rate lambda. It is a particularly fair ordinary comparator, although its explicit trajectory construction retains a number of jumps typically proportional to lambda T:
https://quantum-journal.org/papers/q-2026-04-13-2063/

The dissipative-ODE algorithm of An, Onwunta, and Yang assumes a uniformly strictly negative logarithmic norm and prepares normalized solution/history states. The complete trace-preserving telegraph dilation has a stationary zero mode, so that theorem is not directly the controlled-process receiver:
https://quantum-journal.org/papers/q-2026-01-27-1986/

The accessible abstract of Gao, Ji, and Liu's Lévy-Khintchine paper establishes fast-forwardable Hamiltonian twirling families and relevant scaling laws:
https://journals.aps.org/prl/abstract/10.1103/qy4b-gzlq

Its full text is authorization-blocked and was not accessed or bypassed. No conclusion about its detailed controlled-process scope is inferred from the abstract.

No priority, practical advantage, or absence of a closer prior theorem is established here. The accepted result is the precise source/controlled-process existence theorem, not novelty of its standard ingredients.
