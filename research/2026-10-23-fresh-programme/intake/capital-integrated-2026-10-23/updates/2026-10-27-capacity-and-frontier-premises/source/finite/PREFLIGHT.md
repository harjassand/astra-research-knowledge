# Finite-signal preflight: NO ADMISSION

27 October 2026. Preparation only; no experimental arms, new agent, programme message, goal or automation. Dots and biology's platform hold were untouched. This supersedes the proposed next experiment in `../DIAGNOSIS.md`.

**Reject admission of finite-state or useful finite-signal existence as the proposed missing operation.** Existing Astra material already contains exact finite rational quantum-memory witnesses. A small ordinary adaptation, checked with its existing exact eigenvalue/logarithm machinery, also supplies a full-rank, moderate-signal, asymmetric positive-channel example. No new representation, optimisation algorithm or difficult mechanism was needed. My earlier suggestion had not checked these direct examples and therefore repeated the prior-selection problem it diagnosed.

## Existing source and status

The inspected local knowledge checkout is commit `65aae508a61d02e4a6ba5b368a94779ae6d744cf`. N405 leads directly to `updates/BG/package/adaptive/CLASSICAL_EXAMPLES.md`, not merely the rare-flag asymptotic theorem. Section 4 gives rational three-dimensional fixed-reference states, an exact information-ratio certificate above 0.91849 for ternary exclusion, and explicitly reports its approximately `5.51e-9`-nat denominator. The conditional qubit example in section 3 is a different quantity and does not have equal reference marginals. These must not be conflated.

The N405/LA125 universal Choi theorem retains its source-reported unreviewed status; this preflight does not certify it. The ordinary symmetric-channel KL bound in CLASSICAL_EXAMPLES sections 1–2 has its own direct proof. The fixed finite witnesses and their arithmetic certificates can be checked without accepting the universal theorem. The HTML extraction of CLASSICAL_EXAMPLES matches its indexed UTF-8 hash `ff2551a7f93df0c46e25acb5442d9a8e589dd1546532a021aae73bf5ad217de0`.

N964/N965's source equality arguments already construct finite equal-reference pairs through a Liouville/vacuum lift. They prove coefficient equality by ordered limits and explicitly disclaim resource efficiency; they do not say every useful finite gap needs extreme precision. Q28's accepted lift is another sufficient construction. Its logarithmic asymptotic error is not an all-state resource lower bound. The direct finite-cq/BKM tools were also already present: exact eigenvalue/log certificates, nullspace-constrained BKM generalized eigenproblems, and explicit finite-pair relative-entropy evaluation. No general optimizer is needed to defeat the present existence target.

## Concrete ordinary construction and exact result

Use the existing fixed-reference family with

`u0=(1/2,0), u1=(0,1/2), u2=(-1/2,-1/2)`;

`p=1/(1+n^2), q=1-p`, and blocks

`rho_x = [[q u_x u_x^T, t sqrt(pq) u_x], [t sqrt(pq) u_x^T, p/3]]`.

Let `omega` delete the off-diagonal active/vacuum blocks. Mix both states with the same `mix*I_9/9`. Normalization and equality of both reference and classical-input marginals hold exactly. The nontrivial Schur complement is `p(1/3-t^2)>0`; mixing gives every input block eigenvalue at least `mix/9`. Since `sqrt(pq)=n/(1+n^2)`, all entries are rational.

For the asymmetric case use `n=3,t=1/2,mix=1/100` and

```
K = (1/30000) [[199,14752,15049],
               [15049,199,14752],
               [14752,15049,199]]
L = (1/300)   [[298,1,1],[1,298,1],[1,1,298]].
```

Both are strictly positive and L is invertible. Put T0's diagonal to `1/297` and its off-diagonal to `148/297`. For the cyclic permutation P,

`K = [(99/100)T0+(1/100)P] L`.

The independently proved ordinary coefficient of T0 is `2401/4917`. Joint convexity of relative entropy and permutation data processing therefore give the uniform ordinary upper bound

`(99/100)(2401/4917)+1/100 = 1838/3725 < 0.493423`.

This is a strong all-classical-pairs upper bound, including arbitrarily large classical reference memories. It is not a weak selected classical witness.

