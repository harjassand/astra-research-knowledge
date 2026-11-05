# Gap definitions, subclass assumptions and actual review coverage

[Collection guide](README.md) · [Complete supplied update](DOTS_MPS_GAP_20261106_RETURN.txt)

## Main proper-parent candidate

The main packet proposes convergence of the unrestricted nearest-neighbor Rai Eq.17 hierarchy to the limiting periodic gap for proper injective-MPS parent Hamiltonians. Properness requires sufficiently long open-chain ground spaces to be exactly the MPS boundary spaces. A CPTP boundary repair decodes buffers, discards outer virtual factors and joins the retained factors into a periodic excitation. The claimed comparison is `O(sqrt(log n/n))` with model-dependent constants.

Three independent internal adversarial audits cover that unrestricted nearest-neighbor theorem. The projected-Y extension was checked by the first auditor only; its literal Appendix-D indexing begins at `n>=4` and finite-level optima are not identified. General level `n=2` is excluded because it can omit a negative overlapping anticommutator; the packet includes an exact AKLT counterexample. Reduced-moment exploratory computations do not establish practical superiority, and the finite-range note is outside the second/third reviews' established scope.

## Separate GNS and weak-parent statements

The [periodic/GNS proof](components/periodic_gns_extension/mps_gns_gap_extension_20261105/PROOF.md) separately assumes proper primitive-MPS finite-range parents, a uniform open gap and unique large-ring ground state. Two internal independent reviews support the candidate; a literature/priority audit is not a third proof review. Its proposed periodic limit/GNS identification and one-sided `O(log N/N)` comparison do not give a matching two-sided rate. Novelty remains unresolved, including an inaccessible full FNW source. The construction checks are exponential physical-Hilbert-space calculations, not efficient or interval-certified improvements on strong existing AKLT variational methods.

The weak-parent packet gives a qutrit counterexample to assuming an open-gap property merely from a unique product bulk: periodic gap `1/5`, exponentially closing open gap. A fixed-block onsite-coboundary/coercivity condition yields an endpoint-reset repair and `O(n^-1/2)` unrestricted convergence for that class, including native noncritical finite-species PVBS. A different asymmetric-buffer operation retains the inner-cut boundary mode; naively resetting both buffers fails.

Its strict product representative preserves original periodic Hamiltonians and infinite dynamics, not original open Hamiltonians or finite-level SDPs. Its GNS interpretation is conditional on the separate proper-parent GNS candidate. These are not an unrestricted weak-parent theorem. Historical statements about what counterexamples had not been found remain in their original packet; the collection's separate separated-defect packet supplies the later exact Ising/toric plateau result and must also be read.

## Higher dimensions and separated defects

The restricted rectangular candidate gives `O(1/L)` convergence for positive finite-range interactions with exactly one product-vacuum kernel on a full cube. One-site translation-covariant finite-depth unitary circuits transport it to a specified entangled PEPS subclass. It does not cover generic injective PEPS, nonunitary filtering, sparse supports or arbitrary periodic circuits. Two internal audits have the stated restricted scope.

The defined dense SDP is already a `65536 x 65536` matrix at the sample `L=2` parameters, requiring 64 GiB for one complex128 copy before solver overhead. No such SDP was solved. Sparse witness checks and a loose analytic constant are not a usable numerical gap estimator or scalability benchmark. Capital does not allocate these matrices.

The separated-defect packet supplies matching primal/dual Ising witnesses and an explicit rectangular toric program. Different toric local groupings share the global Hamiltonian but their finite-window generators are not identified term by term. Two independent internal audits retain their exact normalization and support scopes. Missing cross-energy of widely separated defect pairs defeats exact-value completeness; no new method recovering that information or novelty claim is supplied. The restricted proper-parent/product-class candidates are not silently invalidated or broadened by that example.
