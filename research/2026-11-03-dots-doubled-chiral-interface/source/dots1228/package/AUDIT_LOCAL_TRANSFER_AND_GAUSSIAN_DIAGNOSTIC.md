# Audit: charged moves and optimal local transfer

2026-11-02. Independently read ROOT_CHARGED_MOVE_OBSTRUCTION.md and ROOT_OPTIMAL_LOCAL_TRANSFER.md and checked TPF's actual definitions.

## Verdict and correction

The finite full-fiber trace obstruction is correct. The exterior-fidelity identity is correct. **The instruction to average vector symmetry needs qualification:** fixed rotor-configuration endpoint states need not be vector-charge eigenstates, because U(1)V shifts the rotor configurations. Thus vector averaging is not automatically matrix-element preserving at the fixed pair of endpoints. Construct a covariant family of kernels T(phi',phi) under simultaneous rotor shifts, or prove equivariance of the selected ground states and optimal maps. Axial averaging with a common exterior charge and equal-charge endpoint eigenstates is valid as written.

## Definitions, locality and grading

TPF Eq. (73) defines a rotor-controlled sum of oriented Majorana-pair bilinears. The HTML places the scalar 1 outside the pairing sum, while the subsequent parity and paired-vacuum statements use the number-projector normalization. Either convention differs only by a configuration-independent scalar when the number of Majoranas is fixed; the trace argument survives. Eq. (76) adds the scalar rotor charge. On a closed geometry this is the self-linking expression, with the exact-derivative contribution integrating away. Every perfect pairing has the same unrestricted Fock spectrum and trace. Therefore Q(phi')=U Q(phi)U† is impossible if the scalar shift changes. An invertible intertwiner would also force equal traces; hence any allowed finite-dimensional transfer has a kernel. Finite configuration-independent ancillary charges cannot change that conclusion. This says nothing against a partial map on the relevant low-energy states. [TPF §§3.3,4.1](https://arxiv.org/html/2601.04304v2)

The graded tensor product creates no extra trace term: all charge operators are even. Choose a fixed regional CAR factorization, with a region containing an even number of Majoranas or complete complex modes. For equal total-parity endpoint states, X_R is even, so parity projection does not reduce its optimizing matrix element. Do not replace spatial fermion operators by commuting bosonic tensor factors without the grading convention.

The required pairing-closed bounded patch is a genuine hypothesis. Closure under the two pairing graphs, and possibly the physical site/mode partition, can enlarge the region. A local change of coefficients does not by itself prove that the required closed patch remains bounded. Check it on the actual reconnection geometry. The charge decomposition also requires slab charge locality, not just decoration locality.

## Optimal map and symmetry

For X_R=Tr_E |psi><psi'|,

max_{||O||<=1}|<psi'|O|psi>|=||X_R||_1=F(rho_E,rho'_E),

with root fidelity. This is trace-norm duality followed by purification duality; O=V† for X_R=V|X_R| attains the value. It need not be Gaussian even if the endpoints are Gaussian. For endpoint charges q,q', the averaged integrand gains precisely exp[it(q'-q)] in its matrix element when Q_E is common. Equal charges therefore preserve the matrix element, provided the regional action is periodic; otherwise include the appropriate character or use the actual compact-group representation. Parity averaging is also valid under equal total parity. Vector averaging requires the family qualification above.

The first-order anticrossing statement additionally requires an isolated two-dimensional degenerate subspace and a Hermitian rotor-hop term g(|phi'><phi| O+h.c.). The asserted split is then 2|g|a_R. It is not a many-configuration gap theorem. The root note's remaining caveats are appropriate.

## Polynomial Gaussian exterior diagnostic

Yes: the diagnostic can use all occupied slab orbitals without constructing an exterior density matrix of size 2^n. Build the full endpoint Majorana covariance matrices and restrict them to E. This costs polynomial work/storage in total slab modes, not constant work in patch size.

Use G_ij=(i/2)Tr(rho[c_i,c_j]), a real antisymmetric 2n-by-2n matrix. Define

A=I-G_rho G_sigma,
B=I-G_sigma G_rho,
T=(G_sigma+G_rho) B^{-1}.

Then root fidelity is

F=2^{-n/2} det(A)^{1/4} det(I+sqrt(I+T^2))^{1/4}.

This is Swingle–Wang Eq. (4.2); their Appendix C.2 addresses singular cases. It covers pairing/BdG Gaussian states, unlike number-conserving-only formulas. [Primary paper](https://arxiv.org/html/1811.04956v2)

### Numerically safe prescription

Pure-state reductions often contain exactly pure modes, so B may be singular. Do not blindly invert it, discard small eigenvalues, or assume exterior states are full rank.

1. For target absolute fidelity error eta, replace each covariance by (1-alpha)G with alpha=eta^2/(16n). This defines a physical full-rank Gaussian state. In a canonical mode basis, changing each occupation probability by at most alpha/2 gives ||rho-rho_alpha||_1<=n alpha. Purification continuity gives a fidelity bias <=2sqrt(n alpha)<=eta/2. This regularization estimate is an elementary audit deduction.
2. Now sigma_min(B)>=1-(1-alpha)^2. Compute T by a linear solve, not explicit inversion.
3. Evaluate the principal matrix square root by Schur methods; compute determinants in logarithmic form. Do not substitute singular values for eigenvalues inside this non-normal matrix function. Track numerical imaginary residuals and branch choices rather than silently discarding them.
4. Increase precision/check residuals until arithmetic error fits the remaining eta/2 budget. Regularization prevents the exact support singularity, but double precision alone is not a universal accuracy certificate. Nearly zero final fidelities should be reported with absolute-error bars, not artificial relative precision.
5. Cross-check F(rho,rho)=1, orthogonal pure states F=0 in the controlled limit, covariance convention, and small-system Fock calculations. Also check monotonicity a_R<=a_R' when R is enlarged.

The supplied scratch script `check_gaussian_fidelity.py` compares the covariance formula with explicit density-matrix square roots on random 1-, 2-, and 3-mode Gaussian states. Maximum discrepancies were 2.3e-16, 1.0e-15, and 2.8e-15 respectively. This is a convention/sanity check, not a certified large-system implementation.

## Obtaining the actual optimal patch operator

Fidelity alone gives the optimum magnitude, not its phase-coherent local matrix. For a patch of r modes, use Gaussian Schmidt decompositions of each pure endpoint across R/E. There are at most 2^r Schmidt vectors per endpoint. If their weights are lambda_a,mu_b and exterior vectors v_a,v'_b, form

M_ab=sqrt(lambda_a mu_b) <v'_b|v_a>.

Then ||M||_1=a_R, and local Schmidt bases reconstruct X_R. This requires at most 4^r Gaussian exterior overlaps and an SVD of a 2^r matrix, polynomial in exterior size for fixed patch. Exterior Schmidt vectors are Gaussian Fock excitations of their respective Schmidt vacua; use phase-consistent Gaussian/Pfaffian overlap routines. Merely taking square roots of covariance determinant overlap magnitudes loses relative phases and cannot construct X_R. Avoid transition-covariance formulas that divide by a possibly vanishing reference overlap.

This supplies an implementable diagnostic and a route to the optimal contraction, but does not prove that endpoint states of the full interacting proposed interface are Gaussian. Gaussianity is valid for the specified fixed-rotor quadratic slab plus Majorana pairing endpoints; it must be rechecked if extra interactions or constrained superpositions are added.
