# Independent receiving review: controlled density/current action

**Reviewer:** existing `record_geometry` complementary role within Astra P1; no additional agents.  
**Date:** 2026-10-29.  
**Method:** actual-file mathematical review, independent reconstruction of the occupation/tilted-hydrodynamic dependency, and comparison with primary predecessors. No numerical fixture or formal proof assistant is claimed.

## 1. Actual reviewed inputs and preserved snapshots

| Root file | SHA-256 read and snapshotted |
|---|---|
| `CONTROLLED_MACROSCOPIC_ACTION.md` | `c15a789c95e8472531fd575a9f252f35d6345ea7f5d830d35c08a4a07ab3202e` |
| `RARE_TRANSPORT_WITHOUT_KINETIC_IDENTIFICATION.md` | `3338d603b4944c6c0dbab415ed913a94b28588788ac690dacb28eb62a4158740` |
| `IMPLEMENTATION_SYMMETRY_AND_RARE_EVENT_CONFIDENCE.md` | `a93e4af190a7aaa45ea2a65b6ad6cdfd1fa2f14440aabe603a63c3c2761f1d20` |
| `PHASE_AVERAGING_AT_LARGE_DEVIATION_SCALE.md` | `1fea0349712fc377e58e273410b158fe1f59713ea05693b64bf34bfdf6ad781b` |

Exact copies are preserved in this directory with `_REVIEWED_<first12sha>.md` suffixes. The reviewed root versions were rehashed after the review and were unchanged at that check. This receipt does not certify later edits automatically.

## 2. Verdict

**The density/current path LDP is accepted as proved at the stated one-dimensional, fixed finite diffusive time, common-mean, `a<1`, deterministic-associated-initial-profile interface, with the explicit tilted receiver identified below as a dependency.** The scalar circulation LDP and its SCGF are also accepted. I found no load-bearing mathematical error in the action identification, current topology, smoothing construction, reciprocal-error estimate, or actual initialization argument.

This acceptance is for every specified sequence of deterministic initial configurations whose empirical measures approach `m dx`, uniformly in the allowed hidden amplitudes, frozen sectors, and initial phases at their stated fresh-future-noise interface. One sentence concerning uniformity over initial configurations needs the quantifier clarification in Section 7 below. The theorem does not become a uniform assertion over all convergent initial sequences without a common modulus of initial-profile association.

The proof is an assembled controlled extension of established exclusion large-deviation machinery. This receipt does not establish historical priority, apparatus feasibility, a new generic large-deviation principle, a practical speedup, or unconditional rare-event accuracy from fixed-confidence calibration.

## 3. The formerly imported occupation and tilted-LLN step is now explicit

The load-bearing receiving dependency is

`TILTED_HYDRODYNAMIC_RECEIVER.md`  
SHA-256 `1146645289a7534616059e57d7fe6e130dc8fd83d161a78f9d4c99a985b8f140`.

It reconstructs the actual variational occupation estimate rather than asserting that a classical path theorem applies directly to a nonlocal joint generator. The argument uses:

- uniform canonical block moments and finite fixed-block Poincare constants;
- a two-block comparison whose connecting transposition obeys `D_(x,x+y)<=4y sum_adjacent D_i`;
- the resulting numerical-range bound, with limits `N -> infinity`, macroscopic block fraction to zero, and fixed auxiliary block size to infinity;
- the joint-to-visible Dirichlet-form inequality, applied separately at every phase configuration;
- the weak-tilt likelihood `L2` bound and actual active initialization solely for superexponential replacement events.

No spatial locality of the unknown amplitudes enters these steps. After phase replacement, the remaining nonlinear flux contains only the ordinary pair activity. The occupation estimate identifies it with `2 rho(1-rho)`. Martingale brackets are `O(1/N)`. The limit solves

\[
\rho_t=(s/2)\rho_{xx}-\partial_x[s\rho(1-\rho)E].
\]

An `L2` difference estimate gives uniqueness for smooth bounded deterministic `E`. The current martingale additionally identifies its spatially constant component; density continuity alone would not do so. Constant `E` and flat initial profile give exactly the activity and circulation assertions required for the scalar lower bound.

The companion endpoint lemma

`PHASE_ENERGY_SUPPLIES_EXCHANGE_COERCIVITY.md`  
SHA-256 `7bcaa5f294219055b598f69e605ee285b5083e01db1fe1f8f2052511d3fe7189`

proves `D_ex <= (4/s)D_native+8D_phase`. It would extend the occupation supplier to `|alpha|<=1` for sufficiently large bath rate. The reviewed root theorem retains `a<1`; this possible extension is not silently added to its claim.

## 4. Full-action proof: specific attacks resolved

### Topology and compact containment

The ambient `D([0,T],H^{-3} x H^{-3})` is a concrete Polish choice. Uniform total-variation balls of signed measures are compact in `H^{-3}`; bounded Fourier coefficients and a summable Fourier tail prove this. On such balls, its topology agrees with weak measure convergence.

Exact one-dimensional conservation gives `|J_i/N-J_j/N|<=1`, hence `||W_t^N||_TV<=|Q_N(t)|+1`. This closes spatial current compact containment from the scalar circulation estimate. The current exponential martingale has the stated jump and bracket scales, and the accumulated phase residual has a superexponential uniform-time bound. A deterministic interval grid therefore supplies the exponential temporal moduli. The ordinary exponential Arzela–Ascoli argument then applies.

The actual text correctly distinguishes continuous limiting support from literal continuity of finite-system paths. Linear interpolation changes density by at most `2/N` and current by at most `1/N^2` in total variation. These deterministic errors are sufficient for exponential equivalence at every fixed positive tolerance.

