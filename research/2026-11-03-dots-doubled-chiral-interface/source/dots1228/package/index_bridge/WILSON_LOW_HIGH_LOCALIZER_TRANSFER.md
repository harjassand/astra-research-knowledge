# Actual Wilson slab to odd spectral localizer: low/high inertia bridge

Status: new analytic construction, with explicit spectral certificates. Not a numerical observation. The final elementary sampling estimate and normal-chain constants should receive an independent audit before promotion to a theorem. Unlike closed clutching, no model or onsite symmetry is changed.

## Model and continuum target

Use the existing code's dimensionless Wilson matrix divided by lattice spacing a, m=-1, open normal length L sites. Tangential physical torus has side lengths L_i, AP spin structure in x. Boundary mass is M U(x_j) at w=0, with U unitary and Lipschitz B0. The doubled particle/hole Hamiltonian is diag(h,-h)+offdiag(M P0 U). Both flavor copies are implicit. Let D=+sigma.p, B=||[D,U]||<=sum_i||partial_i U||. Let pmin>0 be the AP smallest physical momentum.

The odd-localizer theorem (Loring--Schulz-Baldes, arXiv1802.04518, Theorem on pp1-2) gives for M>=12B and Lambda>2M:

  L_low = [[D_Lambda, M U_Lambda],[M U_Lambda^*, -D_Lambda]],
  gap(L_low)>=M/2,
  signature(L_low)/2=Index(P_+ U P_+ +1-P_+).

Here the cutoff is |p|<=Lambda. Its use below is analytical ONLY: the implemented Hamiltonian remains nearest-neighbor Wilson plus onsite mass. No SLAC implementation is proposed.

## Exact free normal-chain decomposition

For tangential dimensionless momentum k=a p in [-pi,pi]^3, put

  b(k)=sum_i(1-cos k_i), s_i=sin k_i.

In X-normal-chirality basis, the normal chain is an SSH chain with offdiagonal L by L matrix b I minus a one-step shift. Its singular values nu_j satisfy:

* all but the smallest are >=1-b for b<1, by singular-value perturbation of the shift;
* the smallest is <=b^L (use the normalized geometric trial vector);
* if b>1, every singular value is >=b-1.

The tangential Dirac term anticommutes with the normal chain, so energies have magnitude sqrt(|s|^2+nu_j^2)/a. The smallest singular vectors are pure opposite X chiralities. For b<=1/8 they differ from the normalized near/far geometric profiles by at most a universal constant times b^L; this follows by projecting their trial-vector residuals across the >=1-b singular-value gap. Conservative working bound 32 b^(L-1) suffices for all boundary amplitudes/errors below (L>=2).

The near branch has X=+1 and kinetic +sigma.sin(k)/a; the far branch has X=-1 and opposite kinetic. Their normal hybridization is <=b^L/a. Near boundary amplitude r(k) differs from1 by O(b^2)+O(b^L). Far boundary amplitude is O(b^(L-1)).

## A uniform high-sector gap

Keep the two lowest normal branches, both faces, ONLY at |p|<=Lambda. Call this free invariant subspace P; put Q=1-P. Suppose a Lambda<=1/8. Then

  gap(Q h Q)>=g_H:= (2/5) Lambda.

Elementary proof: for b<=1, |s|^2=sum(2u_i-u_i^2)>=b>=2|k|^2/pi^2, with u_i=1-cos k_i. For1<=b<=3/2, |s|^2>=2b-b^2>=3/4. For b>=3/2, the normal gap is >=1/2. In the retained low-momentum region, the excluded normal singular values are >=1-b>=1-(a Lambda)^2/2. These four cases establish the stated conservative bound. This is a full UV/doubler statement, not merely low-energy convergence.

For any texture, the boundary perturbation V has norm M. If g_H>M, Q(H0+V)Q remains gapped and has the same inertia as QH0Q, namely balanced positive and negative counts after particle/hole doubling. Thus every UV contribution is fixed WITHOUT evaluating an infinite eta sum.

## Exact inertia reduction

By finite-dimensional Schur congruence,

  inertia(H)=inertia(H_Q)+inertia(S),
  S=P(H0+V)P-PVQ H_Q^{-1}QVP.

The correction norm is <=M^2/(g_H-M). This bound needs no small gradient assumption. Choose Lambda sufficiently larger than M, e.g. Lambda>=1000 M, so the correction on the near block is much smaller than M/2.

