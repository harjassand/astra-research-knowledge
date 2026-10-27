# Independent acquired-positive-gauge audit

27 October 2026. Read only the supplied frozen `COMMON_ULTRA.txt`, learning `CASE.md`, sources S7 and S8, the principal's explicit science messages, and the subsequently authorized u32 scientific artifacts identified below. No memory, other study trajectory, shared edits, other chats, or additional helpers were used. The results below are conditional mathematics, not physical acquisition, novelty, or practical-advantage claims.

## Verdict

The corrected positive-gauge certificate is mathematically sound for the complete classical transcript over the legal action library. Physical preparability of its virtual vertices is unnecessary. Once a true positive realization and a stochastic fitted realization have a certified joint-column error e, both requested bounds follow, with the sharper bounds

    t = min(1,e/2),
    H-step TV <= 1-(1-t)^H <= min(1,H e/2),
    clocked full-transcript TV <= b = gamma t/(delta+gamma t)
                                  <= gamma e/(2 delta).

For M sequential memory-retaining macros with fresh independent clocks, joint transcript TV is at most

    1 - [delta/(delta+gamma t)]^M.

These plus-denominator and sequential-product bounds are sharp from this error information. There is no signed-model requirement gamma e<delta. The remaining hard premise is acquiring and verifying a useful e and positive gauge from counts. The rank-two construction below proves a sharp rare-mode resource obstruction to uniform prediction on all normalized reachable inputs. This obstruction does not apply to every unconditional prediction from the original start.

## 1. Exact coordinate and normalization requirements

Let V be the reachable/observable quotient in S7. The supplied architectural bound is dim(V)<=r. Choose r legal **normalized** positive core preparations rho_j, with rho_1=rho_0, and r future-event tests including the empty test f_0. Set

    H_ij=f_i(rho_j),       (H_z)_ij=f_i(T_z rho_j).

True invertibility of H plus the rank upper bound certifies exhaustion. In preparation coefficients the operators are

    A_z=H^{-1}H_z.

S7's B_z=H_z H^{-1} instead act in test coordinates. Thus the corrected formula is

    W_z=S^{-1}H^{-1}H_z S,
    c_0=S^{-1}e_1,
    1^T S=1^T.

Equivalently V_g=H S, G_z=H_z S, and W_z=V_g^{-1}G_z. The literal S^{-1}B_zS with c_0=S^{-1}e_1 is a coordinate mismatch and is not the theorem audited here.

The true trace row of normalized cores is 1^T. Consequently 1^T H^{-1}=e_0^T. Exact TP gives sum_o e_0^T H_(a,o)=1^T, and hence

    sum_o 1^T W_(a,o)
      = e_0^T sum_o H_(a,o)S
      = 1^T.

Also 1^T c_0=1. If W_z>=0 and c_0>=0, these are stochastic joint outcome/next-state kernels with an exact probability initial vector. For general subnormalized S7 cores with masses m_j, the correct normalization condition is **m^T S=1^T**; column sums one alone are insufficient. The principal's intended normalized outcome-discarded cores satisfy m=1.

## 2. Exact realization and virtual vertices

Exhaustion gives the exact intertwining between physical quotient evolution and the W matrices. Therefore a word w=z_n...z_1 has probability

    p(w)=1^T W_(z_n)...W_(z_1)c_0.

For each positive-probability history, c(w)=W_w c_0/p(w) lies in the simplex. Discarded outcomes, randomized actions, classical feedback, and stopping preserve this property. Thus every input obtainable from rho_0 using the legal library lies inside this simplex. No new inaccessible input, new coherent control, or external reference is included.

The virtual vertex q_j=sum_k S_kj[rho_k] need not have a positive physical representative. That causes no problem for classical predictions: nonnegative W and c_0 define an ordinary controlled edge-emitting HMM, and intertwining proves equality with the true legal process. If an HMM convention demands a separate old-state/new-state emission factorization, state expansion may be necessary; an r-state joint outcome/next-state kernel is the precise contract.

