# Binary controls: exact support identifiability and finite-resolution limits

## Result

In the ideal count-channel model, calibrated binary controls with two distinct label probabilities identify the law of a random *simple* finite age set from exact whole-product count histograms. The proof is elementary: invert each control's binomial-mixture channel, recover the probability that a chosen set contains no entries, use inclusion-exclusion to recover occupied-cell laws on every finite partition, and refine the partition. Simplicity makes the support set equal to the unordered multiset.

This is an infinite-observation identifiability result. It does not imply that a finite experiment identifies an unrestricted law, that entries are physically simple, or that fine temporal recovery is economical. Exact multiplicity laws remain non-identifiable in general. Finite time resolution has a simple-history counterexample, and every finite menu of per-age response profiles has a distinct-simple-law affine-dependence witness.

## Model and exact theorem

Let `I` be a compact metric age domain. The ordinary nonnegative age axis can be compactified and mapped to `[0,1]`, for example by `a -> a/(1+a)`. Let `A={A_1,...,A_n}` be a random unordered multiset of fixed known size `n`. Conditional on `A`, one independently isotope-labeled atom is produced per entry. For a Borel set `B` and its binary control, the stable-heavy-label probability for an entry of age `a` is

`p_B(a) = p_H` when `a in B`, and `p_L` otherwise,

where calibrated `p_H,p_L in [0,1]` are known and `p_H != p_L`. The observed outcome is the exact parent-product heavy-count histogram `K_B in {0,...,n}`. Every Borel `B` is assumed addressable, the full possible age prehistory is in the controlled domain, and the count channel is known. Conditional independence and isotope-neutral ancestry are part of the model.

**Theorem.** If `A` is almost surely simple (its `n` ages are pairwise distinct), then the collection of laws `{Law(K_B): B Borel in I}` uniquely determines the law of `A` as an unordered multiset.

### Step 1: deconvolve the count channel

Put `J_B = #{i: A_i in B}` and `ell(z)=1-p_L+p_L z`, `h(z)=1-p_H+p_H z`. The probability generating polynomial of `K_B` is

`G_B(z) = sum_{j=0}^n P(J_B=j) ell(z)^(n-j) h(z)^j`.

The observed full histogram gives every coefficient of `G_B`. The `n+1` polynomials `ell^(n-j) h^j` are linearly independent. Indeed, `ell` and `h` are linearly independent affine polynomials because the determinant of their constant/linear coefficient vectors is `p_H-p_L != 0`. Since `ell` has at most one root, on an open interval avoiding that root a relation among these polynomials becomes a polynomial relation in the nonconstant ratio `h/ell`; all coefficients must vanish. Thus the mixture weights `P(J_B=j)` are uniquely recovered, in particular

`V(B) = P(J_B=0) = P(A has no age in B)`.

Imperfect purity is allowed. Equality of the two calibrated probabilities (`p_H=p_L`) destroys this step completely. If `p_L,p_H` are not initially known, ideal all-low and all-high controls identify them from `E[K]/n`, provided `n` and the detector response are known; finite calibration uncertainty adds to the inversion cost. With a known detector matrix `R` from count bins to observed channels, the exact condition becomes full column rank of `R A`, where `A` is the binomial-mixture matrix above. An unknown or rank-deficient channel gives no general recovery guarantee.

### Step 2: recover a finite partition's occupied-cell law

Take any finite Borel partition `C_1,...,C_q` of `I`, and set

`O = {i: A intersects C_i}`.

For each `U subseteq {1,...,q}`, the event `O subseteq U` is exactly the void event for the complement union:

`F(U) = P(O subseteq U) = V(union_{i not in U} C_i)`.

All these values are available from the binary controls. Inclusion-exclusion (Möbius inversion on the finite subset lattice) gives each occupied-cell probability:

`P(O=T) = sum_{U subseteq T} (-1)^(|T|-|U|) F(U)`.

So the law of the occupied-cell set is determined for every finite partition. For a partition with `q` cells this constructive void-only route uses `2^q` set controls; this is an acquisition upper bound for the finite-bin support law, not a lower bound on arbitrary full-histogram protocols. If feasible occupied patterns are restricted to a known family `Omega`, an unrestricted law on that family has `|Omega|-1` free parameters, so void-only recovery needs at least that many independent nonconstant scalar queries. For example, if a separation assumption guarantees exactly `n` occupied cells among `q`, then `|Omega|=C(q,n)`. This dimension count applies only to the void-query route.

### Step 3: refine without invoking a random-set theorem

Choose nested finite interval partitions `P_m` of `[0,1]` with maximum cell diameter `h_m -> 0`; assign boundary points to one cell by a fixed half-open convention. Let `S` be the support set of `A`, and let `S_m` be the union of the closures of cells occupied by `S`.

The distribution of `S_m` is known by Step 2. Deterministically, `d_H(S_m,S) <= h_m` in Hausdorff distance: every support point lies in an occupied cell, and every point in the closure of an occupied cell is within its diameter of an actual support point. The space of nonempty compact subsets of compact `I`, with Hausdorff distance, is compact. For every bounded continuous function `f` on that space, continuity and dominated convergence therefore give

