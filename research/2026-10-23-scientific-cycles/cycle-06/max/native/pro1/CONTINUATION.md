# Continuation: temporal length beyond the quartic product-block law

## Owned state and source

The unchanged Cycle4 ZIP is in preserved/. It proves a strict quantum-capacity
gain on the same coherent recurrent qutrit tree. Read FIXED_BLOCK_ORDER.tex with
INHERITED_COMPRESSION.tex, REVIEW_STATUS.md, FAILED_ROUTES.md and the focused
contributions. COMPLETE_PROOF.tex.txt merges the entire proof for private
UTF-8 reading. Do not certify the result from this continuation summary.

Bath: C2_seed tensor F(C2); S_j prepend color j, R exchanges vacuum seeds.
U=[[R,S1,S2],[S1*,0,0],[S2*,0,0]], V=alpha U+i beta I.
Depth plus port color charge is conserved, including R. Actual tau_pi has
depth mass (2/3)3^-ell and remains fixed. All forward calls/outcomes/retained
registers count. No bath access/reset/fresh bath/preshared entanglement,
postselection, timing channel or terminal-return promise.

## New upper and matching order

Let k be fixed and Q_k count colored input ports. Independent input blocks
rho_1 tensor ... tensor rho_n may be nonidentical and horizon dependent, but
each commutes with Q_k. There is still one evolving physical bath.
For beta <= beta_k=(3/8)^(2k)/(64 k^4 ln2), the full proof gives

    Ic/(nk) <= 3/2 + 8 k^5 ln2 beta^4.

This upper is uniform in n, all allowed block choices, and EVERY normal bath
initializer, including infinite-entropy/infinite-mean states. Bounded charge
transfer and finite R,B entropies avoid infinity minus infinity.
For actual tau_pi, padded pair inputs and the new coding criterion give
Theta_k(beta^4) optimized asymptotic excess for every fixed k>=2.
This is a restricted coherent-information result, not a general capacity
converse. The inherited exact identical-single-site theorem is preserved.

The explicit constants also handle k(beta)<=c ln(1/beta),
c<1/[2 ln(8/3)], with excess O(beta^4 ln^5(1/beta)).
This excludes lower beta powers in that controlled window, not logarithmic
enhancement or faster-growing blocks. Inter-block correlations, charge-changing
coherences and feedback are outside this upper.
The k4 threshold is far below 1/512: do not use it as a numeric upper at the
selected angle.

## Exact mechanisms retained

G_s=Q_k-W_k*Q_kW_k is bounded by k. For charge-preserving rho,
D_s(rho)=Tr_input[(rho tensor I)G_s] commutes with depth. Above depth k-1,
matching charge histories have stay counts of equal parity, killing linear
beta terms. The root is not governed by that parity. Critical sigma=rho_c^k,
rho_c=diag(1/2,1/4,1/4), has the positive boundary margin
D_s(sigma)>=(3/8)^k P_<k. This absorbs near-reference root corrections.
Far states pay relative entropy, using S(rho)-1.5k=m-D2(rho||sigma).

Generic four-call inputs do NOT give a scalar depth chain. The exact example
sigma+epsilon(|1000><0100|+h.c.) has drift 2epsilon ab(I-S1S1*).
The representation JSON exports the full 81-input by16-prefix polynomial,
tensor identity on the seed and untouched tail.

For any charge-preserving block, homogeneous bath Kraus operators give
positive effects A_Delta summing to I and commuting with L. Exactly,

    Phi*exp(tL)=[sum_Delta exp(t Delta)A_Delta]exp(tL).

Uniform negative operator drift on depths>=k implies an exponential moment
with t=kappa/(2k²), lambda=1-kappa²/(4k²), and finite root remainder.
The proof carries this through spectral types and the inherited compression
operation, preserving r², the auxiliary CPTP normalization and polar repair.
One code sequence has rate S(rho)/k and pointwise vanishing full-diamond error
for every fixed normal initializer. Scalar/radial depth closure is unnecessary.
The uniform upper quantifier does not make this lower error limit uniform.

Actual non-scalar receiving use:
rho4=omega tensor omega - x c(|1000><0100|+h.c.), with omega the Cycle4
pair density. Deleting this reducing 2-by-2 coherence raises entropy, and
bulk drift=-2kappa2 I+2x kappa2(I-S1S1*)<=-2kappa2(1-x)I.
It gives actual arbitrary-reference codes; its tiny coefficient is not the
next optimization target.

## Selected next scientific question

Does temporal extent beyond the controlled window change the small-angle
order? Study the full operator variational benefit A_k/k together with a
uniform nonlinear window.

For charge-preserving trace-zero X,Y, TrQX=0, let rho_b=sigma+bX+b²Y,
b=beta². Put H_k(X)=Tr(sigma^-1 X²)/(2 ln2) and m=TrQY. The exact finite
prefix polynomial G_k(b) gives T_k(X) by contracting its b coefficient:

    entropy excess=b²[m-H_k(X)]+O_k(b³)
    bulk drift=b²[T_k(X)+2m I]+O_k(b³).

If H_k(X)<m<-(1/2)lambda_max T_k(X), strict positivity, negative exact drift
and actual coding follow for sufficiently small fixed beta.
Y=(4m/k)sigma(Q_k-k/2) realizes the required charge shift.
A_k=sup_X[-lambda_max T_k(X)/2-H_k(X)] is per block; A_k/k supplies
attainable per-call leading coefficients by strict-margin approximation.
It is not a formula for capacity or the complete block-input optimum.

The next operation is uniform control of T_k and the nonlinear remainder.
Uniform-prefix traces cannot replace the maximum eigenvalue. Included
k=2 through 6 susceptibility numbers are finite diagnostics, not a growing-k law.
Any growth must survive input positivity, a strict exact operator drift and
the coding limit with beta fixed before horizon. The logarithmic-window upper
is an existing constraint. No current result determines divergence of A_k/k.

The fixed-four-call improved-power attempt is closed in the proved class.
Do not reopen iid stabilization, balanced-only, diagonal-biased, product-
stationarity or reflecting-cutoff routes. Protected programmes keep their
owners and closures. Internal proof and challenge are not external acceptance
or historical priority. Useful finite blocklength, efficient encoding and
physical performance remain unestablished. Discovery/model/encoder costs are
unknown; replay cost is not discovery cost. Max integrates; delivery does not
imply reading, acceptance or integration.
