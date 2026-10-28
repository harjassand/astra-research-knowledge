# Independent proof audit: local mixed-gauge decoder tournament

28 October 2026. **PASS for the mathematical acquisition, physical comparison, conditional confidence, coarse overlap localization, and separate encoder composition, subject to the stated source/control contract.** This is a proof review, not a simulation or new count-acquisition experiment. No previous pilot file, source, private parameter, or measurement record was changed or sampled. Final source SHA256: `b1102426bfb3af58483e0d84fedde59e9317a6c0bfaac0a9e59a761f4976a9be`. The companion statistics receipt binds this source, the imported received contracts, and this audit.

## 1. Local reduction and colored collective banks

The necessary promise is one common unknown width-w interval supporting both exact logical Pauli reflections, with a known physical output register and geometry. Separate width-w supports justify only a common width at most min(n,2w-1). The theorem does not infer that promise or identify the true interval exactly.

For the true patch I, locality gives X_j^I=B_j^I Tr_out|X_j|. Since B_j is a reflection commuting with |X_j|, the traced positive factor commutes with B_j^I, so |X_j^I|=Tr_out|X_j|. Partial trace preserves kappa rho <= |X_j| <= rho. The marginal sign problem therefore has the same relative margin, without a lower bound on a nonzero gauge eigenvalue. Commutation of the marginal rho_I with both local Pauli reflections gives a local logical-qubit/gauge decomposition. This is a proof of local correctability of the virtual ideal channel, not source access to that virtual channel.

