# Acquired tensor-network baseline and exact matching contract

## Outcome

The strongest directly relevant acquired tensor baseline is Nicholson–Gingrich's Doi–Peliti/MPS TDVP ensemble evolution with absorbing target. It can represent this benchmark after adaptation; no matched eight-site computation or certificate has been run here. Source acquisition is complete, but the published repository is not a self-contained runnable matched evaluator.

Paper: Schuyler B. Nicholson and Todd R. Gingrich, *Quantifying Rare Events in Stochastic Reaction-Diffusion Dynamics Using Tensor Networks*, Physical Review X 13, 041006 (2023), DOI https://doi.org/10.1103/PhysRevX.13.041006; primary full text https://journals.aps.org/prx/pdf/10.1103/PhysRevX.13.041006 and https://arxiv.org/pdf/2301.03717.

Paper-specific findings: Sections V–VI and Appendix D explicitly include an absorbing hypercubic target, so the underlying method is not restricted to asymptotic rates. Published experiments use a one-dimensional chain, a basin-conditioned distribution, and a maximum occupancy of 85. Appendix E examines numerical sensitivity rather than giving a rigorous residual certificate. The reported timing starts with an already prepared initial distribution. Paper Eq. (6) uses factorial-divided coefficients, while its numerical parameter discussion needs care when transferred to code. The repository operator is the operational reference for avoiding coefficient ambiguity. No published timing is a matched deadline-one comparison for this benchmark.

## Acquired files and static inspection

Repository: https://github.com/SchuylerNicholson/Rare-Events-using-Tensor-Networks

Pinned commit: `345b3126f46de45e84b9c4c1f6a46aa2e8c5512c` (2026-03-27).

All six Julia source files plus README and MIT LICENSE are preserved byte-for-byte under `upstream/`; all eight Git blob hashes were independently verified. `MANIFEST.json` records hashes. `acquisition.json` preserves fetched text. Figure binaries were not acquired. No upstream source was executed or imported.

Direct reusable source:
- `Experiments/MPO_Mechanisms.jl`: local reaction and adjacent-site diffusion MPOs, including `Schlogl_NoBOutFlow` branch.
- `Experiments/Tensor_Operations_NoQn.jl`: single-site TDVP, tensor projection, contractions and local dimension growth.
- `Experiments/Proj_EscapeProb.jl`: projected initial distribution and time-dependent basin probability driver.
- `Experiments/Schlogl_Evolve.jl`: distribution preparation.
- `Experiments/Escape_Rate_VaryBD_FindErr.jl` and `Escape_Rate_Vary_Diff.jl`: parameter-sweep drivers.

Static blockers, not runtime claims:
1. Three drivers include `Proj_Operator.jl`, absent from the complete repository tree. The MPO calls missing `List_ProjectorCombinations` and `Generate_Projector_Assignment`; these are not defined in any acquired source.
2. `Proj_EscapeProb.jl:98` accesses `psi` without initializing or loading it in that file. It appears to assume an existing Julia session state.
3. No Project.toml/Manifest.toml or saved stationary checkpoint is present in the repository tree.
4. `MPO_Mechanisms.jl:202–207` constructs reverse-direction `DLg`/`DL` corrections but appends only `DRg`/`DR`. Conditional on the absent helpers implementing Appendix D's intended target-boundary projector, this leaves one diffusion exit direction from the target active. An independent algebra reconstruction, not execution of author code, gives both entries `(16,14)->(15,15)` and `(14,16)->(15,15)` rate 131.5312; from `(15,15)`, exit to `(14,16)` has rate zero but exit to `(16,14)` remains 123.3105. See `check_absorbing_diffusion.py` and its JSON output. This does not establish what code produced the paper's published results.
5. Positive `Fix_Norm` terms and the top-zero `IX` operator suppress overflow. They do not implement killing at 163.

The literal operator coefficients multiply falling factorials without additional factorial divisors. Set the exact requested values directly; do not silently recompute slightly different coefficients from the driver's physical constants.

## Exact adapted benchmark contract (independent specification)

State space K={0,...,162}^8; N=163^8=498311414318121121. Target B={0,...,15}^8. Initial state x0=(50,...,50), deadline T=1. Required finite-box answer is p_K=P_x0(tau_B<=1, tau_B<tau_overflow). Any transition that first creates a coordinate 163 kills the trajectory, including diffusion into a full recipient.

