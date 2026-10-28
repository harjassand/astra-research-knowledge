# Scalar-dependent local curvature for Task C

27 October 2026. Reviewer deduction before constructor reports. This extends the public N1090 differentiation argument to avoid assuming a known `||e||`. It is not being counted as retrieval performance, an already indexed source result, a physical acquisition or a novelty claim. I have not searched the entire corpus or literature for this formulation.

Assume the Task C physical class: `Q>=mI`, joint Loewner concavity, C2 regularity, and `||Q_i||<=L_i`, `||Q_ii||<=B_i` on the dose domain. The sensor is stable and resettable and its calibration/error contract is independently supplied. For each individual forward audit segment, both endpoints must be feasible. Reports must yield finite reciprocal intervals: if `r_k-epsilon>3/2`, set

`a_k=1/(r_k+epsilon-3/2)`, `b_k=1/(r_k-epsilon-3/2)`.

Here index `0` denotes the report at `x`, not necessarily the zero-dose action. Index `i` denotes `x+h_i e_i`.

## Derivation

The source's shape-transfer proof establishes convexity of `Z=e^T Q^-1 e`. With `p=Q^-1e`, its differentiation identity gives

`Z_ii=2p^T Q_i Q^-1 Q_i p-p^T Q_ii p`.

Loewner concavity implies `Q_ii<=0`; hence `Z_ii>=0`. The magnitude caps and spectral lower bound give

`Z_ii <= (2L_i²/m+B_i)||p||²`.

Since `Q^-2 <= (1/m)Q^-1`, we have `||p||²<=Z/m`. Therefore

`0 <= Z_ii <= (2L_i²/m²+B_i/m) Z`.

Convexity of `Z` along the forward segment bounds every intermediate value by the larger endpoint value, which in turn is at most `max(b0,bi)`. Consequently the observable constant

`M_i^local=(2L_i²/m²+B_i/m) max(b0,bi)`

satisfies `-M_i^local <= G_ii <=0` on precisely the segment required by the forward-difference proof. No global maximum of `Z` and no knowledge of microscopic dimension or `||e||` is required. Global concavity of `G` still uses the independently supplied *joint* Loewner concavity of `Q`; the readings do not certify that physical premise.

Define the raw signed gradient bounds

`ell_i=(a0-bi)/h_i-c_i`,

`nu_i=(b0-ai)/h_i-c_i+M_i^local h_i/2`.

Integrating the segment curvature gives `ell_i<=partial_i G(x)<=nu_i`, with arbitrary correlated deterministic report errors. There is no monotonicity clipping. The public simplex tangent argument then yields

`regret(x) <= max{ -sum_i x_i ell_i, max_j[(delta-x_j)nu_j-sum_(i!=j)x_i ell_i] }`.

A nonnegative maximum can be taken for numerical reporting. This is a bound on the full-simplex objective difference because `G` is globally concave; only the curvature estimate is local to the audit segments. The unknown constant `Z(0)` cancels from these differences.

All endpoint intervals and local curvature constants are price independent. For new prices `c'`, subtract `c'_i` instead of `c_i` in both gradient bounds and recompute the vertex maximum. The result can be weaker and does not assert that the old action remains good. Missing endpoint readings for a different audit location still have to be acquired.

## Worked check for the supplied fixture

For the task's diagonal `Q`,

`Z(u)=(1+u1)/(1+2u1)+(1/2)(1+u2)/(1+2u2)`.

At the three requested points the exact values are

`Z(x)=153/104`, `Z(x+h1 e1)=8059/5512`, `Z(x+h2 e2)=2021/1378`.

The exact sensor centers are `r_k=3/2+1/Z_k`. With `epsilon=10^-8`, rational interval arithmetic gives the following decimal displays:

| Quantity | Coordinate 1 | Coordinate 2 |
|---|---:|---:|
| Local curvature constant | 5.884615471187131 | 17.653846413561393 |
| Raw lower gradient bound | 0.8071074541888162 | 0.4035515628213404 |
| Upper gradient bound | 0.8365391355038405 | 0.4918294254148272 |
| True fixture gradient, for checking only | 0.8245562130177515 | 0.4122781065088758 |

The three vertex bounds are approximately `-0.0242131803402031`, `0.1425060131342645`, and `0.0723871474908926`. Thus **0.142507** is a sound upward-rounded regret bound from these three reports under the stated physical assumptions. Using the supplied fixture norm `||e||²=2` instead gives the source's valid global constants `(8,24)` and the looser upward-rounded bound **0.144410**.

The arithmetic used exact rational values and reciprocal intervals; decimals are displays. These are new synthetic calculations, not replay of the original producer's unavailable 932-report programme or an acquisition from physical hardware.

## Source and scope

The input identities are in the pinned public source `research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-response-and-physical-interfaces/source/shape/ASTRA_PRO3_MATRIX_CONCAVE_CLASS_AUDIT.md`, lines 32–75, at public revision `6360a39d9488a041f259181e38c37e638b83c609`, SHA256 `0fbfd812cecf613c61a2b77e77a6feb1eff563ef70de2c8a6136c057e0ebeb8a`. The correction retaining the raw lower endpoint is explicit at source line 75 and curator review lines 42–55. The replacement of the norm-based curvature constant by the observed segment bound is the deduction made in this review.
