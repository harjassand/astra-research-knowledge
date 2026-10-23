# Independent matched-photon challenge: 532 nm nitrite microdroplets

Source read: Wallace et al., *Solvent Fluctuations Enable Photoionization of Aqueous Nitrite Microdroplets*, arXiv:2610.17021v1, 12 October 2026, https://arxiv.org/html/2610.17021v1 . Only this new primary source was consulted. Main Eq. 1 and SI S2 are the mathematical starting point. All comparator derivations below are independent.

## Bottom line

The reported smaller-droplet fractional rate is not a demonstration of higher nitrogen-product throughput per supplied photon. In the admitted linear model, a centered narrow beam in a sphere gives fractional rate proportional to P/R², inventory proportional to R³, and initial absolute reaction rate proportional to P R. At fixed power, shrinking radius makes the fractional trace faster while making molar throughput and photon use worse.

The relevant optical resource is the total aqueous path accumulated by supplied photons, not focal intensity alone. An ordinary slab at the same concentration, chemistry, power and useful product definition is a strong comparator. In the unattenuated linear model, replace the sphere's 2R by the slab's path L. If the sample inventory is also matched, a sufficiently beam-capturing slab with L = 2R has the same rate constant, not a slower one. A much larger cuvette can have a slow fractional trace and simultaneously greater molar throughput.

This is a geometry/resource result, not an assertion that the paper's photochemistry is absent. It also does not rank complete alternative plants using their component lower bounds.

## 1. Definitions and the exact Gaussian bound

Let:

- C be nitrite concentration in mol/L (M).
- V be sample volume in cm³, so n0 = C V/1000 mol.
- b = εφ = 3.46 × 10⁻⁶ M⁻¹ cm⁻¹, the admitted effective coefficient. The reported uncertainty is ±0.19 × 10⁻⁶; this is not automatically a rigorous confidence envelope.
- ε be absorption extinction and φ the quantum yield for the specified effective event. Their product is not absorption alone and need not be a nitrate-production quantum yield.
- e = N_A h c_light/λ = 224,861.965486 J per mole of 532 nm photons.
- P be optical power supplied at the sample, before any sample clipping, not wall-plug power.
- β(C) = ln(10) b C, in cm⁻¹.

For the source's centered Gaussian geometry, define

ℓ_G = ∫[-R,R] {1 − exp[−2(R²−z²)/w(z)²]} dz.

The integrand is between zero and one. Therefore, without any large-droplet approximation,

0 ≤ ℓ_G ≤ 2R.

The source's unattenuated local-rate model gives

k = (1000 P/e) ln(10) b ℓ_G/V,

and hence

r0 = k n0 = (P/e) β(C) ℓ_G ≤ (P/e) β(C) 2R.

The right-hand side generously grants complete beam interception at every axial slice. Finite beam clipping only lowers it. In the limit used for main Eq. 1, ℓ_G ≈ 2R and V = 4πR³/3, recovering exactly

k ≈ [3P/(2πR²)] [1000 ln(10)b/e].

No beam-waist multiplier belongs in the integrated molar rate once P and ℓ_G are counted. A tighter waist changes local intensity and spatial exposure, not the integral P ℓ_G when the whole beam already fits.

This bound belongs to the source's propagation/local-rate model. Internal optical recycling, resonances, a different actinic field, or multiple encounters require a measured or defensible total effective path; they must not silently be given the 2R bound.

## 2. Do not infer weak absorption from a small εφ

A small b does not prove ε itself is small: φ could be small. Nevertheless the favorable linear resource bound survives attenuation.

For a homogeneous straight path L with no competing absorber, the effective-event yield per incident photon is

Y_event = φ [1 − exp(−ln(10) ε C L)].

Since 1 − exp(−x) ≤ x for x ≥ 0,

Y_event ≤ ln(10) (εφ) C L = β(C)L.

Thus the linear expression is an upper bound even if the true absorption depth is unknown. This step does NOT set φ = 1 or relabel b as absorption. With competing absorbers and losses, the upper bound remains favorable. For primary one-electron ionization, if additionally 0 ≤ φ ≤ 1 is established, the sharper upper bound is 1 − exp(−βL), which differs negligibly here. Do not use that one-event constraint for an unbounded chain-amplified product yield.

A stated exact droplet/cuvette rate ratio L/(2R) additionally requires the unattenuated linear regime or direct empirical validation. At appreciable attenuation, matched ε and φ still make a longer fully intercepted path no worse in primary-event yield, but the improvement saturates. Equal b alone does not identify the full attenuation curve.

## 3. Strong fair slab/cuvette comparators

For a slab that captures the supplied beam over path L,

r_slab,0 = (P/e) β(C)L

in the same linear model. For volume V_slab = A L,

