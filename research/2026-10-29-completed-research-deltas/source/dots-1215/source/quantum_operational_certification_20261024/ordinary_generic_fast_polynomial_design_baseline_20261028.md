# Generic ordinary relative learning with polynomial design: a k^6 baseline

28 October 2026. New author construction; independent receiving pending. This is a generic strict-ordinary-input fast-accuracy baseline, not the desired rank-squared dimension rate. Its purpose is to remove an exponential decoder menu while retaining inverse-accuracy source scaling. It compares with the strongest equally informed conventional learner, which can use this same construction.

## 1. Contract and claimed scale

Throughout0<gamma,epsilon<=1. Use the supplied four-real-coordinate linear isometric encoder V_x, x in S3; a stationary/reset source with encoded Choi rank at most R; and ONE actually paid finite-horizon common receiver frame of dimension k<=8R. Full CPTP decoders are allowed. For a decoder Choi matrix C in k-input/two-output order, write

    C>=0, Tr_out C=I_k, C_0=I_(2k)/2.

One ordinary six-state preparation/source/decoder/projector-test trial produces a bit with mean

    q(x,C)=(2/3)ell(x,C),   0<=q<=1.                       (1)

The actual completed Bell loss is ell. The input carries no retained sender reference or coherent encoder selector. Collective receiving is not needed for the bit estimator, but the retained-frame compiler and arbitrary full decoder controls remain substantive resources.

The construction below has deterministic source cap

    N=O_tilde(k^6/(gamma epsilon))                        (2)

and polynomial learner/design processing in k,1/gamma,1/epsilon and the paid precision, giving for ONE subsequent payload

    E ell_selected <=(1+gamma)ell_star+epsilon.            (3)

The original unrestricted encoder/full-CPTP optimum is ell_star. No zero-optimum, spectral floor, flag, useful warm seed, sparse source model or physical Choi completion is assumed. The governing frame import is the later RECEIVED `explicit_online_random_dimension_reduction_compiler_20261027.md` and its independent receipt, NOT merely the older causal existence/dense-synthesis note. It supplies an arbitrary-operator common-frame law with gatesproducer-workspace/workspace polynomial in the full horizon H,k,log(d_phys),log(1/nu), where d_phys is the ambient physical output dimension and nu the whole-process precision. These H-dependent controls/memory, known decoder synthesis and supplied source controls must all be paid over the entire experiment. The high polynomial processing and dimension exponent are not practical-performance claims.

The live generic target remains k^2/(gamma epsilon) with useful processing. The existing k^4/(gamma epsilon) information-theoretic baseline may use an exponential decoder menu; the existing k^2/epsilon^2 route has polynomial processing. Equation(2), if received, is a different tradeoff: fast accuracy AND polynomial processing, at a worse dimension exponent.

## 2. A polynomial-dimensional linear action model with an SDP action oracle

Let 0<s<=1/64 and restrict the search to the safely interior decoder body

    K_s={C: C>=(s/2)I, Tr_out C=I_k}.                     (4)

For any full decoder D, (1-s)D+s C_0 belongs to K_s and increases Bell loss by at most s. The comparator restriction is paid, not silently imposed.

Choose the standard rational Hermitian k-by-k basis consisting of E_ii, E_ij+E_ji and i(E_ij-E_ji); tensor with each of the three logical Pauli matrices to obtain F_j, j=1,...,3k^2. They are orthogonal, traceless on the logical output, and ||F_j||<=1. Every feasible decoder has unique real coordinates

    C=C_0+sum_j t_j(C)F_j.

Let d_C=3k^2+1 and b(C)=(1,t_1,...,t_(d_C-1)). The physical decoders C_0 and C_0+F_j/4 lie in K_s and span this affine coordinate system. Their coefficients are rational and their least positive eigenvalue is at least1/4.

Use the ten real quadratic features a_2(x)=(x_i^2,2x_i x_j). On a fixed rational quadratic encoder net X, the action feature

    a(x,C)=a_2(x) tensor b(C) in R^D,
    D=10d_C<=40k^2,                                      (5)

