# Receiving review: locality cost, paired currents, and objective separation

30 October 2026. Reviewer: the existing physical-mechanism allocation. This is an actual-file mathematical and physical-scope review. It adds no worker, apparatus claim, priority claim or new numerical fixture.

## 1. Exact inputs and disposition

| Actual input | SHA256 | Preserved snapshot |
|---|---|---|
| `LOCALITY_COST_OF_CURRENT_CONTROL.md` | `75a50fa72e31c7544d3d9c0f80b0eeb497d8ce1a2f32b37e228efd152cfe7cf2` | `LOCALITY_COST_REVIEWED_75a50fa72e31.md` |
| `PAIRED_CURRENT_COMPARATOR_AND_DENSITY_LAW.md` | `ac447c32d63cba927aad46c4c81326a372590844ce8a7921a0d5537f9f2eea05` | `PAIRED_CURRENT_REVIEWED_ac447c32d63c.md` |
| `LOCAL_MEMORY_OBJECTIVE_SEPARATION.md` | `1279b01f0686da86f8d28dc0b971d873f7bdd77cfe2805afeec62d901511614d` | `LOCAL_MEMORY_OBJECTIVE_REVIEWED_1279b01f0686.md` |

**Disposition: accept the exact scoped statements in all three inputs. No required correction was found.** The first is a reversible bounded-controller resource theorem. The second supplies an exact harmonic comparator at an explicitly stronger nonlocal current port. The third applies specifically to the per-bond elastic-counter construction and correctly separates its stationary fluctuation objective from macroscopic profile evolution. None is a universal prohibition on current control.

## 2. The locality proof controls the visible mode

I reconstructed the corrected Fourier coordinate rather than relying on a spectral-gap interpretation. With the actual current convention `(Bj)_i=j_(i-1)-j_i`, one obtains

\[
\Delta X=(e^{ik}-1)\sum_i e^{iki}j_i.
\]

The exact counter condition removes the constant Fourier part from `Delta F`, where `F=X-(e^{ik}-1)Z_k`. Choosing an origin inside each event's common circular support gives the stated extra factor `k R_N`. Wrapping the interval across the periodic seam causes no problem because `exp(ikN)=1`. This argument requires the union of current and memory updates to share the stated support; a remote bit update does not qualify as local merely because each component separately has small support.

The pointwise total-event-rate and l1 update budgets give the stated Dirichlet bound. The equilibrium spectral inequality

\[
\mathbb E|F_t-F_0|^2\le 2t\mathcal D(F)
\]

is valid for a reversible, possibly reducible process and complex `F` by treating its two real parts. No hidden-state mixing is used. The bounded memory contribution is at most `2bN|e^{ik}-1|`; the constants in the resulting displayed inequality follow from the squared triangle bound.

The exact canonical variance `M_N(N-M_N)/(N-1)` is correct. Consequently, at fixed positive equilibrium density, the estimate concerns the actual stationary visible density autocorrelation. It is not a spurious slow mode confined to an unobserved conserved memory. The `N^4/R_N^2` lower relaxation scale and failure of fixed-fraction diffusive decorrelation when `R_N=o(N)` follow for the stated fixed budgets.

## 3. Hidden memory, omitted motion, and approximate counters

The hidden state may be arbitrarily large or frozen. Only reversibility of the actual complete generator and the supplied canonical visible marginal enter. Unrecorded physical particle motion would invalidate the premise `Delta eta=Bj`; the proof does not license omitting it. A physical circulation with zero visible divergence must still appear in `j` and therefore in the support and current budget.

For imperfect counting, the decomposition into the scalar mismatch `e_a` and the support remainder produces the stated factors of two in the Dirichlet estimate. The required quantity is the actual rate-weighted quadratic mismatch, not merely observed small variance of an output current. A modulo-counter wrap has a genuine large update or mismatch; relabeling the stored value does not erase it. External memory flips and apparatus-induced motion must be included on the same basis.

The theorem deliberately does not cover nonreversible generators, growing update/rate budgets, growing memory, or other ways of reducing a current's variance without this counter relation. Those are premises to compare, not logical errors in the result.

## 4. The paired-current comparator supplies the claimed full path law

The drift and noise in the supplied bath form a compatible reversible pair with state generator

\[
\mathcal Lf=-\tfrac12(BCB^Tx)\cdot\nabla f
+\tfrac12(BCB^T):\nabla^2f.
\]

The unit Gaussian on the zero-sum subspace is invariant. The ordered full-range pair sum is `2N P`, where `P=I-11^T/N`, so the normalization in the input gives `C=sP`. The identities `BP=B` and `PB^T=B^T` are exact. They establish equality of the entire density generator with the ordinary `C=sI` bath. Coupling the two supplied architectures with one mathematical Brownian path then makes their density paths identical for any common initial density, at every finite N and horizon.

