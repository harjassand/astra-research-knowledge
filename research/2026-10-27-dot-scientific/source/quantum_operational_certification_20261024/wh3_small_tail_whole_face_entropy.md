# A whole logical entropy face survives the fixed-lift obstruction

## Certified theorem

Let

    psi=(4|01>+4|10>+4|21>+|22>)/7, phi=|00>,
    V|0>=psi, V|1>=phi,
    N=(W3 tensor id_R)V(.)V*, M=Tr_A V(.)V*.

For EVERY logical qubit density matrix Y, including arbitrary complex coherence and boundary states,

    2 S(NY)-S(Y)-S(MY) >= ln(3)+0.0904514158.

Entropies are in nats. This is a finite computer-assisted proof using a certified cover and outward interval spectral bounds, not a sampled minimum. It proves the original entropy inequality on this entire code face even though the fixed full-Gram signed-lift comparison is impossible for the same code.

It does not prove complete BKM comparison, logical convexity, the entire tail-parameter family, or the unrestricted W3 conjecture.

## Exact phase reduction and cover

The physical unitaries

    U_A(theta)=diag(1,e^(i theta),1),
    U_R(theta)=diag(1,e^(i theta),e^(i theta))

map psi to e^(i theta)psi and leave phi fixed. Werner–Holevo covariance transforms the output by conjugate U_A and by U_R. Consequently all three entropies depend only on the magnitude of logical coherence.

Write a representative logical state as

    Y(u,v)=(I+u sigma_z+v sigma_x)/2,
    v>=0, u^2+v^2<=1.

Fix m=64. For every integer i=-64,...,64 and j=0,...,64, take (i/m,j/m) if it lies in the unit disk; otherwise project it radially onto that disk. There are 8385 declared centers.

Rounding a point in the half-disk to its nearest square-grid point gives Euclidean error at most sqrt(2)/(2m). Projection onto the disk is nonexpansive and leaves the original point fixed. Qubit trace distance is half the Bloch-vector Euclidean distance. Thus every state is within

    delta=sqrt(2)/(4m)=sqrt(2)/256

of a center. This includes the circular boundary and the diameter; no region is discarded.

## Continuity penalty

The exact source output support has dimension 5 for this fixed code. The reference dimension is3 and logical dimension 2. Trace distance contracts through both channels. Audenaert's sharp entropy continuity inequality, Theorem 1 / Eq.(6), gives

    |S(rho)-S(sigma)| <= h2(delta)+delta ln(d-1).

Here trace distance includes the factor1/2. Converting the source's base-2 statement to nats gives the formula above. Primary source: https://arxiv.org/pdf/quant-ph/0610146 .

Applying it to the three entropy terms yields

    |Delta gap| <= 4 h2(delta)+delta ln(32)
                 < 0.156055607105101.

This modulus is monotone at the small radius used here, so an upper bound on distance suffices.

## Rigorous center entropies, without trusting floating eigenvalues

The script first constructs the actual physical skew Kraus operators and an exact algebraic orthonormal basis of their five-dimensional common range. It verifies the basis and range symbolically. Every center matrix is then evaluated in 40-digit outward interval arithmetic from rational numbers and square roots.

NumPy eigenvectors and eigenvalues are only proposals. For every output matrix A and every reference matrix, the script verifies outward interval bounds

    ||A-Q Lambda Q*|| <= r < 10^(-10),
    ||Q*Q-I|| <= epsilon < 10^(-10).

The operator norms are bounded by dimension times the maximum absolute interval entry. This does not require eigenvalue separation.

Let U be the polar unitary of Q. Since epsilon is small,

    ||Q-U|| <= epsilon,
    ||Q|| < 1.1,
    ||Lambda|| < 2.

Therefore

    ||A-U Lambda U*|| < r+5 epsilon < 6*10^(-10) < eta,
    eta=10^(-8).

