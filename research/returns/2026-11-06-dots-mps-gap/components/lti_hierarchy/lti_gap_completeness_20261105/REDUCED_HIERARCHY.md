# Energy-moment-only hierarchy: precise reduced formulation

Status: provisional corollary of the reviewed moment-based proof. The three audits address the core unrestricted nearest-neighbor theorem; the first also checks the projected energy-moment reasoning. This document is not a separately three-times-audited numerical algorithm or novelty claim. Close quadratic scalar-SDP prior art is documented separately. No claim that the following ansatz is entirely new is made.

Require n>=3 throughout: n=2 omits an overlapping anticommutator and is not a certified hierarchy level. Let h_i be the nearest-neighbor interactions on an n-site open window, and let

    g_n(delta)=h_1^2+sum_(j=2)^(n-1){h_1,h_j}-delta h_1.

On n-1 sites define the real Hermitian span

    V_(n-1)=span_R{ h_i, h_i^2, {h_i,h_j} : 1<=i<j<=n-2 }.

Define the reduced primal by

    maximize delta
    subject to g_n(delta)+I tensor Y-Y tensor I >=0,
               Y in V_(n-1).

Equivalently its dual minimizes Tr rho g_n(0), with rho>=0, Tr rho h_1=1, and

    Tr rho (I tensor O-O tensor I)=0 for every O in V_(n-1).

These constraints impose exactly all one-step translation equalities for the first and second local-energy moments. Iteration gives every translated moment fitting the n-site window. They do not enforce equality of complete reduced density matrices.

## Convergence argument

Every step of PROOF_CANDIDATE.md uses only these energy moments, positivity, and normalization of the dual rho. In particular the open-energy identities, exact ground-mass removal, trace bound, contiguous-core second-moment estimate, and boundary-energy estimates do not need full LTI. Therefore the same repaired-state comparison gives

    gamma_reduced,n >= Delta_n-O(sqrt(log n/n))

under the identical proper injective-MPS parent assumptions. Telescoping still gives gamma_reduced,n<=Delta_N for every N>=2n, with n>=3. The identity gives a strict dual feasible point and the delta=-M energy-polynomial witness gives primal feasibility. This establishes the same provisional completeness conclusion for the reduced hierarchy.

Every energy polynomial in V_(n-1) annihilates the open ground space on both sides. Thus this ansatz lies inside the projected-Y family, and, with a common indexing convention,

    gamma_reduced,n <= gamma_projected,n <= gamma_unrestricted,n.

This inclusion is another route to the projected-family convergence statement. Appendix D's literal printed endpoint differs by one level; see PROJECTED_VARIANT_EXTENSION.md rather than asserting a same-level identity across inconsistent conventions.

## Size and limitations

Writing L=n-2, the span has at most 2L+L(L-1)/2=(n-2)(n+1)/2 real scalar coefficients. For h_i^2=h_i, this drops to L(L+1)/2=(n-2)(n-1)/2. Add one variable for delta. Linear dependencies can reduce the count further.

The constraint is still positivity of a d^n by d^n physical matrix. This is not a low-degree formal Gram-SOS relaxation and not a polynomial-time algorithm in n. Symmetries, sparse eigenvalue oracles, known-ground-space removal, and coefficient conditioning affect practical cost. The first benchmark does not establish a competitive resource advantage over strongest prior solvers.
