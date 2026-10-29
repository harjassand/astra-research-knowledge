# Native logical control and causal completion of local protection

Root construction, 29 October 2026. Authored investigation; actual reviews and corrections are recorded separately. Compact GKP stabilizer-subsystem coordinates, error-transparent control, periodic logical Pauli functions and Galerkin propagation are established constituents. The new bridge here is a **single normalized causal reference with the complete returning memory**, constructed without a future-dependent polar normalization. Physical control acquisition and renewal remain separate interfaces.

## 1. Consequence and choice of attack

The completed postrecord comparison supplies a regular logical isometry even when physical postmeasurement moments diverge. Its final normalization is on the original input of a fixed programme and can reweight earlier records. It does not supply one causal ideal process under arbitrary future interventions.

Measurement-free hybrid gate teleportation and periodic Pauli controls are strong conventional alternatives, not discoveries claimed here. We ask a deeper question: can the local protected algebra be completed into a genuine causal noise dynamics while universal physical controls act only on the logical factor throughout every finite protected history?

We construct such a completion at a qualified finite-lifetime interface. Smoothly modify **comparison** differential operators near syndrome boundaries. They generate a normalized gauge-memory evolution on a torus. Every finite history from the protected compact core agrees with the physical dynamics. Two finite actual-suffix remainders then compare the physical process with this fixed causal process. No boundary is physically modified, no filtering is applied, and no bath is reset.

This supports a coherent universal computation window without per-gate syndrome deformation, magic supply or detector feedback. It does not imply that the required periodic nonlinear couplings are cheap or already acquired. The aim is a causal foundation and an explicit control target, not a threshold claim.

## 2. Qualified input and complete physical model

Set [q_j,p_l]=i delta_(jl), L=sqrt(pi), C=(-L/2,L/2)^(2n). The accepted symmetric SSS map is the unitary

    J : (C^2)^(tensor n) tensor L^2(C) -> L^2(R^n).

On a smooth function supported in the strict interior,

    q_j = I_L tensor (u_j/2+i partial_(v_j)),
    p_j = I_L tensor (v_j/2-i partial_(u_j)).                 (1)

Physical closures have twisted logical boundary conditions. They are not independent periodic derivatives on each logical component.

Fix K=[-a,a]^(2n), a<L/2, and a common initial embedding

    V_0=J(I_L tensor Q),                                    (2)

where Q is a normalized isometry from the declared original gauge-memory input, supported in K and in all finite word domains. Logical, memory and external reference inputs may be entangled. Require the uniform interface bound

    ||W_m V_0|| <= M C_0^m (m!)^2,   m>=0,  M>=1, C_0>=1.  (3)

This is a bound on a linear qualified input interface, not all finite-energy or all supported states. The accepted compact Gevrey profiles supply examples.

Replace any smaller supplied radius by max{1,C_0}; this lets the length-2k envelope bound all shorter words, including the identity. This convention was made explicit after the domain challenge.

Let the residual physical Hamiltonian be

    H_e(t)=sum_(|omega|<=2) R_omega tensor C_omega(t),
    c(t)=sum_omega ||C_omega(t)||,
    b(T)=integral_0^T c(t)dt < infinity.                     (4)

Use an explicitly adjoint-paired Hermitian word representation. Bounded strongly measurable C_omega act on the **complete** external memory and can be mutually noncommuting. Their chronological products are retained. A declared memory-only evolution may first be removed by its interaction picture. An environmental annihilator is not a bounded coefficient: an interacting unbounded mode must be explicit or separately qualified.

All live modes, coupling terms, holding and actual control durations contribute to b over the entire window. A change of round label does not renew (2) or reset exposure. Other acquisition discrepancies are separate.

## 3. Smooth universal controls on the finite core

Choose real smooth f with

    f(x+2L)=f(x),  f(x+L)=-f(x),  |f(x)|<=1,
    f(mL+x)=(-1)^m for |x|<=a_0,  a<a_0<L/2.               (5)

The physical symmetric Zak kernel gives

    J^dagger exp(ikLq_j)J = Z_j^k tensor exp(ikLu_j),
    J^dagger exp(ikLp_j)J = X_j^k tensor exp(ikLv_j),        (6)

for integral k. The momentum identity follows directly from the Fourier-transformed kernel; there is no residual logical/gauge phase in this convention. Only odd Fourier harmonics occur in f. Thus

    J^dagger f(q_j)J=Z_j tensor f(u_j),
    J^dagger f(p_j)J=X_j tensor f(v_j).                     (7)

These preserve the joint syndrome support. They anticommute globally, have norm at most one, and square to identity on the plateau band. Sharp crenellation Pauli functions have close ancestry; their physical derivative domains are not silently substituted for these smooth controls.

The physical family

    H_c(t)=sum_j[x_j(t)f(p_j)+z_j(t)f(q_j)]
            +sum_(j,l)z_(jl)(t)f(q_j)f(q_l)                (8)

has real integrable amplitudes. On the compact core it acts as

    h_L(t)=sum_j[x_j(t)X_j+z_j(t)Z_j]
            +sum_(j,l)z_(jl)(t)Z_j Z_l                    (9)

