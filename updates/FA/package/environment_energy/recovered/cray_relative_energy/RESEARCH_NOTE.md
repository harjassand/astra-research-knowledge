# CRAY: Environment-eliminating ground-energy comparison

Research record — 13 October 2026

## Status and scope

This investigation derives a finite semidefinite characterization of the sharp ground-energy comparison that can be certified from a local Hamiltonian pair while leaving the common quantum environment completely unspecified. It includes a constructive converse: a proposed bound stronger than the semidefinite optimum has a finite compatible environment that violates it. The comparison therefore has both positive certificates and adversarial physical-Hamiltonian witnesses.

A nonperturbative spin-1/2 motif gives an exact rational certificate, independent of environment size. A frustrated kagome motif fails, and that failure is explained by an explicit compatible environment rather than attributed to solver weakness. This is not a chemical-accuracy computation for a molecule, an experimental discovery, a general solution of correlated matter, a demonstrated speedup over the strongest specialized method, or an established civilization-changing capability. Historical priority of the particular ground-energy characterization has not been established. The proof is self-contained below; it has not been independently refereed or formalized in a proof assistant.

## 1. Scientific problem selection

Three opportunities were considered before consulting the supplied research repositories.

**Certified local reaction or defect energies in correlated matter.** The scientifically relevant output is often an energy difference, ordering, or barrier—not an absolute electronic energy. However, calculating differences and exploiting cancellation is already established practice. Correlated-sampling auxiliary-field quantum Monte Carlo explicitly targets chemical transformations [2]. Moreover, the FeMo-cofactor model should not be described as classically untouched: Zhai and collaborators' January 2026 preprint, revised 22 June 2026, combines high-order coupled cluster, density-matrix renormalization group, and extrapolation to estimate its ground energy to chemical accuracy [1]. The remaining target here is *certified comparison with controlled physical-model error*, not another unqualified estimate of that model's total energy.

**Complete reaction-path discovery.** YARP-based deep exploration provides substantial concrete reaction-network benchmarks, including glucose pyrolysis [3]. The unresolved computational target considered was a completeness certificate that important pathways have not been missed. No constructive mechanism developed here removes the need to explore the relevant chemistry, so this direction was not pursued merely to produce a network formalism.

**Long-time sensitivity for turbulent design.** NILSAS already confines an adjoint-shadowing optimization to the unstable subspace and avoids cost proportional to the number of design parameters [4]. A credible advance must confront that baseline, rather than rediscover why ordinary trajectory adjoints fail. No convincing way to avoid the remaining dynamical burden was obtained here.

The selected question was whether two many-body Hamiltonians could be compared *without solving either global ground state*. A first sufficient channel inequality was easy. The substantive result was showing that it computes the best bound allowed by a precisely specified local-information contract.

## 2. Exact input/output contract

Let A be an active Hilbert space of dimension d and C an interface of dimension r. The supplied inputs are two finite Hermitian matrices h0,h1 on A tensor C. C must contain the support outside A of every term that touches A. All changes must be included in h1-h0.

For an arbitrary finite additional environment R and an arbitrary Hermitian K on C tensor R, define

    H_j(K) = h_j tensor I_R + I_A tensor K,
    E_j(K) = lambda_min(H_j(K)),
    Delta(K) = E_1(K) - E_0(K).

K is exactly the same in the two systems. It may be interacting, frustrated, gapless, strongly coupled to C, nonlocal, and of arbitrarily large finite dimension. There is no ground-state preparation, tomography, spectral-gap promise, or mixing assumption. Conversely, no locality, norm bound, or antiferromagnetic-sign restriction is imposed on K. These are important qualifications, not technical details.

The output is the smallest closed interval containing Delta(K) for every such environment. This is a robust comparison problem. It is not the problem of determining Delta for one fully specified material. Verifying the common-environment promise from two arbitrary global input lists costs at least reading those lists; that verification is not eliminated.

The energies are unconstrained minima on the full Hilbert spaces. Fixed particle-number or other superselection-sector applications require additional channel restrictions and a sector-specific theorem. They are not covered automatically by the spin examples.

## 3. The comparison operation

Let Phi be a unital completely positive (UCP) map on operators of A. Define

    L(h0,h1) = max_Phi lambda_min[h1 - (Phi tensor id_C)(h0)].

