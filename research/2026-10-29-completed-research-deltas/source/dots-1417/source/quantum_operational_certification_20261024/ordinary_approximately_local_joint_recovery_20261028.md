# Joint ordinary recovery from approximately local hidden generators

28 October 2026. **New constructive proof candidate, independent receiving in progress.** No new source samples. All received exact-locality sources, their receipts and the two completed pilots remain unchanged. This note relaxes exact physical support, not the supplied four-coordinate encoder family or the reset-source interface.

## 1. Contract and actual new conclusion

Import the physical source and full-reference conventions from `ordinary_joint_local_logical_swap_recovery_20261028.md` (SHA `f22c549bcb545387b4761ff31ec90886ff7b677c1d1f32a411b05e65024f89c0`) and the paid ordinary acquisition architecture from `ordinary_colored_pooled_joint_recovery_20261028.md` (SHA `d63c30417caee39cc16f8b80f44bb01ac25933c7cab647f33897a651bdd22c47`). In particular, a known n-qubit physical output register receives q-logical-qubit reset calls, with one unknown common U and

    E_x(omega)=U[sum_alpha P_alpha omega P_alpha^dagger tensor G_alpha(x)]U^dagger.

The positive gauge matrices are quadratic in the four real encoder coordinates, sum to a unit-trace gauge state G(x), and may be noncommuting, correlated, rank deficient or arbitrarily ill-conditioned. Let bar denote the uniform four-anchor average and put

    rho=U[(I/2^q) tensor Gbar]U^dagger,
    B_ji=U[sigma_ji tensor I_gauge]U^dagger, j=X,Z.

The B_ji are EXACT compatible global logical generators, but need not be physically local. Aggregate operator contrasts obey Hbar_ji>=kappa Gbar with0<kappa<=1. Thus the ordinary half-difference X_ji of the two signed input states, with all other logical inputs mixed, has

    X_ji=B_ji R_ji,  kappa rho<=R_ji<=rho,
    [R_ji,B_ki]=0 for all true logical generators.

The last commutation statement concerns R_ji, the gauge-only magnitude, not X_ji. The separate promise G_I(x)>=G_alpha(x) for EVERY global Pauli alpha and x remains necessary for the unrestricted full-CPTP noisy-source comparator. The coherent virtual recovery bound below does not itself require this dominance.

**New approximate-locality promise.** For each logical i there exists one unknown width-w physical interval I_i and local Hermitian reflections V_Xi,V_Zi supported there such that

    Tr rho(B_ji−V_ji)^2<=tau^2, j=X,Z,   0<=tau<=kappa/8.       (1)

Neither intervals nor reflections are supplied. No within-pair or cross-pair commutation is assumed for these local proxies. Tau is a supplied valid upper bound on a structural approximation error, not inferred from the learned fit or a holdout. The exact global compatible algebra and common gauge source are still substantive assumptions. Norms in(1) are state weighted; no gauge eigenvalue floor or full operator-norm approximation is required.

We construct an ACTUAL local controlled-reflection receiver and ordinary acquisition whose virtual joint Bell loss and oracle regret have explicit approximation floors. With

    W=min(n,3w−2), C=min(q,4W−2),
    S=W+2(C−1)(W−1), K=min(q,2S), A=min(q,K^2),
    eta=epsilon/(16384 q A),                              (2)

the good-history receiver satisfies

    ell0_joint<=1980 q A tau^2/kappa+(225/2)q A eta,
    sup_x[ell(D E_x)−ell_star(x)]
           <=7920 q A tau^2/kappa+450q A eta.             (3)

At fixed w the coefficient A is bounded uniformly in q; the displayed min formulas may still vary for small q. The joint conclusion retains all Bell references and arbitrary correlated gauges; it is not an aggregation of separately deployed marginal decoder fidelities. A final global ordinary encoder learner gives expected one-payload loss

    <=(1+gamma)ell_star+epsilon
                    +(1+gamma)7920 q A tau^2/kappa,       (4)

for integers1<=q<=n and1<=w<=n,0<epsilon<=1 and0<gamma<=1, under the same finite confidence/control ledger. The right side may always be clipped at1. Thus useful small joint error requires a sufficiently small aggregate tail; no fixed nonzero per-logical tail yields error independent of q.

## 2. Coarse overlap localization survives weighted tails

