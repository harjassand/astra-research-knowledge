# Acquiring a common extremal recovery without learning its environment

Author construction, 2026-10-28. **Unreviewed**. This is a finite-dimensional robustness and acquisition theorem, not a claim of efficient arbitrary-noise quantum memory, historical novelty, or a completed hardware architecture. Existing Pauli-extractor results remain intact.

## 1. Conventions and operational target

A recovery D maps dimension d to dimension k. Its unnormalized Choi matrix K is ordered output then input, is PSD, and A(K) = Tr_output K = I_d. Thus Tr K = d. Native noise N maps logical dimension k to receiver dimension d. For Kraus E_a of N, define H_N = sum_a |vec(E_a†)><vec(E_a†)|. For recovery Kraus R_l,

    F_e(D N) = sum_{a,l} |Tr(R_l E_a)|²/k² = Tr(H_N K)/k².

H_N is a transpose and tensor-factor swap of the native Choi matrix. It is therefore obtainable from ordinary input-output process statistics without learning a Kraus representation or measuring the environment. Generic informationally complete acquisition still has dimension-dependent cost; no tomography-free scaling advantage is claimed here. The reduced task is acquiring a common recovery, with a certificate that can remain valid as native noise drifts inside its normal cone.

## 2. Global quadratic growth from a support certificate

Let K_0 be feasible, P its support, and suppose A restricted to Herm(P) has smallest Frobenius singular value sigma > 0. Suppose a Hermitian objective H has a dual witness Y such that

    Q = I_k tensor Y - H,  Q K_0 = 0,  Q >= mu (I-P),  mu > 0.

Set G = 2d(1 + k/sigma²). Then K_0 is the unique optimizer among all CPTP recoveries, and every feasible K obeys

    Tr H(K_0-K) >= (mu/G) ||K-K_0||_F².                 (1)

**Proof.** Write A_0 = PKP, B = PKPperp and R = Pperp K Pperp, with t = Tr R. Positivity gives ||B||_F² <= (d-t)t (e.g. PSD block factorization B=A_0^(1/2) C R^(1/2), ||C||op<=1). For Z = B+B†+R, orthogonality and ||R||_F <= Tr R give

    ||Z||_F² <= 2(d-t)t + t² = 2dt-t².

Since A(PKP-K_0)=-A(Z) and the partial trace has Frobenius operator norm sqrt(k),

    ||PKP-K_0||_F² <= k ||Z||_F²/sigma².

The support and remaining blocks are orthogonal, so

    ||K-K_0||_F² <= (1+k/sigma²)(2dt-t²) <= Gt.

Dual feasibility and TP give Tr H(K_0-K)=Tr QK >= mu t. This proves (1). No generic SDP error-bound theorem is required for this bound. Support injectivity is the familiar extreme-channel criterion: a nonzero support-Hermitian TP-null direction would yield a small feasible two-sided perturbation; conversely any nontrivial convex decomposition supplies such a direction. In particular rank(K_0) <= d.

## 3. A posteriori acquisition and regret

Suppose a physical fitted candidate K_c has a certificate (P_c,sigma_c,mu_c,Y_c) for fitted objective H_tilde, with G_c as above. If the actual calibration objective H satisfies ||H-H_tilde||_F <= e, then **every** optimizer K_* of H obeys

    ||K_c-K_*||_F <= G_c e/mu_c.                       (2)

Indeed candidate quadratic growth, actual optimality, and Cauchy-Schwarz imply (mu_c/G_c)D² <= eD. The actual objective regret has the sharper bound

    max_K Tr HK - Tr H K_c <= G_c e²/(4mu_c),          (3)

by maximizing eD-(mu_c/G_c)D². Divide (3) by k² for entanglement-fidelity regret. It is not legitimate to apply (3) to a different future objective solely because it shares K_*; future regret then needs its objective norm or a direct channel-distance bound.

For operation substitution, standard unnormalized Choi inequalities give

    1/2 ||D_c-D_*||diamond <= 1/2 ||K_c-K_*||_1
                             <= sqrt(dk) G_c e/(2mu_c).

Clip this at 1. This is a composable channel comparison, not a capacity claim. Hardware compilation/calibration error adds separately by triangle inequality. Repeated use costs at most the sum of per-use half-diamond errors, even with joint memory and adaptive surrounding operations.

An objective confidence radius epsilon plus fit residual rho gives e=epsilon+rho. Confidence must hold for the acquired objective before data-dependent fitting, e.g. a simultaneous matrix-norm confidence set, rather than a pointwise confidence statement for a subsequently chosen optimizer.

## 3a. One explicit ordinary-probe acquisition interface

Choose k² linearly independent logical density matrices rho_j: the computational-basis projectors and, for each a<b, the projectors onto (|a>+|b>)/sqrt(2) and (|a>+i|b>)/sqrt(2). Let their Hermitian Hilbert-Schmidt duals D_j satisfy Tr(D_j rho_i)=delta_ji. For the d-dimensional output use the analogous d² spanning density matrices sigma_l, T=sum_l sigma_l>0, and the informationally complete POVM M_l=T^(-1/2) sigma_l T^(-1/2). Compute its Hermitian dual frame F_l, so X=sum_l Tr(M_l X) F_l. These finite matrices and their conditioning constants are acquired/calibrated control requirements, not environmental access.