The map is a classical mathematical witness. No physical implementation of Phi is needed.

### Theorem: complete environment-uniform comparison

For every finite Hermitian pair h0,h1,

    inf_{R,K} Delta(K) = L(h0,h1),
    sup_{R,K} Delta(K) = -L(h1,h0).

The extrema on the left are infimum and supremum; finite environments need not attain the endpoints. For every positive epsilon, a finite environment approximates either endpoint within epsilon. An additional space of dimension at most dr suffices for the construction below. Thus the total Hamiltonian dimension of an adversarial construction can be bounded by (dr)^2, independently of any larger proposed environment.

Equivalently, the following statements are equivalent for a real c:

    Delta(K) >= c for all finite R and Hermitian K;

    h1 - (Phi tensor id_C)(h0) >= c I for some UCP Phi.

### 3.1 Sufficiency and exact cancellation

If h1 - Phi(h0) >= cI, with identities on untouched factors implicit, then

    H1(K) - Phi(H0(K)) = h1 - Phi(h0) >= cI.

Unitality is what cancels K. Since H0(K) >= E0(K)I and Phi tensor id is positive,

    H1(K) >= Phi(H0(K)) + cI >= (E0(K)+c)I.

This proves Delta(K)>=c. Complete positivity, rather than positivity just on A, is needed because A can be entangled with C and R.

For example, partial transposition is positive and unital on one qubit but is not completely positive. Applying it to a two-qubit singlet projector produces an operator with minimum eigenvalue -1/2, whereas the original projector has minimum eigenvalue zero. Replacing complete positivity by ordinary positivity would make the proposed inference false.

### 3.2 Minimax dual

Write D=dr and let rho range over density matrices on A tensor C. Both this set and the UCP-map set are compact and convex. The objective is bilinear, so finite-dimensional convex minimax gives

    L = min_rho { Tr(rho h1) - min_Phi Tr[rho Phi(h0)] }.

Let f(rho) denote the expression in braces. Choose a minimizing rho and purify it as a vector psi on A tensor C tensor R, with dim R <= D. Put B=C tensor R and sigma=Tr_A |psi><psi|.

The Schrödinger adjoints of the UCP maps are exactly trace-preserving completely positive maps. Acting on the A part of the purification psi, they produce every density matrix omega on A tensor B with marginal sigma on B. This follows by purifying omega and using an isometry between purifications of the same sigma. Therefore

    g0(sigma) := min_{omega: Tr_A omega = sigma}
                       Tr[(h0 tensor I_R) omega]
               = min_Phi Tr[rho Phi(h0)].

This is the key conversion. The optimal channel problem becomes a conditional-energy problem for a *specific marginal*, rather than an assumed unknown-state oracle.

### 3.3 A finite adversarial environment

Let S be the support of sigma, V:S -> B its inclusion isometry, and sigma_S=V* sigma V. Its dimension s is at most d. The compressed Hamiltonian is

    h0_tilde = (I_A tensor V*) (h0 tensor I_R) (I_A tensor V).

The conditional problem has the dual

    g0(sigma) = max_Z Tr(sigma_S Z)
               subject to h0_tilde >= I_A tensor Z.

This equality has no missing Slater assumption: the primal point I_A/d tensor sigma_S is strictly positive on A tensor S, and a sufficiently negative scalar Z is strictly feasible for the dual. A maximizing Z exists.

Choose B0 >= ||h0|| and a positive eta. Define the environment Hamiltonian

    K = -V Z V* + M(I_B - VV*),
    M >= B0 + B0^2/eta.

Let P=I_A tensor VV* and Q=I-P. On P, H0(K) is positive semidefinite by dual feasibility. On Q it is bounded below by (M-B0)I, while the off-diagonal block has norm at most B0. For vectors p in P and q in Q,

    <p+q,H0(K)(p+q)>
      >= (M-B0)||q||^2 - 2B0||p||||q||
      >= -eta ||p||^2.

Hence E0(K)>=-eta. On the other hand, psi lies in P and

    E1(K) <= <psi,H1(K)psi>
            = Tr(rho h1)-Tr(sigma_S Z)
            = f(rho)=L.

Consequently Delta(K)<=L+eta. Combined with sufficiency, this proves the lower-endpoint equality. Exchange h0 and h1 for the upper endpoint.