The total physical paired current is zero, whereas the reference's total current has variance `sNt`. This is not the reassignment of an unmodified physical current to a different observable: the pair bath is an actual different covariance and matching force-response port. The input states that substantial requirement. Its proof coupling does not require a hidden specimen to be copied in an experiment.

The finite-range Fourier calculation is also correct. Expanding `|1-exp(ikr)|^2` uniformly for `r<=R=o(N)` and using `sum r^2=R(R+1)(2R+1)/6` yields the coefficient `s(N-1)(R+1)(2R+1)/(24N)` multiplying `k^4`. Inclusion of separation one removes extra commensurate null modes. Full-range operation restores the ordinary `k^2` decay rate. This attains the analogous range scaling in the specified harmonic bath, without asserting sharpness inside the exclusion jump class.

Ideal white-noise covariance, paired dissipative response, and nonlocal simultaneous currents remain actual supplier premises. They are not supplied merely by knowledge of an invariant law or by a sensor.

## 5. A sharper memory resource corollary

The locality argument admits a useful refinement, not a correction. Centering the memory mode and using stationarity gives

\[
\frac{\mathbb E|X_t-X_0|^2}{V_N}
\le\frac{4t\mathcal D(F)}{V_N}
+\frac{8|e^{ik}-1|^2\operatorname{Var}(Z_k)}{V_N}.
\]

With the other budgets fixed and `R_N=o(N)`, fixed-fraction visible decorrelation on `N^2` time therefore requires fundamental-mode memory susceptibility of order at least `N^3`. If the actual memory covariance has absolute row sum at most `C b_N^2 xi_N`, this implies `b_N^2 xi_N` of order at least `N^2`.

Thus local capacity and spatial covariance are distinct resources. Short-correlated memories need capacity of order N in this bound; the weaker worst-case threshold of order `sqrt(N)` allows coherent long-wavelength storage. The separately saved `LOCAL_ELASTIC_MEMORY_COUNTER.md` constructs such prepared coherent storage in a harmonic continuous-current system, at a weaker path objective. This does not alter the accepted exclusion theorem.

## 6. The per-bond objective-separation result has the right interface

The actual elastic construction satisfies `dx=B dJ`, `dz=dJ`, and `|z_i|<=b_N`, including reflection forces. Hence `x-Bz` is conserved. For every periodic C1 test function, its empirical macroscopic density obeys the stronger all-time bound

\[
\left|\left\langle\frac1N\sum_i[x_i(t)-x_i(0)]\delta_{i/N},\phi\right\rangle\right|
\le\frac{2b_N}{N}\|\phi'\|_\infty.
\]

The input's fundamental Fourier bound follows with `||phi'||=2pi`. With `b_N=sqrt(N)[log(N+1)]^2`, an order-one density profile is frozen on every time scale. This is fully compatible with a stationary Gaussian marginal and ordinary density fluctuations: multiplying the bound by `sqrt(N)` leaves a divergent allowance at the fluctuation scale.

The proof depends on **per-bond** exact counters, a stronger architecture than the locality theorem's total-counter premise. The input explicitly makes this restriction; there is no interface mismatch. It also correctly rules out equality with ordinary heat relaxation or its full speed-N density/current history action, including under stationary initialization at the rare-history scale.

## 7. Close primary predecessors and priority limit

The following primary sources were inspected for mechanisms and comparison, not treated as proofs of the new finite-size statement:

* Hexner and Levine, *Noise, diffusion, and hyperuniformity*, [arXiv:1611.02386](https://arxiv.org/abs/1611.02386), PRL 118, 020601 (2017). Their center-of-mass-conserving active model already changes fluctuation noise while retaining ordinary mean diffusion. It is not the reversible canonical bounded-memory interface here.
* Morningstar, O'Dea, and Richter, *Hydrodynamics in long-range interacting systems with center-of-mass conservation*, [arXiv:2304.12354](https://arxiv.org/abs/2304.12354), PRB 108, L020304 (2023). Variable-range equal/opposite pair transfers and their subdiffusive/diffusive dispersion are direct predecessors for the paired-current comparison.
* Meerson, *Relaxation and fluctuations of a mass- and dipole-conserving stochastic lattice gas*, [arXiv:2406.03462](https://arxiv.org/abs/2406.03462) (2024). The inspected local dipole-conserving dynamics and fourth-order hydrodynamics are close to the zero-memory local-pair case. The bounded controller memory, finite-size visible covariance inequality and explicit leakage budget are additional conditions in the present statement, not a claim that fourth-order relaxation is new.

The inspected sources and targeted search do not settle priority for the particular memory-susceptibility/resource bound. An unsuccessful search is not evidence of novelty. The Gaussian projection comparator itself is explicitly an ordinary construction.

## 8. Validation boundary

This review reconstructed the exact algebra, stochastic-generator identities, covariance normalization, and physical current interfaces. No additional numerical fixture was needed. It accepts the pinned mathematical statements and their declared idealized suppliers, not an apparatus, practical speedup, universal exclusion-class sharpness, or a new universality class.