Virtual positivity does not imply that the vertices can be physically prepared, that W has a CP realization in that gauge, or that a physical hidden state can be sampled from the latent label. Physical memory is retained by the actual procedure; the predictor retains an abstract state giving all later allowed classical laws.

An explicit counterexample to the demand for physically preparable vertices is given in section 7: it has nonphysical vertices and strictly positive gauged kernels.

## 3. What finite count intervals must certify

Let C(D) be a simultaneous confidence set for H and the H_z from legal raw joint-event counts. With probability at least 1-alpha it contains the true tuple. On that same event, the certificate must rigorously establish:

* every feasible H is invertible and the supplied architectural rank bound exhausts V;
* exact known trace and TP identities, rather than merely a small sampled equality residual;
* W_z>=0 and the exact c_0=S^{-1}e_1>=0;
* fitted What_z>=0 and sum_o 1^T What_(a,o)=1^T exactly;
* a common upper bound e on max_(a,j) sum_o ||(W_(a,o)-What_(a,o))e_j||_1.

An entry interval [L_z,ij,U_z,ij] supplies the valid upper bound

    e_bar=max_(a,j) sum_(o,i)
       max(|L_(a,o),ij-What_(a,o),ij|,
           |U_(a,o),ij-What_(a,o),ij|).

Clip it at 2 because the two joint columns are probability vectors. Using simultaneous entry intervals as an outer set is sound but potentially loose. Core/S/model selection after seeing D does not itself require a new union bound when every used event was already covered and the reported property is verified uniformly on C(D).

Exact TP should enter as a known structural identity or by an exact stochastic fit. A generic rectangular box of noisy entries does not imply an equality for all points in the box. Numerical inverse and positivity computations need directed rounding or other rigorous residual/error bounds. A universal inequality over an empty feasible set must not be accepted as a substantive certificate.

At an unknown true zero, a generic positive-width outer box can extend to negative gauge entries. This certificate can therefore require a strict positivity margin or exact known zero structure. It need not succeed on every positive realization. Not every CP process has an r-state positive realization, and no efficient general search for S is proved. An empirical low rank alone cannot rule out unseen modes.

With confidence at least 1-alpha the following deployment inequalities hold simultaneously for every allowed classical policy, including a policy chosen from the acquisition data. Alpha is the probability that the certificate's premises fail; it is not silently folded into e. A joint acquisition/deployment comparison can conservatively add alpha to the deployment TV bound.

## 4. Governing coupling proof

Fix the acquisition data on the confidence event. Let t=min(1,e/2). For any action a and old latent label j, the true and fitted joint distributions on (outcome,next latent label) have TV at most t, since

    (1/2)sum_(o,i)|W_(a,o),ij-What_(a,o),ij|<=t.

Draw the same initial latent label from the exact c_0. While the labels and complete classical histories agree, share the policy randomness, choose the same action, and maximally couple these joint columns. Agreement persists for the next attempt with conditional probability at least 1-t. On first disagreement the coupling may be arbitrary.

For at most H attempts, agreement probability is at least (1-t)^H. The coupling inequality proves the fixed-horizon result, including the entire classical record and the abstract terminal latent label. Marginalizing any part of that record only decreases TV.

For the paid abort clock, share the independent coin before each attempted primitive. Let F be the supremum probability of coupling failure before termination, starting from any matched latent label and classical controller history. Immediate forced abort, probability delta, terminates with agreement. Otherwise failure on this primitive has probability at most t; agreement followed by native termination can only help. Thus

    F<=gamma[t+(1-t)F],
    F<=gamma t/(delta+gamma t).

For a fully finite proof, first cap the number of attempts, apply this recurrence to the truncated failure probability, solve the geometric sum, and let the cap tend to infinity. The paid clock guarantees almost-sure finite termination. Equivalently the potential attempt count N has P(N=n)=delta gamma^n and

    Pr(agreement)>=E[(1-t)^N]=delta/(delta+gamma t).

