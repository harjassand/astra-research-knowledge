# Generic ordinary encoder acquisition by Sylvester transformation and iterated matrix clipping

28 October 2026. Author construction; independent receiving pending. This is a separate proposed improvement, leaving all received GLS files immutable. The parent independently cross-checked the biased recentering calculation and supplied the convenient rational Cholesky scaling used below; those finite-interface contributions are credited, not described as a fresh full-module receipt. A separate fresh reviewer is auditing the proof.

## 1. Contract and result to be received

Retain the physical and comparator assumptions of the received `ordinary_generic_matrix_gls_fast_design_20261028.md` (SHA `a331566da59a07b7d9b679e4516368866fd38df20e44cff4f87f8496332d52ea`) and its fixed-cap companion (SHA `23a7d41b408007eb11c5616129cb2bc5253ba3bd44e92538659d2382cda3072c`): fixed four-real-coordinate isometric encoder, stationary independent resets, ONE paid causal common output frame of dimension k<=8R, d=2k, and actual ordinary loss densities T_x of rank at most r=min(d,3R). Every copy is one ordinary six-state source call plus a receiver-local anti-state register. The local matrix-query import is the received finite MSE theorem, SHA `483a8507c4ca0dfef510c888a2fc755e84b653bcee81a0329830d152b9ed3968`.

For0<gamma,epsilon<=1 the construction below gives the candidate bound

    E ell_selected<=(1+gamma)ell_star+epsilon,
    N=O_tilde(k^4/(gamma epsilon)),
    Q=O_tilde(k^2),                                      (1)

where N counts ALL ordinary source calls, Q counts actual chosen-x homogeneous matrix-query banks including repetitions, and the expectation concerns ONE subsequent completed-loss payload. The comparator is the original unrestricted encoder/full-CPTP recovery optimum. Processing is polynomial, though deliberately large. The generic k^2 source target remains open.

The new step is entirely CLASSICAL postprocessing of received finite matrix responses. It uses a bounded matrix Bernstein inequality AFTER explicit clipping, not an assumed tail bound for a quantum estimator. It retains collective receiver memory, local purification, the causal frame and all controls as paid resources. The equally informed conventional learner can use the identical procedure.

## 2. Block design and a true-target matrix second moment

Fix the same polynomial-size encoder grid X, with M=|X|, containing the ten quadratic anchors and with squared chord radius h_enc^2<=epsilon/256. The true model remains

    vec(T_x)=F_x^T theta, F_x=a(x) tensor I_(d^2),
    D=10d^2, L=8D.

At stage eta=2^-j maintain a KNOWN MATRIX TABLE U_x on X. It need NOT be a quadratic function of x. Range-certify eta I<=U_x<=19I on every grid point. On the good preceding history it also satisfies

    T_x+eta I<=U_x<=3T_x+32eta I.                         (2)

The received block design uses only these known matrix VALUES. Its proof does not require the envelope itself to be quadratic. Define K(U)O=(UO+OU)/2 and

    V=sum_i pi_i F_i K(U_i)^(-1) F_i^T.

Use the same ten-anchor initialization, trace-leverage scan and1/D determinant updates. They stop with

    F_x^T V^(-1)F_x<=L K(U_x),
    S_j<=10+ceil[D log_2((4/eta)/2^-20)]+1.               (3)

All previous finite conditioning bounds remain valid from the range certificate alone. No decoder quadratic maximization occurs.

Set

    n=ceil(2^28 d L/eta), f=ceil(2+r/eta),
    m_i=ceil(n pi_i)+f, m_bar=n+f+1,
    zeta=min{eta/(10^6 D n),m_bar^-2}.                    (4)

ONE batch consists of an independent actual local matrix query at every support i with these parameters, followed by the same GLS linear combination. Its fine floors, centers and every failed record are paid. The local MSE, weighted bias contraction, and m_i>=r/eta imply

    E[(theta_batch-theta)(theta_batch-theta)^T]
         <=101 V^(-1)/n.                                (5)

This is about the TRUE theta and includes bias. Hence each predicted Hermitian matrix Y_x=unvec(F_x^T theta_batch) satisfies

    E[vec(Y_x-T_x)vec(Y_x-T_x)^T]
         <=alpha K(U_x), alpha=101L/n.                  (6)

There is no coordinate-median event at this step. Different x predictions from one batch may be correlated; later confidence uses a finite classical union bound over X. Fresh WHOLE batches are independent conditional on the mathematical common frame, the stage design, and all earlier records.

## 3. A known rational Sylvester transform removes the extra matrix-coordinate factor