Fix i and write X=X_Xi=B_Xi R, V=V_Zi, B=B_Zi. The true algebra gives B X B=−X. If a tested physical interval J is disjoint from I_i, the partial trace onto J is invariant under conjugation by V. Therefore

    2||X^J||_1<=||VXV−BXB||_1<=2tau,
    hence ||X^J||_1<=tau.                                 (5)

For clarity, split the difference as(V−B)XV+BX(V−B). Each trace norm is at most tau by Cauchy–Schwarz in the positive weight R: R commutes with the true B_Xi and B_Zi, R<=rho, Tr R<=1, and Tr R(V−B)^2<=tau^2. No lower bound on R's eigenvalues is used. The physical support of the TRUE B is irrelevant to this estimate; the proxy V is the operator traced out.

On the true proxy interval I_i, test X^I_i with V_Xi. Weighted Cauchy–Schwarz gives

    ||X^I_i||_1>=Tr R−|Tr(V_Xi−B_Xi)B_Xi R|
                  >=kappa−tau.                          (6)

Use the same physical coarse Bures banks and trace-norm scoring as the received exact-local construction: density root deficit m0=kappa^2/512 gives half-difference trace error<=kappa/8, and certified numerical score error<=kappa/16. Under(1), the true proxy interval has score at least11kappa/16, whereas every disjoint interval has score at most5kappa/16. Threshold kappa/2 therefore finds an interval J_i OVERLAPPING I_i on the simultaneous coarse good event. This is only overlap localization, not identification of the proxy or actual exact B support.

Expand J_i by w−1 sites each side and clip at boundaries. The known envelope W_i has width at most W, contains I_i, and contains every width-w candidate that overlaps J_i. The candidate count remains R_max=min(n−w+1,2w−1). Coarse failure histories remain physical and charged, not postselected away.

## 3. Robust logical packing without exact physical algebras

Exact local matrix-algebra packing cannot be reused when the true B_i are nonlocal. The following information bound replaces it.

### 3.1 A local proxy decoder exists