This proves the full finite-string transcript law, not just each fixed prefix. Native success or other termination only improves it. The learned continuation matrix has l1 norm at most gamma<1, so its resolvent exists with norm at most 1/delta. Positivity removes S7's signed-model denominator delta-gamma e.

For M successive macros, condition on agreement at each macro boundary. Both the latent label and observed record then match, even though the physical memory was retained. Each next macro has conditional agreement probability at least q=delta/(delta+gamma t), regardless of its adaptive selection from that record. Induction gives agreement at least q^M. Independence of macro inputs is neither assumed nor needed. For predetermined varying clocks, multiply the corresponding q factors. Unbounded adaptive reuse needs its own bound on total work or stopping rule; this is a fixed-M guarantee.

Sharpness uses one latent state: true output always 0; fitted output equals 1 with probability t. The exact joint-column error is 2t. Under the fitted model the chance of seeing no 1 before abort is exactly q. True transcripts contain no 1, so TV is exactly 1-q. After M clocked macros, TV is exactly 1-q^M. At fixed H it is exactly 1-(1-t)^H.

## 5. Retention, initialization, and conditioning scope

The intended rho_1=rho_0 convention makes c_0 exact. If initial fitted distribution has TV error t_0, replace the agreement bounds by (1-t_0)(1-t)^H and (1-t_0)q^M.

This is a uniform **whole-law** guarantee, not a uniform posterior guarantee after every particular history. If a common conditioning event has true mass p>beta and the full laws have TV at most beta, its fitted mass is positive and

    TV(P(.|E),Phat(.|E))<=beta/p.

Indeed, writing mu=P restricted to E minus Phat restricted to E and q_E=Phat(E), conditional TV is at most [||mu||_1+|p-q_E|]/(2p). The complement's l1 distance is at least |p-q_E|, giving the bound. Symmetrizing gives beta/max(p,q_E). If beta>=p the fitted event can have probability zero. Rare filtering therefore still pays inverse history mass.

For physical quotient comparisons, let

    mu_g=max_j ||q_j||_Q <= max_j sum_k |S_kj|

for normalized cores. Mapping the joint abstract terminal-state law back to V gives branch-summed quotient-norm error at most 2 mu_g beta. The classical transcript bound needs no mu_g. This does not bound the full hidden-memory trace norm, because observational null directions have been removed, and does not imply a CP approximation.

## 6. Sharp rank-two rare-mode lower bound

Use diagonal qubit memory states |0>,|1>. Fix known eta in (0,1). Each independent full-process start prepares

    rho_0=(1-eta)|0><0|+eta|1><1|.

The only unknown is theta in {0,1}. Define a finite time-homogeneous action library:

    Herald h:
      T_(h,0)(X)=X_00|0><0|,
      T_(h,1)(X)=X_11|1><1|.

    Probe p:
      T_(p,1)^theta(X)=theta X_11|1><1|,
      T_(p,0)^theta(X)=X_00|0><0|+(1-theta)X_11|1><1|.

    Erase e (single outcome):
      T_e(X)=Tr(X)|0><0|.

All maps are CP, since each term X_jj|i><i| has Kraus operator |i><j| times its nonnegative coefficient's square root. Each action's outcome sum is TP. The maps do not change with time. The start is invariant under the nonselective herald and probe; erase is a legal controlled action returning to the common state, not an independent full-process start.

The reachable span is exactly the two-dimensional diagonal space: rho_0 and its erased state are linearly independent. Herald distinguishes the two populations, so the observable quotient has exact predictive rank two. In particular the learner may have a supplied exact rank upper bound two.

Normalized legal core preparations rho_1=rho_0 and rho_2=|0><0| after erase, with empty and herald-1 tests, give

    H=[[1,1],[eta,0]],  det H=-eta.

Thus the obstruction persists with a full normalized exhaustive core. Let

    C=[[1-eta,1],[eta,0]],
    S=C^{-1}=[[0,1/eta],[1,-(1-eta)/eta]].

