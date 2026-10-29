# Independent review: gap-free weighted soft-polar recovery

28 October2026. Result: **ACCEPTED at its stated one-use, supplied-frame/block-access scope.** No algebraic correction to GOVERNING_LEMMA_v1.md is required. The concrete frame construction, efficient normalized access, finite-precision compiled implementation and memory application remain separate obligations.

## Convention and physical channel

I independently expanded the purification rather than relying on root's random tests. With |s>=sum_i |i>|e_i> and <e_j|e_i>=S_ij, the reduced error-index matrix is S, and tracing the source environment gives exactly sum_ij S_ij F_i rho F_j†. For every operator Q on error-index tensor logical input,

    <s,Phi|(Q tensor I)|s,Phi> = Tr[(S tensor I/K)Q].

Thus R=S tensor I/K, NOT S^T tensor I/K. Source TP implies Tr(RG)=1. An exact Gaussian-rational fixture with genuinely complex S and noncommuting R,G gives Tr(RG)=1 but Tr((S^T tensor I/K)G)=44209/40625. The latter is a decisive wrong-transpose negative control.

A=f^(SV)(M/alpha)† is a contraction whenever |f|<=1 on the singular-value domain. Success Kraus operators are the K-row blocks of A. For any square root B of I−A†A, failure Kraus operators |0><r|B, one per physical-output row r, complete their squared adjoints to I_D. This gives a deterministic CPTP channel; the success measurement is not postselection. The square root is an existence description only. An actual heralded block unitary already supplies its physical failure branch, which can be erased and replaced by |0> without synthesizing that square root.

For the actual normalized source purification, the success-vector norm discrepancy plus failure probability is

    L = Tr[R((AM−I)†(AM−I)+M†(I−A†A)M)]
      = Tr[R(I+G−AM−M†A†)].

Since AM=sqrt(G) f(sqrt(G)/alpha), this is exactly the root formula even when R and G do not commute, with zero/null singular subspaces included. The ideal purification has norm1 and the total physical Stinespring output has norm1. Its overlap z with the ideal vector embedded into the success sector satisfies L=2−2Re z and F_e>=|z|²>=2Re z−1. Therefore1−F_e<=L. No lower singular-value hypothesis enters any step.

## Scalar polynomial and weighted bound

The binomial coefficients c_j are nonnegative and at most1. For0<x<=1, the infinite series sums to1/x, so the finite polynomial lies in[0,1]. The omitted tail is at most(1−x²)^(m+1)/x<=exp(−(m+1)x²)/x. At x=0, oddness gives0. Choosing the stated m therefore gives error at most epsilon for singular values at least1/2.

On0<=sigma<=1/2, the ratio(1+sigma²)/(1−sigma²)² is increasing and reaches20/9 at1/2. On sigma>=1/2, the identity(sigma²−1)²=(sigma−1)²(sigma+1)² gives the factor4/9, while sigma<=alpha bounds the residual2sigma epsilon by2alpha epsilon. The resulting scalar inequality is an operator inequality by spectral calculus. Taking its trace against arbitrary positive R preserves order; simultaneous diagonalization with R is unnecessary. TrR=1 yields the claimed(20/9)b+2alpha epsilon bound. Clipping at1 is legitimate because entanglement fidelity lies in[0,1].

Coefficient bit length is polynomial in m: c_j has denominator4^j and numerator binomial(2j,j), and expansion of(1−x²)^j increases coefficient bit length only polynomially. This is not by itself a phase-compilation stability proof.

## Independent checks

check_independent_v1.py does not import the root checker. It includes:
- one exact complex, noncommuting convention/normalization fixture;
-160 independent physical cases with unequal frame-domain/output dimensions, rank defects, near-orthogonal frames and rank-deficient S;
-80 further examples whose F_i are NOT individually isometric;
- direct success-plus-failure Kraus completion and fidelity from the original physical source Kraus family.

Maximum recovery TP residual is below4.76e−15 in the first160 cases. All penalty and bound checks pass. These numerical tests supplement the preceding independent analytic proof; they are not interval certification or evidence of efficient circuit implementation. Root's120-case diagnostic is preserved separately.

## Actual scope accepted

The decoder is independent of S but depends on the known F_i family and its physical block access. The theorem is pointwise over S for which the displayed source is TP. It does not permit correlations between the logical input/reference and a previously retained error-index state merely by naming that state S. It does not infer a uniform multi-use channel from a one-use marginal. A small average defect may be used in an average-fidelity conclusion only with the actual ensemble and normalization assumptions made explicit.

The QSVT circuit and classical preprocessing are discussed separately in QSVT_INTERFACE_ADDENDUM_v1.md. That addendum supplies precise conditional interfaces, not a compiled Schur transform or free access to M/alpha.
