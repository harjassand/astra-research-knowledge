> Completed in BACKWARD_CONSTRUCTION.md and the executable exact-arithmetic certificate. Closest prior work directly covers the central mechanism, so this candidate is not recommended as the scientific endpoint.

# Backward positive continuation (interim)

Chosen refined endpoint: recover the full static input-output law of an unknown stable sparse quadratic physical network from a number of full-state equilibrium experiments controlled by local degree, not network dimension, with a deterministic certificate computed from the acquired data. This is a full boundary/cost attempt; it is not yet a claim of new science.

For U(x)=x^T Kx/2, mI <= K <= LI, symmetric K with at most s nonzeros per row, equilibrium experiments with known controls H and observed states X give KX=H. Let A=X^T/sqrt(q). Compute the actual restricted-injectivity certificate alpha=min_{|S|<=2s} sigma_min(A_S). Each row k_i can be recovered by finite support enumeration and least squares. If a fitted s-sparse row has residual <=eta and true row has residual <=eta, then ||khat_i-k_i||_2 <= 2eta/alpha. This inequality is proved directly, and certifies ambiguity bounds on every unknown local coefficient. With exact observations, alpha>0 yields exact law recovery.

Under independent Gaussian controls H_t and a fixed unknown K, a net argument gives alpha >= 1/(2L) with q=O(s log(d/s)+log(1/delta)). All states are read in parallel: experiment count q, d*q scalar outputs, and support-enumeration computation O(d*binom(d,s)*poly(q,s)); certification enumerates binom(d,2s) supports. This does not hide exponential computation in degree. For very large d, compressed sensing is the ordinary faster substitute; the new submission must not claim novelty over it.

After rowwise recovery with error bound tau, threshold |khat_ij|<=tau to zero. Every retained edge belongs to the true support; each deleted true edge has magnitude <=2tau. Symmetrization then has max entry error <=2tau on the true graph, degree <=s, hence spectral error <=2s*tau. If 2s*tau<m, every allowed intervention satisfies ||Khat^-1 h-K^-1 h|| <= (2s*tau)/(m*(m-2s*tau))*||h||. Thus finite errors and missing weak edges are included without a beta-min assumption.

Indispensable assumption is the sparse quadratic constitutive law (and full actuation/readout), not mere smoothness/stability. It cannot be proven over an unrestricted smooth class by finite experiments: the disjoint energy-bump lower construction in INITIAL_FINDING supplies that obstruction. Will complete exact/noisy quantifiers and primary comparison.
