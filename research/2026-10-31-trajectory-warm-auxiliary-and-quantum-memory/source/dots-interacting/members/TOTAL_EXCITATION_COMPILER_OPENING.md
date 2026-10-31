# An interacting-reservoir opening through total excitation

Root unreviewed construction, 31 October 2026. It is separate from all accepted/delivered results. The intended new consequence is rapid-damping simulation with genuine number-conserving reservoir interactions, without assuming independent Gaussian mode paths.

## 1. Model and paid operation
Let N=sum_i a_i^dagger a_i. Allow an arbitrary bounded-on-cutoff joint free Hamiltonian H_f satisfying [H_f,N]=0. It can contain non-Gaussian interactions, such as Kerr and excitation-preserving mode couplings, as well as the system drift. Its actual controlled evolution cost on N<=L must be acquired and paid; no generic fast-forwarding is assumed.

Let R_plus=sum_i F_i a_i^dagger, with bounded system-only F_i and accessible block normalizations f_i. Set g=sqrt(sum_i f_i^2). The interaction is R_plus+R_plus^dagger. All mode damping rates are the SAME lambda>0, with J_i=2sqrt(lambda)a_i. Initial reservoir is vacuum. System controls commute with N and are at prescribed times.

Unequal damping with arbitrary mode-mixing H_f is not silently included. Its noncommuting free contraction would need a separate acquired operation.

## 2. Coherent photon removal earns the square-root normalization
For N>=1, photon removal is the isometry

V_minus|n_1,...,n_r> =sum_i sqrt(n_i/N)|i>|n_1,...,n_i-1,...,n_r>.

It is implemented by coherent finite arithmetic on the occupation registers, preparation of the known probabilities n_i/N, and a controlled decrement. Old occupation data can be uncomputed from the post-state and the retained i. No occupation is measured. A separate zero/vacuum flag makes the map a contraction on the whole space. Its inverse unitary's designated block supplies V_minus^dagger.

The stacked system map W/g:psi->sum_i |i>F_i psi/g is also an acquired contraction: prepare index amplitudes f_i/g, apply the supplied normalized F_i block controlled by i, and retain the index rather than unprepare it. Its squared norm is sum F_i^dagger F_i/g^2<=I.

Compose this stack with V_minus^dagger. On the N=n sector the resulting block is

O_plus=R_plus/[g sqrt(n+1)], ||O_plus||<=1.

This proves and IMPLEMENTS the bound ||R_plus Pi_n||<=g sqrt(n+1), rather than spending sum_i f_i or an extra sqrt(r) without need. Its adjoint supplies the normalized lowering block. Products use fresh success flags.

The actual stacked jump is 2sqrt(lambda N)V_minus. Its post-jump mode label is a private Kraus record. One need not enumerate r jump operators with an additional sum-of-norms normalization.

## 3. Scalar occupation majorant, quantum dynamics within each sector
Because H_f preserves N and common damping is2lambda N in the no-jump generator, its free propagation factors into a scalar occupation decay and the charged unitary exp(-i H_f t). Expand only R_plus+R_plus^dagger. A virtual occupation path has scalar ladder weights g sqrt(n+1),g sqrt(n), exactly those of

M=-2lambda n+g(a+a^dagger)

on ONE abstract occupation ladder. Its normalized bridge is the already constructed immigration-death bridge with birth g^2/(2lambda) and death2lambda n. The quantum state WITHIN a sector is never replaced by a scalar: SELECT applies O_plus/O_plus^dagger and the actual H_f interval evolutions in chronological order.

Use a GLOBAL total-excitation cutoff N<=L. A virtual path crossing L selects zero. The source endpoints are only total occupations n,m in0..L, not the exponentially many mode configurations.

## 4. Operator-valued row/column overlap with varying sector dimensions
The physical Hilbert space is a direct sum of excitation sectors, whose dimensions need not agree. On input sector n, a right source isometry copies n into work and prepares terminal label m with amplitude sqrt(E_mn/Rnorm). A left source isometry, on output sector m, copies m and prepares n with the same amplitude. Keep distinct failure tags and append IDENTICAL bridge seeds on both sides.

SELECT leaves the source labels unchanged but applies the actual quantum word, mapping the physical n sector into the m sector. The left inverse then matches the actual output sector. The overlap block Pi_m K Pi_n is E_mn times the conditional operator mean. This is not a matrix-unit replacement of the unknown within-sector state.

Row sums of the scalar occupation kernel are bounded by exp[Gamma*t/2+sqrt(2Gamma L t)], Gamma=g^2/lambda. Windows tau<=1/[16Gamma(L+1)] therefore give a constant no-event normalizer, with no factor r in the number of scalar bridges. The stacked first-jump majorant is the same scalar lowering row as for one oscillator, with integrable squared envelope O(lambda(L+1)exp(-4lambda t)+Gamma). Its normalizer is O(sqrt(L+1)), while actual jump records include the efficiently prepared mode index.

## 5. Physical bounds and boundary of the claim
The number and jump-count weighted-square arguments extend because R_plus R_plus^dagger<=g^2 N. One may complete the square using R_plus^dagger/g as a lowering contraction; its adjoint product is at most N. The free H_f commutes with number. Thus the same Gamma-scale number/count estimates are plausible, and the global-cutoff crossing norm is at most g sqrt(L+1), rather than enumerating mode boundaries.

This would yield a compiler for an interacting, non-Gaussian number-conserving reservoir at common rapid damping, with the actual H_f simulation cost paid. It is not yet accepted: the sector-isometry implementation, global-cutoff limit and complete finite-bit first-event receiver must be independently checked. Arbitrary number-changing free interactions, unequal damping with mode mixing, unpriced bath control or arbitrary thermal nonlinear reservoirs do not follow.

For independent harmonic modes at equal damping the construction might also simplify the existing source. For genuinely interacting H_f it opens a different physical capability. Known diagonal/free number phases may be implemented efficiently when actually supplied; unknown interacting Hamiltonians retain their ordinary cost.
