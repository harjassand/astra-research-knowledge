# Ordinary acquisition of a gap-certified NPT seed for the finite two-way factory

28 October 2026. Separate constructive candidate, conditional on receiving the neighboring finite factory. The filter mechanism is established entanglement-distillation machinery; the obligations here are ordinary encoder discovery, a quantitative acceptance/fidelity margin, finite raw-call caps and the same retained-frame interface. This is not a claim about arbitrary higher-dimensional NPT distillability or unassisted quantum capacity.

## 1. Promise and resulting interface

Use the same stationary/reset source, fixed four-real-coordinate encoder family, supplied rank bound, k-dimensional retained receiver frame and paid two-way classical/local-memory resources as the factory. Write J_x in REFERENCE-A-first, output-B-second order; dim A=2. Let partial transpose T_A refer to the known logical computational basis. Supply rational 0<mu<=1/4 and promise

    min_x lambda_min(J_x^(T_A))<=-2mu.                  (NPT)

No Choi state, negative vector, support subspace, filter or useful decoder is supplied. The warm phase uses only ordinary loss-state preparations. After warmup, actual Bell-half source queries and two local success filters create the resource; they are not relabelled ordinary queries.

The construction returns a fixed encoder x and local contractions F_A:C^2->C^2, F_B:C^k->C^2 such that, on one latent warm good event,

    J_f=(F_A tensor F_B) J_x (F_A tensor F_B)^*,
    a=Tr J_f>=mu,
    F=<Phi|J_f|Phi>/a>=1/2+mu/2.                       (1)

Both lower bounds hold together; no arbitrarily rare normalized-success claim replaces the raw source bill. A fixed success reservoir supplies the ordinary factory's recurrence input at gap g=mu/2. Its finite code-teleportation and complete-error conclusions then apply with the extra filter shortage debit.

## 2. Ten ordinary banks and a finite global negative witness

Use the accepted inverse-square positive-model fit, but set anchor trace tolerance

    delta_a=mu/4096, m_a=delta_a^2/8,
    n_a=ceil[(80 nextpow2(d r)/m_a) log(120 nextpow2(d r)/beta_t)],
    d=2k, r=min(d,3R).

Acquire ten ordinary T anchors, fit the same compact PSD lift with the same finite Slater/inward-rounding contract, and allocate failure beta_t across the banks. On the joint good event its real-x family obeys

    sup_x ||T_x(Hhat)-T_x||_1<=28delta_a.

After the known tensor-factor swap, the actual identity is

    J_x=2 I_A tensor Tr_A(T_x)-3T_x.

Therefore the fitted PHYSICAL normalized Choi family satisfies

    sup_x ||J_x(Hhat)-J_x||_1<=196delta_a<mu/20.         (2)

This is trace-precision prediction, not a Bures-close positive completion. For every unit v, W_v=(|v><v|)^(T_A) has operator norm at most1, hence (2) transfers its expectation uniformly without an output-dimension factor. Likewise the smallest eigenvalue of J^(T_A) changes by at most the trace error: partial transpose preserves Frobenius norm and ||Delta^(T_A)||op<=||Delta||F<=||Delta||1.

Scan a normalized rational cube-face encoder grid of chord radius h with h^2<=mu/16. At each x compute a unit vector with Rayleigh value within mu/16 of lambda_min(J_x(Hhat)^(T_A)), using finite backward-stable Hermitian arithmetic and certified value bounds, not an eigengap oracle. Select the smallest achieved Rayleigh value and its vector v. A normalized rational vector with sufficiently accurate coefficients suffices; its normalization is a known algebraic operation.

For the true comparator witness v_*, its quadratic x -> <v_*|J_x^(T_A)|v_*> has range inside[-1,1], since ||J_x^(T_A)||op<=||J_x||F<=1. Minimize this TRUE quadratic over x first; its least eigenvector has grid loss at most2h^2. Two uses of (2) and the finite Rayleigh tolerance give, under (NPT),

    theta=<v|J_selected^(T_A)|v>
       <=-2mu+2h^2+mu/10+mu/16<-3mu/2.                 (3)