Use row-major physical labels 0,1,2,3 / 4,5,6,7 and undirected edges (0,1),(1,2),(2,3),(4,5),(5,6),(6,7),(0,4),(1,5),(2,6),(3,7). Include both directions, 20 directed edges. A column-wise ordering can shorten MPO interaction distances, but must preserve this graph. A 1D MPS representation does not imply a 1D physical graph; nonadjacent-site MPO terms implement the ladder. Practical bond requirements must be measured.

Let S+ and S- be unit-coefficient truncated shift matrices, N=diag(n), Bop=diag(2.676n(n-1)+108.102), Dop=diag(.040n(n-1)(n-2)+37.881n). With column probability convention, build exactly

H_K = sum_i [(S+_i-I) Bop_i + (S-_i-I) Dop_i] + sum_(i->j) 8.2207 [S-_i N_i S+_j - N_i].

All diagonal loss remains at the cap. There are no positive overflow-normalizing corrections. H_K is substochastic. Define P_B as the product of eight local diagonal projectors onto counts 0..15. A particularly simple exact first-hit operator is G=H_K(I-P_B), freezing every target microstate. This also avoids the missing boundary-projector helper. Then p_K=1_B^T exp(G T) delta_x0. Freezing internal target transitions changes no first-entry probability. Use the accumulated target mass at T, not a plateau derivative or an exponential-rate approximation.

For backward propagation, A=G^T and u(t)=exp(A t)1_B; evaluate u(1,x0). On C=K\B an equivalent inhomogeneous equation is u'_C=H_CC^T u_C+c_B with initial zero, where c_B(x) is total original rate from x into B. The target and initial delta are exact rank-one tensors. Do not normalize backward u as a probability distribution; it is an observable with values in [0,1].

## Residual certificate: feasible operation, unmeasured conditioning

This is an application of established Markov semigroup residual control, not a new bound or a claimed result of the acquired paper. For any continuous reconstructed approximation v(t), r=v'-Av,

|u(T,x0)-v(T,x0)| <= ||u(0)-v(0)||_infinity + integral_0^T ||r(t)||_infinity dt
<= ||u(0)-v(0)||_2 + integral_0^T ||r(t)||_2 dt.

The substochastic backward semigroup is an infinity-norm contraction. For piecewise-discontinuous reconstructions, add the norm of every jump. TT/MPS inner products contract the full discrete squared 2-norm without state enumeration. A residual TT can be assembled from the derivative and exact MPO application; any tensor rounding must have its error included. The acquired code's `Overlap_MPS` is an ordinary full 2-norm-squared contraction for real tensors. Its `Eq_Dist` computes a scalar quadratic form, not a residual norm or certificate; local Krylov tolerances are not global residual bounds.

A concrete missing implementation is a validated continuous-time reconstruction and interval-enclosed contraction of its full residual. For a piecewise-linear interpolation between saved tensor states, derivative is constant and residual is affine on each interval. Convexity gives an upper integral bound by the trapezoid rule applied to certified endpoint residual norms. This is rigorous but could require impractically small timesteps; it must be tested rather than asserted sufficient. Higher-order dense output can reduce that burden if the derivative and interval bound are validated.

There is no extra dimension factor in ||r||_infinity<=||r||_2 when the latter is the unnormalized counting-measure norm. If someone reports RMS or uniform-probability-weighted norm instead, multiply by sqrt(N)=163^4=705911761. To obtain a 1e-9 total bound over time one, a full-support roughly uniform residual would need RMS around 1.41660765e-18. A sparse/localized residual need not face this full penalty. The exact initial backward target indicator has 2-norm 16^4=65536; scaling it to unit norm and later rescaling restores the same absolute error requirement. Thus volume/normalization can make naive tolerances misleading, but without execution they do not prove impossibility.

Further hazards: computing ||v'-Av||_2^2 by subtraction of large inner products can suffer catastrophic cancellation; floating point can yield tiny or negative estimates without a valid bound. Forming the residual tensor first, stable orthogonalization, higher precision and/or interval arithmetic are possible remedies, whose cost belongs in the comparison. Interval time coverage, coefficient rounding, tensor contractions, initialization and any truncation all require accounting. No such validated implementation was found in acquired files.

## Fair strongest-baseline comparison

The stronger comparator is an adapted, repaired TT/MPS first-hit evolution on the exact 2x4 killed generator, ideally in both forward and backward forms, with a validated residual postprocessor. It should not be replaced by a rate fit or by code that reflects at the cap. Reproduce small one-/two-site dense operators and both directional target-closure tests first; then run the exact eight-site instance with bond/timestep refinement and report probability, certified absolute error, peak rank, memory and all preparation/certification time. Forward residual control naturally requires a 1-norm bound; using a 2-norm bound there incurs a separate conversion issue. Backward control avoids that conversion but still has the full counting-measure norm conditioning above.

