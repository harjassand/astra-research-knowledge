# Microscopic reconnection test and failed smooth-mass interface

## Status and scope

A local symmetry-neutral **partial** decoration/slab transfer operator was constructed. Its decoration factor was fully diagonalized. A separate, geometrically faithful cubic Wilson-slab endpoint test then rejects the smooth-mass implementation: slab ground-state axial charge fails to compensate the exact cochain self-linking change. Thus no combined gapped interface or thermodynamic gap is claimed. The minimal S3 decoration calculation is not falsely identified with the cubic slab geometry.

## Explicit decoration move

Use the boundary of an oriented 4-simplex with vertices 0,...,4 and tetrahedron orientations (-1)^i on the face omitting i. Rotors are period-one, m_ij=round(phi_j-phi_i), n=dm, s=integral m cup n. Take

phi=(.39162483,.18725257,.34596067,.51106597,.89120941),
phi'=(.77556394,.18725257,.34596067,.51106597,.89120941).

Only m_01 changes, 0 to -1, and s changes 0 to 1. One complex decoration fermion sits on each triangular face, split into the two incident-tetrahedron Majoranas, exactly as in the primary model. Construct pairings across faces with even n and inside tetrahedra along odd n. Orientation signs were solved over GF(2) to obey the primary parity identity for **all 384 generic rotor chambers** on this triangulation. The enumeration fixes phi_0=0 modulo global shifts; each other phi has one of two half-circle bits and the four residual coordinates have one of 24 orders. This verifies the requisite parity identity here, rather than asserting a general orientation construction on arbitrary meshes.

The changed matching has eight Majoranas numbered (8,9,11,12,13,14,16,17) by the supplied code. Old bonds are (8,17),(9,11),(12,16),(13,14); new bonds are (8,11),(9,13),(12,14),(16,17). Let P and P' be products of the signed bond ground-state projectors (1+i s_ab gamma_a gamma_b)/2. Exact 16-dimensional Fock-space diagonalization gives endpoint spectra, for H_dec=-sum signed i gamma gamma,

    -4 (multiplicity 1), -2 (4), 0 (6), 2 (4), 4 (1).

P' gamma_a P has rank one and norm 1/sqrt(8) for every vertex of this alternating loop. It is odd. Its polar normalization sqrt(8) P' gamma_a P has norm one and maps the two decoration ground states exactly, up to phase. The normalization is not an intrinsic physical suppression. Its rank-one kernel is real and prevents using it as a full-fiber unitary transporter.

On these decoration ground states the charge change is +1. Therefore multiply the rotor move and P' gamma_a P by creation of a microscopic slab fermion of (V,A)=(0,-1). The full term is even, has total axial charge zero on the selected sectors, and is vector neutral. Axial group averaging makes an exact charge-sector operator on the full finite fiber if required; its support only expands over the fixed neighborhood of the affected pairing bonds. The complete rotor-shift kernel must be defined covariantly on simultaneous global shifts; the local cochains and pairings depend only on rotor differences, not on an absolute global rotor reference. This is a bounded local partial transfer term, not a statement that its matrix element between slab ground states is nonzero.

## Actual finite-range free slab

The Wilson representative chosen for the paper's class-A root is

    h(k)=sum_{mu=1}^4 sin(k_mu) Gamma_mu
         + [-1+sum_mu(1-cos(k_mu))] Gamma_5.

Gamma=(X⊗X,X⊗Y,X⊗Z,Y⊗I,Z⊗I). Space is a cubic 3^3 torus times an open normal chain of thickness L. All normal-direction orbitals and all four Weyl species are retained. A Freudenthal triangulation of the physical 3-torus computes s from the actual vertex rotors. Antiperiodic spin structure in x removes exact desired-far-surface zero-mode occupancy ambiguity while preserving both global U(1)s. The antiperiodic finite-volume gap is NOT an interface gap certificate.

After particle-hole conjugation of the two A=-1 species, the exact single-particle Hamiltonian is

    H(phi) = [[h⊗I_flavor, M P_boundary U(phi)],
              [M U(phi)^dagger P_boundary, -h⊗I_flavor]].

The particle-hole conjugation uses R=Gamma_1 Gamma_3, which intertwines the transposed Wilson operator appropriately. All transformed fermions carry axial charge +1, so Q_A=N_occupied-2 dim(h). Two trial mass prescriptions were tested:

1. U=diag(z,z*), z_x=exp(2 pi i phi_x).
2. U_x=[[z_x,b_x],[-b_x*,z_x*]]/sqrt(1+|b_x|^2), with
   b_x=lambda[z_(x+ex)-z_(x-ex)+i(z_(x+ey)-z_(x-ey))].