For each known U=U_x construct a rational complex matrix L_ch with

    ||L_ch L_ch* - U||op<=eta/10,
    B=(11/10)L_ch, Ubar=B B*.

Because U>=eta I,

    U<=Ubar<=2U, ||B||<=sqrt(38).                         (7)

Indeed L_ch L_ch* lies between0.9U and1.1U, and multiplying by1.21 gives factors1.089 and1.331. This is a known, strictly conditioned Cholesky calculation, not an unknown source operation. Rational rounding can be made to satisfy the displayed backward-error bound with polynomial bits in d, input bit length and log(1/eta); the inequalities can be verified directly. Cholesky pivots are bounded away from zero by the supplied eta scale. A predetermined sufficiently fine rational arithmetic budget, or certified refinement within that budget, provides the factor; no favorable spectral event is assumed.

Define the invertible known Sylvester map

    S_Ubar(H)=Ubar H+H Ubar,
    Z(Y)=B* S_Ubar^(-1)(Y), Z_*=Z(T).

All coefficients are known rational/fixed-field data and the solve is a finite linear system with smallest singular value at least2eta. Crucially,

    T=B Z_*+Z_*^* B*.                                   (8)

Thus operational reconstruction is EXACT for this rational factor, rather than an approximate use of an irrational square root.

The following second-moment lemma is the key improvement:

    E DeltaZ DeltaZ*<=sigma^2 I,
    E DeltaZ* DeltaZ<=sigma^2 I,
    sigma^2=alpha d/2, DeltaZ=Z(Y)-Z_*.                  (9)

Proof. By(7),(6), the real-Hermitian second moment is at most alpha K(Ubar). Domination of quadratic forms permits comparison with the zero-mean Gaussian having exactly this covariance; this is only a proof device. In an eigenbasis Ubar=diag(lambda_i), first use B=sqrt(Ubar). Then

    DeltaZ_ij=sqrt(lambda_i) E_ij/(lambda_i+lambda_j),
    E_ref |DeltaZ_ij|^2
       =alpha lambda_i/[2(lambda_i+lambda_j)].

The reference row and column second-moment matrices are diagonal, each bounded by alpha d I/2. The same bounds hold for a dominated real covariance because squared norms of all row/column linear combinations are positive real quadratic forms. A general B with BB*=Ubar differs from sqrt(Ubar) by a right unitary; this merely rotates one of the two matrix moments. This proves(9), including nonzero biases and correlated matrix entries. It is NOT a Gaussian assumption on the actual query output.

On the good stage history T<=Ubar. The positive integral representation of S_Ubar^-1 gives

    0<=S_Ubar^-1(T)<=S_Ubar^-1(Ubar)=I/2,
    ||Z_*||<=sqrt(38)/2<4.                              (10)

No inverse of T or source spectrum occurs. Let H(Z)=[[0,Z],[Z*,0]] denote Hermitian dilation. Equation(9) is exactly

    E H(DeltaZ)^2<=sigma^2 I_(2d),
    ||E H(DeltaZ)||<=sigma.                              (11)

The second statement follows from matrix square convexity, so a possibly biased batch is covered explicitly.

## 4. A finite clipping lemma, with fresh biased observations

Suppose independent Hermitian matrices X_l satisfy E X_l^2<=vI. Let clip_t act spectrally by clipping real eigenvalues to[-t,t]. Functional calculus gives

    -X_l^2/t<=clip_t(X_l)-X_l<=X_l^2/t,
    clip_t(X_l)^2<=X_l^2.

Therefore its bias relative to E X_l has norm at most v/t; its centered matrix variance is at most vI and its centered range is at most2t. Bounded matrix Bernstein, applied to both signs of the centered sum in dimension2d, yields except probability4d exp(-h),

    ||(1/b)sum_l clip_t(X_l)-(1/b)sum_l E X_l||
       <=v/t+sqrt(2vh/b)+4th/(3b).

For t in[sqrt(vb/h),2sqrt(vb/h)], the right side is below

    8 sqrt(vh/b).                                       (12)

The constant8 is deliberately conservative for the entire factor-two threshold interval; no endpoint cancellation is needed. The only imported tail inequality here is Tropp's established bounded matrix Bernstein theorem, Theorem6.1(ii), applied to the bounded clipped matrices: https://tropp.caltech.edu/papers/Tro11-User-Friendly-preprint.pdf . There is no unsupported tail premise for the original local quantum estimator.

Now let a current known dilation center M_t obey ||M_t-H(Z_*)||<=delta_t. Fresh transformed GLS batches give residuals

    X_l=H(Z_l)-M_t,
    E X_l^2<=2(sigma^2+delta_t^2)I.                      (13)