Its columns sum to one and c_0=S^{-1}e_1=(1-eta,eta). The corrected gauge W is exactly the physical stochastic two-state instrument. Granting the learner eta, this true gauge, and all maps except the rare probe bit only strengthens the learner and does not change the lower bound.

The legal positive-probability history h=1 produces normalized input |1><1|. Its next probe output is theta, so the two models' laws from this reachable input have TV separation one.

**Reset-limited theorem.** Let any randomized adaptive acquisition strategy use at most R independent full-process starts, with arbitrarily many native interventions per episode and unlimited computation. Couple all start bits and the policy randomness. On the event that all R potential starts select state 0, every action and outcome is identical in both models forever. This event has probability

    q_R=(1-eta)^R.

Drawing unused potential start bits in advance also covers adaptive stopping. Therefore the acquisition transcript laws obey

    TV(P_0^acq,P_1^acq)<=1-(1-eta)^R.

Counts are functions of transcripts, so this is also a lower bound against every legal count learner. For any target epsilon<1/2 on the next-probe law from the normalized input after h=1, the two acceptable output sets are disjoint. Turning an accurate predictor into a binary test gives

    max_theta Pr_theta[prediction TV error>epsilon]
      >= (1-eta)^R/2.

The elementary testing inequality is [P_0(A)+P_1(A^c)]/2 >= [1-TV(P_0,P_1)]/2 for any acceptance set A. Hence failure probability at most alpha for both models requires

    R >= log(1/(2alpha))/[-log(1-eta)]
      = Omega(log(1/alpha)/eta) for small eta.

This bound is sharp. Herald each episode; on the first h=1, perform one probe to determine theta exactly and stop. If all R heralds fail, guess uniformly. Failure is exactly (1-eta)^R/2. The maximum native cost is R herald calls plus one probe, and the start cost is R. Rare successful preparation is paid, including all failed heralds. Arbitrarily many calls inside a common-state episode do not replace starts.

For every finite R, an eta can be chosen so small that failure approaches 1/2. Thus rank alone does not give a finite uniform sample bound. At a fixed eta, the result is a quantitative resource requirement, not impossibility at all finite budgets.

**Intervention dependence.** Add a known activation action with success probability lambda in [0,1), represented by physical population matrices

    M_(a,0)=[[1-lambda,0],[0,0]],
    M_(a,1)=[[0,0],[lambda,1]].

It moves common state 0 to rare state 1 on a heralded success; state 1 stays rare. These are again stationary CP instruments. With at most R starts and A activation calls, coupling all opportunities shows

    TV(P_0^acq,P_1^acq)
      <=1-(1-eta)^R(1-lambda)^A,

    worst-case prediction failure
      >=(1/2)(1-eta)^R(1-lambda)^A.

Therefore a necessary tradeoff is

    R[-log(1-eta)]+A[-log(1-lambda)]>=log(1/(2alpha)).

For small probabilities, R eta+A lambda must be of order log(1/alpha). Only activation calls contribute the second term; taking A equal to all native calls weakens but preserves the lower bound. The product exponent is achieved by heralding starts, distributing A activation attempts among common episodes, probing once upon the first success, and guessing only if every opportunity fails. Its maximum native cost is R+A+1. Thus the resource separation and exponent are exact under those two opportunity budgets.

With lambda=0 the reset obstruction survives unbounded within-episode calls. With eta=0 and lambda>0, resets do not create the rare mode; Omega(1/lambda) activation calls are required. In that case normalized cores can be the common start and one outcome-discarded activation, giving H=[[1,1],[0,lambda]] with determinant lambda.

**Clock and unconditional-law limitation.** From rho_0 with lambda=0 the two models' entire unconditional within-episode laws differ by at most eta, however long the episode runs. The common component of mass 1-eta is identical. The obstruction concerns uniform prediction on all normalized reachable inputs, including rare conditioning, or uniform e certificates giving the rare state full weight. It does not rule out useful unconditional starting-state prediction.