Crucially, this coarse bound must NOT be applied to the gapless-in-volume far face. Set b_*=(a Lambda)^2/2 and delta=32 b_*^(L-1). A normalized low far state has boundary norm <=delta. Consequently its direct mass, near/far coupling through V, and Schur terms carry delta factors. The total difference of S from its near-only Schur block direct-summed with the free far kinetic block has norm bounded conservatively by

  E_far <= b_*^L/a + 4 M delta + 4 M^2 delta/(g_H-M).

This includes the normal hybridization. Requiring E_far<min(pmin/8,3M/16) preserves the free far-sector inertia. For physical pmin and a Lambda<=1/8, L=O(log[(M+1/a)/pmin]) suffices. This is the explicit far-sector contract; AP twist is not being ignored.

## Matching the near block to the continuum finite localizer

There are three errors before the high Schur correction:

1. kinetic dispersion: ||sin(ap)/a-p||<=a^2 Lambda^3/6 (using sum of coordinate errors conservatively replace1/6 by1);
2. normal-profile mass factors: R U_grid,Lambda R versus U_grid,Lambda, with ||R-I||<=2b_*^2+delta;
3. sampled texture versus continuum multiplication compressed to low momenta.

The third is a standard cell-embedding estimate, not an assumed spectral oracle. Embed lattice vectors as normalized functions constant on each cube. For lattice plane waves at |p|<=Lambda, their staircase embedding differs from the continuum plane-wave isometry in operator norm <=C a Lambda. This can be verified exactly using discrete Fourier orthogonality on cells: the overlap is diagonal and its entry is the product of sinc(a p_i/2). Multiplication by sampled U differs from continuum U in sup norm <=sqrt(3) B0 a. Therefore

  ||U_grid,Lambda-U_Lambda||<=2 C a Lambda+sqrt(3)B0 a,

with a fixed universal C (C=10 is ample). This also controls aliasing without any dimension-dependent quadrature oracle.

A sufficient checkable near error bound is therefore

 E_near = a^2 Lambda^3
        + M[4b_*^2+2delta+20a Lambda+sqrt(3)B0 a]
        + M^2/(g_H-M) < M/8.

Then the near Schur block has the same inertia as L_low and gap at least3M/8. Together with E_far<min(pmin/8,3M/16), the complete low Schur complement has the same inertia as L_low direct-summed with the free far block. The high and far signatures vanish, so

  N_negative(H)-dim(H)/2 = -signature(L_low)/2
                         = -Index(P_+ U P_+ +1-P_+).

This holds relative to the constant-texture reference, whose localizer has zero signature. The actual physical sign must be fixed by orientation: the code w=0 branch is +sigma.p, so the earlier continuum calculation gives +s in its existing (x,y,z) and q conventions. Reversing the root/normal orientation gives the desired -s. Do not change this sign silently.

## Resources, gap, covariance

Choose M>=12B, Lambda=1000M, then choose a small enough for the displayed E_near inequality; for fixed Lambda/M and B0/M, a=O(1/M) with an explicit small constant suffices. Choose L by E_far<pmin/8. Total spatial sites are O(Vol(T3) a^-3 L), with fixed onsite dimension (16 fermionic orbitals in the doubled representation). All interactions remain nearest-neighbor in the four spatial directions and onsite at the texture face. The finite physical gap is bounded below by a fixed fraction of min(M,pmin), after accounting for Schur congruence: its condition number is at most (1+M/(g_H-M))^2. There is no uniform thermodynamic gap claim for the untreated far face.

The proof's free Fourier projections are analysis tools and commute with constant onsite V and A generators. Actual H retains exactly U->D(alpha)U covariance and conserved axial particle number. No clutching seam or extra symmetry-breaking frame is introduced.

## Remaining audit points

The normal-chain eigenvector numerical constants (32 etc.) and the cell-embedding norm estimate should be checked independently. They can instead be replaced by explicitly computed singular-vector boundary amplitudes and exact finite Fourier Gram matrices, giving a finite certificate without trusting those constants. No giant occupied-state diagonalization is required. The index sign needs independent convention calibration; the Wilson-to-localizer inertia equality itself does not depend on a chosen naming of degree.

## Brutally explicit existence-scale ledger (not a practical solver)

