# Generic ordinary active encoder acquisition by block matrix GLS: a k^5 candidate

28 October 2026. New author construction; independent receiving and diagnostics are pending. This is a proposed improvement of the received generic k^6 polynomial-design baseline, not a claim of the target k^2 rate. The equally informed conventional learner can use the identical ordinary-input, collective-receiver procedure.

## 1. Physical contract and scope

Assume 0<gamma,epsilon<=1, the supplied four-real-coordinate linear isometric encoder V_x for x in S^3, stationary independent source resets, encoded Choi rank at most R, and ONE actually paid finite-horizon common output frame of dimension k<=8R. Put d=2k and use the actual ordinary six-state loss-state preparation T_x on a known d-dimensional receiver register. Each preparation uses one ordinary source call and a receiver-local anti-state register, not a retained sender reference or coherent encoder selector. The matrices obey

    T_x>=0, Tr T_x=1, rank T_x<=r:=min(d,3R),
    T_x=sum_(j=1)^10 a_j(x) Theta_j,
    a(x)=(x_i^2,2x_i x_j).

For the full CPTP decoder body K={C>=0: Tr_out C=I_k}, use the transposed Choi convention so that

    q(x,C)=Tr(T_x C)=(2/3)ell(x,C),
    Tr C=k, 0<=C<=2I_d.                                  (1)

The target is expected ONE-payload completed Bell loss <=(1+gamma)ell_star+epsilon, against the ORIGINAL unrestricted encoder/full-CPTP receiver optimum. There is no zero-optimum, known flag, eigenvalue floor, useful seed, positive Choi completion, or uncounted decoder acquisition premise.

The candidate deterministic source cap is O_tilde(k^5/(gamma epsilon)), with polynomial design/processing and the complete paid frame/receiver controls. The key new step is a block experimental design over encoder settings ONLY; it does not optimize a positive quadratic over the decoder cone.

Governing imports, already received separately, are: `ordinary_adaptive_pure_matrix_query_20261028.md` (SHA 483a8507c4ca0dfef510c888a2fc755e84b653bcee81a0329830d152b9ed3968) and its receipt; `explicit_online_random_dimension_reduction_compiler_20261027.md` and its PASS receipt; the finite ordinary loss-state construction; and the finite feasible decoder-SDP/net machinery in `ordinary_generic_fast_polynomial_design_baseline_20261028.md` (SHA 74e7ff7ee4a02b2b7096602cecc7eec6583aa34e318cebfe66d558b396bb0f84). Their resource contracts are retained below, not replaced by a free matrix observation or an older existence-only frame theorem.

## 2. Exactly what the local matrix query supplies

For a chosen x, integer m>=2 and finite bias target 0<zeta<=m^(-2), the imported receiver returns an actual finite Hermitian matrix Y, generally indefinite, satisfying

    ||E Y-T_x||_1<=zeta,
    E[Tr(O(Y-T_x))^2]
      <=100[Tr(T_x O^2)/m+r Tr(O^2)/m^2]                 (2)

for EVERY Hermitian O. Its raw source cost is

    N_query=O(d r log(d r (m+log(1/zeta))/zeta)
                +m+log(1/zeta)).                         (3)

All coarse-center, fine random-basis, binary reciprocal, purification, failure and finite-control costs are included. In particular the d*r coarse bank is paid for EACH actual invocation. The source input remains ordinary; the receiver uses collective quantum memory and the paid efficient random-purification channel. This is not a count-only or separable-receiver theorem.

A bank is homogeneous at its selected x. Its ONE latent purification is retained through the coarse and fine parts, and is averaged only after the imported whole-query bound. Different support settings/batches need not have aligned purifications: each returned matrix is reduced to the SAME known output frame and targets T_x. All subsequent conditional independence statements are pointwise conditional on the common mathematical output frame U and all prior stage records, not on physical records alone. Independent fresh source banks and receiver resets then give independent query outputs. The target T_x is the same for every latent local purification.

## 3. Positive matrix envelopes and real Hilbert-space notation

Fix one polynomial-size quadratic encoder net X, containing the four e_i and six (e_i+e_j)/sqrt(2) anchors. Its quadratic features are rational; the selected physical encoders have paid finite synthesis. The net has squared chord radius h^2<=epsilon/256. It is used only for known classical searches; source calls are made at the acquired design support, not at every grid point.

