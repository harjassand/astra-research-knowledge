# Approximate-locality bridge: fine ERM, rounding and residual floor

Independent statistics derivation, 28 October 2026. Analytic, source-disabled review of the parent's proposed approximate-locality extension. This is a NEW audit, not a modification or retrospective extension of any received theorem or pilot. No source calls, count samples, simulations, private source reads, or source-manuscript edits were made. The full forthcoming approximate-locality manuscript, especially its acquired coarse locator, is NOT bound by this note.

## 1. Precisely needed interface

Let 0<kappa<=1, 0<epsilon,gamma<=1 and q>=1. The source still has its exact global compatible logical algebra B_(j,i), the shared rho commuting with every true B, the exact operator-relative X/Z margin, and the separately required global dominance condition. Exact locality of B is NOT assumed here. For a fixed logical index, a width-w patch admits an actual physical CPTP comparator D0, built from local proxy reflections with weighted errors at most tau^2 on each axis. The received literal extraction-isometry inequality gives

    ell0(D0)<=r_proxy:=11 tau^2/4,
    r0:=g(D0)-g_*<=ell0(D0)<=r_proxy.

For every actual physical decoder D, including globally interpreted local channels,

    (kappa/2)ell0(D)<=r(D):=g(D)-g_*<=ell0(D).

The ideal decoder giving g_* need not be local or feasible in the local ERM. Neither g_*, D0 nor the proxy reflections are provided to the learner. Four estimated ordinary local states have root-fidelity deficits at most m. The exactly feasible local CPTP ERM returns D with empirical objective at most that of D0 plus zeta>=0. Its rational Choi repair and finite numerical certificate are the received ones, not a floating nonphysical optimizer.

All statements below are pointwise on this simultaneous four-state fidelity event and therefore allow the ERM to depend on all four estimated states.

## 2. Uhlmann comparison against the feasible imperfect decoder

Put A_j=D^dagger(sigma_j), A0_j=D0^dagger(sigma_j), and H_j=A_j-A0_j. Both pullbacks are local Hermitian contractions, so ||H_j||<=2. For an individual true state r and its estimate hat r with root deficit at most m, choose Uhlmann purifications u,v with ||u-v||^2<=2m. Expanding the expectation difference around u gives

    |Tr H(r-hat r)|
      <=2 sqrt(2m Tr r H^2)+2m ||H||
      <=2 sqrt(2m Tr r H^2)+4m.                         (1)

This inequality holds for every H simultaneously once the fidelity event holds; choosing H from the same estimates causes no statistical independence problem. Both A and A0 are local, so (1) applies to the actual local density estimates even though the proof reference B is nonlocal.

Write a_(j,s)=Tr r_(j,s) H_j^2, with the local observable extended by identity when using global trace notation. Empirical optimality, the 1/8 normalization in the four-state calibration objective, and Cauchy--Schwarz give

    r <= r0+zeta+(1/8)sum_(j,s)[2sqrt(2m a_(j,s))+4m]
      <= r0+zeta+sqrt[(m/2)sum_(j,s)a_(j,s)]+2m.         (2)

Because r_(j,+)+r_(j,-)=2rho, weighted Hilbert--Schmidt triangle/Young bounds and the actual-channel qubit Bell inequality imply

    sum_(j,s)a_(j,s)
      =2 sum_j Tr rho(A_j-A0_j)^2
      <=4 sum_j [Tr rho(A_j-B_j)^2+Tr rho(A0_j-B_j)^2]
      <=32[ell0(D)+ell0(D0)]
      <=64(r+r0)/kappa.                                (3)

Here each axis obeys Tr rho(A_j-B_j)^2<=4ell0(D). This is a property of the actual CPTP logical channel, not an assertion that its fitted pullbacks are reflections or anticommute. Combining (2)--(3),

    r <= r0+zeta+4sqrt[2m(r+r0)/kappa]+2m.              (4)

For M=m/kappa, the exact scalar inequality

    4sqrt(2M s) <= s/3+24M

is the square (sqrt(s/3)-sqrt(24M))^2>=0. Setting s=r+r0 in (4) yields

    r <= 2r0+(3/2)zeta+36m/kappa+3m
      <= 2r0+39m/kappa+(3/2)zeta
      <= 2r0+40m/kappa+2zeta.                           (5)