Both are finite-range, exactly periodic in each rotor, and covariant under V: U -> exp(i alpha tau_z)U. The second supplies an explicit local off-diagonal/core-mixing attempt; it is not claimed to be the unique correct framing prescription.

## Decisive endpoint failure

The supplied deterministic search finds a one-vertex change of size 2e-5 in period-one angle, crossing only the m_01 rounded-edge wall. It changes s: 0 -> -1. Endpoint arrays and the whole triangulation are saved in cubic_move.npz.

Complete diagonalization gives:

- L=3, all M in {.5,2,8}, lambda in {0,.4}: N_occupied=648 at BOTH endpoints.
- L=5, same parameters: N_occupied=1080 at BOTH endpoints.

Thus Delta Q_A,slab=0, not the required +1. All twelve parameter choices fail the necessary charge-matching test. No local operator, including higher-degree polynomials or the optimal local operator, can yield a symmetry-preserving matrix element between the two combined endpoint ground states when their exact total charges differ. A formal neutral hopping instead connects an endpoint ground state to an excited state.

For representative L=3,M=2,lambda=.4, the entire 1296-dimensional spectrum is saved in complete_endpoint_spectra.npz. Endpoint one-particle gaps about zero are .5611398921852024 and .5611371445249995. The exact matrix difference has numerical operator norm .00016439297636523022, far below that gap. These are double-precision computations, not interval-arithmetic certification.

The initial periodic-spin-structure run had exact far-boundary zero modes, so its raw counts based on floating-point signs were invalid. That failed script is retained as wilson_endpoint_periodic_failed.py. It is not evidence for charge transfer. The corrected antiperiodic runs use a consistent nonzero finite-volume Fermi gap.

## General reason the smooth ansatz cannot provide exact rough-field matching

For a finite Hermitian matrix H(phi) continuous in phi, if 0 is outside its spectrum at a rounded-edge wall, the dimension of its negative-energy subspace is locally constant. The integer cochain self-linking can jump at that same wall. Therefore a smooth gapped free-slab family cannot have its filled axial charge exactly equal to minus the rotor self-linking on both sides of every such wall. This is an elementary continuity observation about this implementation, not a no-go for the full interacting interface. The scalar lattice self-linking may jump even for arbitrarily close rotor configurations; anomaly response derived for smooth textures does not establish the exact rough-configuration identity.

A repair must force appropriate spectral flow on the cochain walls, use genuinely piecewise-defined local couplings, or abandon the separated-slab Born-Oppenheimer ground-state premise and prove a joint interacting gap directly. Generic smooth mass tuning cannot make the integer jump without a slab crossing. The decoration-assisted partial transfer could avoid the **combined** crossing only after that microscopic charge-flow problem is solved.

## Independently checked mirror relocation

A uniform boundary mass was tested in the same Wilson representative, retaining all 12 normal layers, at tangential k_x=pi/24,k_y=k_z=0. The low eigenstates were summed as a subspace to avoid basis-dependent localization. Of the eight lowest-|E| states, half remain on the desired far boundary. The other half move inward:

 M    first-layer weight   second-layer weight   unwanted-branch |E|
 0       .4999634              .00003659             .1305262
 2       .07321689             .42673760             .4342563
 8       .00746382             .49249901             .1794152
64       .00012197             .49984142             .1314575

Weights are averages over all eight selected states; hence .5 means essentially the entire unwanted half-subspace. Large M sends the unwanted branch back toward the massless surface dispersion sin(k)=.1305262 while shifting its support to layer two. This directly confirms, rather than merely assumes, the Schur-complement relocation failure.

## Stronger repair inspected, not solved

A local neutral charge reservoir cannot simply be assigned energy -s_x. The invariant local cochain density is (m-dphi) cup dm, which is real-valued; only its closed-manifold sum is integer. m cup dm alone changes by local coboundaries under changing rotor representatives. Local filled-orbital counts are integers, so identifying each with that real density is not a construction. Arbitrary reference-phase choices also threaten vector covariance or joint rotor–fermion locality. Copying the decoration pairing onto charged slab Majoranas breaks axial U(1), unless an additional construction supplies the charge action. These shortcuts have not repaired the failed slab charge matching.

Files: find_move.py, matching_move.py, decor_transfer.py, wilson_endpoint.py, wilson_verify.py, corresponding NPZ data, and wilson_endpoint_results.json.
