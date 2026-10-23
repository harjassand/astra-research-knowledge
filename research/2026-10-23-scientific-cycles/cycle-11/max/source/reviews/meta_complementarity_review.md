# Independent review of the Cycle11 scalar complementarity study

Reviewer: `/root/cycle11_quantum`. Date: 2026-10-23.

## Scope

Read `meta_study/complementarity.py`, `meta_study/ANALYSIS_PLAN.txt` and the saved `meta_study/COMPLEMENTARITY_RESULT.json` against the actual owner identities inspected in `reviews/quantum_review.md`. I did not rerun the owner suite or the new study. This review concerns source mathematics, inequality directions, exact-enclosure logic and interpretation. It does not establish independent invention, external novelty or a causal agent-process effect.

## Correct formulas and direction checks

The logarithm interval is valid. With `N=52`,

`ln2 = 2 sum_(j>=0) [1/((2j+1) 3^(2j+1))]`.

After the first `N` positive terms, replacing all remaining denominators `2j+1` by `2N+1` and summing the geometric series gives exactly the code's upper remainder `9/[4(2N+1)3^(2N+1)]`. Its lower endpoint is the partial sum.

The central-binomial closed sums are correct:

- `sum_(j=0)^n a_j = (2n+1)a_n`;
- `sum j a_j = n(2n+1)a_n/3`;
- `sum j²a_j = n(3n+2)(2n+1)a_n/15`, where `a_j=binom(2j,j)/4^j`.

These identities can be checked by telescoping using `a_n/a_(n-1)=(2n-1)/(2n)`. Splitting the owner's defining sums into even and odd walk lengths gives the code's exact `v,c` formulas. In particular, even `j=2m` contributes `2(k-1)m-4m²` to the charge sum, and odd `j=2m+1` contributes `(k-2)+(2k-6)m-4m²`. The direct sum uses the right endpoint `j=k-2`; the 79 checks `k=2,...,80` are correctly counted.

The exact rational square-root assertions give a lower bound on `sqrt2` and an upper bound on `sqrt105`. The same raw square is correctly identified by `s=(ln2/8)b`, because the delivered polynomial factor is `C=I-(ln2/8)bH`.

For `r=1/256`, `b=r/k`, all selected `k>=4` lie in the owner's window. The structured correction allowance is `8 gamma² r³=(ln2)²r³/2` and the generic correction allowance obtained from the offered weighted remainder is `k(ln2)²r²/4`. The affine inward margin is `a ln2 v b²(1/16-2r)`, and the retained target is `a ln2 v b²/128`. Lower affine margin minus upper correction minus upper target is the correct direction for certifying a remaining positive inward margin.

The raw-square drift lower also has correct directions: lower `s²c` divided by an upper `1+s²v` gives a lower charge term; replacing inverse `sqrt2` by the inverse of a lower bound and `sqrt105` by an upper bound gives an upper coherent correction. Subtracting gives a valid lower bound on the complete bulk drift. The positive saved value at `k=131072`, about `3.27039186474547e-7`, therefore certifies outward drift for the stated raw family at this parameter, conditional on the owner's proved operator identities. The negative values at smaller `k` establish nothing about the drift sign.

## Repairs requested from the root

1. **Exact generic-budget exhaustion:** the first source compares `generic_hi` with an upper affine margin. A positive difference of two upper enclosures is not, by itself, a proof that the exact generic allowance exceeds the exact margin. Use `generic_lo=k*ell_lo**2*r*r/4` minus `margin_hi=a*ell_hi*v*b*b*(1/16-2r)` and assert that difference positive. The gaps are large, so this is expected to preserve all conclusions; it fixes the rigorous direction.
2. **Displayed decimal directions:** the first source converts rational bounds with rounding-to-nearest while naming fields `lower` and `upper`. The exact internal sign comparisons remain sound, but a nearest-rounded decimal can lie just outside the claimed bound. Use directed `ROUND_FLOOR`/`ROUND_CEILING`, or explicitly identify displayed decimals as approximate renderings of exact internally compared rational bounds.
3. **Avoid a false factorial interpretation:** the delivered pattern-normalized state includes the positive charge tilt `T`; the raw-square comparator does not. The source-supported comparison remains scientifically meaningful, but normalization is not the sole changed factor in the two complete input states. Describe the study as two complementary-obligation analyses using the same polynomial square, not a fully crossed intervention holding every other state factor fixed. No theorem about all trace-normalized tilted alternatives follows.

The first two requests concern mathematical reporting precision. The third concerns causal scope, not invalidity of the source-derived raw-family bound. Current repaired-source status should be recorded separately rather than silently rebinding this review to changed files.

## Strongest conventional alternatives and what is not excluded

The old cubic and clipping certificates are already successful alternative constructions under the same channel contract; at several fixed parameters they outperform the new conservative floor. A conventional researcher is allowed to derive a sharper state-specific norm bound, use conditional-expectation normalization directly, or choose another feasible input. Exhaustion of one generic sufficient allowance is not a theorem excluding those alternatives.

For Ultra, the ordinary periodic receiver provides useful actual coherent information and is a strong finite-size control; coding the actual preprocessed state is standard distillation machinery. Negative raw coherent information only makes the raw single-letter lower bound uninformative. It does not prove nondistillability or universal necessity of the particular two-step receiver.

The study supports **route-level complementarity** and one **family-level actual obstruction**. It does not prove universal complementarity, superiority of an agent prescription, or an improvement in Astra's invention ability. Its useful new contribution is a sharply scoped finite witness and a quantitative identification of where the delivered proof spends its margin.