This construction does not merely rename the missing computation. It uses a density matrix of dimension D, a conditional SDP of matrix size at most d^2, a purification, and a finite explicit penalty Hamiltonian. All of these are finite operations on sizes bounded by the supplied local matrices.

### 3.4 Quantitative conditioning of the adversary

A small eigenvalue of sigma can make Z large. That cost must not be suppressed. If lambda is the smallest positive eigenvalue of sigma_S, an optimal Z may be chosen with

    ||Z|| <= 2 B0/lambda.

Indeed, dual feasibility implies Z<=B0 I, while Tr(sigma_S Z)=g0>=-B0; these two inequalities bound its most negative eigenvalue.

For a controlled epsilon construction, smooth the minimizer:

    rho_tau = (1-tau)rho + tau I_D/D.

Let B1>=||h1|| and S0=B0+B1>0. Convexity and boundedness of f give

    f(rho_tau) <= L+2S0 tau.

Its A marginal has smallest eigenvalue at least tau/d. The nonzero spectrum of sigma equals that of the A marginal, so lambda>=tau/d. Taking tau=epsilon/(4S0) and eta=epsilon/2, for epsilon small enough that tau<=1, gives Delta(K)<=L+epsilon with

    ||Z|| = O(d B0 S0/epsilon),
    M = O(B0+B0^2/epsilon).

The energy scale of this adversarial environment grows as inverse accuracy; its entries are not promised to resemble a realistic material. Approximate numerical construction also needs rounding/error budgets. The actual implementation supplied here constructs special explicit adversaries, not this entire generic dual-extraction pipeline.

## 4. Constructing the channel: no supplied representation oracle

Use the Choi convention

    C_Phi[(i,a),(j,b)] = Phi(|i><j|)[a,b].

Then Phi is UCP exactly when

    C_Phi >= 0,
    sum_i C_Phi[(i,a),(i,b)] = delta_ab.

Writing h0=sum_ij |i><j| tensor h0_ij, the image is the linear expression

    Phi(h0) = sum_ij C_Phi[i,:,j,:] tensor h0_ij.

Therefore L is the finite SDP

    maximize c
    subject to C_Phi >=0,
               Tr_input C_Phi=I_d,
               h1-Phi(h0)-cI >=0.

It has d^4 real degrees of freedom before equalities in the general complex-Hermitian case, and PSD blocks of sizes d^2 and dr. Identity recovers the usual perturbation interval [lambda_min(h1-h0),lambda_max(h1-h0)]. The map is optimized from the supplied matrices rather than assumed known.

The prototype uses linear outer approximations of PSD cones with eigenvector separation and SciPy/HiGHS. For isotropic two-active-spin examples, covariance under simultaneous spin rotations and complex conjugation permits an eight-real-parameter affine Choi representation. Twirling is valid here because the Hamiltonian pair is invariant and the minimum eigenvalue is concave. This reduction is proved by symmetry, not asserted for general chemistry.

Numerical optimizer bounds are not treated as formal certificates. For the principal positive example, the computed Choi matrix was rounded to rational entries, corrected to exactly satisfy the unital constraint, mixed with a small rational depolarizing component, and then checked by exact rational LDL^T factorization. Both the Choi and residual matrices have strictly positive pivots.

## 5. An exact nonperturbative positive result

Let A contain spins 0 and 1, and let C contain distinct spins 2 and 3. In units where the initial exchanges equal one,

    h0 = S0.S1 + S0.S2 + S1.S3,
    h1 = 2 S0.S1 + S0.S2 + S1.S3.

K can be any Hamiltonian on spins 2,3 and any additional environment. In particular, the two interface exchanges are as strong as the original central exchange; this is not a weak-boundary expansion.

The rational certificate proves

    -3/4 <= E1(K)-E0(K) <= -22421/100000 = -0.22421

for every compatible environment. Thus strengthening this bond is guaranteed to lower the ground energy by at least 0.22421 in these units, without calculating either global ground state.

### 5.1 A short symbolic certificate

Let Ps be the central-pair singlet projector and Pt=I-Ps the triplet projector. With q=1/2, define Schrödinger Kraus operators

    K0=Ps+q Pt,
    Km=sqrt(1-q^2)|s><t_m|, m=1,2,3.