Use the literal local two-reflection isometry

    V_i' psi=|0> P_Zi' psi+|1> V_Xi(I−P_Zi')psi,
    P_Zi'=(I+V_Zi)/2.

It is an isometry even if the proxy reflections fail to anticommute. Compare with the mathematically ideal global extraction under the virtual channel omega -> U(omega tensor Gbar)U^dagger, keeping every reference and gauge purifier. The received weighted extraction argument requires only true Pauli relations and[rho,B_ji]=0, not locality of B_ji. It gives

    ell0_i(D_i^0)<=2delta_Xi+(3/4)delta_Zi
                         <=eta0:=11tau^2/4.              (7)

This D_i^0 is a proof-only feasible local comparator, never supplied to the learner and never sequentially applied to all logical qubits.

### 3.2 Information packing proof

Suppose s proxy pairs have their supports contained in one L-qubit physical interval J. Apply the global virtual channel to q halves of Bell pairs; their reference marginal is exactly the PRODUCT I_R/2^q. Each local decoder D_i^0 on J produces a qubit A_i with Bell failure at most eta0. These individual data-processing arguments are on the SAME premeasurement state; there is no assertion that all D_i^0 can be run simultaneously or that J can be cloned.

Let f(u)=h2(u)+u log2 3. Pinching onto the Bell line and its three-dimensional orthogonal complement shows S(R_i A_i)<=f(eta0) for eta0<=3/4. Araki–Lieb and S(R_i)=1 imply S(A_i)>=1−f(eta0), hence

    I(R_i:J)>=I(R_i:A_i)>=2−2f(eta0).

For product references, strong subadditivity/chain rule gives sum_i I(R_i:J)<=I(R_1...R_s:J). The latter is at most2 log2 dim J=2L. Consequently

    s[1−f(eta0)]<=L.                                    (8)

The coarse tail assumption already makes this nonvacuous: eta0<=11/256. Using h2(u)<=u log2(e/u), e<3 and monotonicity of f on[0,3/4], f(eta0)<11/32<1/2. Thus s<=2L is a valid simple integer bound; an additional entropy promise is unnecessary.

A stronger optional packing certificate uses only the X proxies. In the proof-only uniformly random logical X-bit ensemble with other logicals mixed and gauge Gbar, measuring local V_Xi predicts its bit with average error delta_Xi/4<=tau^2/4. Conditional-entropy subadditivity, classical Fano and the Holevo dimension bound yield s[1−h2(tau^2/4)]<=L. This is not an acquired ensemble or an additional control resource. We use the conservative s<=2L throughout so no improved entropy constant is hidden in the schedule.

### 3.3 Observable schedule guard

All width-at-most-W envelopes covering one site lie inside an interval of at most2W−1 sites. On coarse success their proxy supports lie there, so(8) bounds point overlap by2(2W−1). Use a left-endpoint sweep/optimal interval coloring. If the observed number of colors exceeds C from(2), terminate with a prescribed physical replacement receiver and predetermined encoder. On the promised simultaneous good event this guard never triggers. Passing it does not certify family membership or tau.

Execute complete learned SWAP blocks in this new color order. Their actual local envelopes and private ancilla leaves are exactly known. A graph edge j->k joins intersecting envelopes in increasing color order. Every ancestor or descendant family lies in a physical span of at most S sites; robust packing bounds its cardinality by K. The factors2 in C and K are paid consequences of approximate rather than exact local packing. The old global-hybrid bound also remains valid, giving A=min(q,K^2).

## 4. Fine CPTP learning against a feasible approximate comparator

Import the finite local Bures instruments, exactly feasible rational Choi SDP/repair and actual spectrum-valued tournament from the received mixed-gauge sources. Do NOT pretend that the exact ideal global decoder is a feasible local SDP point.

For a local CPTP D define calibration excess r(D)=g(D)−g_* and virtual marginal Bell loss ell0_i(D). The exact global source contrast still proves for EVERY physical D

    (kappa/2)ell0_i(D)<=r(D)<=ell0_i(D).                  (9)

On the true proxy interval, use D0 from(7), with r0=r(D0)<=11tau^2/4. Let D be the empirical local optimizer to error zeta, four root deficits at most m, and H_j=D^dagger sigma_j−D0^dagger sigma_j. Each H_j is a Hermitian contraction difference of norm at most2. The pointwise Uhlmann inequality applies even though D depends on the estimates. Its four-state second-moment sum obeys

    sum_(j,s)Tr r_(j,s)H_j^2
           <=32[ell0_i(D)+ell0_i(D0)]<=64(r+r0)/kappa.

Therefore empirical optimality gives

    r<=r0+zeta+4sqrt[2m(r+r0)/kappa]+2m.

Young's inequality with(r+r0)/3 yields

    r<=2r0+39m/kappa+(3/2)zeta
      <=2r0+40m/kappa+2zeta.                             (10)

For zeta<=m this is at most2r0+42m/kappa. The approximation floor is an actual comparator term, not a raw calibration-noise floor or an asserted local sign gap.

Choose

    m=kappa^2 eta/512, zeta<=m,
    h=ceil(log2 R_max), t=kappa eta/(4h^2),
    L_T=log[2q(R_max−1)/beta_T],
    N_pair=ceil[2048h^2 L_T/(kappa^2 eta)],
    xi<=kappa t/4096.                                   (11)

For R_max=1 omit every h,t,L_T,N_pair formula and comparison call. The inherited actual-observable tournament remains valid with nonzero r_min and gives

    r_selected<=2r_min+t h^2
                <=11tau^2+(53/128)kappa eta,
    ell0_i(D_selected)<=22tau^2/kappa+(53/64)eta.         (12)

For R_max=1, the direct ERM bound is smaller than this displayed common bound.

Compute the selected channel's actual pullbacks A_ji. A certified Hermitian backward matrix C_ji with||C_ji−A_ji||<=sqrt(eta)/2 is sign-rounded into a physical local reflection B'_ji. The weighted sign inequality relative to the exact B_ji and the pointwise pullback bound a=Tr rho(A_ji−B_ji)^2<=4ell0_i give

    delta_ji=Tr rho(B_ji−B'_ji)^2
       <=4(sqrt(a)+sqrt(eta)/2)^2
       <=5a+5eta<=20ell0_i+5eta
       <=440tau^2/kappa+25eta.                           (13)

The last coefficient is conservatively rounded upward using53/64<1. Exact projector/reference-isometry definitions and finite controlled synthesis are the received ones; floating eigenspaces are not declared exact physical controls. Learned reflections need not obey Pauli or crosscommutation relations.

## 5. Actual local cones versus nonlocal ideal subsets

This is the essential repair to the exact-local proof. The TRUE ideal generators can be physically nonlocal, so it would be invalid to delete ideal outside-cone gates by physical support. Instead:

1. For output i, delete outside-cone blocks ONLY in the ACTUAL learned receiver's Heisenberg evolution of Phi_(R_i,A_i). This is exact because learned blocks have their declared known local net supports and private ancillas. Arbitrary gauge correlations do not affect the operator identity.
2. Compare this restricted actual circuit with the ideal complete logical SWAP blocks on the SAME retained index set. These proof-only ideal blocks may be physically nonlocal. In the unknown U frame they act only on their DISTINCT abstract logical factors and matching ancillas, so complete blocks commute. The subset contains i and therefore transfers its Bell half perfectly to A_i.
3. Every elementary ideal prefix of this subset preserves the physical-plus-all-ancilla reduced state rho tensor I_A/2^q. This follows from maximally mixed logical Bell halves and separately maximally mixed receiver ancillas, with the same gauge Gbar untouched. The full R, gauge purifier and ancilla purifiers are retained throughout the comparison. No actual learned prefix is asserted to preserve rho.

The elementary controlled-gate squared errors are delta_Zj/2,delta_Xj/2,delta_Zj/2. The restricted unitary hybrid gives

    p_i<=3|Anc(i)| sum_(j in Anc(i))e_j,
    e_j=delta_Zj+delta_Xj/2.

Both cone sizes and forward multiplicity are at most K. The commuting Bell-projector operator union then gives the actual joint-channel statement

    ell0_joint<=3A sum_j e_j.                            (14)

Substituting(13) yields(3). This argument does not claim the ideal nonlocal gates can be executed, nor does it infer full diamond closeness from joint Bell loss. The received optional discarded-key whole-logical Pauli twirl changes the service and retains its separate paid interface; the untwirled dimension-dependent diamond boundary is unchanged.

## 6. Pooled acquisition, finite cap and interpretation

Keep the received exact-fill antithetic fine pools: independent pairs of actual calls with q-sign vectors s and−s, independent anchors, and disjoint candidate registers inside disjoint known envelope colors. Each single sign estimator uses only its own routed bank/records; opposite-sign banks and different learners may remain correlated. The per-bank iid marginal plus union bounds is unchanged by approximate support. All estimates freeze before they are combined into ERM candidates. Fresh synchronized tournament batches use independent axes/signs per call, past-only contender adaptation and the real spectral difference observable. Do not condition a learner's marginal law on other CURRENT input labels or measurement records.

Put M=n−w+1,c=min(w,M),c1=min(w,R_max),m0=kappa^2/512. With the new m in(11), take

    N0=ceil[(80*4^w/m0)log(24*4^w*q*M/beta_L)],
    N_B=ceil[(80*4^w/m)log(48*4^w*q*R_max/beta_F)].       (15)

Choose strictly positive beta_L,beta_F,beta_T,beta_C with sum<=epsilon/8 and whole-process operational discrepancy0<=nu<=epsilon/8. The unused tournament allowance may simply be retained when R_max=1. The complete fixed upper cap is

    N_total<=2q cN0+4C c1 N_B
                   +C(R_max−1)N_pair+N_count+1.         (16)

Use zero comparison term when R_max=1. Every executed call, including failed/terminated histories, counts. The final+1 is one q-logical payload. After freezing this actual color-ordered receiver, the received paid global Clifford/stabilizer ordinary-input test learns the encoder from its genuine global Bell-risk scalar; product marginal tests are not substituted. N_count and the finite scalar-design controls are unchanged. Its relative comparison and bounded-loss exceptional events give(4).

At fixed w the fine/comparison block-call rate remains O_tilde(q/(kappa^2 epsilon)), with C,c1,A,R_max and4^w explicitly paid as in(15)–(16), and an additive tail floor in(4). There are qN_total input-qubit uses, nN_total output exposures, up to4qR_max collective state-estimator circuits, bank storage up to2N_B n qubits plus workspace, and their cross-copy routing. The payload circuit uses3q controlled reflections,4q Hadamards and q fresh mixed ancillas with restored physical routing. Abstract color depth is not physical hardware depth. The conventional learner with the same information and controls can implement this entire construction.

The supplied tau bound is not learned model validation. A known quantitative quasi-local tail bound from a physical generator class could imply(1); an empirical fit alone cannot. Width chosen to suppress that tail may depend on q and epsilon, in which case the displayed4^w cost must be substituted before claiming a scaling advantage. Arbitrary non-reset sources, unrestricted unknown encoders and unverified approximate-family membership remain outside this theorem.
