# Repair: fixed-system local channels from restricted covariance

2026-11-01, 23:06 UTC. This supersedes any interpretation of the earlier Poisson-record construction as an unchanged-lattice, bounded-work-density phase circuit. The independent audit correctly identified that gap. The earlier construction is retained ONLY as a dimension-free correlation proof device. The final channels below act on the original physical data blocks, with fresh disposable environment inside each individual gate and no persistent growing local register.

## Target and exact scope

First prove the memory-only actual recursive code theorem. For a compact sufficiently low finite-temperature interval and strict sufficiently small generic bounded-body local Hermitian perturbations, actual Gibbs states are connected two ways to P_0/2 by standard local CPTP block circuits on the original bounded-dimensional physical system. For every fixed inverse-polynomial requested accuracy these have polylogarithmic range. They are also approximately gate-by-gate locally reversible on the specified source state, with the error bounds below. A bounded-density finite qubit bath can be included for finite-temperature endpoint connectivity; the ground-connection statement is kept memory-only here. A uniformly gapped product bath admits a separate straightforward ground approximation, but is not needed.

This is an extension of the PROOF of Ma–Khemani–Sang2509.15204v3, Sections III.1–III.3, using restricted stretched covariance. It is not a literal application of their full exponential/all-annulus definition.

## 1. The covariance input actually needed

The audited augmented product-work-register representation proves the following mathematical fact uniformly throughout a strict parameter box: for every needed accuracy zeta, every inner ball X of polylogarithmic radius, and arbitrary norm-one O_Y on the exterior beyond distance C log^q(N/zeta),

 |Cov_rho(O_X,O_Y)| <= C zeta + C eta_n,

provided the enlarged inner ball has fewer than d_n physical qubits and the cluster cutoff is below c d_n. This follows from exact P_0/2 factorization and independent local work inputs. No bound on work dimension enters this equality or the norm-one pullback. The representation need not itself be an allowed phase circuit to prove this observable inequality.

The correctability condition must include BOTH the already-polylog inner radius and the correlation-proof lightcone radius. Their sum is still a fixed power of log(N/zeta), hence has volume below polynomially growing d_n for every fixed inverse-polynomial target tolerance. This avoids circularly assuming the unknown standard-system phase channel.

Uniformity covers all spatially inhomogeneous hybrid coefficient choices inside a strict local-interaction box. The analytical smallness norms may be chosen with slack, so changing any subset of local coefficients by a sufficiently small fixed amount stays within the same bounds. There are finitely many bounded-body Pauli interaction types per physical site. This is the OPEN-domain input, not translation invariance.

## 2. Microscopic variation cores avoid any large-inner-ball requirement

Partition the interaction list into O(N) microscopic local terms. Consider one elementary coefficient change h_A of bounded norm and fixed support diameter, with the entire interpolation in the admitted parameter box. Surround A by two buffers B_1,B_2, and let C be the remainder. Set the first buffer width r_1 and choose l=r_1/2 in the MKS LPPL lemma.

The ONLY covariance invoked is between the ball A_{+l} (radius O(r_1)) and B_2 C, separated by r_1-l. Thus the restricted covariance above is sufficient. It is immaterial whether clustering holds for annuli with macroscopically large inner cores. Let G bound the total number of elementary gates in the intended complete path, and allocate epsilon/G to each ideal gate. Choose

 zeta = epsilon/(C G),
 r_1 = C log^q(N G/epsilon),

also increasing r_1 to dominate the LR truncation length. At bounded finite beta, the LR velocity is constant. The exterior marginal change obeys

 ||rho_old^(B_2 C)-rho_new^(B_2 C)||_1
 <= C[zeta+eta_n+exp(-c r_1)].

The local perturbation norm is O(1) because A is microscopic. Choosing r_a=r_1 as in the source's optimized layout is unnecessary; fixed r_a only worsens a polylogarithmic coloring factor.

## 3. Local recovery on the ACTUAL data system

For the target Gibbs state, the locally Markovian bound gives

 I(AB_1:C|B_2) <= poly(N) exp[kappa+mu |AB_1|-r_2/lambda],

where kappa,mu,lambda are fixed at bounded beta. Choose

 r_2 >= C[|AB_1|+log(NG/epsilon)]
       = O(r_1^3+log(NG/epsilon)),

with constants accounting for the square root in recovery error. The twirled Petz recovery map R_new: B_2 -> AB_1B_2 then defines

 E_A = R_new composed with Tr_(AB_1).

This is ONE CPTP gate supported on the original physical block AB_1B_2. Its environment is internal to that gate and discarded; no timestamp, syndrome label or work state survives to the next gate. Approximate recovery and the LPPL estimate give

 ||E_A(rho_old)-rho_new||_1 <= epsilon/G + C eta_n.

Define its local reverse by the same formula using rho_old. That gate has identical physical support and the same estimate in the opposite direction.

## 4. Global circuit, local reversibility, and error floor

Order microscopic cores by a coloring whose radius-r_b blocks are disjoint within each color, where r_b=O(r_1+r_2). Bounded density/incidence gives O(r_b^3) colors. Define each gate using the Gibbs state of its particular sequential hybrid Hamiltonian. Gates in the same color act on disjoint DATA supports, so their sequential product is exactly their parallel implementation even though their offline parameters were chosen for sequential hybrid reference states.

A constant number of parameter slices suffices between finite-beta endpoints in a fixed convex perturbation box. There are G=O(N) gates and depth O(r_b^3), giving range O(r_b^4), a fixed power of log(N/epsilon). Telescoping and contractivity give total error

 E_total <= epsilon + C G eta_n.

