# Acceptance addendum: finite confidence and static-disorder receiving theorem

29 October2026. Actual internal review completion. Scope: Sections5--6, their
calibration/deployment correction, and the synthetic sampling certificate.
This is not external peer review, formal verification or apparatus validation.

Final reviewed proof SHA256:
`c4d9c883fe9fd4eefac93d726e78483519d3d129eb43f4e1d16b7ff087a1d24c`.
Reviewed sampling script SHA256:
`31cc013e74a73dd54c53d57847db0b7834c8ca238dda78d9f45aebd5b5b6ab89`.
Exact versions are retained in this directory with REVIEWED_ prefixes.

## Verdict: ACCEPT at the stated interface

The required calibration/configuration qualification is now explicit adjacent
to the finite-error theorem: freeze the library, or condition on data D and
supply the actual deployment density ceiling given D; independent deployment
is sufficient. Arbitrary further old Z remains permitted. The finite fixed-
configuration-menu alternative correctly pays its entire row sum. This resolves
the exact selection counterexample in the earlier review. The qualification
is explicitly carried into preparation equation(8).

The static-H chain-rule KL argument and the distinction between a positive
Markov reference and a genuinely initialized physical reference remain correct.
The independent source-ensemble requirement for frozen H is explicit. No
retained-history-cardinality factor is needed under those declared premises.

## Synthetic acquisition check

I reran only `sample_rehearsal()` at the saved default seed and N=100000 per
setting, without changing the root output or rerunning population enumeration.
The saved reviewer output is ROOT_SAMPLING_REVIEW_RERUN.json.

The estimator receives visible one-call flip frequencies and two-call return
frequencies. Hidden h is used by the synthetic source and by after-the-fact
population checks, not by the optimizer. Pooling the two visible-label rows
is valid because binary-symmetric conditional dynamics is a WARRANTED
structural premise here. It would not be valid for arbitrary reversible
binary calls with unequal stationary weights or extra unmodeled memory.

There are14 bounded scalar settings:4 flip means and10 return means. The
Hoeffding radius

    eta=sqrt(log(2*14/0.01)/(2*100000))
       =0.0062997518586700284

covers them simultaneously with failure budget0.01 under the iid ideal-source
contract. For g(u,v)=(1-u)(1-v)+uv, each partial derivative has magnitude<=1
on[0,1]^2; therefore the mean-product error is<=2eta. Adding return error eta
gives the valid H-entry radius3eta=0.018899255576010084. This argument also
covers diagonal entries. Each simplex mixture has true mean error<=eta, so
the binary-row mean-square error bound2eta^2 is valid.

The data-selected objective uses a PSD projection, and the selected mixtures
are checked against the ORIGINAL empirical H plus its3eta confidence radius.
Thus PSD regularization is not silently treated as additional data. The two
reference flip targets0.15 and0.30 were fixed beforehand. Independent deployment
is expressly assumed; no same-specimen calibration transfer is claimed.

The replay returns full-record TV bounds:

| Calls | Bound |
| --- | ---: |
| 1 | 0.5068048277887284 |
| 3 | 0.8778117112512728 |
| 100 | 1.0 |

The resource count is1,400,000 independent baseline preparations,
2,400,000 native calls and3,800,000 label reads. The hundred-call certificate
is VACUOUS. This limitation is correctly reported despite good realized
population residuals for some fitted mixtures. Population closeness is not a
replacement for finite-data certification.

The routine uses ordinary floating-point postprocessing and optimization;
there is no interval-arithmetic proof of rounding or a hardware implementation
precision budget. The general theorem separately charges selector and call
errors. The sampling rehearsal is therefore a check of the stated ideal
statistical construction, not an end-to-end apparatus certificate or evidence
of practical advantage. Within that scope, no remaining error was found.
