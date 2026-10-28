# Nonlinear oscillator-to-continuum packet benchmark

28 October 2026. New implementation by the solver-instrument contributor. This is a numerical benchmark and a derivation of the represented channel. Its floating compression errors have **not** been enclosed by interval arithmetic. It is not the baseline P2 circuit, its notch variant, or a delivered readout waveform.

## Construction

The initial source code is the two-dimensional span of oscillator Fock states |0> and |1>. The source **output** oscillator is untruncated. The bath starts in vacuum. At times 0 and 0.65, apply exact finite-area product-sine kicks

`U_j = exp[-i theta_j sin(Phi_s(t_j)) sin(Phi_b(t_j))]`,

with areas 1.5 and 1.2, source phase amplitude 0.8 and source angular frequency 1. All units in this benchmark are dimensionless. Kicks are declared primitive unitary operations, with no assertion that they approximate a finite-duration physical waveform.

Because source and bath fields commute at the same vertex,

`sin(Phi_s)sin(Phi_b) = (cos(Phi_s-Phi_b)-cos(Phi_s+Phi_b))/2`.

The two cosine terms commute, so the exponential factors exactly. For each cosine factor the Jacobi–Anger functional-calculus identity gives

`exp[-i theta cos Phi(f)] = sum_(ell in Z) (-i)^ell J_ell(theta) D(i ell f)`.

There is no rotating-wave approximation. Truncating |ell| at L has operator error at most

`2 exp(theta^2/4) (|theta|/2)^(L+1)/(L+1)! / [1-|theta|/(2(L+2))]`,

provided |theta|/2 < L+2. This follows by bounding each Bessel power series absolutely, then a geometric majorant of the factorial tail. The implemented L=8 yields a summed analytic tail expression near 2.18e-9. This decimal is a floating evaluation of the displayed analytic bound; it has not itself received outward rounding.

## Exact displaced-Fock closure

Keep packet states `D_s(alpha_s)|n> tensor |alpha_b>` with n in {0,1}. A Weyl vertex shifts the source and bath displacements and multiplies the coefficient by its Weyl phase; it never changes n. The output packet has support at arbitrarily high physical source and bath photon number. Fixed n is a polynomial label of a displaced packet, **not** an output Fock truncation.

For delta_s = beta_s-alpha_s and the ordinary multimode coherent overlap g(alpha,beta), the 2x2 source-label overlap is

`g * [[1, -conj(delta_s)], [delta_s, 1-|delta_s|^2]]`.

This identity supplies the physical Gram matrix. Every retained packet has a two-component coefficient row mapping the complete input code. Consequently `C^dagger G C` is the full input Gram matrix, not merely the norm of one test state.

Compression selects actual packet vectors and projects the current map onto their span. If I is the selected set, the implemented coefficient solution is

`G_II C_new = G_I,all C_old`.

The residual is evaluated from the actual rounded coefficient difference, `R=C_difference^dagger G C_difference`, rather than being assumed equal to a normal-equation expression. In exact arithmetic its operator norm is sqrt(lambda_max(R)); arbitrary source/reference entanglement is then covered. Our calculation uses float64, so the reported residuals are diagnostics. The endpoint is repaired by the input-side polar factor `(C^dagger G C)^(-1/2)`; again, rounded arithmetic is not a proof of exact normalization.

## A genuine positive-frequency continuum test

The continuum run uses

`rho(omega)=v (omega-omega_min) exp[-(omega-omega_min)/s]/s^2`, for omega >= omega_min,

with v=0.5625, omega_min=0.8 and s=0.4. This gives exactly

`<f_t,f_u> = v exp[i omega_min(u-t)] / [1-i s(u-t)]^2`.

Only the two vectors f_0 and f_0.65 occur in this exact kicked model. Their span is exactly two-dimensional; all orthogonal bath modes remain vacuum. A two-by-two Gram factorization therefore realizes the continuum channel on two collective oscillators **with zero temporal-span representation error for this kicked model**. This does not approximate a continuously varying physical bath field by two modes. It cannot be transferred to a smooth pulse without a charged residual theorem.

The reference calculation independently constructs the quadrature matrices of one source and two bath oscillators, diagonalizes the quadratures, and applies the full product-sine exponential. It is repeated at increasing local Fock cutoffs. For comparison, the packet solution is analytically projected onto those Fock spaces; its exact infinite-space input Gram is retained in the full isometry-difference formula. Thus the reported comparison includes photon mass outside the reference cutoff.

## Recorded outcome and useful failures

The final continuum calculation keeps 744 packet vectors. Its selected Gram condition number is about 3.65e7. The sum of floating compression-map norms is about 8.53e-4; the endpoint polar correction is about 1.68e-7. The full input operator differences against the independently computed three-oscillator Fock model are approximately:

