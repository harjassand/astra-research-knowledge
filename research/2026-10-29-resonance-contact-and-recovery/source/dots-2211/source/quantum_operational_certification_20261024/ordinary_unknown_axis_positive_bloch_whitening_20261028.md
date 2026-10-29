# Local inverse acquisition by positive Bloch whitening, including unknown-axis amplitude damping

28 October 2026. **New candidate; independent review pending.** This extends the aligned-axis contrast construction through a different representation. It does not assume that each measured contrast already has the sign of the desired physical generator. It uses three paid ordinary preparation axes and a small Gram matrix to cancel an unknown positive Bloch contraction. All historical novelty and practical superiority claims remain open.

## 1. Consequence and actual interface

The desired operation is a reusable inverse of a fixed unknown local output mixer V, learned without reconstructing the noise environment, before a known quantum code decoder if one is supplied. V is an n-qubit unitary. The true generators B_(i,j)=V sigma_(i,j) Vdagger, j=X,Y,Z, have a common unknown interval support S_i of width at most supplied w on the known output line. X/Z support already contains Y=i X Z, with the usual Pauli convention Y=i X Z. Distinct qubit algebras commute.

Every calibration block prepares all n physical inputs in independently uniform X/Y/Z axes and independent signs, then reads all physical outputs in independent uniformly random Pauli bases. This THIRD input axis is a genuine extension of the earlier two-axis apparatus. There is no unknown payload during calibration. Source and controller cannot select the current source map using undisclosed current preparation/readout coins except through their actual quantum inputs. Complete prior records may affect the source. Local reflection synthesis, routing, mixed receiver ancillas and whole-process control discrepancies are paid.

For each input i, require a fixed unknown REAL SYMMETRIC POSITIVE DEFINITE 3-by-3 matrix T_i. On every allowed prior history h, after averaging the OTHER current input labels, require the actual reduced output contrasts

    Delta_(i,j,h) = sum_k (T_i)_(k,j) B_(i,k) R_(i,h),       (1)
    R_(i,h)>=0, [R_(i,h),B_(i,k)]=0 for k=X,Y,Z.

The SAME factor R_(i,h) appears for all THREE axes of i. It can vary with history and fail to commute with other qubits' algebras. No numeric gap or eigenvalue bound is given to the learner. T_i is fixed across the data bank (and fixed across stages in this version). Equivalently, positive scalar changes of T_i can be absorbed in R; arbitrary matrix changes correlated with R are not covered. The source outputs are actual normalized positive states, and all signed contrasts obey ||Delta||1<=1. The sign-averaged input is I/2^n for every selected axis, so its conditional output rho_h is the same, although not necessarily maximally mixed.

This is a structural promise, not a claim that finite calibration can certify arbitrary inaccessible source histories. The complete source may retain coherent noise records. Only the reduced conditional contrasts are constrained. The future guarantee is comparison with the PARTICULAR fixed Vdagger operation, not undoing all noise, an optimal decoder, or identity logical dynamics.

## 2. Support discovery still works

Write A_j=sum_k T_(k,j) B_k. Pauli anticommutation gives A_j^2=||T e_j||_2^2 I. Since R commutes with the whole own-qubit algebra, for every interval J containing S_i,

    Delta_(i,j,J)=A_(j,J) R_J,
    ||Delta_(i,j,J)||1=||T e_j||_2 Tr R.

For J disjoint from S_i, choose an own-qubit reflection B_v perpendicular to the nonzero real vector T e_j. It anticommutes with A_j, commutes with R and is wholly traced out. Thus Delta_(i,j,J)=0. This is a proof device; the learner is not supplied B_v or T.

The paired-axis margin-free support guard therefore extends verbatim to THREE axes with its actual statistical constants changed below. A confidence-positive empirical trace norm identifies an overlapping width-w interval, whose expansion by w-1 sites on either side contains S_i. Let W=min(n,3w-2) and d=2^W. Support certificates remain valid because the true algebra is fixed. Finite caps can return ABSTAIN.

## 3. The common factor cancels through a 3-by-3 Gram matrix

On a fixed containing interval J and a reached bank, predictable averaging gives Delta_j=(sum_k T_kj B_k) Rbar with Rbar>=0 commuting with the own algebra. Define

    G_jk = Tr(Delta_j Delta_k), c=Tr(Rbar^2).

If a fine gap is available then c>0. Because Rbar^2 commutes with the own-qubit algebra, Tr(B_a B_b Rbar^2)=delta_ab c: cross terms are proportional to a Pauli operator whose trace vanishes under conjugation by a complementary own Pauli. Therefore

    G=c T^2,
    C_j=sum_k Delta_k (G^(-1/2))_kj = B_j Rbar/sqrt(c).       (2)

The last equality uses T symmetric positive definite. It is not valid for an arbitrary invertible Bloch matrix: whitening would leave its orthogonal polar factor, a real physical calibration ambiguity. No hidden determinant or handedness choice is inferred from observations.

