# Checkpoint for root — chosen full construction

Question: Can a retained physical apparatus with an arbitrarily slow, unobserved passive bath be acquired and simulated at its nonlinear observed coordinate, with a computable long-horizon prediction certificate that neither requires resetting/equilibrating the bath nor reconstructing microscopic modes?

Model: x'=-V'(x)-sum_i w_i(x-y_i)+f; y_i'=lambda_i(x-y_i), w_i>=0, lambda_i>=0, sum_i w_i<=B; V is mu-strongly convex. Eliminating the bath gives x'+V'(x)+K*x'=f+g_initial, K(t)=sum_i w_i exp(-lambda_i t). Endpoint is the actual forced nonlinear x trajectory in this supplied physical class, not bath trajectories.

Strongest derived mechanism: for the same prepared initial coordinate and true passive K, an arbitrary passive surrogate xhat with kernel Khat satisfies

||x-xhat||_{L2(0,T)} <= [ ||K-Khat||_{L1(0,T)} ||xhat'||_{L2(0,T)} + ||rho||_{L2(0,T)} ] / mu.

rho includes initial-force mismatch and numerical residual. Proof uses exact passivity integral int e(K*e')>=0 rather than an absolute-kernel Gronwall estimate. Thus no exponential-in-T multiplier, bath spectral gap, finite DC gain, or weak-coupling/smallness premise. Also |e(T)| <= RHS_numerator/sqrt(2mu).

Acquisition: in run r choose a fresh sign s_r AFTER the arbitrary latent initial state is fixed, clamp x=a s_r, and measure bath reaction F_r(t)=a s_r K(t)-g_r(t)+noise. Then s_r F_r/a is an unbiased martingale observation of K(t), even though prior runs altered the bath. Bounded latent energy and sensor noise give explicit Hoeffding-type repeat counts. No matched reset required. The difficult finite-slew/control-bandwidth assumption must still be paid; ideal discontinuous clamps cannot be hidden.

A posteriori kernel certificate from finite noisy samples: K is decreasing, so values on a mesh h and sound node errors bound L1 kernel error by hB+O(T*node_error). A fixed exponential rate dictionary plus nonnegative least squares/linear feasibility retains passivity and is polynomial in target horizon/accuracy, independent of latent dimension (but rate constants and acquisition time can be large).

Novelty concern: strongest primary comparator is Lang & Lu, arXiv:2512.10256 (Dec 2025), published SIAM/ASA JUQ 2026 DOI 10.1137/26M1837290, on trajectory error for approximated GLE kernels. They already handle strongly convex potentials and time-uniform error under structured weighted conditions. My specific passivity certificate avoids their damping-dominance conditions in a narrower model, and the unequilibrated random-clamp acquisition may add something; broad GLE reduction is certainly not new. Astra N1069 already has positive-memory families/slow-mode obstruction; N1607 and N1688 have retained-device thermal acquisition and simulation. Reading exact packets next. This may prove incremental relative to root's correlated Gibbs construction, not a major foundational advance. I will report that candidly if so.

Collaboration send_message tools are not exposed in my available registry; leaving this checkpoint in the shared authorized directory immediately for root.

## Comparator update

Astra N1688 already explicitly acquires impulse response through fresh precommitted random signs on a retained nonstationary apparatus, and certifies the encoded future law for arbitrary bounded causal feedback after a paid guard. Therefore the random-sign/no-reset part is NOT a new primitive relative to Astra. My remaining distinctive candidate is the gap-independent nonlinear continuous-trajectory L2 error certificate for strongly convex V and completely monotone derivative memory, plus an executable finite-data passive approximation. This is a useful restricted extension but currently weaker in ambition than a new broad scientific capability. I am finishing the proof and exact limitations rather than claiming novelty by recombination.