On Hermitian d-by-d matrices use the real Hilbert-Schmidt inner product. Let p=d^2 and choose the standard orthonormal Hermitian basis. It has entries in the fixed algebraic field Q(i,sqrt(2)); exact field arithmetic or certified rational enclosures cost polynomial bit complexity. Let vec denote its real coefficient vector. Define

    K(U): O -> (UO+OU)/2,
    <O,K(U)O>=Tr(U O^2).

If eta I<=U<=19I, then eta I_p<=K(U)<=19I_p. Write theta for the ten stacked unknown vec(Theta_j), D=10p, and

    F_x=a(x) tensor I_p : R^p -> R^D,
    vec(T_x)=F_x^T theta.                                (4)

At a stage with target eta, the previous known envelope U_x is a quadratic matrix function on X. It is certified, on EVERY x in the fixed grid, to lie in [eta I,19I]. On good histories it additionally obeys

    T_x+eta I<=U_x<=3T_x+32eta I.                         (5)

The factor32 uses the previous dyadic scale. The design algorithm uses only the certified range, so it still has a finite cap on bad histories.

## 4. Block log-det design: no decoder quadratic oracle

For a distribution pi on X form

    B_x=F_x K(U_x)^(-1) F_x^T,
    V=sum_x pi_x B_x.

The ten anchors give a positive initial covariance V_0. The fixed encoder anchor covariance is >=I_10/4000, and K(U_x)^(-1)>=I_p/19. Thus the conservative source-independent bound

    V_0>=lambda_* I_D, lambda_*=2^(-20)

holds. Also ||a(x)||^2<=2, so V<=Lambda I_D with Lambda=4/eta. Define the known scalar block leverage

    L_x=Tr(V^(-1) B_x).                                  (6)

Compute it for each x by finite matrix inversion/arithmetic. There is no maximization over C and no nonlinear decoder net. If all L_x<=8D, stop. Otherwise choose a violating x and update

    V_new=(1-1/D)V+(1/D)B_x.

For M=V^(-1/2) B_x V^(-1/2)>=0, det(I+tM)>=1+t Tr M. Consequently a violating update satisfies

    det(V_new)/det V
      >=(1-1/D)^D [1+L_x/(D-1)]>2.

Since det V<=Lambda^D and det V_0>=lambda_*^D, at most

    T_max=ceil[D log_2(Lambda/lambda_*)]+1                 (7)

updates occur. The support size is at most S_max=10+T_max. Retaining the initial weight through this capped number of updates gives the conservative bound

    V>=lambda_low I,
    lambda_low=lambda_* (eta lambda_*/4)^4/4.             (8)

This follows inductively, exactly as the received determinant construction; it is not a post hoc unknown condition number. Recompute V from the finite list and rational weights, rather than recursively rounding inverses. The update probabilities have polynomial bit length. Since all previous envelope coefficients are rounded at the end of each stage, all inversions, leverage comparisons and determinants have polynomial finite arithmetic cost. Fixed-field comparisons may be exact; alternatively use disjoint certified threshold margins and enlarge8D by an absolute constant.

At termination, positivity and (6) imply the OPERATOR inequality

    F_x^T V^(-1) F_x <= L K(U_x), L=8D, all x in X.       (9)

Indeed the conjugated left side is PSD and has trace L_x<=L. This is the benefit of a block query: one setting supplies all p matrix coordinates, and the trace leverage is O(D), rather than the O(D^2) leverage of the received scalar coordinate-search baseline.

## 5. Paid stratified matrix GLS, including bias

For each support x_i and in EACH of b independent batches, invoke the actual query (2) with

    m_i=ceil(n pi_i)+ceil(2+r/eta),
    n=ceil(2^24 D L/eta),
    m_bar=n+ceil(2+r/eta)+1,
    zeta=min{eta/(10^6 D n),m_bar^(-2)}.                                (10)

In particular m_i>=r/eta and m_i<=m_bar, so the local import's internal requirement zeta<=m_i^(-2) is respected. Tightening zeta costs only logarithmic additional work. On the good stage history (5), (2) implies the real covariance bound

    Cov(vec Y_i)<=100 K(U_i)/m_i.                        (11)

This uses Tr(T_i O^2)+r Tr(O^2)/m_i<=Tr(U_i O^2), not an assumed true-state inverse oracle. Every per-support floor in (10) is paid, including a rare or vanishing source sector.

Form the batch GLS estimate

    theta_batch=V^(-1) sum_i pi_i F_i K(U_i)^(-1) vec Y_i. (12)