The discrete continuity relation differs from its continuum test formulation by at most `C_G ||W^N||_TV/N`. In a bounded neighborhood of a candidate path, the circulation is bounded because it is the continuous functional `W -> <W,1>`. The preceding deterministic TV bound therefore makes this error vanish. Thus excluding paths that violate limiting continuity is justified, rather than being a formal substitution of derivatives.

### Upper functional

The sign and normalization in the likelihood functional are correct: its linear part is the pairing of `j+(s/2)rho_x` with `E`, and its quadratic term is `(s/2) int chi(rho) E^2`. The nonlinear mobility must first be spatially smoothed. On the bounded-density support, this makes the functional continuous in the chosen weak path topology. A sharp block kernel can also be replaced by a smooth one; its boundary error tends to zero.

The text uses the correct block-limit order. It does not claim a superexponential occupation error at every fixed macroscopic block scale. For each required finite upper exponent, choose the scale sufficiently small after the volume limsup. Finite covers of compact sets and exponential tightness then give the closed-set upper bound.

### Finite energy and goodness

The weighted Riesz argument is valid even where `chi(rho)=0`: finiteness of the supremum annihilates the null space of the weighted norm. The resulting `A=j+(s/2)rho_x` has weighted finite energy and hence ordinary `L2` energy because `chi<=1/4`. The forced heat equation with initial trace `m` has the displayed energy estimate by Fourier/Galerkin or mollified weak testing. It supplies `rho_x` and `j` in `L2`.

Action bounds therefore give compactness of both density and integrated current in the stated weak continuous path topology. The integral of `A^2/chi(rho)` is jointly convex and lower semicontinuous, so weak compactness yields the good-rate property. No visible spectral-gap lower bound is inserted in this argument.

### Lower bound and smooth approximation

For a smooth interior-density path, `E=[j+(s/2)rho_x]/[s chi(rho)]` is a legitimate bounded deterministic comparison field. The reconstructed receiver starts from the actual initial visible configuration and arbitrary initial phases, and yields convergence to that path. Restricting the inverse likelihood to a typical likelihood-cost event gives the desired lower exponent.

The smoothing construction survives the initial-trace attack. Mixing with `(m,0)` preserves continuity and opens a positive density margin. Spatial convolution preserves the constant initial profile. Extending by `(m,0)` to negative times creates no distributional continuity defect because the density trace is `m`. Past-only time convolution supported away from zero produces a smooth path that is exactly flat near time zero, uses no values beyond `T`, and does not increase the integrated convex action. Ordinary `L2` convergence of `A,j,rho_x`, convergence of the integrated currents, and lower semicontinuity provide the claimed convergence of costs. Weighted-energy convergence need not be assumed separately.

## 5. Scalar circulation and exponential moments

The finite disjoint-block activity upper estimate has the correct canonical normalization. With `ell-1` internal bonds and normalization `1/ell`, the canonical mean of activity is exactly `2 chi(k/ell)`. Its FK cost is of order `b^2 C_ell ell/N` before division by the speed. The omitted-bond term and concavity of `chi` give the stated activity upper bound.

The lower connection is closed by the explicit receiver. Its current is `s chi(m) E T`, consistent with the native rate `s/2` and canonical activity `2 chi(m)`. The inverse-likelihood restriction is in the correct direction.

The SCGF is not inferred solely by a formal Legendre transform. The actual proof supplies exponential-moment bounds at `2 lambda`, exponential tightness, and the required tail estimate. Splitting the initial active layer by Cauchy–Schwarz uses its unconditional endpoint density and the Markov continuation, not a conditional endpoint reset. The Poisson contribution of that short layer has the stated negligible fixed exponential-moment cost.

## 6. Implementation and confidence review

The own-swap antisymmetry identity for the reciprocal residual is correct. With `D_native=(1/2)sum r_i(Delta_i f)^2`, its constant

\[
\frac{s\|F\|_\infty}{\sqrt{2c_*}}d_N\sqrt{N D_{\rm native}}
\]

is consistent with the factor `s/4` in the change-of-variables identity. Completing the square gives the claimed `O(b^2 N d_N^2)` numerical-range cost. Thus no condition `N d_N ->0` is needed for these uniformly vanishing reciprocal errors. The pointwise mobility error is also `O(d_N)`.

The directional `exp(c delta_i/N)` example genuinely changes the macroscopic current and is an appropriate contrast in assumptions. The calibration mixture is a valid exact obstruction: a fixed positive weight on a larger mobility selects its cheaper rare-current exponent. The text correctly distinguishes population structure, coverage, conditional records, and an unconditional failure exponent. The actual operation and sensing costs remain explicit.

## 7. Requested quantifier clarification

In the scalar file, the sentence that the conclusion holds "uniformly over such deterministic initial contexts" should specify one of the following equivalent intended uses:

1. **For every sequence** of deterministic initial configurations whose empirical profile tends to `m`; the dynamical estimates are uniform in hidden amplitudes, frozen sectors, and initial phases.
2. Uniformly over a family of initial configurations with a **common vanishing bound** on their weak-profile distance from `m dx`.

Literal uniformity over the set of all convergent initial sequences is false: for each volume one may select a sequence with an arbitrarily bad initial configuration at that single volume and the desired configurations thereafter. Each sequence converges, while the supremum over sequences at that volume need not. This does not refute the fixed-sequence theorem proved in the files; it is a quantifier correction to prevent an unintended stronger claim.

For a final receiving record, also link the exact `TILTED_HYDRODYNAMIC_RECEIVER.md` filename and its reviewed hash instead of leaving only the general phrase that the complementary proof is saved separately.

