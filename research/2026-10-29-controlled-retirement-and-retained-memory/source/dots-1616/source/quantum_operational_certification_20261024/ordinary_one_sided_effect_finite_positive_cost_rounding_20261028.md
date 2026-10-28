# Finite positive-cost rounding for one-sided effects

28 October 2026. New author construction; independent receiving pending. This closes the finite-processing gap in the preserved `ordinary_one_sided_effect_spectral_block_rounding_working_20261028.md`, without changing that historical working file. It concerns KNOWN rational matrix optimization, not a new source query, unknown spectral projector, full moving-effect decoder oracle, or physical acquisition rate.

## 1. Problem and supplied relaxation

Let m>0, W>=0 be rational, and n(A)=||L(A)||² a homogeneous PSD quadratic on Hermitian k by k matrices. Use the rational Hermitian basis E_ii, E_ij+E_ji and i(E_ij-E_ji), whose Hilbert-Schmidt Gram matrix is diagonal with entries1 or2. Real coordinate covariances and their matrix moment maps are therefore rational; Hilbert-Schmidt norms keep this explicit Gram matrix. The target is

    max_{0<=A<=I} n(A)/(m+Tr WA).                        (1)

A supplied rational covariance Z>=0 defines a centered Hermitian Gaussian G, rho=E G², s=E n(G) and q=Tr W rho. Impose rho<=I. Then

    F_Z=s/(m+q)                                         (2)

is a fractional SDP relaxation: the deterministic covariance of an actual effect A has rho=A²<=I and q<=Tr WA. The perspective transform is an SDP; Tr Z<=Tr rho<=k bounds its feasible domain and a sufficiently small scalar coordinate covariance is strictly feasible. Finite certified optimization uses the same paid standard SDP contract as the received coherent-effect branch. The theorem below rounds ANY supplied feasible Z, rather than presuming an exact optimum.

If s=0, return A=0. Otherwise first replace Z by Z/2. Henceforth rho<=I/2 and denote the resulting quantities by s,q,F. They satisfy F>=F_Z/2. Choose a rational bound a>=max(1,||L*L||op), and

    delta=min(1/16, s/(64ak)),
    eta=min(1/8, m/[8(1+Tr W)]).                         (3)

Tiny positive s,m affect precision bits; no repeat count proportional to their reciprocals is used.

## 2. Gap-free rational approximate diagonalization

There is a finite rational unitary Q and rational diagonal D such that

    rho<=rho_bar:=Q D Q*<=rho+eta I,
    0<D<I.                                             (4)

Here and below Q is a KNOWN classical covariance basis, not an acquired physical source basis. A constructive implementation avoiding any eigengap is as follows.

For k>=2, perform rational approximate Jacobi rotations on rho. If E is the squared Frobenius norm of its off-diagonal entries, an exact two-coordinate rotation at a largest off-diagonal entry decreases E by at least2E/k². Every matrix encountered has operator norm<=1/2, because the implemented rotations are exactly unitary. A rotation with operator error at most d_ctrl changes this energy by at most2k d_ctrl. Set

    d_ctrl<=eta²/(128k³).

Thus the actual energy recurrence is

    E_next<=(1-2/k²)E+eta²/(64k²).                       (5)

Stop when E<=eta²/16, or after the public cap

    k² ceil[log_2(32k/eta²)]

rotations. Starting at E<=k/4, (5) ensures that the cap also reaches that stopping threshold. No eigenvector or distinct-eigenvalue identification is required.

To implement one approximate rotation with EXACT rational unitarity, use its SU(2) representation. Its four real quaternion coordinates lie on S³; changing the overall sign has no effect on conjugation, so choose the scalar coordinate nonnegative. Stereographic coordinates then lie in the unit three-ball, and rational approximations give rational quaternion coordinates through

    (q0,qvec)=((1-||t||²)/(1+||t||²), 2t/(1+||t||²)).

This is exactly on S³. The resulting complex two-coordinate matrix is exactly unitary. A polynomial number of precision bits achieves the stated operator error. Whenever a rotation is still required, its chosen off-diagonal magnitude is at least eta/(4k), so the elementary two-by-two square-root formulas are only polynomially conditioned in k/eta. This is precision-bit dependence, not an inverse-eta number of rotations. The product Q remains rational exactly unitary, with polynomial bit growth over the declared cap. If k=1, use Q=I directly.