This uses(A+B)^2<=2A^2+2B^2, without commuting matrices. Its mean differs from H(Z_*)-M_t by at most sigma, by(11). Taking v=2(sigma_bar^2+delta_t^2), sigma_bar>=sigma, and b>=2^16 h, (12) gives an ideal next-center error at most

    sigma_bar+8sqrt(v/2^16)
       <delta_t/16+17sigma_bar/16.                      (14)

Allowing at most sigma_bar/4 further operator error for ALL finite clipping/addition/center rounding at that iteration still fits the conservative recursion

    delta_(t+1)=delta_t/4+2sigma_bar.                    (15)

Neither unbiasedness nor identical individual biases are assumed. Fresh banks are essential because the current center depends on previous records.

## 5. The actual finite inner loop on every grid point

For eta_j=2^-j choose the dyadic upper bound and round count

    sigma_bar,j=2^(-11-floor(j/2)),
    t_j=ceil[(13+floor(j/2))/2].                          (16)

The n in(4) ensures sigma<=sigma_bar,j<=sqrt(2eta_j)/2048. Start M_0,x=0 and delta_0=4. After t_j iterations of(15),

    delta_(t_j)<=4 sigma_bar,j.                          (17)

Let J be the least integer with eta_J<=gamma epsilon/(2^15 k), beta=epsilon/32, t_max=t_J, and

    h=ceil log_2(8d M J t_max/beta), b=2^16 h.             (18)

All these parameters are fixed before records. For each inner iteration acquire b NEW GLS batches and process their predicted matrices at EVERY x in the classical grid. They are the SAME b batch data, not b new physical banks per grid point. The correlations across x are irrelevant to a union bound. Before each iteration choose a dyadic threshold t in[sqrt(vb/h),2sqrt(vb/h)]; since b/h=2^16 and v is known rational, this choice uses integer comparisons of powers of two.

For each x perform the clipped-residual mean update M_new=M_old+(1/b)sum clip_t(H(Z_l)-M_old). These matrices remain off-diagonal Hermitian dilations: the residual anticommutes with diag(I,-I), and odd spectral clipping preserves that symmetry. Extract the new Z center and keep it in an exactly Hermitian/off-diagonal rational representation.

A completely finite clipping implementation is available without an eigengap. The clipped matrix is the unique Frobenius projection of its known input onto the convex set -tI<=Y<=tI within the off-diagonal Hermitian subspace. This is a strongly convex quadratic SDP with the explicit relative-interior point0. A feasible output with objective gap at most e^2/2 has Frobenius error at most e. Compute each projection with e<=sigma_bar/8; its AVERAGE error is then at most sigma_bar/8, not b times that amount. Center addition/rounding receives another sigma_bar/8. This proves the numerical budget used in(15). Exact feasible rational repair and finite certified optimization are paid known-matrix operations, not a free quantum oracle.

All input matrices have deterministic polynomial bounds: the local receiver has its all-history finite output cap, V has the received inverse bound, the Sylvester inverse is at most1/(2eta), and centers move by at most the predetermined clipping thresholds plus rounding budgets. Hence the SDP accuracies, all arithmetic and memory have polynomial bit complexity even on failed statistical histories. The clip need not be computed by diagonalizing a near-degenerate empirical eigenbasis.

A conditional first-failure union bound over x, stage and inner iteration, using(18), makes all recentering events simultaneous except probability at most beta. At a successful stage, reconstruct the final Hermitian predictor

    T_tilde,x=B_x Zhat_x+Zhat_x* B_x*.

By(7),(17), every unit vector v obeys

    |v*(T_tilde,x-T_x)v|
       <=8sigma_bar sqrt(v*Ubar_x v)
       <=(1/128)sqrt(eta v*U_x v).                      (19)

Round EACH grid matrix directly on real/imaginary entry mesh at most eta/(2^12 d), with conjugate symmetry. This costs operator error below eta/128. Since U_x>=eta I, the rounded T_hat,x obeys the received conservative event

    |v*(T_hat,x-T_x)v|<=(1/16)sqrt(eta v*U_x v).          (20)

The predictor is not asserted PSD, and need not be quadratic in x.

## 6. Global induction, decision and scope of the representation change

Start U_0,x=2I. At the end of stage j propose U_j,x=2T_hat_j,x+2eta_j I, as a TABLE on X. Certify every eigenvalue lies in[eta_j,19], with enclosure precision eta_j/16; otherwise abort and use the fixed replacement decoder. The same scalar inequality as in the received source, applied to(20), gives

    T_x+(5/4)eta_j I<=U_j,x<=3T_x+(11/4)eta_j I

