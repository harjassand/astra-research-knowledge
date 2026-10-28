# Ordinary acquisition of a hidden common logical algebra

28 October 2026. **Author construction; independent mathematical and source-disabled checks completed in the companion receipt.** This is a concrete floor-free mixed-spectator subfamily, not a generic unflagged-source theorem. The output algebra is unknown and actually learned. No environment, source inverse, supplied output flag, protected reference, output eigenvalue floor, or free cross-frame alignment is used.

## 1. Physical family and comparator

The source is independently reset/memoryless between calls, as in the received programme contract; arbitrary inter-call source memory is not covered. Controls are trusted up to the single whole-process implementation budget below. The encoder is a supplied linear isometry V_x, x in the real unit sphere S^3. The unknown fixed source induces

    E_x(w) = E_0(Lambda_x(w)),
    E_0(w) = U(w tensor sigma)U^dagger.                      (1)

Here sigma is an arbitrary unknown gauge density matrix, with arbitrarily small or zero eigenvalues, and U is an unknown isometry into a known finite physical output space of dimension d. The channel Lambda_x is a unital Pauli channel in the *known input* Pauli coordinates:

    Lambda_x(sigma_j) = lambda_j(x) sigma_j,
    lambda_j(x) = x^T A_j x >= 0,  j=X,Y,Z.                 (2)

The three real quadratic forms are unknown; all Lambda_x must be CPTP. Neither U nor its Pauli observables nor sigma is supplied. All encoder choices share this unknown logical subsystem. This is a substantive restriction for Sections 1-7: output logical rotations changing with x, negative contractions, and x-dependent correlated gauge noise are not covered there. Sections 8-9 extend the last restriction under explicit common-algebra and contrast hypotheses.

A physical realization is V_x|psi> = sum_(a=1)^4 x_a |a> tensor |psi>. The fixed source measures its selector in an unknown real orthonormal basis {v_a}, applies unknown positive-contraction Pauli channel Lambda_a to the logical system, appends sigma, and applies U. The selector result is discarded, NOT output as a flag. Thus lambda_j(x)=sum_a (v_a^T x)^2 lambda_(ja). Taking one Lambda_a to be identity and the other three to be completely depolarizing gives a genuinely unknown unique perfect encoder, with perfect mixed-gauge output at that encoder. The good selector is not given or measured by the receiver.

The strongest comparator is the best x and **any full CPTP decoder**, with precisely the same source/control information as the learner. For a positive-contraction Pauli channel the identity Pauli probability

    p_0(x) = [1+lambda_X(x)+lambda_Y(x)+lambda_Z(x)]/4

is the largest Pauli probability. Pauli twirling of any proposed decoder leaves its Bell fidelity unchanged against Lambda_x; the twirled decoder is a Pauli channel, whose success is a convex combination of the p_alpha. Therefore

    ell_*(x) = 1-p_0(x),                                    (3)

attained by tracing out sigma after U^dagger. Tensoring a fixed state and applying U cannot improve on this full-CPTP optimum: every decoder after E_0 is itself a feasible qubit decoder. The same unknown decoder is optimal for every x.

The source is not presumed to be in this family merely because finite data fit it. The theorem is conditional on this structural promise; it is not a universal certificate of that promise.

## 2. One ordinary calibration mixture exposes two signs

Choose each of the four known encoder anchors e_a uniformly and discard the choice label. For each of the four logical pure inputs P_(X,+), P_(X,-), P_(Z,+), P_(Z,-), this produces an actual ordinary output bank from

    E_bar = (1/4) sum_a E_(e_a) = E_0 Lambda_bar,
    lambda_bar_j = Tr(A_j)/4.

Let rho=E_0(I/2), and B_j=U(sigma_j tensor I)U^dagger on its occupied support, completed as reflections off that support. Then

    rho_(j,+/-) = (I +/- lambda_bar_j B_j) rho,
    [B_j,rho]=0.                                           (4)