For a simple one-line conservative choice take Btot=sum_i||partial_i U||, M>=max(12 Btot,pmin), Lambda=1000 M, and a M<=10^-6. Round the grid finer to fit the physical torus. Then a Lambda<=10^-3, b_*<=5*10^-7, g_H-M>=399M. Ignoring the exponentially tiny delta term, the displayed near error divided by M is bounded by

  .001 + 4(5*10^-7)^2 + .020 + sqrt(3)*10^-6/12 + 1/399 < .024.

Thus there is substantial room below the required1/8, without optimization. Choose

  L >= max(2, 1+ceil(log(1040 M/pmin)/log(2*10^6))).

Then E_far<=130 M (5*10^-7)^(L-1)<=pmin/8. The delta contribution to near error is negligible under this same condition when M>=pmin. Thickness is L lattice sites, physical thickness aL; this Wilson root has a bulk gap of order1/a and localization length of order a, so no fixed macroscopic normal thickness was assumed.

If the rotor coarse-cell side is ell and Btot ell=K, the minimum selected M ell is at least12K, and the UV subdivisions per coarse edge are

  ell/a >=10^6 M ell >=12*10^6 K.

Consequently each coarse spatial cell needs at least (12*10^6 K)^3 L four-dimensional slab sites for THIS conservative proof choice. For K=1 this is already about1.7*10^21 L sites; K=100 gives about1.7*10^27 L sites. These are existence resources, not a computationally useful simulation regime. The bounded onsite orbital count does not mitigate this UV volume. Nearest-neighbor single-particle coupling norms are of order1/a>=10^6M; a safe local matrix norm bound is O(10/a). The proof therefore earns a finite-range microscopic existence/index component, not predictive access at these constants.

The final physical gap lower bound is a constant fraction of min(M,pmin), not a volume-independent gap for the far boundary. The full many-body free-fermion charge-sector excitation gap equals the one-particle Fermi gap under the chosen grand-canonical filling, with the usual factor-of-two distinction for fixed-number particle-hole excitations.

## Closing the two elementary constant checks

Normal vectors: let v be the normalized geometric trial vector, so ||T_b v||<=b^L. Expand in right singular vectors. Since every other singular value is >=1-b, the component perpendicular to the lowest right singular vector has norm <=b^L/(1-b). Choose its phase for positive overlap; its distance from v is <=sqrt(2)b^L/(1-b)<=2b^L for b<=1/8. Apply the same argument to T_b^* and the reversed geometric vector for the left singular vector. The near geometric boundary amplitude lies between sqrt(1-b²) and1, so |r_near-1|<=b²+2b^L. The far geometric boundary amplitude is <=b^(L-1), so |r_far|<=b^(L-1)+2b^L. Thus the previously used32b^(L-1) and2b² bounds are safely conservative. This also proves singular-value isolation for L>=2 and b<=1/8; the case b=0 is exact.

Sampling: center the periodic/AP cubes at the lattice nodes. Both J (staircase) and R (continuum plane waves) are isometries on the same low-frequency coefficient space. Their cross-Gram matrix is exactly diagonal:

  (J^*R)_{pp'}=delta_{pp'} product_i sinc(a p_i/2).

No two retained frequencies differ by a reciprocal lattice vector because a Lambda<=1/8. Therefore ||J-R||²=max_p 2[1-product_i sinc(a p_i/2)]<=a² Lambda²/12. The product inequality follows from sinc x>=1-x²/6 and all factors being positive. The safe C=10 used earlier is overkill. The sampled versus true multiplication estimate follows by adding/subtracting J^* U J and using ||U||=1 and the cell sup-norm Lipschitz error. This works directly for the PL Lipschitz texture; no Fourier smoothness or analytic oracle is required.

### Final orientation and audit status
The elementary bounds were independently checked by the constructor, and the full inertia bridge by the audit worker (AUDIT_WILSON_LOCALIZER_TRANSFER.md). Generic far control is E_far<min(pmin/8,3M/16); the explicit ledger already has M>=pmin. Exact primary-index and Bott-generator calibration is now in EXACT_TOEPLITZ_ORIENTATION.md, independently matched by ROOT_ODD_INDEX_SIGN_CALIBRATION.md: Index=+W3=-s for D=+sigma.p, hence Q=+s for the original w=0 face, and Q=-s for the opposite face/chirality. No mass-gradient eta argument is needed for this conclusion.
