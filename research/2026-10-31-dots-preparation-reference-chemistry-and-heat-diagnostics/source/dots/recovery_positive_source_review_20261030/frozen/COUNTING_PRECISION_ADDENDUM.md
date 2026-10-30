# Counting precision for the deterministic source certificate
2026-10-30. Addendum; original source certificate remains unchanged.

For witness (c), use a selected a-element subset of erroneous boundary sites and retain exactly the repair components touching that subset. Require EVERY component of a candidate union to contain at least one selected root. This still catches every excessive repair and allows the rooted-union counting used in the tail estimate. A broader family permitting components that touch the boundary but contain no selected root is a sufficient deterministic exclusion but does not earn the stated root-only counting bound.

The global connected witness family in (a) has O(nT) potential roots. An O(n) prefactor requires restricting to boundary-incident spanning candidates; the coherent lift manuscript safely uses O(nT).

These corrections were identified by the parallel root reviewer and checked here. They do not alter the deterministic cancellation, Pauli-span lift, gentle estimate, or fixed-baseline identity. Final coherent lift SHA256 ce2ac017dc0858c26d0fa7ef6006ac5925b4e1813b5c88bee66b72a39d2ae966 includes them.
