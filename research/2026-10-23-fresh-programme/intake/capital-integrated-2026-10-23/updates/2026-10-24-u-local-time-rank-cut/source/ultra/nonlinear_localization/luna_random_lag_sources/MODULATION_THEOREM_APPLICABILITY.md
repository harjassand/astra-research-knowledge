# Closest 1D point-KG modulation theorem: applicability gate

24 October 2026. Bounded theorem check for the weak fourfold-breaking
modulation candidate in `WEAK_ANISOTROPY_RESPONSE_AND_MODULATION.md`.

## Closest primary result

Elena Kopylova, **“Soliton type asymptotics for the Klein-Gordon equation
coupled to nonlinear oscillator,”** NoDEA 32, article 75 (2025),
[DOI 10.1007/s00030-025-01078-y](https://doi.org/10.1007/s00030-025-01078-y).
This is substantially closer than the 3D small-bound-state theorem already
noted in the frozen file: it treats a one-dimensional KG field with a point
nonlinearity and proves a nonlinear modulation/scattering theorem.

The model is
`ψ_tt = ψ_xx − m²ψ + δ(x) a(|ψ(0,t)|²) ψ(0,t)`, with `m>0` and real radial
`a`. The force must derive from a radial `U(z)=u(|z|²)∈C²`, and obey the
coercive lower bound `U(z) ≥ A−B|z|²`, `A∈R`, `0≤B<m`; the stated global
well-posedness hypothesis takes `a∈C¹`. Its solitary profile is
`φω(x)=cω exp(−√(m²−ω²)|x|)`, `|ω|<m`, with
`a(cω²)=2√(m²−ω²)`.

Theorem 4.3 assumes initial data close to a solitary state in the weighted
intersection `E ∩ F_{3/2} ∩ W_{3/2+}`. Here `E=H¹⊕L²`; `F_{3/2}` uses
weighted `H^{1,1}` data and a weighted `L¹` source space that admits a delta
mass, while `W_{3/2+}` is the corresponding weighted `L²⊕H⁻¹` topology with
weight strictly above `3/2`. Smallness is measured in
`F_{3/2}∩W_{3/2+}`, not merely finite energy. The reference frequency must
satisfy the paper's spectral condition
`ω∈(−m,m)` and
`κnl := cω² a′(cω²)/a(cω²) ∈ (−∞, Kω)\{0}`, where
`Kω=(2√|ω|−√(m+ω))/(2√(m+ω)−2√|ω|)`.
Under that condition the linearized point spectrum is only the neutral
eigenvalue zero of algebraic multiplicity two, and the essential-spectrum
endpoints have no virtual levels. The theorem yields a modulated solitary
state plus a freely dispersing KG component, with global `W=L²⊕H⁻¹`
remainder `O(t⁻¹/²)`. Its modulation equations and estimates give
`|ω̇|+|γ̇|=O(t⁻³)` along the unforced asymptotic evolution.

## Applicability to the proposed drift

This proves an important baseline: in a spectrally stable, nonresonant
point-KG model, small, strongly weighted perturbations admit all-time
modulation and dispersive relaxation. It does **not** control the proposed
`ε⁻²` drift. The theorem evolves the unforced, exactly `U(1)`-invariant
equation; it has no persistent fourfold term, no `ε`-uniform constants or
remainder for a symmetry-breaking family, and no averaged radiation-loss
law of the candidate form `H′bound(Ω) Ω̇=−ε² ΓE(Ω)`. In particular, the
quartic anisotropy breaks the radial force hypothesis used here. Moreover,
the article's point-force model uses the field value as the oscillator
coordinate; it is not literally the separate inertial `q` oscillator plus
linear KG bath in the frozen construction.

Thus this is an exact methodological ancestor and a useful theorem template,
not a ready-made metastability/lifetime theorem. To use it for the claim one
still needs a perturbed nonlinear normal form controlling the anisotropy
source, the neutral projection and continuum memory with errors uniform to
times `O(ε⁻²)`, starting from the actually prepared weighted state. The
formal sideband coefficient and no-internal-mode calculation do not provide
that remainder bound. No novelty or priority conclusion is drawn.