Its covariance is <=100 V^(-1)/n. It is NOT exactly unbiased. If b_i=E vec Y_i-vec T_i, then ||b_i||_2<=zeta and weighted least-squares Cauchy gives

    ||E theta_batch-theta||_V^2
      <=sum_i pi_i <b_i,K(U_i)^(-1)b_i>
      <=zeta^2/eta<=1/n.                                 (13)

Here ||v||_V^2=v^T Vv. Hence the complete second-moment matrix ABOUT THE TRUE theta obeys

    E[(theta_batch-theta)(theta_batch-theta)^T]
      <=101 V^(-1)/n.                                    (14)

The bound does not need identical tiny biases across batches. Each fresh local query's entire coarse/fine/finite-implementation law is already included. The previous-stage choice of U and pi is fixed before these fresh banks.

Use the exact known LDL factorization V=L_0 diag(d_j)L_0^T. In coordinates phi=L_0^T theta, (14) gives per-coordinate mean-square error <=101/(n d_j). By Markov/Chebyshev, error exceeding64/sqrt(n d_j) has probability below1/16. Take an odd

    b>=8 log(2 D J/beta),

where J is the predetermined number of scales, and use the coordinatewise median across batches before undoing L_0^T. Independence across fresh batches suffices even though coordinates within a batch are correlated. A conditional union bound across D coordinates and J stages gives

    ||theta_med-theta||_V<=64 sqrt(D/n).                  (15)

No decoder or output-projector net is used in this probability event.

For any UNIT vector v in C^d, put P=vv*. Equations (9),(15) give

    |v*(T_med,x-T_x)v|
      <=64 sqrt(D L/n) sqrt(v*U_x v)
      <=(1/64) sqrt(eta v*U_x v).                        (16)

The event is simultaneous over EVERY v and every x in X, by one coefficient norm bound; it does not union over an exponential family. Round each independent real/imaginary entry of each Hermitian coefficient matrix on a grid of mesh at most eta/(2^12 d), keeping conjugate symmetry exact. Since sum_j |a_j(x)|<=sqrt(20)<5, the extra operator error is below eta/64. Since U_x>=eta I, the rounded predictor T_hat therefore satisfies the convenient conservative bound

    |v*(T_hat,x-T_x)v| <= c sqrt(eta v*U_x v), c=1/16.     (17)

The predictor need not be PSD. No positive Choi completion is inferred.

## 6. Certified Loewner induction on the whole fixed grid

Let eta_j=2^(-j), eta_0=1, and U_0,x=2I_d. This base satisfies T_x+eta_0 I<=U_0,x<=3T_x+16eta_0 I. At stage j use U_(j-1) with target eta=eta_j. After (17), propose the quadratic matrix function

    U_j,x=2 T_hat_j,x+2 eta_j I_d.                        (18)

For every x in X, certify lambda_min(U_j,x)>=eta_j and lambda_max(U_j,x)<=19 by finite Hermitian eigenvalue enclosures. Allocate enclosure accuracy eta_j/16. If any range check is not certified, abort and use the fixed CPTP replacement decoder. There is no source call for this grid scan and no assertion of positivity at unqueried continuous encoders.

On a good previous history, U_(j-1)<=3T+32eta_j I. Applying (17) to any unit v and using

    2c sqrt[eta(3t+32eta)]
       <=t+(3c^2+2c sqrt32)eta < t+(3/4)eta

gives the simultaneous Loewner bounds

    T_x+(5/4)eta_j I <= U_j,x <= 3T_x+(11/4)eta_j I.      (19)

Thus all range certificates pass with slack on good histories, and in particular the invariant T+eta_j I<=U_j<=3T+16eta_j I is preserved. Accepted envelopes on bad histories remain certified positive and bounded, so (7)-(10) still cap every subsequent source bank and arithmetic step. Conditional first-failure accounting costs at most beta. The initial U_0=2I, rather than I, is important for the covariance floor at the first stage.

## 7. Full-CPTP final risk and comparator

At the final scale eta, put tau=k eta. For ANY full CPTP C, diagonalize C only in the proof. Its positive eigenvalues sum to EXACTLY k. Sum (17) over those eigenvectors and use scalar Cauchy-Schwarz. With q=Tr(T_x C), qhat=Tr(T_hat_x C), the result is

    |qhat-q|<=c sqrt(3k eta q+32k^2 eta^2)
             =c sqrt(3tau q+32tau^2).                    (20)

Thus the only final trace penalty is k, not d*k or k^2. In particular

    |sqrt(max(0,qhat))-sqrt(q)|<=2 sqrt(tau).