For gate i, its actual prefix differs from the ideal hybrid Gibbs state by at most E_prefix. Combining the forward and reverse local errors gives reversal error <=2 E_prefix+2(epsilon/G+C eta_n)<=2 E_total. Thus the constructed circuit is 2E_total-locally reversible on its specified source, exactly in the gatewise sense—not merely endpoint bidirectional conversion.

For nonconvex paths cover a fixed compact path by finitely many slack boxes; only their number enters. No full MKS all-annulus premise has been asserted.

## 5. Commuting cooling uniformly down to the code projector

At V=0 the reference trace gas has weights exp[-sum_j t_j sigma_j], where t_j are dimensionless check coefficients. All small-activity bounds and the graphical correlation proof are UNIFORM for every heterogeneous choice t_j>=t_min with t_min sufficiently large: increasing coefficients only lowers proposal activities. There is no quantum Gram remainder, no filtered-parent flow and no noncommuting smallness parameter that deteriorates as beta grows. Ground-sector corrections remain the same.

The original memory has M=O(N) checks and every valid syndrome sector has dimension 2. With each energy coefficient J_j>=J_min>0, the excited-to-ground partition ratio satisfies

 Z_exc/Z_ground <= sum_(k>=1) binom(M,k) exp(-beta J_min k)
                = (1+exp(-beta J_min))^M-1.

Redundant checks only REDUCE the valid-syndrome count; no independence assumption is made. For beta_max >= J_min^(-1) log(CM/epsilon), the ratio is O(epsilon), hence ||rho_(beta_max,0)-P_0/2||_1<=O(epsilon).

Connect beta_0 H_0 to beta_max H_0 through microscopic coefficient increments bounded by a fixed delta. There are O(log(N/epsilon)) global sweeps, G=O(N log(N/epsilon)) local gates. Every hybrid choice still has t_j>=t_min. The restricted covariance constants remain uniform. Because all these Hamiltonians commute, the annular Markov property is EXACT once B_2 is wider than the check range; no growing quantum Markov constants are needed. One can take r_2=O(1), r_b=O(r_1).

Even using the generic LR estimate, its velocity is O(beta_max)=O(log(N/epsilon)), so choose r_1 to exceed C beta_max log(NG/epsilon) as well as the stretched-covariance scale. All sizes, colors and sweep counts remain polylogarithmic, with polylog-volume inner balls well below distance. Thus the entire commuting cooling/heating circuit has standard physical range polylog(N/epsilon).

Feed P_0/2 in place of rho_(beta_max,0) to the heating circuit. Contractivity adds only O(epsilon) to endpoint error and twice that to each gatewise reversibility error. Reverse cooling maps the finite-temperature reference within O(epsilon) of P_0/2. Concatenate with the bounded-beta generic-quantum circuit. This proves the stated ground-to-thermal standard-system connection without using the growing-record simulation as a physical circuit.

## 6. Constructive gate data: no free marginal oracle

Petz gates use finite Gibbs reduced matrices. Their existence does not automatically make these matrices computationally free. A conservative charged construction is available using the independently earned ideal thermal encoder as an OFFLINE state source and tomography, or exact finite computation if computational efficiency is not required.

For a block X, split H=H_out+H_touch with K=||H_touch||<=C|X|. For every unit vector psi on X, Jensen's inequality in the product of psi and eigenvectors of H_out gives

 <psi|Tr_out exp(-beta H)|psi> >= exp(-beta K) Z_out.

The partition-function bound Z_H<=dim(X) exp(beta K) Z_out gives

 lambda_min(rho_X) >= exp(-2 beta K)/dim(X).

Thus polylog-volume blocks at beta<=O(log N) have inverse conditioning exp(polylog N), not exp(O(N)). Estimate the larger block state to suitably small exp(-polylog N) error, project onto positive full-rank density matrices, and derive its smaller marginal by partial trace. This maintains exact consistency for defining CPTP Petz maps. Finite positive-weight quadrature of the twirled map and a sufficiently accurate Stinespring synthesis give CPTP approximants; tails, conditioning, matrix powers, and local synthesis are charged at exp(polylog) conservative cost. Fresh environment is allowed per gate, but no persistent environment is left between gates.

For bounded-beta noncommuting hybrid states, the existing encoder supplies the required exp(-polylog) accuracy within its cutoff regime and intrinsic floor, at exp(polylog) cost. For commuting heterogeneous states in the cooling leg, the actual classical trace sampler and known stabilizer encoding suffice uniformly; no noncommuting finite-beta theorem is extrapolated to beta_max. Tomography can be performed with failure probability allocated across all G gates. This is offline randomized circuit construction with certified high-probability error, not globally shared runtime randomness.

The final claim is therefore constructive standard block-channel connectivity, with a conservative exp(polylog) offline/synthesis budget. It remains distinct from the earlier polynomial global ideal encoder, and supplies no polylog native elementary-gate runtime or noisy release.

## 7. What changed

The independent audit's work-register objection is accepted, not renamed. Earlier files establish augmented causal representations and correlations. The standard fixed-system phase theorem now rests on restricted covariance plus actual-data erase/recover gates, with a separate commuting cooling leg. The strongest open mathematical dependencies remain the inherited actual-code/Gram/gap inputs and the general Gibbs Markov/recovery/Lieb–Robinson results consumed explicitly above; an independent audit of this repaired join is still appropriate.

## Logical-frame restriction

The result above is specified-STATE connectivity and gatewise reversibility relative to the specified source states. It does not identify the new MKS encoding frame with the fixed protected decoder frame used in the exact-H overwrite/storage theorem. Any logical encoding obtained through the MKS code theorem must be stated in that theorem's own frame and with its own dynamical hypotheses. Do not transfer the earlier exact-H memory lifetime to this circuit without a frame/channel comparison. The separately delivered polynomial ideal thermal encoder retains its own reference-safe unknown-logical-input guarantee.
