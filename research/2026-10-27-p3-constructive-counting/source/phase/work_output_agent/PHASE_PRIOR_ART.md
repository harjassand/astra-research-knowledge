# Targeted prior-art and scope audit: many-factor local phase sums

27 October 2026. This audit concerns the construction in
`work_dense_agent/PHASE_PRODUCT_CONSTRUCTION.md`. It is not a comprehensive
priority search and does not certify a first-ever result.

## Verdict

The conditional theorem has a substantive parameter regime beyond the ordinary
linear-size circuit-to-CNF corollary. I found no primary source in this targeted
search establishing exact, worst-case, original-input subexponential evaluation
of arbitrary fixed-locality, fixed-2-power-root phase products with

    m = n exp(o(log n))

factors and no width, geometric locality, randomness, or supplied decomposition
assumption. Existing results below do not subsume that statement. This is a
defensible conditional extension of the governing machinery; describing it as a
historically established breakthrough, a general circuit solver, or a practical
quantum-simulation speedup would exceed the evidence.

The strongest clean presentation is the raw local-phase family itself and its
binary degree-at-least-three special case. Quadratic polynomials over F_2 have
polynomial-time Gauss-sum algorithms already. For m=O(n), the qualitative
subexponential conclusion also follows from the supplied linear-size circuit
corollary. The substantive extension is the growing factor-density range.

## Why a direct #kSAT conversion does not establish this bound

For a binary phase sum, compute each local Boolean function into a fresh bit
and combine those bits by a parity tree. A parsimonious bounded-width CNF uses
n+O_(k)(m) variables. Applying the supplied theorem measures its exponent in
that larger variable count. For example,

    m = n 2^(sqrt(log_2 n))

is admitted by the phase construction. Its new exponent is

    O_k(n (log n)^(-1/4) (log log n)^(3/2)),

whereas a direct O(n+m)-variable encoding inserted into the supplied bound does
not give 2^o(n). The same issue occurs when applying Appendix D directly to an
incidence tensor network with Theta(m) wires.

This comparison proves a gap between the explicit transformations analyzed;
it is not a lower bound excluding every possible O(n)-variable reduction.
No such alternative exact reduction was found in the search below.

The phase construction instead manufactures a truncated product with retained
incidence degree O_(k,b)(n), independently of m. This is a new use of the
source's general factor-product routine. Uniform control of the growing
incidence bound is required; the fixed-polylogarithmic scope/incidence statement
alone cannot be cited unchanged.

Standard #CSP gadget reductions and exact weighted-counting reductions do not
automatically preserve original variable count: auxiliary local-value or edge
variables are generally charged per constraint. Likewise, the usual #kSAT
sparsification proof cannot simply treat a nonzero phase factor as a hard
clause. A failed hard clause kills an assignment; a phase factor changes its
weight. The branch and normalization invariants differ. Search results on
weighted CSP sparsification mostly preserve the value/energy approximately,
which does not preserve exact complex cancellation.

## Primary sources checked

### 1. Exact versus approximate low-degree polynomial counting

R. Ryan Williams, *Counting Solutions to Polynomial Systems via Reductions*,
SOSA 2018, DOI 10.4230/OASIcs.SOSA.2018.6.

Author PDF: https://people.csail.mit.edu/rrw/counting-sosa.pdf

Proceedings: https://drops.dagstuhl.de/entities/document/10.4230/OASIcs.SOSA.2018.6

The positive result is deterministic additive approximate counting for systems
of quadratic equations. The paper also gives an original-variable-preserving
reduction from #kSAT to counting one constant-degree polynomial and explains
the difficulty of exact degree-three counting. It does not provide the
candidate's exact subexponential algorithm. Its reductions run toward polynomial
counting, not an established reverse O(n)-variable #kSAT encoding for arbitrary
phase sums. Root independently read the governing theorem details.

### 2. Complex weighted #CSP dichotomy

Ying Liu, *The Exponential-Time Complexity of the complex weighted #CSP*, 2022.

https://arxiv.org/html/2202.02782v1

