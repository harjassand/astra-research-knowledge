# Independent receiving review: two rotation records to four spinor programs

2026-10-29. Reviewer `producer-workspace/review_finite_quantum_sampler`. **Accepted at the exact conditional finite-dimensional program-conversion scope.** This review covers the author's frozen `four_program_extension/GOVERNING_v2.md`, construction and certificate. It does not accept the reviewer's separate symmetrized two-output candidate or claim optimality.

## Independent exact reconstruction

I derived the rotation polynomials from R_ij=Tr(sigma_i V sigma_j V†)/2 for V=wI-i(xX+yY+zZ), rather than copying the author's displayed nine polynomials. Their 35 degree-four exponent tuples are distinct and exhaustive. Expanding all ordered products R_i R_j gives an independently constructed coefficient matrix M of shape35×81. The retained rational B satisfies B Mᵀ=I35 exactly; this itself proves rank35. No floating pseudoinverse or fit is used.

I independently enumerated all256 ordered four-spinor tensor positions to construct J. For exponent alpha, its column appears4!/prod alpha_i! times, so JᵀJ is precisely the stated multiplicity diagonal W. With T=JB, the exact check T Mᵀ=J proves T(vecR tensor vecR)=q^tensor4 as a polynomial identity for every quaternion, including nonunit ones. The output's256 entries contain only35 distinct degree-four monomials; this is not assuming256 independent input features.

## Contractivity without numerical spectrum inference

Set F=TᵀT, a symmetric rational81×81 matrix. In addition to reconstructing it, I checked exactly

F(16F-I)(8F-I)(16F-3I)=0.

Thus its eigenvalues lie in {0,1/16,1/8,3/16}, since F is real symmetric. Traces of I,F,F²,F³ give multiplicities46,25,1,9. As a separate structural check, the four Lagrange spectral projectors built as products (F-bI)/(a-b) are each exactly symmetric and idempotent and sum to I. This supplies an exact positivity/spectral certificate independent of the author's `eigenvals()` result.

Therefore K=(4/sqrt3)T has K†K eigenvalues0,1/3,2/3,1. It is a valid Kraus contraction, including its unit-singular-value sector; strict contractivity is unnecessary. The known complement sqrt(I-K†K) exists. A finite-dimensional Stinespring realization uses known algebraic controls, not source inversion, an unknown-operation oracle or an uncertified SDP factor. Rational2T is also contractive with maximal squared singular value3/4.

## Probability and physical interpretation

For unit q, c=vecR/sqrt3 is normalized and c tensor c=(vecR tensor vecR)/3. Hence K(c tensor c)=4 q^tensor4/(3sqrt3), of squared norm16/27. On success the four normalized output factors are exactly |q>, not four noisy estimates. Rational2T instead succeeds with probability4/9. The even tensor degree removes the q versus -q gauge ambiguity. The matrix K is algebraic, not rational; only T and2T are rational.

This uses TWO already extracted rotation programs. Under the previously reviewed fixed full-joint symmetry and protected-register premise, each successful extracted program is pure and decoupled from all retained source memory and references. Conditional acquisition correlations do not prevent their joint state from being c tensor c. The trusted transducer therefore preserves decoupling on success. It does not require iid acquisitions, but it also does not establish that two programs will ever be acquired.

Each output may be mapped by the already reviewed known Bell-basis conversion into a normalized Choi program. A specified identity-Bell outcome implements V/2 on an arbitrary payload, or V†/2 after the known spinor sign operation. One specified gate has success1/4 conditional on transduction, yielding combined probability4/27. Four specified gate successes, on independent or jointly entangled payloads, have conditional probability(1/4)^4 and combined probability1/432. These are conditional on possession of the two rotation programs and exclude their acquisition probability. All-input validity follows from the exact Kraus factors, not assumptions about payload states.

The four programs may support different attempts, but unknown payload damage on a failed Bell outcome prevents treating them as four harmless retries on the same input. There is no supplied multi-program retrieval protocol with improved single-payload success, no automatic correction of nonidentity outcomes and no reusable deterministic program. Gate conversion consumes programs.

## Resource and dependency boundary

The output contains four four-dimensional programs (eight qubits in a direct encoding), plus paid heralding/dilation workspace and control. The source's hidden environment is not reconstructed, but acquired quantum records, isolated coherent storage, exact common symmetry, gates, readout and any finite-precision implementation are required resources. This packet specifies a known finite-dimensional dilation mathematically; it does not compile that dilation to a calibrated native gate set or show a useful device runtime. Exact algebraic rotations are not implicitly exact Clifford+T operations.

This extension improves only the post-acquisition conversion over the frozen simple v1 map. It does not improve the prior exterior extraction probability, which can be zero or extremely small, nor its fragility to approximate symmetry or false heralding. The original support-wording erratum remains binding: zero exterior yield follows from common single-label support dimension below8, not from low rank of the joint record state. No practical recovery, noisy robustness, acquisition rate, novelty, optimum success or conventional-controller advantage is established here.

Evidence: `independent_exact_check.py` and its JSON reproduce all matrix/identity/projector checks using exact SymPy rationals and independent adjoint coefficients. Original source files were not altered. This is independent mathematical verification, not a physical measurement or accepted engineering implementation. Prior exterior/programming machinery and its primary-source comparison remain as in the earlier independently reviewed packet.
