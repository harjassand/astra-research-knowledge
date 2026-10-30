# Exact bad-block estimates with a logarithmic good set

30 October 2026. Completion to PARAMETRIC_INTERFACE_TRANSFER_CANDIDATE, not part of the earlier reviewed bundle.

Let the ACTUAL section kernel P have the already constructed unrestricted identity

    P(w f_m)(z) <= C w(z) T(z),

and uniform T(z)<=C(1+r)^(-eta) on positive-D inputs. Let B0 and B+ be dormant and positive-D bad section states with A<=K(r)=log^2(2+r), killed below r0. Put

    g0=w f_m,   g+=w(1+r)^(-eta),
    epsilon0=sup_{u>=r0} C(1+K(u))^m(1+u)^(-eta).

Then epsilon0 tends to zero. On an ACTUAL terminal state z' in B+,

    g+(z') <= epsilon0 w(z') f_m(A(z')).

This is an output-state inequality followed by a global threshold supremum. It does NOT replace output r by input r and needs no logarithmic derivative of a potential.

It immediately yields, on positive-D bad input,

    P(g0 1_B0) <= C w T <= C g+,
    P(g+ 1_B+) <= epsilon0 P(w f_m) <= C epsilon0 g+.

For dormant bad input, the actual profile-preserving full-cycle kernel gives P(w f_m)<=C g0. Consequently

    P(g+ 1_B+) <= C epsilon0 g0.

The pure dormant B0->B0 row remains non-small and must be preconditioned by its earned Green. Its seed-mediated addition is small in g0 by the actual weighted positive-D return estimate. Preconditioning multiplies these displayed finite constants by that fixed Green norm; it does not remove epsilon0. The resulting 2x2 majorant has small first and second diagonals, bounded B+->B0 entry, and O(epsilon0) reverse entry. Its spectral radius is below one after r0 is raised.

The actual correction therefore satisfies H0<=C g0 and H+<=C g+. Globally on the bad sets H<=Cw f_m, so on a good input

    PH <= C P(w f_m) <= C w T = o(wU).

This proves the base correction leakage with no extra negative residual exponent. Fixed polynomial enlargements for physical running costs use the corresponding earned polynomial-weight version of the same actual profile identity; they are a separate necessary part of the full transfer. The completion does not prove that identity or dormant Green anew, nor certify the complementary Z trials.