Theorem 1.2 distinguishes tractable product-type and affine signatures from
#ETH-hard signatures, including bounded-occurrence instances. The reductions
and pinning arguments preserve linear size for the hardness direction. This
establishes relevant prior classification and algebraic tractable cases, not
an unconditional exact subexponential algorithm or a reverse encoding that
removes arbitrary constraint density. Since the governing manuscript refutes
#ETH, these old conditional lower bounds are not a contradiction.

### 3. Exact IQP simulation through random graph structure

Julien Codsi and John van de Wetering, *Classically Simulating Quantum Supremacy
IQP Circuits*, Physical Review A 111, 012422 (2025); earlier arXiv versions.

Primary repository PDF: https://ir.cwi.nl/pub/35965/35965.pdf

The reported amplitude algorithms exploit random interaction graphs. Dense
random two-qubit instances have a polynomial factor saving over 2^n; the
sparse random regime has superpolynomial savings over 2^n. Those are not
2^o(n) worst-case guarantees for every allowed local interaction list.
The root read the PDF separately; the comparison should retain its random
instance qualification and should not be called a practical benchmark here.

### 4. A genuinely subexponential but geometrically restricted simulator

Thorsten B. Wahl and Sergii Strelchuk, *Simulating Quantum Circuits Using
Efficient Tensor Network Contraction Algorithms with Subexponential Upper
Bound*, Physical Review Letters 131, 180601 (2023).

https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.131.180601

https://arxiv.org/abs/2208.01498

This work gives subexponential bounds for finite-range tensor networks in
fixed-dimensional geometry, using geometric separators; its abstract measures
the simulation bound in gate count. This is a real prior subexponential
simulation theorem and must not be omitted in a broad historical statement.
The present phase construction admits arbitrary interaction hypergraphs and
does not use finite-range geometry, so this result does not subsume it.

### 5. Rank-width algorithms for quadratic sums of powers

Alexis de Colnet et al., *Quadratic Sums-of-Powers for Fixed-Parameter Tractable
Quantum-Circuit Simulation*, 28 May 2026.

https://arxiv.org/html/2605.29944v1

Theorem 2/3 and the contribution statement give a rank-decomposition dynamic
program with cost O(n r 4^k poly(n)+r log r), where k is rank-width and r the
phase modulus. It constructs SOPs from raw circuits, including Clifford+T,
and goes beyond ordinary contraction width. It still requires a small
rank-width parameter for a strong bound. The phase construction guarantees
subexponential time from factor density alone, without small rank-width.
Conversely the rank-width method can cover large factor lists when rank-width
is small, so neither should be described as uniformly dominating the other.

Related application already exists: Bin Cheng and Feng Pan, *Exact Maximum
Likelihood Decoding beyond Treewidth via Rank-Decomposition Dynamic
Programming*, 30 September 2026:

https://arxiv.org/html/2609.39556v1

It includes decomposition construction, Gaussian elimination, tractable code
families, likelihood learning, and numerical comparisons. Those straightforward
applications of rank-width machinery are not new contributions of this work.

## Limits that should accompany the theorem

1. The algorithm is conditional on the supplied OpenAI replacement theorem.
2. It does not cover dense degree-k polynomials with Theta(n^k) distinct
   monomials for fixed k>=2. Then log(m/n)/log n does not vanish.
3. Fixed 2-power roots are substantive: divisibility gives a short product
   truncation while the final cyclotomic coordinates remain bounded by 2^n.
   Arbitrary positive integer local weights may produce Theta(m)-bit answers
   and do not inherit the same precision argument.
4. The raw bounded-formal-degree arithmetic-program compiler must pay for
   canonical polynomial expansion and use the support it actually computes.
   A low semantic degree or a useful sparse expansion cannot be assumed.
5. The finite programs validate compilation, truncation, reconstruction and
   Fourier identities. They do not implement the asymptotic replacement solver
   and support no practical speed comparison.

Subject to these limits, the sought advancement is best described as a
precision-controlled local phase representation that removes a superlinear
operation-count obstruction over a meaningful unrestricted-interaction family.
