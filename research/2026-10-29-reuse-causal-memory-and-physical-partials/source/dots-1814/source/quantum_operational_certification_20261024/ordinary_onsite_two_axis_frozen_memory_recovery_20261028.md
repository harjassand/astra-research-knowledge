# Two-axis on-site calibration gives a frozen future decoder under retained memory

28 October 2026. **New scoped construction; independent receiving pending.** This is a stronger ON-SITE subfamily, not a general redundant multi-qubit code. It uses the strongest equally informed conventional proper-rotation learner, motivated by the separate adverse bandit pilot. No new sampled experiment, source calls, production optimizer or hardware advantage is claimed.

## 1. What changes, and the actual physical promise

Use the physical source/known-register/ordinary-input contract in `ordinary_local_multilogical_prequential_contractions_20261028.md`, final SHA256 `bd9586b4c324db0509eabfcdde6ad8d8a4144dc84d8a957550fa7a9087a47eef`, but restrict BOTH true logical generators of each logicali to ONE unknown physical site. There areq<=n logical input qubits andn known physical output qubits. The complete source is

    Ad_(U tensor I_M') composed with
             sum_(alpha in Pauli_q) (Ad_(P_alpha) tensor G_alpha),  (1)

with a fixed unknownU:L tensor G→P and arbitrary retained coherent memoryM. The CP mapsG_alpha:M→G M' can depend on time/exposed past, sum_alpha Tr_G G_alpha is TP, and for eachi andj=X,Z,

    H_(i,j)−kappa G_total is CP,  H_(i,j)=sum_alpha chi_(i,j)G_alpha. (2)

kappa is a supplied positive rational lower bound, at most1. The global full-CPTP oracle comparison separately assumesG_I−G_alpha CP for allalpha. The Y contrast may be negative; no Y margin is added. Source gauge states can have zero/tiny eigenvalues and arbitrary correlations with retained memory. No gauge, spectral basis, site matching, intrinsic error flag or environment is supplied to the learner.

Independent logical matrix algebras cannot share one physical qubit, so the unknown physical sitespi(i) are distinct. There exist local single-qubit unitariesV_i satisfying

    B_(i,j)=V_i sigma_j V_i† on sitepi(i),  j=X,Y,Z.      (3)

This is a consequence, not an acquired input: X,Z anticommute and fix the third oriented axis. After moving the matched sites into logical order and conjugating by theV_i†, the transformedU commutes with every logical matrix unit. Therefore it isI_L tensor V_G. This commutant argument establishes an actual logical/spectator tensor decomposition, not merely matching two expectation values.

The promise thatU and its on-site logical factors remain fixed persists through the future service call. Arbitrary algebra drift is NOT permitted or inferred absent from a calibration fit. Source memory and Pauli/gauge weights can otherwise change arbitrarily, including at a deterministic train/use boundary. Current private measurement/preparation coins remain nonanticipating through the complete port, as in the imported source. The learner never uses a protected entangled calibration reference.

The capability improvement is genuine at this restricted contract: train for a fixed finite number of calls, freeze one receiver, then introduce an unknown q-qubit payload/reference AFTER training. There is no private random terminal time and no long trusted storage of that unknown payload during calibration. One may choose any later finite service time while the stated source-family promise remains valid. This note proves one arbitrary future simultaneousq-input service, not an automatic reusable joint many-payload guarantee.

## 2. Fixed coarse bank learns the site matching

Let0<epsilon,beta<=1 be rational, setbeta0=beta1=beta/2, and use the imported w=1 coarse bank:

    L0=ceil log2(8 q n/beta),
    N0=ceil[3072 L0/kappa²].                            (4)

Each actual call prepares ALLq logical inputs in independentX± states and measures ALLn physical outputs in fresh independent Pauli bases. The ordinary local signed shadow is s_i(3Pi−I) for every logicali/site candidate. The imported one-copy identity and matrix martingale bound guarantee simultaneous trace-norm error<=kappa/8 except probabilitybeta0. True sites have contrast norm>=kappa; every other site has exactzero contrast, by the complementary local logical generator and gauge commutation. Finite scores within kappa/16 and thresholdkappa/2 therefore recover every pi(i) on this event. Check all selected sites are distinct, else set a physical replacement flag. A passed guard alone does not certify source-family membership.

No incompatible measurements or cloned output are used: every logical/site statistic is computed from the one actual full product measurement record. Other CURRENT signs/outcomes are averaged for each conditional mean; only the complete PRIOR record is conditioned on. The site matching is frozen before the fine bank. A coarse bad history remains a physical algorithm history and is charged, not discarded by acceptance conditioning. If matching is missing, flagged or nonunique, define the ENTIRE fixed N1 fine schedule nonetheless: retain the same ordinary product-input/all-output-Pauli schedule, use predetermined placeholder sites for any unused F accumulators, and never deploy those fits. At the future service call return the prescribed q-qubit replacement, for example by resettingq predetermined distinct physical output sites. These fallback resets and all fine calls are included in the worst-case resource cap.

## 3. Fine records estimate two columns of a proper rotation

On each ofN1 subsequent ordinary calls, independently draw for every logicali an axisj_i in{X,Z} and signs_i in{±1}. Measure every physical output site in an independent fresh axisa in{X,Y,Z}, obtaining b in{±1}. No learned receiver is coherently applied during these probes.

For a matched logical/site pair, its actual conditional Bloch matrix is

    M_(i,t)=R_i diag(lambda_(i,X,t),0,lambda_(i,Z,t)),
    R_i in SO(3),    lambda_(i,X,t),lambda_(i,Z,t)>=kappa. (5)

This follows by tracing all other logical/gauge outputs in(1), averaging other fresh input labels, and using(2). The unknownR_i is the fixed Bloch rotation ofV_i. Pauli weights, the two contrasts and the whole memory state may depend on the prior record; no iid or constant contrast is asserted.

From the actual ordinary input/output labels retain the real3-by-3 matrix

    F_(i,t)=6 s_i b_(pi(i)) e_(a_(pi(i))) e_(j_i)^T.      (6)

Its Y column is exactlyzero. Conditional expectation given the entire prior history isM_(i,t); the input-axis probability1/2 and physical-axis probability1/3 explain the factor6. Each realization has Frobenius norm6. Define the count-acquired average

    Mhat_i=(1/N1)sum_t F_(i,t),
    N_i=Mhat_i−R_i Dbar_i,  Dbar_i=(1/N1)sum_t diag(lambda_X,0,lambda_Z). (7)

Even thoughDbar is random/adaptive, N_i is the average of martingale differences, and E||N_i||F²<=36/N1. No conditional independence between logical learners is needed.

For a finite confidence statement, each of the six possibly nonzero scalar coordinates ofF lies in[−6,6]. Conditional Hoeffding's lemma gives a mean-zero increment mgf<=exp(18z²), hence

    Pr(|(N_i)_(a,j)|>=t)<=2 exp(−N1 t²/72).             (8)

This follows by iterating the conditional mgf and optimizing the scalar exponential parameter; it is not an iid tail imported for drifting states. Union over6q coordinates and ||N_i||F²<=6 max_entry² imply, with

    L1=ceil log2(24q/beta),
    N1=ceil[4096 q L1/(kappa² epsilon)],                (9)

that simultaneously

    ||N_i||F²<=kappa² epsilon/(8q)                     (10)

except probabilitybeta1. Indeed the exponent at each entry threshold isN1 kappa² epsilon/(3456q)>=(32/27)L1>=ln(12q/beta1). This proof can first condition on ANY correct coarse history, since all fine records are fresh and the source promise applies to every subsequent conditional memory state.

## 4. Proper SO(3) fitting: no improper branch and no Y assumption

Fit a PROPER rotationRhat_i with known objective gap

    <Rhat_i,Mhat_i>>=max_(R in SO(3))<R,Mhat_i>−delta,
    delta=kappa epsilon/(32q).                         (11)

All matricesRhat are known finite-control hypotheses. The scalar product is the real Frobenius product. This is conventional proper-rotation/Procrustes fitting, not a new online quantum optimization principle.

Here is the required two-axis curvature. For anyQ in SO(3),

    1−Q_YY<=(1−Q_XX)+(1−Q_ZZ).                         (12)

For a unit quaternionu=(u0,ux,uy,uz), the left side is2(ux²+uz²), while the right side is2(ux²+uz²+2uy²). Thus ifD=diag(lambdaX,0,lambdaZ), lambdaX,lambdaZ>=kappa,

    <R−Rhat,RD>=Tr[D(I−R^T Rhat)]
       >=(kappa/4)||Rhat−R||F².                        (13)

The proper-rotation constraint is essential: an improper reflection could preserve X,Z while reversingY. No polar determinant branch is swept under an error event.

Use(11) with the TRUE feasibleR_i and(7), then Cauchy and Young:

    (kappa/4)||Rhat_i−R_i||F²
       <=||N_i||F ||Rhat_i−R_i||F+delta,
    ||Rhat_i−R_i||F²<=16||N_i||F²/kappa²+8delta/kappa.   (14)

For the physical inverseVhat_i†, the virtual single-qubit unitary extraction loss is EXACTLY

    ell_i=1−|Tr(Vhat_i† V_i)|²/4
         =||Rhat_i−R_i||F²/8
         <=2||N_i||F²/kappa²+delta/kappa.               (15)

No good-estimate or eigenvalue/determinant branch is omitted. On(10), ell_i<=9epsilon/(32q). The same inequality also gives expected squared-error rates; this theorem uses the explicit fixed-bank confidence event instead of averaging a random terminal time.

## 5. A finite exactly physical quaternion fit

The conventional quaternion eigenproblem is classical; see Horn, *Closed-form solution of absolute orientation using unit quaternions*, JOSA A4 (1987), §§1D,3–4, [author-hosted primary paper](https://people.csail.mit.edu/bkph/papers/Absolute_Orientation_Scanned.pdf). We use finite backward accuracy rather than declare an irrational top eigenvector to be a free control.

For a known real matrixM, define a real symmetric4-by-4 matrixK(M), in coordinate order(0,x,y,z), by

    K00=Mxx+Myy+Mzz,
    Kxx=Mxx−Myy−Mzz, Kyy=−Mxx+Myy−Mzz, Kzz=−Mxx−Myy+Mzz,
    K0x=Mzy−Myz, K0y=Mxz−Mzx, K0z=Myx−Mxy,
    Kxy=Mxy+Myx, Kxz=Mxz+Mzx, Kyz=Myz+Mzy.              (16)

Direct expansion ofV(u)=u0 I−i(ux X+uy Y+uz Z) gives

    <R(u),M>=u^T K(M)u,  ||u||2=1.                    (17)

The full sphere parametrizes proper rotations, andV(u) is exactly unitary. Since||Mhat||F<=6, ||K(Mhat)||op<=6sqrt3<12 on EVERY record, not only the good event.

Use the received exactly rational Jacobi primitive in §2 of `ordinary_one_sided_effect_finite_positive_cost_rounding_20261028.md`, SHA256 `8b5859b44e398d5d97d5b14580041bd9232b9fe59188a9c090634d6a4dbab0b6`, after scalingK/48+I/4. For real input use real two-coordinate rotations: rational stereographic circle coordinates givec=(1−t²)/(1+t²),s=2t/(1+t²), so every accumulated matrixQ is EXACTLY real orthogonal. Its complex quaternion primitive specializes to this case without an eigengap assumption. Obtain

    ||K−Q diag(Q^T K Q)Q^T||F<=delta/2.                 (18)

Select a columnu ofQ corresponding to the largest rational diagonal label. Its Rayleigh quotient is that label exactly, whilelambda_max(K) exceeds it by at mostdelta/2. Thus(11) holds. The selectedu has exactly rational entries and norm1, soVhat=V(u) is an exactly rational SU(2) reference control. Zero/repeated top eigenvalues and arbitrary bad estimates stay physical.

Only4-by-4 classical matrices are diagonalized. All counts/means have O(logN1) entry bits; the known Jacobi cap is polynomial in log(1/delta), and its rational products have polynomial bit length. Each fit is computed from scratch from the rational empirical mean, so there is no recursive denominator growth. Compile theq one-qubit inverse rotations to a specified uniform service tolerance. There is no arbitrary local CPTP SDP, dense multi-qubit decoder, or source spectral inverse in this step.

## 6. Frozen receiver: full joint channel, uniform future memory

After the fixedN0+N1 calibration calls, freeze the acquired matching andq inverse rotations. In any later specified service call, applyVhat_i† on the acquired sitepi(i), retain thoseq sites in logical order and trace all other physical outputs. On flagged histories return the prescribed physical replacement. No update uses the unknown payload, and no protected payload/reference needed to exist during training.

On the joint calibration good event, the virtual logical-identity/gauge channel followed by this ACTUAL product receiver has

    ell0_joint=1−product_i(1−ell_i)<=sum_i ell_i<=9epsilon/32.      (19)

This is a full q-input Bell-reference statement: the receiver really is a product of local inverse unitaries on the distinct exact logical factors established by(3), so its virtual Choi state factors. It is NOT an independence assumption about the actual correlated noisy channel. The crucial extra feature is that(19) contains NO gauge or memory state at all.

For ANY later conditional source memory sigma, letG_(alpha,sigma) be its emitted positive gauge blocks. The general Bell-block POVM identity gives

    ell(Dhat E_sigma)−ell(D_* E_sigma)
       =sum_(alpha!=I)Tr[(G_(I,sigma)−G_(alpha,sigma))T_alpha]
       <=ell0_joint.                                  (20)

Under global CP dominance, D_* is pointwise optimal among every full-CPTP q-logical decoder for that SAMEsigma. Therefore one calibration good event, of probability at least1−beta, implies the frozen receiver's excess bound(19) for EVERY later memory state and time that still obeys the source-family promise. The comparator is a current-state channel evaluation, never an alternative past-policy memory trajectory.

The earlier deterministic-cutoff counterexample with a gauge-controlled logical flip is not contradicted: its true complementary logical operator occupies more than one physical site, so it fails the present on-site promise. General-width logical/gauge subsystems retain that obstruction and need the distinct private-terminal theorem or stronger persistence assumptions.

For one unknown future payload, require its FULL joint payload/reference to be introduced product with source/acquisition at the chosen service boundary (or conditionally product given the allowed classical record). Its state can otherwise be arbitrary and entangled across logical qubits. The ideal calibrated receiver's Bell loss is then within9epsilon/32 of the strongest informed oracle on that actual source memory. This does not assert an untwirled dimension-free diamond bound.

## 7. Implementation error and the actual later-memory comparator

The present uniform-memory property permits a stronger, explicit comparator transfer than generic prequential regret. Allocate rationalnu_cal,nu_svc>0 withnu_cal+nu_svc<=epsilon/4.

Require the complete implemented calibration process to be withinnu_cal of its declared ideal process in a norm strong enough to bound total variation of the retained classical calibration record, uniformly over initial source memory. A whole-process half-diamond/strategy discrepancy retaining future-accessible source memory suffices. Require the implemented ONE future payload service to be uniformly withinnu_svc in whole-q-input HALF-diamond distance of its nominal frozen receiver/source service at the ACTUAL pre-call memory state, including input/output controls, routing and storage during that service.

LetG_good be the unobservable mathematical set of calibration records with correct matching and the rotation-error bound. Its ideal probability is at least1−beta. The calibration-record TV bound gives physical probability at least1−beta−nu_cal. For EVERY physical good record, the nominal frozen receiver is good for ALL memory states by(19)–(20), including memory states changed by imperfect calibration or by intervening source evolution. Thus averaging over the PHYSICALLY ACTUAL later memory occupation is legitimate here, with

    actual mean excess <=9epsilon/32+beta+nu_cal+nu_svc.           (21)

This conclusion is not inferred merely from a generic whole-service norm bound; it uses the record-defined event and the new state-uniform extraction error. Withbeta<=epsilon/8 the right side is at most21epsilon/32<epsilon. No bad record is accepted conditionally without its probability charge. If the implementation interface cannot supply the stated uniform bounds, the corresponding physical guarantee is not certified by these calculations.

Optional paid operational service: use2q fresh private Pauli bits, one local input frame and inverse output frame per logical. With the same complete current-port nonanticipation, averaging makes each nominal q-input service a Pauli channel, whose half-diamond distance to identity equals its global Bell loss. The known-noise ideal extraction already produces a global Pauli channel, so its Bell-optimal loss is also the full-CPTP minimum half-diamond distance to identity. Triangle inequality addsnu_svc even when actual controls spoil exact Pauli form. No key-conditioned security or indefinitely repeated joint-payload guarantee is asserted.

## 8. Full resource comparison and scope

* Fixed calibration capN0+N1 from(4),(9), then one future payload call: O(kappa^(-2)log(qn/beta)+q kappa^(-2)epsilon^(-1)log(q/beta)) BLOCK calls. Every calibration block still preparesq input qubits and measuresn physical outputs. Near-linearq block calls do not mean linear total qubit traffic.
* Coarse storage is at mostqn two-by-two accumulators. Fine storage is six real rational counts per logical plus labels. Retaining all raw records costsO((N0+N1)(n+q)) symbols. There is no cross-copy quantum memory, environment access or held unknown payload during training. An actually supplied future payload still needs ordinary storage/routing during its one service.
* The acquired receiver usesq one-qubit inverse rotations and traces spectators. There are no controlled multi-qubit reflection blocks or mixed extraction ancillas in this on-site subfamily. Outputs may remain at their learned distinct sites. If a fixed layout is required, pay an explicit permutation/routing network, conservativelyO(nq) nearest-neighbor SWAPs; do not charge or grant endpoint routing implicitly.
* All calibration Pauli settings are actual local controls/readouts. Fine input axes useq bits/call and signs useq bits/call; coarse signs useq bits/call. Output axes use capped two-bit rejection on ALLn sites. WithB=N0+N1 andr=ceil log2(4nB/nu_rng), nu_rng<=nu_cal, at most2nB r fair bits suffice for output axes and sampler exhaustion costs at mostnu_rng. Use physical fallback on exhaustion. Total calibration sign/axis bits are at mostqN0+2qN1+2nB r, plus2q optional service-frame bits. All caps are fixed before outcomes.
* This is a provably fast conventional estimator in a structurally simpler physical model. It calibrates unknown on-site logical bases and an unknown matching, not a redundant multi-qubit error-correcting code. Arbitrarily correlated Pauli/gauge memory remains allowed, but generic changing encodings, non-Pauli logical noise, and wider gauge-coupled generators do not follow. The source promise is not learned from finite data.
* The root's practical Pauli/Procrustes pilot supplies motivation, not evidence for this exact theorem or a reused sample set. No new empirical advantage is claimed. The scientific addition is the finite ordinary data/control and confidence-to-future-channel composition, with all-reference and actual-memory comparison, not novelty of proper-rotation fitting.
