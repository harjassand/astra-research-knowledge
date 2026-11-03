# Compressed rest gap: acquired static input and remaining collective transfer

The response theorem in FAR_BAND_REALTIME_DECOUPLING.md deliberately makes no claim that the arbitrary rest sector has no extra low excitations. This note separates the next proposed bridge into earned and unearned parts.

## Static one-particle compression

Take F to include ALL far low momenta |p|<=Lambda from the audited Wilson/localizer proof, not merely the narrower probe band. F uses the explicit normalized geometric profiles and includes complete internal species. Its exact free dispersion is balanced in positive/negative signs. Let Q=1-P_F.

At fixed texture, consider Q h_near(phi) Q on Q, with the original near mass but no remote mass. Use first the exact smallest-singular-vector far branch F_exact of the finite normal SSH chain. Its removal leaves the near low localizer plus the high sector. The audited high-sector gap gH=.4Lambda and Schur error M²/(gH-M), together with profile/sampling/dispersion errors, give a gap of a fixed fraction of M; the formerly dangerous massless far block is now absent.

The direct rotation between F_exact and F_geo differs from identity by O(b_*^L), independently of tangential volume, because every Fourier block obeys the same geometric-trial singular-vector estimate. Transporting the compressed operators changes their norm by O(||h_near|| b_*^L)=O(b_*^L/a). Choosing L sufficiently large preserves, for example, a static rest gap M/4. This is a one-particle operator-norm statement, not an extensive many-body estimate. The removed far block has balanced signature, so the compensated rest axial index is unchanged. The canonical fast-copy multiplicity must be included as in the response note.

## Exact canonical parent on Q

Given this uniform static gap, the algebraic canonical purification and compensated rotor construction can be repeated on the Q one-particle space. It gives an exact gapped rest parent. This does NOT require a rest response oracle. However, Q is nonlocal in physical position: a sharp far momentum cutoff produces a nonlocal projector along the remote face.

Therefore the existing strict-range stability proof cannot simply be invoked unchanged. Its physical onsite product-vacuum localization and interaction locality assumptions must be transferred or replaced. A naive global-norm truncation bound proportional to volume times the range tail would require a volume-dependent range and would not establish the requested fixed-range interface theorem.

## Concrete possible repair, not yet a completed theorem

For a physical near patch S_X with alpha_X=||P_F P_SX||<1, the projected one-particle patch Q S_X has Gram matrix bounded below by1-alpha_X². Its orthogonal projector obeys

 projector(Q S_X) <= (1-alpha_X²)^-1 Q P_SX Q.

Thus a vacuum-annihilating even operator on the projected patch can be bounded by the excitation count on that subspace. Summing physical patch frame bounds gives a uniform multiple of N_Bell,Q, despite nonorthogonal overlapping projected patches. Rotor factors retain their original onsite tensor product.

Moreover all PF-induced changes on a fixed near patch have norm exponentially small in L minus patch depth. Finite polynomial and finite-patch Gaussian-exponential coefficient maps are Lipschitz with fixed, paid constants; their total finite-volume mismatch can be made small with L proportional to log(volume/error). This suggests separating a genuinely quasilocal near interaction from globally norm-small nonlocal projector tails before applying the coercive stability argument.

The missing proof is the complete filtered-flow/localization transfer in this projected algebra, including the required uniform interaction bounds and comparison to the actual fixed-range physical Hamiltonian. It is not supplied by the static gap or by the realtime decoupling theorem alone. The gap worker has been asked to audit/complete this specific interface. Until then, no claim that the finite device has ONLY the desired Weyl low-energy sector is made.

### Explicit static constants

For the exact far singular-vector compression, the one-face near/high inertia proof gives gap>=M/3 under Lambda=1000M,aM<=10^-6. A direct rotation identifying F_exact with F_geo has ||U-I||<=4b_*^L. Taking R_h>=||h_near||, transported compressions differ by at most8R_h b_*^L. Thus requiring8R_h b_*^L<=M/12 gives the claimed geometric-compression gap>=M/4. The elementary Wilson row norm allows R_h=10/a+M; with b_*<=5*10^-7 the requirement already holds forL>=2. All constants are independent of lateral volume.

### Simultaneous near-strip algebra embedding

One can avoid relying solely on overlapping projected-patch algebras. Let S be the ENTIRE physical one-particle strip containing every near-interface interaction support, with dimension d_strip N. Its overlap obeys ||P_F P_S||<=sqrt(d_strip N)b_*^(L-1-R). A single direct rotation maps all of S isometrically into Q, preserving all its tensor-factor/graded-commutation relations simultaneously. Its second-quantized norm distance from identity is at most O((d_strip N)^(3/2)b_*^(L-1-R)). This is globally small after a paid logarithmic increase inL. The exact same local near-strip algebra can therefore be embedded in the compressed rest, with no implicit approximate-commutation assumption.

This alone does not prove the necessary locality of filtered dynamics involving the remaining free rest modes. A capped weighted-resolvent estimate should separate ordinary near-interface locality from a globally norm-small far-projector contribution; that additional stability transfer remains the active gate.

Subsequent resolution at finite-volume scope: GLOBAL_NORM_REST_PARENT_TRANSFER.md closes the rest gap without solving the stronger projected-algebra uniform-range stability problem. It allows volume-dependent O(log²(n/epsilon)) physical range, and independently passed AUDIT_GLOBAL_NORM_REST_TRANSFER.md. The stronger fixed-range transfer described as open above is not claimed, but is no longer required for the finite-device operation. FINITE_AUXILIARY_CHIRAL_DEVICE_INTEGRATION.md then combines the actual symmetry frame and rotor cutoff with this comparison.