For finite decoder synthesis search the explicit interior body K_s={C>=sI/2,Tr_out C=I_k}, with a convenient rational s in [epsilon/512,epsilon/256]. A full decoder can be mixed with replacement at Bell-loss cost at most s. Minimize the FINAL affine qhat over all x in X and C in K_s using standard feasible decoder SDPs, to objective gap at most tau. Exact rational PSD/TP repair and all compilation costs are the received finite interface, with the gap debit shared between solver and repair. No unknown decoder is supplied after selection.

The same scalar root-risk calculation as the received k^6 theorem gives

    q_selected <=(1+gamma/4)min_(X,K_s) q+125 tau/gamma.   (21)

At the true optimum (x*,C*), the fixed-C* risk is a nonnegative bounded quadratic in x, and x* minimizes that quadratic. Therefore the fixed net's squared radius h^2, not a Lipschitz radius h, pays comparator discretization. With h^2<=epsilon/256 and s<=epsilon/256,

    min_(X,K_s)q <= (2/3)ell_star+s+h^2.

Choose the final dyadic eta within a factor two below gamma epsilon/(2^15 k). Equations (20)-(21) then give on the good ideal-frame branch

    ell_selected <=(1+gamma/4)ell_star+epsilon/16.

Use beta<=epsilon/32 and reserve a separate whole-process final Bell-loss debit at most epsilon/4 for finite frame, ordinary preparation, purification, known measurements, decoding and the ONE payload. Bad/aborted records have completed loss at most one. This proves the candidate expected relative target with slack if the imported interfaces and the new argument are independently received.

## 8. Complete deterministic source and control bill

For stage j let S_j<=10+T_max,j. Summing (3),(10) over support and b batches gives the capped bill

    N_j=O(b [ n_j + S_j(r/eta_j
                +d r log(d r (n_j+r/eta_j+log(1/zeta_j))/zeta_j)
                +log(1/zeta_j)+1) ]).                   (22)

Every support ceiling, center, failure and bias precision appears. There are no expected-stopping refunds. The geometric sum of 1/eta_j and D=10d^2,L=8D imply

    N=O_tilde(D^2/eta_final)
      =O_tilde(k^5/(gamma epsilon)).                    (23)

The total fine-bank floors contribute O_tilde(D r/eta_final)=O_tilde(k^4/(gamma epsilon)); total coarse centers contribute O_tilde(D d r)=O_tilde(k^4), with the displayed logarithms. Both are dominated by (23), not omitted.

The encoder grid is polynomial in inverse accuracy because the real selector dimension is fixed. Each design support has O(D log(1/eta)) settings, and design arithmetic consists of polynomial-size matrix inversions, trace comparisons and LDL factorization. Matrix dimension D=10d^2 is explicit. All coefficient rounding is stagewise; finite bit complexity does not inherit unbounded recursive numerical expressions. The final continuous decoder optimization is an SDP with an explicit positive interior margin. Thus processing is polynomial, though deliberately large and not a practical performance guarantee.

Let H be the predetermined source cap N plus one payload; pad unused slots with dummy ordinary calls when required by the frame contract. The later explicit causal frame compiler supplies the common-U law for arbitrary linked operators and costs polynomial gates/workspace in H,k,log(d_phys),log(1/nu). Retain this SAME frame throughout all adaptively chosen homogeneous query banks and the payload. Each local purification's own memory/control ledger is additionally paid. Prove the entire adaptive history conditional on mathematical U, then average U and all internal/local purification records. A batch-only compression statement or unrelated frames across settings would not justify the GLS model.

## 9. Scientific boundary and evidence status

The proposed advance is a block-design composition of the received local matrix oracle, not new tomography, an efficient Hayashi implementation, or a quantum advantage over an equally informed conventional learner. The scalar k^6 proof remains independently authoritative until this manuscript receives its own review. The generic k^2 fast-rate target remains open. This construction explicitly pays collective receiver memory and controls, unlike the scalar-bit baseline.

The possible further k^4 route would replace the D-dimensional coordinate-median norm with a sharper matrix concentration argument. That concentration is NOT assumed here: only the received finite directional MSE, weighted least squares, coordinate medians, and deterministic matrix inequalities are used. Nor does this theorem infer a universal sup-average Bures bound or sum independently learned row-cone radii. It uses fresh adaptive encoder settings and globally certified Loewner envelopes on one fixed finite grid.