| Local cutoff | Complete isometry difference, floating diagnostic |
|---:|---:|
| 12 | 3.078e-2 |
| 18 | 9.137e-3 |
| 24 | 2.693e-3 |
| 32 | 7.205e-4 |
| 44 | 5.784e-4 |

These agree with convergence toward the packet compression scale. They are neither a rigorous upper bound on numerical arithmetic nor a device error rate.

Three failures/limits are informative:

1. **Unweighted Gram pivoting failed.** Every normalized packet had the same diagonal Gram weight, including remote packets with tiny Bessel coefficients. It selected 512 largely irrelevant vectors, gave a roughly 0.072 discarded-map norm at the second factor, and the next expanded matrix exhausted the process memory. Coefficient-weighted pivots fixed this failure for the diagnostic. The unweighted run did not produce a completed receipt; the values are preserved from the actual tool output.
2. **A fixed rank ceiling hid a computational bottleneck.** A continuum run capped at 512 selected vectors stopped at a roughly 0.0015 full-map comparison scale. Its receipt is preserved as `continuum_rank512_receipt.json`. Increasing the cap to 1024 let the adaptive rule stop naturally at 744 and improved the comparison. This is a resource limit, not physical noise.
3. **Near-dependent packets obstruct certification.** The one-bath-oscillator variant reaches Gram condition about 1.93e11. Small normal-equation residuals do not prove trustworthy channel errors at that condition. The continuum variant is better conditioned, but it still needs interval or validated linear algebra before promoting the compression diagnostics to certified bounds. The 512-rank historical receipt was produced before the final source added code-hash metadata and the configurable rank ceiling; it is a diagnostic history item, not an exact-source replay claim.

## Photon effects retain source leakage and all bath photon numbers

The code evaluates generating operators `z_s^N_s z_b^N_b` directly from displaced-Fock kernels. Writing `F=exp[-(||alpha||^2+||beta||^2)/2 + z_s conj(alpha_s) beta_s + z_b <alpha_b,beta_b>]`, the source polynomial entries are

`P00=1`, `P10=z_s beta_s-alpha_s`,

`P01=z_s conj(alpha_s)-conj(beta_s)`,

`P11=z_s+(z_s beta_s-alpha_s)(z_s conj(alpha_s)-conj(beta_s))`.

For the event source vacuum and at least three total bath photons, set z_s=0, subtract bath coefficients 0,1,2 from the value at z_b=1, and sandwich the resulting Gram kernel by the full input coefficient matrix. This produces a 2x2 POVM effect, including off-diagonal source-input coherence. It is independently compared with direct number projection of the largest Fock reference.

The continuum diagnostic yields event probabilities near 0.00361561 and 0.02863903 for inputs |0> and |1>. These illustrate a multiphoton record computation, not a useful detector contrast or a P2 bright/dark error operating point. Physical collection modes, efficiency, deadtime, dark counts and reset have not been supplied.

## Reproduction and scope

Run `python coherent_packet_benchmark.py` for the two-oscillator case and `python continuum_benchmark.py` for the exact two-time continuum case, preferably with `OPENBLAS_NUM_THREADS=1`. They require NumPy and SciPy. Each final receipt pins the core implementation hash; NPZ files retain all final packets, coefficient matrices and Gram matrices. Runtime logs are included.

The reusable capability tested here is: strong non-RWA sine vertices can propagate a finite input code into the unbounded source-plus-continuum output and evaluate complete-input Gram errors and multiphoton effects without a Fock approximation in the packet representation. The decisive outstanding numerical work is reliable compression/linear-algebra enclosure, and the decisive physical work is evaluating an actual finite-duration P2 waveform with its detector kernels. No generic polynomial cost is asserted.

## Prior constructions consulted

- Gheeraert, Bera and Florens, *Spontaneous emission of Schrödinger cats in a waveguide at ultrastrong coupling*, New Journal of Physics 19, 023036 (2017), https://arxiv.org/abs/1601.01545v2. Coherent-state superposition dynamics already treats strong non-Markovian emitted fields. No priority claim is made for that representation.
- Zoufal, Sutter and Woerner, *Error Bounds for Variational Quantum Time Evolution*, Physical Review Applied 20, 044059 (2023), https://arxiv.org/abs/2108.00022v2. A posteriori residual/error ideas are established; the current bridge must be judged at the full-input and retained-output scope.
- Liu and Lu, *Error Bounds for Open Quantum Systems with Harmonic Bosonic Bath*, Quantum 9, 1896 (2025), https://arxiv.org/html/2408.04009v3. The reviewed paper controls changes of reduced physical observables from changes of bath correlations. Its assumptions and output scope do not directly certify the present nonlinear full-output computation.
