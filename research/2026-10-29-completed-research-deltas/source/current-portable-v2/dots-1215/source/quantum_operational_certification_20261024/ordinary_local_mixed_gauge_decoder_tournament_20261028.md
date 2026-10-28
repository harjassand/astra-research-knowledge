# Local hidden-algebra acquisition with arbitrary quantum gauges

28 October 2026. **Constructive proof candidate; independent review in progress.** No new source simulation or hardware experiment is reported. This follows the received hidden-common-algebra theorem and the separately received 73,064-call flat-gauge local pilot; it does not silently extend that pilot's empirical certificate to this family.

## 1. Contract, target, and the actual new difficulty

Let n,w be integers with 1<=w<=n. There are n KNOWN physical output qubits on a known nearest-neighbor line, and supplied real unit-vector encoders x in R^4. Source calls reset independently. For unknown U and unknown positive matrix-valued quadratics G_alpha(x), assume

    E_x(omega)=U[sum_alpha sigma_alpha omega sigma_alpha tensor G_alpha(x)]U†,
    G(x)=sum_alpha G_alpha(x),  Tr G(x)=1,
    H_j(x)=sum_alpha chi_(j,alpha)G_alpha(x)>=0  (j=X,Y,Z).       (1)

Here U may be taken as an unknown unitary from one logical qubit and n−1 gauge qubits to the physical register. Gauge matrices may be noncommuting, rank changing, entangled across physical patches, and arbitrarily ill-conditioned. The Pauli/instrument index alpha is not supplied or measured. No source environment, source inverse, protected reference, flag, gauge eigenbasis, or retained unknown-output frame is used.

Let bars denote the uniform mixture of the four supplied encoder anchors. Promise

    Hbar_X>=kappa Gbar,  Hbar_Z>=kappa Gbar,  0<kappa<=1.        (2)

The exact common logical reflections B_j=U(sigma_j tensor I)U† satisfy the Pauli algebra. BOTH B_X and B_Z are supported on ONE unknown physical interval of width at most w. A valid w and geometry are supplied, not the interval or generators. If only separate width-w intervals are promised, their true supports must overlap, so substitute W=min(n,2w−1) throughout. Learned supports need not overlap. Gauge flatness is NOT assumed. This is still a strong structural-family theorem, not generic discovery or a test of family membership.

The target is a decoder D and encoder xhat with averaged Bell loss at most (1+gamma)ell_star+epsilon against the optimal encoder and unrestricted CPTP decoder on the ORIGINAL source. Take 0<epsilon,gamma<=1. Known ordinary input controls and the entire finite receiver process are paid. The new bridge is unknown-patch acquisition without relying on flat-gauge sparse coefficients. A useful decoder on each local candidate can be learned by conventional local tomography; the remaining task is choosing one despite gauge aliases and an unknown nonzero calibration noise floor.

## 2. The received global theorem supplies three local ingredients

The imports here are `ordinary_hidden_common_algebra_acquisition_20261028.md`, especially Sections5–6 and9, and `ordinary_bures_matrix_query_confidence_20261027.md` Section2. Their finite physical estimators, not abstract state oracles, are used.

Write

    rho=U[I/2 tensor Gbar]U†,
    E0(omega)=U[omega tensor Gbar]U†,
    r_(j,s)=U[(I tensor Gbar+s sigma_j tensor Hbar_j)/2]U†,
    X_j=(r_(j,+)−r_(j,−))/2.

For j in {X,Z}, [B_j,rho]=0, X_j=B_j|X_j|, and kappa rho<=|X_j|<=rho. For any actual CPTP D, let ell0(D)=ell(D E0). The received gauge-POVM argument establishes the unrestricted optimum ell_star(x)=1−Tr G_I(x) and

    0<=ell(D E_x)−ell_star(x)<=4 ell0(D),  for ALL x.           (3)

This follows from G(x)<=4Gbar, not a generic sup/average continuity shortcut.