tensor identity on gauge. This set supplies arbitrary single-qubit rotations and an entangling ZZ rotation. In particular exp[-i(pi/8)Z] is T up to global phase; ZZ and local Z rotations give controlled-Z.

The conventional companion constructs a stronger entangling option when 2a<a_0: replace f(q_j)f(q_l) by the **single collective potential** f(q_j+q_l). Equation (6) gives its exact action Z_j Z_l tensor f(u_j+u_l), hence Z_j Z_l on the admitted sum band. It preserves each individual syndrome support. This needs only one harmonic family on the collective coordinate, rather than a product expansion; the narrower sum-band condition is essential. All arguments below apply to either family.

Every finite quadrature word P preserves compact smooth support. Therefore, with R_c the control-only propagator,

    R_c(t,s) P V_0=P J[U_L(t,s) tensor Q].                  (10)

The same holds for finite strings including arbitrary bounded memory coefficients. Known control does not amplify the word radius C_0 on these histories, regardless of logical gate count or noncommutation of h_L at different times. This is a common-domain local intertwiner, **not** global commutation with physical q,p. Those self-adjoint closures retain boundary transitions; irreducibility of the Weyl representation is not contradicted.

The physical propagator of H_e+H_c exists by the accepted canonical quadratic all-Fock construction and bounded time-dependent perturbation. At every fixed order, smooth periodic functions of q,p preserve the required weighted Schwartz domains. The bounded control is not being treated as a polynomial error.

## 4. Construct a normalized auxiliary process

Identify L^2(C) with L^2(T_L^(2n)) as a Hilbert space. Choose real smooth periodic a_j(u_j),d_j(v_j) equal to u_j/2,v_j/2 on an open neighborhood of [-a,a]. Multiplying the coordinate by a smooth cutoff that is one there and zero near the cell edges gives such functions.

On periodic smooth functions set

    Q_j=i partial_(v_j)+a_j(u_j),
    P_j=-i partial_(u_j)+d_j(v_j).                          (11)

Each is a self-adjoint periodic derivative plus bounded real multiplication. Their local commutator is

    [Q_j,P_j]=i[a_j'(u_j)+d_j'(v_j)].                       (12)

It equals i near K and differs at the edges. There is deliberately no global auxiliary CCR; its periodic curvature has zero integral.

Replace each word in (4) by its ordered Q,P word, keeping the same coefficients and adjoint pairing:

    H_g(t)=sum_omega R_tilde_omega tensor C_omega(t),
    H_ref(t)=h_L(t) tensor I+I_L tensor H_g(t).              (13)

The auxiliary gauge propagator W_g constructed below is unitary. For deterministic controls the reference is exactly U_L(t,s) tensor W_g(t,s). A single W_g works for every programme with the same noise process; its definition does not depend on future controls.

### 4.1 Unitary construction, without ellipticity or a classical bath

Expand H_g on the torus. The principal second-order spatial coefficients are constant bounded operators on memory. The remaining first- and zero-order coefficients are smooth bounded spatial functions times bounded memory operators. The specified adjoint pairing makes the whole expression Hermitian.

Let Pi_N project onto Fourier modes with each |k_i|<=N, leaving all memory untouched. H_(g,N)=Pi_N H_g Pi_N is bounded self-adjoint. For integral s>=0 use

    ||psi||_Hs^2=sum_(|alpha|<=s)||partial^alpha psi||^2.

The principal part commutes with every partial^alpha and Pi_N and cancels from the derivative of this norm. In a commutator with a first-order term, at least one derivative hits its coefficient, leaving at most |alpha| derivatives on psi. Boundedness of the finitely many coefficient derivatives yields

    |d/dt ||psi_N(t)||_Hs^2|
       <=K_s c(t)||psi_N(t)||_Hs^2.                        (14)

K_s is finite and independent of N and memory dimension. No memory operators are commuted or jointly diagonalized. Integrable strongly measurable time dependence gives the corresponding integral estimate.

For smooth initial data, (14) bounds every fixed Sobolev norm uniformly in N. The Fourier-tail estimate

    ||(I-Pi_N)phi||_H2 <= const N^(-r)||phi||_H(r+2)

and ||H_g(t)phi||<=K c(t)||phi||_H2 prove strong Cauchy convergence of the projected evolutions. Explicitly compare Pi_N psi_M with psi_N: the forcing is Pi_N H_g(I-Pi_N)psi_M, and the displayed tail bounds its time integral uniformly in M. Initial tails vanish as well. Apply the same argument in reverse time. Forward and reverse strong limits are inverse isometries, so W_g(t,s) is unitary; density extends it to all inputs. It obeys the composition law and is the canonical evolution of this smooth periodic expression.

This is an auxiliary dynamics, not an implemented change of physical boundary conditions. Fourier projection is a proof device, not a physical source or memory cutoff.

### 4.2 Shared finite expansion and complete bound

