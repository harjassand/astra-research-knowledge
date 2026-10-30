# A compatible theorem with all three output polarizations free

The global QC question for P0 at coefficient 3/16 remains open. This tranche proves a substantive larger safe class: **every right-isosceles resonant three-wave gradient satisfies the P0 inequality for arbitrary output vectors, amplitudes, phases and background means**. All three output polarizations are unrestricted.

The actual map is

    φ(X)=p₁ sin(X₁+θ₁)+p₂ sin(X₂+θ₂)+p₃ sin(X₁+X₂+θ₃),

with arbitrary real two-vectors p₁,p₂,p₃. Rotations and common frequency scales are included. The inequality is strict when all three vectors are nonzero. A uniform margin also proves that an open neighborhood of these triangle shapes has the same unrestricted-output property; no explicit neighborhood width is claimed.

This goes beyond the frozen theorem, which prescribes all output polarizations as U(k)=i conj(k)³. It controls actual noncharacteristic gradients with genuinely nonzero cubic correlation. For p₁=(1,1), p₂=(1,1), p₃=(2,0), exact moments give c=-6, r=-80/19 and ab-r²=33749/38>0.

The hardest step was the arbitrary-output determinant. Direct reconstruction of the compatible 6×6 moment matrix gives a degree-fourteen polynomial with 2,780 terms. I separated its safe two-wave boundary terms, then certified each of its fifteen interior output multidegrees on all eight dominant-coordinate charts. An exact rational Bernstein cover has 904 boxes; every coefficient is positive, with smallest coefficient 864. This proves a continuum statement, not a finite list of passing fields.

Writing p₁=(s₀,s₁), p₂=(s₂,s₃), p₃=(s₄+s₅,-s₄+s₅), and U=s₀²+s₁², V=s₂²+s₃², W=s₄²+s₅², the certificate yields the explicit margin

    det N ≥ (27/4) Σ UⁱVʲWᵏ,

where the sum is over i+j+k=7 and i,j,k≥1. The inherited homogeneous-QC and ROC Schur signs then complete the PSD proof. Arbitrary phases follow from the exact resonance factor cos(θ₁+θ₂-θ₃).

`PROOF.md` supplies the proof and scope. `verify_all_free.py` independently rebuilds the determinant, all chart polynomials, every rational subdivision, and the complete covering certificate. Its replay passed. `check_actual_all_free.py` also passed direct energy checks for actual maps with arbitrary phases and means; those numerical checks are QA only.

Useful replays:

    PYTHONDONTWRITEBYTECODE=1 python3 verify_all_free.py
    PYTHONDONTWRITEBYTECODE=1 python3 check_actual_all_free.py

The complete coefficient list, exact certificate, intermediate SOS constructions and genuine failed certificate attempts are retained here. No frozen trial files were changed. No network, other post-comparison construction, new agents or external sources were used.

This does not establish QC for arbitrary Fourier spectra, all triangle shapes, or the entire exceptional face. The supplied polynomial heat obstruction is respected: this proof uses whole-triangle compatibility rather than pointwise polynomial heat positivity. Homogeneous QC and the general compatible moment reduction retain their original packet credits.
