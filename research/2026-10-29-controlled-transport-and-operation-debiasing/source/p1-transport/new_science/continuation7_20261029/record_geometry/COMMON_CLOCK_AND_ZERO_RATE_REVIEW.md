# Focused review: common clock and the zero-rate endpoint

**Reviewer:** existing Astra P1 `record_geometry` role. **Date:** 2026-10-29. This is an independent mathematical review, not a numerical or formal verification claim.

## Actual inputs

| File/version | SHA-256 |
|---|---|
| `COMMON_CLOCK_FAILS_ON_THE_CONSERVING_RING.md`, initial Sections 1–6 read | `34c56ffb5dfe4fddb239d3828ea0bd45d9902a56ee5679f70acd889b842d7621` |
| Same file, full version including Section 7 | `4609f636ea4b0291d929efe19000e84556cbdc4218bb8b2ff34d85e026d02572` |
| `INDEPENDENT_CONTROL_OPENS_ZERO_RATE_GATES.md` | `42b0e66f96e12059613cd6fccda9e05f03e2d3e21f836c109a5b43fcea383db3` |

All three byte-exact inputs are snapshotted in this directory with `_REVIEWED_<first12sha>.md` suffixes. The later common-clock version was compared against the first; it appends Section 7 without changing Sections 1–6.

## Verdict

**Accepted at the stated interfaces.** The fixed-amplitude common-clock upper bound genuinely rules out the independent-control reference circulation LDP. The amplitude-one limit suppresses every fixed nonzero circulation event superexponentially at speed `N`. The independent phase/sign form comparison extends the positive full action theorem to the exact zero-rate endpoint. Together these give the claimed matched-ring distinction based on the joint correlations of the physical controls. No load-bearing correction was found.

## 1. Reversibility and admitted amplitude family

For an active bond, the parity coordinate changes sign under exchange; the wraparound bond does so because `N` is even. The local occupation difference changes sign as well. Thus `p delta_i` is invariant under its own exchange. Uniform occupancy in each particle sector times a fair common sign is reversible.

The permitted amplitude is nonlocal, but it does not violate own-swap reciprocity. On an active bond it can even be written as a sign determined by the occupations outside the pair, times a fixed bond sign: the orientation dependence cancels. Null attempts must be excluded from exchange counts, as the actual text expressly does.

The equal number of `10` and `01` active bonds gives total intensity `c A` and signed drift `c alpha u A`. Hence the native increment `d_i=delta_i-alpha u` has zero conditional summed drift. Direct expansion gives

\[
\sum_{i\,\mathrm{active}}r_i d_i^2=c(1-\alpha^2)A.
\]

The sum of the native increments is therefore itself a martingale with the stated bracket. No compensator has been omitted.

## 2. Current identity and rare-event scaling

Since both kinds of events flip `u`,

\[
\sum_{\rm native}u_-=
\tfrac12(u_0-u_t)-\sum_{\rm common\ clock}u_-.
\]

Substituting this into the total current proves the root's path identity with exactly its signs. The common-clock compensated sum needs only predictability and its fresh conditional Poisson intensity; the evolving `u` need not be independent of its past.

The clock-martingale log moment at multiplier `b/N` is `O_b(gamma_N)`. The one-sign Feynman–Kac calculation has the same order, with constant `alpha^2 b^2 gamma_N T/2`. An arbitrary initial occupancy/sign law costs at most `2^(N+1)` relative to the reference. Dividing by `N`, letting `gamma_N/N ->0`, and then sending the fixed Chernoff parameter to infinity removes that cost. Both corrections are consequently superexponentially small at speed `N`; the endpoint sign term is deterministically `O(N^-2)`.

For fixed `alpha<1`, native ellipticity supplies the previously reviewed activity upper estimate. The cubic martingale remainder is `O_b(1)` before division by `N`: total physical integrated rate is `O(N^3)` and each cubic term is `O_b(N^-3)`. This verifies the local upper exponent

\[
\frac{q^2}{2s\chi(m)(1-\alpha^2)T}.
\]

At nonzero `q` it strictly exceeds the independent-control action. The lower bound that a reference LDP would assign to sufficiently small open neighborhoods contradicts this upper bound. A matching common-clock lower bound is unnecessary. The argument requires only conserved mass convergence, so the same deterministic flat initial profiles and recorded initial `+1` sign are allowed.

## 3. Stationary CLT is correctly separate

The canonical moments of activity have the stated normalization. Stationarity bounds the variance of its integrated spatial average by `T^2` times its one-time variance, so temporal mixing is unnecessary. The native martingale's scaled bracket converges and its scaled jumps vanish.

The clock correction has squared norm `gamma_N T/N` at the `N^(3/2)` scale. Substituting `b=t/sqrt(N)` into the exact sign Feynman–Kac bound gives the occupation correction a centered variance proxy `alpha^2 gamma_N T/N`. Both vanish. Thus the separate stationary Gaussian limit has variance `s chi(m)(1-alpha^2)T`. The actual text does not mistake this CLT for an LDP proof.

## 4. Endpoint pinning needs no native ellipticity

At `alpha=1`, every allowed native exchange has `delta_i=u_pre`; its corrected increment is exactly zero. For `alpha_N ->1`, the upper bound `A<=N` makes the native martingale log moment divided by speed `N` tend to zero for each fixed multiplier, without an occupation estimate. The common-clock corrections retain their uniform `O(gamma_N)` bounds, because nonnegative reversible native rates suffice for the sign Feynman–Kac estimate even when some vanish.

The same Chernoff argument therefore gives the root's superexponential suppression of `|Q_N|>epsilon`. It permits arbitrary initial occupancies and recorded initial sign. No equilibrium initialization or hidden limiting spectral gap is introduced at the endpoint.

## 5. Independent control reopens the receiving form

The supplied circle inequality `D_ex <=(4/s)D_native+8D_theta` was independently proved in this directory. The root's sign calculation is also correct. For `h=f^i-f`, sign symmetry gives `I<=W+sqrt(IJ)`, hence `I<=2W+J`. The commuting native swap and its own sign flip give `J<=4 int|f^(flip_i)-f|^2`. Summing with the specified half-form conventions yields

\[
D_{\rm ex}\le(4/s)D_{\rm native}+4D_{\rm sign}.
\]

Thus `gamma_N>=s` supplies `(s/4)D_ex` from the joint form. The phase-independent occupation potential can still be treated one phase fiber at a time after this inequality. Phase replacement, bounded jump estimates, initial density ceilings, and the macroscopic energy/smoothing proof do not require positive instantaneous native rates.

Weak comparison likelihoods also remain valid: tilting multiplies an existing rate and preserves its zero set. Their formulas require no division by that rate. Consequently both independent suppliers support the full positive action theorem at amplitude one. The reciprocal additive-error theorem is correctly left at its separate uniformly positive interface.

## 6. Comparison scope

Each individual bond sign has the same marginal Poisson flip rate in the shared and independent implementations, including recorded all-positive starts. Their joint control processes and total actuation resources differ. The result is a distinction between physical suppliers, not an algorithmic advantage at identical resources.

The common-clock proof establishes failure of this shared Poisson program in the stated scaling. It does not prove failure of every common control, a universal necessary threshold, or a full shared-clock spatial action. Historical priority, apparatus realization, and practical costs remain separate questions.