Thus, with zeta<=m and kappa<=1, the convenient canonical bound is

    r_min <= 2r0+42m/kappa.                             (6)

No exact local ideal comparator, inverse gauge eigenvalue, statistical sample splitting inside ERM, or supplied local algebra is used. The older 3r0+36m/kappa+2zeta bound is also safe but is NOT the canonical budget below.

## 3. Canonical fine and tournament budgets

Let A>=1 be a valid deterministic colored-composition upper bound, and set

    eta=epsilon/(16384 q A),
    m=kappa^2 eta/512,  0<=zeta<=m.

For R_max>=2, use the received balanced tournament with

    h=ceil(log2 R_max),
    L=log[2q(R_max-1)/beta_T],
    t=kappa eta/(4h^2),
    N_pair=ceil[2048h^2 L/(kappa^2 eta)],
    xi<=kappa t/4096.

The physical comparison remains the spectrum-valued difference-observable measurement. It is not a binary +/-1 POVM, and it is not a difference of independently sampled decoder errors. The relative variance and conditional Bernstein proof refer to r against the exact global ideal calibration value g_*; they remain valid when that ideal decoder is not local. Contenders and controls are frozen within each fresh batch, and cross-learner outcomes can be correlated.

Using r_selected<=2r_min+t h^2 and r0<=11tau^2/4,

    r_selected <= 4r0+84m/kappa+t h^2
               <= 11tau^2+(53/128)kappa eta,
    ell0(D_selected) <= 22tau^2/kappa+(53/64)eta
                     <= 22tau^2/kappa+eta.              (7)

For R_max=1, do NOT instantiate h,t,L or N_pair. There are no comparisons. Directly from (6),

    ell0(D_selected)<=11tau^2/kappa+(21/128)eta,

which is bounded by (7). Empty/byes slots do not create source calls beyond the predeclared cap.

For at most 4qR_max individual fine state estimates, the unchanged marginal union bound permits

    N_B=ceil[(80*4^w/m)log(48*4^w q R_max/beta_F)].        (8)

With exact antithetic pairs, the raw fine cap is 4 C_max c1 N_B, c1=min(w,R_max). The accuracy parameter is half the received exact-local parameter, so its leading N_B factor doubles; no extra q factor is introduced by the local comparator residual.

## 4. Finite signs and the explicit generator floor

For A_j=D_selected^dagger(sigma_j),

    a_j:=Tr rho(A_j-B_j)^2<=4ell0(D_selected).

Use a known backward-diagonalized Hermitian C_j satisfying ||C_j-A_j||<=u, where u<=sqrt(eta)/2. Exact-reference signs can be represented by certified unitary/projector controls, with arbitrary kernel completion; no spectral gap or floating eigenvector exactness is assumed. A sufficiently small positive dyadic u can be specified by finite arithmetic. Gate compilation is charged to the whole-process operational error budget.

Since rho commutes with the true B_j, the received weighted sign lemma and weighted triangle inequality give

    delta_j:=Tr rho(B_j-sign C_j)^2
       <=4(sqrt(a_j)+u)^2
       <=5a_j+20u^2
       <=20ell0(D_selected)+5eta
       <=440tau^2/kappa+25eta.                          (9)

The middle scalar bound follows from (sqrt(a)+u)^2 <=(5/4)a+5u^2. It is stronger than folding everything into 25(22tau^2/kappa+eta). The fitted X/Z signs need not satisfy the Pauli algebra; the deployed controlled-reflection swap blocks remain unitary regardless.

## 5. Conditional joint composition and the learned-encoder comparator

If the actual known envelope geometry supplies the colored cone bound A=min(q,K^2), the same compatible TRUE global algebra and maximally mixed receiver ancillas yield

    ell0_joint <=3A sum_i(delta_Zi+delta_Xi/2)
       <=1980 qA tau^2/kappa+(225/2)qA eta.              (10)

There is a locality distinction worth preserving in the full theorem: with nonlocal true B, delete outside-cone blocks only in the ACTUAL local circuit's Heisenberg expression. Then compare that restricted actual circuit to the exact compatible ideal SUBSET containing the target index. Every such ideal subset recovers that target perfectly and every ideal prefix preserves rho tensor I_A/2^q. One must not assert that nonlocal ideal gates have the actual spatial cone. The full Bell-projector operator union bound, not an independence assumption about marginal fidelities, yields (10).