They obey sum_m Km*Km=I. The associated Heisenberg map applied to h1 gives a residual h0-Phi(h1) whose exact spectrum is

    13/8                        multiplicity 5
    7/8                         multiplicity 3
    1-sqrt(2)/4                 multiplicity 3
    1+sqrt(2)/4                 multiplicity 3
    (5-sqrt(13))/8              multiplicity 1
    (5+sqrt(13))/8              multiplicity 1.

This already proves the weaker but transparent upper bound

    Delta <= -(5-sqrt(13))/8 = -0.1743060905...

The exact symbolic script checks all eigenvalues and the Kraus normalization. The stronger rational certificate is supplied separately.

This use of a nonunitary channel is essential for these trace-zero local Hamiltonians: a unitary conjugation, or a mixture of unitary conjugations, preserves the trace. Its residual has trace zero and hence cannot have strictly positive minimum eigenvalue. The useful channel partly transfers triplet weight to the singlet while retaining coherence relevant to the boundary interaction.

### 5.2 Near-sharpness with an explicit compatible environment

A particularly small environment already nearly saturates the optimized result:

    K = t S2.S3,
    t approximately (1-sqrt(33))/8.

Floating-point diagonalization at that algebraic t gives Delta approximately -0.224218635754. A channel reconstructed from the corresponding ground spaces reproduces the same residual minimum numerically. This agreement is not used as an exact proof of the last decimal or of the algebraic optimum.

For a wholly rational independent check, set t=-59307/100000. Exact positive-definite shifts and rational Rayleigh quotients enclose its energy difference in

    [-0.22421874, -0.22421872].

Therefore the sharp environment-uniform upper endpoint lies between -0.22421874 and the proved bound -0.22421: the certificate is within 0.00000874 of optimal for this information contract.

## 6. Canonical controls and a decisive failure

The implemented control models use unit nearest-neighbor spin-1/2 Heisenberg exchanges and double one bond. The 12-site periodic chain and 2-by-2 periodic kagome cell were assembled from their standard geometries, not fitted to the proposed certificate. The kagome graph has 12 vertices, 24 edges, degree four, and eight triangles.

| Control | Ground-energy difference from numerical diagonalization | Local uniform comparison |
|---|---:|---:|
| 12-site periodic chain | -0.571709258083 | rigorously [-0.75,-0.22421] |
| 12-site periodic kagome | -0.599353969884 | [-0.75,+0.25], no improvement |
| Four-spin weakly connected dimer control | -0.748644703216 | numerical [-0.75,-0.745680794] |

The dimer is a deliberately easy diagnostic and is not the claimed scientific advance. The 12-site controls are also small enough for ordinary diagonalization. These runs do not establish a runtime advantage over modern correlated-electron methods, DMRG, bootstrap hierarchies, or exact diagonalization on the same fully specified inputs. No independently supplied molecular benchmark was completed.

### 6.1 The kagome failure is information-theoretic for this patch

