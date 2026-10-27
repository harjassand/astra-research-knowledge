# Pointwise reverse-logdet with small physical bias and coherent qubit reference

27 October2026. Exact conditional-coherence receiver for the pointwise determinant problem. This is not an unconditional physical/reference pinching claim and is not merely an integrated VALUE result.

Let M>0 on C3⊗C2 satisfy EM=I6 and M≤2I6. Define the physical marginal operator

R=(1/2)Tr_R M, TrR=3.

Suppose R≤(13/12)I3. Then

F(M):=2logdet(NM)−logdetM
 ≥2F_3(R)+||M−R⊗I2||_HS²/2312≥0,              (1)

where F_3(R)=2logdet(W3(R))−logdetR is the already received scalar-reference determinant gap. Equality holds exactly at M=I6. The reference coherence in M need not commute with R or with its own block coefficients.

## Actual spin-flip receiving

The received qubit-reference state-inversion identity makes NM spectrally equal to

S/2, S=M+3I6−2R⊗I2.

Set C=M−R⊗I2, so Tr_R C=0. Along the fixed-physical-marginal path

M_t=R⊗I2+tC, 0≤t≤1,
S_t=M_t+3I6−2R⊗I2,

both sources remain faithful and M_t≤2I. The actual marginal E(M_t)=I also survives, because E(M)=I and TrR=3. No arbitrary reference twirl is imposed on the source.

The small-bias assumption gives

S_t≥M_t+(5/6)I≥(17/12)M_t.

The second inequality uses M_t≤2I. This source-linked order is the quantitative mechanism; it does not hold throughout the unrestricted norm ball.

## Conditional Hessian comparison

Let G(t)=2logdetS_t−logdetM_t−12log2. Exact differentiation gives

G''(t)=Tr[M_t^(-1) C M_t^(-1) C]
 −2Tr[S_t^(-1) C S_t^(-1) C].

Since S_t^(-1)≤(12/17)M_t^(-1), Kronecker-product order of positive matrices yields

Tr[S_t^(-1) C S_t^(-1) C]
 ≤(12/17)^2 Tr[M_t^(-1) C M_t^(-1) C].

This is valid for Hermitian C without commutation: vectorization expresses the quadratic forms through the positive tensor products B^T⊗B. Hence

G''(t)≥(1/289)Tr[M_t^(-1) C M_t^(-1) C]
 ≥||C||_HS²/1156,

where the last bound uses M_t≤2I. At t=0, both inverse heads are physical-only tensor identity, so Tr_R C=0 implies G'(0)=0. Integrating with weight1−t gives

G(1)≥G(0)+||C||²/2312.

The initial source is R⊗I2, so G(0)=2F_3(R)≥0 by reference_classical_inverse_trace_exact_receiver.md and radial integration. This proves(1).

For a singular M satisfying the same closed constraints, S≥5I/6 remains faithful while detM=0. The determinant inequality is then immediate (or the logarithmic difference tends to+infinity); no finite value is assigned to logdetM itself. Equality in the faithful case requires C=0 and R=I3, hence M=I6.

## Scope and remaining stationary sector

Any reference-two counterexample to the pointwise determinant target must violate this physical-bias gate: λ_max(Tr_R M/2)>13/12. The statement does not by itself prove the stronger inverse-trace inequality R(M)≥0 in this region, since differentiating a positive logdet bound would be invalid. The unrestricted inverse-trace stationarity problem remains open with its actual upper-face normal. The root's unconditional physical-pinching counterexample is fully compatible with this conditional fixed-marginal Hessian argument.

## Source-adaptive head-order version

The mechanism is more general than the uniform13/12 bias gate. For any faithful qubit-reference source with EM=I, define R and S as above. If the ACTUAL LMI

S≥cM for some c≥sqrt2

holds, then F(M)≥2F3(R)≥0, without requiring M≤2I. Indeed conditional expectation onto the physical algebra sends the endpoint LMI to3I−(c+1)R≥0, which is exactly the same LMI at M0=R⊗I. Linearity preserves it along M_t. The preceding Hessian argument then gives convexity along that actual coherence path.

For c>sqrt2 the quantitative form is

F(M)≥2F3(R)+(1−2/c²)||M−R⊗I||²/[2||M||²].

Here ||R||≤||M|| ensures the whole path has norm at most||M||. The uniform13/12 gate is simply a readily checked sufficient condition with c=17/12 and||M||≤2. This source-adaptive LMI does not follow automatically for a general physical source; failure of the LMI is not a determinant or VALUE counterexample.