Under the separately stated global source dominance and G(x)<=4Gbar transfer,

    sup_x[ell(D E_x)-ell_star(x)]
       <=7920 qA tau^2/kappa+450qA eta
       =7920 qA tau^2/kappa+(225/8192)epsilon.            (11)

The approximation floor is real and does not shrink with additional samples. A useful near-oracle guarantee requires qA tau^2/kappa sufficiently small; no unconditional epsilon conclusion may hide this term.

After the colored joint receiver is frozen, use the unchanged fresh GLOBAL Clifford/stabilizer ordinary-input design, whose Bernoulli mean is [2^q/(2^q+1)] times the ACTUAL global Bell loss. Known entanglement within the q-input block, joint inverse-Clifford readout, and all controls are still paid. Scalar tolerance epsilon/8 gives Bell additive tolerance at most epsilon/4. The learned-encoder approximation compares against the optimum of this fixed acquired decoder, so its factor (1+gamma) multiplies the entire decoder floor. With the received total statistical beta<=epsilon/8, whole-process nu<=epsilon/8, and gamma<=1,

    E ell_final <= (1+gamma) ell_star
          +(1+gamma)7920 qA tau^2/kappa
          +(1/2+225/4096)epsilon
       <= (1+gamma)ell_star
          +(1+gamma)7920 qA tau^2/kappa+3epsilon/5.        (12)

Consequently the looser +epsilon is safe. The factor (1+gamma) on the approximation floor cannot be dropped merely because (11) is uniform in the encoder. Bad histories stay physical and all executed calls are charged; no postselection or conditioning on successful retained records is permitted.

## 6. Geometry and acquisition interfaces that remain distinct

The exact-local dimension packing proof cannot simply be reused after replacing exact local generators by approximate proxies. A sufficient replacement follows from a single-axis quantum random-access argument. If s compatible logical bits each admit a local Z-proxy within the same L-site physical union and weighted error <=tau^2, encode uniform virtual logical Z bits and the same mixed gauge. Measuring each bit's proxy recovers it with average error p_i<=tau^2/4. The L-qubit register Q has

    L >= I(X:Q) >= sum_i I(X_i:Q)
      >= sum_i[1-h2(p_i)] >= s[1-h2(tau^2/4)].

The middle inequality uses independence of the classical input bits and strong subadditivity; each final bound uses data processing and binary Fano. It does not require joint proxy measurements or independent measurement errors. For tau<=kappa/8<=1/8, h2(tau^2/4)<1/2, hence s<=2L. This proves the sufficient envelope parameters

    W=min(n,3w-2),
    C_max=min(q,4W-2),
    span=W+2(C_max-1)(W-1),
    K=min(q,2span),  A=min(q,K^2),

PROVIDED the coarse good event really makes every known envelope contain the relevant proxy patch. The observable color-count fallback is still required on bad histories. At fixed w these geometry bounds are independent of q. The coarse approximate-local locator and its source budget are a separate acquisition proof, not supplied by the fine-ERM calculation here.

Conditional on any valid pre-pool coarse history, exact antithetic routing gives each individual sign bank the required iid local marginal. Plus/minus banks and distinct learners may be correlated. Fixed separate state-estimator instruments use only their own bank/routing labels/internal outcomes until every estimate is frozen; union bounds require no joint product law. Approximate locality changes none of this marginal argument. The comparison pools still use fresh independent per-call axis/sign labels, not antithetic pairs.

Thus, conditional on valid coarse acquisition, the complete cap retains the form

    N_coarse +4 C_max c1 N_B
       +C_max(R_max-1)N_pair+N_count+1,

with a zero comparison term for R_max=1 and one final payload. At fixed w, fine block calls scale O_tilde(qA/(kappa^2 epsilon)); full qubit traffic, local estimator instances, collective memory and controls do not become free. This is available equally to the strongest conventional learner with the same source access. It is not a new count-acquired experiment or a hardware claim.

## Review result

PASS for the feasible-comparator fine-ERM extension, canonical tournament and sign constants, explicit joint/encoder residual floor, and pooled-statistics interface under the stated exact global-source and valid-envelope contracts. The acquired coarse approximate-locality theorem is explicitly outside this note's binding scope. Prior received sources and pilots remain immutable.
