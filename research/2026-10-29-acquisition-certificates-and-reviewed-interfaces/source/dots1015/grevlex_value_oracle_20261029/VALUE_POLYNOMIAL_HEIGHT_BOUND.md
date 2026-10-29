# Exact height certificate for CRT value-polynomial reconstruction

2026-10-29 — receiving review requested; new load-bearing reconstruction bound.

The input is the accepted perturbed Choi–Lam G in input.json. Its normalized value polynomial P is the primitive integer polynomial of degree40 with positive leading coefficient whose roots are the40 distinct normalized stationary values. Existence, distinctness, no isotropic critical ray and projective coverage are already certified by the accepted shape/boundary and modular primitive-element witness. This does not assume a proposed CRT candidate is P.

Set D=358400000, so all four cubics H_i=D((partial_i G)/4−lambda Qq_i) have integer polynomial coefficients a_{i,e}+lambda b_{i,e}. The220×220 coefficient matrix has rows given by degree9 monomial multiples of those cubics. At every normalized critical value, the degree9 monomial evaluation vector of its ray is nonzero (q0^9=1) and lies in this matrix's kernel. Thus its determinant vanishes at all40 distinct roots of P, so P divides detM over Q. Gauss's lemma gives an integer cofactor because P is primitive. The full matrix atlambda0 has determinant333279776 modulo1000000007, proving detM is not the zero polynomial. This direct kernel/divisibility proof DOES NOT depend on the classical resultant quotient identity. The separately checked112×112 minor determinant560786759 modulo that prime is retained only as redundant diagnostic evidence.

For each block define the exact positive integer S_i=sum_e(|a_{i,e}|+|b_{i,e}|)^2. On the complex unit lambda-circle, every corresponding matrix row has Euclidean norm at mostsqrt(S_i). The row-block counts are[84,64,45,27]. Therefore Hadamard gives

 max_{|lambda|=1}|detM(lambda)| <= sqrt(W), W=product_i S_i^{count_i}.

For a nonzero complex polynomial A=a product(lambda−r), its Mahler measure M(A)=|a| product max(1,|r|) also equals exp(mean_circle log|A|). A nonzero integer polynomial has M>=1. Multiplicativity applied to detM=P C with integer C gives M(P)<=M(detM)<=max_circle|detM|. Every coefficient of a degree40 polynomial has absolute value at most its corresponding binomial coefficient times M(P), hence at most2^40 sqrt(W).

The executed exact bound is H=2^40 ceil(sqrt(W)), a6613bit integer retained in value_polynomial_height_bound.json. Every coefficient of the unknown primitive P is at mostH in absolute value. After making P monic, each rational coefficient in reduced form has numerator and positive denominator at mostH. This proof uses no numerical estimate of the candidate coefficients.

If an independently constructed primitive integer candidate also has all coefficients bounded byH, and its monic rational coefficients agree with the actual modular characteristic polynomial modulo pairwise distinct good primes of product m>2H², then the candidate is exact. Indeed for corresponding reduced fractions a/b and c/d, denominator invertibility gives m|(ad−bc), whereas |ad−bc|<=2H²<m. Thus they are equal. The required threshold2H² is a13227bit integer. Each prime must certify valid reduction of the quotient basis, norm inversion and rational input denominators; candidate denominators must also be invertible. These are exact modular certificates, not probability-of-random-prime assertions.

The modular quotient algorithm can therefore replace an expensive rational identity check by enough exact modular matches plus this height bound. The bound alone does NOT prove the candidate matches at any prime; the peer's reconstruction/replay must supply all modular checks and modulus product. No generic optimized runtime follows from this instance certificate.
