# Exact spatial minimax for a global coefficient ellipsoid

16 October 2026. This append-only refinement preserves v0001 and v0002. The
separate proposal-budget auditor identified the closed form below after checking
v0002. Its general convex feasibility characterization remains correct, but its
restriction of the closed form to disjoint incidence sets was unnecessary.

Assume exactly the modewise supported Pauli unitary proposal family of v0002,
one acquired global ellipsoid sum_i(h_i/b_i)^2 <= 1, and a common scalar cap on
each receiving cell's touching rate. Let S_c be arbitrary overlapping incidence
sets. Put B_c = sqrt(sum_(i in S_c) b_i^2) and B_* = max_c B_c > 0. Then

    inf_(gamma_i > 0) max_c sup_h sum_(i in S_c)
           [gamma_i + h_i^2/gamma_i] = 2 B_*.

One simultaneous optimal floor is gamma_i = b_i^2/B_* for every charged mode.
Modes charged nowhere are omitted. If no charged mode remains, the optimum is
zero. Zero ellipsoid axes can be omitted rather than assigned an undefined rate.

Proof. At a fixed cell the exact worst rate is

    F_c(gamma) = sum_(i in S_c) gamma_i
                         + max_(i in S_c) b_i^2/gamma_i.

For z_c = max_(i in S_c) b_i^2/gamma_i, its first term is at least B_c^2/z_c.
Hence F_c >= B_c^2/z_c + z_c >= 2 B_c; maximizing gives the lower bound 2 B_*.
For the proposed common floors, every nonempty cell has
F_c = B_c^2/B_* + B_* <= 2 B_*. A maximizing cell attains equality. No
disjointness, equal supports or common number of modes was used. QED.

For coefficient boxes the distinct result remains 2 max_c sum_(i in S_c)
epsilon_i, attained by gamma_i = epsilon_i. A box cannot be replaced by an
ellipsoid with the same marginal axes without acquiring its joint promise.

This establishes the exact receiving rate within a specified mathematical
representation and floor family. It is not optimization over all correlated
proposal decompositions, all physical noise interventions, or energy. Unequal
cell caps, fractional incidence charges and independent-block ellipsoids are
different contracts; the common-cap closed form cannot be asserted for them.
The exact 4D sweep lifetime still depends on its universal schedule certificate,
probability imports, completed correction dynamics and acquired local rates.
Historical originality, independent external review, physical acquisition,
useful threshold constants and technological superiority remain UNKNOWN.