The received raw-sign Bures bound and literal extraction give delta_X,delta_Z <=56m/kappa^2 and ell0 <=154m/kappa^2. The extraction V=[P;X'(I-P)] has V†V=P+(I-P)=I for any two exact reflections, whether or not they anticommute. Thus failed statistical acquisition does not produce a nonphysical candidate.

Coloring the M=n-w+1 starting positions modulo w uses q=min(w,M) colors, with disjoint patches per color. A source bank has N_B independent global output copies, although its patch subsystems may be entangled. Local trace-preserving instruments on other patches do not change one patch's outcome marginal. This remains true for a local adaptive estimator regarded as one overall instrument, provided its controls depend only on its own local records, not other patches or the hidden/shared anchor labels. Consequently each patch receives exactly its imported iid-marginal Bures experiment. There is no cloning or reuse of an overlapping physical register.

Four estimates per patch at failure beta_A/(4M), with the received dimension d=2^w and D0=4^w, give

    N_B=ceil[(80*4^w/m) log(48*4^w*M/beta_A)].

The source cost is 4qN_B, while the receiver really performs 4M collective estimation procedures. A union bound requires no independence across patches. One must not instead condition the local guarantee on another patch's observed record. The proof correctly does not do so. It would also suffice to control one fixed source-dependent true patch, but the stated all-patch confidence allocation is conservative and valid.

## 2. The unknown calibration floor cancels in a physical comparison

For any candidate decoder, A_j=D†(sigma_j) is a Hermitian contraction. With B_j the true reflection, K_j=I-{B_j,A_j}/2 is positive: Re<Bv,Av> <= ||v||^2. The trace t_jj=Tr rho B_j A_j is real because [rho,B_j]=0. The excess two-axis error is

    r(D)=(1/4) sum_(j=X,Z) Tr |X_j| K_j.

The relative operator margin gives kappa/4 times the sum of (1-t_jj) <= r <=1/4 times that sum. For the actual qubit channel D E0, Pauli twirling has nonnegative Pauli probabilities, so

    2 ell0 <= (1-t_XX)+(1-t_ZZ) <=4 ell0.

Hence (kappa/2)ell0 <=r<=ell0 for every candidate, including bad ones. The unknown nonzero noise floor is never estimated.

The candidate controls specify the actual pullbacks of their extraction. In particular, A_Z=Z' and A_X=(X'-Z'X'Z')/2; treating X' as the X pullback without anticommutation would be wrong. The manuscript uses the correct expression.

On each fresh ordinary input, choose X/Z, its sign, and an encoder anchor uniformly. A spectrum-valued measurement of s(A_j^b-A_j^a)/2 has mean r_a-r_b and second moment

    (1/8) sum_j Tr rho (A_j^a-A_j^b)^2.

Since A^2<=I, (A-B)^2<=2I-{A,B}. Combining this with the operator square triangle inequality gives E Z^2 <=2(ell0_a+ell0_b)<=4(r_a+r_b)/kappa. This is the essential fast-rate argument. Independent noisy decoder-error counts would retain a constant variance floor.

The measurement MUST return the spectral value (or a known bounded rational approximation), not a ±1 outcome from the binary POVM (I±C)/2. The latter has second moment one. Integer eigenlabel counts, weighted by the known rational labels, suffice; no true coefficient or source risk is an oracle input.

For disjoint patches, local spectral measurements on the SAME global source output preserve the joint outcome distribution and covariance; their difference labels implement the union difference observable. Separate copies or separately reconstructed marginal distributions do not. Overlapping intervals have a contiguous union of width at most 2w-1, on which a generic joint spectral measurement is paid. The final chosen decoder still acts only on one width-w patch.

## 3. Finite arithmetic and explicit Bernstein constants

Use an exactly unitary reference circuit V and rational eigenlabels c_l in [-1,1], defining C=V diag(c_l)V† with a certified total operator-norm residual ||C-H||<=xi. This specifies an exact physical reference measurement even with spectral degeneracies. A backward residual, not forward eigenvector closeness or a spectral gap, is what the argument needs. Clipping eigenlabels can be budgeted within the total residual. Gate-synthesis/implementation error belongs to the separate linked process budget, not this statistical backward-error term.

The stated maximum-offdiagonal Jacobi argument is valid: squared offdiagonal Frobenius mass decreases by at least the fraction 2/[d_c(d_c-1)] per exact chosen plane rotation. Its initial value is at most d_c for a contraction, so O(d_c^2 log(d_c/xi)) rotations suffice to reach a chosen Frobenius residual. Finite rotation/label errors must be bounded and included in the final residual certificate, as stated. This gives no free accurate eigenvectors and no inverse rare eigenvalue.

Write s=r_a+r_b. Because ||C||,||H||<=1, the mean bias is <=xi and E C^2 <=4s/kappa+2xi. The centered outcome is bounded by 2. A conservative two-sided Bernstein inversion is

    |mean C-E C| <=sqrt(2 Var(C)L/N)+4L/(3N)

except probability 2 exp(-L). With N>=512L/(kappa t), xi<=kappa t/4096, and 0<kappa<=1, this yields the stronger bound

    |mean C-(r_a-r_b)|
       <=(1/8)sqrt(ts)
          +t[1/(512 sqrt(2))+1/384+1/4096]
       <=(1/8)sqrt(ts)+(59/12288)t
       < (1/4)sqrt(ts)+t/96.

Thus the displayed comparison event is valid with substantial slack. No independence between candidates or between calibration outcomes is needed. Conditional on all prior data, a fresh comparison bank is iid with its now fixed contenders and known comparison controls. At most M-1 such batches occur, so L=log[2(M-1)/beta_Q] and conditional union bounds give failure <=beta_Q. Correlations among physical subsystems WITHIN a source output do not invalidate iid independence BETWEEN fresh source calls.

## 4. Tournament recurrence, constants, and deterministic cap

If the larger risk v+d wins, its empirical comparison event implies

    d <=(1/4)sqrt(t(2v+d))+t/96.

Using (1/4)sqrt(td)<=d/2+t/32 gives d<=sqrt(tv/2)+t/12. Young's inequality then gives

    d <=eta v+t/(8eta)+t/12 <=eta v+t/(4eta),  0<eta<=1.

The same winner inequality holds trivially when the smaller risk wins. Follow a minimum-risk candidate's surviving branch through at most h=ceil(log2 M) levels. With eta=1/(2h), (1+eta)^h<2 and the accumulated additive term is at most th^2. Therefore r_selected<=2r_min+th^2, without a support-separation gap.

At m=kappa^3 epsilon/2^17 and t=kappa epsilon/(320h^2),

    r_min <=(154/2^17) kappa epsilon < kappa epsilon/640,
    r_selected <=(897/163840) kappa epsilon
                < kappa epsilon/160.

Uniform transfer from the received common-gauge theorem and ell0<=2r/kappa give uniform decoder regret <=8r/kappa<=epsilon/20. The M=1 branch correctly skips the tournament; log(M-1), h^-1, and t are not evaluated there. Its single candidate already has smaller regret. The parameter choice also ensures m<=1/16.

The acquisition cap is exactly the stated 4qN_B plus (M-1)ceil[163840h^2 L/(kappa^2 epsilon)] for M>=2. Ceilings and all failed histories remain charged. Up to logarithms this is w4^w/(kappa^3 epsilon)+n/(kappa^2 epsilon), not logarithmic dependence on n and not the flat-gauge shadow cap.

## 5. Encoder learning, operational scope, and stopping boundary

After the tournament, freeze the actual specified decoder. Its fresh randomized-six-state error q_D(x)=2ell(D E_x)/3 is a nonnegative real quadratic on four coordinates even on bad training histories. Thus the imported ten-feature Bernoulli active-design result applies conditionally to this fixed decoder. Its displayed b, J, and source cap match epsilon_q=epsilon/6. This is not the completed pilot's fixed ten-point empirical interpolation and not an assertion that any noisy fitted matrix is PSD.

On the joint good event, the encoder step gives

    ell(D E_xhat) <=(1+gamma)(ell_star+epsilon/20)+epsilon/4
                  <=(1+gamma)ell_star+7epsilon/20.

With beta_A+beta_Q+beta_C<=epsilon/8 and whole-process implementation discrepancy nu<=epsilon/8, bounded loss gives an averaged additive allowance at most 3epsilon/5, hence the claimed epsilon with slack. No extra independence assumption among training successes is required. The uniform ideal/reference-decoder statement and the final averaged real-process statement should remain distinguished; a process-level nu does not certify every individual transcript conditionally.

The scheme uses ordinary source inputs but substantial collective receiver memory and local tomography. It is not the earlier single-copy Pauli-shadow experiment. The source count does not replace the 4M estimator circuit invocations, physical output qubits, storage, known input controls, spectral measurement synthesis, output routing, or payload call. For overlapping patches a generic spectral unitary is exponential in w; for disjoint patches joint local measurements avoid unnecessary distant quantum routing while retaining same-copy covariance. All these controls are available equally to an informed conventional learner.

Sections 1-5 above establish the all-patch tournament baseline. The following section checks the stronger preferred construction appended to the manuscript. Both remain conditional finite constructive theorems, not family-membership verification, experimental results, historical priority claims, generic unknown-noise theorems, or superiority over the strongest same-information baseline.

## 6. Preferred coarse-overlap localization and fresh fine stage

The cancellation identity is exact under the stated global local-Pauli promise. B_Z anticommutes with X_X and acts only on the fixed padded true interval I_*. If J is disjoint from I_*, conjugation by B_Z acts wholly on the subsystem traced out. Partial-trace invariance therefore gives X_X^J=-X_X^J=0. On the true interval, the positive factor traces without changing its trace, so ||X_X^I_*||_1=Tr Hbar_X>=kappa. This uses the exact common local algebra, not a guessed support or a learned approximate anticommutator. Entanglement of gauge subsystems does not invalidate partial-trace unitary invariance.

For each of 2M coarse state estimates, allocate beta_0/(2M). The received cap is then

    N0=ceil[(80*4^w/m0)log(24*4^w*M/beta_0)],
    m0=kappa^2/512,

and the colored source cost is 2qN0. The root-fidelity to trace-norm inequality follows by choosing Uhlmann purifications, applying the exact pure-state trace-distance formula, and tracing out the purification. Thus each state error is <=2sqrt(2m0), and each half-difference error is <=2sqrt(2m0)=kappa/8. A further certified trace-norm score error <=kappa/16 gives:

    true patch score >= kappa-kappa/8-kappa/16=13kappa/16;
    disjoint patch score <=kappa/8+kappa/16=3kappa/16.

The first score above kappa/2 therefore exists and overlaps I_* on the coarse good event. A deterministic fallback interval on failure preserves finite operation and is not postselection. The conclusion is only overlap conditional on the model; it neither identifies the exact algebra nor tests model membership.

All width-w intervals overlapping that chosen J have starts within w-1 of J's start. There are R<=R_max=min(M,2w-1), and the list contains I_* whenever coarse localization succeeded. Conditional on the COMPLETE coarse record, the list is fixed and FRESH source copies are iid. Its fine Bures procedures have failure at most beta_A/(4R_max) each; at most 4R of them occur, giving conditional failure <=beta_A. This remains valid even on a bad coarse history, although such a history need not include a correctable candidate.

Similarly, fixed h_max=ceil(log2 R_max), L_max=log[2(R_max-1)/beta_Q], and the specified comparison cap dominate every possible localized bracket. At most R-1<=R_max-1 comparisons occur, each with conditional failure <=beta_Q/(R_max-1). The proof can use eta=1/(2h_max) and depth at most h_max, so its risk bound is unchanged. If R_max=1, no h-dependent comparison formula is evaluated. Combining unconditional coarse failure, conditional fine failure, conditional comparison failure, and conditional encoder failure costs only beta_0+beta_A+beta_Q+beta_C; no independence between these events is assumed.

The predeclared complete cap is

    2qN0+4q1N1+(R_max-1)Npair+N_count+1,

with q1=min(w,R_max), the comparison term defined as zero for R_max=1, and the final one being an actual payload source use. It is an upper bound on every history, including failed coarse localization and smaller boundary candidate lists. At fixed w,kappa, source dependence on n is logarithmic through coarse confidence, not n/epsilon. This does NOT remove the n physical output qubits, 2M coarse collective estimator invocations, record/control handling, or memory-bank interconnect costs. All fine candidate patches are contained in a known neighborhood of width at most 3w-2 after coarse localization.

The expansion alternative is also valid. Enlarging J by w-1 on each side yields a patch K containing I_*, of width W<=W_max=min(n,3w-2). Fresh four-bank acquisition at m_exp=kappa^2 epsilon/32768 gives uniform regret <=616m_exp/kappa^2<epsilon/20. Using W_max in its N_exp formula makes the worst-case source cap fully predetermined; actual W can lower execution cost. Its cap includes the same coarse phase, four fine banks, separate encoder stage, and one payload call. It avoids a tournament and an inverse-kappa factor in fine tomography, but pays 4^W rather than 4^w and deploys a wider decoder. Both constructions belong to the same-informed conventional baseline.

No simulations, newly sampled measurements, or changes to frozen pilots were performed for this review. The manuscript's authored proof-candidate status is superseded for this scoped statistical acceptance by the bound companion receipt; no historical or experimental claim is added.