Let R=Q* rho Q and D=diag(R)+(eta/2)I. Since ||R-diag(R)||<=eta/4, (4) follows with slack; D<=I/2+eta I/2<I. All residual and energy certificates are rational. This supplies the formerly missing finite spectral step without presuming rational exact eigenvectors or enumerating a fine unitary net.

## 3. Keep every block; remove only a paid tail

Discard the D coordinates below delta. Partition the rest into base-FOUR bands P_i, i=1,...,ell, with

    p_i/4 < (rho_bar)_i <= p_i,  p_i=4^(-j_i).

Every P_i is an exact rational projector Q times a coordinate projector times Q*. The p_i are distinct; sqrt(p_i)=2^(-j_i) is rational. Moreover

    ell<=1+ceil(log_4(1/delta)), sum_i p_i<=4/3.

Let P=sum P_i and T=G-PGP. Since rho<=rho_bar,

    E||T||F²<=2Tr[(I-P)rho]<=2k delta.

Consequently, with s_keep=E n(PGP),

    s<=2s_keep+4ak delta, hence s_keep>=s/4.             (6)

The retained Hermitian matrix PGP has K=ell(ell+1)/2 components: all diagonal G_ii and every Hermitian off-diagonal pair (G_ij,G_ji). No component is dropped because it lies between different bands. PSD Cauchy gives

    s_keep<=K sum_components s_j.                       (7)

Define q_bar=Tr W rho_bar and D_bar=m+q_bar. By(3)-(4),

    D_bar<=m+q+m/8<=2(m+q).                             (8)

All component numerator moments and the following weighted costs are known rational linear functions of Z.

For a diagonal component i put

    b_i=p_i(m+Tr W_i).

For an off-diagonal pair orient i,j so p_i<=p_j, let B=G_ij and

    R_ij=E BB*, C_ij=E B*B,
    R_ij<=(rho_bar)_i, C_ij<=(rho_bar)_j,
    t_ij=Tr(W_i R_ij),
    b_ij=p_j m+2p_j Tr W_j+48t_ij.                      (9)

The total cost satisfies

    sum_components b_j <= (8ell+56)D_bar.               (10)

Indeed the diagonal contribution is at most(4/3)m+4q_bar. The pair baseline costs sum to at most(4/3)ell m. Their large-side terms sum to at most8ell q_bar. Crucially, sum_pairs t_ij<=q_bar because for each small band sum_j R_ij<=P_i rho P_i; this part does NOT acquire another factor ell. These estimates use positivity of W. They do not discard its off-diagonal blocks in a returned effect.

Choose the component maximizing the exactly computed rational ratio s_j/b_j. Equations(6)-(10) imply

    s_j/b_j >= F/[8K(8ell+56)].                         (11)

At least one component has s_j>0. Thus there is no search over exponentially many choices of components or unknown source-dependent signs.

## 4. A finite actual effect for the chosen component

Choose the integer

    R0=2 ceil(sqrt(ceil(log_2(192 max(2,k))))).

The established Hermitian/rectangular Gaussian-series bound gives operator-norm failure at most1/48 at norm threshold R0 sqrt(p), where p=p_i for a diagonal component or p=p_j for a pair. Paley-Zygmund gives numerator at least s_j/2 with probability1/12. For a pair, Markov gives Tr(W_i BB*)<=48t_ij except probability1/48; if t_ij=0 it is zero almost surely. Thus a common favorable event has probability at least1/24 (the diagonal case has more slack). This is a union bound, not independence of these three quantities. Gaussian concentration is imported only at its standard known-matrix statement from Tropp, User-Friendly Tail Bounds, Theorem4.1/Corollary4.2, https://tropp.caltech.edu/papers/Tro11-User-Friendly-preprint.pdf .

Use the already received finite Gaussian coupling construction in `ordinary_binary_povm_coherent_cost_rounding_20261028.md`, Section4, to make the component rational within Frobenius error d_g, except probability1/96. It suffices to choose rational d_g<=1/8 with

    d_g<=sqrt(p)/8,
    d_g sqrt(2a)<=sqrt(s_j)/4,
    d_g sqrt(max(1,||W||))<=sqrt(pm)/4.                 (12)

