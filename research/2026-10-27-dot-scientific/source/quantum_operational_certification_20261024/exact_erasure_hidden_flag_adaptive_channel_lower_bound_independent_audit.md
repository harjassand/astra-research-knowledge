# Independent receipt: adaptive physical-query lower bound at exact erasure

PASS, 2026-10-27. Independently checked the complete statement and proof in `exact_erasure_hidden_flag_adaptive_channel_lower_bound_root.md`. The governing quantitative result is n >= D^2[1-(1+(1-zeta)^2)^(-1/2)]/8, and n >= D^2/40 for zeta<=1/4, where p=1/D and output dimension is 3D.

## Source and access receiving

The source E_(U,psi)(rho)=[U rho U* tensor Ppsi + Tr(rho) I3/3 tensor (I-Ppsi)]/D has a genuine isometry term of weight p=1/D and a normalized replacement term of weight q=(D-1)/D. Their receiver supports are orthogonal. It is exactly in the zero-deficit family. No pure flag or code-support oracle is given beyond the one independent code datum used to test the promised inverse. The source stays fixed during all training; Haar averaging is over possible fixed sources, not an IID redraw of the source on each call.

The full normalized Choi state is I/(9D)+(Phi_U-I9/9) tensor Ppsi/D. Its positive eigenvalues and zero code-complement eigenvalues follow either directly from the physical channel or the rank-one-plus-white block form. Tr B=0, Tr B^2=8/9, and the Choi overlap is (1+8t/D)/(9D).

## Common teleportation simulator

Root's Bell vectors (I tensor conjugate(W))|Phi3> yield input W x/3 by direct index contraction. Because both chosen U=I and U=X3 are qutrit Weyls, they commute up to phase with each known Weyl W. The replacement logical state is invariant. Consequently the correction W* tensor I_flag simulates EACH source with exactly the SAME fixed processor. This is a stronger fact than separate source-by-source teleportation covariance; the correction does not depend on unknown U or psi. It extends to entangled inputs by linearity.

Replacing every use in a finite definite-causal-order adaptive query strategy by this simulator gives a source-independent CPTP map of J^tensor n and the datum, retaining all adaptive records and memory inside the map. No parallel-training assumption is needed. A maximum-call budget can be padded. Indefinite-order processes and postselected normalized branches are not silently included.

## Haar and norm receiving

The data's physical logical state |0> is identical for both hypotheses; ideal inverse states U*|0> are orthogonal. The data flag is a separate product Ppsi at each fixed source. The averaged program-plus-flag state's chi-square against the scalar maximally mixed baseline is exactly E[D t(1+8t/D)^n]-1. Haar moments give the geometric bound with x=8n/D^2. The scalar-baseline Hilbert-Schmidt estimate gives half trace distance <=sqrt(chi-square) between the two ensembles by a triangle inequality. Complete unhalved diamond error zeta gives ideal-output half-distance at least1-zeta, not1-2zeta. Constants and the trivial n>=D^2/8 branch are correct.

The accompanying checker `exact_erasure_hidden_flag_lower_bound_check.py` independently verifies actual T/J source overlaps, all nine known Weyl corrections for both logical hypotheses in dimensions D=2,3,5, and the finite Haar-moment bound. It passed. These numerical tests corroborate the analytic proof; they do not replace it.

## Scope

This receives a worst-case Omega(p^-2) lower bound for approximate deterministic CODE inversion at fixed accuracy, even under arbitrary entangled/adaptive physical channel queries of bounded total number, and even at EXACT entropy deficit zero. Receiver dimension grows as3/p. It does not imply the same lower bound at fixed receiver dimension, for a known code/flag, for a weaker channel-composed recovery guarantee, or for an error-conditioned accepted-only map. No inverse-accuracy exponent is established. The result is compatible with the separate fixed-p pairwise information theorem because the lower bound uses a many-source Haar prior.
