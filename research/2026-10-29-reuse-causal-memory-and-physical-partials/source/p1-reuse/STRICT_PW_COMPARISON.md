# Stricter stationary target: executed ordinary global-PW comparators

Both new comparators target per-output stationary W2 at most 0.1 for 8,192
outputs from the same fixed source (`d=96`, supplied `L=.5`, `sigma=1`,
source seed `2026102963`). They preserve all earlier code and receipts.

## Complete executed comparison

| Route | Values per output after preparation | Complete original vector queries | Complete scalar answers | Proved per-output W2 bound |
|---|---:|---:|---:|---:|
| Standalone ordinary global PW, start at zero | 238 | 1,949,697 | 187,170,912 | 0.0998763231023892 |
| Same acquired candidate start, ordinary global PW | 191 | 1,589,249 | 152,567,904 | 0.09979577096414748 |
| Acquired integrated-noise control-variate correction | 52 | 450,561 | 43,253,856 | 0.09840593680410953 |

The second row is the stronger equally informed ordinary global-PW
comparison. It starts from exactly the acquired candidate law and initial
residual-radius certificate used by the corrected sampler. Its complete
count includes the same 24,577 acquisition queries, plus 1,564,672 newly
executed production queries. The acquired training anchor is included in
that acquisition; no duplicate anchor is needed.

The corrected route also pays 24,577 acquisition queries, followed by
425,984 correction queries. The equally informed global comparator uses
1,138,688 more native vector values, a factor 3.527267118103875 in complete
query cost. This is a comparison of explicit policies and their finite
schedule families, not a lower bound on other methods.

## Schedules and accepted proof

Both global comparators use the previously accepted Paulin-Whalley
Theorem 2.8 application, with

    eta_global(q)=sqrt(d ln 2) L^2/(q sigma),
    e_t <= L e_(t-1)+eta_global(q_t).

The source theorem is in Daniel Paulin and Peter A. Whalley,
*Theoretical guarantees for stochastic gradient sampling methods via
Gaussian convolution inequalities*,
https://arxiv.org/html/2604.24632v2 . The Gaussian pushforward Poincare,
transport-entropy and mollification application is already recorded in
`PW_GAUSSIAN_SAMPLE_AVERAGE_COMPARATOR.md`; it is unchanged here.

The finite search used at most 30 steps, total integer samples at most
1,000, and at least one sample at every executed step. The standalone
baseline acquires one g(0), obtains the same moment radius
`B=29.433876913398134`, and uses

    [1,1,1,2,2,3,4,6,9,12,18,25,35,49,70], sum=238.

The best searched bound with fewer samples was 0.10029285373562809.

For the acquired-start comparator, the authorized shared interface record
gives `A0=0.4943461674646958`. The chosen schedule is

    [17,24,34,48,68], sum=191.

The best searched bound with fewer samples was 0.10024338597300121.

Independent 70-digit recurrence calculations from the recorded initial
radii reproduced both final error bounds. The saved full search tables
document the stated finite-domain comparisons. No schedule optimality
outside that domain is asserted.

The root corrected execution uses the same acquired initial radius and
`c=0.5452285285907604`, with schedule `[5,7,9,13,18]`. The global kernel
coefficient is `sqrt(96 ln2)*.25=2.039333980337618`. The smaller corrected
coefficient comes from the acquired integrated-noise bound and its proved
transfer to the target law, together with the affine control variate. It is
not obtained by substituting average covariance for a uniform bound.

## Information and execution

The standalone policy receives only original source values and the supplied
dimension, L and sigma. The acquired-start policy additionally reads the
authorized frozen candidate Gaussian law and its acquired initial error
radius from `ACQUIRED_ACCURACY_INTERFACE_RESULTS.json`. It has the same S
information available, but its ordinary global formula does not exploit S.
The control-variate correction is the explicit route that does exploit it.

The acquired-start production uses the same initial Gaussian seed family
as the corrected execution. At every step both new policies query original
values at their own actual adaptive chain centers. Every batch row is
charged. No private source matrix, frequency, analytic mean, covariance or
stationary reference is accessed. No private diagnostic was run.

The shared acquisition receipt and the new production receipt are both
preserved. Their counts are summed for the complete acquired-start cost;
the already executed acquisition is not represented as free information.
The exact source hash agrees between the shared acquisition and production.

The dense fixture costs O(d^2) arithmetic per original value, in addition
to all Gaussian preparation and O(d) vector arithmetic. Its QR setup costs
O(d^3). For the actual separated acquired-start experiment, the source was
instantiated once for the shared acquisition and reinstantiated identically
for new production, so two such setup operations occurred across those
stages. A single persistent-oracle implementation can use one setup. This
distinction does not change the fully charged native value counts. BLAS
execution was restricted to one thread.

## Confidence and remaining scope

The standalone global guarantee is deterministic under the declared ideal
primitives and global Lipschitz premise. Both policies using the acquired
record inherit its joint false-certificate budget of 1/1024. This is an
unconditional failure-probability guarantee over acquisition, not posterior
confidence conditional on the observed record or an unconditional mixture
W2 assertion.

For the acquired policies, fresh production chains are independent
conditional on the frozen representation. Shared training can correlate
their unconditional laws. All displayed W2 guarantees are per output; the
ordinary product-space bound scales by sqrt(8192).

These floating executions preserve the accepted ideal-value and
ideal-Gaussian scope; neither counts nor numerical recurrence checks acquire
instrument precision. No stronger sampler using only the present acquired
record was established that beats the integrated-noise correction. That
absence is not an optimality claim. Conventional control-variate sampling
can itself adopt the acquired interface; the comparison isolates the value
of that acquired information rather than establishing a new sampling
primitive by nomenclature.

## Saved files

- `pw_global_strict_sampler.py`, `PW_GLOBAL_STRICT_01_RESULTS.json`, and
  `PW_GLOBAL_STRICT_01_DATA.npz`: standalone global baseline.
- `pw_acquired_start_strict_sampler.py`,
  `PW_ACQUIRED_START_STRICT_01_RESULTS.json`, and
  `PW_ACQUIRED_START_STRICT_01_DATA.npz`: equally informed acquired-start
  global baseline.
- `STRICT_PW_COMPARATOR_CHECKS.json`: high-precision recurrence checks,
  hashes, frozen-code verification, and setup-accounting clarification.
