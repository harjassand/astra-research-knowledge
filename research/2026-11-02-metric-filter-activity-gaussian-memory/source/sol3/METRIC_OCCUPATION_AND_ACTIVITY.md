# A Gaussian Lyapunov lift beyond common loss

Author-derived stage-three construction, prompted by the accepted N1511/N1512 sources. Their common-loss occupation/activity/scheduling results are prior premises at their actual scope. This argument does not import their source oracle or assume that common loss applies to a rank-deficient matrix. The stage-two construction and both frozen returns are unchanged.

## 1. Input and certificate

Retain the stage-two input

    A=-iH-EE^dagger/2,
    L_mu=e_mu^dagger b,
    V=sum_j Q_j[a(c_j)+a(c_j)^dagger],
    a(c)=c b,

where the Q_j are bounded Hermitian system operators, with actual supplied block normalizations q_j. The joint system may be noncommuting and reference-entangled. The retained bath is initially vacuum. Prescribed system-only instruments and their unconditional records remain allowed.

Acquire an explicit positive Hermitian one-particle matrix P and a number gamma>0 such that

    P>=I,             A^dagger P+PA <= -gamma P.             (1)

This is an additional **checked small-matrix certificate**, not an assumed occupation theorem. Its entries, finite arithmetic, inequality slack and any conditioning are charged. Define

    a_P=sum_j q_j ||c_j P^(1/2)||,
    a_inv=sum_j q_j ||c_j P^(-1/2)||,
    mu=4 a_P^2/gamma^2,
    Lambda=4 a_P a_inv/gamma.                              (2)

These may be unfavorable and remain explicit in the cost. A Hurwitz matrix has a positive Lyapunov solution, but merely invoking that fact does not supply bounded mu or Lambda. Exact dark modes do not satisfy (1). The general stage-two theorem remains applicable without (1).

The key point is that EE^dagger itself need not be positive definite. Hamiltonian mixing can make (1) hold with bounded P and gamma even when loss has rank one and its largest rate diverges.

## 2. Gaussian observable and free counted identity

For a positive one-particle matrix R let Gamma(R) be its bosonic second quantization, on the finite global number cutoff N<=K. It is a positive observable; it is used only in the proof. No quantum implementation or preparation of Gamma(R) is needed.

Let Phi_(0,eta,t) be the free passive evolution with every actual emission weighted by eta>0. Its adjoint satisfies

    Phi_(0,eta,t)^dagger[Gamma(R)]
      =Gamma[eta I+F(t)^dagger(R-eta I)F(t)],
    F(t)=exp(At).                                         (3)

One derivation uses the free passive one-particle isometry into retained modes and vacuum output, weighting each lost photon by eta. Second quantization factors the n-particle weight. This is an identity for a single **observable** and physical total count, not an interval-dependent output-field dilation substituted into coherent Dyson words. On N<=K the free process only lowers number, so the identity is exact on the entire intended subspace. It can also be checked by differentiating its finite adjoint master equation.

Gamma is order preserving on positive matrices: tensor products are order preserving in every factor, and restriction to the symmetric n-particle subspace preserves the inequality. Consequently (1) and (3) imply, for R=eta I+sP with s>0,

    Gamma(R)^(-1/2) L_(0,eta)^dagger[Gamma(R)] Gamma(R)^(-1/2)
      <=-gamma s D_R,
    D_R=dGamma(P R^(-1)).                                 (4)

To see this without incorrectly commuting P with A, differentiate Gamma at R. Its Frechet derivative preserves the order of the direction. The one-particle direction is s(A^dagger P+PA)<=-gamma sP. Only the bounding direction P commutes with R, which gives the right-hand side of (4).

## 3. Bounded system forcing in this metric

Conjugating the interaction commutator gives exactly

    Gamma(R)^(-1/2) i[V,Gamma(R)] Gamma(R)^(-1/2)
       =i(B_R-B_R^dagger),
    B_R=sum_j Q_j a[c_j(R-I)R^(-1/2)].                     (5)

This uses the annihilation intertwining identity, not a simultaneous diagonalization of A and P. Global number cutoffs commute with Gamma(R), so the same relations hold for the truncated raising/lowering maps; no cutoff canonical commutator is used.