is known. The true q=a^T theta is linear in an UNKNOWN real coefficient vector theta. Coefficients need not be positive or form a positive completion: only the actual physical action means are nonnegative. For fixed x the feature is affine in C, so optimizing any fixed linear functional of a over K_s is a standard decoder SDP with strict feasible center C_0. The number of x values is polynomial because the selector dimension is fixed.

The four e_i and six(e_i+e_j)/sqrt2 have rational quadratic features and span R^10. Tensor them with the d_C decoder anchors above. Their D actions give an explicitly conditioned initial covariance. For example the unweighted uniform decoder-anchor covariance has minimum eigenvalue at least1/(33d_C^2); the fixed encoder covariance has minimum eigenvalue at least1/4000. Thus, whenever a known action weight u lies in[tau,19], the initial weighted design covariance has

    V_0=(1/D)sum_anchor aa^T/u >= lambda_* I,
    lambda_*=2^-22 D^-2                                 (6)

as a conservative rational bound. The fixed numerical constant can also be checked directly from the rational10-by10 encoder evaluation matrix. A known bound ||a||<=B=4kD is more than sufficient. All bit-length and conditioning bounds below use these explicit polynomial bounds, not favorable unknown source eigenvalues.

## 3. Polynomial approximate weighted design, without a decoder net

At a stage, u(x,C) is a KNOWN affine function of C for each x in X, certified to lie in[tau,19] on the whole body K_s. Construct a finitely supported distribution pi and covariance

    V=sum_i pi_i a_i a_i^T/u_i.

The objective is a uniform leverage bound a^T V^-1 a/u. We accept a dimension-factor approximation, which accounts for the k^6 rather than k^4 source rate.

Compute the exact rational LDL factorization V=L diag(d_i)L^T, with L unit lower triangular. For r_i^T the rows of L^-1,

    a^T V^-1 a/u =sum_(i=1)^D (r_i^T a)^2/(d_i u).        (7)

For each coordinate, x, and scalar z,

    (r_i^T a)^2/(d_i u)
      =sup_(z in R)[2z r_i^T a-z^2 d_i u].                (8)

For FIXED x,z, the bracket is affine in C. A decoder SDP therefore maximizes it. A known bounded rational z grid and finite feasible SDP optimization compute the coordinate supremum to additive error at most2, returning an actual feasible decoder and an achieved LOWER value. This is not an exact-real quadratic optimization oracle.

For clarity, the grid has a polynomial finite cap. During the design, V<=Lambda I with Lambda=B^2/tau. The determinant argument below bounds the number of updates by

    T_max=ceil[D log_2(B^2/(tau lambda_*))]+1.

Since each update retains a fraction1-1/D of the preceding design, V>=lambda_low I throughout, where the rational bound

    lambda_low=lambda_* [tau lambda_*/B^2]^4 /4

is conservative. In particular d_i lie between lambda_low and Lambda, and |r_i^T a| is bounded by a known polynomial M, for example B(1+Lambda/lambda_low). An optimizer z has |z|<=M/(lambda_low tau). Cover this interval by a rational grid of mesh at most1/(1+19Lambda), including zero. Rounding z loses at most1 in(8), since the exact loss is d_i u (z-z_opt)^2. Standard finite decoder SDP optimization to error at most1, keeping a feasible C, adds at most another1. Grid size and coefficient bits are polynomial in the paid dimensions and inverse tolerances. There is no exponential decoder action list.

Let A_low be the largest achieved coordinate value over this grid, all x and all i. If A_low<8D, every coordinate supremum is below8D+2, so STOP with

    sup_(x,C) a^T V^-1 a/u <=10D^2=:L_* .                (9)

Otherwise the returned physical action has leverage at least8D. Update

    V_new=(1-1/D)V+(1/D) aa^T/u

and retain the corresponding finite design distribution. The determinant lemma gives

    det(V_new)/det V
      =(1-1/D)^D [1+leverage/(D-1)]>2,

using D>=2 and(1-1/D)^D>=1/4. On the other hand det V<=(B^2/tau)^D and det V_0>=lambda_*^D. Therefore at most T_max updates occur. This also proves the lower eigenvalue bound used to fix the oracle's finite grid before iteration. The support has size at most D+T_max; no exponential support or unproved constant support is assumed.

