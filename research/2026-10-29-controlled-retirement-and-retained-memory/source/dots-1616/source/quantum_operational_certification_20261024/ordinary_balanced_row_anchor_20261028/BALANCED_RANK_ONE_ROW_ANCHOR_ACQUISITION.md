# Ordinary full-policy acquisition from a balanced rank-one row anchor

28 October 2026. New construction candidate; independent receiving pending. This is a conditional STRICT-ORDINARY acquisition theorem with a substantive, basis-dependent model promise. It does not claim that arbitrary sources have this structure or that a random output frame preserves it. The final decoder is unrestricted CPTP and may use quantum coherence between every output row; pilot measurement labels are not intrinsic source flags.

## 1. Actual interface, model promise and target

Use a stationary independently reset source and the known linear four-real-coordinate encoder V_x=sum_{s=1}^4 x_s V_s, x in S³. Its physical output is an ACTUALLY AVAILABLE known k-dimensional quantum register with a fixed known basis. A separately justified structure-preserving interface may replace this register only with its own paid error/control contract. Generic random frame reduction is NOT such an interface.

At any chosen x, the received ordinary six-state preparation produces the actual loss density T_x on B tensor A, dimension d=2k, from ONE source call. It is PSD, quadratic in real x, normalized, and

    ell(x,C)=(3/2)Tr(C^T T_x)

for every full-CPTP decoder Choi matrix C, with Tr_A C=I_k and0<=C<=2I. The known tensor-product B/A basis is used below. A valid encoded Choi-rank bound R gives rank T_x<=r=min(d,3R); it is a tomography parameter, not a source spectral floor.

**Rank-one row promise.** For each coordinate i=1,...,d,

    p_i(x):=(T_x)_ii=x^T B_i x,
    B_i=lambda_i u_i u_i^T, lambda_i>=0, ||u_i||=1

when lambda_i>0. The real directions u_i and masses lambda_i are UNKNOWN. Normalization gives sum_i B_i=I_4 and sum_i lambda_i=4. Rank zero is allowed. Exact rank-one structure is a model promise, not a conclusion certified from noisy data.

**Balanced anchor promise.** A known calibrated rational unit vector x0 and rational0<kappa<=1 satisfy

    |u_i^T x0|²>=kappa

for every nonzero row. This is not a useful logical-code or small-loss seed promise. The anchor may have large optimal loss, and all lambda_i may be arbitrarily small. No Kraus matrices, output flags, protected reference or coherent selector input is supplied.

For0<gamma,epsilon<=1, the construction learns an encoder and an actual full CPTP decoder with

    E ell_selected <=(1+gamma/2)ell_star+epsilon/64,       (1)

before a separately budgeted whole-process implementation discrepancy. Here ell_star=min_{x,C CPTP}ell(x,C), with no zero-optimum assumption. Independent private Pauli framing on one subsequent payload then gives actual unhalved error at most

    min{2,(1+gamma)Delta_star+epsilon}, Delta_star=2ell_star,

when the implementation discrepancy is at most epsilon/2. All calibration precedes the unknown payload. The source cap is

    O_tilde((d+dr)/(kappa gamma epsilon))+1
       =O_tilde(k²/(kappa gamma epsilon))+1.             (2)

If an actual known output interface additionally has k=O(R), this is rank-squared. That dimension relation is not obtained by applying a structure-destroying random frame. The equally informed conventional learner can use the identical construction.

## 2. Exact positive-polynomial quotient, not a fitted Choi completion

For i,j with nonzero rows, PSD implies

    |(T_x)_ij|²<=lambda_i lambda_j (u_i^T x)²(u_j^T x)².

The quadratic polynomial (T_x)_ij vanishes on each of the two real hyperplanes u_i^T x=0 and u_j^T x=0. If the forms are independent, polynomial divisibility therefore makes it a scalar multiple of their product. If they are proportional, the displayed bound forces divisibility by their square. Zero diagonal rows vanish identically. Thus, on the nonzero rows,

    T_x=R_x T_x0 R_x,
    R_x=diag(r_i(x)), r_i(x)=(u_i^T x)/(u_i^T x0),
    ||R_x||<=kappa^(-1/2).                              (3)

The unknown row sign cancels. Equivalently r_i(x)=(x^T B_i x0)/(x0^T B_i x0); no coherent-selector phase or row gauge is granted. Equation(3) is an identity of the ACTUAL source under the stated rank-one promise. It is not an inference that any positive completion of arbitrary measured quadratic coefficients is Bures-close.

One actual quantum bank at x0 therefore carries all the output coherences. The remaining acquisition is only the directions of the small real effects B_i. A predictor built with estimated rows need not itself be a TP channel Choi state; positivity, uniform task-risk transfer and a feasible decoder optimization suffice below.

## 3. Fixed ordinary count acquisition, with no minimum row mass

