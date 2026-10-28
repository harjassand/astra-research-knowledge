# Working continuation: retain every spectral block in one-sided effect rounding

28 October 2026. **Unreceived working derivation, not a completed theorem or acquisition claim.** Paused at the parent's request to preserve fresh independence for review of a different matrix-design construction. The received/frozen coherent-branch candidate is `ordinary_binary_povm_coherent_cost_rounding_20261028.md` SHA `df4d15eb7b102092cc7932f7f5d5ac331be37e9a2e7c24b8478af71fb6ea49fc`.

## Target and relaxation

For known W>=0,m>0 and a homogeneous PSD quadratic n(A)=||L(A)||^2, maximize n(A)/(m+Tr W A) over effects0<=A<=I. A real Hermitian-Gaussian covariance X>=0 has rho=E G^2. The fractional SDP

    rho<=I, S=E||L(G)||^2, D=m+Tr W rho, F=S/D

relaxes the actual problem: deterministic G=A gives rho=A^2<=I and Tr W A^2<=Tr W A. No unknown statistical model enters this classical relaxation. The main question is how to round an arbitrary feasible covariance while paying linear cost in the ACTUAL positive effect.

## Ideal exact spectral accounting

Assume for this derivation that the spectral bands of known rho are processed exactly. Let a>=max(1,||L*L||op), delta=min(1/2,m/(64ad)), remove the rho eigenvectors below delta, and partition the remainder into L dyadic bands P_i with p_i/2<rho_i<=p_i. There are K=L(L+1)/2 Hermitian diagonal/off-diagonal components of QGQ, Q=sum P_i.

The removed Hermitian component T=G-QGQ satisfies

    E||T||F^2<=2Tr(P_tail rho)<=2d delta,
    S<=2S_keep+4ad delta.

Thus F>=1 implies S_keep>=S/4. PSD Cauchy, retaining EVERY block, gives

    S_keep<=K sum_components S_component.

For each diagonal block G_ii, variance E G_ii^2<=rho_i<=p_i I. Normalize by sqrt(p_i), perform a Gaussian operator-norm round, and use both effects(P_i +/- G_ii/(R sqrt(p_i)))/2. Their homogeneous affine-offset cancellation is exact. Choose R^2=O(log d) with Gaussian norm-failure budget1/48. On a constant-probability numerator/norm event, the ratio is at least

    S_ii/[8R^2 p_i c_ii],   c_ii=m+Tr W_i.

The weighted diagonal cost sums to at most2D because sum p_i<=2 and p_i Tr W_i<=2Tr W_i rho_i.

For an off-diagonal block B_ij=P_i G P_j, orient indices so p_i<=p_j. Define

    R_ij=E B_ij B_ij*, C_ij=E B_ij* B_ij,
    R_ij<=rho_i, C_ij<=rho_j.

Normalize B_ij by sqrt(p_j), Gaussian-round with norm cap R, and use the EXACT coherent polynomial completion around the LARGE-scale projector P_j:

    A_±=[[2BB*, +/-B],[+/-B*, I_j-2B*B]].

This orientation is essential. For any PSD W and PSD A on the two blocks,

    Tr W A<=2[Tr W_i A_ii+Tr W_j A_jj],

by scalar Cauchy on the positive block matrices. Thus the actual cross terms of W are not discarded. The small-side weighted covariance is controlled on a Markov event. Paley-Zygmund numerator probability1/12, norm failure1/48 and weighted-cost failure1/48 leave a JOINT event of probability at least1/24, without independence. On it one of the two effects has ratio at least

    S_ij/[8R^2 p_j c_ij],
    p_j c_ij=p_j m+2p_j Tr W_j+48Tr(W_i R_ij).

The summed costs obey

    sum_pairs p_j m<=2Lm,
    sum_pairs 2p_j Tr W_j<=4L Tr W rho,
    sum_pairs Tr W_i R_ij<=Tr W rho.

The last inequality uses sum_j R_ij<=rho_i; it does NOT acquire an additional factor L. Including the diagonal components gives total weighted cost at most(4L+50)D.

Selecting the component of largest KNOWN ratio S_component/(weighted cost) would therefore yield the ideal approximation

    actual ratio >=F/[32 R^2 K(4L+50)]

with constant success probability, i.e. O(L^3 log d) approximation rather than discarding off-diagonal moments. This ideal accounting has been derived but has not yet received a separate check script or independent audit.

## Remaining finite-processing work, not silently assumed

The spectral bands above must not be treated as an operational unknown-basis oracle. Here rho is a KNOWN rational covariance contraction, so finite classical approximate diagonalization is plausible, but the following ledger still needs to be completed and checked:

1. Use a rational exactly-unitary approximate eigenbasis and a diagonal upper envelope rho_bar>=rho, with rho_bar<=rho+eta I. Choose eta Tr W=O(m) and eta ad=O(m), so neither actual denominator nor discarded numerator is distorted materially. No empirical eigengap should be assumed.
2. One possible conditioning repair is first to scale X by1/2, then build rho_bar<=I with known strict slack. This loses only a constant in F and avoids upper-band overflow.
3. Rational exact unitarity can in principle be obtained from a finite Cayley-chart approximation to a numerical unitary. A chart phase avoiding the spectrum by inverse-polynomial distance should be selected and paid, rather than presuming rational orthonormal eigenvectors.
4. The accepted effect remains exactly PSD/<=I by a rational norm certificate and polynomial completion. Finite Gaussian precision must protect tiny known S_component and m with BIT precision, not reciprocal-probability retries; the frozen coherent note supplies that local pattern.
5. Score-selection arithmetic, approximate eigenvalue-bin boundaries, SDP objective accuracy and all-history output feasibility must be bound explicitly before promoting the ideal approximation to a finite algorithm.

Even completion of this one-sided theorem would concern known binary POVM optimization. It would not itself preserve the full-CPTP partial-trace equality or establish a new physical source exponent. The strongest conventional learner has the same known-matrix routines.