Rational updates have fixed mixing factor1/D. Recompute covariances from the finite action list and weights. Round newly optimized decoder matrices inward at a prescribed inverse-polynomial mesh, using the positive center/margin in(4), so their coefficients have uniformly polynomial bit length and the objective debit remains within the stated1. This prevents recursive exact-arithmetic bit growth. The existence and explicit inner radius of K_s supply the finite SDP contract; no condition number of the unknown source is used.

## 4. Simultaneous all-action regression from paid bit samples

For the stage's fixed design, use b independent batches. In EACH batch take

    n_i=ceil(n pi_i)

ordinary bit trials at support action i, including every source/decoder invocation. Let y_i be its empirical frequency and form

    theta_batch=V^-1 sum_i pi_i a_i y_i/u_i.              (10)

Pointwise conditional on ONE common mathematical frame U and the prior records, when q_i<=u_i the estimator is unbiased and

    Cov(theta_batch)<=V^-1/n.                            (11)

Indeed q_i(1-q_i)/n_i<=u_i/(n pi_i). The source is iid in that common-U description; conditioning only on physical records would leave a mixture and is not substituted for this law. Prove the whole branch guarantee conditional on U, then average U and the records. No unknown source inverse or hypothetical matrix observation enters(10).

Whiten only the KNOWN coordinates: phi_batch=L^T theta_batch. Its ith variance is at most1/(n d_i). For each i take the median across the b batches, then undo L^T, producing theta_med. Chebyshev gives probability at most1/16 of a coordinate error exceeding4/sqrt(n d_i) in one batch. Taking odd

    b>=8 log(2DJ/beta)

and a union bound over D coordinates and at most J stages gives, on the simultaneous event,

    ||V^(1/2)(theta_med-theta)||<=4sqrt(D/n).

The square root here denotes the quadratic norm; no numerically constructed matrix square root is required by the estimator. Correlations between coordinates do not invalidate the coordinatewise median union bound.

Choose n=ceil[2^14 D L_*/tau]. Then (9) gives a uniform prediction error at most(1/32)sqrt(tau u) for EVERY x in X and EVERY decoder in K_s. Round theta_med on a rational coordinate grid so the uniform extra prediction error is at most tau/64. Using ||a||_1<=DB, a mesh tau/(64DB) with an extra factor two if needed suffices. Since u>=tau, the rounded vector thetahat satisfies

    |qhat(x,C)-q(x,C)|<= (1/16)sqrt(tau u(x,C)),           (12)

uniformly over the continuous decoder set. This is a finite-dimensional quadratic-norm event, not a union bound over an exponential decoder net.

Each batch uses at most n+D+T_max calls. Coordinate medians, rational feature arithmetic and rounding have fixed polynomial caps. The envelope coefficients are rounded at EVERY stage, preventing hidden super-polynomial bit length. Arbitrarily bad histories still have the same source and arithmetic caps.

## 5. Affine envelopes retain both fast statistics and an SDP oracle

Set tau_j=2^-j, tau_0=1, u_0=1. At stage j use the previous envelope u_(j-1) in the design/regression, at target tau=tau_j. After obtaining the ROUNDED affine predictor qhat_j, propose

    u_j(x,C)=2 qhat_j(x,C)+2 tau_j.                       (13)

Do NOT clip this into a nonlinear action function. Instead perform global finite SDP range checks for every x in X. Accept only if the range is certified inside[tau_j,19]; otherwise abort to the fixed CPTP replacement policy. The SDP objective tolerance tau_j/16 leaves ample slack on good histories. No source observations are spent scanning this classical list.

Here is the induction. Suppose q<=u_(j-1)<=3q+16tau_(j-1), and u_(j-1)>=tau_(j-1). Since tau_(j-1)=2tau_j, (12) and 2sqrt(ab)<=a+b imply

    q+tau_j <=u_j<=3q+16tau_j.                            (14)

Explicitly, with c=1/16, bound 2c sqrt[tau(3q+32tau)] by q+(3c^2+2c sqrt32)tau. The coefficient3c^2+2c sqrt32 is below3/4. Thus the lower proposal is at least q+(5/4)tau, while the upper is at most3q+(11/4)tau. Its whole range is strictly inside[tau,19], with enough margin for the finite range checks. The base u_0 obeys the invariant. Hence aborts on good histories cannot occur, and a conditional first-failure union bound pays all bad pilot histories by beta. On bad histories an accepted u is still known positive and bounded, so the finite design cap remains valid even if the statistical promise q<=u has failed.

