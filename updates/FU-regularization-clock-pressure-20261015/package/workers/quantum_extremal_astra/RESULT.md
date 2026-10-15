# Sharp Pauli scalar-noise variance

The exact radial optimum is attained and equals

\[
\boxed{v_*={23\over9}-{2\over9(4K+2)}
       \simeq2.533766977979502.}
\]

Here \(h_0=1\) on \([0,2]\), \(2(s-1)h_0'(s)+h_0(s)+h_0(s-2)=0\) for \(s>2\), and \(K=\int_1^\infty h_0\simeq2.0497559609679565\). The profile is strictly positive and has factorial tails. Set \(c=(4K+2)^{-1}\).

The scalar noise radius has law \(2cs h_0(s)ds\). The measurement is ordinary covariant spin followed by an independent radius with density

\[
q(r)=cr[h_0(r-1)+h_0(r+1)]\mathbf1_{r\ge1}.
\]

Both are positive probabilities. Their full transform is exactly \(\widehat M(t)=\widehat\nu(t)e^{it\cdot\sigma}\), for every vector \(t\), and the scalar law has every exponential moment.

The sharp lower bound is proved by explicit positive dual multipliers for the one-dimensional radial inequalities. It applies to all finite-variance radial scalar noise laws, including singular laws, by common Gaussian smoothing and the explicit covariance charge. Centering and rotation averaging further give \(\operatorname{tr}\operatorname{Cov}(\nu)\ge3v_*\) for general scalar laws; this is not an isotropic matrix bound on an anisotropic law.

The spatial noise density behaves as \(c/(2\pi|z|)\) near the origin. Consequently the all-exponential-moment class has an attained minimum, whereas the subclass of spatially smooth densities has the same infimum without attainment. Gaussian smoothing approaches it.

The new radius improves the supplied Dickman variance \(23/9\), but the measurement remains exactly Blackwell equivalent to ordinary covariant spin: recover its direction using \(n=X/|X|\). The raw unit-direction second moment is \(1+v_*\simeq3.533767\), still above 3 for the usual report \(3n\). No quantum-information or finite-bit implementation advantage is claimed.

The complete proof is in `GLOBAL_OPTIMALITY_PROOF.md`. A separate independent internal audit passed after an explicit endpoint integrability clarification; its artifact is `../pauli_optimal_sol/GLOBAL_DUAL_AUDIT.md`. The corrected numerical adjoint diagnostic has maximum tested residual about \(1.14\times10^{-13}\); that numerical result is not the proof. Initial failed numerical code and output are retained. Exact historical priority, external review, formal verification, and compiled finite-bit sampling remain open.
