# Independent audit of the compact-coordinate proof

31 October 2026. Review of geometry_learning/PROOF.txt during the root's live revision. This audit targets errors, omitted hypotheses, and finite implementation gaps. It does not establish historical novelty or formal verification.

## Verdict

The exact mathematical core is sound at the stated scalar-return and common-contraction interface. I did not find an error in the factor-isometry argument, the feasibility of contraction fitting, the linear-horizon comparison of the two stable rollouts, the additional-readout bound, or the fresh-Gram martingale/net calculation.

The issues found concern connecting that core to finite stored factors, the specific projected-subgradient implementation, and the full cost/confidence ledger. Two issues were already patched by root during the audit: the zero-dimensional branch and use of the stored factor's actual Gram discrepancy in the dictionary-readout bound. The remaining items and a stronger optional numerical construction are detailed below.

## 1. Exact factor geometry: accepted

For the exact thresholded factor, the proof uses ||Ghat-G||op<=eta, drops eigenvalues <=2eta, and obtains ||B-G||op<=3eta. The negative eigenvalues of Ghat are >=-eta, so discarding them is covered by the same truncation bound. Weyl's inequality establishes k<=rank(G), with no unknown Gram floor.

The polar-factor argument is valid after enlarging the true Hilbert space. Extend the partial polar isometry of V to an isometry J from R^N into H'. Then V=J sqrt(G). For the spectral factor X=sqrt(Lambda) W*, take Q=JW, giving QX=J sqrt(B). The source extends by zero on added directions and remains contractive. The square-root Holder bound is valid: order monotonicity and sqrt(C+dI)<=sqrt(C)+sqrt(d)I give both Loewner inequalities and hence the operator-norm bound.

For an arbitrary rational full-row-rank factor X with B=X*X, the same coupling follows by inserting the row-polar isometry R:R^k->R^N satisfying RX=sqrt(B), and taking Q=JR. No inverse is needed by the learning algorithm; this is an existence argument in the proof. The analogous zero-rank case is immediate.

The sufficient rational certificate e_B>=||Ghat-X*X||op, D=eta+e_B, alpha=sqrt(D) is correct. If lambda_min(XX*)>D, then G is positive on range(X*), establishing k<=rank(G).

## 2. The new rank certificate is sufficient, not automatically attainable by the plain proposal

**Needs explicit scope or a fallback.** A plain thresholded factor can fail lambda_min(XX*)>eta+e_B even in exact arithmetic. For example, Ghat=G=diag(2.01eta,1.99eta), with threshold 2eta, gives B=diag(2.01eta,0). The exact discrepancy e_B is 1.99eta, so D=2.99eta exceeds the retained eigenvalue 2.01eta. Increased numerical precision cannot change this failure.

The exact spectral proof still certifies k<=rank(G). Therefore the simplest correction is to call the rational inequality an optional sufficient fixture certificate and keep a separately bounded, certified spectral fallback. Do not define the universal algorithm as retrying proposals without a stopping argument until this conservative certificate passes. Likewise, a raw row-sum upper bound can remain conservative even at infinite arithmetic precision; certified PSD inequalities can be tighter.

A useful stronger construction supplies a fixed margin. After keeping exact eigenvalues above 2eta, replace every kept eigenvalue lambda by max(lambda,4eta). Then

    ||B-Ghat||op <= 2eta,
    D <= 3eta,
    lambda_min(XX*) >= 4eta > D.

Both discarded eigenvalues and upward modifications have magnitude <=2eta. Thus the same coupling alpha<=sqrt(3eta) holds, while the rank certificate has margin eta. Controlled rational perturbations can preserve a fixed fraction of this margin. Certified PSD checks of e_B I +/- (Ghat-X*X) can establish the discrepancy without the dimension-dependent conservatism of a raw row-sum bound.

With interval eigenvalue selection, keep a fixed buffer above the noise level and enlarge the flooring constant as necessary; do not demand exact decisions at a repeated threshold eigenvalue. The proof should state which finite spectral method or certificate supplies the operator residual, since eigenvalue approximations alone do not certify a numerically computed eigenvector matrix.

## 3. Contraction feasibility and rollout comparison: accepted

For A*=Q*TQ, ||A*||op<=1. In

    A*X-XM = Q*T(QX-V) + Q*(TV-VM) + (Q*V-X)M,

the three maximum-column norms are bounded by alpha, rho, and alpha. The final bound uses the acquired column l1 norm of M, exactly as required. This does not accidentally assume a small normalized leakage operator on all of span(V).

The comparison y_w versus Xc_w is also valid. Contractivity of A and l1 stability of c_w yield ||y_w-Xc_w||<=|w| beta. Combined with the old physical approximation and columnwise coupling, this gives |w|rho+alpha+|w|beta. No quadratic horizon accumulation is needed.

The dictionary-readout bound is correct when it uses the actual D>=||X*X-G||op. Root has replaced the original 3eta by D for rounded factors, which resolves the earlier gap. Per-column factor rounding of size s/4 need not preserve a Gram error of order eta=s^2/16; this replacement is necessary, not cosmetic.

For an added norm-one readout, h*=Q*g is feasible, the true coordinate fit error is at most alpha+2tau_g+zeta_g, and the predictor bound |w|(rho+beta)+chi follows directly by comparing through Vc_w. The readout proof has no hidden inverse eigenvalue.

## 4. Finite optimization: one norm cap should be explicit

