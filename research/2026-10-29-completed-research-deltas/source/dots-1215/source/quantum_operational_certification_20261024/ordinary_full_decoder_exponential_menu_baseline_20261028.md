# Generic strict-ordinary relative learning: the exponential-menu baseline

28 October 2026. Explicit composition of the received nonnegative linear-action design and the paid common-frame compiler. This records a conventional upper bound already implied by the programme, not a new optimal-rate result. The unresolved generic target is a better dimension rate and efficient design/processing, not absence of any relative learner.

## 1. Access and comparator

Use the supplied four-real-coordinate isometric encoder family, a stationary/reset source, a valid encoded Choi-rank bound R, and the received finite-horizon common-frame processor. Every output is represented in the SAME retained k-dimensional frame, k<=8R. Its memory, whole-process precision, local controls and future-payload interface are paid. A physical support basis is not supplied for free. Ordinary Pauli preparations and actual full-CPTP receiver tests are allowed; no source-entangled reference or coherent encoder selector is introduced.

For every x and full-CPTP decoder Choi C,

    ell(x,C)=(3/2)Tr[T_x C^T],
    C>=0, Tr_logical C=I_k, ||C||<=2, Tr C=k.

The actual six-state mismatch is Bernoulli with mean f(x,C)=2ell(x,C)/3. It is linear in the features q2(x) tensor vec_Herm(C^T), whose real span dimension is at most d_feat=40k^2. The comparator ell_star is the true unrestricted minimum over this encoder family and ALL full-CPTP decoders in the same source model.

## 2. A literal finite feasible decoder net

Fix 0<epsilon<=1 and let tau=epsilon/128. For any feasible C define

    C_tau=(1-tau)C+tau I_(2k)/2.

This obeys the TP affine equations, C_tau>=tau I/2 and ||C_tau||<=2. Round its independent Hermitian coordinates to a rational mesh delta<=tau/(16k), producing a Hermitian M with ||M-C_tau||_F<=2k delta. Enforce TP by the explicit affine projection

    Cnet=M+[I_k-Tr_logical M] tensor I_2/2.

The error relative to C_tau is the Hilbert-Schmidt orthogonal projection of M-C_tau onto the trace-homogeneous subspace, so its Frobenius norm cannot increase. Thus ||Cnet-C_tau||op<=tau/8, and Cnet is positive with margin at least3tau/8. All coefficients and TP equations are rational.

An ACTUAL finite list can enumerate all such bounded rational Hermitian coordinate grids, apply the affine projection and retain only PSD matrices with the TP constraint. Rational PSD can be checked exactly, for example by principal minors; exponential computation is allowed for this baseline. The retained list contains the above approximation to EVERY feasible C. Raw coordinate bounds can be conservatively enlarged to [-3,3] for real/imaginary parts. Therefore

    log M_C=O(k^2 log(k/epsilon)).                         (1)

The list is not just a covering-number existence assertion.

The comparator risk debit is small uniformly in x. Mixing toward I/2 changes a valid risk by at most tau. The final correction costs at most

    ||(3/2)T_x^T||_F ||Cnet-C_tau||_F <=3tau/16,

because T_x is a density. Thus ell(x,Cnet)<=ell(x,C)+2tau. In particular the fine mesh is chosen to preserve FEASIBILITY, not by rounding a boundary Choi matrix and declaring it positive.

## 3. A finite encoder list and comparator discretization

Use a normalized rational cube-face grid of S^3 with chord radius h<=sqrt(epsilon/128). Its cardinality is O(h^-3)=O(epsilon^-3/2). The matrix xx^T is rational even when the normalized vector uses a square root; ordinary gate approximations are paid separately.

At a joint optimal pair (x_star,C_star), x_star minimizes the nonnegative quadratic ell(x,C_star)=x^T B x with 0<=B<=I. It is a least-eigenvalue vector. Therefore a grid x within chord h has

    ell(x,C_star)-ell(x_star,C_star)<=h^2.

This is only a comparator argument for a fixed C_star, not a claim that the optimized nonsmooth value has a uniformly quadratic modulus. Combining with Section2 gives a finite feasible pair satisfying

    ell_menu <=ell_star+h^2+2tau <ell_star+epsilon/32.     (2)

All menu actions are actual ordinary encoder/decoder experiments. The finite net does not restrict the original comparator; (2) pays its approximation.

## 4. Source count and actual operational guarantee

Apply `ordinary_adaptive_nonnegative_design_bridge_20261027.md` to the finite menu X_grid times C_net, the actual Bernoulli records, and its known d_feat-dimensional feature span. Use relative slack gamma/2 and additive slack epsilon/4, with failure probability at most epsilon/8. The bridge learns the ACTUAL risks, not only a model prediction. Its deterministic cap has the form

    N=O_tilde(d_feat log(M_C M_X)/(gamma epsilon))
      =O_tilde(k^4/(gamma epsilon)),                     (3)

where the tilde includes logarithmic accuracy/confidence terms. Both k^2 factors are explicit: one is the linear feature dimension; the other comes from log of the full decoder menu. Because actual Bell loss is at most one, bad histories add at most epsilon/8. Comparator debit (2), finite processing and final channel/control discrepancy can be allocated the remaining epsilon budget, yielding the averaged IMPLEMENTED guarantee

    E ell_alg <=(1+gamma)ell_star+epsilon.                (4)

The conventional learner may use this same quantum receiver/frame interface. Its source preparations are strictly ordinary. All calibration calls are pre-datum and every unused/failed record counts. A deterministic horizon and the paid compiler cost are fixed before execution. Approximation of statistical records is charged at the requested confidence level; final operational synthesis is charged at the remaining loss budget. No posterior quality guarantee for every exposed record follows merely from (4).

The finite design algorithm enumerates a finite, potentially enormous action menu. Its arithmetic is polynomial in that menu size and bit precision, hence generally exponential in k^2. This is NOT a polynomial-processing generic k^4 theorem independent of the menu size, much less a k^2 theorem.

## 5. Why linear SDP access does not close efficient design

For a fixed x and linear score, maximizing over C is a standard full-CPTP SDP; a classical fixed-dimensional x grid gives polynomial weak linear-action optimization. But the received determinant/weighted-design update maximizes a leverage expression of the form

    a(x,C)^T V^-1 a(x,C) / U(x,C).

This is a quadratic or rational objective in C, not the linear SDP objective. Maximization of that expression over the continuous decoder spectrahedron is not justified by a linear optimization oracle alone. No computational hardness theorem is claimed here; the necessary efficient design reduction is simply not supplied by the preceding observation.

The live generic strict-ordinary programme therefore asks for:
- O_tilde(R^2/(gamma epsilon)) rather than the loose R^4 source rate;
- polynomially represented and executable active design/model processing;
- the same honest paid common-frame and control ledger.

New received local matrix responses and prospective operator envelopes may help by serving many decoder tests at once. Their existence does not by itself bound adaptive encoder-query counts or rank-weighted cumulative source cost. Generic coherent-reference/bootstrap routes under their separate supplied/paid seed promise remain valid stronger-access comparators; they are not relabeled strict ordinary inputs.

## Evidence scope

This note gives an explicit finite feasible net and its comparator debit, then invokes the already received finite-action theorem and compiler. It does not independently re-receive those imports. The companion check verifies rational affine rounding, decoder feasibility, feature/entropy scaling and quadratic comparator transfer on finite fixtures. The continuum covering argument and statistical theorem are the mathematical grounds, not Monte Carlo. No universal quantum-over-conventional advantage is claimed.
