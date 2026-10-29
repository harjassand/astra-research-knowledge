# Physical Schur front-end: corrected dependency

Date: 2026-10-28. This addendum does not change the frozen orbit-access receipt.

## Primary-source check

Burchardt, Fei, Grinko, Larocca, Ozols, Timmerman and Visnevskyi, *High-dimensional quantum Schur transforms*, arXiv:2509.22640v1 (26 September 2025): https://arxiv.org/html/2509.22640v1 . Version and argument checked on the above date.

Sections 1.3–1.4 identify and repair a missing multiplicity-basis conversion in Krovi's earlier algorithm. The corrected circuit uses alphabet/coset preparation, symmetric-group Fourier transformation, and an inverse compression isometry implementing the required basis conversion. Section 6.1 charges preparation at soft-O(k^3); section 7.1 charges the conversion at soft-O(k^3). The stated total is soft-O(k^4), dominated by the group Fourier transform, with soft-O(k^2) space. Here polylogarithmic local-dimension dependence and polynomial logarithmic accuracy dependence are suppressed. Section 8 separately develops a compressed BCH route with soft-O(min(k^5,k d^4)) gates. Consequently the high-dimensional physical front end need not have polynomial d dependence. This is reliance on that primary construction, not an independent reproof or hardware execution.

## Consequence for this Astra construction

The audited new orbit compiler concerns supplied Specht/tableau registers. Its k^{O(j)} bound does not itself implement physical Schur transforms on k local d-dimensional inputs. Add the corrected front-end cost separately for each participating local system and each actual invocation. When d=2^q, retain the input's kq qubits and all arithmetic/gate-synthesis overhead; do not read soft-O(k^2) as a qubit bound independent of q. Allocate each invoked approximate unitary an error budget and telescope errors over the actual circuit.

The approximate-design encoder on a Specht space is yet another operation: its code dimension, moment approximation, actual code circuit C and inverse, and controlled block/reflection costs remain separate. Neither the revised Schur dependency nor the orbit frame proves source yield, moment concentration, or hardware advantage. A bibliography citing only the uncorrected Krovi algorithm is insufficient for the asserted high-dimensional full basis transformation.
