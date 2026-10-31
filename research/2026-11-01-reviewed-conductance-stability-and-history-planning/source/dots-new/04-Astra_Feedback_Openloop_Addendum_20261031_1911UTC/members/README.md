# Separate reviewed addendum: feedback versus every open-loop schedule

This small local addendum does NOT change the accepted feedback archive.
The separate conditional PASS is bound in INDEPENDENT_OPENLOOP_REVIEW.md
(SHA15c9a95a96d28639d4347460de3b6c74a2baec48c3ce72941f512d7c51689778).

All 16,777,216 length24 retained-model open-loop schedules were exhaustively
checked with bounded-grid uint64 arithmetic. Their coarse optimum is at
most0.3773533192; the learned feedback policy has coarse value0.6244843519.
Using the SAME accepted polynomial feedback error for both yields a true
expected-value advantage of at least0.2183264200 on that good event.
This is a distinction between open-loop and observed-block feedback, not a
new DP algorithm or an end-to-end acquisition superiority result. Feedback
requires the explicit-state simulator's label/map interface.

Paid comparator cost:536,870,880 scalar products; rounding and uint64 overflow
are bounded. All557 exact backend/regression checks passed. The resource
field bounds bulk arrays, not total RSS/internal-library scratch. Historical
short-horizon output and peak-temporary defects are retained and marked
obsolete. Shorter-horizon calls now return null same-horizon gap fields.

## Dependency and reproduction

Extract this addendum alongside the contents of
Astra_Acquired_Feedback_Planning_20261031_1904UTC.zip
SHA256 c92b777c3edfc2fef64fa2fa8ae0aea2b40b0fa5eb16eb582830e55b3f07502d.
The directory layouts merge without replacing any existing scientific file.
This addendum consumes the already received model certificate and does not
independently authenticate/replay its statistical provenance.

```bash
export PYTHONDONTWRITEBYTECODE=1
python - <<'PYTEST'
import sys
sys.path.insert(0,'two_rate_operator_acquisition_20261031/feedback_postfreeze_openloop')
import exhaustive_openloop, check_exhaustive
print(exhaustive_openloop.run())
print(check_exhaustive.run())
PYTEST
```

Local-only; no upload. No caches/logs, ongoing prior analysis or unrelated
branch files included. SHA256SUMS binds all payload bytes.
