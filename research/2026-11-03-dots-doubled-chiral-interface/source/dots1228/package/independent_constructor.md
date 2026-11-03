# Independent constructor: explicit core mass, and where construction stops

Status: **No complete symmetry-preserving lattice interface constructed.** This note gives an explicit continuum local core filling and a decisive test of why it does not yet define the requested Hamiltonian. It must not be represented as a completed regulator or a gap theorem for the interface.

## Primary-source check

Read https://arxiv.org/html/2601.04304v1, particularly §4.1 and Appendix E, before constructing. Checked https://arxiv.org/html/2601.04304v2 (12 June 2026): §4.1 still leaves the interface conjectural; the revised text adds a caution about the vortex-disordering argument. Its symmetry disentangler is not the missing fermion/rotor gluing map. Checked https://arxiv.org/html/2505.20436 (v3, 12 January 2026) and https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.132.081903. The former's no-go result has hypotheses, including an appropriate zero-free interpolator matrix; it is not an unconditional exclusion of interacting chiral regulators. The latter analyzes gauging a propagator-zero effective description; a microscopic Hamiltonian must instead be gauged before reducing fields.

## 1. Positive local construction in a smooth continuum patch

Use four left-handed Weyls with (V,A) charges (1,1),(-1,1),(0,-1),(0,-1). Charge-conjugate the last two. They form two right-handed Weyls with V=0,A=1; the first two form a left-handed flavor doublet with V generator tau_z,A=1. Thus both left and right transform vectorially under A. A mass matrix U between these doublets transforms under V as

    U -> exp(i alpha tau_z) U.

Take U in SU(2), and the fixed-modulus mass M U. The diagonal mass U=diag(exp(i phi),exp(-i phi)) is the starting broken-V configuration. An explicitly nonsingular filling of a straight unit vortex is

    U(r,theta) = [[ f(r) exp(i theta),  g(r) exp(i chi) ],
                  [-g(r) exp(-i chi), f(r) exp(-i theta)]],
    f^2+g^2=1, f(0)=0, g(0)=1, f(r>=ell)=1.

Choose f(r)~r/ell at the core and g smooth. The diagonal elements are then regular in Cartesian coordinates and the off-diagonal elements give a nonzero core mass. chi is the local framing-dependent spurion; covariance requires chi -> chi+alpha. For a smooth vortex of a charged order parameter Delta, a nonzero framed normal derivative n·grad Delta supplies such a spurion. A bare constant chi on the whole ensemble would explicitly violate V and is not allowed. The SU(2) mass fills the vortex because pi_1(SU(2))=0; it does not discard the vortex's charge pumping.

For the continuum single-particle operator

    h = [[-sigma·p, M U(x)], [M U(x)^dagger, +sigma·p]],

squaring gives p^2+M^2 on the diagonal and off-diagonal derivative terms. For a smooth fixed U with bounded derivatives,

    h^2 >= M^2 - M sum_j ||partial_j U||_infinity.

Here the norm includes the finite flavor matrices. Hence a texture varying on ell, with sum ||partial U|| <= C/ell, has |E| >= sqrt(M^2-C M/ell) when M ell>C. The operation gaps the two counterpropagating vortex-core channels in that smooth patch while preserving A. This is a local continuum result, not a lattice bulk-boundary theorem. It also does not prove a gap for all fluctuating configurations.

## 2. The decisive remaining operation is a reconnection, not a straight vortex

The mass manifold is S^3: pi_3(SU(2))=Z. Smooth globally defined maps on compactified 3-space have integer texture number. Local changes of vortex self-linking and reconnection can change this number. A continuous fixed-modulus interpolation cannot connect different degrees. Somewhere a coordinate chart, the framing prescription, or the mass magnitude must fail. A gradient estimate restricted to smooth fixed-U configurations is therefore insufficient for the quantum rotor kinetic term.

The needed elementary operation is more specific than 'condense vortices': for every allowed local rotor move phi->phi' that changes self-linking, supply a bounded-support, symmetry-neutral fermionic transfer operator taking the complete free-slab-plus-decoration low-energy sector to the new one. A move changing the decoration's A charge by one needs a charge-minus-one transfer from the slab, and hence odd parity transfer on each side but even total parity. Total charge equality is necessary but gives neither this operator nor a nonzero uniform matrix element. Framing singularities/reconnections are precisely where low-energy levels can cross, so an adiabatic theorem presupposing a gap cannot construct the required transfer.

Even if each isolated move can be avoided-crossed using a local ancillary fermion, overlapping moves must obey consistent compositions. Products around closed loops of rotor moves may carry Berry holonomy or act on additional modes. Showing that the resulting fluctuation Hamiltonian has a unique symmetric ground state with a size-independent gap is a further calculation, not a consequence of matching charges. Pairwise reconnection success alone cannot exclude topological order.

## 3. Why large M is not a free solution

For a finite-range free slab, split its microscopic orbitals into a boundary layer b and retained interior I. Giving b an invertible onsite mass M B and coupling it by T to I yields the Schur complement

    h_eff(E)=h_I+T^dagger(E-M B)^(-1)T
            =h_I - M^(-1) T^dagger B^(-1)T + O(E ||T||^2/M^2).

When M >> ||T||, this is the original slab with the outer layer removed, up to a small local correction. Its topological boundary lies one layer inward. This is mirror relocation, not removal. A claimed all-configuration lattice bound obtained by letting the boundary mass dominate all hopping must explicitly check this surviving interior sector. The continuum bound above cannot bypass it: it applies only to the low-energy smooth patch and does not control the complete Wilson/slab spectrum.

Likewise, take an interface interaction g H_b with a unique charge-symmetric product ground state and g->infinity. If this simply freezes finitely many boundary orbitals, projecting leaves the same free interior plus corrections vanishing with g. The topological boundary survives. A viable interface must leave a nontrivial operator matching to the anomalous rotor sector at finite coupling; it cannot merely freeze that sector.

## 4. Required resource ledger still unpaid

Microscopic candidate Hilbert space would have finite fermion Fock factors per 4D slab cell, L^2(S^1) rotors and decoration Majoranas per 3D boundary cell, and eventual gauge-link rotor factors after the known symmetry disentangler. The continuum core fill only specifies a mass on smooth backgrounds; it provides no finite-range quantum reconnection Hamiltonian, no self-adjoint rotor domain for that Hamiltonian, no thermodynamic gap bound, no proved rotor truncation error, no allowed cutoff-to-continuum scaling, and no full-spectrum absence-of-mirrors proof. Thus these resource entries cannot honestly be filled with numbers.

An explicit Hamiltonian transfer term with a uniform gap for a single self-linking-changing reconnection in the **actual finite-range free slab**, including all transverse orbitals and its charge transfer to the actual decoration Majoranas, is the most sharply isolated next constructive target. It would still be an intermediate result, not fulfillment of the full interface request.