If Rbar is full rank on J, sign(C_j)=B_j. Thus a scalar, observable 3-by-3 Gram normalization followed by the previously received matrix-sign primitive recovers the desired axes even though sign(Delta_j) generally points in the WRONG unknown rotated direction. A containing interval with singular Rbar need not accept. The normalized C_j need not be a quantum channel or state; it is a known Hermitian matrix used to synthesize a reflection.

## 4. Finite confidence, whitening error and strict acceptance

Use the actual record Y_(i,j)=3*1{current input axis of i=j}*s_i*Z_J, where Z_J is the ordinary product Pauli shadow. Conditional means equal Delta_(i,j,h). Their conditional second moments are <=3*3^|J| I, and centered increments have norm <=6*2^|J|. These follow by importance weighting the one-in-three input axis and the positive physical shadow second-moment bound; no stationarity of R or outgoing-memory CP sign is assumed.

For a fixed fine radius a in (0,1], a fresh bank of N=16*3^W*L/a^2 blocks, with L a ceiling natural logarithm of 6dn times the declared total number of fine banks divided by beta_f, is sufficient for simultaneous ||Deltahat_j-Delta_bar_j||op<=a. Indeed matrix Freedman's denominator 2(3*3^W+6*2^W*a/3) is <=10*3^W, so each tail is <=2d exp(-1.6L); the chosen L pays every one of 3n processes and all banks. Coarse stages replace a by eta/2^w and use 16*12^w*L_c/eta^2, with L_c covering 3n(n-w+1) processes and coarse banks. Finite integer ceilings and the earlier rational score tolerances are retained. Fresh banks and finite caps remain mandatory.

Here is a conservative, explicit whitening guard using only known finite matrices. Empirical matrices are exact rational Hermitian shadow averages. Put Ghat_jk=Tr(Deltahat_j Deltahat_k), a real symmetric PSD Gram matrix, and

    g=3d(2a+a^2).

Since ||Delta_j||op<=1, every Gram-entry error is <=d(2a+a^2), hence ||Ghat-G||op<=g. Obtain a certified rational lower bound h<=lambda_min(Ghat), and require h>g. A concrete implementation first tests rational positive definiteness by the three leading principal minors; if it fails, reject this bank. Put q=max(1,Tr Ghat), start h=q/2 and halve until all leading minors of Ghat-h I are strictly positive. Then h is a certified positive lower bound (at least lambda_min(Ghat)/2); all operations and search iterations are paid.

Here is an explicit rational inverse-root construction, including the degenerate-eigenvalue case. Put A=I-Ghat/q and r=1-h/q in [0,1). Then 0<=A<=r I and

    Ghat^(-1/2)=q^(-1/2) sum_(k>=0) b_k A^k,
    b_k=binom(2k,k)/4^k in (0,1].

For desired rational u>0, select a finite m by exact rational comparisons until r^(m+1)/(1-r)<=u/2. Bisect the scalar q^(-1/2) to a rational z within u(1-r)/2, and set W0=z sum_(k=0)^m b_k A^k. The series tail is <=u/2 because q>=1, and the scalar rounding error times the polynomial norm is <=u/2. Therefore W0 is exactly rational real symmetric and ||W0-Ghat^(-1/2)||op<=u. Powers, rational coefficients, bisection comparisons and denominators are explicit finite arithmetic. A conservative m is O((q/h)*log(1/[u(1-r)])) when a nontrivial tail is required; this is conditioning-dependent work, not a free spectral oracle or a claim of logarithmic conditioning cost.

Define Ctilde_j=sum_k Deltahat_k (W0)_kj. A valid computable upper bound E is any rational number at least

    sqrt(3)*a/sqrt(h)
      + sqrt(3)*g/[2(h-g)^(3/2)]
      + sqrt(3)*(1+a)*u.                                    (3)

To prove it, use ||Ghat^(-1/2)||<=h^(-1/2), and the positive inverse-square-root integral/Sylvester bound

    ||Ghat^(-1/2)-G^(-1/2)||
       <=g/[2(h-g)^(3/2)].

The three-term sum is estimated with Cauchy–Schwarz in its three real coefficients. Equation (3) therefore bounds ||Ctilde_j-C_j||op. Roots/divisions in this guard are outward-rounded rational bounds, not free exact irrational arithmetic.

Apply the received finite rational Jacobi primitive to Ctilde_j, producing exactly rational-unitary Q_j and rational diagonal D_j with Frobenius residual <=v. Let e=E+v and ell_j=min|D_j,kk|. Require the strict raw-sign guards

    ell_j>e,  2e<=delta(2ell_j-e),                             (4)

where delta is the desired reflection operator error, chosen <=zeta/(3n). Then the same two-sector Sylvester argument proves

    S_j=Q_j sign(D_j) Q_jdagger,
    ||S_j-B_j||op<=delta.

Every S_j is a physical reflection even on bad records. Only X and Z are needed in the three-controlled-reflection extraction circuit; Y is acquired as a contrast for whitening and can also serve as a consistency diagnostic. Do not turn a diagnostic into structural membership certification. A fine stage may retain X/Z separately after its common Gram guard, and combine retained certificates from different stages because B is fixed.