Assume lambda_bar_X,lambda_bar_Z >= kappa>0. This is a **logical visibility/contrast promise, not a gauge eigenvalue floor**. Crucially, if this family contains a perfect encoder, kappa=1/4 follows automatically: each A_j is positive semidefinite and some unit x_* has x_*^T A_j x_*=1, so Tr A_j>=1. No contrast parameter is additionally supplied for this zero-optimum corollary. More generally, a supplied useful-optimum promise ell_*<=c<1/4 gives kappa=(1-4c)/4, since every lambda_j(x_*)>=1-4c.

Use the received finite Bures density estimator on the four real banks, in one known physical basis or one actually paid common retained output frame. Obtain arbitrary density estimates tau_(j,+/-) with root-fidelity deficits m_(j,+/-). They need not fit the family, share a gauge, commute, or form a channel. No inverse of rho is taken.

Define, entirely classically in that *same* physical frame,

    A'_j = sqrt(tau_(j,+)) - sqrt(tau_(j,-)),
    B'_j = sign A'_j,                                      (5)

with any reflection completion on its kernel. These are learned signs. The following polar-perturbation proof uses these square roots. Section 9 supplies a different, stronger raw-pair-sign proof; no universal necessity of square roots is claimed.

## 3. Weighted sign stability without an eigenvalue floor

Write a_j=sqrt(1+lambda_bar_j)-sqrt(1-lambda_bar_j). Then

    A_j^true := sqrt(rho_(j,+))-sqrt(rho_(j,-))
              = a_j B_j sqrt(rho),
    a_j^2 = 2[1-sqrt(1-lambda_bar_j^2)] >= kappa^2.          (6)

