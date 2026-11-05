# A suppression-stable all-loop contraction bound for the square-AKLT loop gas

## Result and scope

For the positive routed closed-loop representation of the undecorated square-lattice spin-2 AKLT norm, set

- L(γ): number of edges of a single routed, edge-simple closed trail;
- r(γ): number of its degree-four vertices;
- w(γ) = 3^(1−L(γ))(3/5)^r(γ);
- δ(γ,η)=0 if the loops share an edge, and (3/5)^k otherwise, where k is their number of shared vertices. Include δ(γ,γ)=0 in the proposal-ancestor kernel.

The construction below bounds, simultaneously for every placed routed root loop γ,

  (1/L(γ)) Σ_η w(η)[1−δ(γ,η)] L(η) exp[μL(η)] ≤ q,

with

  μ = log(1000001/1000000) > 0,
  q < 0.996411 < 1.

The sum is over all loop lengths and all placements on the infinite square lattice. Finite regions and arbitrary componentwise activity suppressions can only decrease it. The exact rational arithmetic bound is stored in certified_geometry_m10_L32.json.

This is a classical loop-gas contraction certificate, conditional on the stated loop representation. It is NOT a proof of the square-AKLT quantum spectral gap. It does not yet supply a uniform all-order noncommutative boundary-response expansion. The marked proposal-ancestor consequence is developed separately by the collaborating construction lane.

## 1. Local interaction charge and coverage

Follow γ's cyclic edge sequence and mark which edges also belong to η. At each routed vertex visit, charge:

- 2/5 if neither incident γ edge is shared, but η visits the vertex;
- 1/2 if exactly one incident γ edge is shared;
- zero otherwise.

If some but not all γ edges are shared, there are at least two transitions between marked and unmarked cyclic runs, so the charge is at least one. If no edges are shared, 1−(3/5)^k≤(2/5)k. Therefore

  1−δ(γ,η) ≤ total local charge + 1{E(γ)⊆E(η)}.

A degree-four vertex of η contributes zero to the local charge. For any translation- and D4-invariant nonnegative target weight, write S₂ and T₂ for its total masses at a fixed vertex with degree-two straight and turning geometry, respectively. Then the summed local charge of a straight root visit is

  a_s = S₂/5 + T₂/2,

and that of a turning root visit is

  a_t = S₂/2 + 7T₂/20.

These are exactly the coefficients in ROUTED_CONTACT_BOUND.md in the collaborating boundary-operation directory.

Let M₄ be the mass of target loops with degree four at a fixed vertex. If γ has a degree-four vertex, every covering η also has degree four there. If γ is simple and η is distinct with E(γ)⊆E(η), the nonempty edge difference η\γ is even-degree; connectedness of η forces it to attach to γ, creating a degree-four vertex of η on γ. A union bound over root visits, divided by L(γ), consequently bounds all non-self coverage by M₄. For a nonsimple root, the same bound also includes the identical-loop proposal.

A simple root's identical-loop proposal contributes w(γ)exp[μL(γ)]. Every closed edge-simple square-lattice trail has at least four turning visits. If a_s−a_t≥3x⁴, where x=exp(μ)/3 and x<1/2, this self term is absorbed by the loss from those four turns:

  (4/L)(a_s−a_t) ≥ 3x^L,  L≥4.

Here the required scalar inequality is verified exactly in the certificate. Therefore a uniform raw ancestor bound is q≤a_s+M₄, including self-exclusion.

## 2. Degree-four roots from two excursions

Let G_s(x) and G_t(x) be generating functions of degree-two rooted, edge-simple closed trails with fixed first directed edge East. Their coefficient is (3/5)^r, without the overall loop-color factor three. Straight closure means final step East; turning closure means final step North or South. Final step West reuses the initial edge and is excluded.

Let G₄ be the corresponding fixed-first-East degree-four-root generating function. Cutting a degree-four-root loop at its two root visits gives two first-return excursions. Dropping exclusions and extra contact penalties between the excursions only increases weight. There are two ways to orient the second straight excursion and the turning generating function already includes both turning orientations. Coefficientwise,

  G₄(x) ≤ (3/5)[2G_s(x)²+G_t(x)²].

The root contact supplies the factor3/5. The coefficientwise assertion, not just a pointwise inequality, permits differentiation. Rooted-orientation counting gives

  S₂=6xG_s'(x),  T₂=6xG_t'(x),  M₄=3xG₄'(x).

Thus

  M₄ ≤ (6/5)G_s S₂ + (3/5)G_t T₂.

The factors differ because a degree-two-root loop has two rooted orientations at that vertex, whereas a degree-four-root loop has four. This decomposition independently reproduces exact degree-four-root coefficients12/5 at length8 and48/5 at length10.

## 3. Finite-memory positive return majorant

The memory length is m=10. Canonical states are m-edge trails whose first step is East; there are15,023. Four world orientations give60,092 states.

