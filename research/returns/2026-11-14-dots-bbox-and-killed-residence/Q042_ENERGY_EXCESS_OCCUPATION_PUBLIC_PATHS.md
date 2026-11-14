# Direct static bound for sparse/rough macroscopic and winding states

The all-topology loop-gas injection of HIGH_PERIMETER_OCCUPATION.md also yields a sharper state-dependent localization. Define
S_bad={x: (24/5)P(x)−Nplus(x)/25≥2600}.
Equivalently, Nplus≤120P−65000.

On this set, E(x)=8P−Nplus/25≥(16/5)P+2600. Therefore
Σ_{x∈S_bad} [w(x)/w(a)]h_a(x)
≤e^-2600 Σ_x exp[−(16/5)P(x)]
≤2 exp[−2600+n/1080]
<10^-97.

The last comparison is an exact rational certificate in energy_excess_occupation.py/json, using e>8/3. It uses only h_a≤1 and counts every torus topology, including arbitrary companions. Flow independently reviewed the underlying loop encoding and found no objection; the full boundary determines the spins up to a global flip, which is paid.

This includes sparse winding structures that the planar-area core excludes. For example, a full-height strip of widthw has P=3200 and Nplus=1600w. Everyw≤199 satisfies the displayed condition. A thin plus cross wrapping in both directions also satisfies it, without any need to assert its boundary contains noncontractible loops.

## Remaining occupation
After this bound and the planar-area core bound, the unresolved sector must simultaneously:
- fail the explicit small planar-component core condition; and
- satisfy Nplus>120P−65000.

The previous P≥11200 estimate can still be retained separately to remove the narrow residual high-P band. The remaining dense, comparatively low-perimeter macroscopic/nonplanar states include genuinely growing droplets and thick strips. Their equilibrium potential cannot be replaced by1, and no direct upper bound on their total occupation has yet been obtained. No duration or full first-passage claim follows from these localizations alone.