| Exact interval check | Asymmetric positive case | Existing positive quantum control |
|---|---:|---:|
| `D_K(rho||omega)`, nats | `[0.109608921871205,0.109608921871206]` | `[0.003808759466377,0.003808759466378]` |
| `D_L(rho||omega)`, nats | `[0.201240747202982,0.201240747202983]` | `[0.012335556114923,0.012335556114924]` |
| Ratio | `[0.544665647462775,0.544665647462776]` | `[0.308762688191243,0.308762688191244]` |
| Certified ordinary upper | `1838/3725` | `625/2046` |
| Input-block spectral floor | `1/900` | `1/9000` |
| Largest rational denominator size, states and channels | 16 bits | 19 bits |

The second column uses exactly K,L from `experiments/channel_case/public/DEVELOPMENT.json`'s quantum control, with the same ordinary source family at `n=10,t=3/10,mix=1/1000`. Its scalar upper follows from the known symmetric channel `K L^-1`. The finite-state construction is thus available even on the actual previously supplied control; a free certificate is not its only route to finite evidence.

`preflight.py` imports the existing exact routines with their main programs disabled, checks rational normalization/marginals/PSD floors, isolates eigenvalues with exact rational Sturm intervals, and encloses logarithms with the source's proved rational remainder. Assertions compare the interval lower ratio with the exact classical upper. `RESULT.json` records source hashes and all outputs. Floating point is not used in these certificate assertions. These small checks are preparation and earn no later experimental performance credit.

## Keep the resources separate

- **Signal:** the asymmetric example's denominator is approximately 0.20124 nats, not a vanishing perturbation. The actual output trace distances between rho and omega are approximately 0.124248 for K and 0.250970 for L. Corresponding one-copy optimal equal-prior discrimination success probabilities are approximately 0.562124 and 0.625485. These describe known states, not an acquired detector or preparation device.
- **Copies:** repeating the individual Helstrom binary measurement and thresholding its outcomes gives sufficient bounds of 389 K-output copies or 96 L-output copies for each error at most 5%, by Hoeffding. These conservative bounds refer to this pair and measurement; they are not optimal copy complexity and do not compare quantum versus classical end-to-end cost. The control's analogous sufficient counts are 9340 and 2383.
- **Precision:** the displayed state entries have small rational descriptions. Description size is neither preparation accuracy nor synthesis cost. No state-preparation/calibration/noise-control cost was acquired.
- **Spectrum:** the floors above are chosen mathematical properties. Small eigenvalues or pure states are not automatically hard physical resources. No necessity claim follows from imposing a floor or inspecting one lift.
- **Matched comparison:** the coefficient gap compares the same known K,L and one channel use per sample, against a uniform ordinary relative-entropy inequality. It does not by itself establish a measurement, communication-rate, total-copy or physical advantage over the strongest ordinary implementation.

## Residual and decision

An exact all-state optimum under a chosen `(delta,h)` restriction is not supplied by this bounded inspection. Neither is a sharp necessary precision/copy frontier near the unconstrained coefficient. Those are possible mathematical questions, not admitted targets: there is presently no independently justified preparation/noise model, consequential resource target, strong implemented constrained-state incumbent, or demonstrated obstruction that makes the proposed hard mechanism necessary. Inventing a restrictive floor or demanding another small constant would recreate the earlier artificial benchmark problem.

**Honest outcome: no admissible residual from this suggestion.** Preserve the valid evaluator, existing finite examples and this prior correction. A later research question would need its own substantive use case and preflight. No historically-open assertion follows from this search.

## Read paths

- N405/LA125 packets: `astra-retrieval-knowledge-20261025/repo/knowledge/current/packets/`.
- Existing source originals, represented as exact UTF-8 `<pre>` text: `repo/web/pages/d-ab1d4c30c4e4f791.html` (CLASSICAL_EXAMPLES); `d-eb306dc665938036.html` (RESULTS, especially sections 7 and 8.3); `d-33ac0978b4a4cfcf.html` and `d-7904726a2bf560da.html` (exact finite certificates). Their original path mappings are in `repo/web/BG-library/0001.txt`.
- N964/N965 governing sources: `repo/research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-25-dots-ultra-selected-sources/source/dots/classical_channel_sld_bkm_equality.md`, `classical_two_channel_relative_equality.md`, and `classical_liouville_lift_root.md`.
- Direct BKM code: `repo/web/pages/d-c569400f3fc5e2fc.html`, `d-7626eaa5d3c10f83.html`; Q28 finite-state evaluation: `astra-method-experiment-20261026/review_material/Q28/stage2/stress_finite_reference.py:80–165`.

All paths above beginning with `repo/` refer to `astra-retrieval-knowledge-20261025/repo/` under the shared coordination `work/` directory.