**Spectral lemma.** For Hermitian A,C and reflection signs B=sign A, B'=sign C, with arbitrary signs on zero eigenspaces,

    ||(B-B')A||_F^2 <= 4||A-C||_F^2.                       (7)

In eigenbases of A,C, each matrix element on the left is
(sgn(a)-sgn(c))^2 a^2 times the squared basis overlap. It is zero for equal signs; for opposite signs it is at most 4(a-c)^2. Zero eigenvalues and either completion satisfy the same inequality. This proves (7), without dividing by an eigenvalue.

Because A_j^true=a_j B_j sqrt(rho), its sign is B_j on occupied support. Also (B-B')^2 and B(B-B')^2B have equal rho expectation when [B,rho]=0. Consequently (7) gives

    delta_j := Tr rho(B_j-B'_j)^2
       <= (4/a_j^2)||A_j^true-A'_j||_F^2
       <= (8/kappa^2) sum_+/- ||sqrt(rho_j±)-sqrt(tau_j±)||_F^2
       <= (32/kappa^2) sum_+/- [1-f(rho_j±,tau_j±)].         (8)

The last step follows self-containedly from Schatten Holder with exponents (4,2,4):

    f(r,t)=||r^(1/4)[r^(1/4)t^(1/4)]t^(1/4)||_1
           <=||r^(1/4)||_4 ||r^(1/4)t^(1/4)||_2 ||t^(1/4)||_4
           =sqrt(Tr sqrt(r)sqrt(t)).

Thus ||sqrt(r)-sqrt(t)||_F^2=2-2Tr sqrt(r)sqrt(t)<=2(1-f^2)<=4(1-f). This is a squared-error/Bures estimate, not a trace-distance perturbation divided by a rare gauge eigenvalue. Tiny gauge weights contribute only their actual mass.

For finite arithmetic, after square roots and a certified eigensolve define C_j=Q_j diag(c_j)Q_j^dagger with Q_j unitary and TOTAL residual ||C_j-A'_j||_F<=zeta, including both square-root and eigensolver backward errors. Use B'_j=Q_j diag(sign c_j)Q_j^dagger as the ideal compiled reflection. Replacing A'_j by C_j in (7) gives the safe bound

    delta_j <= (64/kappa^2) sum_+/- m_j± + 8 zeta^2/kappa^2. (9)

No spectral gap is needed to classify tiny eigenvalues: an incorrect sign on a tiny eigenvalue is already covered by its residual. Approximate unitary synthesis is charged separately as a physical process error, not treated as an exact sign gate.

## 4. Two arbitrary learned reflections yield a real CPTP decoder

There is no nonconvex common-algebra fit and no need to assume B'_X,B'_Z exactly anticommute. Put X'=B'_X, Z'=B'_Z, P'±=(I±Z')/2 and implement

    V|psi> = |0> tensor P'+|psi> + |1> tensor X'P'-|psi>,
    D(Y) = Tr_old-output[V Y V^dagger].                     (10)

V^dagger V=I, so this is a CPTP receiver on every physical input. Coherently record the Z' reflection eigenvalue in one qubit and apply X' to the old output conditional on value 1. This is an actual local circuit, not a formal Petz inverse or three incompatible classifier tests.

Let V_0 be (10) built from the true X,Z. On E_0 it perfectly transfers the logical state to the new qubit and leaves U(|0> tensor gauge) in the discarded system. For any purification of the gauge, including an entangled Bell input, its squared vector difference from V is

    ||(V-V_0)sqrt(rho)||_F^2
       = ||(P'+-P+)sqrt(rho)||_F^2
         + ||(X'P'--XP-)sqrt(rho)||_F^2
       <= (3/4)delta_Z + 2 delta_X.                         (11)

Here the second term is split into X'(P'--P-) and (X'-X)P-; [P-,rho]=0 allows its last squared norm to be bounded by delta_X. The orthogonal-to-Bell projection annihilates the ideal V_0 vector. Therefore the *actual learned decoder* obeys

    ell(D E_0) <= (3/4)delta_Z + 2 delta_X.                 (12)

No environment is accessed in this argument. The purification is only a proof device.

For T=D E_0, its Bloch diagonal entries T_jj lie in [-1,1]. Since all lambda_j(x)>=0,

    ell(D E_x)-ell_*(x)
       = (1/4)sum_j lambda_j(x)[1-T_jj]
       <= (1/4)sum_j [1-T_jj] = ell(D E_0).                (13)

Thus this one genuinely learned decoder is uniformly near optimal over *all* encoders, not merely over the calibration anchors. This uniformity follows from the common physical algebra and Pauli positivity; it is not the invalid generic sup/average Bures shortcut.

## 5. Global encoder acquisition becomes a paid scalar quadratic task

Freeze the actual decoder D and its physical frame. At any selected x, choose one of six input Pauli eigenstates uniformly, query E_x, apply D, and test in that known input basis. Let Y be the error bit. The six-state identity yields

    q_D(x)=Pr(Y=1)=(2/3)ell(D E_x).                         (14)

This is a nonnegative quadratic x^T Q_D x in the four real encoder coordinates, with 0<=q_D<=1. Its ordinary Bernoulli variance is at most its mean. The received nonnegative active-design argument therefore applies with **10 quadratic features**, not an encoder-grid source multiplier.

For explicit conservative constants, take a finite chord-h net with h^2<=epsilon_q/4096 plus a fixed spanning quadratic set. Let L=40, S=56, t=gamma epsilon_q/16, J=ceil(log2(1/t)), tau_j=2^-j. Use the same clipped upper-envelope invariant q<=U<=2q+2tau, weighted G-optimal design, and covariance compression as the received quartic theorem, replacing its U-statistic by ordinary Bernoulli batch means. At each of at most S support encoders per stage use

    b = smallest odd integer >= 8 log(2 S J/beta_count),
    n_j = ceil(2^14 L/tau_j).

At radius sqrt(tau_j u_x)/(16 sqrt L), the conditional Chebyshev bad-batch probability is at most 1/64. Median amplification and weighted interpolation give the same 1/16 sqrt(tau_j u_z) global envelope error. The same finite rational rounding is valid. Final empirical minimization gives

    q_D(xhat) <= (1+gamma) min_x q_D(x)+epsilon_q,
    N_count <= S b[J+2^20 L/(gamma epsilon_q)].             (15)

The finite list has polynomial classical size, but only O(log(1/(gamma epsilon_q))) constant-size compressed designs receive source calls. All label bits, ordinary inputs, decoder invocations and source failures count. The main quartic receiving proof supplies the algebraic envelope induction; this specialization has the simpler directly verified variance bound.

## 6. A finite-budget theorem and physical ledger

Choose 0<gamma<=1, 0<epsilon<=1. In the four calibration banks require

    m_j± <= m = kappa^2 epsilon/8192,
    zeta^2 <= m.

Equations (9)-(12) then give ell(D E_0)<=374m/kappa^2<epsilon/20. Apply (15) at epsilon_q=epsilon/6, so its Bell-risk additive error is epsilon/4. On the joint statistical good event,

    ell(D E_xhat) <= (1+gamma)ell_* + 7epsilon/20,           (16)

where ell_*=min_x ell_*(x), with ample rounding slack.

Use the received finite Bures estimator from `ordinary_bures_matrix_query_confidence_20261027.md` Section 2 and its `direct_cptp_bures_bridge_20261027/DIRECT_CPTP_BURES_RISK_RECOVERY.md` primitive, with dimension and rank upper bound both d. Its explicit deterministic copy cap is

    D_0=2^ceil(log2(d^2)),
    N_B(d,m,beta_B)=ceil[(80D_0/m) log(12D_0/beta_B)].

This is not an asymptotic oracle: its random-purification channel, finite-Clifford pure-state tomography, certified near-top eigenvector and partial trace, collective measurement/memory and finite arithmetic are imported and paid. Here m<=1/16, as required by that contract. With per-bank failure beta/8 and total count failure beta/2, a deterministic total source cap is

    N_total <= 4 N_B(d,kappa^2 epsilon/8192,beta/8)
               + 56 b[J+6*2^20*40/(gamma epsilon)],        (17)

where J=ceil(log2(96/(gamma epsilon))) and b is as above with beta_count=beta/2. Thus

    N_total = O_tilde(d^2/(kappa^2 epsilon)+1/(gamma epsilon)). (18)

The bound is a theorem composition, not a sampled full-cap run or a practical constant claim. A common output-support frame can replace the known physical basis only after paying its actual acquisition, retained programme and full future horizon. A rank-only replacement d->r is NOT established in this note by assuming that alignment.

Explicit physical resources: four ordinary mixed-anchor state banks; the collective receiver measurement/memory of N_B; same-frame matrix representation; square roots/eigendecompositions; two compiled arbitrary d-dimensional reflection controls; one decoder qubit plus the old d-dimensional output and synthesis workspace; all active-count decoder invocations; resets; encoder and Pauli preparation controls; the final retained frame through payload. There is no coherent encoder selector or reference sent through the source and no source inversion. In a known physical output basis, generic reflection synthesis is polynomial in d and requested precision, rather than the old special-purpose parity decoder.

Budget a single linked calibration/count/payload implementation discrepancy nu for the WHOLE adaptive process; closeness of classical transcripts alone is insufficient. Taking beta<=epsilon/8 and nu<=epsilon/8 gives an averaged Bell-risk statement <=(1+gamma)ell_*+epsilon after including failure and operation errors. Optionally a paid whole-logical Pauli twirl makes the final averaged logical channel Pauli, so its unhalved complete error is exactly twice its Bell loss; rescale epsilon accordingly. A payload and its decoder controls are additional to (17).

If an exact-correctable encoder exists, kappa=1/4 is automatic and the theorem gives additive epsilon at O_tilde(d^2/epsilon) ordinary source cost, with mixed or arbitrarily ill-conditioned spectators. The construction does not need to locate the perfect encoder before acquiring the decoder.

## 7. Conventional baseline and exact scope

This is **not a claimed asymptotic advantage over the strongest equally informed conventional learner**. Such a learner receives the same common-subsystem/positive-Pauli promise and can implement the same four-bank Bures/sign/extraction construction, or exploit that structure in ordinary process tomography. Comparing only against naive uniform trace-norm tomography at epsilon^-2 would be unfair. No historical priority is asserted for weighted polar perturbation, coherent two-reflection extraction, or fast Bures estimation.

There is also an important equally informed existing-programme baseline: for the fixed-sigma model, the received correctability quartic is

    D(x)=Tr(sigma^2) sum_j[1-lambda_j(x)^2]
         >=4 ell_*(x)/rank(sigma).

Thus the previous active-quartic construction already gives a zero-optimum rank-based route without a gauge eigenvalue floor in this restricted family. The zero-optimum scaling alone is NOT a separation or an otherwise unclosed case. Distinct value here is actual acquisition of a reusable common decoder and (1+gamma)-relative **nonzero-optimum** encoder selection. The quartic can misorder those encoders: lambda=(1,0,0) has Bell loss1/2 and squared-contraction sum1, whereas lambda=(2/5,2/5,2/5) has smaller loss9/20 but squared-contraction sum12/25. The quartic prefers the worse first endpoint in their selector-mixture family. With two anchors of each type, aggregate X/Z contractions are7/10 and1/5; the hidden-algebra construction applies with kappa=1/5.

What is concretely closed is a nontrivial strict-ordinary unflagged family: the hidden output logical basis and the good encoder are both unknown; mixed gauge modes can be arbitrarily rare; one actual common decoder is learned; the remaining encoder problem has a finite fast scalar design; and the comparator is unrestricted CPTP, not a frozen arbitrary frontend.

The general source mission remains open. If the logical algebra changes with x, calibration signs can still trap. If Pauli contractions change sign, one common receiver need not be optimal. For the original fixed-sigma theorem, gauge states correlated with encoder-dependent logical noise need not produce calibration mixtures of form (4); Section 9 handles an explicit noncommuting correlated-gauge extension by a different margin argument, not arbitrary correlations. The kappa dependence is an honest logical-visibility conditioning cost; it cannot be called a generic no-condition result. The automatic kappa=1/4 statement relies on the positive quadratic common-algebra family, not merely existence of a perfect encoder in an arbitrary source.


## 8. Extension: encoder-dependent, hidden commuting gauge noise

The same mechanism is not confined to a fixed spectator tensor factor. Consider the unknown physical family

    E_x(w)=U[sum_(g,alpha) w_(alpha,g)(x)
                 sigma_alpha w sigma_alpha tensor |g><g|]U^dagger,
    w_(alpha,g)(x)=x^T W_(alpha,g)x>=0,
    sum_(g,alpha) W_(alpha,g)=I_4.                         (19)

All W matrices, U, and the gauge basis are unknown. This is implemented by a fixed source POVM {W_(alpha,g)} on the four-dimensional selector, a conditional Pauli on the logical input, preparation of |g>, and U. The outcome is discarded. The output has orthogonal gauge sectors only in an UNKNOWN basis entangled with the logical system; a nondestructive gauge flag is not supplied. The learner never discovers or measures that sector label. Both gauge probabilities and logical error rates can vary with x.

Define nonnegative quadratic gauge masses and signed contractions

    p_g(x)=sum_alpha w_(alpha,g)(x),
    h_jg(x)=sum_alpha chi_(j,alpha) w_(alpha,g)(x),

where sigma_alpha sigma_j sigma_alpha=chi_(j,alpha)sigma_j. Require h_jg(x)>=0 for all j,g,x. Consequently 0<=h_jg<=p_g and the identity Pauli is optimal separately in every gauge block. A full decoder has no cross-block coherence to exploit, so

    ell_*(x)=1-sum_g w_(I,g)(x)
             =[3-sum_(j,g) h_jg(x)]/4.                    (20)

The ideal common U^dagger/discard-gauge receiver is again optimal for every x. The full-CPTP comparator is retained.

Use the same four-anchor mixture and write pbar_g=(1/4)sum_a p_g(e_a), hbar_jg similarly. Assume **aggregate logical visibility**

    hbar_Xg >= kappa pbar_g,
    hbar_Zg >= kappa pbar_g                                (21)

for each occupied g. This allows pbar_g to vanish or be arbitrarily small. It is NOT a minimum probability or eigenvalue promise. For example, (21) follows if within each gauge every occupied encoder branch has its X and Z contractions at least kappa; weaker aggregate cases also qualify. In this extension (21) does NOT follow merely from a perfect encoder.

Let rho_bar=U[I_2/2 tensor diag(pbar)]U^dagger. Ordinary calibration pairs have g blocks

    rho_bar,j± = U[sum_g (pbar_g I ± hbar_jg sigma_j)/2
                                 tensor |g><g|]U^dagger.

Their square-root difference A_j has sign B_j=U(sigma_j tensor I)U^dagger and

    A_j^2 >= kappa^2 rho_bar.                              (22)

Indeed, in each gauge block its squared coefficient is
pbar_g[1-sqrt(1-(hbar_jg/pbar_g)^2)], at least kappa^2 pbar_g/2. The sign and rho_bar commute. For the positive operator H=(B_j-B'_j)^2, (22), cyclicity and the spectral lemma give

    Tr rho_bar H <= kappa^-2 Tr A_j^2 H
                 <=4 kappa^-2 ||A_j-A'_j||_F^2.            (23)

Thus all sign and extraction bounds (8)-(12) hold with rho_bar and the mathematical target channel E_(0,bar)(w)=U[w tensor diag(pbar)]U^dagger. This target need NOT itself be an available source call. Actual input banks are the noisy ordinary mixtures, as specified.

Let ell_(D,g) be D's Bell loss on the perfect logical embedding in gauge g. Every ell_(D,g)>=0. For a fixed x, positivity of the within-gauge contractions gives

    ell(D E_x)-ell_*(x) <=sum_g p_g(x) ell_(D,g).            (24)

The real PSD matrix P_g=sum_alpha W_(alpha,g) satisfies

    p_g(x)=x^T P_g x <=Tr P_g=4 pbar_g.                    (25)

Therefore the actual uniform decoder regret is

    ell(D E_x)-ell_*(x) <=4 ell(D E_(0,bar)).               (26)

This is a legitimate structured uniform transfer, not a general sup/average Bures principle. It follows from positivity of the actual quadratic masses and a shared logical decoder. No hidden label is acquired or assumed measurable.

Run the four-bank algorithm with m=kappa^2 epsilon/32768 and zeta^2<=m, and the identical active-count stage with epsilon_q=epsilon/6. Then (26) is below epsilon/20, and (16)-(18) hold with that four-times smaller m. Thus the extended theorem still costs

    O_tilde(d^2/(kappa^2 epsilon)+1/(gamma epsilon))

ordinary source calls, and returns (1+gamma)-relative performance against all CPTP decoders for this broader model. Unknown arbitrarily rare gauge weights are handled by their mass, not divided out. Classical/quantum controls, common frame, finite horizon and conventional-comparator caveats remain exactly as above.

Noncommuting gauge operators are NOT covered by this extension: (22) used a common gauge diagonalization. Replacing it by a merely Loewner lower bound between noncommuting contrasts and marginals does not automatically permit squaring a Loewner inequality. The direct squaring route fails; Section 9 bypasses it with a different Bures-margin argument.

## 9. Stronger route: raw-sign Bures margin and noncommuting quantum gauges

The invalid Loewner-squaring shortcut at the end of Section 8 is not needed. A localized Bures-risk argument yields a stronger raw-sign result and genuinely noncommuting hidden gauge noise.

### 9.1 A relative binary margin gives fast sign acquisition

For ANY pair of density matrices r_+,r_-, put

    rho=(r_++r_-)/2,  X=(r_+-r_-)/2,  B=sign X.

Assume |X|>=kappa rho for 0<kappa<=1; in the application below B also commutes with rho. Let tau_± be arbitrary estimated states with m_±=1-f(r_±,tau_±), M=m_++m_-. Put Xhat=(tau_+-tau_-)/2. Compute a Hermitian C with total certified trace-norm residual ||C-Xhat||_1<=eta and use B'=sign C, including arbitrary kernel completion. Set H=B-B', delta=Tr rho H^2. No matrix square root or gauge model fit is needed for this estimator.

For any density states r,t with root-fidelity deficit m, Uhlmann purifications |r>,|t> can be chosen at vector distance sqrt(2m). For a fixed Hermitian H,

    |Tr H(r-t)|
      <=sqrt(2m)[sqrt(Tr r H^2)+sqrt(Tr t H^2)].

The second square root is at most the first plus ||H||sqrt(2m). Here ||H||<=2, giving

    |Tr H(r-t)|<=2sqrt(2m Tr r H^2)+4m.                     (27)

This argument is pointwise for every H, so it remains valid when H is selected from the same estimated states; no independent-data assertion is used.

Empirical sign optimality gives Tr C(B-B')<=0. Since Tr|X|H^2=2Tr X(B-B'), the true linear regret R obeys

    kappa delta/2 <= R := Tr X(B-B')
         <=(1/2)sum_s |Tr H(r_s-tau_s)| + 2eta
         <=2sqrt(M delta)+2M+2eta.                         (28)

The identity preceding (28) only requires that B is a reflection sign of X, hence commutes with |X|. The lower bound follows directly from |X|>=kappa rho and H^2>=0, not from squaring Loewner inequalities. Using 2sqrt(M delta)<=kappa delta/4+4M/kappa yields the finite-arithmetic bound

    delta <=(24M+8eta)/kappa^2.                            (29)

For eta=0 the sharper solved constant is 4(1+sqrt(1+kappa))^2<=12+8sqrt2<24. If both m_s<=m and eta<=m, (29) gives delta<=56m/kappa^2. This is a fast **weighted policy-error** bound, despite nonzero binary Bayes error; it is not the generic root-risk continuity bound that would lose a square root. Arbitrarily small eigenvalues of rho are allowed.

### 9.2 Physical noncommuting-gauge family

Let the unknown memoryless source and supplied real linear encoders induce

    E_x(w)=U[sum_alpha sigma_alpha w sigma_alpha
                              tensor G_alpha(x)]U^dagger,  (30)

where the positive semidefinite gauge matrices G_alpha(x) are unknown matrix-valued quadratics in x, sum_alpha Tr G_alpha(x)=1, and U is an unknown isometry. They need NOT commute or share a gauge eigenbasis, and may change rank. A concrete physical implementation takes the selector state |x><x| through an unknown quantum instrument {Psi_alpha}, sets G_alpha(x)=Psi_alpha(|x><x|), applies sigma_alpha to the logical input and U to logical plus the quantum instrument output. The instrument outcome is discarded; no flag, environment state, or gauge observable is supplied.

Define

    G(x)=sum_alpha G_alpha(x),
    H_j(x)=sum_alpha chi_(j,alpha) G_alpha(x),

and assume H_j(x)>=0 for j=X,Y,Z and every real unit x. Define Gbar and Hbar_j by the same four-anchor average. The only acquisition-conditioning assumption is the **operator-relative logical contrast**

    Hbar_X>=kappa Gbar,  Hbar_Z>=kappa Gbar.                (31)

This does not bound any nonzero eigenvalue of Gbar away from zero. It does not provide its eigenvectors. For example, sufficiently identity-biased unknown Pauli/gauge instruments satisfy (31) even with noncommuting gauge states.

A nonvacuous explicit fixture: measure the selector in an UNKNOWN real orthobasis {v_b}, use Pauli distributions with identity probabilities (1,4/5,3/4,7/10), prepare arbitrary unknown gauge states sigma_b that need not commute, and apply unknown U. Let the remaining Pauli probabilities in each branch be arbitrary. Then

    G_alpha(x)=sum_b (v_b^T x)^2 p_(alpha,b) sigma_b.

Every branch has each Pauli contraction at least2p_(I,b)-1>=2/5, so H_j(x)>=(2/5)G(x), making kappa=2/5 valid at calibration. The unique best selector v_1 is unknown and exactly correctable; choose its sigma_1 mixed with arbitrarily tiny positive eigenvalues. Other branches have different error and noncommuting gauge states, so this is not a constant-quality or fixed-spectator example. Neither the selector result, the gauge basis nor the output logical frame is given. The optimum is genuinely acquired. A nonzero-optimum fixture follows by reducing the first identity probability below1 but keeping it strictly largest.

The ordinary calibration pair and marginal are

    r_(j,±)=U[(I_2 tensor Gbar ± sigma_j tensor Hbar_j)/2]U^dagger,
    rho_bar=U[I_2/2 tensor Gbar]U^dagger.

Because Hbar_j>=kappa Gbar and Hbar_j<=Gbar, its support equals that of Gbar, and

    sign X_j=B_j=U(sigma_j tensor I_supp Gbar)U^dagger,
    |X_j|=U[I_2/2 tensor Hbar_j]U^dagger>=kappa rho_bar.    (32)

The raw-sign lemma applies to both axes. [B_j,rho_bar]=0 and the Pauli relations hold on the occupied support, so the actual extraction circuit (10) and proof (11)-(12) apply unchanged to the virtual ideal subsystem channel E_(0,bar)(w)=U[w tensor Gbar]U^dagger. Only the noisy banks above are ever queried.

### 9.3 Unrestricted CPTP optimum and uniform transfer

For any fixed actual D after U, Bell-outcome probabilities on its output when its input is half a Bell pair tensor an arbitrary gauge state define a POVM {T_alpha} ON THE GAUGE:

    Pr(Bell outcome alpha | gauge G)=Tr G T_alpha,
    T_alpha>=0, sum_alpha T_alpha=I.

This POVM is solely a mathematical representation of D; the learner neither implements nor discovers it. Moving an input Pauli through the Bell pair to its reference shows that the decoder success in (30) is

    F_e(D E_x)=sum_alpha Tr[G_alpha(x) T_alpha].            (33)

For alpha unequal to I, G_I-G_alpha is half the sum of the other two H_j, hence is positive. Equation (33) is therefore at most Tr G_I(x), attained by the ideal common U^dagger/discard-gauge receiver. Consequently

    ell_*(x)=1-Tr G_I(x)                                   (34)

is the unrestricted full-CPTP optimum, again a nonnegative quadratic. Moreover

    ell(D E_x)-ell_*(x)
       =sum_(alpha!=I) Tr[(G_I-G_alpha)T_alpha]
       <=Tr[G(x)(I-T_I)].                                 (35)

Each positive matrix-valued quadratic satisfies the operator domination

    G(x)<=sum_(a=1)^4 G(e_a)=4Gbar.                        (36)

To verify (36) without a supplied CP coefficient lift, pair with any gauge vector v: v^dagger G(x)v is a nonnegative scalar quadratic, so its real coefficient matrix is PSD and its unit-vector value is at most its trace. Pairing (36) with I-T_I>=0 and using (35) gives

    ell(D E_x)-ell_*(x)<=4 ell(D E_(0,bar))                 (37)

for every x. No simultaneous diagonalization or classical gauge flag is used anywhere in this proof.

### 9.4 Finite-cap consequence and limitations

Acquire the four real banks with m=kappa^2 epsilon/32768, and compute each raw-sign matrix with certified TOTAL trace-norm residual eta<=m (equivalently a Frobenius residual at most m/sqrt(d)). Then each delta_j<=56m/kappa^2, the extraction loss is at most154m/kappa^2, and its UNIFORM actual regret in (37) is at most616m/kappa^2<epsilon/20. The identical frozen-decoder scalar count stage, explicit finite N_B and all source/control/horizon budgets from Sections 5-6 apply. Thus the fully noncommuting model (30)-(31) has

    N_total <=4 N_B(d,kappa^2 epsilon/32768,beta/8)
                 +56 b[J+6*2^20*40/(gamma epsilon)],
    N_total=O_tilde(d^2/(kappa^2 epsilon)+1/(gamma epsilon)),
    ell(D E_xhat)<=(1+gamma)ell_*+epsilon

with the stated averaged operational budgets. This is still a structural-family theorem, not generic unflagged acquisition. The common logical Pauli algebra, positivity H_j(x)>=0, finite physical dimension and aggregate contrast promise are explicit. Their unknown matrices are actually acquired only to the extent needed for the two reflection controls; no environment or G_alpha(x) reconstruction occurs. The fixed-sigma automatic-kappa zero/useful-optimum corollaries do not automatically extend to arbitrary quantum gauge fields.

**Evidence status:** The companion independent audit/receipt binds this complete source, Sections 1-9. Source-disabled checks include 64 original sign/extraction cases, 16 finite scalar schedules, 24 commuting-gauge models/384 encoder checks, and 36 noncommuting physical instrument models/864 encoder checks. These test mathematical formulas and deterministic budgets, not sampled source acquisition. No full finite-cap acquisition experiment, hardware run, historical-priority claim, or general unflagged-source theorem is asserted.