From the normalized rare state, one probe preceded by the delta abort coin has model separation gamma. M such sequential retained-memory macros have separation 1-delta^M. From rho_0 both acquire the eta prefactor. The deployment abort clock does not manufacture acquisition access to the rare mode.

In the common physical gauge the two true rare probe columns have l1 distance 2. Any single fitted stochastic instrument therefore has e>=1 for at least one compatible model, by triangle inequality. A small uniform e cannot be promised without resolving theta. The zero entries in this exact lower-bound example may prevent a generic robust-box positivity certificate; the information lower bound does not depend on that certificate's particular implementation.

## 7. Nonphysical virtual vertices with strict positivity

Here is a rank-two CP process for which demanding physical vertices would incorrectly reject a valid positive realization. Let physical diagonal-state population dynamics be

    P=[[3/4,1/4],[1/4,3/4]],
    M_1=P diag(1/4,3/4),
    M_0=P diag(3/4,1/4).

Add single-outcome erase M_e=e_1 1^T. Start at (1/2,1/2). Core preparations are start and its erased state, and tests are empty and probe outcome 1. Then

    C=[[1/2,1],[1/2,0]],
    F=[[1,1],[1/4,3/4]],
    H=FC=[[1,1],[1/2,1/4]],  det H=-1/4.

Choose virtual physical-population columns

    U=[[11/10,-1/10],[-1/10,11/10]],
    S=C^{-1}U=[[-1/5,11/5],[6/5,-6/5]].

Each vertex has a negative physical population. Yet c_0=(1/2,1/2), 1^T S=1^T, and the gauged matrices are

    W_1=(1/480)[[83,107],[13,277]],
    W_0=(1/480)[[277,13],[107,83]],
    W_e=[[11/12,11/12],[1/12,1/12]].

They are strictly positive, and every joint action column sums to one. The smallest entry is 13/480. This is an open positivity regime with a fixed rational S: sufficiently narrow rigorously propagated confidence intervals can certify it. These are exact mathematical parameters, not claimed acquired sample data. This example validates the virtual-vertex reasoning; it supplies no sample-cost advantage.

## 8. Comparator and remaining limits

An equally informed controlled-HMM, PSR, OOM, or CP-fitting competitor can use the same counts, S search, stochastic fit, certificate, coupling, and sharp rare-mode acquisition strategy. No novelty, priority, learning separation, physical computational advantage, or practical speedup is proved here.

The principal subsequently supplied explicit read-only authorization for `counts.json`, `exact_certificate.py`, `rational_certificate.json`, and `POSITIVE_GAUGE_THEOREM.md`. The rank-two count certificate was independently replayed and challenged as recorded in section 9. The original frozen rank-four fixture scan and private-plant scoring were not read or replayed; those empirical claims remain the principal's evidence.

The principal's proposed coherent rank-three obstruction is consistent with the mathematics: for a finite positive HMM, the stochastic matrix P representing a discarded-outcome rotation action gives response f^T P^n c asymptotic to a finite periodic sequence. If a qubit gives (1+cos(2n theta))/2 with theta/pi irrational, then on each residue class the quantum response is dense in [0,1]. Any such periodic limiting prediction has uniform error at least 1/2. This observation assumes a valid finite stochastic (or appropriately bounded substochastic) model, and does not reject signed finite-dimensional predictors, CP models, finite-horizon approximation, or paid-clock approximation.

The strongest remaining certificate obligation is computable count confidence geometry that supplies a useful joint-column e, strict/structural positivity where required, and exact causal normalization at the actual paid resource budget. The sharp transcript bound solves deployment stability once those premises hold; it does not remove acquisition conditioning or rare-mode access costs.

## 9. Independent replay of the actual count certificate

