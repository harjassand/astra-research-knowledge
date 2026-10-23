# P1 general Green-diagonal criterion — 23 October 2026

This append-only handoff preserves the selected Section 6 and Section 6.1 theorem extract from the supplied P1 continuation. It records a source-reported proof review and a bounded local reading of the displayed argument. It does not certify the theorem, establish novelty or priority, or show a uniformly realizable design.

## Theorem 6.2 as stated in the source

Let `G` be a simple `q`-regular graph. For each vertex `i`, let `V_i` contain the local probe rows on the closed neighborhood `N[i]`. Assume `V_i` has rank `q`, and all its nonzero squared singular values lie in `[alpha,beta]` with `alpha > 0`. Let `ell_i` be a unit generator of `ker(V_i^T)`. On the space `S_G` of symmetric matrices supported on the graph, the source defines `R`, `Q = I - R*R`, and the scalar constraint matrix `K = I - RR*`. Under `K > 0`, set `g = max_i (K^-1)_{ii}` and

`kappa_op = sup_{0 != H in S_G} ||H||_op / ||H X||_F`.

The source claims

`max{1, g - 1}/beta <= kappa_op^2 <= [1 + (q + 1)g]/alpha`.

Its decoder solves one `n`-variable sparse system `K a = R Z` after local lifting, is exact on noiseless data, and has arbitrary-noise amplification at most the square root of the upper bound. For fixed `q` and uniform positive local frame bounds, the source states that optimal operator amplification is uniformly bounded across a family exactly when the corresponding `g` values are uniformly bounded.

## Proof spine and review boundary

The displayed argument derives an exact weighted-Laplacian identity for `K`, compares the measurement normal operator to `Q` using the local frame bounds, and uses the resolvent identity `Q^-1 = I + R*K^-1R`. Hilbert-space duality supplies the operator-norm expression; a bound on `||R A_u||_1` and positive definiteness of `K` give the upper estimate, while local functionals and the normal-operator bound give the lower estimate. The source also distinguishes a localized low-energy compatibility obstruction from a small global spectral gap with spread-out eigenvectors.

The coordinator handoff reports a proof check of the frame inequalities, resolvent identity, operator-norm duality, and decoder bound, conditional on full local rank and `K > 0`. Capital inspected the displayed Section 6–6.1 argument and page context. This is a same-team internal review only: no independent proof reconstruction, formal verification, or external review was performed. The cited identification of `K` with a rank-one cellular-sheaf Laplacian points to reference `[3]`, whose bibliography entry is outside this extract and was not checked here.

The source's full certificate archive was unavailable, so numerical certificates were not replayed. The producer states that a uniform realizable design remains open. No physical experiment or practical advantage is established. The theorem's assumptions, including `K > 0`, full local rank, and uniform frame bounds where the family statement is used, must be checked for any proposed instance.

## Source handling

`source/section-6-general-green-diagonal-criterion-pages-8-10.pdf` contains pages 8–10 from the supplied 14-page PDF, extracted without cropping or retouching. Page 8 includes the end of the preceding section; page 10 continues into the start of Section 7. The complete source PDF and the unavailable certificate archive are not included. The manifest pins the original PDF and selected extract by size and SHA-256.