**Needs a small implementation condition.** The stated inexact projected-subgradient telescope is valid if the approximate gradient is explicitly constrained to have Frobenius norm <=L. The proof otherwise contains an extra step-size term proportional to

    h ((L+e_g)^2-L^2)/2.

This term is not among the listed perturbations and can matter when L is very small. Radially clipping the computed gradient to the Frobenius ball of radius L fixes the issue: the true gradient lies in that ball, so clipping does not increase the norm error e_g.

Subject to this cap, the remaining error expression is correct. An index within gamma of the maximum supplies a gamma-subgradient. Gradient error contributes at most 2sqrt(k)e_g because the spectral-norm unit ball has Frobenius diameter 2sqrt(k). A feasible point within nu of the exact projection contributes (4sqrt(k)nu+nu^2)/(2h). The proposed tolerances leave ample slack within zeta.

The exact projected method has initial distance at most sqrt(k), Lipschitz constant L, and rate Lsqrt(k/T). Averaging feasible contraction iterates preserves contraction. The smoothed maximum differs from the original maximum by at most mu. No source-side oracle is needed for this optimization.

**Already patched:** k=0 must return the zero predictor before defining h=sqrt(k)/(Lsqrt(T)). The original formula would otherwise divide 0 by 0. If the implementation accepts arbitrary factors instead of a positive-rank certified factor, it should also handle L=0 explicitly.

## 5. Gram concentration and adaptive conditioning: accepted

Condition on the complete history just before the new Gram stage, rather than merely informally on N. The dictionary and all requested pairs are then fixed. For a unit x, the unordered-pair weights are x_i^2 on the diagonal and 2x_i x_j off it, with squared sum

    sum_i x_i^4 + 4 sum_(i<j) x_i^2 x_j^2
      = 2 - sum_i x_i^4 <= 2.

For reports bounded in [-R_ij,R_ij], the martingale Hoeffding bound is therefore

    Pr(|x*(Ghat-G)x|>t) <= 2 exp[-t^2/(4v)],
    v=max R_ij^2/n_ij.

The stated n_ij makes v<=eta^2/(16L_N). A 1/4-net has at most 9^N points and converts the eta/2 quadratic-form threshold into eta operator norm. The constants give total conditional failure probability at most delta_G, for every selected dictionary. Therefore adaptive dictionary construction does not require another N-dependent confidence allocation in this fresh stage.

The stage can use martingale reports; mutual independence is unnecessary if the full conditional-unbiasedness and conditional range bounds really hold. If R_ij=0 is permitted, define that entry directly as zero instead of taking the mean of zero reports.

## 6. Confidence, arithmetic, and digitization ledger

**Recommended explicit additions:**

- State the overall success probability, e.g. at least 1-delta_old-delta_G-delta_R, with delta_R already joint over the retained readout library. Numerical certificates may be deterministic. There is no subsequent union bound over words.
- Include the dense geometry proposal, conventionally O(N^3) arithmetic, and the finite rational/interval certification work. Computing X*X costs O(kN^2); computing XX* costs O(k^2N). Exact PSD certification has its own arithmetic and bit cost. Source-report accumulation also requires arithmetic. These may be dominated by other displayed terms, but a complete bill should name them.
- Include the analogous readout-fitting work and qN readout scalar jobs at their actual ranges and tolerances. The main proof currently states their existence but does not give a single combined budget for this stage.
- For deployment rounding, multiply the propagated state error by the actual stored readout norm. Fitted h has norm <=1, but a retained dictionary readout x_j can have norm up to 1+alpha. Dot products computed to absolute tolerance need the usual guard bits for k-term accumulation. Stored seed rounding must either be included in the acquisition factor or added as an initial error.
- The generic finite-bit claim needs finitely encoded reports or a known digitization bound. A bounded unbiased abstract real report does not automatically provide a finite rational input. Common endpoint products are binary and satisfy this directly. For more general reports, entrywise rounding at most eta_digit/N produces a Gram operator bias at most eta_digit; reserve that budget or use an explicitly justified unbiased quantization scheme. Repetition cannot remove unknown systematic bias.

## 7. Expected work and rejected attempts

The old atomic guard and literal-pair cache were checked in the preserved proof. Their packing-plus-bad-estimates argument supplies the needed exceptional-path control, so adding a polynomial-in-N fresh stage preserves finite moments under the common bounded-range, finite-rank premises. The new Gram concentration event need not hold for the algorithm to terminate; the numerical routines should have finite prescribed budgets and return a model or failure status rather than enter an unbounded acceptance loop.

Actual L and the actual input magnitudes should determine the finite optimization budget on failure paths. The good-event inequality L<=1+alpha cannot be treated as an unconditional input bound when Ghat is corrupted. Bounded reports still provide a polynomial unconditional matrix-size bound in N, so this is repairable without a new source assumption.

The caution about depth-dependent report weights is appropriate. A geometry compression does not remove original word lengths, stationary preparations, or large weights. The older proof has a stronger exponential-moment estimate for the number of bad jobs, but no new weighted expected-cost claim should be made without carrying the actual cost function through that estimate.

## Final assessment

After the explicit numerical qualifications above, the central result appears sound: an already acquired l1-stable finite dictionary can be compiled, through fresh noisy Gram acquisition, into at most r Euclidean runtime coordinates at a chosen finite task tolerance. The proof genuinely avoids normalizing arbitrary weak Gram directions and genuinely has a linear horizon bill. It does not remove the old exponential-in-rank dictionary-discovery cost, and it does not distinguish itself from a strong retaining spectral/model learner allowed to use the same construction.