A transition rejects reuse of any of the last m edges. It carries weight3/5 if the new endpoint occurs among the internal remembered vertices, and weight1 otherwise. Excluding the oldest remembered vertex from the contact test only removes a possible penalty. Every true edge-simple trail is admitted and receives weight at least its physical contact weight. Forgotten violations add nonphysical positive terms; they do not remove physical trails.

Initialization uses actual m-step prefixes, first East, with their exact within-prefix contact weight. Prefixes revisiting the original root are rejected. The terminal filter rejects a state if its endpoint appears earlier in its last m-step segment. It also selects the final world direction as East for G_s or North/South for G_t. Every true degree-two-root loop of length greater than m passes these prefix and suffix filters. Interior root returns farther than m from both ends may still survive; these only enlarge the majorant.

Displacement is tracked modulo a32×32 torus. True closures are included; nonzero-image closures add positive terms. This is an upper bound from periodic images, not a quadrature approximation to an infinite-domain integral.

For a torus Fourier mode k, T(k) is the orientation-lifted transition matrix, b(k) is the initialized prefix vector, and R(k)=[I−xT(k)]^−1. The unweighted generating function at lengths above m is bounded by

  x^m average_k [f^T R(k)b(k)],

and its length moment by

  x^m average_k [f^T((m−1)R(k)+R(k)²)b(k)].

The coefficient of a continuation of length j in the latter is m+j. Exact coefficients at lengths at most m are added separately. Reflection across the initial East axis and complex conjugation justify the quarter-grid real-part multiplicities.

The short fixed-first-East straight coefficients at lengths4,6,8,10 are0,2,10,308/5. The turning coefficients are2,4,126/5,584/5. These come from independent exact enumeration in square_aklt_loop_audit_20261105/root_geometry_counts.py.

## 4. Arithmetic certification

The exact parameter is x=1000001/3000000. Fourier phases are roots of unity. mpmath interval sine/cosine, at100-bit interval precision, enclose their real and imaginary parts; outward binary64 conversion supplies coefficient rectangles.

GMRES produces candidate vectors y≈Rb and z≈Ry. Their convergence report is not used as evidence. All residual components are bounded by rectangular interval arithmetic, applying nextafter outward after every elementary multiplication and addition. Positive sums and linear-output sums receive conservative gamma_n rounding bounds using twice the unit roundoff. Final Fourier averaging and scalar assembly use exact Python rational arithmetic.

An integer supersolution first satisfies q₀≥1+T(0)^Tq₀/3. The actual scaled binary64 vector used for the tilted parameter is converted to exact dyadic rationals and independently checked to satisfy q≥1+xT(0)^Tq. Thus it bounds the l1 resolvent amplification at every Fourier mode, because |T(k)|≤T(0).

If e₁ bounds the weighted residual of y, then ||y−Rb||₁≤e₁. If e₂ is the weighted residual of z plus max(q)e₁, then ||z−R²b||₁≤e₂. These inequalities enclose the desired linear outputs for arbitrary finite candidate vectors. The exact dyadic tilted-supersolution check is also recorded separately in tilted_supersolution_verification.json.

The arithmetic uses standard correctly rounded IEEE-754 basic operations and nextafter, and mpmath's outward interval elementary functions. It is reproducible computer-assisted interval mathematics, not a machine-checked proof in a proof assistant.

## 5. Certified numerical bounds

Rounding all displayed upper bounds upward:

- G_s <0.007804025440.
- G_t <0.041045250940.
- S₂ <0.523943909811.
- T₂ <1.690182152836.
- a_s <0.949879858380.
- a_t <0.853535708398.
- M₄ <0.046531016280.
- q <0.996410874660 <0.996411.

The margin below one exceeds0.003589. Runtime was about186seconds on the available environment. No loop-length cutoff is used in the final bound.

## 6. What remains unproved

The known spectral-gap route needs control of the instantaneous relative operator response ρdotρ^−1 and a common invertible congruence. Classical two-point mixing, perfect sampling, or a positive ratio Z(P)/Z(0) does not automatically supply this. The required all-order connected finite-difference/cumulant bounds, under arbitrary path-induced activity suppressions and with useful constants, remain separate work.

No new claim of universal MBQC, efficient thermal preparation, experimental noise tolerance, or hardware access follows from this certificate. The earlier local boundary metric lemma remains an independent ingredient.

## Primary sources

The exact square-AKLT loop representation and contact factors are background, not claimed as new: Martyn, Kato and Lucia, https://arxiv.org/abs/1912.10327; Jackson, Nachtergaele and Young, https://arxiv.org/abs/2605.12184.

The target quantum-response framework is Kastoryano, https://arxiv.org/abs/2609.27993. Its honeycomb proof does not automatically extend to this square-loop certificate.

The loss-network/ancestor method is Fernandez, Ferrari and Garcia, https://arxiv.org/abs/math/9806131 and https://arxiv.org/abs/math/9911162. The soft Bernoulli-mark refinement and exact loop proposal are stated separately; these references alone do not provide the missing quantum all-order bound.