The grid costs O(mu^(-3/2)) CLASSICAL eigensolver calls, not new source banks. The fit/eigensolvers and known controls have polynomial charged complexity in k,1/mu and bit precision. This is where the fixed four-selector dimension matters.

## 3. A fresh entirely ordinary witness certificate

Freeze x and v. Define rho_v=Tr_A |v><v| and the known receiver observable on the A-first loss state

    O_v=2 I_A tensor rho_v-3W_v,
    ||O_v||op<=5.

The exact loss-state identity gives

    Tr(T_x O_v)=Tr(J_x W_v)=theta.                      (4)

Thus each certificate sample is one ordinary T_x preparation followed by the known spectral measurement of O_v in the continuing frame. The signed measurement outcomes lie in[-5,5]; no entangled sender input is needed. Use

    n_v=ceil[(800/mu^2) log(2/beta_v)].

Hoeffding gives |theta_hat-theta|<=mu/4 with conditional failure at most beta_v, pointwise in the fixed U and training record. Accept iff theta_hat<=-5mu/4. On the training and validation good events, acceptance occurs and the TRUE witness satisfies theta<=-mu. Without the promise, false acceptance of theta>-mu still has probability at most beta_v. As usual, this is not a posterior statement for every exposed acceptance record.

Finite spectral controls have known dimension2k and bounded norm, so ordinary known-matrix circuit synthesis applies with the single complete-process budget. There is no source eigenbasis oracle. Arithmetic already allocated in (2)-(3) is not debited twice.

## 4. Quantitative local filters, with complex transpose conventions fixed

Take a Schmidt decomposition of the ACTUAL KNOWN VECTOR v, not of the unknown state:

    v=(V_A tensor V_B)(sqrt(s)|00>+sqrt(1-s)|11>),
    V_A unitary2, V_B:C^2->C^k isometric,
    D=diag(sqrt(s),sqrt(1-s)),
    J_-= [[0,-1],[1,0]],
    F_A=(V_A D J_-)^T, F_B=V_B^*.

Both are contractions. Let psi_-=(|01>-|10>)/sqrt2. Directly,

    v=sqrt2 (F_A^T tensor F_B^*)psi_-,
    (|psi_-><psi_-|)^(T_A)=I_4/2-Phi_2,
    W_v=2(F_A^* tensor F_B^*) (I_4/2-Phi_2)
                         (F_A tensor F_B).             (5)

The transpose on F_A is essential for complex Schmidt bases. With J_f as in(1), equation(5) gives the EXACT relation

    theta=a-2<Phi|J_f|Phi>=a(1-2F).

Accepted theta<=-mu therefore implies a(2F-1)>=mu. Since a<=1 and F<=1, both inequalities in(1) follow. The filters act on a fixed Bell resource, so their success probability is the actual fixed a; no input-independent conditional channel on unknown logical data is asserted.

There is no hidden small-Schmidt denominator. The spectrum of W_v is s,1-s,+sqrt(s(1-s)),-sqrt(s(1-s)), plus zero spectators. Since J_x is positive trace one, theta>=-sqrt(s(1-s)). Thus an accepted true witness theta<=-mu forces min{s,1-s}>=mu^2. On favorable histories the two-dimensional Schmidt support has this public conditioning. A finite algorithm can reject uncertified min-Schmidt-square below mu^2/2, using tolerance mu^2/8; this does not reject the good event and prevents an unbounded bad-history condition number. Degenerate equal Schmidt values require no unique basis: any computed factorization with certified backward error is adequate. Known filter circuits are synthesized to the total process tolerance, using an exactly contractive reference filter and its complementary failure branch. No unknown source conditioning enters.

## 5. A paid filtered-pair reservoir before recurrence

Generate one raw Bell pair by retaining its reference at the sender and sending its logical half through the selected x, the source, and the SAME receiver frame. Apply F_A locally at the sender and F_B at the receiver; exchange the two success flags and keep the pair only if both succeed. Discard all other pairs. Bilaterally twirl EACH successful pair only AFTER filtering, so it becomes sigma_F with F as in(1). Twirling before the filter would generally destroy the useful NPT witness and is not the protocol.

