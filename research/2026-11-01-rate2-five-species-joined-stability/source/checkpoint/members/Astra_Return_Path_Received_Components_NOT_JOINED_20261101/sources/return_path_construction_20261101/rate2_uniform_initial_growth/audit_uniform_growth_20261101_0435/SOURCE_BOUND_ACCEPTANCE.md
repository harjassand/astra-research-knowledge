# Source-bound acceptance: uniform actual initial-growth component

**Verdict: PASS, mathematical component only. No source correction or numerical-constant change is required.**

Accepted exact theorem: `../UNIFORM_FULL_GENERATOR_INITIAL_GROWTH.md`, SHA256 `90a80f12bfc045350b5254a4c8d731f506da5520ee161ccd9e7cbb11df82329e` (6,521 bytes). Author freeze SHA256 `470477675de2d3c2f38ea6fba90bbe06e6b58e455aefecf46044dde4b48f4ffa` (510 bytes), with all three listed payloads independently hash-verified.

For the full 12-channel rate-2 count chain, fixed reference integers N,m>=1 with N>=10^8(m+1)^2, M=A+min(C,D), and every initial state with B>=N/2 and M<m, this review earns:

- The actual-generator inequality LV<=-V/4 for V=2^(-M)[1+16 A^2 phi(M,R)/N], with the SAME V at enabled exit targets.
- Exact min/cutoff-corner treatment, all positive zero-M correction costs, core capture and outer-return payments, including arbitrarily large B/R and odd reference N.
- For the first actual sigma hitting M>=m OR B<N/2, E[exp(sigma/4)]<=2^m V(x)<=(101/100)2^m. Consequently sigma is almost surely finite and P(sigma>8m)<=(101/100)exp(-m).

The crucial lower bound V>=2^(-m) holds throughout t wedge sigma, including finite-jump targets. Localized stopped Dynkin, Fatou, and monotone convergence establish the moment without assuming sigma finite in advance. Constant-rate immigration and internal population conservation establish nonexplosion. N is a fixed reference, not the moving population.

**Scope limitations:** The output is M hitting or B-half exit, not activation or population removal. There is no total-population-band stop; any consumer needing one must account for it separately. AB->CD can produce the B-half exit while conserving population. The M hit supplies neither balanced E/C-D nor a small fast-A share; the accepted dyadic stage and any removal/recurrence/stationary-moment consumer remain separate. No numerical probability receiver, physical preparation/acquisition, or runtime resource-budget API is accepted.

Evidence: `MATHEMATICAL_REVIEW.md` contains the independent uniform derivation. The separately entered exact checker passed 658,415 assertions across 7,360 states and 59,532 enabled jumps (18,394 terminal checks), without importing author code. These finite checks supplement rather than prove the uniform result. A copied-tree author replay reproduced its 6,675-state/58,680-jump report byte-for-byte. No original file was edited and no external source was used.

`AUDIT_SHA256.json` is the controlling payload allowlist; `verify_saved_audit.py` performs read-only readback. Copy this directory before rerunning either check script, which writes adjacent results. This receipt does not subsume any earlier or later component acceptance.
