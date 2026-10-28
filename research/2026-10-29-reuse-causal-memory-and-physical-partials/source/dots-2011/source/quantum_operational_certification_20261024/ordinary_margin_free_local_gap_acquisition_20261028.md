# Margin-free local support and signed-gap acquisition under retained memory

28 October 2026. **New candidate; independent receiving pending.** The received acquired-patch theorem and its receipts are unchanged. This source removes its SUPPLIED positive numerical contrast margin, and permits different supports/generators to become informative at different calibration stages. It does not remove qualitative source structure or guarantee acceptance on uninformative histories.

## 1. What is supplied, and what is now acquired

There are q logical input qubits and a known n-qubit physical line. A fixed unknown unitary identification U:L tensor G->P gives exact logical generators B_(i,X),B_(i,Z), jointly supported on an unknown interval of length at most a supplied w. Independent logical algebras commute. The inaccessible memory can be arbitrary, and each source call has the complete nonanticipating form

    Ad_(U tensor I_M') o sum_alpha(Ad_(P_alpha) tensor G_(alpha,h)), (1)

with CP maps G_(alpha,h):M->G M', total trace preserving after discarding G. These maps may depend on time and exposed past history, but not on current private preparation/readout coins except through the actual quantum input. U and its algebra are fixed through calibration and future use.

During acquisition impose ONLY the qualitative CP conditions

    H_(i,j,h)=sum_alpha chi_(i,j)(alpha) G_(alpha,h) is CP,
    j=X,Z.                                             (2)

No rational kappa, positive uniform contrast margin, source eigenvalue floor, contrast mass, or signed spectral gap is supplied. A positive uniform kappa need not even exist. As always, G_total-H_(i,j,h) is CP. The nonnegative signed blocks in (2) orient the recovered logical generators; they are a structural promise, not a statistic certified by this procedure. Global identity dominance alone does not imply (2).

The learner has the same ordinary product-state preparation, actual product-Pauli readout, finite classical arithmetic, known local controlled-unitary synthesis, routing and trusted service controls as the received local source. There is no calibration reference bypass, source inverse, readable error flag, inaccessible gauge control, reset or source spectral basis. Inputs for a later unknown q-qubit payload/reference are introduced only after acceptance, initially product with source/acquisition or conditionally product given the allowed classical record.

For rational 0<epsilon<=1 and 0<beta<=epsilon/8, the caller supplies finite coarse/fine stage caps S_c,S_f>=0, not an unknown noise margin. Define

    W=min(n,3w-2), d0=2^w, d=2^W, M0=n-w+1,
    C=min(q,2W-1), K=min(q,W+2(C-1)(W-1)), A=min(q,K^2),
    beta_c=beta_f=beta/2.                              (3)

The output is either an explicit physical frozen coherent receiver with a simultaneous high-probability operator certificate, or ABSTAIN before requesting an unknown payload. Bad certificate probability and implementation error are charged below. There is no unconditional near-oracle service claim after abstention and no posterior correctness guarantee for every exposed accepted record.

## 2. Conditional contrast identities need positivity, not a numerical margin

Given the complete PRIOR record and after averaging all other fresh input labels, write the physical output from the sign-s j-state of logical i as rho_h+s Delta_(i,j,h), where

    Delta_(i,j,h)=B_(i,j) R_(i,j,h),
    0<=R_(i,j,h)<=rho_h,
    [R_(i,j,h),B_(k,l)]=[rho_h,B_(k,l)]=0.             (4)

They follow directly from (1)--(2). Put lambda_(i,j,h)=Tr R_(i,j,h) in [0,1]. If J contains the true support, reduction gives Delta_J=B_(i,j) R_J and therefore, for a finite stage average,

    ||Delta_bar_(i,j,J)||1=Tr Rbar_(i,j,J)=lambda_bar_(i,j). (5)

The fixed B can be taken through the time average, even though every gauge state and noise weight may drift with the actual past.

If J is DISJOINT from the true support, Delta_(i,j,J)=0 at EVERY history for j=X,Z. Indeed the complementary true generator flips Delta_(i,j), commutes with R_(i,j), and is supported entirely in the subsystem traced out. This exact zero, not a supplied lower signal, enables sound support discovery. Current outcomes or other learners' current signs are never conditioned on in these asserted conditional means.

## 3. Nonzero confidence scores acquire supports without kappa

For stages s=0,...,S_c, set

    eta_s=2^(-s)/4,
    L_c=ceil log2(4d0 q M0(S_c+1)/beta_c),
    N_(c,s)=8*12^w*L_c/eta_s^2=128*12^w*L_c*4^s.       (6)

Every stage uses a FRESH bank of exactly this integer number of ordinary source blocks. Prepare all q inputs in independent uniformly chosen X/Z axes and signs, and measure every physical output in an independently uniform Pauli basis. For every unresolved logical i, candidate length-w interval J, and j=X,Z, accumulate the actual shadow record

    2*1{j_i=j}*s_i*Z_J,
    Z_J=tensor_(l in J)(3 Pi_(a_l,b_l)-I).

The conditional matrix variance is <=2*3^w I and centered increment norm <=4d0. Matrix Freedman at a=eta_s/d0 yields

    Pr(||estimate-its predictable average||op>a)
       <=2d0 exp[-N_(c,s)a^2/(2(2*3^w+4d0 a/3))].     (7)

Because eta_s<=1/4, the denominator is <=5*3^w. Equations (6)--(7) and a union over all 2q M0 processes and S_c+1 stages give total coarse failure at most beta_c, with simultaneous TRACE-norm errors <=eta_s. Correlations among intervals/logicals and retained-memory backaction do not require independence. The extra factor two in the coarse budget pays the input-axis importance weight; it is not free information from incompatible probes.

Compute each empirical trace-norm score to additive eta_s/4 using the received finite rational Jacobi primitive. A Frobenius residual eta_s/(4d0) suffices because trace-norm error is at most sqrt(d0) times that residual. For every unresolved i, retain the FIRST candidate interval/axis pair whose finite score satisfies

    score_(i,J,j,s)>2 eta_s.                          (8)

One may instead choose the greatest score; soundness does not depend on maximizing. Strict inequality handles equality without implicit acceptance. On the confidence event, every disjoint interval has score <=5eta_s/4, so ANY retained interval overlaps the true support. No unknown kappa or positive lower signal was used in this inference.

A logical's first certified interval is retained across later stages. Its validity is permanent because the true algebra is fixed. Once all q intervals are acquired, expand each by w-1 sites on both sides, clip/pad within the line to length W, and freeze the envelopes. The received packing and interval-coloring argument gives at most C colors and the same A in (3). Missing supports by S_c, or a failed physical coloring guard, produce ABSTAIN. On the confidence event the latter guard passes whenever all supports have been acquired.

At a reached stage, a true containing interval has its axis-j score >=lambda_bar_(i,j,s)-5eta_s/4. Thus any unresolved logical with

    max_(j=X,Z) lambda_bar_(i,j,s)>=4 eta_s            (9)

is discovered at that stage. Different logicals may satisfy (9) at DIFFERENT stages and through different axes; there is no coincident-signal requirement. If, more strongly, every unresolved logical has this maximum nominal average mass persistently >=lambda_*>0, AND the first sufficient stage eta_s<=lambda_*/4 lies within the caller-funded cap, then

    N_(c,s)<=512*12^w*L_c/lambda_*^2,
    total coarse blocks through s <(4/3)N_(c,s).        (10)

Here lambda_* is an instance-analysis parameter, never an algorithm input. The dyadic first-scale bound also holds at s=0 because lambda_*<=1. Both the more general itemwise implication and the persistent-mass rate are pathwise statements on the ONE confidence event; section 7 gives their correct probability/occupation interpretation.

## 4. Direct signed gaps acquire each generator at its own informative stage

Let b be the largest positive dyadic with

    b^2<=epsilon/(18Aq),                               (11)

so b<=1/4 and b^2>epsilon/(72Aq). After all supports have been frozen, use fresh fine stages t=0,...,S_f, with

    L_f=ceil log2(4dq(S_f+1)/beta_f),
    a_t=2^(-t)/(16d),
    N_(f,t)=8*3^W*L_f/a_t^2.                          (12)

Each bank prepares all logical inputs in independent uniform X/Z axes and signs, and measures all physical outputs in independent uniform Pauli bases. For every unresolved generator use the actual record

    Y_(i,j)=2*1{j_i=j}*s_i*Z_(W_i).                   (13)

Its conditional expectation is the local Delta_(i,j,h) of (4), its conditional second moment is <=2*3^W I, and centered increment norm is <=4d. The same finite martingale calculation as in the received acquired-patch source gives, with total failure at most beta_f over the 2q(S_f+1) processes,

    ||Deltahat_(i,j,t)-Delta_bar_(i,j,t)||op<=a_t.     (14)

No unsigned marginal or positive marginal lower bound is needed by this direct-only fine learner. An unsigned shadow can be retained for interpretation, but does not replace the signed-gap test. Fresh random input-axis mixing is retained; deterministic axis cycling is not substituted under drifting memory.

For each unresolved generator use finite rational Jacobi on its known empirical matrix, obtaining C=Q D Q^dagger with ||C-Deltahat||F<=a_t/4. Q is EXACTLY rational unitary and D has rational labels. Define

    e_t=5a_t/4, h=min_k|D_kk|,
    S_(i,j,t)=Q diag(sign D_kk)Q^dagger, sign(0)=+1.    (15)

The reflection is exactly physical on every record. Retain this generator's FIRST S passing the rational comparisons

    h>e_t,
    2e_t<=b(2h-e_t),                                  (16)

equivalently h>5a_t/4 and 10a_t<=b(8h-5a_t). Previously retained S operators are not updated. All later probes still use ordinary random axes/signs; they do not apply the learned decoder or inspect an unknown payload.

Here is the exact operator implication. By (4), Delta_bar=B Rbar with Rbar>=0 and [B,Rbar]=0. On (14), ||C-Delta_bar||op<=e_t. If h>e_t, the true Delta_bar is invertible, its gap is at least h-e_t and sign(Delta_bar)=B. The standard two-sector Sylvester argument gives

    ||S-B||op<=2e_t/(2h-e_t)<=b.                       (17)

The true and estimated sign sectors have equal ranks because their straight perturbation path cannot cross zero. Their opposite-sector spectral separation is at least (h-e_t)+h. This proves (17) without a source eigenbasis, a supplied spectral gap, a numerical contrast lower bound or a free irrational control. It is precisely the received acquired-patch sign lemma, using only its direct-gap branch and positivity, not importing the stronger kappa premise of that parent theorem.

Accept once ALL 2q reflections have been acquired, even if their successful banks occurred at different stages. Fixed B makes every retained operator certificate permanent. If any generator remains unresolved at S_f, ABSTAIN. The physical coherent extraction theorem does not require the learned reflections to commute exactly, so fitting different generators at different stages creates no compatibility loophole.

If an unresolved generator's actual predictable average at a reached fine stage has signed gap at least gamma_(i,j,t)>0, the sufficient condition

    a_t<=b gamma_(i,j,t)/5                            (18)

forces (16) on the confidence event. Indeed e_t<=b gamma/4 and h>=gamma-e_t, so 2e_t/(2h-e_t)<=b/(4-3b/2)<b. Thus different generators can be informative at different stages. Under the stronger persistent common nominal gap gamma_*>0, a first sufficient stage within the cap obeys

    N_(f,t)<57600 A q 3^W L_f/(gamma_*^2 epsilon)+1,
    total fine blocks through t <(4/3)N_(f,t).         (19)

Gamma_* is not supplied. It does not follow from positivity alone and is not conditioned into a high-probability statement without the qualification in section 7.

## 5. One frozen all-future-memory decoder after acceptance

On the simultaneous coarse/fine event Good, whose probability is at least 1-beta, all retained envelopes contain their true generators and all retained reflections satisfy (17). Apply the same actually physical colored coherent receiver as the received acquired-patch theorem: q mixed receiver ancillas, three controlled-reflection gates per logical block, the declared color order, and discard the physical register only after all blocks finish. This is not a sequence of separately reconstructed marginal CPTP decoders.

The received full-reference cone estimate yields, for EVERY future emitted gauge state g, including one entangled with retained memory,

    ell0_joint(g)<=3A sum_i(delta_(i,Z,g)+delta_(i,X,g)/2)
       <=(9/2)Aq b^2<=epsilon/4,                       (20)

where delta_(i,j,g)=Tr[rho_g(S_(i,j)-B_(i,j))^2]<=b^2. All q Bell references and a gauge/memory purifier are retained in that theorem. The bound is operator-uniform, so no training-gauge floor or support has to persist after certification.

For any ACTUAL later source memory omega, the Pauli/gauge Bell-block identity compares this receiver to D_*=Tr_G Ad_(U^dagger) by excess <=ell0_joint(g_omega)<=epsilon/4. If the future CP blocks also obey G_I-G_alpha CP, D_* is the pointwise full-CPTP optimum. If not, it remains the specified exact-extraction benchmark. Future positive contrasts are unnecessary for this latter comparison after the algebra has been acquired. The source still has the fixed algebra and Pauli/gauge form; arbitrary future changes of U are not covered.

Optional private Pauli input/output framing has its explicit 2q-bit and complete-norm control bill. No unframed dimension-free diamond conversion or repeated-payload conclusion is automatically claimed here. A separate received complete-CP-domination theorem can consume this uniform certificate with its own key-retirement/common-controller interface; that is not a hidden part of the present one-service guarantee.

## 6. Physical implementation and accepted risk

Let nu_cal bound the TV discrepancy of the full retained calibration record, including frozen support/reflection labels, stopping times and acceptance flags, between the implemented and declared experiment; a stronger complete-process discrepancy retaining future-accessible source memory suffices. Let nu_svc uniformly bound the whole-q-input half-diamond error of the ONE future service at its ACTUAL pre-call memory, including finite synthesis, routing, ancillas and service storage. Allocate nu_cal+nu_svc<=epsilon/4.

Because every good accepted record supplies an all-gauge operator certificate, changes to the actual memory during imperfect calibration or intervening evolution do not invalidate its nominal receiver bound. False physical accepted certificates have total probability at most beta+nu_cal. Thus the unnormalized joint accepted excess satisfies

    E[1_accept*(ell_actual-ell_exact/current_oracle)]
       <=epsilon/4+beta+nu_cal+nu_svc<epsilon.         (21)

The oracle label requires the separate future dominance condition. Conditional-on-acceptance bad mass is at most (beta+nu_cal)/Pr(accept), not beta; there is no record-by-record posterior guarantee. If the procedure abstains, it has not acquired an unknown payload and promises no high-fidelity replacement for a caller that nevertheless forces a service.

## 7. Stopping, varying excitation, and the declared occupation

All conditional averages in (4)--(19) refer first to the DECLARED calibration experiment with the unknown noisy source and ideal trusted ordinary controls. They are random functions of that actual source's prior record, not an iid state or a different comparison policy. On one simultaneous confidence event:

* Every unresolved logical satisfying (9) at a reached coarse stage acquires a correct permanent envelope.
* Every unresolved generator satisfying (18) at a reached fine stage acquires a permanent operator approximation.
* When every item has acquired its witness, the stagewise procedure accepts and (20) holds for every later memory state.

A high-probability completion rate such as (10),(19) needs an almost-sure persistent-excitation premise on reached histories, or a separate debit for histories where the required excitation fails. Conditioning the source's random favorable averages into the concentration statement is not justified. The more general itemwise statement can cover intermittent/asynchronous excitation, but it is still an implication on Good, not a prediction that arbitrary adversarial memory must supply useful data.

Arbitrary delay until an item's informative episode still costs every elapsed geometric stage. Mere existence of positive-gap episodes at unspecified later times does not imply the persistent-gap inverse-accuracy rate; an explicit bound on their arrival or the stated persistent premise is needed. Permanent certificates remove a coincidence requirement, not the cost of waiting for information.

Transfer a PROVED declared stopping/completion record-event probability to the physical record law with nu_cal. A floor or contrast mass asserted only on a different imperfect physical-memory trajectory cannot be substituted into the declared law from record TV alone. Uniform excitation promises covering all allowed histories in both experiments are sufficient; they are not required for acceptance soundness.

## 8. A genuine zero-uniform-margin instance

Use one logical qubit, four gauge states and any fixed width-three identification U (for example the reversible repetition/majority unitary followed by an unknown fixed output mixer). Let P_0 be a rank-two gauge projector and P_1=I-P_0. At alternating calls take P=P_0,P_1 and the CP preparation blocks

    G_I=(I+P)/8, G_Z=(I-P)/8, G_X=G_Y=0.              (22)

These may be viewed as maps discarding their incoming memory and preparing the displayed states; a retained spectator memory can also be tensored through. Their total gauge state is I4/4, their traces sum to one, and G_I-G_Z=P/4>=0. The acquisition contrasts are

    H_X=P/4, H_Z=I4/4.                               (23)

They are CP nonnegative, but H_X-kappa G_total is NOT positive for ANY kappa>0, at either kind of call. This is not merely a source whose positive margin was forgotten; the earlier uniform-positive-margin premise genuinely fails.

Every coarse X contrast has mass 1/2. Every even-length fine bank, regardless of its start parity, has average H_X=I4/8 and H_Z=I4/4, giving signed gaps 1/16 and 1/8 after the logical I/2 factor. All stage lengths above are even. Consequently sufficient funded stages certify the full algebra. Exact extraction has nonzero oracle loss Tr G_Z=1/4, and an acquired receiver attains the declared excess bound. No gauge flag or projector P is supplied to the learner. The example is source-disabled exact algebra, not a sample run.

It also illustrates why separately retained generator certificates are legitimate: the SAME fixed B operators underlie all moments, despite changing noise/gauge blocks. A changing encoding would invalidate this inference and is excluded.

A second witness makes the gain from retained certificates explicit. With a fixed full mixed gauge, one source phase uses logical Pauli probabilities p_I=p_X=1/2 and another uses p_I=p_Z=1/2. In the first phase H_X=G_total,H_Z=0; in the second H_X=0,H_Z=G_total. Take source changes at predictable exposed phase/stage boundaries, not as a function of a fresh private input axis. Each fine stage can lie wholly within one phase, so NO fine stage has both signed gaps. Fund an early sufficiently accurate X-informative stage and a later sufficiently accurate Z-informative stage. The retained procedure acquires the two operators separately and accepts; a rule demanding simultaneous X/Z gaps in one fresh bank would always abstain. The coarse phase can be X-informative. Both training logical channels are complete dephasing channels, yet they reveal complementary pieces of the same fixed physical decoder; a later allowed source call may be noiseless. This is a source-model witness, not a promise that arbitrary memory will schedule favorable phases or an execution using sampled outcomes.

## 9. Resource ledger and conventional baseline

The explicit worst-case source cap is

    sum_(s=0)^S_c N_(c,s) + sum_(t=0)^S_f N_(f,t),     (24)

plus one later payload call only after acceptance. Both sums are integer geometric series with ratio four. Stopping early only reduces the bill. All source blocks still prepare q logical input qubits and measure n physical output qubits; block-call bounds are not total-qubit-traffic bounds. Coarse storage is at most 2q M0 matrices of dimension d0; fine storage is at most 2q matrices of dimension d, plus retained exact rational reflection controls and labels. Finite known-matrix diagonalization and controlled-reflection synthesis are paid as in the received sources; no global Choi SDP, gauge reconstruction or source eigenbasis is provided.

For B equal to the worst-case calibration cap, finite output-axis samplers use at most 2nB r_rng bits with r_rng=ceil log2(4nB/nu_rng), nu_rng<=nu_cal. Coarse and fine input signs/axes together use at most 2qB bits. Exhaustion produces a declared physical abstention flag and is within nu_cal. Optional later Pauli frames use 2q further private bits. Decoder mixed ancillas, all controlled-reflection gates, layout/routing and service-time storage remain the received physical bill; there is no unknown payload held through calibration.

All computation can be padded to public finite durations and all caps are fixed before outcomes. The conventional benchmark receives exactly the same access and may use exactly the same confidence-certified nonzero support scores, retained certificates, direct signs and coherent extraction. This source claims neither a new matrix-sign algorithm nor practical hardware advantage. It proves acquisition without a supplied numerical margin, at an instance-sensitive cost, and allows pointwise zero-margin sources whose observable stage averages identify the fixed algebra.

The qualitative CP positivity, exact support, fixed algebra, known output register and current-port privacy are still promises. Wider conservative envelopes can contain unexcited spectator directions and cause abstention even when a smaller support would suffice; no automatic minimal-support refinement is claimed. No finite transcript validates arbitrary unseen source-model completions.

## Dependency boundaries

The coarse shadow/martingale and support-expansion ingredients are from `ordinary_local_multilogical_prequential_contractions_20261028.md` (SHA bd9586b4c324db0509eabfcdde6ad8d8a4144dc84d8a957550fa7a9087a47eef). The finite direct signed-gap lemma, coherent future-uniform extraction and accepted-risk interfaces are independently received in `ordinary_acquired_patch_excitation_frozen_recovery_20261028.md` (SHA ce0ba44ec65e6364f6537063491eb4e329c8918f2ae27e4e6718a5b41e442117). Their older supplied-kappa theorem is NOT imported wholesale as a claim that (2) has a numerical margin; the displayed conditional identities, new nonzero-score guard and direct-gap proof supply that relaxation explicitly. The gap-free finite rational primitive remains `ordinary_one_sided_effect_finite_positive_cost_rounding_20261028.md` (SHA 8b5859b44e398d5d97d5b14580041bd9232b9fe59188a9c090634d6a4dbab0b6). Separate independent checks and receiving will bind this source's final bytes.