At use t choose j uniformly with a fresh private random coin, prepare rho_j independently of source memory, pass it through the native channel and measure this POVM, observing l. In output-then-input order define

    J_hat_t = k² F_l tensor D_j^T,
    H_hat_t = Swap J_hat_t^T Swap.

Conditional on past records before the private current input choice, the mean is H_t, the objective of the conditional native channel. This follows from N_t(rho_j)=sum_l p_t(l|j)F_l and J_Nt=sum_j N_t(rho_j) tensor D_j^T. Retained source memory is allowed; current-input side channels or an initial probe-memory correlation are not included. The estimator does not assume a measured error syndrome, known Kraus operators or a channel-fit oracle.

Here is a deliberately conservative fully explicit confidence bound. Let B=k² max_l ||F_l||_F max_j ||D_j||_F and n=(dk)². Expand in any fixed Hermitian Frobenius-orthonormal basis. Each coordinate of H_hat_t-H_t is a martingale difference bounded in absolute value by 2B. Coordinate Azuma and a union bound imply, with probability at least 1-delta,

    ||(1/Tuses) sum_t H_hat_t - (1/Tuses) sum_t H_t||_F
       <= B sqrt(8 n log(2n/delta)/Tuses).            (4)

The target is the predictable bank average H_bar, not a fictitious stationary channel. If one K_* optimizes every conditional H_t, it optimizes H_bar, since each objective inequality averages. Thus (2) with H=H_bar bounds distance to this same K_*. A common optimizer only for an unconditional average is insufficient to identify a future conditional oracle. Future optimality, high fidelity, capacity and a favorable dimension/sample scaling do not follow from (4). Preparation/readout bias must be included as a separately bounded additive objective bias, and execution error as a separate channel implementation error. For stopping over repeated banks, preallocate failure budgets delta_b with sum_b delta_b<=delta or use a genuinely time-uniform bound.

## 4. Finite candidate construction, rank selection and dual fitting

There is no supplied extreme recovery oracle.

1. Acquire an ordinary informationally complete native-channel data bank and compute objective estimate H_hat with a simultaneous Frobenius confidence radius. A fixed bounded dual-frame estimator and a martingale/vector concentration bound suffice under drifting conditional native channels. Record actual preparations, measurements, frame conditioning and sample count; this theorem does not supply those resources for free.
2. Solve the empirical recovery SDP to a certified objective tolerance zeta, using a feasible physical solution or certified feasibility repair. Enumerate ranks r=1,...,d. For each r, form its PSD largest-r-eigenvalue truncation K_r.
3. Certify M=Tr_output K_r > 0. Normalize

       K_c = (I_k tensor M^(-1/2)) K_r (I_k tensor M^(-1/2)).

   This is exactly PSD and TP; retain candidates only when rank and eigenvalue guards can be certified. Evaluate support-TP smallest singular value sigma_c and require a positive certified lower bound.
4. For fixed candidate support let Z have orthonormal columns spanning its complement. Fit Hermitian Y and L >= mu I by convex least-squares/conic optimization:

       Q_c = Z L Z†,  H_tilde = I_k tensor Y - Q_c,
       minimize ||H_hat-H_tilde||_F.

   Exact kernel is enforced algebraically, not inferred from a small floating-point Q_c K_c residual. Acceptance requires only a feasible fit with a certified residual, not attainment of the global least-squares infimum. Use bounded-variable caps expanded across stages, or algebraic feasible-point enumeration, as a finite fallback. The transported strict-gap witness in the completion argument has finite coefficients and eventually lies inside a cap; choosing a smaller mu threshold leaves a strict margin for finite approximation. Search finite grids of positive mu thresholds and increasing accuracy; record a rigorous upper bound rho on fit residual. H_tilde need not itself be a physically realizable native objective: it is a dual robustness witness.
5. Accept only when the certified right side of (2) or a requested operational tolerance is small enough; otherwise acquire more data or abstain. Every stage has finite rank/grid/solver caps. Symbolic algebraic matrices, interval evaluation with strict margins, or certified rational parameterizations can represent the witnesses; a bare float eigenvalue test is not a certificate.

**Finite proposal realization rather than an ideal solver oracle.** A floating Hermitian proposal X with certified X>=-eta I can first be shifted to X+eta I and TP-normalized whenever its partial trace has a certified positive floor. If eta and the original TP residual vanish, this repair is continuous near the feasible set (whose partial trace is I). Alternatively a slow, complete finite search supplies the empirical SDP tolerance: rational strictly positive feasible primal matrices are dense in the CPTP set by mixing with I_k/k tensor I_d, and rational strictly dual-feasible Y are dense above a sufficiently positive scalar identity. Enumerate rational TP-feasible PSD primal and dual witnesses for the acquired algebraic objective, accepting when their rigorously evaluated objective gap is below zeta. Strict feasible witnesses make their positivity checks terminate; strong duality follows from primal/dual Slater points. This is a computability/completion fallback, not an efficient implementation claim. Efficient certified SDP numerical solvers may replace it. Spectral truncation and inverse square roots at guarded algebraic inputs are finite algebraic matrix operations; physical synthesis is still separately paid. If the empirical objective or controls are only represented by intervals, enlarge their error budget and use interval-safe strict witnesses rather than pretending exact coefficients are available.