The active kagome bond has five distinct interface spins; each active spin couples to three of them. Consider the compatible environment that couples all five interface spins ferromagnetically:

    K_M = M [ (5/2) I - sum_{c<c'} Sc.Sc' ].

Its ground subspace is the fully symmetric interface-spin S_C=5/2 multiplet, with gap (5/2)M. Within that subspace each interface spin projects to S_C/5. Consequently the projected active Hamiltonian is

    J S0.S1 + (3/5)(S0+S1).S_C.

For both J=1 and J=2 its lowest state has active spin one and energy

    e_J=J/4-21/10.

Its energy change is +1/4, not negative.

For a finite rigorous witness, use M=100. The norm of h1 is at most six by the triangle inequality, the environment gap is 250, and a block-compression bound gives

    E1 >= e_2 - 36/(250-12),
    E0 <= e_1.

Hence

    Delta >= 1/4 - 36/238 = 47/476 >0.

Numerical differences are 0.24886634 at M=10, 0.24998807 at M=100, and 0.24999988 at M=1000. The positivity conclusion at M=100 follows from the analytical inequality, not those floating-point numbers.

The other endpoint -3/4 is approached by pairing each interface spin into a strongly bound singlet with a fresh environment spin. The projected boundary interaction vanishes, leaving an isolated active singlet with energy -3J/4. Thus both endpoints of the perturbation interval are sharp in the closure of compatible environments.

The actual antiferromagnetic kagome model has a negative energy change, but the same supplied local patch admits a positive change. No method receiving only this patch and the same unrestricted-environment promise can certify the sign. Adding ground-state stability constraints that are valid for all these same environments cannot change that fact. Additional actual environment information is required.

## 7. Resource accounting and limits

**Input generation.** The theorem starts with accurate local Hamiltonian matrices and a correct common-environment specification. It does not supply an electronic-structure model or infer missing couplings. Extracting a patch from an explicit global term list requires inspecting the relevant list. Verifying that nothing changed outside the patch can require reading the entire input.

**Dense arithmetic and memory.** Store h0,h1 in O(d^2 r^2) numbers and the Choi witness in O(d^4) numbers. A direct image contraction takes O(d^4 r^2) arithmetic operations; dense spectral verification additionally uses O(d^6+(dr)^3) arithmetic operations. A generic SDP solver can require considerably more memory than these matrices. The prototype's outer-approximation iteration count is empirical, not a proved polynomial bound.

**Bit complexity.** With rational input of bounded bit length and explicit norm bounds, the bounded Choi domain and explicit strictly feasible point (depolarizing Choi, sufficiently negative c) put additive weak optimization within standard polynomial-bit SDP machinery. This is polynomial in the *matrix dimensions* and input/accuracy bit lengths—not in the number of active spins. Exact rational LDL^T verification is finite polynomial-bit linear algebra. Approximate solver output must be repaired and independently checked; raw eigenvalues near zero are not a certificate.

**Exponential local dimension.** For k active spin-1/2 variables, d=2^k and the Choi matrix contains 16^k entries. Already k=8 gives about 4.3 billion entries, approximately 69 GB if stored as complex doubles, before solver overhead. A small active-region assumption is indispensable. No unprovided tensor, low-rank, or sparse-channel structure is assumed to remove this cost.

**Precision and global cancellation.** The unknown K cancels symbolically before numerical arithmetic. Large extensive energies never need to be subtracted. The residual still needs ordinary certified spectral accuracy on its finite matrix. The sharp uniform interval may be wide even with exact arithmetic; that is a physical-information limitation, not rounding error.

**Model discrepancy.** If the true Hamiltonians differ from the modeled pair by noncommon errors with norms eta0,eta1, enlarge the interval by eta0+eta1 on each side. Arbitrarily large errors confined to an exactly common environment term cancel. A common error touching A does not generally cancel: its residual is delta h-Phi(delta h). Long-range electronic terms, fixed-charge sectors, basis truncation, nuclear relaxation, and finite-temperature free energies are not solved by the theorem.

**Randomness and hardware.** No quantum device, physical channel, quantum sampling, or state preparation is used. Exact certificate verification is deterministic. Floating-point numerical controls use standard eigensolvers; they are not substitutes for the exact certificate checks. Recorded core runtimes were roughly 0.15 seconds for the symmetry-reduced chain optimization and 0.055 seconds for constructing/checking its rational certificate in this container. These small-matrix timings are not general scalability claims.

**Output and calibration.** The primary output is two numbers plus finite matrix witnesses. No extensive wavefunction is requested. Experimental calibration costs belong to acquiring h0,h1 and their error bounds; no calibration procedure was demonstrated here.

## 8. Information refinement without a hidden locality oracle

For a fully supplied local lattice model, a constructive refinement algorithm is available: start with A containing the changed terms, collect its complete interaction collar C, solve both comparison SDPs, and enlarge A when the interval does not settle the requested decision. The channel from a smaller region can be tensored with the identity on newly included degrees of freedom, so the certified intervals cannot widen. At the full finite system, the comparison is exact, but that final step is exponentially large.

There is no proved small-radius guarantee for important chemical systems. Merely adding a common term supported only on C to both h0 and h1 does not help this certificate, since it cancels under id_C; actual environmental information must change the allowed-environment contract, for example by incorporating more sites into the modeled active region and moving the interface outward. An inexpensive verified comparison radius would be useful new structure. This investigation discovers no theorem ensuring that radius is small on realistic correlated catalysts.

## 9. Prior-art boundary and research capital

Choi's characterization of completely positive maps is established mathematics [5]. Exact local energy-extraction optimization by semidefinite programming is already developed in CP-local passivity [6]. Quantum majorization and statistical comparison provide closely related complete channel-comparison criteria [7]. Completely positive domination of matrix pencils is also established [8]. Therefore the basic channel inequality and its SDP representation cannot responsibly be presented as a wholly new mathematical language.

The candidate contribution is the exact identification of a paired ground-energy extremum over arbitrary common environments with a single local UCP comparison, including the finite adversarial-environment construction and its resource bound. Its novelty relative to those literatures remains unresolved. The independent proof is evidence of correctness under the stated contract, not evidence of historical priority.

Bootstrap ground-energy methods already provide rigorous local and thermodynamic-limit bounds [9]; recent defect-bootstrap work explicitly improves constraints using ancillary defect models under additional physical assumptions [10]. No measured advantage over these strongest relevant certifying methods was established here.

The supplied repositories were consulted selectively after developing the opportunity. Targeted searches in openai/math did not yield a result used as a premise. Astra's N681 replica-programmed-operation dossier was examined as a possible CP-operation connection; it has a different information contract involving source-state copies and physical routed-channel access. Its claims were not imported into this proof. No repository write or independent audit of the full capital was performed.

## 10. Outcome

The completed mathematical operation computes an optimal *environment-uniform* local ground-energy interval and, in principle, returns a finite counterenvironment when a stronger claim is impossible from those inputs. A nonperturbative motif has a machine-checkable rational certificate and a near-matching explicit environment. A frustrated benchmark has a rigorously explained failure.

The original scientific target remains accurate, certified reaction or defect energies in important correlated materials. This record does not meet that entire target. The missing advance is a constructive way to use realistic environmental structure and obtain tight comparisons while keeping the active dimension manageable. Additional isolated-spin demonstrations would not close that gap.

## References and retrieval scope

[1] H. Zhai et al., *Classical computational simulation of the FeMo-cofactor model to chemical accuracy and its implications*, arXiv:2601.04621v2, revised 22 June 2026. Abstract and version history checked; the chemical-accuracy claim uses extrapolation and is not adopted as an independently certified interval.

[2] J. Shee et al., *Chemical Transformations Approaching Chemical Accuracy via Correlated Sampling in Auxiliary-Field Quantum Monte Carlo*, JCTC 13, 2667 (2017), arXiv:1703.01545v2, DOI 10.1021/acs.jctc.7b00224.

[3] Q. Zhao et al., *Deep reaction network exploration of glucose pyrolysis*, PNAS (2023), DOI 10.1073/pnas.2305884120, PMID 37579176. Primary abstract/research description used, not a claim that the network is universally complete.

[4] A. Ni and C. Talnikar, *Adjoint sensitivity analysis on chaotic dynamical systems by Non-Intrusive Least Squares Adjoint Shadowing*, arXiv:1801.08674v4, JCP (2019), DOI 10.1016/j.jcp.2019.06.035.

[5] M.-D. Choi, *Completely positive linear maps on complex matrices*, Linear Algebra and its Applications 10 (1975), DOI 10.1016/0024-3795(75)90075-0.

[6] A. M. Alhambra et al., *Fundamental limitations to local energy extraction in quantum systems*, PRL 123, 190601 (2019), arXiv:1902.02357v2. The SDP/local-passivity theorem and PDF page were inspected.

[7] G. Gour et al., *Quantum majorization and a complete set of entropic conditions for quantum thermodynamics*, Nature Communications 9, 5352 (2018), DOI 10.1038/s41467-018-06261-7. Definition and complete comparison theorem inspected.

[8] I. Klep and M. Schweighofer, *Infeasibility certificates for linear matrix inequalities*, arXiv:1108.5930. The CP-domination/matrix-pencil section was inspected. Its boundedness/strict-feasibility assumptions are not silently transferred to a different assertion.

[9] S. Lawrence, *Bootstrapping Lattice Vacua*, arXiv:2111.13007 (2021).

[10] M. G. Scheer et al., *Defect Bootstrap: Tight Ground State Bounds in Spontaneous Symmetry Breaking Phases*, arXiv:2511.20860 (2025). Abstract-level comparison; its additional defect-diamagnetism condition is important.
