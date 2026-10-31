# Final source binding: reset-free sign epochs

I reread the complete updated RESET_FREE_SIGN_EPOCH_COMPILER_CANDIDATE.md and verified SHA-256 2c5eeb3c5c9d957022425987a32200bdbaa1d3c579cbf0aef868b165e61fa298 on 2026-10-31.

The two qualifications from the independent review are now explicit in the source:

1. Old private sign/controller registers cease controlling subsequent hardware. Retained correlations are allowed only with registers that are then idle or traced; hiding an old bit from the user alone is insufficient.
2. Certified rational bounds b, ell and d determine C1 and C2 consistently, making tau0=b ell/C1 an exact rational threshold. A smaller implemented cap must charge the actual number of epochs or redo the ceiling bound; the coefficient 19 cannot be retained for free.

These additions close the stated operational and scheduling qualifications without changing the mathematical error constants or output scope. The scoped PASS therefore binds this final source version. The earlier full receipt RESET_FREE_SIGN_EPOCH_INDEPENDENT_REVIEW.md, SHA-256 770b1b57767832a1150b13a41827209eff757d6ead1ffdccd4b4cb4d2c5c299c, remains unchanged and records its original source binding. This note extends that receipt only to the fully reread final source above.

No bath reset, retained-source approximation, free sign-setting access, practical advantage, or novelty claim is added.