Choose dyadic a_s decreasing to zero and rational u_s,v_s decreasing to zero; bank sizes and caps are fixed before outcomes. Under persistent positive Gram and normalized-sign gaps, sufficiently funded finite stages accept. Without such promises the algorithm is sound but can abstain. No numeric conditioning is supplied to it. The three-way preparation/readout samplers also have a finite physical debit: for a declared worst-case B source blocks there are 2nB ternary choices. Generate each by at most r_rng=max(1,ceil(log_4(2nB/nu_rng))) independent two-bit attempts, accepting 00/01/10 and rejecting 11; exhaustion produces ABSTAIN. Its probability is at most nu_rng by a union bound. This pays at most 4nB*r_rng axis coin bits and nB independent preparation-sign bits, with nu_rng included in the calibration-record implementation allowance. Conditional-on-no-exhaustion choices are uniform; the ideal-versus-bounded actual record coupling pays the exhaustion event rather than silently using an unbounded sampler. For explicit instance accounting, if h_* is a uniform true Gram minimum and r_* is a uniform normalized C gap, it suffices to fund a satisfying g<=h_*/4, the right side of (3) plus v <=delta*r_*/4, and u,v budgets of the same size. The bill is 16*3^W*L/a^2 per stage plus geometric predecessors, coarse discovery, finite arithmetic and controls. This deliberately conservative bound exposes the extra Gram-conditioning penalty rather than declaring an optimal scaling law.

## 5. Actual unknown-axis amplitude damping realizes the promise

A qubit amplitude-damping channel of rate gamma in an unknown fixed Bloch direction u has affine Bloch action

    r -> T r+gamma*u,
    T=sqrt(1-gamma) I + [(1-gamma)-sqrt(1-gamma)] u u^T.

For 0<=gamma<1 this T is real symmetric positive definite. The translation cancels in signed input contrasts. For a product of such fixed qubit channels before the SAME fixed local V,

    R_i=V[(I_i/2) tensor product_(k!=i) rho_k]Vdagger,
    rho_k=(I+gamma_k u_k.sigma)/2,

and (1) follows exactly. Arbitrary compatible coherent environment completions are permitted, provided the same reduced conditional contract holds on every calibration history. Allowing an arbitrary memory-dependent mixture of differently oriented T_i correlated with different spectator factors would BREAK the common-factor proof and is not included.

The previous local backward-cone proof applies to R_i without requiring aligned axes. For a containing interval J, let K(J) be inputs whose support intersects J. Then |K|<=min(n,|J|+2(w-1)); a normalized-unital CPTP map from K to J removes inputs outside K. If gamma_k<=gamma_max<1 and a0=1-gamma_max, then

    R_(i,J)>=a0^(|K|-1) I_J/2^|J|,
    lambda_min(T_i)>=a0.

Here the own factor is I/2, so the exponent for R is |K|-1, not |K|. Consequently c=Tr R_J^2>=1/d and lambda_min(G)>=a0^2/d. Also c<=1 because R_J is a density operator, so the normalized C gap is at least a0^(|K|-1)/d. These are conservative persistent conditioning parameters at fixed width; no all-n spectator product floor appears. The learner is not supplied gamma_max, u_k, T_i, V, or R_i.

## 6. Complete service and what is actually added

Once all X/Z operator certificates hold, the ACTUAL unframed coherent 3n-block receiver differs from the true V-inverse extraction by operator norm <=3n delta<=zeta. Hence the extracted channel is within half-diamond zeta of Ad_Vdagger on arbitrary inputs entangled with continuing source memory. This invokes the separately reviewed operator-telescope fallback, NOT a Bell-to-diamond shortcut, a private-frame CP mixture or a Pauli noise representation. J common causal future uses pay at most J*zeta plus bad-record, calibration-record and whole-service implementation allowances. The fixed inverse can precede any supplied known CPTP code decoder. It does not itself eliminate amplitude damping or establish a native error threshold.

The separately received algebraic source `local_noise_polar_identifiability_extension_20261028.md` extends the target to stationary product qubit channels with nonsingular orientation-preserving Bloch matrices: absorb their proper orthogonal polar factors into V_eff and apply this finite acquisition mechanism to the resulting positive factors. The learned inverse is V_eff-dagger, not an independently identifiable original V. Its source and separate receiving receipt govern that algebraic extension; this source supplies the finite acquisition obligations.

The acquisition uses only local ordinary signed responses and a 3-by-3 Gram calculation. It does not reconstruct microscopic environment or a global channel Choi matrix. This is not by itself a practical or historical advantage: an equally informed conventional process learner can use these exact local contrasts, polar/Gram normalization and sign extraction. Direct end-to-end service tomography remains a competing method when dimensions and calibration depth permit. Prior local-unitary product-probe learning and SWAP sewing, including Huang et al. arXiv:2401.10095, is an existing foundation rather than claimed new here. The new scoped mechanism is cancellation of a common unknown positive spectator factor and positive Bloch contraction, with finite error guards and complete-memory transfer. Unknown coherent rotations inside the noise prevent identifying the original V under this positive-T orientation convention; in the separate canonical polar extension those rotations are absorbed into V_eff rather than independently identified. Arbitrary unknown noise remains open.
