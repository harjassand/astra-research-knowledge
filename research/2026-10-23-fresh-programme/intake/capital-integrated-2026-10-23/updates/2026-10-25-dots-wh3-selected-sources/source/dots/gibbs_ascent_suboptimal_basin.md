# A provably suboptimal attracting basin of the same Gibbs search

24 October 2026, root derivation. This is a load-bearing failure of using monotone convergence as a global certificate, not a rejection of the exact variational duality.

Use W3 and the general parameter a>1 from reference_adapted_gibbs_duality.md. Every product X0=I3/3 tensor tau is a fixed point of the update S_a(X)=W3(Y_X). Its entropy/dual objective is (1−a)ln3.

On traceless Hermitian perturbations H, the derivative is exactly

 DS_a|X0(H)=I3/3 tensor H_R +(a/4)[H−I3/3 tensor H_R].

At the product point, the BKM derivative and inverse derivative act identically on each physical matrix block, so they commute with W3. The two W3 factors multiply to1/4 on zero-partial-trace operators. The marginal direction has multiplier1 because the entire product family is fixed.

For1<a<4 this is a normally attracting manifold, not just an eigenvalue diagnostic. To see the actual local basin, use coordinates tau=X_R and delta=X−I3/3 tensor tau. On a compact faithful neighborhood of tau0, analyticity gives

 delta_next=(a/4)delta+O(||delta||²),
 tau_next=tau+O(||delta||²),

with uniform constants. Choose q strictly between a/4 and1 and delta small enough that ||delta_next||<=q||delta||. The total marginal drift is bounded by a constant times sum q^(2n)||delta0||², so all iterates stay faithful in the chosen neighborhood and converge to a product point. This produces an open basin.

But for a>2, the maximally entangled input rho=Phi3 has

 F_a(rho)=−ln3 > (1−a)ln3.

Its output is alpha3, with the same reference marginal I3/3. Thus EVERY2<a<4 has a strictly suboptimal attracting product basin. The gap is not merely due to singular witness states: at a=3 the faithful input rho=.99Phi3+.01I9/9 has spectrum (1−8epsilon/9, epsilon/9×8), and its output spectrum ((3−2epsilon)/9×3, epsilon/9×6), epsilon=1/100. The exact logarithmic entropy gap over the product fixed point is greater than1.03 nats, certified by the adjacent interval script.

This does NOT disprove the a=2 squashing target. It proves that the identical search architecture can converge smoothly and monotonically to the wrong answer in a neighboring, explicitly solvable comparison. At a=2 the product and maximally entangled boundary witnesses tie, while the product remains locally attracting. Therefore the completed a=2 product convergences cannot be upgraded to a global proof.

No claim of a general new Blahut–Arimoto failure phenomenon: monotonicity versus global optimality is already treated in primary work such as Liu–Hayashi arXiv:2609.09731. This is an exact failure within our own current operation and resource interface.