**Result: PASS at the stated conditional scope.** The authorized count-only script and count file were copied into the owned `helper/replay` directory before execution. The generated `rational_certificate.json` was byte-identical to the separately copied reference certificate. Source hashes are recorded in `replay/input_hashes.json`. An independent exact `fractions.Fraction` implementation in `replay/independent_check.py` then reconstructed the events and interval algebra without importing the principal's script, plant, generator, scoring code, or any other trajectory. Its complete result and legal-event manifest are in `replay/INDEPENDENT_CHECKS.json`.

The code and algebra checks establish:

* All seven count tables contain every binary outcome string of the appropriate length, nonnegative integer counts summing to one million, and unique action settings. Their budgets sum exactly to 7,000,000 starts and 14,000,000 native interventions.
* The preparation `[0]` is correctly implemented by discarding its outcome. H's second row uses the final action-1 outcome; each shifted entry constrains the primitive outcome and, for the nonempty test row, the appended test outcome. All required tables exist. The extracted H is `[[1,1],[250175/1000000,675085/1000000]]`.
* There are 18 estimated matrix-entry slots, consisting of two nontrivial H entries and sixteen shift entries. Two shifts reuse the same event as an H entry, leaving 16 distinct extracted events. Taking K=18 is a valid conservative union count. Independence between slots is unnecessary. The claimed uniform width 21/10000 and N=1,000,000 give exponent 441/50 and failure bound `36 exp(-441/50)`, approximately 0.00531894096835321. An exact positive Taylor-series sandwich independently proves this is below 0.01.
* The selected S is `[[5/4,-1/4],[-1/4,5/4]]`, has exact column sums one, and gives exact initial vector `(5/6,1/6)`. No estimated initial probability is being substituted.
* With U=(Hhat S)^{-1}, A=|U|D_V, the exact maximum row sum is `420/42491<1`. The computed nonnegative M satisfies `(I-A)M=|U|` exactly. This is the correct Neumann entrywise inverse majorant. Independently, the true H determinant remains in `[42071/100000,42911/100000]` on the confidence box, so it cannot vanish.
* The residual identity is correctly ordered: `(HS)(What-W)=(Hhat_z-H_z)S+(HS-Hhat S)What`. Consequently `E_z=M[D_z|S|+D_V|What_z|]` is valid without assuming commuting matrices. Every reported rational entry of What and E was reproduced independently. In addition, 256 exact H/shift-box corner challenges satisfy the inverse majorant, exact residual identity, entry error bounds, and positive lower inequalities. These corner checks supplement the algebraic proof; the Neumann/residual proof, rather than a finite corner sample, covers the full continuous confidence set.
* The fitted kernels have exact branch-summed stochastic columns. The smallest robust lower entry equals `30002740030003/1430111088800000>0`, approximately 0.0209793073. Thus both true and fitted models are positive on the confidence event.
* The box-simplex TV calculation was independently checked by enumerating its vertices: fix any three of four coordinates at lower/upper bounds and determine the fourth by normalization, retaining feasible points. Its maximum l1 distance divided by two exactly matches the script's sixteen-subset formula for every action/column. The overall maximum is `4121523/210355000`, approximately 0.0195931782. This maximum is exact for the outer box-simplex intersection; it need not be attained by a CP process or jointly consistent uncertain matrices, which only makes the bound conservative.
* At delta=2/5, the one-macro and two-reuse fractions reproduce exactly as `12364569/433074569` and `10556678214535761/187553582314535761`, approximately 0.0285506698 and 0.0562861988.

The principal then explicitly authorized `learner.py:frozen_spectral_bound`, resolving the old-bound comparison. That function uses the tighter valid bound kappa_bar=khat+2 Jbar dH Jhat, where khat=||Hhat^{-1}||_(infinity->1), rather than the coarse 2 Jbar. The bound follows from ||H^{-1}-Hhat^{-1}||_infinity<=Jbar dH Jhat and ||A||_(infinity->1)<=2||A||_infinity. Independent exact rational reconstruction gives khat=292526/42491, kappa_bar=2932295357/417874643, e=103148723329687245/174619217262377449, approximately 0.590706595452774, and signed-resolvent bound 309446169989061735/39792264535693163, approximately 7.776540832741309. Thus the stated approximately 0.590707 is confirmed; approximately 7.80 is a rough display of the vacuous 7.77654 result. The current-data condition gamma e<delta holds. The function needs that precondition and nu<1 if reused elsewhere; the present certificate checks them.