Explicit rational sufficient bounds use s_j/[32(1+s_j)a] and pm/[16(1+pm)Wbar] for the last two, with rational Wbar>=max(1,||W||). Since sqrt(p) is rational, all requested precisions are finite rational quantities. The imported construction samples dyadic normal coordinates and approximates a covariance factor with polynomial precision bits; it is not a reciprocal-mesh sampler or a TV approximation of continuous and discrete laws.

On the coupled event the numerator is at least s_j/8, the norm is at most R0 sqrt(p)+d_g, and for a pair the small-side cost is at most96t_ij+pm/8. The common probability is at least1/32.

**Diagonal component.** With rational Hermitian Gtilde supported on P_i, put

    T_i=Gtilde/(2R0 sqrt(p_i)),
    A_±=(P_i +/- T_i)/2,

and zero on the orthogonal complement. Certify P_i-T_i²>=0 on its support, equivalently ||T_i||<=1. A failed certificate returns A=0. The favorable event passes with strict slack. Both candidates are effects, their costs are at most m+Tr W_i, and parity of the linear numerator gives

    max_± n(A_±)/u(A_±)>=s_i/(128R0² b_i).              (13)

**Off-diagonal component.** Set Btilde=Gtilde/(4R0 sqrt(p_j)). Certify ||Btilde||<=1/2 using exact rational PSD arithmetic on the two supports. On the favorable event it has strict slack. Return both polynomial completions, zero outside the two supports,

    A_±=[[2Btilde Btilde*, +/-Btilde],
         [+/-Btilde*, I_j-2Btilde*Btilde]].             (14)

They satisfy0<=A_±<=I by the same exact polynomial identity as the received coherent-effect branch. Their parity retains the entire Hermitian cross numerator.

For ANY PSD W and PSD two-block A,

    Tr W A<=2[Tr(W_i A_ii)+Tr(W_j A_jj)].               (15)

Thus the off-diagonal cost of W is paid, not deleted. On the favorable event the actual cost of(14) is at most

    m+2Tr W_j+[96t_ij+pm/8]/(4R0²p_j)
       <=2[m+2Tr W_j+48t_ij/p_j].

Consequently

    max_± n(A_±)/u(A_±)>=s_ij/(256R0² b_ij).            (16)

All matrices are exactly rational in the original known basis because Q is rational unitary. Every accepted output is an actual effect; an adverse random history cannot output an infeasible substitute. Take a public cap ceil[32 log(1/beta)] independent trials, evaluate both actual rational objective ratios and include A=0. With probability at least1-beta,

    returned ratio >= F_Z/[4096R0² K(8ell+56)].         (17)

This is O(ell³ log(2k)) approximation. Its arithmetic is polynomial in the rational input bit length and log(1/beta). If a design uses only relaxation values F_Z>=1, then s>=m/2 and ell=O(log(2ak/m)); no new reciprocal-small-cost factor enters the physical design budget.

## 5. Affine objective and scope of the fixed-decoder transfer

For an affine numerator N(A)=||c+L(A)||², include A=0 and use the homogeneous algorithm on ||L(A)||². At a selected homogeneous candidate, n(A)<=2N(A)+2||c||². Since m+Tr WA>=m, the larger ACTUAL affine ratio at A or0 is at least one quarter of the homogeneous ratio. Conversely any target affine ratio is at most twice the baseline ratio plus twice the optimal homogeneous ratio. Thus the same algorithm yields an affine approximation with at most the additional factor 2+8kappa, where kappa is the homogeneous approximation factor. No favorable sign of c is assumed.

Combined with the exact fixed-effect decoder polar reduction and its odd branch in `ordinary_fixed_effect_decoder_positive_cost_geometry_20261028.md`, this supplies the previously missing canonical even-effect branch. A certified conversion of general rational fixed-slice data through square roots/polar frames still needs its declared rounding ledger before claiming a whole rational decoder oracle. Most importantly, the actual decoder effect A in C=[[A,B],[B*,I-A]] has NOT been optimized by these slice routines. No full-CPTP leverage rate, source saving, or generic strict-ordinary k² theorem is concluded. All known-matrix routines are equally available to the strongest conventional learner.
