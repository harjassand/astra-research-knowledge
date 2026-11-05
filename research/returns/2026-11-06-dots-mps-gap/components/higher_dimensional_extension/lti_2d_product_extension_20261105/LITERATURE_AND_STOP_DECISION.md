# Prior art and stopping decision for generic PEPS

## Existing baseline, inspected early

1. Rai et al., *A Hierarchy of Spectral Gap Certificates for Frustration-Free Spin Systems*, Quantum 10,2065 (2026), arXiv:2411.03680v3. The starting H²/local-positive-decomposition method and LTI constraints are theirs. Their paper states that higher-dimensional versions are possible, while completeness remains unresolved and cannot be expected without restrictions in arbitrary dimension. The present draft defines its own centered rectangular levels explicitly.
   https://arxiv.org/html/2411.03680v3
   https://doi.org/10.22331/q-2026-04-13-2065

2. Lemm, *Finite-size criteria for spectral gaps in D-dimensional quantum spin systems*, arXiv:1902.07141. This is the closest established higher-dimensional pair-counting/finite-size framework. Its role is to turn finite subsystem information into lower gap estimates; it is not the exact-value LTI completeness assertion derived here.
   https://arxiv.org/abs/1902.07141

3. Lemm–Mozgunov, *Spectral gaps of frustration-free spin systems with boundary*, JMP 60,051901 (2019), and Lemm–Xiang, *Quantitatively improved finite-size criteria for spectral gaps*, J. Phys. A 55,295203 (2022). These improve finite-size criteria and explicitly address boundary costs. They should be compared before claiming that a surface/volume idea itself is new.
   https://arxiv.org/abs/1801.08915
   https://arxiv.org/abs/2112.07756

4. Kastoryano–Lucia–Pérez-García, *Locality at the Boundary Implies Gap in the Bulk for 2D PEPS*, CMP 366,895–926 (2019). Definition 9/Theorem 10 use relative boundary factorization to control ground-projector intersections and prove a gap. Necessity from a gap is formulated as Conjecture 30. This is not a CPTP repair of arbitrary excited or LTI-dual states preserving interior moments.
   https://arxiv.org/pdf/1709.07691

5. Kastoryano, *Spectral Gap of the Hexagonal AKLT Model via Boundary-State Factorization*, arXiv:2609.27993v1 (September 2026). Theorem 1 assumes compatible cut paths and a small remainder after removal of a common boundary response. The paper applies this framework to AKLT/Ising PEPS and controls errors with a cut-length prefactor. Its stated conditions were inspected; the long AKLT proof was not independently verified here. It does not supply a generic arbitrary-state repair channel.
   https://arxiv.org/html/2609.27993v1

6. Schwarz–Buerschaper–Eisert, *Approximating local observables on projected entangled pair states*, PRA 95,060102(R) (2017). Its preparation/observable result assumes uniformly gapped intermediate sub-PEPS parent Hamiltonians, not merely a gap for the final bulk Hamiltonian. Its boundary-condition variation is distinguished from standard LTQO. It cannot be cited as an unrestricted repair theorem.
   https://arxiv.org/pdf/1606.06301

7. Pérez-García–Verstraete–Cirac–Wolf, *PEPS as unique ground states of local Hamiltonians*, QIC 8 (2008). Critical injective PEPS show that injectivity alone does not imply a gap. Any proposed extension making that inference is false.
   https://arxiv.org/pdf/0707.2260

8. Xu et al., *The bulk spectral gap is certifiable from above but uncomputable from below*, arXiv:2606.03836v5 (October 2026). This is an important obstruction to unrestricted lower-bound claims. Its general construction is not automatically inside the strict product-parent class here, which is manifestly gapped by an elementary finite local inequality.
   https://arxiv.org/abs/2606.03836

## Concrete invalid shortcuts

- **Injectivity implies gap:** false, by critical injective PEPS.
- **LTI implies a surface-sized seam second moment:** false. For h=I-|0_K><0_K| on an R=2 square and rho=|1...1><1...1|, rho is LTI and energy-normalized. After vacuum padding, every crossing projector has value one, so <V²>=|Y|². Its dual objective grows as |D_L|, so the bounded near-optimal objective condition excludes this counterexample. That condition cannot be omitted.
- **Vacuum compression preserves arbitrary products:** false for overlapping operators sharing an exterior site. The proof uses factorization only for disjoint original supports; near pairs are bounded before compression.
- **Ordered positive operators can always be multiplied:** false without commutation. All product comparisons in the proof are on disjoint tensor factors.
- **The MPS Gram inverse has a size-independent PEPS analogue:** not supplied. In 2D the virtual boundary dimension grows exponentially with perimeter, and its smallest Gram eigenvalue can decay accordingly. A fixed-D MPS inverse-norm constant cannot simply be reused.

## Why the generic PEPS branch stops here

No completely positive boundary operation was established for generic PEPS that preserves the bulk witness moments, closes a torus, and controls the H² error with constants that remain subextensive. Ground-state clustering, approximate projector factorization, or a local-observable contraction theorem is not that operation. Relative boundary estimates may be useful ingredients, but converting them into the required all-input repair is still missing.

The finite-depth-circuit subclass avoids this gap by exact conjugacy, not by assuming the desired repair theorem. It is genuinely entangled but short-range-entangled and explicitly presented; it does not cover arbitrary injective PEPS or intrinsic topological order.

No exact previous theorem for the restricted O(1/L) LTI statement surfaced in the targeted search. That is not enough to assert priority. The present work should remain a provisional mathematical extension until expert proof and literature review, and should not be sold as a practical computational breakthrough.
