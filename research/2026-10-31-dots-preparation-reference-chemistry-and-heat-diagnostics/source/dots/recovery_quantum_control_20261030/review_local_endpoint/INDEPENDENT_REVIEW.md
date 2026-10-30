# Independent review: local herald endpoint bound
2026-10-30. Verdict: scoped PASS for exact localized operator legs and clean-channel corollary; general noisy endpoint theorem not established.

## Bound inputs
- LOCAL_HERALD_ENDPOINT_BOUND.md SHA256 35e18173cb7803c46503bfb254075641cb7f061f2133d3503ab367349bc4032d
- TWIRL_CHANNEL_ADDENDUM.md SHA256 97c469bf9ab555cab8cdfe6c2bb73a6dcefacd22219f60b37f4cc5cbf92579df
- check_local_herald.py SHA256 56cc9772955e6b002e91ea18b23538a351848a22a3cdd98fe5a9b458902c18af

## Independent algebra
For any attainable character chi on the actual X-stabilizer row space C, P_chi=|C|^{-1} sum_g chi(g) X^g. Restrict to a computational subcube free on S. Only g in C(S) survive. Each orbit block is a character outer product of length |C(S)|, scaled by p=1/|C|. Thus its norm is exactly p|C(S)|. No full-row-rank presentation assumption is needed. In particular empty S gives p, while S=all DATA gives 1: correct limiting cases.

For arbitrary joint-bath bounded E acting identically outside S, E maps |x> tensor R into the corresponding subcube tensor R. Compression then yields <x|E† P_chi E|x> <= p|C(S)| ||E||² I_R. Dephasing the adjoint effect makes these diagonal blocks the entire effect. The CP-map diamond norm is its adjoint identity norm, giving the manuscript bound including retained input correlations and external reference.

The bilinear orientation is correct, with A_x†A_x, not A_x A_x†. Explicitly define V_A=sum_x |x>_L tensor A_x and V_B similarly. The map is Tr_L[V_A rho V_B†]. The trace norm of rectangular multiplication is bounded by ||V_A|| ||V_B|| ||rho||_1, and the partial-trace channel has completely bounded trace norm one. This remains true after adjoining any reference. Since ||V_A||²=||sum A_x†A_x||, the asserted p 2^((h_S+h_T)/2) ||E|| ||F|| follows. Different attainable left/right syndrome characters do not change the effect bounds. S and T need not overlap.

The full clean map S(rho)=P_+ T_Z(rho)P_+ obeys S*(I)=pI, so C=S/p is CPTP. Composition with C contracts diamond norm of every incoming linear signed channel error. It is unnecessary to assume positivity or a Pauli mixture. This requires exactly the same clean final instrument for both terms being compared.

## Required scope qualification
The operator-leg theorem does not automatically supply a finite decomposition with bath-dimension-independent coefficient cost for every arbitrary joint-bath bounded-support superoperator. Finite system support alone does not imply a finite Kraus rank on an unrestricted retained bath. One must state a proven local-leg decomposition norm (or prove a suitable completely bounded extension/factorization estimate) before using the sentence about arbitrary superoperators as a uniform noise bound. This is a limitation of the proposed extension, not a gap in the explicit E,F lemma. It was communicated to the author before this receipt.

The missing-links list is essential: full twirl must actually precede the localized legs; spread, false acceptance, complete classical output, noisy success lower bound, and the norm of the summed family remain unproved. Per-term estimates do not justify multiplying bounds or conditioning on an arbitrary noisy event.

## Replay
The supplied script replay passed 1024 exact compression cases (maximum residual zero) and sampled two-dimensional-bath operator blocks (maximum bound ratio one). Output: source_replay.json. These finite checks do not certify a physical endpoint or generic superoperator decomposition. The analytic derivation above is the basis for the scoped verdict.