Use the following finite even fourth-moment design on S³: each of the four coordinate axes has probability1/12, and each of the16 sign vectors (±1,±1,±1,±1)/2 has probability1/24. A uniform24-slot sampler implements these rational probabilities exactly. Only even moments are used, so the sign of an axis representative is irrelevant. The moments are

    E xx^T=I_4/4,
    E[xx^T(u^T x)²]=(I_4+2uu^T)/24.

On each pilot call draw x from this design, prepare the actual T_x by the ordinary six-state procedure, then measure its B/A coordinate i. Store the classical pair (x,i). All source calls and all outcomes are counted. The quantum output is destroyed only in this CALIBRATION pilot, never silently in deployment.

For a nonzero row,

    Pr(i)=lambda_i/4,
    E[xx^T | i]=(I_4+2u_i u_i^T)/6.                    (4)

The conditional population matrix has eigengap1/3, independent of lambda_i. This is the source of the fast weighted rate. Conditional on the observed label sequence, the x records of each row are iid from (4). It is not an assumption that an expected rare count is a realized count.

Let beta_t=epsilon/256 and choose an integer

    L>=log(64d/beta_t), L>=1,
    N=ceil[2^32 d L/(kappa gamma epsilon)].              (5)

A ceiling of the corresponding base-two logarithm is a conservative finite integer choice. Let n_i be the actual count. If n_i<=256L, use a safe row fallback. Otherwise form its empirical4 by4 mean and compute a rational unit vector v_i approximating a top eigenvector to Euclidean error at most sqrt(L/N)/100. A failed observed-gap/eigenvector certificate also uses the fallback; on the good event below, every high-count row has a certified gap at least1/12 and does not fail. Four-dimensional rational eigenvector/normalization arithmetic costs polynomial precision bits; there is no unknown source eigengap in this operation.

For high-count rows, matrix Bernstein and the gap give, simultaneously except probability at most beta_t,

    e_i:=sin² angle(u_i,v_i)<=256L/n_i.

For low-count or missing rows set the error-accounting value e_i=1. The usual bounded Hermitian Bernstein bound applies to xx^T of norm1; taking t=sqrt(3L/n_i) gives failure at most8e^(-L), and Davis-Kahan plus the stated finite vector error fits the factor256. This uses only a4 by4 known-matrix calculation. The finite rational unit vector can be produced by a stereographic S³ approximation; no exact irrational eigenvector is assumed.

At the same time, for every row with N lambda_i/4>=8L, a binomial lower-tail bound gives n_i>=N lambda_i/8. Rows below that threshold have total mass at most32dL/N. Combining the two classes yields the weighted bound

    sum_i lambda_i e_i <=4096 d L/N.                    (6)

This includes all missing/rare rows and has no lambda_min. The confidence allocations in L dominate both union bounds. The fixed raw cap N is never replaced by an expected stopping time.

## 4. Safe ratios and their weighted stability

For an accepted direction v_i, use the EXACT rational test |v_i^T x0|²>=kappa/4. If it passes, put

    s_hat_i=v_i/(v_i^T x0).

Otherwise, and for every low-count/missing row, put s_hat_i=x0. Thus every returned row obeys s_hat_i^T x0=1 and ||s_hat_i||<=2/sqrt(kappa). Define Rhat_x=diag(s_hat_i^T x). The directions' arbitrary signs cancel in the ratio; no anchor-orientation sign inference is needed.

Let w_i=p_i(x0)=lambda_i(u_i^T x0)². For a passing row, choose the sign of v_i only in the proof to align it optimally with u_i. Writing a=u_i^T x0, b=v_i^T x0, one has

    w_i ||s_hat_i-u_i/a||²
      =lambda_i ||a v_i/b-u_i||²
      <=32 lambda_i e_i/kappa.                         (7)

Indeed |b|>=sqrt(kappa)/2, ||a v_i-bu_i||<=2||v_i-u_i||, and the aligned squared vector distance is at most2sin² angle. If the anchor test fails, |a|-|b|>=sqrt(kappa)/2 forces e_i>=kappa/8, while the fallback has weighted squared error lambda_i(1-a²)<=lambda_i. Low-count rows are also covered by e_i=1. Hence, uniformly over all real unit x, including unqueried encoders,

    sum_i w_i |rhat_i(x)-r_i(x)|²
       <=32/kappa sum_i lambda_i e_i
       <=2^17 d L/(kappa N)=:E_row.                    (8)

No denominator depending on an unknown rare row mass is divided out. All finite ratio denominators that are actually used have the known direction floor sqrt(kappa)/2.

## 5. One ordinary quantum bank and the full-decoder root bound

Independently acquire n0 actual T_x0 copies in the SAME known physical output basis. Apply the received ordinary Bures matrix query with

    m=kappa gamma epsilon/2^20, beta_q=epsilon/256,
    D0=nextpow2(d r),
    n0=ceil[(80D0/m)log(12D0/beta_q)].                  (9)