For the unbounded original process, add an independently certified pre-hit overflow allowance epsilon_exit: p_K <= p_unbounded <= p_K+epsilon_exit. The finite-box solve itself has no physical truncation error when the benchmark explicitly specifies killing. A certified estimate p_hat with interior error epsilon_inside yields [max(0,p_hat-epsilon_inside), min(1,p_hat+epsilon_inside+epsilon_exit)] for the unbounded target. Use the already existing overflow work; this acquisition does not duplicate it.

Status: source acquired and statically audited; independent diffusion algebra check executed; adapted solver, eight-site probability and rigorous numerical residual certificate not executed. No novelty or performance conclusion follows from this acquisition.

## Exact MPO rank bound and tiny-system verification

For the physical ordering [0,4,1,5,2,6,3,7], the seven cuts cross [2,2,3,2,3,2,2] undirected edges. Absorb all negative diffusion escape diagonals into each site's local generator. Across a cut, H_K decomposes into H_left⊗I + I⊗H_right plus two product terms for each crossing undirected edge. Thus the exact operator Schmidt/TT ranks are at most [6,6,8,6,8,6,6]. This is a conservative representability bound, not a measured rank or proof of minimality. Multiplication by I-P_B, an MPO of rank at most two, bounds G and A=G^T ranks by [12,12,16,12,16,12,12]. These bounds are independent of local cap. No explicit overflow sink is necessary: missing column mass already implements killing and backward overflow value zero. The backward initial tensor 1_B is rank one and its target values remain exactly one under the true A evolution.

An independent sparse-Kronecker construction was compared with separately enumerated elementary CTMC transitions on (i) the complete eight-site ladder with cap one and target all-zero, and (ii) a two-site system with cap four and target counts at most one, which also exercises cubic deaths. Maximum matrix-entry discrepancies were 4.55e-13 and 1.14e-13, respectively, consistent with floating summation order; target columns were identically zero and column sums were nonpositive up to 5.7e-14 roundoff. This is a numerical algebra smoke test, not an interval proof or eight-site cap-162 integration. See `verify_killed_operator.py` and `killed_operator_check.json`; only independently written code was executed.

The exact operator is therefore not the main representational obstacle: its bond dimension is conservatively at most 16. The unknowns are the solution/residual ranks and validated precision. For endpoint residuals of a piecewise-linear interpolation between rank-chi snapshots, an unrounded derivative uses rank at most 2chi and A applied to an endpoint uses at most 16chi, hence a simple residual representation has rank at most 18chi. Such rank estimates establish feasibility of forming a representation, not adequate residual size or affordable validated contractions.

## Alternative forward weighted-residual certification interface

The proposed forward interface is also valid established residual control. For a column-probability generator Qf and residual r=p_tilde'-Qf p_tilde, substochastic 1-norm contraction gives error at most initial 1-norm error plus the time integral of ||r||_1. For any strictly positive normalized product mass mu on K, weighted Cauchy–Schwarz gives

||r||_1 <= sqrt(sum_x r(x)^2/mu(x)).

The weighted square is a double-layer TT contraction with local weights 1/mu_i. No stationary-distribution assumption is needed. Uniform mu recovers sqrt(|K|)||r||_2; a residual-adapted product mu can improve this, but correlations and tiny mu values can cause poor bounds or conditioning. Selection of mu does not itself establish a useful certificate. Strict positivity, exact normalization or validated normalization bounds, rounding and the time integral must be certified. If mu varies between time intervals, bound each interval with its own valid weights.

One can restrict the dynamic state tensor to C=K\B and accumulate success in one scalar s with s'=c_B^T p_C, treating all overflow as killed. Zero-pad p_C and its residual on B so product weights may still be defined on the rectangular K. Certify the state-tensor residual by the weighted bound and add the absolute scalar success residual to form the augmented 1-norm defect. This avoids representing the full absorbed-target distribution. The success accumulator coupling and its numerical quadrature must be included; renormalizing lost mass would invalidate the killed contract.

The acquired files provide neither full forward residual assembly nor continuous-time derivative output, interval integration of the defect, validated contractions, or certified error records for any SVD/bond change. `TDVP_FwrdPass` advances individual tensors using projected local exponentials and QR; local solver tolerances and conserved total mass do not substitute for a full-generator residual. Saving snapshots enables construction of an independent interpolation/residual postprocessor, but this must be implemented and measured. No actual useful weighted norm was attained in this acquisition.