`E[f(S)] = lim_m E[f(S_m)]`.

Every expectation on the right is determined by the occupied-cell law. Hence the law of `S` is determined. When `A` is almost surely simple, `S=A` as an unordered multiset, proving the theorem.

This argument uses only finite inclusion-exclusion and a deterministic mesh limit. With nonsimple ages it still identifies the support-set law, but the support forgets multiplicity.

## What the theorem identifies, and the gauges it leaves

The ideal theorem identifies the probability law of the unordered set of entry ages; it does not label atoms, recover a causal ordering among equal ages, or distinguish any physical histories that induce the same age multiset.

If command-to-input timing has an unknown common delay `tau`, a commanded high set `B` acts on actual ages as a translate of `B`. The data identify the law in command-clock coordinates (equivalently, the translated age law), while `(A,tau)` and `(A+c,tau+c)` give the same response. Absolute entry time needs an aligned clock or a justified anchor. Calibration of `p_L,p_H` does not calibrate this time origin.

The proof also requires control of the full prehistory. If all ages older than a controlled window receive the same low probability under every waveform, their locations cannot be recovered; at most their count contribution can be learned. If the label changes reaction kinetics, if one feed entry does not correspond to exactly one independently labeled parent atom, or if the isotope effect is not represented by the calibrated probabilities, the model theorem does not apply.

The interface must preserve the full `n+1`-bin count histogram, or a known full-column-rank detector transform of it. A mean, a selected charge channel, or an unvalidated summary can discard the void probability or make the mixture matrix rank-deficient. A calibrated detector response `R` should be included in the channel map and checked for rank and conditioning. Charge-state-dependent efficiency or isotope-dependent fragmentation requires a richer calibrated response model.

## Exact multiplicity witness remains valid

Put six entries at three fixed distinct ages, allowing coincident entries at each age. Consider two laws, each uniform over three multiplicity vectors:

* law E: `(0,1,5), (1,5,0), (5,0,1)`;
* law O: `(0,5,1), (1,0,5), (5,1,0)`.

For each of the three sites, the marginal multiplicity is uniform on `{0,1,5}` under either law. For a subset `B` of the three sites, the number `J_B` is either 0 or 6, a single site's multiplicity, or 6 minus a single site's multiplicity. Its law is therefore identical under E and O for every possible `B`. The full count histogram after any fixed `p_L != p_H` is a channel applied to that same `J_B` law, so all binary whole-product histograms agree. The support law is the same; the multiplicity law differs. This is precisely what the simple-set hypothesis removes.

## Finite-bin consequence and simple-age collision witness

For a fixed partition, binary controls over all unions recover exactly the random set of occupied cells. If the scientific model supplies a known minimum separation `s>0` and the maximum cell diameter is below `s`, every cell contains at most one entry. The recovered occupied-cell set then gives the full joint law of the `n` age bins, not just cell marginals. In a no-separation model, it gives a finite-resolution support law only.

There is an exact six-entry, three-cell witness even when all actual ages are distinct. Use the two occupancy laws E and O above, but in each cell choose the required number (at most five) of distinct interior ages. Every binary control that is constant on the three cells sees the same `J_B` distribution under E and O, and hence the same full count histogram, at any purity contrast. The within-cell age configurations can differ. This is a finite-resolution obstruction; controls that split a cell can separate the chosen configurations.

For a simple random age set define `D_min` as its minimum pairwise distance in the compactified age metric. On a mesh of diameter `h`, the collision probability is `rho(h)=P(D_min <= h)`. Simplicity implies `D_min>0` almost surely, so `rho(h)->0` by continuity of probability. For every fixed law this makes the finite-bin multiset approximation converge, but there is no uniform rate over all simple laws: for any prescribed `h`, two ages can be separated by `h/10` with probability one. If a model separately supplies `P(D_min<=h) <= r(h)`, then the probability that occupied bins fail to represent all `n` entries is at most `r(h)`; on the complement, matching each age to a representative in its bin has error at most `h`.

If there is an unbounded uncompactified acquisition cutoff `T`, add tail risk `P(max_i A_i>T)`. A useful finite-grid failure bound is therefore

`P(cell collision or age beyond T) <= P(D_min<=h) + P(max_i A_i>T)`.

Neither term has a uniform law-free rate under the theorem's assumptions.

## Finite-observation lower witness, including shaped controls

An unrestricted law on a continuous or sufficiently rich age domain is not identified by any finite menu of controls, even if each control has a known nonlinear, shaped, or multipulse per-age probability profile. Suppose there are `M` controls, each inducing a known function `f_r(a) in [0,1]`. Choose `M+2` distinct candidate ages `a_i`. The `M+2` vectors

`v_i = (1, f_1(a_i), ..., f_M(a_i)) in R^(M+1)`

are linearly dependent: choose nonzero `c_i` with `sum_i c_i v_i=0`. Since `sum_i c_i=0`, the coefficients have both signs. Normalize the positive and negative parts to probability measures `mu_+` and `mu_-` on the candidate ages. They are different, simple one-atom age laws, but

`int f_r d mu_+ = int f_r d mu_-` for every one of the `M` controls.