Put eta=1+d, d>=0, and R=eta I+sP. Then

    B_R^dagger B_R <=(d a_inv+s a_P)^2 D_R.                (6)

Indeed factor each row as

    c_j(dI+sP)R^(-1/2)
     =[d c_j P^(-1/2)+s c_j P^(1/2)] P^(1/2)R^(-1/2).

A normalized linear annihilator is bounded by the square root of its associated number quadratic form. Apply the triangle inequality over actual Q_j block normalizations. This proves (6), including noncommuting system Q_j.

For any vector, Cauchy--Schwarz and Young give

    +/- i(B_R-B_R^dagger)
       <= gamma s D_R+(d a_inv+s a_P)^2/(gamma s) I.        (7)

Equations (4)-(7) are finite operator inequalities on all system/bath/reference inputs.

## 4. Uniform occupation bound, earned without a direct loss gap

Set eta=1, s=z-1>0, R_z=I+(z-1)P, and

    M(t,z)=Tr[Gamma(R_z)rho(t)].

Keep half of the negative term in (4) and apply (7) with half its coefficient. Since

    Gamma(R_z)^(-1/2) partial_z Gamma(R_z) Gamma(R_z)^(-1/2)
      =dGamma(P R_z^(-1)),

we obtain the scalar transport inequality

    partial_t M <=-(gamma/2)(z-1) partial_z M
                  +(2a_P^2/gamma)(z-1)M.                 (8)

Along the characteristic z(u)=1+(z-1)exp[-gamma(t-u)/2], vacuum has M(0,z(0))=1. Thus

    M(t,z)<=exp{mu(z-1)[1-exp(-gamma t/2)]}
           <=exp[mu(z-1)].                               (9)

This is uniform in K and time. P>=I implies R_z>=zI and Gamma(R_z)>=z^N, so

    E z^N(t)<=exp[mu(z-1)] .                              (10)

System-only instruments preserve Gamma(R_z) exactly when averaged with their retained records; (8)-(10) compose through every prescribed control. No rare outcome is normalized. This does not assert that the interacting state is Gaussian.

At z=2, P(N>=K)<=exp(mu)2^(-K). The same boundary-Hamiltonian Duhamel argument as stage one therefore gives complete vacuum-channel cutoff error

    error_K <= 2aT sqrt(K+1) exp(mu/2) 2^(-K/2),
    a=sum_j q_j||c_j||.                                  (11)

An integer K=O(1+mu+log[(1+aT)/epsilon]) suffices, with a fixed enlargement absorbing log(K+1). Finite-to-finite cutoff comparison first proves the canonical controlled limit. No arbitrary unbounded-GKSL uniqueness is asserted.

## 5. Actual emitted-count MGF with linear horizon

Let C count **actual** physical emissions. For theta>0 set d=exp(theta)-1 and choose

    s=d a_inv/a_P,
    R_theta=exp(theta)I+sP.                               (12)

If a_P=0 then V=0 and the vacuum process emits nothing; handle that case directly. Otherwise a_inv>0. Equations (4)-(7) imply

    L_theta^dagger[Gamma(R_theta)]
      <= Lambda[exp(theta)-1] Gamma(R_theta).             (13)

Here L_theta is the actual count-tilted generator, with eta=exp(theta) multiplying the jump term. Vacuum weight is one. Positivity and Gronwall, with system instruments inserted, give

    E[exp(theta C) Gamma(R_theta)]
       <=exp{Lambda T[exp(theta)-1]}.

Since R_theta>=I, discarding its positive bath weight yields

    E exp(theta C)<=exp{Lambda T[exp(theta)-1]}.            (14)

This proves the **actual** count cap Jmax=O(Lambda T+log(1/epsilon)). Unlike the invalid transfer identified in the Dots uniform-occupation source, no normalized-state log-convexity is applied to a tilted state. The unnormalized tilted process is controlled by an explicit positive observable and operator inequality.