Let N_0 be the already specified number of input pairs required by the neighboring finite factory at recurrence gap g=mu/2 and its requested Q,delta_c,beta_r. For an additional shortage budget beta_f, put

    t_f=4 ceil(log_2(2/beta_f)),
    N_raw=ceil[2(N_0+t_f)/mu].                          (6)

Use at most N_raw raw source calls, retaining the first N_0 joint successes. If there are too few, abort with replacement outputs. On every good warm branch, independent raw trials have success probability a>=mu, so their mean is at least2(N_0+t_f). Chernoff bounds the shortage probability by exp(-t_f/4)<=beta_f. Tensor-instrument factorization again makes the retained normalized pairs iid sigma_F conditional on their coarse success pattern; fine private twirl keys and resource environments are not exported.

This reservoir adds real failed-filter source uses and classical flag communication. Its expected acceptance is not substituted for the deterministic cap. The subsequent recurrence cap, code-teleportation level, both-direction messages, memory and full finite-control costs remain those of the factory. In particular

    N_total_reference=N_w+N_raw,
    N_w=10n_a+n_v,
    error<=2(beta_t+beta_v+beta_f+beta_r)+delta_c+nu.     (7)

The common-frame horizon includes N_raw (not merely N_0) and every later typed data/payload slot. Warm/factory bad mass is paid once for the entire reference batch. At fixed mu the source scaling is still O_tilde(k^2+Q), with the explicitly large gap-dependent recurrence/filter factors and code logarithm. This is not a uniform near-PPT boundary rate.

## 6. A source beyond any CPTP Bell-fraction seed

Take amplitude damping with survival r=1/16:

    K_0=diag(1,sqrt(r)), K_1=sqrt(1-r)|0><1|.

Its normalized Choi partial transpose has negative eigenvalue -r/2=-1/32 with eigenvector

    v=(|01>-sqrt(r)|10>)/sqrt(1+r).

For the known filter F_A=diag(1,sqrt(r))/sqrt(1+r), F_B=I, direct calculation gives

    a=1/2, F=(1+r)/2=17/32>1/2,
    a(2F-1)=r/2.

This particular filter differs by harmless local basis choices from(5). The source meets (NPT) at mu=1/64.

In contrast its best CPTP recovery, even with any qubit unitary encoder, has Bell fidelity

    F_CPTP,max=(1+2sqrt(r)+r)/4=25/64<1/2.

Proof: its Bloch linear part is diag(sqrt(r),sqrt(r),r). Any CPTP qubit decoder has Bloch linear operator norm at most1 by trace-distance contraction. For any unitary encoder rotation R, von Neumann's trace inequality bounds Tr(T_D T_E R) by the nuclear norm2sqrt(r)+r, attained by the identity policy (or undoing an input unitary). Entanglement fidelity is [1+Tr(T_D T_E R)]/4; affine translations do not enter. Thus the preceding unfiltered F>1/2 seed promise truly fails for this family, not merely for an inconvenient chosen decoder.

For completeness the source is antidegradable as well: its complementary channel is amplitude damping with survival1-r, and subsequent amplitude damping of survival r/(1-r) reproduces the original when r<=1/2. This is an explicit antidegrading map, so the extension is two-way-assisted resource acquisition, not positive unassisted capacity. The quaternion family can be the calibrated logical unitaries. The equally informed conventional learner can use these same ordinary tests and filters.

## 7. Prior art and limits

Horodecki, Horodecki and Horodecki, *Distillability of Inseparable Quantum Systems*, https://arxiv.org/pdf/quant-ph/9607009 , equations2–8, directly uses negative partial-transpose vectors, local filtering and recurrence. That primary source was inspected. We do not claim a new NPT distillability theorem. Here dim A=2 forces every negative vector to have Schmidt rank at most two; projection onto its Bob Schmidt support makes the two-qubit filtering argument explicit. Nothing implies that arbitrary higher-dimensional NPT states are distillable, or that PPT entangled channels have zero assisted resources beyond this one-copy method.

The potentially useful extension is the source-unknown, ordinary-discovered encoder/witness, quantitatively nonrare filter, finite capped reference factory and paid typed calibration composition. It remains a candidate until independently checked. Existing accepted internal foundations, including the more general undecidability results, are neither contradicted nor reopened by this promised finite-gap construction.