k_slab = (1000 P/e) ln(10)b/A.

Three comparisons answer different questions:

1. Same C, P, b, product definition and path: equal initial molar throughput, regardless of the larger unilluminated or mixed inventory. A larger inventory merely lowers the fractional rate.
2. Same C, P, b and inventory as the sphere, with L = 2R and A = V_sphere/(2R) = 2πR²/3: the ideal fully captured slab has the same fractional rate as the sphere as well. Beam capture is asymptotically consistent with the narrow-beam assumption. This ideal matched-inventory comparator is not a claim that a real ordinary cuvette has micrometre-scale dimensions.
3. A practical longer cuvette path L: the initial ideal molar-throughput ratio is L/(2R), but its inventory, mixing, residence time, attenuation and output specification must be stated. Failure to observe fractional decay in a large sample is not a matched-photon efficiency measurement.

The equal-inventory construction above uses only L = 2R. Do not extrapolate it to an arbitrarily long path at fixed tiny inventory: a 0.59 µm-waist Gaussian has a finite Rayleigh range, and propagation over a centimetre can require a much larger sample cross-section/inventory or redesigned optics. The 1 cm³ cuvette arithmetic below explicitly changes inventory and is an optical identity/example, not an optimized or demonstrated apparatus.

Hold concentration, pH, temperature, oxygen supply, other electron/radical scavengers, composition and desired product/recovery specification fixed or explicitly account for their effects. Granting the same effective coefficient is already favorable to the droplet claim; a new microenvironment advantage must be measured rather than supplied by comparing unmatched fractional traces.

## 4. What “thinning” actually changes

Sphere, fixed P and C, R → R/f:

- Total inventory falls by f³.
- Effective aqueous path falls by f.
- Initial molar throughput falls by f.
- Fractional rate rises by f².
- Ideal supplied optical energy per mole at fixed fractional conversion rises by f.

A smaller sample presents fewer molecules to the same source power, but also wastes a larger fraction of photons because their aqueous path is shorter. Both facts must be retained.

For a slab at fixed illuminated area A and P, merely reducing thickness L decreases inventory and initial throughput in the same proportion. Its optically thin fractional rate is unchanged. At fixed inventory, making the path shorter requires greater area and therefore decreases fractional rate at fixed power. Reducing focal area at fixed captured P and L can accelerate local disappearance in a smaller locally exposed inventory; it does not increase the volume-integrated initial throughput. For an approximately collimated fixed-width beam, the geometrically illuminated column inventory scales with L. For a diverging Gaussian, do not substitute an arbitrary beam-volume estimate: the exact weighted quantity is ∫I dV = P ℓ_G.

Uniform mixing/exposure is an optimistic finite-conversion assumption. Local depletion in an unmixed focus generally worsens use of photons; under fixed spatial exposure the concavity of 1 − exp(−dose) makes uniform exposure optimal for total conversion at fixed mean dose.

## 5. Finite dose, finite inventory and per-mole optical cost

Let Q = Pt/e be moles of photons supplied, and initially C = C0. As long as C never exceeds C0, the cumulative number of specified effective events is bounded by

n_event ≤ Q β(C0) ℓ_G ≤ Q β(C0) 2R.

For net disappearance, also n_loss ≤ n0, giving the general favorable bound

n_loss ≤ min[n0, Q β(C0) 2R],

provided b is an admissible coefficient for NET disappearance, not merely primary initiation with unknown amplification. This bound counts supplied rather than absorbed photons and does not require complete conversion or constant concentration.

For the admitted constant-volume, well-mixed, first-order batch model,

X = 1 − exp[−Q β(C0)ℓ_G/n0].

At a desired fractional nitrite conversion X, the optical energy per mole disappeared is therefore

E_sample/n_loss = [e/(β(C0)ℓ_G)] × [−ln(1−X)/X]

≥ [e/(β(C0)2R)] × [−ln(1−X)/X].

The finite-conversion penalty is 1.386294 at 50% conversion and 2.558428 at 90%; its limiting value as X → 0 is one. These penalties belong to that batch law, not every possible staged-flow arrangement. The lower linear floor remains the more generally favorable screening bound.

If s = recovered nitrate-N / net nitrite-N disappeared, then E_sample/n_recovered_nitrate = (E_sample/n_loss)/s. For a closed and corrected nitrogen balance with product nitrogen proven to originate in the original nitrite inventory, 0 ≤ s ≤ 1. Initial nitrate, other initial nitrogen pools and external nitrogen contributions must be excluded or explicitly subtracted. Granting s = 1 for a LOWER resource bound is explicitly an optimistic screening assumption, not evidence that the actual nitrate quantum yield is one.

## 6. The crucial event-versus-product fork

There are two legitimate uses of b, which must not be mixed:

