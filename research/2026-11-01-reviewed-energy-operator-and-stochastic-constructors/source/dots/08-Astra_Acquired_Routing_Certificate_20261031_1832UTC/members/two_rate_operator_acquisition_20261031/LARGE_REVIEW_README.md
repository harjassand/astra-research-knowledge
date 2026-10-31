# Acquired large-state routing certificates — local review checkpoint

Status: author proofs and executable checks; independent review pending for
this new branch. No earlier receipt covers it. No upload or publication.

## Result and scope

An ordinary sparse-edge community proposal acquires a four-block partition
of a 4096-state source. A separate observation pass acquires column mass and
a finite-bit fresh-probe complement bound. Fresh quadratic statistics certify
small incoming and outgoing leakage without learning every transition entry
accurately. The same outgoing batches also provide fine stochastic block
action, with a second simultaneous confidence event, not extra source calls.

For fixed compatible b and ell, stochastic full dynamics and positive coarse
replay give the uniform bound

    error <= ||ell||1 ||b||infinity [L d + e_out sum_{j<L} t_j],
    t_0=0,  t_(j+1)=min(1, alpha t_j+e_in).

It covers every word of length <=L on one confidence event, including future
words chosen adaptively from previous predictions. This is NOT state-feedback
control of an evolving realized trajectory. It does not promise arbitrary
new observables, microscopic initial states, or unbounded future horizons.

The source access is ordinary named-row forward sampling. All represented
queries, failed precision rounds, row choices and label lookups are charged.
Synthetic aggregate NumPy multinomials do not physically execute those calls
or prove ideal iid randomness. The theorem assumes authentic iid fresh
batches and independent fresh norm probes; saved counts cannot authenticate
that provenance. Fixed mock seeds are for reproduction, not cryptographic
or adversarial-input guarantees. True source coordinates are not learner input.

## Current measured ledger

| Fixture | Retained logical calls | Rank | Uniform error bound | Online grid |
|---|---:|---:|---:|---:|
| Slow routing tau=.02 | 942,957,056 | 4 | .0193316655 | 13 bits |
| History-sensitive tau=.04 | 3,298,951,680 | 4 | .0150512743 | 11 bits |

The first unretained implementation cost 4,315,164,672 calls on the slow
fixture; its source/results remain a historical comparison. The retained
implementation uses exactly its original observation prefix, stops sooner,
and avoids all independent fine sampling. These are sufficient schedules,
not necessary prices. No practical deployment advantage is established.

For the stronger fixture, two same-action-count words have a certified true
output spread >=.0636474, so action-count-only epsilon=.02 prediction fails.
The earlier slow fixture did not establish that distinction; both are kept.
For 50,000 supplied schedules, list-best regret is at most .04. There is no
unpriced search over policies. Cached evaluation stores 475,132 prefix states
and about 1.90 million state integers (plus prefix keys and Python overhead).
The separate streamed backend emits every prediction with four live state
integers, 24 live input symbols, 19.2 million scalar operator products and
200,000 output products. Its compressed output is 459,659 bytes; input and
output storage are not part of the 468-byte compiled-model figure.

Sparse norm acquisition uses hundreds-of-bit integers: the slow case's grid
is 562 bits and peak accumulators 629 bits, not 13-bit arithmetic throughout.
All serialized rational components in that result reach 632 bits. Exact
arithmetic costs during acquisition are not reduced to the online rank alone.

## Strong comparisons and limitations

Ordinary community/spectral/Krylov/range learners PLUS this acquired
certificate have the same permission and capability. The construction is
not an exclusive new learner. Conversely their ability to adopt a derived
certificate does not automatically erase that certificate's contribution.
Exact historical matching of the assembled certificate remains unresolved;
standard aggregation, concentration, power iteration, U-statistics and
empirical Bernstein ingredients are explicitly credited in
LARGE_PRIOR_AND_LIMITS.md and PRIOR_MATCH_AND_SCOPE.md.

