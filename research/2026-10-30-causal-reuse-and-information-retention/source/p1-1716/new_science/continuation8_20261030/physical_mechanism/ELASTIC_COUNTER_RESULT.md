# Round-eight constructive result and final handoff

30 October 2026. Existing physical-mechanism allocation; all predecessor units are preserved.

## Constructive result

`LOCAL_ELASTIC_MEMORY_COUNTER.md`, SHA256
`3582455c9ca0351afa305e8f0f69d05a6fa547873034c9c5ebef00427cab22eb`,
constructs a local reversible harmonic current bath with prepared elastic memory. The exact initial law is the unit Gaussian visible field on the zero-sum subspace, independent of a Gaussian memory with precision

\[
H_N=\frac{B^TB+N^{-2}I}{[\log(N+1)]^2},
\]

conditioned on `|z_i|<=b_N=sqrt(N)[log(N+1)]^2`. This is an actual stationary initialization premise. Its long-wavelength correlations cannot be supplied by merely waiting from an arbitrary fixed hidden sector.

The physical current is

\[
dJ=-\tfrac s2(B^Tx+H_Nz)dt+\sqrt s\,dW-dR,
\qquad dx=BdJ,\quad dz=dJ.
\]

Reflection acts in the complete direction `(Be_i,e_i)`: its reaction current changes both density and memory. It is fully counted. The precision and runtime forces are local; the prepared covariance is long-range. White noise and ideal conormal reflection are specified mathematical suppliers, not finite-bandwidth hardware claims.

The proof establishes the following together:

* Exact stationary visible Gaussian law at every N, with arbitrary frozen conserved `x-Bz` sectors mixed according to the specified initializer.
* Deterministic all-time circulation cap `|J_total|/N^2<=2[log(N+1)]^2/sqrt(N) -> 0`.
* Ordinary stationary density-fluctuation **whole-path** convergence on physical `N^2T` horizons to the conserved OU field, in `C([0,T],H^(-p))` for every `p>3/2`.
* Ordinary circulation CLT, including its joint independence from the limiting density field. CLT current noise is not suppressed.

The key estimate compares the actual reflected process to its stationary unconfined elastic reference. Its site/time boundary-hit probability is at most a constant times

\[
N^3\left[e^{-c[\log(N+1)]^2}
+e^{-c'N[\log(N+1)]^4}\right]\longrightarrow0.
\]

The estimate uses stationarity, Gaussian tails, a unit-time grid, and a Jensen bound on the integrated Gaussian drift; it requires no mixing of the frozen sector. Before the first hit, the complete actual and reference paths coincide under the supplied Brownian coupling. Fourier covariance and Sobolev tightness then prove the stated whole-path limit. This is not a superexponential comparison at speed N.

## Exact limitation: macroscopic profiles freeze

The root's independently saved `LOCAL_MEMORY_OBJECTIVE_SEPARATION.md`, SHA256
`1279b01f0686da86f8d28dc0b971d873f7bdd77cfe2805afeec62d901511614d`,
sharpens the limitation of this construction. I checked its interface and proof. Since each physical bond current equals its memory increment, for every periodic C1 test function,

\[
\left|\left\langle\rho_N(t)-\rho_N(0),\phi\right\rangle\right|
\le\frac{2b_N}{N}\|\phi'\|_\infty\to0,
\qquad \rho_N=N^{-1}\sum_i x_i\delta_{i/N}.
\]

This is an all-time statement. An order-one nonconstant density profile cannot undergo ordinary heat relaxation. At stationary equilibrium the empirical profile is zero in the limit, while its `N^-1/2` fluctuations can still evolve diffusively. The growing memory admits typical current fluctuations and excludes sufficiently large rare density changes and circulation histories.

Consequently the construction preserves a stationary fluctuation objective, not the full macroscopic density/current action, nonflat heat evolution, exact finite-N ordinary density paths, or the root event gate's suppression of CLT current noise. The distinction follows pathwise, beyond the insufficient exponential scale of the boundary-hit estimate. It applies specifically to per-bond counters; it is not a conclusion about every local controller.

## Resource conclusion

The accepted locality theorem can be sharpened by replacing its worst-case counter bound with the actual equilibrium Fourier susceptibility:

\[
\frac{\mathbb E|X_t-X_0|^2}{\operatorname{Var}X}
\le \frac{4t\mathcal D(F)}{\operatorname{Var}X}
+\frac{8|e^{ik}-1|^2\operatorname{Var}Z_k}{\operatorname{Var}X}.
\]

At diffusive time and submacroscopic interaction range, ordinary visible decorrelation needs `Var(Z_k)` of order at least `N^3`. With an absolute covariance row-sum bound `C b_N^2 xi_N`, the necessary resource is `b_N^2 xi_N` of order at least `N^2`. Coherent prepared memory can therefore replace runtime nonlocal coupling for the weaker stationary fluctuation objective. Uncorrelated memories of sublinear capacity cannot do so by this bound.

This construction is harmonic and continuous-current, rather than binary exclusion. It changes memory capacity and initialization resources while retaining reversibility and local runtime coupling. It neither disproves the bounded-controller jump theorem nor proves sharpness in that jump class.

Keep the close primary resource-bound credit visible: Ogunnaike, Feldmeier, and Lee, PRL 131, 220403 (2023), [DOI 10.1103/PhysRevLett.131.220403](https://doi.org/10.1103/PhysRevLett.131.220403), has an explicit single-mode `k^4/static-structure-factor` bound and area-law sectors that permit diffusion. Root read the actual proof and records the comparison in `../PRIMARY_CONSTRUCTION_COMPARISON.md`. This materially narrows any novelty interpretation of the present susceptibility refinement; known dipole hydrodynamics and single-mode bounds remain primary predecessors. The elastic construction and the declared complete-current/initial-law/resource interfaces are the statements established here.

## Receiving reviews and preserved ordinary alternatives

`receiving_review/LOCALITY_AND_PAIRED_CURRENT_REVIEW.md` accepts the actual pinned root locality theorem, full-range paired-current comparator, and per-bond objective-separation result. The review records the hidden-memory, reversibility, all-current-accounting, finite-range, and primary-predecessor checks. No required correction or further fixture was found.

Root independently accepted the exact elastic-counter proof above. Its detailed receipt is
`../receiving_review/LOCAL_ELASTIC_MEMORY_RECEIVING_REVIEW.md`, SHA256
`a21d6c8f9e40f071afad51af87a28c26bf0bbe6519c7214060fd6274790eeee1`.

The earlier ordinary common-activity comparator remains unchanged:
`COMMON_ACTIVITY_CLOCK_AND_ITS_LIMIT.md`, SHA256
`1aa08bc0ffc04ffb1a024b0628bb7a9a861261568439c4912813e9b40e63ffde`.
Root's actual acceptance receipt is
`../receiving_review/COMMON_ACTIVITY_CLOCK_RECEIVING_REVIEW.md`, SHA256
`136d1b7398cad921fa5fc31a445c335f41d788b577e888db82545f51e221c124`.
That unit proves positive common speed modulation at unchanged mean speed cannot suppress circulation rare events, while explicit deterministic duty cycling or a real global hold offers stronger ordinary alternatives at its separate ports. It is not replaced by the elastic-counter result.

The finite-network event-memory receiving review and its pinned source also remain unchanged. The final local-resource files and exact input snapshots are enumerated in `ELASTIC_AND_LOCALITY_MANIFEST.json`; the prior manifests continue to cover their original units.

No apparatus, new physical experiment, practical speedup, complete unknown-kinetics implementation, or settled priority is asserted. The independent receiving work and constructive alternative are complete for this allocation.