The useful point of(13) is that u remains AFFINE in C, enabling(8). Earlier square-root-envelope formulas need not be maximized over a decoder menu. The price is only constant factors in the statistical invariant, not an extra accuracy exponent.

## 6. Selection, comparator discretization and constants

At the final scale tau, (12) with the preceding invariant yields

    |qhat-q|<=c sqrt(3tau q+32tau^2).

For every action this implies

    |sqrt(max(0,qhat))-sqrt(q)|<=2sqrt(tau).              (15)

For q>=tau divide the probability error by sqrt q; for q<tau both nonnegative roots are at most sqrt[(1+c sqrt35)tau]. Minimize the FINAL AFFINE qhat over all x in X and C in K_s to feasible objective gap at most tau using ordinary decoder SDPs. Clipping for the proof of(15) is monotone and is NOT used in the envelope/design. The actual selected feasible action obeys

    sqrt(q_selected)<=sqrt(min_(X,K_s)q)+5sqrt(tau),
    q_selected<=(1+gamma/4)min_(X,K_s)q+125tau/gamma.     (16)

Use a rational encoder net with squared chord radius h^2<=epsilon/256, containing the ten spanning anchors, and s<=epsilon/256. At the original optimal policy(x*,C*), fixed-decoder loss is a bounded nonnegative quadratic and x* is its minimum eigenvector. Mixing C* with C_0 changes q by at most s and leaves a bounded quadratic. Thus

    min_(X,K_s)q <=(2/3)ell_star+s+h^2.                   (17)

This is a comparator stationarity argument, not differentiability of a nonsmooth optimized risk. Choose the final dyadic tau within a factor two below gamma epsilon/2^15. Multiplying(16) by3/2 yields

    ell_selected <=(1+gamma/4)ell_star+epsilon/16

with conservative slack. The selected C is already an explicit physical full decoder; no fresh unknown-decoder oracle is needed.

Take beta<=epsilon/32. On bad/aborted records the final CPTP replacement has loss at most one. Allocate a separate final Bell-loss debit at most epsilon/4 to the WHOLE interactive frame, preparation, reset, adaptive bit experiments, finite decoder controls and the one payload. This proves(3), with room to spare. A common-frame identity must hold for arbitrary operators linked into this adaptive process; a batch-only support reduction or classical identification of a hidden frame is insufficient.

Since sum_j 1/tau_j<=2/tau and L_*=10D^2, the complete capped bit-pilot bill is

    N<=b sum_(j=1)^J [ceil(2^14 D L_*/tau_j)+D+T_max,j]
      =O_tilde(D^3/(gamma epsilon))
      =O_tilde(k^6/(gamma epsilon)).                     (18)

The initial design is a classical construction, not an uncounted tomography bank. Every support action's ceiling and all batches/stages are included. Let H=N+1, padding with dummy ordinary calls when required by a fixed-horizon frame contract. Retain the SAME causal frame through all design-selected decoder trials and the payload. The physical source calls, growing memory, known arbitrary full-decoder synthesis, local ancillas, random choices and finite arithmetic are paid. There is no hidden k-dimensional Haar measurement or efficient-Keyl assumption.

## 7. Scope and novelty discipline

The new proposed ingredient is a deliberately loose polynomial weighted-design implementation for the continuous full-decoder action set, combined with an affine root-sensitive envelope and simultaneous coordinate-median regression. It uses familiar determinant design, scalar fractional-quadratic variational identities, decoder SDPs and positive-loss sampling; no priority claim is made for those components. The earlier positive-design and finite decoder/frame machinery remain credited imports.

No PSD output-state estimate or positive Choi completion is inferred from the unconstrained coefficient estimate. No global ordinary-versus-coherent separation or practical speedup is claimed. The construction improves the GENERIC accuracy/processing tradeoff, not the target rank-squared source rate. It is compatible with the received fixed-rank nonadaptive lower bound because the actual encoder/policy settings depend on earlier outcomes through u_j. All statistical guarantees are averaged across records and confined to the stated source/control/reset assumptions. Independent receiving and finite tests are pending.