For any desired fixed `n`, add the same `n-1` distinct ages outside the candidate set to every history, and let the final age be drawn from `mu_+` or `mu_-`. Each history is simple. Under control `r`, the first `n-1` label bits have the same fixed distribution in both hypotheses; after averaging over the final age, its label is Bernoulli with parameter `int f_r d mu`. Equality of this parameter implies equality of the *entire* count histogram. Thus all `M` controls have identical observations under two distinct simple `n`-entry laws.

The conclusion covers any finite collection of per-age response profiles; a waveform's shape or nonlinear construction does not evade finite dimensionality. It also covers adaptive choice from a finite menu when every new product is an independent draw from the ancestry law, by induction on the transcript: under either hypothesis every possible selected next control has the same conditional observation law. It does not assert that the ideal infinite family of controls is uninformative.

The exact rational check uses `M=2`, four candidate ages `t=0,1/3,2/3,1`, and profiles `f_1(t)=1/4+t/2`, `f_2(t)=1/4+t^2/2`. The distinct laws with weights `(1/4,0,3/4,0)` and `(0,3/4,0,1/4)` both have profile means `(1/2,5/12)`. Adding two common atoms gives a simple three-entry witness with identical full histograms for both shaped controls.

## Purity contrast and statistical cost

Let `A_n` be the `(n+1)x(n+1)` stochastic channel whose column `j` is the count histogram from `n-j` low-probability and `j` high-probability independent labels. Its columns are the coefficients of `ell^(n-j) h^j`; it is invertible exactly when `Delta=|p_H-p_L|>0`. Its determinant magnitude is `Delta^(n(n+1)/2)` (the degree-`n` symmetric-power change of basis), and exact inversion can be poorly conditioned.

An explicit pair demonstrates the contrast cost. Put

`pi_+(j)=2^(-(n-1)) C(n,j)` for even `j`, zero for odd `j`,

`pi_-(j)=2^(-(n-1)) C(n,j)` for odd `j`, zero for even `j`.

These are probability laws with total variation one and a void-probability gap `2^(-(n-1))`. Their output generating functions differ by

`G_+(z)-G_-(z) = 2^(-(n-1)) (ell(z)-h(z))^n`

so the total variation of the observed count histograms is exactly `Delta^n`. The input/output `l1` ratio gives `||A_n^(-1)||_(1->1) >= Delta^(-n)`. At `n=6`, `p_L=0.25`, `p_H=0.35`, the output TV is `10^-6` despite a TV-one difference in the `J_B` laws.

For this pair, if every per-atom label probability lies in `[eta,1-eta]`, then each output count bin under either mixture is at least `eta^n`. The exact histogram difference has coefficients `2^(-(n-1)) Delta^n (-1)^(n-k) C(n,k)`, yielding

`KL(q_+ || q_-) <= chi^2(q_+,q_-) <= Delta^(2n) C(2n,n) / (2^(2n-2) eta^n)`.

For `n=6`, `eta=1/4`, `Delta=0.1`, this upper bound is `3.696e-9`. Pinsker's inequality implies that distinguishing this pair with maximum error at most `alpha` from `N` independent products in this one-set assay requires

`N >= 2(1-2 alpha)^2 / [Delta^(2n) C(2n,n)/(2^(2n-2) eta^n)]`.

At `alpha=0.05`, this is at least about `4.38e8` products. This is a per-set worst-case channel-conditioning witness, not a universal lower bound for a richer multi-control design.

Finite temporal bandwidth has a separate cost. If every admissible per-age profile is `M`-Lipschitz and two simple histories can be atomwise matched within `epsilon`, then their per-atom label probabilities differ by at most `M epsilon`. If all probabilities lie in `[eta,1-eta]`, the KL divergence of the full labeled product (and hence of the count histogram) is at most

`n (M epsilon)^2 / [eta(1-eta)]`.

For `N` independent products and maximum testing error `alpha`, Pinsker gives the necessary condition

`N >= 2(1-2 alpha)^2 eta(1-eta) / [n M^2 epsilon^2]`.

Thus simple but nearly coincident histories can be practically indistinguishable at finite bandwidth. This statement assumes the stated uniform slope bound; without a bandwidth bound, no such resolution scale follows.

## What is needed for a consequential decision

Full ancestry-law recovery is a sufficient representation, not a default experimental objective. The decision-maker should first name the estimand and the action threshold. If the decision depends on one event such as `P(J_B=0)` or on a particular contrast of entry-time regions, acquire the calibrated controls and count bins that estimate that quantity directly, then quantify its uncertainty relative to the threshold. Full multiscale support tomography is warranted only if the decision actually depends on the whole law. A mathematically identifiable inverse with poor contrast, unknown delay, unmodeled prehistory, or a rank-deficient detector may still be inadequate for a finite-cost decision.

## Reproduction

`python3 finite_checks.py` uses exact rational arithmetic for the finite partition Möbius inversion, the three-cell and multiplicity witnesses, the parity-channel identity and determinant, the purity-conditioning calculation, the near-pair bound, and the finite shaped-control affine witness. The generated values are saved in `results.json`.
