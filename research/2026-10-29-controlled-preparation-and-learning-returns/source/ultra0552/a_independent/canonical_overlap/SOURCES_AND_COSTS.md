# Boundary of the overlap investigation

The prior canonical construction and stable continuous finite-part counter in `../canonical_boson/` are frozen. This continuation asks whether unused HS phase moments can repair overlap rather than just produce positive polynomial kernels.

The strongest directly read canonical incumbent is Shen et al., [arXiv:2010.09813](https://arxiv.org/abs/2010.09813), computational details equations(53)–(54): their actual field distribution includes the canonical partition weight and they use heat-bath/Metropolis updates. Its coefficient recurrences, stabilization concerns and correlated sampling are not replaced by the present iid theorem. The frozen PDF SHA is `b38611246ca098051abfbbf66ce8df7652a2cb16fc6a1fc54ac7ce733f2e8cf4`; no new acquisition was required. The existing Yu–Wei–Li primary supplies the source conjugate-Gaussian family, not a variance guarantee. Both papers' governing input/version scopes remain as recorded in the frozen package.

Importance/force-bias proposals, Rao–Blackwell/conditional integration, control variates and cluster methods are ordinary alternatives. They may change the measure or estimator, and are deliberately outside the phase-law obstruction. No absence of an efficient method is inferred from a bounded literature screen. In particular, a correlated field posterior is not an independent product of bounded-size phase blocks, even if its MCMC update is local.

The new analytic results are:

1. `PHASE_LAW_BARRIER.md`: all independent local phase laws and independent fixed-size equal blocks, with arbitrary unused moments, still have exponential DIRECT iid relative-RMSE and constant-envelope rejection cost on a native stable fixed-density family. Required low moments are forced by the physical HS identity up to a common phase. A paid O(M)-bit moment-error condition retains the exponential bound. This goes beyond the prior Gaussian argument; it does not turn the conclusion into an all-estimator lower bound.
2. `GAUSSIAN_RIGIDITY.md`: within the explicitly stated standard independent Hermitian-square, number-conserving conjugate Gaussian class, native paired-hop matrix elements and fixed-sector finite differences force diagonal phase covariance and only a scalar attractive mode. Gaussian factorization/Fierz/charge gauges within that class cannot change the optimum nuisance-integrated weight law. General non-Hermitian or correlated drift, pairing HS, changed estimators and importance distributions are not covered.

No finite optimization or passing small phase table is a premise of either proof. The block32 integer inequality and the all-r>=64 induction have exact Fraction/integer checks in `BOUND_CONSTANTS.json`.

## Actual full-cycle computation

`compile_bound_and_condition.py` compiled the proof constants in0.0003249s. It then executed the strong ordinary positive difference-vector DP on the SAME M64,K64,t4 input in0.0532775s, total0.0541225s after imports. Process startup/import and tool-orchestration time were not independently measured; only the explicit perf_counter measurements are used. There were zero random draws or physical actions.

The DP had2100 states,437414 integer updates and86-bit maximum count integers. It acquired a rational canonical normalizer interval to relative width2.79e-14, with17,976/18,622-bit endpoint descriptions, and similarly qualified a density-difference moment. This is ordinary conditional/occupation computation, not claimed as a new diagonal-model algorithm. The large Fock dimension was not constructed. Peak process memory was not measured.

The saved M64 direct-sample lower bound is1,234,855 for relative RMSE1/10. It applies to the whole admitted phase-law family, including any optimized positive finite alphabet, but it is not a fixed-confidence lower bound for every estimator. The exact optimal-envelope rejection lower bound is a separate consequence. No M64 phase sampling or M9 retuning occurred; costs are not extrapolated into an invented wall-time speedup.

The physical input is a declared mathematical Hamiltonian, not an acquired material or laboratory device. Interactions commute, so there is no Trotter or continuum-time approximation in this discriminator. The DP energy truncation and exponential evaluation are rigorously bounded; it is not an uncharged occupation cutoff or a thermal-state oracle. Historical priority and practical many-body advantage remain UNKNOWN.

## Changed question

Unused local phase moments are not the missing resource. Neither Gaussian reparameterization in the standard class nor bounded-block phase cubature can uniformly cure this overlap. The diagonal comparator shows that an actual conditional operation can do so. For noncommuting frustrated hopping, the scientifically unpaid step is a tractable global conditional contraction/correlated proposal or another estimator, with its own canonical precision and mixing cost. Existing field-MCMC/importance/cluster routes must be admitted when addressing it; this package does not establish that they fail.
