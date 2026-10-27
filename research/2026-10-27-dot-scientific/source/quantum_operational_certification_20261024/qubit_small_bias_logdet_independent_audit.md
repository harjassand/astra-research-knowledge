# Independent coherent qubit-reference small-bias logdet receiver

PASS, 27 October 2026, including the source-adaptive head-order extension. This is a pointwise logdet theorem, not an inverse-trace sign theorem.

The actual spin-flip identity gives spectrum(NM)=spectrum(S/2), S=M+3I-2R tensor I. Along M_t=R tensor I+tC, Tr_R C=0 and EM_t=I; both endpoints are faithful and satisfy the stated norm cap, hence so does the segment. R<=13I/12 yields S_t>=M_t+5I/6>=(17/12)M_t. No commutation or unconditional pinching is used.

For positive inverse heads B<=aA, the tensor difference a²A^T tensor A-B^T tensor B=(aA^T-B^T) tensor aA+B^T tensor(aA-B) is PSD. Vectorization therefore gives the claimed quadratic-form comparison for arbitrary Hermitian C. This verifies the noncommuting Hessian step. Exact arithmetic gives1-2(12/17)²=1/289. Since M_t<=2I, its inverse quadratic form is>=||C||²/4; integration against1-t gives margin||C||²/2312. The derivative at zero vanishes because both inverse heads are physical-only and Tr_R C=0. The starting logdet gap is exactly2F3(R), paid by the independently received scalar inverse-trace theorem and radial integration. Equality forces C=0 and R=I. Constants checker replay matched nonmutating.

For the closed singular case under the uniform bias gate, S>=5I/6 stays faithful while detM=0, so the determinant statement is immediate; no finite singular logdet is invented.

For the source-adaptive variant, applying the unital physical conditional expectation to S-cM>=0 gives3I-(c+1)R>=0, precisely the same LMI at M0=R tensor I. The LMI is affine in M along the fixed-R segment, hence holds throughout. The preceding Hessian proof applies for c>=sqrt2 without an upper spectral cap. For c>sqrt2, ||R||<=||M|| controls every path norm and yields the stated(1-2/c²)||C||²/[2||M||²] margin. Failure of this LMI gives no negative example. Differentiating a positive logdet result to infer inverse-trace positivity is not licensed.