For comparison, the literal coarse kappa=2 Jbar gives e approximately 0.674886829 and fails the signed-resolvent condition. Other valid tighter estimates give e approximately 0.589289333 and bound 7.61578754, or e approximately 0.585317843 and bound 7.19516050. All remain vacuous for the intended classical-law comparison. The exact reconstructions and the authorized function fragment/hash are in `replay/S7_SAME_COUNTS_CHECK.json` and `replay/frozen_spectral_bound.py.txt`. This comparison against sufficient S7 estimates proves no advantage over an optimized equally informed HMM learner.

The supplied CP stationarity, independent repeatable episode starts, action calibration, architectural upper bound two, and synthetic sampling provenance are assumptions of the source interface. Count totals alone cannot prove them. No physical acquisition, private-plant identity, true laboratory process, private scoring result, original-fixture failure, novelty, or incumbent advantage was verified by this replay. The verified achievement is a nonvacuous exact-rational count-confidence certificate for the supplied synthetic count artifact under its explicit acquisition assumptions, and the resulting complete classical transcript/reuse guarantees.

## 10. Overcomplete cone extension: independently confirmed

The principal explicitly authorized `OVERCOMPLETE_CONE.md` and `overcomplete_fixture.py`. Both were copied into owned `helper/overcomplete_replay`, and only the owned script was executed because it writes its output. It passed. The independent reconstruction `overcomplete_replay/independent_overcomplete.py` also passes; its exact results are in `INDEPENDENT_OVERCOMPLETE_CHECKS.json`. No count acquisition is claimed for either algebraic fixture.

**General correction theorem.** Work in normalized preparation coefficients. Let V be r by q of full row rank, with 1_r^T V=1_q^T, and fix a right inverse L with V L=I_r. Multiplying the mass identity by L proves 1_q^T L=1_r^T; this is a consequence, not an extra assumption. For a fitted stochastic joint kernel Khat_z and true C_z=H^{-1}H_z, set

    K_z=Khat_z+L(C_z V-V Khat_z).

Then V K_z=C_z V exactly. The correction can equally be written

    K_z-Khat_z=L H^{-1}(H_z V-H V Khat_z).

If |H^{-1}|<=M_H on the count-confidence event, write

    Rhat_z=Hhat_z V-Hhat V Khat_z,
    E_z=|L|M_H[|Rhat_z|+D_z|V|+D_H|V Khat_z|].

The bracket bounds the exact residual because

    H_z V-H V Khat_z
      =Rhat_z+(H_z-Hhat_z)V-(H-Hhat)V Khat_z.

Therefore |K_z-Khat_z|<=E_z. A verified Khat_z-E_z>=0 proves true positivity, with the fitted nonnegativity following as well.

For any action, the summed correction has zero mass:

    sum_o 1_q^T(K_z-Khat_z)
      =1_r^T sum_o C_z V-1_r^T V sum_o Khat_z
      =1_q^T-1_q^T=0.

Here both true causality and the fitted stochastic constraint are load-bearing. Hence K_z is a true stochastic lift, despite not being unique. If eta>=0 and V eta=e_1, mass normalization gives 1_q^T eta=1, and induction gives V K_w eta=C_w e_1. All true word probabilities, feedback laws, and the previous full-transcript coupling follow exactly. No physical preparation of vertices or of the lifted labels is assumed.

**LP statement.** For fixed rational V,L and count estimates/widths/M_H, the feasibility reduction is correct. Introduce nonnegative U_z>=+/-Rhat_z and B_z>=+/-V Khat_z. Impose

    Khat_z>=|L|M_H[U_z+D_z|V|+D_H B_z],
    Khat_z>=0,
    sum_o 1_q^T Khat_(a,o)=1_q^T.