On the compact core, every finite product of R_tilde equals its physical local counterpart and preserves K. Equation (10) then gives common j-insertion histories for the physical and auxiliary processes:

    T_j(T)V_0=J[U_L(T,0) tensor G_j(T)](I_L tensor Q).      (15)

G_j keeps the chronological noncommuting coefficient products. It is neither a probability nor a fresh noise state.

Use finite right-sided variation of constants relative to the respective control evolutions. In each remainder the **actual normalized suffix is on the left**; all unbounded insertions act on finite reference prefixes. Word length is at most 2k. Equation (3) and the ordered-simplex integral give

    E_k(T)=M C_0^(2k) ((2k)!)^2 b(T)^k/k!,
    ||F(T)V_0-T_(<k)(T)V_0||<=E_k(T),
    ||J[U_L(T) tensor W_g(T)](I_L tensor Q)
                              -T_(<k)(T)V_0||<=E_k(T).    (16)

For the torus, the finite identity passes through the graph convergence above. For the physical process, first compress H_e and retain the bounded smooth H_c. The bounded-perturbation strong limit of the accepted all-Fock propagators gives F. At each fixed k, weighted Schwartz graph bounds and bounded derivatives of the controls justify convergence of fixed products and dominated time integration. The exact core identity is applied after that limit; no false logical identity is assigned to a Fock compression. Finite derivative constants used in this domain passage need not enter the sharper core norm (3).

Consequently

    ||F(T)V_0-J[U_L(T) tensor W_g(T)](I_L tensor Q)||
                                         <=2 E_k(T).      (17)

The reference was normalized before the comparison. No singular-value gap, polar decomposition or normalization of outcomes is required. The complete half-diamond discrepancy is bounded by 2E_k, capped at one. Matching formal series is not enough: both actual finite remainders are essential on these nonanalytic inputs.

## 5. Causal scope, interventions and reuse

Fix the qualified initial interface, physical time slots and a residual process (4) independent of the external logical tester. Admit logical/reference-only isometries at those slots whose physical lift agrees with that operation tensor identity on the supported finite core. Tester ancillas and reported histories remain explicit. They are not noisy device memory without a separate contract.

A purified adaptive tester is a chronological sequence of such isometries, with classical choices represented by controlled maps on its retained record. These operations preserve raw syndrome support and commute with gauge-memory words. The same proof is uniform over every such tester, retaining its complete output. Segmented simplexes combine to b(T)^k/k!, without an extra gate-count factor. The auxiliary process consists of those chronological logical maps and W_g(t,s), so it is a normalized causal process: future trace-preserving choices cannot change an earlier marginal record.

This establishes a **restricted logical-port strategy comparison**, not an unrestricted diamond bound on all physical oscillator inputs or access to syndrome/memory. Native (8) constructs universal coherent paths. It does not automatically acquire arbitrary instantaneous tester readout, loading or reset. Actual completed ports and their durations must be supplied to turn the broader logical-port abstraction into an operational adaptive architecture.

If coefficients depend on an actual controller record, one must specify a single causal controlled-memory law and preserve the faithful selector. Separate noise histories selected after learning the entire future programme do not define one strategy. That general controlled-memory extension is not asserted here.

W_g(T)Q can leave K and need not retain C_0. Therefore (17) is a finite **whole-lifetime** bound from the qualified input, not a per-gate bound that can be restarted at zero exposure. Renewal needs a separately constructed interface with actual supply, retained memory and readout. Earlier renewal results remain assets at their actual scopes; they are not automatically upgraded to a causal comb.

There is a further domain distinction: periodic Sobolev regularity of W_g(T)Q is not physical oscillator regularity after J. At a cell edge a generic common logical profile fails the physical twisted X/Z gluing; its physical image can have infinite momentum or number moments. This does not affect the normalized norm comparison. It prevents using auxiliary Sobolev estimates alone to certify a newly qualified physical preparation or calibration prefix.

## 6. Physical acquisition and foundational reach

The companion [finite harmonic construction](FINITE_HARMONIC_CONTROL.md) replaces the exact smooth controls by explicit finite sums of bounded cosine terms. It obtains a global bounded-Hamiltonian discrepancy without differentiating the approximation through noisy paths. This constructs a target interaction family, not the hardware that delivers it.

Amplitude errors along a native logical generator are direct logical errors and are not suppressed by k. Period errors need occupied-range or moment-weighted calibration. Simultaneous harmonic delivery and a noiseless endpoint-equivalent sequential synthesis are different noisy interfaces. Initial preparation, control pumps, whole-window duration, final capture/readout/flags and any future renewal retain their physical costs.

The general principle is **causal completion from a common local differential core**. Two normalized processes can have different self-adjoint boundary behavior but identical finite histories on a compact core. Controlled finite remainders compare them. Here the globally logical-factorized auxiliary has been explicitly constructed, supplying causality and normalization before the future programme is known. The physical nonlinear controls are also explicit. This goes beyond a final programme-dependent polar comparison while preserving its earlier valid use cases.

Exact finite algebra checks are supporting diagnostics, not continuum proofs, numerical enclosures or acquired device evidence. Historical priority for this synthesis is not established. Close primary constructions and actual review scopes are retained with the package.
