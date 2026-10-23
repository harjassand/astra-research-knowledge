# Exact finite diagnostics and observed limitations

The principal personally wrote and executed code/exact_checks.py.
EXPERIMENT_CONTRACT.md and the source hashes were frozen in
evidence/PREEXECUTION_FREEZE.json before the first execution at
2026-10-22T04:51:24.064334+00:00. The first run passed; no repair,
parameter selection, stochastic simulation, or earlier suite was run.

## Results

| Check | Count | Meaning |
|---|---:|---|
| Local weighted energy, exact LDL | 128 | All-vector quadratic inequality on frozen finite inputs |
| Mixed absorbed weighted energy, exact LDL | 128 | Actual global killing, local diagonal, boundary weight |
| Absorbed first-hit versus independent decomposition | 384 | All first-hit times through N=1,3,7 |
| Original full-return decomposition | 16 | Original C after every hit, n=8,N=3 |
| Native tree configurations | 8 | Both mismatch signs and their matched controls |
| Native/quotient full-law TV equality | 24 | Fourteen native states before quotienting |
| Capture and retention bounds | 24 | Actual mixture choices and whole terminal union |
| Same-input pure-IMH bounds | 24 | Full-return comparison, not cost equivalence |

The energy fixtures use five states and two nonreversible proposals.
The 128 cases include 64 tau=0 envelopes, 16 interior scalar maxima,
and 48 endpoint maxima. Both zero and positive finite killing deficits
occur. All checks use exact Fraction arithmetic and reconstructed LDL
factors; floating positivity or normalization is not an acceptance test.

The native tree uses R=9/4, ceil R=3 and depth two, hence 14 states including
the core. Native reverse-proposal ratios, both outgoing row budgets,
per-state screens, actual backward acceptance, and terminal-union holds
are verified before lumping. The rational KL upper bounds are 3/8 for
coalescence and 73/128 for expansion, each below K=1.

## Numerical limitation that is retained

All 24 conservative finite TV lower bounds are nonpositive at these
deliberately small fixed fixtures. They do not numerically certify the
asymptotic positive floor. The marked capture event has positive exact
probability, and its comparison with the full terminal probability is
nontrivial and checked. The asymptotic floor is a theorem from the
moving family, not a pattern extrapolated from these matrices.

At horizon 16, for example, the mismatched coalescing fixture with
alpha=1/2 has TV approximately 0.04969181 versus ordinary G's
0.03871634. The expanding fixture with the same alpha has hybrid TV
approximately 0.05687680 versus G's 0.05895847. These differing
finite comparisons were not optimized or used to claim a sampler
ordering. Exact rational values, every other selected outcome, and
the matched controls are in evidence/exact/EXACT_RESULTS.json.

The fixture target mass p=1/16 is a rational identity-check input.
It is not the asymptotic entropy allocation p_n=1/[log(n)^2(1+V_n)].
No native graph larger than 14 states was materialized.

## Reproducibility and resources

Run from the source root with Python 3 and assertions enabled:

python3 code/exact_checks.py --output-dir /tmp/pro3_cycle8_replay

All mathematical inputs and results are deterministic; resource times vary.
The portable replay entry point also verifies the manifest and exact
deterministic JSON digests without rerunning any predecessor campaign.

Initial diagnostic body:
- energy: 0.593171924 wall seconds, 0.591426755 CPU seconds;
- native trees: 0.203918566 wall seconds, 0.203924584 CPU seconds;
- combined: 0.797103309 wall seconds, 0.795355455 CPU seconds;
- process peak RSS: 14,080 KiB.

These readings exclude output serialization, later replay, source retrieval,
proof construction, interpretation and model inference. They are not
discovery costs. Total inference, token, monetary and research costs
are unavailable and remain unknown.

Deterministic input SHA256:
55c3c8810d481e4860c0a98705d582f296ebd0b2ed7b4ac3388b518638a1752d

Deterministic result SHA256:
a85128ae4be3590d4dc52a2fd7e4590d237e8f9752e2c6374c614f97b5e8dce3