**Conditional eventual acceptance.** Suppose the true common optimizer K_* has rank r_*, a positive nonzero eigenvalue floor, injectivity sigma_*>0, and a strict complementary dual gap mu_*>0 for a fixed limiting objective H_*. If empirical objectives converge to H_* and solver tolerances vanish, feasible empirical solutions converge to K_*. In fact with ||H_hat-H_*||_F<=epsilon, a zeta-optimal empirical solution has distance at most

    G_*/(2mu_*) [epsilon + sqrt(epsilon²+4mu_* zeta/G_*)].

The r_* truncation therefore converges to K_*, M converges to I, and its normalized support converges to P_*. Support injectivity is open. Choose a near-identity ambient unitary W mapping P_* to P_c. Q_c=WQ_*W† has the same strict gap and exact candidate kernel, while H_tilde=I_k tensor Y_*-Q_c converges to H_*. Thus the fitted residual can approach zero. W is only an existence witness for the finite fitting problem, not a free physical operation. Positive guards and a sufficiently fine finite mu search eventually accept for any fixed nonzero target tolerance. The same argument extends to varying bank objectives only with uniform eigenvalue/injectivity/gap bounds and bounded dual witnesses, or another explicitly proved uniform condition; arbitrary drift alone does not prove completion.

Matrix sizes are dk by dk; support injectivity has r² real columns and d² rows. Generic acquisition and dense SDP costs may be prohibitive. Compilation of a rank-r recovery requires a Stinespring isometry into k*r dimensions (padding allowed) and a specified finite gate set, accuracy and gate count. Algebraic decidability, SDP existence and physical efficiency are separate claims.

## 5. A strict nonunitary oracle on a physical native family

Take k=2, d=3, receiver basis 0,1,e, p in (0,1), and s=sqrt(1-p). Native noise has Kraus

    E_0=|0><0|+s|1><1|,   E_1=sqrt(p)|e><1|.

Recovery Kraus are R_0=[I_2,0] and R_1=|1><e|. Its K_0 has eigenvectors r_0=|00>+|11> and r_1=|1e>, with nonzero eigenvalues 2 and 1. The orthonormal support basis is r_0/sqrt(2),r_1. The TP restriction has singular values {1/sqrt(2),1/sqrt(2),1/sqrt(2),1}; hence sigma²=1/2 and G=30.

The physical objective and dual are

    H=|00+s11><00+s11|+p|1e><1e|,
    Y=diag(1+s,s(1+s),p).

Q=I_2 tensor Y-H is zero exactly on supp K_0, and its positive eigenvalues are 2s, s(1+s), 1+s, p. Therefore

    mu=min(2s,s(1+s),1+s,p)>0,
    max_D F_e(D N) = (1+s)/2,

with K_0 the unique full-CPTP optimum. This is a genuinely rank-two nonunitary recovery, not a qubit Pauli-subsystem extractor (the receiver dimension is odd). The same receiver is optimal for every p in (0,1), and for convex mixtures of these objectives. A fixed unknown receiver-basis unitary U sends E_a to U E_a and rotates the optimal receiver to D_0 composed with Ad(U†); the physical acquisition task must learn this orientation, rather than having it supplied. Restricting p away from 0 and 1 gives a uniform strict gap. Finite stored latent control selecting p values can generate memory-correlated instances, but a common conditional optimizer is an explicit promise, not something this certificate establishes for unseen source states.

The fixture only partially corrects the logical dephasing: F_e<1 for p>0. It demonstrates recovery acquisition under drift, not a near-perfect memory threshold. Ordinary unflagged qubit amplitude damping is not substituted as a strict unique uniform-entanglement-fidelity oracle; the mixed-unitary/unital degeneracy obstructs that particular claim.

## 6. Comparison and remaining scientific obligation

The recovery SDP, dual bounds and extreme-channel characterization are established machinery. This note's elementary quantitative estimate and rank-normalize/dual-fit mechanism are author derivations pending review; no priority claim is made. Relevant primary references: M.-D. Choi, *Completely positive linear maps on complex matrices*, LAA 10 (1975), 285–290, DOI 10.1016/0024-3795(75)90075-0; J. Watrous, *The Theory of Quantum Information* (2018), Theorem 2.31, https://johnwatrous.com/wp-content/uploads/TQI.pdf (search located theorem; direct retrieval failed in this pass); Fletcher, Shor and Win recovery-optimization work already scoped in the existing Astra primary comparison. The proof above is self-contained and does not rely on an unread passage.

Consequential next obligation: replace generic process acquisition with a physically acquired sufficient statistic that identifies a broad useful common recovery class at favorable scaling, and show an advantage over an equally informed adaptive conventional channel-recovery SDP. This result supplies a nonunitary, all-CPTP unique-oracle robustness interface, not that scaling separation.