A. Empirical net-disappearance fit: if Eq. 1 is accepted as an upper envelope for observed nitrite disappearance at the proposed conditions, use it for n_loss. Nitrogen conservation bounds net recovered nitrate derived from the original nitrite by net nitrite loss after correcting initial product/other N pools and all other N inputs/outputs. Grant 100% nitrate selectivity and recovery to construct a favorable deployment bound.

B. Primary photoionization coefficient: if b is only ε times electron/photoionization yield, it bounds primary events, not necessarily nitrate. Define g as net recovered nitrate molecules per primary event. Then nitrate throughput is bounded by g_max Q β(C0)ℓ_G only if g_max is justified. Nitrite recycling, competing reduction, gas loss, nitrate destruction and possible chain amplification all matter. Mass balance alone does not prove g ≤ 1. An enormous event-energy bound is not by itself a rigorous nitrate-energy bound when amplification is unbounded.

The paper fits decay kinetics but also uses the resulting coefficient as an initiation rate in its kinetic mechanism. Preserve that distinction explicitly rather than assuming both identifications are exact.

Needed measurements: absolute time-resolved nitrite and nitrate amounts, calibrated product response rather than normalized band growth, total nitrogen balance including gases and oil/other phases, background and light/dark corrections, nitrate loss/reduction, stable droplet volume, sample-delivered and incident/transmitted optical powers, geometry/actual effective path, quantum-yield or actinometric calibration for the relevant event, and isolated-product recovery. Conditions and dose must match the proposed process. Measuring only exponential disappearance or a normalized nitrate-growth curve does not establish recovered nitrate quantum yield.

## 7. Independent numerical check, deliberately favorable

Use C0 = 2.5 M, b = 3.46 × 10⁻⁶ M⁻¹ cm⁻¹, λ = 532 nm and R = 30 µm = 0.003 cm. Radius is explicit; no diameter/radius inference from prose is used.

β(C0)2R = 1.1950416633 × 10⁻⁷ effective events per supplied photon.

Thus at least 8.367909 × 10⁶ supplied photons are required per effective event, and the sample-optical floor is 1.881624486 × 10¹² J/mol event. This is also a nitrate floor ONLY under fork A with the stated favorable mass-balance assumptions, or under fork B after dividing by a justified g_max.

At P = 0.1 W: n0 = 2.827433388 × 10⁻¹⁰ mol, initial ideal throughput = 5.314556691 × 10⁻¹⁴ mol/s, k = 1.879639928 × 10⁻⁴ s⁻¹, and half-life = 3,687.659 s. The floor is 522,673 kWh/mol or 37.33 million kWh/kg N using 14 g/mol N, before optical transfer or wall-plug losses and all auxiliaries.

A 1 cm, 1 cm³ ideal cuvette has 166.667 times the initial molar throughput, yet k = 3.5430 × 10⁻⁹ s⁻¹ because its inventory is much larger. Its own 532 nm event floor is still 1.128974691 × 10¹⁰ J/mol. This does not make visible-light bulk conversion attractive; it disproves the inference from fast fractional droplet kinetics to favorable photon economy.

Using b + the stated uncertainty reduces the nominal energy floor by only 5.21%. That sensitivity is not a statistical upper bound on all possible process coefficients.

Machine-readable independent arithmetic: independent_arithmetic.json in this directory.

## 8. Proper deployment rejection and system boundary

A clean no-go gate is possible for the specified one-beam/one-droplet, single-material-crossing 532 nm process: even after granting best-case coefficient, full beam capture, 100% selectivity/recovery, perfect mixing and zero auxiliary load, its sample-optical resource floor must fit an independently justified total-energy/cost limit or credible feasible alternative upper estimate. If it cannot, reject that implementation.

Do not compare two component LOWER bounds and call the smaller one a superior complete plant. For ordinary oxidation, count oxidant production/delivery, gas conditioning and transfer, pumps, pH/temperature control, separations, recovery and wastes at the same incoming-nitrite to specified-recovered-nitrate boundary. Nitrite-to-nitrate is not N₂ fixation; upstream nitrogen acquisition is common or must be included consistently.

Parallel identical traps do not improve photons per mole: at fixed total power their throughputs simply add to the same β2R bound. More power buys proportional throughput, not better resource efficiency. Sequential droplets, multipass optics or photon recycling increase cumulative aqueous path and therefore constitute a materially different architecture; use its own path and losses. Changing wavelength changes both photon energy and effective coefficient, so this 532 nm bound does not reject optimized UV photochemistry, bulk absorption, long-path reactors or recycling.

The publication reports substantial transfer-optics loss. Such losses, electrical conversion and auxiliaries can only raise the energy required relative to the sample-optical lower bound. They should be accounted for in a complete deployment comparison, but are not needed to make the favorable sample-optical screening test.