On the TRUE interval I_*, the reduced ordinary pairs have the SAME relative-sign property: B_j is local, partial trace gives X_j^I=B_j^I Tr_out|X_j|, and

    |X_j^I|=Tr_out|X_j|>=kappa rho_I,  [B_j^I,rho_I]=0.

Thus known-patch acquisition already permits arbitrary quantum gauges. Reduction of E0 is a perfect logical subsystem channel on that patch: its two exact Pauli reflections imply a local qubit/gauge tensor decomposition, and rho_I commutes with both.

For each axis, two normalized density estimates with root-fidelity deficits <=m and a certified TOTAL trace-norm backward residual eta<=m give a learned raw-sign reflection B'_j satisfying

    delta_j=Tr rho_I(B_j^I−B'_j)^2<=56m/kappa^2.               (4)

For arbitrary learned reflections X',Z', put P=(I+Z')/2 and implement the literal isometry

    V psi=|0> tensor P psi+|1> tensor X'(I−P)psi.              (5)

It is an isometry even when the two reflections do NOT anticommute. Trace its residual register. This CPTP decoder obeys

    ell0(D)<=2delta_X+(3/4)delta_Z<=154m/kappa^2               (6)

on the true interval. Every candidate decoder remains physical on every failed estimation history. Exact-reference reflections can be specified through rational range projectors Q(Q†Q)^−1Q†, with certified backward residual and arbitrary null-space completion. Finite implementation error is charged globally below.

## 3. Acquire every local candidate with colored parallel banks

There are M=n−w+1 width-w intervals. Color their starting positions modulo w; q=min(w,M) colors suffice and intervals of one color are disjoint. For each color and each ordinary j=X/Z,s=± bank, use N_B source calls with independently uniform anchors. A single source output is split into its disjoint physical interval registers. Run the known finite Bures estimator on each interval's N_B registers. No register is cloned or reused by two overlapping estimators in this bank.

Across intervals, the registers and their measurement outcomes CAN be correlated or entangled. Across independent source calls, each particular interval has iid marginal copies of r_(j,s)^I. Tensor products of local trace-preserving measurement instruments imply each individual estimator's outcome marginal is exactly that of its ordinary local Bures experiment. Union-bound confidence requires no independence across patches. Fix each estimator's control policy before the bank, with adaptation only to its OWN local records; do not condition its guarantee on other patches' outcomes or the per-copy anchor labels.

Set d=2^w and D0=d^2=4^w. For beta_A>0 and 0<m<=1/16, use

    N_B=ceil[(80*4^w/m) log(48*4^w*M/beta_A)].                (7)

There are four state estimates per interval, each with failure at most beta_A/(4M). Source cost is EXACTLY 4qN_B, not 4MN_B. The imported random-purification channel, finite-Clifford estimator, certified near-top eigenvector and partial trace all count; this is a collective receiver with quantum storage, NOT the previous single-copy-shadow/count-only pilot.

Construct all M candidate decoders by (5) and freeze them. On the calibration good event at least one satisfies (6); no promise says other patches fail. Gauge aliases may yield additional genuinely good decoders, which is harmless. No support score, learned gap, supplied gauge coefficient, or exact word identification is inferred.

## 4. Excess two-axis calibration risk controls ideal extraction loss

For any physical candidate D, define its ACTUAL Heisenberg contractions

    A_j^D=D†(sigma_j),  ||A_j^D||<=1,
    t_jj=Tr rho B_j A_j^D,
    ell0(D)=(3−t_XX−t_YY−t_ZZ)/4.

The t_jj are those of the actual qubit channel D E0; they are proof quantities, never given to the learner. Define e_j(D) as the ordinary binary error when s is uniform, input P_(j,s) is sent through the uniform anchor mixture, D is applied and sigma_j is measured. Let g(D)=[e_X(D)+e_Z(D)]/2. The common ideal subsystem decoder has value g_*, unknown to the learner. Put r(D)=g(D)−g_*.

Since K_j=I−{B_j,A_j^D}/2 is positive and Tr rho K_j=1−t_jj,

    e_j(D)−e_j(*)=(1/2)Tr |X_j|K_j,
    (kappa/4)sum_(j=X,Z)(1−t_jj)<=r(D)
                          <=(1/4)sum_(j=X,Z)(1−t_jj).       (8)

No commutation of Gbar and Hbar_j is assumed: the inequalities pair the positive K_j with the relative operator bounds. For every CPTP qubit channel, its Pauli-twirl probabilities p_alpha are nonnegative; therefore

    2ell0<= (1−t_XX)+(1−t_ZZ)<=4ell0.

Consequently

    (kappa/2)ell0(D)<=r(D)<=ell0(D).                        (9)

In particular r is an EXCESS risk, not raw noisy calibration error. It is nonnegative for every candidate, including failed acquisitions. The unknown noise floor g_* will cancel physically, not be estimated.

## 5. A measurable decoder-difference observable with small variance

For two frozen decoders a,b, independently choose j in {X,Z}, s in {±1}, and one encoder anchor, all uniformly. Prepare the ordinary P_(j,s) input and on its physical output measure

    H_(j,s)=s(A_j^b−A_j^a)/2,  ||H_(j,s)||<=1.               (10)

This is a known Hermitian observable. It is NOT a supplied logical measurement and NOT independent runs of two noisy decoder tests. The learned controls specify its spectral measurement on the UNION of the two candidate patches. If its real outcome is Z, direct averaging gives

    E Z=g(D_a)−g(D_b)=r_a−r_b,
    E Z^2=(1/8)sum_(j=X,Z)Tr rho(A_j^a−A_j^b)^2.             (11)

For each contraction A_j, (A_j−B_j)^2<=2I−{A_j,B_j}, so

    sum_(j=X,Z)Tr rho(A_j−B_j)^2<=8ell0(D).

The operator square inequality (A−C)^2<=2(A−B)^2+2(C−B)^2 then proves

    E Z^2<=2[ell0(D_a)+ell0(D_b)]<=4(r_a+r_b)/kappa.         (12)

Thus BOTH the common noisy mean and its constant variance floor are removed. Merely subtracting independent error counts would not have this property.

It is essential to use the actual pullbacks of (5), not pretend its raw signs anticommute:

    A_Z=Z',
    A_X=P X'(I−P)+(I−P)X'P=(X'−Z'X'Z')/2.                 (13)

These are supported on their learned patches and are computable from the controls. The literal isometry or its adjoint proves (13).

### Finite spectral measurements without a spectral-gap assumption

For each comparison axis define the UNSIGNED H_j=(A_j^b−A_j^a)/2. Construct a known Hermitian C_j with ||C_j−H_j||_infinity<=xi and ||C_j||<=1, represented as C_j=V_j diag(c_l)V_j†. Here V is a known exactly unitary finite-gate reference circuit and the c_l in [−1,1] are rational. Measure V_j† followed by computational-basis readout and return the rational s*c_l. Integer eigenlabel counts and the known rational labels determine the empirical mean. For the following variance statements C means this signed observable s*C_j. A binary POVM (I±C)/2 returning ±1 is NOT a substitute: it preserves only the mean and has second moment one, destroying the fast comparison bound. No unknown spectral projectors or infinitely precise outcome numbers are supplied.

One can obtain this representation by approximate Jacobi diagonalization and rounding the diagonal inside [−1,1], then certify the TOTAL backward residual; the target is an approximated observable, NOT closeness of individual eigenvectors. For a d_c-by-d_c Hermitian matrix, a maximum-offdiagonal exact plane rotation decreases squared offdiagonal Frobenius mass by at least a fraction 2/[d_c(d_c−1)]. O(d_c^2 log(d_c/xi)) rotations therefore suffice to reach the target. Finite plane-rotation errors and coefficient rounding can be given a smaller total residual budget before the final certificate. Pairs smaller than the target residual do not require division by a spectral gap. Alternatively any certified finite diagonalization achieving this reference representation suffices. Exact rational Givens parameterizations or exact-reference one-qubit rotations followed by paid finite gate synthesis preserve unitarity.

The implemented-reference outcome C has mean bias <=xi and second moment at most 4(r_a+r_b)/kappa+2xi, since ||C^2−H^2||<=2xi. Set

    xi<=kappa*t/4096,
    L=log[2(M−1)/beta_Q],
    N_pair=ceil[512 L/(kappa*t)] .                          (14)

For M>=2, Bernstein for each fresh conditional comparison batch yields, except probability 2exp(−L),

    |Zbar−(r_a−r_b)| <= (1/4)sqrt[t(r_a+r_b)]+t/96.         (15)

For example the variance term's leading coefficient is only 1/8, while bias, extra second moment and centered-range term fit the displayed additive allowance. Gate implementation discrepancy is accounted for once for the whole process; it is not disguised as a small spectral-projector distance at a vanishing eigenvalue gap.

## 6. Balanced tournament, finite confidence, and explicit constants

Use a fixed balanced bracket on the M frozen candidates, with byes where needed; h=ceil(log2 M). Each comparison has the fixed cap (14), fresh ordinary inputs, and winner chosen by the sign of Zbar (smaller empirical g wins). Its identity can depend on earlier comparison records. Conditional concentration is valid because every new source bank resets independently and its controls are known from previous data. There are M−1 comparisons. A union bound with the L in (14) costs at most beta_Q regardless of within-batch quantum correlations inherited from fixed source structure; source copies themselves are iid.

On (15), if a comparison mistakenly retains the larger risk m+d over the smaller m, then

    d<=(1/4)sqrt[t(2m+d)]+t/96.

Splitting the root and using (1/4)sqrt(td)<=d/2+t/32 gives

    d<=(1/2)sqrt(2tm)+t/12<=eta*m+t/(4eta),  0<eta<=1.

Thus each winner obeys

    r_win<=(1+eta)min(r_a,r_b)+t/(4eta).                    (16)

Follow the branch containing a minimum-risk candidate, through at most h levels, and set eta=1/(2h). Since (1+eta)^h<2, the total additive accumulation is at most t h^2. Hence

    r_selected<=2r_min+t h^2.                              (17)

For a uniform decoder-regret target epsilon/20, choose

    m=kappa^3 epsilon/2^17,
    t=kappa epsilon/(320 h^2).                             (18)

Equation (6) gives r_min<=154m/kappa^2<kappa epsilon/640. Equations (17)–(18) give r_selected<=kappa epsilon/160, and (3),(9) give

    ell(D_selected E_x)−ell_star(x)<=epsilon/20  for ALL x. (19)

For M=1 skip the tournament and use the one decoder; (6) gives an even smaller regret at the same m. Do not evaluate log(M−1) or divide by h in that case.

The deterministic acquisition cap before encoder optimization is

    N_acq=4q ceil[(80*4^w/m)log(48*4^w*M/beta_A)]
            +(M−1)ceil[163840 h^2 L/(kappa^2 epsilon)],    (20)

with the second term zero for M=1. This is a real n/epsilon selection cost. The earlier flat-gauge shadow theorem's logarithmic n query dependence is NOT preserved.

## 7. Freeze the decoder, then learn the encoder separately

After the tournament freeze D_selected. Its actual six-state error q_D(x)=2ell(D_selected E_x)/3 is a nonnegative ten-feature quadratic, including on bad calibration histories. Use the received ordinary Bernoulli active-design specialization at epsilon_q=epsilon/6, failure beta_C, L0=40 and S=56. Its deterministic cap is

    N_count<=56 b[J+6*2^20*40/(gamma epsilon)],
    J=ceil(log2[96/(gamma epsilon)]),
    b=smallest odd integer >=8log(112J/beta_C).             (21)

All actual decoder executions, ordinary source preparations and failed histories count. This is adaptive active encoder learning, unlike the completed pilot's fixed ten-point interpolation. Nothing here declares a noisy empirical interpolant PSD. On the joint good event,

    ell(D_selected E_xhat)<=(1+gamma)ell_star+7epsilon/20.   (22)

Take strictly positive beta_A,beta_Q,beta_C and allocate beta_A+beta_Q+beta_C<=beta<=epsilon/8, and a linked acquisition/selection/payload implementation discrepancy nu<=epsilon/8 in complete operational norm. Loss is bounded by one on all statistical failure histories. These allowances imply averaged risk <=(1+gamma)ell_star+epsilon with slack. A final payload call and its controls are additional to (20)–(21). A paid whole-logical Pauli twirl can be used if an exact Bell-loss-to-complete-error conversion is wanted; it is not silently assumed for the untwirled receiver.

The source bound, suppressing confidence and displayed logarithms, is

    O_tilde[w*4^w/(kappa^3 epsilon)
              + n/(kappa^2 epsilon) + 1/(gamma epsilon)].  (23)

No inverse smallest gauge eigenvalue occurs. There is no assertion that useful-optimum alone makes (2) automatic for arbitrary varying quantum gauges.

## 8. Actual memory, controls, and conventional comparison

Known physical output register and locality are indispensable. No generic rank-only common frame or free cross-frame alignment is imported. Every calibration source call emits n physical qubits. Sequentially processing bank/color combinations can store one full n*N_B bank at a time, plus the paid local Bures estimator workspace. Across all estimates, invoke 4M known d-dimensional Bures estimator circuits, each with N_B copies; receiver memory/control cost may scale polynomially with N_B and d and is NOT just the logarithm of the source count. Correlated outputs do not permit replacing these controls by simultaneous independent sample oracles. Locality of each physical output register does not make collective cross-copy memory controls free: specify a memory-bank interconnect, or compile every imported estimator circuit to a linear layout of ALL stored bank/workspace qubits, paying at worst a factor proportional to that workspace width in SWAP routing per abstract two-qubit gate. This extra factor is polynomial in the deterministic bank/workspace cap and can be enormous.

Each candidate sign and extraction is confined to w qubits. Dense known-matrix processing is polynomial in 2^w and precision; generic extraction synthesis is O(poly(w)4^w) elementary gates before precision overhead. A comparison acts on the union of TWO learned patches, at most 2w qubits. For disjoint distant patches the state may be entangled; measure the union observable on that actual state, not separately reconstructed marginals. Its dense spectral matrix has dimension at most4^w. A generic compiled known unitary costs O(poly(w)16^w) two-qubit/one-qubit controls before precision overhead; dense classical diagonalization may cost O(64^w) per numerical sweep. The explicit finite Jacobi fallback may use additional polynomial factors, which must not be mislabeled as the cubic bound.

A better actual implementation exploits the interval geometry. If the two patches overlap, their union is contiguous of width at most2w−1, and the known union observable is measured there with at most O(w) local routing overhead per generic two-qubit gate. If they are disjoint, their pullbacks commute. Diagonalize each learned local contraction separately, measure BOTH on the SAME physical source output, retain the ACTUAL joint outcomes a,b, and return s*(b−a)/2. This commuting product measurement has exactly first moment H_(j,s) and second moment H_(j,s)^2, even when the two patches are entangled. Never replace the joint experiment by independent-output tests or independently resampled marginals. Local backward approximations of each contraction within xi imply their half-difference error at most xi, while clipped individual labels keep the difference label in [−1,1]. Thus disjoint-patch comparisons need no long-distance coupling or routing. A generic gather-and-measure implementation would additionally pay O(nw) SWAPs, but is unnecessary for these interval candidates. This is still a measurement on the actual union, not a free marginal-operator oracle. Allocate compilation precision across ALL acquisition, comparison, count and payload invocations to meet the single nu budget. Known unitaries, resets, readouts, label bits, classical counts, and feedforward all count. The final deployed decoder uses only its selected width-w patch and has no tournament-sized support. Routing it to a fixed endpoint costs extra only if that endpoint is required. There is no constant-depth architecture claim for the selection stage, and no claim of recovering n logical qubits: this protects ONE logical qubit.

An equally informed conventional subsystem learner can use the SAME parallel local Bures candidates, physical difference measurements and tournament. No asymptotic or historical novelty separation is asserted. Comparing only against independent noisy scalar validation at epsilon^−2 would omit this legitimate stronger conventional procedure. The substantive extension over the completed local pilot is removal of known maximally mixed gauge while preserving finite ordinary-input source/control costs, at the stated polynomial-n query and collective-memory price. Unknown family violations, arbitrary noisy controls without a paid bound, long-range nonlocal algebras, and multiple logical qubits remain outside this contract.

## 9. Evidence and stopping boundary

This manuscript is a mathematical construction, not a new count-acquired experiment. Its inputs and controls are actual operational prescriptions with deterministic caps. Independent reviewers are checking (8)–(17), the correlated parallel marginal experiment, and finite union-patch controls. Frozen previous reports, counts, private source files, failed calibration and compiled decoders are unchanged. A review receipt and any deterministic diagnostic evidence will be bound separately; until then this new theorem remains a proof candidate.


## 10. Stronger coarse overlap localization before the fine tournament

The n/epsilon comparison term above is valid but avoidable under this SAME exact local-algebra promise. This section is the preferred construction. It is not a generic locality inference: its key identity uses an exact local anticommuting logical reflection and the gauge structure in (1).

### 10.1 A disjoint physical marginal has exactly no logical X contrast

Fix a padded width-w true interval I_* supporting B_X and B_Z. In (1), B_Z X_X B_Z=−X_X because B_Z anticommutes with B_X and commutes with the gauge operator U(I/2 tensor Hbar_X)U†. No commutation of Gbar and Hbar_X is required. If J is any candidate interval disjoint I_*, B_Z acts entirely on the register traced out when taking the J marginal. Invariance of partial trace under that conjugation gives

    X_X^J=Tr_notJ X_X=Tr_notJ(B_Z X_X B_Z)=−X_X^J=0.       (24)

On the true interval, by Section2,

    ||X_X^I_*||_1=Tr|X_X|=Tr Hbar_X>=kappa.                (25)

Thus nonzero local contrast need not identify the correct algebra, but it DOES identify a patch overlapping a true one. This statement would fail if the exact common local logical algebra were merely guessed from approximate individual fits.

### 10.2 Two coarse colored banks acquire a certified overlap

Use only the X+ and X− ordinary inputs for this phase, with the same q-color disjoint-bank schedule as Section3. For beta_0>0, set

    m0=kappa^2/512,
    N0=ceil[(80*4^w/m0)log(24*4^w*M/beta_0)].              (26)

There are2M coarse state estimates and2qN0 actual source calls. The imported root-fidelity guarantee and the trace-distance bound

    ||rho−tau||_1<=2sqrt(1−f(rho,tau)^2)<=2sqrt(2m0)

show that every coarse half-difference Xhat_X^J obeys

    ||Xhat_X^J−X_X^J||_1<=2sqrt(2m0)=kappa/8              (27)

simultaneously except probability beta_0. Compute each trace-norm score to certified additive error kappa/16; this is a finite known-matrix calculation with no eigenvalue-gap assumption. The true score is at least13kappa/16, while any disjoint patch score is at most3kappa/16. Choose the FIRST interval J whose score exceeds kappa/2 under a fixed ordering. On the good event a choice exists and J overlaps I_*. If no score passes, choose a predetermined interval anyway; all subsequent routines retain their deterministic caps and physical fallbacks. The bad event is paid, not postselected away. Scores certify overlap only GIVEN the family, not membership in the family.

### 10.3 Fresh fine candidate banks and the smaller tournament

Restrict candidates to ALL width-w intervals K overlapping the selected J. Their starts lie within w−1 of its start, so their number R is at most

    R_max=min(M,2w−1),                                    (28)

and they include I_* on the coarse good event. They form a contiguous list of possible starts. Use FRESH source banks; conditional on the complete coarse record, each bank is an iid experiment with fixed selected physical patches. Color these candidates by start modulo w, using at most q1=min(w,R_max) colors. Apply Sections3–7 to these R candidates. For a fully predetermined cap, use R_max instead of M in the fine N_B logarithm, h_max=ceil(log2 R_max), and L_max=log[2(R_max−1)/beta_Q]. Let

    N1=ceil[(80*4^w/m)log(48*4^w*R_max/beta_A)],
    m=kappa^3 epsilon/2^17.

If R_max>=2 choose t=kappa epsilon/(320 h_max^2) and Npair=ceil[163840 h_max^2 L_max/(kappa^2 epsilon)]; the actual height is no greater than h_max. If R_max=1, skip all comparison formulas and calls. The adaptive candidate list and bracket require no extra independence assumption: beta_A covers conditional fine calibration, beta_Q covers conditional fresh comparisons, and their probabilities remain valid after integrating over the coarse record.

A deterministic complete source cap, with R_max=1 comparison term zero, is

    N_total<=2qN0+4q1N1+(R_max−1)Npair+N_count+1.           (29)

The final +1 is the subsequent payload call; its receiver controls are included in the whole-process allocation. Use strictly positive beta_0,beta_A,beta_Q,beta_C with sum<=epsilon/8, and the same whole-process implementation allowance nu<=epsilon/8. For R_max=1 the unused beta_Q can be reassigned or simply left unused. The proof of (19) and (22) is unchanged. In separated form the source scaling is

    coarse: O_tilde[w*4^w/kappa^2], with log M confidence,
    fine:   O_tilde[w*4^w/(kappa^3 epsilon)], with log R_max,
    select: O_tilde[w/(kappa^2 epsilon)],
    encoder:O_tilde[1/(gamma epsilon)].                    (30)

The tilde hides the logarithms specified in (26),(29), not an n/epsilon term. Source dependence on n is logarithmic again, but physical output qubits, coarse local estimator invocations, record handling, quantum storage and control/routing are NOT logarithmic in n. In particular the coarse bank invokes2M local estimators and costs the collective memory architecture in Section8. Fine intervals all lie inside the expanded neighborhood of J, so comparison quantum routing is also local to a width at most3w−2 region.

### 10.4 Simpler competing construction: expand once, skip selection

After the SAME coarse overlap certificate, expand J by w−1 sites to either side, clipped to the physical boundary. The resulting known patch K has width W<=min(n,3w−2) and contains I_*. Run the received four-bank Bures/sign/extraction learner DIRECTLY on K with

    m_exp=kappa^2 epsilon/32768,
    N_exp=ceil[(80*4^W/m_exp)log(48*4^W/beta_A)].           (31)

It gives uniform decoder regret <=616m_exp/kappa^2<epsilon/20. Freeze that decoder and use the same encoder design. For the predetermined whole-process horizon use W_max=min(n,3w−2) in (31) to obtain N_exp,max, bounding every realized smaller-width bank, memory and control schedule. The actual decoder may still use the smaller realized patch. Complete source cost is at most2qN0+4N_exp,max+N_count+1 (including one final payload), without ANY tournament, and fine source scaling O_tilde(4^(3w−2)/(kappa^2 epsilon)). Controls and final payload decoder now act on width W, with generic extraction synthesis O(poly(W)4^W). This can be the simpler practical choice at small w; the smaller-patch tournament improves exponential dependence on w at the price of a more elaborate spectrum-valued comparison measurement and a further inverse-kappa factor. An equally informed conventional subsystem learner gets BOTH options. Neither route is claimed historically new or superior to every structured alternative.

**Status:** These additions are proof-level constructions, not a rerun of the completed local pilot. Independent reviewers are checking the exact marginal cancellation, score constants, conditional fresh-bank confidence, and both control architectures before receipt.