These are linear equalities and inequalities in Khat and the auxiliaries. Conversely, if the original absolute-value inequalities hold, choosing the auxiliaries equal to their absolute values gives a feasible LP point. Initial eta feasibility is another LP. A positive scalar margin can be added linearly. This proves a finite fixed-cone feasibility formulation; searching V,L or selecting q remains nonconvex/unbounded and is not solved. The code does not implement a general LP search, and no such implementation or runtime advantage should be inferred.

**Rank-three versus four-state fixture.** Let lambda=13/20 and use Bloch coordinates (t,x,z). The rotation/depolarization map is R(t,x,z)=(t,lambda z,-lambda x). It is a unitary conjugation mixed with complete depolarization. The readout branches are CP measure-and-prepare maps with effects (I+/-Z/2)/2 and output states with Bloch z=+/-1/2. Their effects sum to I.

An explicit normalized legal core consists of start +Z, one discarded-outcome R, and two discarded-outcome R calls, with Bloch-column matrix

    B=[[1,1,1],[0,lambda,0],[1,0,-lambda^2]].

Its determinant is -lambda(1+lambda^2), nonzero. Empty, M+, and R-then-M+ tests have row matrix

    F=[[1,0,0],[1/2,0,1/4],[1/2,-lambda/4,0]],

whose determinant is lambda/16. Thus H=F B is nonsingular. The real Bloch plane plus trace is invariant, so the minimal observable rank is exactly three.

Any three-state exact positive realization would be minimal and therefore similar to this rank-three realization. Its nonnegative rotation matrix P would have eigenvalues 1,+i lambda,-i lambda, giving tr(P)=1 and tr(P^2)=1-2lambda^2=31/200. But

    tr(P^2)=sum_i P_ii^2+2 sum_(i<j)P_ij P_ji
            >=sum_i P_ii^2 >=[tr(P)]^2/3=1/3.

Since 31/200<1/3, three states are impossible. This rules out every square rank-three positive gauge, not just the scanned family.

The four cardinal Bloch vertices admit the explicit positive lift in the principal's code. Independent exact computation verifies V_B K_R=R V_B, all readout intertwinings, all stochastic identities, rotation margin 7/80, and measurement branch margin 1/32. The initial +Z state is the first vertex. Thus four is the minimum positive dimension for this fixture: rank requires at least three, three is impossible, and four exists.

**Coordinate caveat.** The fixture's V_B and L_B are written in Bloch coordinates, whose trace covector is (1,0,0), rather than normalized preparation coefficients whose trace covector is 1_r^T. Thus literally 1_r^T V_B=1_q^T does not hold in the displayed Bloch matrices. This is a coordinate convention, not a failed fixture. The explicit legal-core translation

    V_p=B^{-1}V_B,        L_p=L_B B

satisfies V_p L_p=I_r, 1_r^T V_p=1_q^T, and 1_q^T L_p=1_r^T. It maps the first lifted vertex to e_1 and satisfies the count-coordinate intertwining with H=F B. The independent script verifies this translation exactly, so the fixture genuinely instantiates the general theorem after this explicit change of coordinates.

To challenge more than the zero-residual identity, the independent script perturbs each fitted kernel by a small mass-preserving nonzero term, uses nonzero abstract uncertainty widths, and applies the proposed correction. It verifies exact intertwining and causal sums of the corrected lift, the full entrywise error majorant, and a positive certified lower margin. These are algebraic intervals around known constructed maps, not sampled confidence intervals or acquired data.

This extension is valid and strictly enlarges the square mechanism. It preserves the same rarity, inverse-information, finite-confidence, search, and virtual-state limitations. It establishes neither universal finite-positive learnability nor an acquired rank-three example. An equally informed positive-realization/HMM competitor can use the same LP and certificate.
