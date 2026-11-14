# Packaging validation, 14 November 2026

Executed in a disposable copy with Python 3.12.14 on Linux x86_64. All listed subprocesses exited zero:

| Check | Observed wall seconds |
|---|---:|
| Directed four-corner scalar, cubic and quadratic | 0.033 |
| Directed native width-one bare path | 1.344 |
| Native-weight finite geometry/conservation tests | 6.127 |
| Exact q=1/2 flow-conservation diagnostics | 6.009 |
| Independent active-corner enumeration d=1..5 | 1.096 |
| Corrected global-cut default validation suite | 27.922 |

The retained quadratic scaled upper reproduced as
`0.57427315041850698544660451242205191446746981246497392620415310943787422859288017`.

The global-cut default suite recompiled its C++ arithmetic checks, checked exact small cases and reconstructed scalar/convolution certificates from its included large moment receipts. It printed PASS for the marked exp(-6215) upper. **The large R200 magnetic recurrences were not regenerated during packaging.**

A separate exact Fraction check of the thermal scalar returned approximately `1.0931717844078097e-7 < 1e-6`. That assertion is also included in the final portable runner. Small last-digit differences in narrative approximations are not relied upon.

`validation_stdout.txt` contains the original combined run log. Runtime values in original JSON receipts belong to their original runs and were not silently replaced. The portable runner protects those original receipts by working in a temporary directory.

These successful executions do not independently prove the overlap decoder, full source specification, every directed-rounding implementation argument, or the full rare-transition algorithm. No external peer review or physical experiment was performed.