on good histories. Thus range checks pass with slack and the next stage satisfies(2). Bad accepted histories still have the range certificates required for finite design and bank caps. Conditional first-failure accounting covers all stages and inner loops.

The ONLY model required to remain quadratic is the true T_x, for GLS feature prediction. A gridwise nonlinear confidence predictor does not invalidate the feature covariance or the block design. The fixed four-dimensional encoder selector makes exhaustive CLASSICAL grid processing polynomial. No unknown-source query is assigned to each grid point.

At the final stage use the original trace-k decision consequence of(20), tau=k eta: every positive full-CPTP decoder satisfies

    |qhat-q|<=(1/16)sqrt(3tau q+32tau^2).

Search the same interior decoder body C>=sI/2, Tr_out C=I_k, s in[epsilon/512,epsilon/256], with affine objective gap at most tau for every grid x. The received clipped-root/Young argument and the true fixed-decoder stationary quadratic comparator prove, on the good ideal-frame branch,

    ell_selected<=(1+gamma/4)ell_star+epsilon/16.

The same beta<=epsilon/32 and separate whole-process final Bell-loss debit epsilon/4 give(1). All finite frame, preparation, purification, receiver and final decoder controls are retained. The one-use payload and completed-loss/full-CPTP comparison are unchanged. The newer direct-decoder corollary is NOT imported for this nonlinear robust predictor; the older trace-k argument suffices.

## 7. A predetermined raw-source and invocation cap

Use the same exact local-bank ledger as the received fixed-cap companion, but replace its n_j and batch multiplier. For each stage define n,f,m_bar,zeta by(4), the support cap S_j by(3), D_p=d r, D_plus=2^ceil(log_2 D_p), and

    L_zeta=2+ceil(log_2(1/zeta)), l_bar=m_bar+L_zeta,
    beta_bar=zeta/[1000 l_bar^2 D_p^2 m_bar^2],
    n0_bar=ceil[320 D_plus log_2(12D_plus/beta_bar)]+1.

Outward integer logarithm bounds are permitted. Every realized local query uses at most n0_bar+2m_i+L_zeta calls, m_i<=m_bar and sum_i m_i<=n+S_j(f+1). Therefore predeclare

    N_j_bar=b t_j [2n_j+S_j{2(f_j+1)+n0_bar,j+L_zeta,j}],
    N_bar=sum_j N_j_bar, H=N_bar+1,
    Q_bar=b sum_j t_j S_j.                              (21)

Every support ceiling, repeated center, local m/l bank, bias restriction, failure and inner-loop batch is included. Pad unused frame slots with dummy ordinary calls when needed; no expected-stopping or successful-record refund is taken. The frame horizon is fixed BEFORE any acquired design.

Here n_j=O(dL/eta_j)=O(d^3/eta_j). The support-floor contribution S_j r/eta_j is NOW OF THE SAME ORDER O_tilde(d^3/eta_j), not lower and not omitted. Coarse centers contribute O_tilde(S_j d r)=O_tilde(d^4) per logarithmic stage/inner schedule. Since eta_final is Theta(gamma epsilon/k), summing the geometric fine costs and all logarithmic factors gives

    N_bar=O_tilde(k^4/(gamma epsilon)), Q_bar=O_tilde(k^2).

The classical processing scans M grid points and solves polynomial-size known convex problems. Its potentially large polynomial dependence on inverse accuracy is not a physical source-grid multiplier. The causal frame compiler's gates/workspace remain polynomial in H,k,log ambient dimension and precision; local purification memory/control is additional and paid.

## 8. What is and is not new in this composition

The local efficient matrix query and causal frame are imports. Bounded matrix Bernstein, spectral clipping and finite convex optimization are established ingredients. In particular, iterative centered robust matrix means are established background: Minsker, *Sub-Gaussian estimators of the mean of a random matrix with heavy-tailed entries*, section6.2 and equations(6.1)-(6.2), https://arxiv.org/pdf/1605.07129 . Its Theorem6.2 includes an additional dimension-dependent uniform-centering condition; that theorem and its rate are NOT imported here. Fresh independent banks allow the elementary conditional clipping proof in section4 instead. The present proposed gain is the explicit known Sylvester transformation of the Jordan-covariance GLS error, the biased fresh-bank recentering composition, and its gridwise encoder decision/source accounting.

No PSD Choi completion, free conditional support projector, unknown-source inverse, universal sup-average Bures estimate, row-cone radius sum, or unbiasedness after clipping is assumed. This is an ordinary-input procedure with a collective quantum receiver; it is not a classical count-only theorem. It does not claim a separation from an equally informed conventional learner or practical hardware performance. All received earlier sources remain valid and immutable while this separate construction awaits independent receiving.
