# A critical-number interface fails even with perfect grand sampling

29 October 2026. Root has whole-read and accepted the all-occupation analytic theorem at its stated scopes. The independent review is [../../root_boson_ensemble/CRITICAL_MODE_REVIEW.md](../../root_boson_ensemble/CRITICAL_MODE_REVIEW.md).

The fixed native three-site Hamiltonian has PSD frustrated hopping with eigenvalues 0, 2, 12 and the physical noncommuting interaction `sum_i(nb_i-nc_i)^2`. All couplings and one-body diagonal terms are fixed; no occupation cutoff or attractive instability is added.

The main construction changes the critical-mode question in three ways:

* An exact mode-current uncertainty bound gives `H_N>=sqrt(N/12)-1` on EVERY particle sector. The exact zero-chemical-potential grand trace and all its finite number moments are therefore finite.
* An explicitly normalized, number-squeezed trial has sublinear energy `O(K^(2/3) log K)` at K particles per flavor. Hence every common fugacity r>1 makes the grand trace divergent. For EVERY normalizable fugacity, even with a perfect physical grand sampler, the probability of the desired K,K count is at most `binom(K+2,2)^2 exp[beta-beta sqrt(K/6)]`. Adaptive fugacity choices and positive mixtures retain this stretched-exponential postselection obstruction.
* Every FIXED imaginary-time slice count has a polynomial lower tail in K, while the exact trace has a stretched-exponential upper tail. At L=1 the balanced critical grand trace diverges, although the exact physical trace is finite. A declared log-partition error forces at least `Omega(sqrt(K)/log K)` slice growth. This is a necessary mesh condition, not a sufficient mesh theorem or a continuous-time runtime bound.

An exact product-zero-mode projection costs potential energy 4K/3, whereas the number-squeezed trial has sublinear energy and vanishing depleted fraction. Thus knowing the one-particle zero mode and a small depleted fraction does not qualify the interacting critical Gibbs weights.

This is a high-OCCUPATION construction on THREE sites, not fixed-density bulk hardness. Ordinary direct canonical diagonalization is already polynomial in K at fixed mode count, and number-conserving Bogoliubov/squeezed-state methods remain admitted competitors. No lower bound against arbitrary canonical sampling, non-Gibbs umbrellas, temperature reweighting, tensor methods or those condensate corrections follows. No ordered-matter solver or practical advantage was achieved.

`acquire_exact_data.py` checked the fixed 3x3 algebra and evaluated conservative integer consequences in 0.06608 s after imports, using zero RNG draws and zero many-body states. For example, at beta=1, K=10^6 every normalizable-fugacity postselection receiver needs at least 2^329 ideal grand samples in expectation. This is an exact loose bound evaluation, not a sampling benchmark. The analytic proof supplies the all-K result; the finite checks do not stand in for it.

The remaining higher-leverage operation is DIRECT acquisition of an interacting critical sector coupled to an extensive bath or an extensive critical-mode manifold, with its number/coherence correlations and full cost paid. Neither a free interacting weight nor a mixing gap has been acquired here. Historical priority is UNKNOWN.