The sharpened retained-prefix Hoeffding MC budget is 11.2996 billion calls
for the same 49,928 distinct schedules and confidence, not the earlier
base-two-log 16.0573-billion figure. It is a sufficient comparison, NOT a
lower bound or proof against the strongest variance/KL/adaptive/goal-oriented
methods. A same-count interval-cache certificate is also tested and fails on
the slow fixture without proving all such approximations impossible.

Bad column mass restores B=Theta(n); forcing a microscopic initial state to
be a singleton multiplies the outgoing-kappa bound by 1024 here. The L2
small-leak promise is stronger than tolerant TV closeness. A forced probe
orthogonal to the residual invalidates the random norm guarantee. All are
preserved as explicit limitations, not generalized limits on cumulative learning.

## Frozen entry points and dependencies

Core proofs: LARGE_AMBIENT_MIXED_CERTIFICATE.md and
QUADRATIC_LEAKAGE_VALIDATION.md. Matrix concentration uses sections 1–2 of
MATRIX_CONCENTRATION_ACQUISITION.md. The separately stated infinity-norm
no-spectral shortcut and microscopic first-action boundary in
NO_SPECTRAL_SHORTCUT_AND_BOUNDARY.md are paper constructions, not the large
fixture's executed algorithm.

Core code: retained_large_acquisition.py, large_routing_source.py,
quadratic_leakage.py, sparse_norm_probe.py,
check_retained_large_acquisition.py. history_sensitive_case.py constructs
the stronger fixture; stream_schedule_predictions.py emits all predictions;
large_strong_comparison.py checks actual-prefix reuse and stronger baselines.

Executable scope: the routing/screening prototype has two actions, n divisible
by four, a nonzero indicator b and a normalized indicator initial distribution.
screen(out,Q) requires a genuine integer Q>=3 and m=2; it is NOT a general
query-list parser for Q<3 or one-action models. replay is a typed scientific
record API, not a hostile arbitrary-JSON parser. It binds caller b, ell, L,
epsilon, confidence and action count. Fixed defaults for the latter two are
the externally defined fixture request delta=1/1000 and m=2, not record values.
The reviewer found missing norm-list and confidence/action-set binding; the
author also repaired scheduled versus actual incoming-half sample totals.
Old verifier bytes and its obsolete receipt are retained under
historical_receiving_pre_repair/, not current admission evidence.

Unmodified imported dependencies (relative to the workspace):
robust_operator_reuse_20261031/finite_observation/robust_replay.py (square-root
rounding and common-denominator integer replay), with imports from learn.py
and verify.py in that parent directory. Their existing exact/finite reviews
retain only their original scope; they do not certify this new composition.

## Nonmutating replay commands

From the workspace, this verifies saved data without changing result files:

```sh
python - <<'PY'
import sys,json,gzip
from pathlib import Path
p=Path('two_rate_operator_acquisition_20261031')
sys.path.insert(0,str(p))
from quadratic_leakage import run_checks as quadratic
from sparse_norm_probe import run_checks as norms
from check_retained_large_acquisition import replay,R
print('quadratic',quadratic()['checks'],'norm',norms()['checks'])
for stem in ['retained_large_4096','history_sensitive_4096']:
    x=json.loads((p/(stem+'_result.json')).read_text())
    data=json.loads(gzip.decompress((p/(stem+'_observations.json.gz')).read_bytes()))
    print(stem,replay(x,data['records'],expected_b=x['task_b'],
        expected_ell_num=x['task_ell_numer'],expected_ell_den=x['task_ell_denominator'],
        expected_length=24,expected_tolerance=R(1,50),
        expected_confidence=R(1,1000),expected_generators=2))
PY
```

This binds the supplied task to the saved public fixture task, not to hidden
truth. A caller with an external task should pass that task instead.

Full regeneration commands are `retained_large_acquisition.py --n 4096
--queries 50000` and `history_sensitive_case.py`. Run them only in a copied
directory tree if preserving current outputs: they write result files.
`stream_schedule_predictions.py` uses exclusive creation and therefore must
also run in a clean copied tree without its old prediction output. No installs
are required (Python, NumPy, SymPy; standard-library gzip). Use the SHA
manifest to identify exact reviewed versions, not filenames alone.