Weyl's inequality gives matching eigenvalue errors below eta, even at repeated or zero eigenvalues. Clipping a proposed eigenvalue to [0,1] cannot increase its error from a true density-matrix eigenvalue.

For f(x)=-x ln x on [0,1], concavity gives the scalar modulus

    |f(x)-f(y)| <= eta(1-ln eta) whenever |x-y|<=eta.

Interval logarithms evaluate the entropy of each clipped proposed spectrum. The total spectral allowance is 13 eta(1-ln eta): two copies of 5 output eigenvalues and 3 reference eigenvalues. The input entropy is evaluated directly from the exact interval Bloch radius. Pure centers have exactly zero input entropy.

## Actual execution receipt

All 8385 centers passed. The recorded center lower bound was above 0.24650702292015 nats. Subtracting the certified continuity penalty gives a global lower bound above 0.09045141581505. The theorem deliberately reports the rounded-down decimal 0.0904514158, and the script explicitly asserts that value.

The first full execution took 22.7657seconds and used 59188 KiB peak RSS. Its maximum verified reconstruction norm bound was below 6.37e-15; the maximum orthogonality norm bound was below 1.39e-14. A receipt-refresh replay uses exactly the same frozen cover and arithmetic, with no enlargement or changed mathematical claim.

Authoritative files:

- `wh3_small_tail_entropy_net_certificate.py`
- `wh3_small_tail_entropy_net_certificate.json`

The proof's cover, phase reduction, support dimensions, interval residual argument, clipping, scalar entropy allowance, and continuity modulus were independently audited within this research session. This is internal mathematical verification, not external peer review or a proof-assistant formalization.

## An open interval of tail parameters, without another net

For

    psi_t=(|01>+|10>+|21>+t|22>)/sqrt(3+t^2),
    phi=|00>,

write psi_t=cos(theta_t)psi_0+sin(theta_t)|22>, with theta_t=arctan(t/sqrt(3)). Thus

    ||V_t-V_(1/4)|| <= |theta_t-theta_(1/4)|
                     <= |t-1/4|/sqrt(3).

For every fixed logical state, a common purification shows that the trace distance between the two encoded states is no larger than this operator-norm bound. Channels and partial traces contract that distance.

For t in [0.246,0.254], let delta_t=1/(250 sqrt(3)). The input entropy is unchanged. Using the full physical output dimension 9, rather than incorrectly reusing the moving five-dimensional support, gives

    |Delta gap| <= 3 h2(delta_t)+delta_t ln(128)
                 < 0.060184989.

Consequently EVERY logical state for EVERY t in this interval satisfies

    2S(N_tY)-S(Y)-S(M_tY) > ln(3)+0.03026.

This is a continuity corollary of the one fixed-code proof, not a second numerical parameter scan.

## Analytic boundary information and the remaining mechanism

For pure logical states of population x at t=1/4, the physical input marginal has

    e2(x)=17x/49-289x^2/2401,
    det(x)=256x^3/117649.

The largest eigenvalue decreases and the smallest increases with x. For the largest root, differentiation of the characteristic polynomial uses

    e2'(x) lambda_max >= (255/2401)/3 > 3*(256/117649).

For the smallest root, lambda_min<=3det/e2 and e2>=x e2' give the opposite derivative sign. Degeneracies and x=0 follow by continuity. Thus the physical spectrum becomes more mixed as x increases.

The pure-input entropy expression is Schur-concave on the three-simplex: for its scalar summand f(p)=-p ln p+(1-p)ln(1-p), the derivative ordering follows from

    p_i(1-p_i)-p_j(1-p_j)=(p_i-p_j)p_k.

Hence the worst pure boundary point is exactly psi. This explains the boundary minimum found by the certificate, but it does not establish a mixed-state maximum principle.

A parameter-independent analytic explanation for the mixed interior remains open. The direct characteristic-polynomial coherence derivative has a negative large-resolvent tail, so pointwise positivity of that particular integrand is unavailable. No logical-convexity assertion is inferred from the net proof.
