# Executed finite checks and numerical limits

## Frozen native checks

Input: evidence/PREEXECUTION_FREEZE.json, SHA256
357cb63fb78fa1fe0fe627e84c0cf58942cd64261834805224635028736e0253.
Code: code/exact_checks.py, SHA256
c78a5576bc5861501a9f936e495e84d03a0b7f8dffbf80799455c9b814b91711.

Both fixtures use exact Fraction arithmetic, eta=1/2,alpha=1/2,b=1/2,K=1.

| Fixture | R_A | M | kappa | Depth | Horizon | Terminal target mass |
|---|---:|---:|---:|---:|---:|---:|
| Expansion | 3/2 | 2 | 4 | 4 | 64 | 1/512 |
| Coalescence | 16 | 4 | 0 | 6 | 128 | 1/256 |

The actual native proposal edge formula is the new saturated1/(M+R_A),
R_A/(M+R_A) pair. The complete code generates the labels, sparse native
proposal, exact local acceptance and quotient from those inputs. It tests
every native proposal edge and completing diagonal. It never normalizes a
killed row or substitutes a fictitious simulator.

Every structural identity and finite full-law inequality passed. Expansion
has32 native states and a6-state quotient; its dense native G,C and first
four laws were compared exactly with the quotient. Coalescence has5462
native states,10920 directed proposal edges and an8-state quotient; no
dense5462-state global matrix was formed. Horizon laws use the proved quotient.

| Fixture | Rigorous KL gate | Certificate | Full-law TV |
|---|---|---:|---:|
| Expansion | PASS, KL approximately0.7871982548836166 | 0.02153477531169968 | 0.04917383575018947 |
| Coalescence | FAIL, KL approximately1.103836351039874 | 0.004108528887207315 | 0.04237325886901944 |

The rigorous KL decision uses exact binary range reduction,24 positive
atanh-series terms and a rational remainder. Floating values in this table
are only short displays. The second case is excluded from admitted K=1
empirical evidence. Its code exit1 is intentional; neither inputs nor
acceptance criteria were retuned. This finite failure does not establish a
defect in the separately proved eventual-admission limit.

All exact matrices, original laws, ordinary-IMH laws, fractions or their
canonical numerator/denominator hashes, gate decisions and counts are under
evidence/exact/. The producer body used5.262211834 CPU seconds,
5.266222576 wall seconds and19968KiB peak RSS on Linux.

## Constant brackets and scientific figure

code/rate_function.py implements the exact scalar formula. Its constant
certificate uses rational atanh logarithm bounds, exact bisection and an
alternating exp(-1) enclosure; no float determines a theorem inequality.
The reported rational intervals are outward rounded to24 decimal places.
The first serialization failure and code snapshot are preserved.

The accepted constants are approximately:
- c(0)=0.648419527440700...
- log2=0.693147180559945...
- log(1+exp(-1))=0.313261687518223...
- d_middle=log4-1=0.386294361119891...

Their ordering is also proved analytically in the principal source. The
figure evaluates g(d)=(1+d)c(d) on a fixed601-point grid from0 to6 at
K=1,alpha=1/2. It is an illustration of a proved function, not a regression
on chain data or numerical evidence for an asymptotic limit. The final
standalone PNG/PDF and actual grid are under evidence/rate_figure_final/.

The constant certificate plus initial figure used5.357568767 CPU seconds,
4.757848612 wall seconds and79700KiB peak RSS. A layout-only correction
used3.959577826 CPU seconds,3.195043117 wall seconds and79508KiB peak RSS.
The previous executed script versions and both figure receipts are retained.

## Scope of reproduction

Default replay verifies payload identities and the recorded expected gate
pattern. Optional --execute-checks reproduces only the new exact fixtures
in a temporary directory and expects the preserved coalescence failure.
It compares substantive exact-result hashes while ignoring fresh resource
timestamps. No historical scientific suite is included in that execution.

Finite checks and arithmetic certificates do not replace the universal proof.
The asymptotic native trees are not materialized or simulated for enormous
horizons. Total inference, design and discovery costs remain unknown.
