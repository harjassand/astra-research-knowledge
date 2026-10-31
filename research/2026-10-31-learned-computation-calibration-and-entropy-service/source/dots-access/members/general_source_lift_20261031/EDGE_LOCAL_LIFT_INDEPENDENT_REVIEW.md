# Independent review: edge-local continuous pure lift

## Verdict and exact source

PASS as an explicit finite-dimensional construction and return-rate bound, not a general efficient compiler. I read the original candidate and then fully reread the updated source incorporating the requested exit-sum and control-algebra precisions. Final bound source: `EDGE_LOCAL_CONTINUOUS_LIFT_CANDIDATE.md`, SHA-256 `fd7fab42d5ad75caa894a3bb6429334c8bd1fae33dcfc26457b984ccd9395c49`. The original submitted source was `e9cccf31c1898fcffdd07af8080c965f55de9eef25a6d967d27d9f502cc0539c`; this receipt does not silently bind those different bytes as the final source.

## 1. Index and sign check

Rates q_yx denote x to y. The edge-rate sums exclude y=x, equivalently q_xx=0 here rather than using the negative diagonal of a generator matrix. The vector in the edge jump annihilates psi because sqrt(pi_x)-sqrt(pi_x/pi_y)sqrt(pi_y)=0. The proposed off-diagonal Hamiltonian is Hermitian: its bracket is real and antisymmetric under x,y exchange. Multiplication by psi gives the difference between pi_x times total outgoing rate and total incoming stationary flux, which vanishes by stationarity. Thus H psi=0 and every jump annihilates psi; Pi is exactly stationary.

For D diagonal, direct expansion of D[L_yx]^dagger(D) gives diagonal contribution q_yx(d_y-d_x) at x, zero at y, and xy off-diagonal contribution q_yx sqrt(pi_x/pi_y)(d_x-d_y)/2. The reverse edge contributes the opposite orientation. With the written H sign, i[H,D]_xy cancels their sum. The remaining diagonal generator is exactly the backward classical rate generator, not its time reversal. Nonreversible stationary currents are correctly carried by H.

## 2. Operator-valued algebra and controlled equivalence

The same computation holds with each d_x replaced by an arbitrary system/reference operator D_x, since all source coefficients are scalars and the cancellation is linear. Adding a source-diagonal system Hamiltonian preserves that algebra and adds precisely its blockwise commutators. Consequently the Heisenberg evolution of the system-valued diagonal algebra agrees with the CQ classical-source evolution.

Finite controlled experiments follow by backward composition provided every instrument branch, with outcomes retained, has an adjoint preserving this algebra and the prescribed classical/CQ restriction. The final source now states this condition explicitly. Two source-system initial states with the same diagonal system blocks then give the same such experiments; in particular psi as source preparation has stationary diagonal law pi. This is an observable-process equivalence, not equality of the full quantum density matrices or their arbitrary coherent-source outputs.

The correction is substantive: mapping diagonal input states to diagonal output states alone is too weak. The channel measuring a source qubit in the X basis and recording the result in a Z register sends diagonal inputs to diagonal outputs but has adjoint Z -> X, so it can distinguish otherwise invisible coherences. That operation is excluded unless an additional classical-compatible implementation is specified. No general old-quantum-dilation replacement follows.

## 3. Pure-return inequality

Since the generator is unital in the adjoint and the Hamiltonian commutes with Pi, L^dagger Q=-sum L_yx^dagger Pi L_yx. The candidate's expression for C follows by applying each jump adjoint to psi. It is positive. Its quadratic form vanishes exactly when v_x/sqrt(pi_x) agrees across every active edge. If the underlying undirected graph is connected, its kernel is span(psi); directed irreducibility is a sufficient premise as stated. Positivity of pi is essential for this parameterization and for the jump coefficients.

For C>=c_* Q, differentiate e^{c_*t} exp(tL^dagger)Q. Its derivative is the positive adjoint map applied to L^dagger Q+c_*Q, multiplied by a positive scalar, and is nonpositive. Therefore exp(tL^dagger)Q<=e^{-c_*t}Q. This is an operator inequality, hence also bounds leakage for arbitrary reference-correlated states after tensoring identities. It does not presume that a classical gap automatically controls a different quantum realization.

