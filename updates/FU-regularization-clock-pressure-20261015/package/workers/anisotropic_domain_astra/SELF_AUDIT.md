# Mathematical self audit

This is an internal audit of the argument in `PROOF.md`, not an independent review or a numerical proof certificate.

| Potential failure | Resolution in the proof |
| --- | --- |
| An unbounded domain has a polar of deficient dimension. | The polar integral uses relative Lebesgue measure in its span. The zero-dimensional case is explicitly \(D=\mathbb R^m\). |
| A corner prevents a smooth barrier or causes a missed boundary direction. | The homothetic relative-ball estimate forces the polar integral to diverge at every finite boundary point, without normal uniqueness. |
| A large dual Hessian does not by itself control higher primal derivatives. | No such implication is claimed. After conjugation, a compact mollification transfers derivatives to the fixed kernel, leaving only second derivatives of the primal potential to bound. |
| The smoothing samples gradient values with much smaller tolerance. | A 1-Lipschitz positive minorant and the differential inequality \(|g'|\le\eta w(g)\) give explicit exponential transport bounds over the whole physical neighborhood. |
| Averaging gradients could reach the boundary of the open domain. | The average remains within \(w(g_0)/2\) of the central gradient, so its own minorant remains strictly positive; the minorant vanishes outside \(D\). |
| Smoothing changes the moment domain. | Evenness and the uniform Hessian cap prove \(0\le V-V_0\le\eta/2\) globally. Both integrability and divergence are preserved. |
| Only the interior of the moment domain is identified. | The conjugate is finite exactly on \(D\), including exclusion of the boundary. A finite log-concave exponential integral implies a linear tail bound and hence a neighborhood of finite conjugate values. All boundary moments therefore diverge. |
| Surjectivity of the gradient is lost after smoothing. | At every \(g\in D\), \(V-g\cdot x\) is coercive and has a unique minimizer. Its first-order condition is \(\nabla V=g\). |
| The asymmetry of \(D\) breaks necessity. | Compact cutoffs require only the finite moment at \(g\) and total probability at zero. No use of \(-g\) occurs. |
| Weighted integration through an arbitrary finite-order distribution is unjustified. | All higher derivatives of the potential are globally bounded, its gradient grows at most linearly, and every interior tilt has a strict exponential tail bound. These give integrable local \(C^N\) seminorms before interchanging \(T\) and integration. |
| Nonpointed cones or infinite-dimensional target spaces break the argument. | The construction is scalar and the error is measured in Banach norm against distance to the cone complement. No pointedness, matrix diagonalization, or compactness of an infinite-dimensional target ball is used. |
| The proof establishes a quantitative computational procedure. | It does not. The compact-sublevel suprema and entire margin profile may be arbitrarily hard or expensive to obtain. |

The retained hypotheses are finite physical dimension, an open convex domain containing zero, compact support and finite order of the distribution, normalization in the cone interior, and positivity in the cone interior throughout the chosen domain. None has been silently weakened.
