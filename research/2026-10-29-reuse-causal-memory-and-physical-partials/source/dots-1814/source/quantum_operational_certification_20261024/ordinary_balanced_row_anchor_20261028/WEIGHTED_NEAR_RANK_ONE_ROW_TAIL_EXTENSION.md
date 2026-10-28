# Weighted near-rank-one row tails: an explicit task penalty

28 October 2026, post-16:05 candidate work. Author derivation, independent receiving pending. This is separate from the frozen exact rank-one balanced-anchor theorem. It does not claim that finite noisy data certify exact rank one or supply a fast upper certificate for the tail below.

## 1. Physical model and a compatible source factor

Keep the actual known receiver basis, ordinary four-real-coordinate encoder, balanced anchor x0 and full-CPTP decoder task of `BALANCED_RANK_ONE_ROW_ANCHOR_ACQUISITION.md`. Now allow general real PSD diagonal effects B_i, sum_i B_i=I_4. Let lambda_i be a largest eigenvalue, choose a corresponding real unit u_i, and define

    tau_i=Tr B_i-lambda_i, tau_row=sum_i tau_i.

For every nonzero B_i assume the selected leading direction satisfies |u_i^T x0|²>=kappa. This remains a structural promise in the ACTUAL basis. The tail may be supplied as a bound or simply appear in the resulting oracle inequality; it is not inferred from a confidence interval that was proved only for rank-one rows.

The true physical family admits one PSD selector/output coefficient lift: factor it into row maps G_i from the four-dimensional selector into one common environment, so

    Psi_x=sum_i |i> G_i x, T_x=Tr_env |Psi_x><Psi_x|,
    B_i=Re(G_i*G_i).

This is a mathematical factor of the ACTUAL source. Such a lift is supplied by the physical linear encoder and ordinary six-state loss preparation; no coherent selector is physically prepared here. It is not an arbitrary fitted positive completion and does not follow merely from positivity of an unrelated matrix polynomial.

Project each row input onto P_i=u_i u_i^T and put

    Phi_x=sum_i |i> G_i P_i x,
    R_x=diag((u_i^T x)/(u_i^T x0)).

Then Phi_x=R_x Phi_x0. Also

    ||Psi_x-Phi_x||²
      =sum_i x^T(I-P_i)B_i(I-P_i)x<=tau_row,
    ||R_x||<=1/sqrt(kappa).

Using the SAME actual purification through both encoders therefore gives

    ||Psi_x-R_x Psi_x0||
       <=sqrt(tau_row)+(1/sqrt(kappa))sqrt(tau_row)
       <=2sqrt(tau_row/kappa).                         (1)

For every actual full decoder C, its loss operator has norm at most3. Thus the root loss of the real T_x differs from that of the positive predictor R_x T_x0 R_x by at most sqrt(12 tau_row/kappa), uniformly in x,C. Independent per-x purifications have not been aligned by assumption.

## 2. The count pilot remains fast after charging poorly shaped rows

The same finite fourth design and coordinate measurement give

    Pr(i)=Tr B_i/4,
    E[xx^T|i]=(I_4+2B_i/Tr B_i)/6.                     (2)

Call a row well shaped if tau_i<=lambda_i/4. Its conditional population eigengap is at least1/5. A row that is not well shaped has Tr B_i<=5tau_i, so all such row masses total at most5tau_row. They need not be detected or assigned a reliable eigenvector by the algorithm.

Use a larger high-count threshold4096L, keeping the finite rational unit-vector accuracy sqrt(L/N)/100 and the same safe anchor test/fallback. On the good bounded-matrix event, well-shaped high-count rows have direction error e_i=sin² angle(u_i,v_i)<=1024L/n_i. Low/missing rows use e_i=1. The same binomial lower-count split at N Tr B_i/4>=8L gives

    sum_(well shaped i) lambda_i e_i <=2^16 d L/N.       (3)

The declared constant covers both low observed counts and high-count eigenvectors. The total ideal failure probability is at most beta_t with the same conservative L>=log(64d/beta_t). No unknown mass or gap is divided out; the constant gap is used only on the mathematical well-shaped class, and the other class is paid by its actual total tail mass.

The algorithm's row vectors always have norm at most2/sqrt(kappa). For a well-shaped row, the actual anchor weight is

    w_i=x0^T B_i x0=lambda_i(u_i^T x0)²+t_i0,
    0<=t_i0<=tau_i.

The earlier ratio inequality pays its leading part, and the extra part costs at most9tau_i/kappa. A poorly shaped row costs at most9 Tr B_i/kappa<=45tau_i/kappa, irrespective of its estimated direction. Hence the uniform squared purification error between the true leading-row predictor and the learned-row predictor is bounded by

    E_row<=2^21 dL/(kappa N)+54tau_row/kappa.             (4)

This is weighted actual mass, not a count of rare labels.

## 3. One actual anchor bank and the complete task inequality

Acquire the actual T_x0 Bures bank as before, at1-f(T_x0,tau)<=m. Combining (1), (4), and the same bounded diagonal row map gives

    delta<=sqrt(12tau_row/kappa)+sqrt(3E_row)
                                   +sqrt(24m/kappa),
    delta²<=522tau_row/kappa
              +9*2^21 dL/(kappa N)+72m/kappa.           (5)

Take, for example,

    N>=2^38 dL/(kappa gamma epsilon),
    m<=kappa gamma epsilon/2^22,
    nu_opt<=gamma epsilon/32768,
    beta_t=beta_q=epsilon/256.

The statistical part of(5) is at most gamma epsilon/8192. The same physical full-CPTP SDP/grid optimizer has

    sqrt(ell_selected)<=sqrt(ell_star)+2delta+sqrt(nu_opt).

Young's inequality and a single bad-history debit therefore give the conservative Bell-risk bound

    E ell_selected
      <=(1+gamma/2)ell_star+epsilon/64
                         +2^14 tau_row/(kappa gamma).   (6)

After a single separately paid whole-process discrepancy at most epsilon/2 and private framing, one subsequent unknown payload satisfies

    ||Lambda_actual-id||_diamond
      <=min{2,(1+gamma)Delta_star+epsilon
                             +2^15 tau_row/(kappa gamma)}. (7)

The source scale remains O_tilde((d+dr)/(kappa gamma epsilon))+1. A supplied tau_row=O(kappa gamma epsilon) makes the extra penalty target-sized; without such a promise, (6)-(7) are explicitly approximation-sensitive oracle bounds and may be vacuous. No calibration transcript is claimed to certify a small tau_row at this fast rate.

## 4. Preserved limits

The factorization in Section1 is the actual physical coefficient lift only. An independently fitted PSD lift cannot be substituted without an acquired error bound. A random causal output frame can destroy the diagonal structure and is still not imported. No unknown basis acquisition, free rare-postselection operation, source inversion, stronger payload encoding, exact-rank certificate or generic strict-ordinary k² result follows.