For v=sqrt(pi) f perpendicular to psi, f has pi-weighted mean zero. The quadratic form is sum q_yx pi_x pi_y |f_x-f_y|^2. Lower bounding pi_y by pi_min and using the stated additive-symmetrization Dirichlet form gives exactly 2 pi_min g ||v||^2. There is no missing factor two. The construction without connectedness still exists, but the claimed strictly positive return constant is conditional on connectedness/irreducibility.

## 4. Refresh and dark-gauge contrast

For uniform complete refresh, the ordered-edge sum of (|x>-|y>)(<x|-<y|) is 2d Q. Including 1/d^2 gives C=2Q/d. Here L^dagger Q=-(2/d)Q exactly, so the leakage exponent is precisely 2/d, not just a lower bound.

The coherent reset generator with jumps J_j=|psi><j| has sum J_j rho J_j^dagger=Pi Tr(rho) and sum J_j^dagger J_j=I. Its diagonal restriction is the same classical refresh generator, and its return rate is one. Shifting each jump by -sqrt(pi_j)I makes it dark. The aggregate gauge commutator vanishes because sum sqrt(pi_j)J_j=Pi is Hermitian, so the generator is unchanged. Directly sum J'_j^dagger Pi J'_j=Q. The example therefore diagnoses a poor realization choice, not an intrinsic lower bound for the classical source.

Preparing the coherent common destination psi is actual access. A classical sampler does not itself provide its coherent preparation or the required controlled adjoints. The return matrix C here is sum L^dagger Pi L, not merely the no-jump loss sum L^dagger L; confusing them would change the return claim.

## 5. Diagnostics and resources

I read and reran `check_edge_lift.py`. All six positive nonreversible dense cases d=2 through 7 passed the Hamiltonian, dark-state, stationary-state, classical restriction, Q-loss and gap comparisons, with maximum reported residual below 10^-15. Complete-refresh identities d=2 through 8 passed. These are floating-point sanity checks, not the proof or a synthesized succinct implementation.

The formulas use explicit rates, positive stationary ratios, a current Hamiltonian and a return certificate. State preparation, coefficient evaluation, jump/selector implementations, norm bounds, precision and inverse-gap costs must all be charged. The sufficient lower bound can be exponentially small in source bit count. Dense numerical spectral work also pays full dimension, and a rigorous numerical lower certificate requires error control. The source correctly leaves efficient acquisition and a whole fast-source compiler unearned.

## 6. Strong primary comparison

The inspected primary abstract of [Kraus et al., Preparation of Entangled States by Quantum Markov Processes](https://arxiv.org/abs/0803.1463) already constructs dissipative preparation of arbitrary pure stationary states and discusses quasi-local examples and relaxation. Pure-state engineering itself is therefore established machinery. That abstract does not establish the exact prescribed classical restriction of the present edge formula; no contrary novelty claim follows.

The inspected primary abstract of [Fagnola–Skeide, Restrictions of CP-Semigroups to Maximal Commutative Subalgebras](https://arxiv.org/abs/math/0703001) gives restriction criteria for CP maps and Markov generators. Invariant classical observable algebras are likewise a standard mathematical subject. This bounded inspection does not determine whether a broader earlier construction reproduces these exact rates and the pure-return bound.

Earlier abstract-only coherification comparisons remain acknowledged; no denied/timed-out full text or alternate copy was retried. The useful consequence of this source is an explicit existence-versus-efficient-realization distinction, not a first pure-state lift, first classical embedding, practical advantage or priority assertion.

## Final scope

Accepted finite edge-local pure lift with correct current sign, classical diagonal controlled restriction under the strengthened adjoint-algebra condition, and explicit dimension/stationary-weight-sensitive return bound. The complete-refresh contrast is valid. General succinct compiler access, favorable return scaling, arbitrary coherent-source equivalence and novelty remain outside this receipt.