For P=I, A=-2lambda I-iH with H commuting with N, gamma=4lambda, and a_P=a_inv=a, (2) gives mu=a^2/(4lambda^2) and Lambda=a^2/lambda: the common-loss occupation/activity scales already earned by N1511/N1512. This is a consistency check and credit boundary, not a claim to originate their scales. The Gaussian lift permits noncommuting unequal and rank-deficient loss.

## 6. Complete scheduling consequence using the acquired stage-two source

Use the already constructed forward contraction/loss-clock source, with actual no-jump and jump blocks, finite prefix CDFs and A0=O(sqrt(1+KM)). It is author-derived and still awaits independent whole review; the new metric theorem does not independently validate it.

Choose windows tau<=1/v, v=1+h+2a sqrt(K+1), and keep the private actual emission record after complete amplification. Equations (11) and (14) replace the stage-two quadratic horizon budgets. The deterministic number of calls is

    S=O(vT+p+Lambda T+log(1/epsilon)).                     (15)

Each free Gaussian block has actual gate cost O~(M^2 K) plus paid polynomial small-matrix arithmetic; its cost does not grow as a positive power of duration or passive norm R. The inner Dyson order and clock bits grow logarithmically with S and inverse error. Thus

    G=O(S sqrt(1+KM) {q[O~(M^2 K)+C_D]
                       +poly(M,r,B,input bits)}),
    B=polylog(M,K,R,v,T,S,1/epsilon).                     (16)

When mu, Lambda, h, a and the metric conditioning are bounded independently of T and passive stiffness, (11) makes K logarithmic in T/epsilon and (15)-(16) are near-linear in horizon after explicit mode/input and logarithmic factors. Actual system-access precision costs remain paid. This removes the T^2 occupation and emitted-count bottlenecks in the old coarse bound for this **certified subclass**, not for every passive bath.

The Dots bounded-duration accounting is credited as prior scheduling insight. Its occupation and immigration source are not assumed here. If one additionally places an ordinary supplied number-preserving Hamiltonian inside a source word, its actual binary duration circuit must be summed exactly as N1512 does; a realized path-time identity alone is insufficient. The present Gaussian blocks already have their explicit finite-matrix/rotation implementation, so (16) does not need a hidden free-Hamiltonian oracle.

## 7. Explicit rank-one-loss family with uniformly favorable certificate

For R>=4 take the stage-two family

    A_R=[[0,sqrt(R)],[-sqrt(R),-R]],
    E_R=(0,sqrt(2R))^T,
    P_R=3[[1,1/(2sqrt(R))],[1/(2sqrt(R)),1/2]],
    gamma=1/2.                                          (17)

The eigenvalues of P_R lie in a fixed interval contained in (1,4), independent of R. Direct multiplication gives

    A_R^dagger P_R+P_R A_R=3 diag(-1,1-R).

The matrix `-gamma P_R-(A_R^dagger P_R+P_R A_R)` is positive for all R>=4: its first diagonal is 3/2, the second is `3R-15/4`, and its determinant is positive already at R=4 and increases thereafter. Thus (1) is an analytic certificate, not a numerical optimization promise.

For c=(.12,.08i), a_P^2=.0528 and mu=.8448. Also

    a_inv^2=.0136/[3(1/2-1/(4R))],

so Lambda is bounded independently of R. The free bath keeps a slow eigenvalue tending to -1 while its other rate grows with R; direct loss remains rank one. This family earns both the new cutoff/activity theorem and the actual coupled source. It is not a practical speedup benchmark: ordinary slow-mode reduction and dense small-system evolution remain strong competitors.

## 8. Genuine limits

An exact dark undamped mode driven by a fixed Q eigenvalue forms a coherent state with mean occupation a^2T^2. It rules out a universal time-uniform occupation theorem under the unrestricted stage-two hypotheses. A favorable Lyapunov certificate is substantive. If gamma shrinks or P becomes unfavorable as a bath fit is refined, mu and Lambda must be paid. In particular, no bounded-metric conclusion for the gapless first-stage continuum hierarchy follows from this theorem without its own certificate and resource analysis.

The new near-linear certified subclass is a constructive mathematical extension. Historical priority, independent whole-proof acceptance and a full-resource advantage over every alternative bath representation are not established.