Its returned physical density tau obeys1-f(T_x0,tau)<=m except beta_q; f is root fidelity. The rank bound is used only for this actual state, not for a signed or fitted source completion. This bank and its collective receiver/control/memory costs are fully paid.

Use the positive quadratic predictor

    T_hat_x=Rhat_x tau Rhat_x.                          (10)

It is not asserted normalized or a valid source Choi completion. On the pilot good event, a single purification of the ACTUAL T_x0 gives

    ||(Rhat_x-R_x)sqrt(T_x0)||F²
       =sum_i w_i |rhat_i-r_i|²<=E_row.

This is one compatible reference state for ALL x, not independently aligned purifications at different encoders. Uhlmann alignment of tau with that same state gives a further squared purification error at most(4/kappa)2m. Since every actual decoder has ||(3/2)C^T||<=3, the positive loss functional obeys

    sup_{x,C CPTP}|sqrt(ell(x,C))-sqrt(ell_hat(x,C))|
       <=sqrt(3E_row)+sqrt(24m/kappa)=:delta.

The chosen constants imply

    delta²<=6E_row+48m/kappa<=gamma epsilon/4096.         (11)

This is the actual task metric, including arbitrary coherent full-CPTP decoders. It does not estimate or deploy a decoder obtained by measuring the row labels.

## 6. Finite encoder/decoder optimization and total error

For a fixed C, ell_hat(x,C) is a nonnegative quadratic in real x, bounded above by12/kappa. Use a finite rational S³ encoder net of squared chord radius h²<=kappa nu_opt/48, and solve the full decoder SDP at each net point to total additive objective debit at most nu_opt/2. Choose

    nu_opt<=gamma epsilon/16384.

At a continuous joint optimum, the fixed-decoder quadratic is stationary in its encoder variable. Its Hessian/range bound therefore gives an h² rather than h loss. The grid and SDP solve together produce a physical pair within nu_opt of the surrogate optimum. The grid is classical processing, not additional source settings. Full CPTP feasibility, exact finite inward rounding and decoder compilation are paid by the received known-coefficient SDP/control contract; no decoder menu is substituted.

From(11), the selected actual pair on the simultaneous good event satisfies

    sqrt(ell_selected)<=sqrt(ell_star)+2delta+sqrt(nu_opt)
       <=sqrt(ell_star)+3sqrt(gamma epsilon/4096).

Young's inequality with gamma/2 gives

    ell_selected<=(1+gamma/2)ell_star+27epsilon/4096
       <(1+gamma/2)ell_star+epsilon/128.

The ideal bad statistical event has probability at most beta_t+beta_q=epsilon/128. Every actually selected decoder is physical, so its Bell loss is at most1 even on a bad pilot/solver record. This proves(1). A single whole-process implementation discrepancy at most epsilon/2, including all preparations, sampler bits, measurements, finite receiver estimation, decoder synthesis and the subsequent private-framed payload, gives the stated unhalved channel guarantee. Private records are discarded; no conditional-on-record or normalized acceptance claim follows.

The deterministic source horizon is H=N+n0+1. There are20 distinct pilot input settings (24 weighted sampler slots) and one quantum anchor bank; no physical encoder-net multiplier occurs. All source calls are ordinary and no half of a sender-entangled input is retained. Receiver-local qubit preparation in T_x and collective receiver memory are allowed and paid. Processing is polynomial in the declared horizon, k,1/kappa,1/gamma,1/epsilon and known control sizes. These are theoretical finite budgets, not practical hardware claims.

## 7. Scope and governing imports

The loss-state preparation, rank bound, full-decoder norm and Bures bank are from `../ordinary_bures_matrix_query_confidence_20261027.md` and its accepted underlying finite estimator. Bernstein concentration is used only for a fixed4-dimensional classical moment estimator; the exact conditional-moment identity and weighted missing-count accounting are proved here. The full known-coefficient decoder optimization and private-framed Bell-to-complete-risk comparator are received programme imports.

The row-rank-one promise is about selector dependence of OBSERVED loss-density diagonal coordinates, not one Kraus operator per flag. The acquired T_x0 can be mixed and carry essential off-diagonal coherences. Sources with ordinary correlated output dephasing after a known-basis product-row isometry provide nontrivial instances; measuring coordinates during deployment can destroy their logical coherence. The theorem imposes neither a source/Choi eigenvalue floor nor zero optimal loss.

A balanced anchor is a structural calibration interface, not a supplied good recovery seed. The fixed known receiver basis is essential. Unknown basis acquisition, approximately rank-one diagonals and the absence of a balanced anchor remain separate problems. An arbitrary positive coefficient completion, mask inverse or random-frame rotation does not inherit this theorem. Strong conventional protocols receive the same controls and the same useful subclass result; no universal quantum-over-classical separation is claimed.
