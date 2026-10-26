# T31 common completion: frozen computational endpoint achieved

All four asymmetric development cases, all six originally frozen released holdouts, and all three controls pass the exact width criterion with rigorously global upper certificates and verifiable lower witnesses. The completed internal proof audits cover arbitrary complex noncommuting effects, all finite reference dimensions, PSD effect boundaries, singular K, the c=1 transition and the exact subunit SDP. No mathematical or rational-verifier gap remained after the audits.

The canonical completion executable is `evaluate.py`; `verify_result.py` independently recomputes the rational PSD tests and witness ratios without a numerical optimizer. `PROOF.md` is the self-contained proof, with precise Schur and dual-sign wording clarified in this round. The frozen proof and scientific implementation are preserved unchanged in `selected/PROOF_ORIGINAL.md`, `selected/evaluator.py` and `selected/verify.py`; SOURCE_PROVENANCE.json and FINAL_SOURCE_CHECK.json record their byte correspondence. Transport checks are provenance, not the scientific proof.

## Exact endpoint evidence

| Case | Certified lower | Certified upper | Width | Incumbent certified upper |
|---|---:|---:|---:|---:|
| D01 | 3.759814109756126 | 3.759814109803115 | 4.699e-11 | 8.47688 |
| D02 | 53.67676197840488 | 53.67676197840734 | 2.469e-12 | 82.756518 |
| D03 | 1.913688669088834 | 1.913688669136547 | 4.771e-11 | 4.588377 |
| D04 | 1.309062245369967 | 1.309062245404667 | 3.47e-11 | 2.987418 |
| H01 | 1.59677132598914 | 1.596771326002502 | 1.336e-11 | 1.956818 |
| H02 | 3.231017425045601 | 3.23101742508799 | 4.239e-11 | 7.636258 |
| H03 | 0.2721194750465545 | 0.2721194777 | 2.653e-09 | 0.438272 |
| H04 | 15.83985259887049 | 15.83985259887856 | 8.07e-12 | 32.080928 |
| H05 | 2.593614207664605 | 2.593614207703167 | 3.856e-11 | 4.348141 |
| H06 | 3.539359156013998 | 3.539359156022936 | 8.938e-12 | 8.482362 |

The table displays decimals; the authoritative endpoints are exact rational strings in RESULTS.json. VERIFIED_RESULTS.json independently checks every upper certificate, lower witness and the rational width test `upper-lower <= (1/50)*max(1,lower)`. The largest width among the ten asymmetric cases is H03 at 2.65344548587e-09. H03 uses the subunit completed-square certificate, so the holdout success does not rely only on the vertex regime.

The identical and constant controls return exactly 1 and 0. The quantum-reference control is certified in [0.3384008430069494, 0.3384008535], width 1.0493e-08, with a noncommuting dimension-two witness. Its supplied scalar search value is a numerical diagnostic, not a substitute for a certified scalar global optimum. Controls diagnose correctness and are not counted as asymmetric endpoint cases.

## General construction and completed audit

The accepted conditional-Umegaki free representation supplies the metric/interface. The evaluator inverts only the denominator quadratic form. A noncommutative block inverse identity and a Schur contraction test convert the desired inequality into a two-by-two covariance polynomial. The singular-K argument is exactly `Z* Z <= cI iff Z Z* <= cI` for `Z=M_K^(1/2) D J_L^(-1/2)`; it requires no inverse of K. This precise argument clarifies an overly broad phrase about products in the frozen exposition, without changing an identity, code formula or certificate.

For c>=1, three rational two-by-two vertex PSD tests are necessary and sufficient. For c<1, completing a square yields an explicit positive operator square plus three PSD coefficient matrices. Three three-by-three LMIs acquire such certificates. An exact Gram primal, explicit strict feasibility and its attained Schur dual prove completeness. The proof applies to complex Hermitian effects in every dimension; it imposes no commutativity restriction. A real active dimension at most two suffices at this interface, followed by the accepted vacuum lift if actual state realizations are desired.

Upper bounds are established by exact rational PSD checks, irrespective of numerical optimizer status. Lower witnesses record rational PSD E_i, G=sum E_i>0 and rational h_i summing to zero. Their genuine free witness is `Q_i=G^(-1/2)E_iG^(-1/2)`, `u_i=G^(-1/2)h_i`; normalization cancels in each inverse quadratic form, permitting exact rational evaluation. Strictly positive channel entries keep every output invertible even at effect boundaries, and the rank of L keeps the denominator positive. Boundary witnesses therefore bound the supremum by continuity.

Two substantive warm-worker audits are complete: worker1/AUDIT_PROOF.md and worker2/AUDIT.md. They independently verify the singular-K contraction step, operator product order, square completion, subunit dual attainment and rational lower normalization. The worker1 audit also retains exact formal noncommuting-coefficient checks and a full-complex PSD-boundary implementation check; these diagnostics support, and do not replace, the universal proof. The worker2 audit replays four already declared singular-K cases through both exact verifiers. No extra fixtures were added merely to increase case counts.

## Comparators and actual resources

The unchanged supplied incumbent was rerun with five full-complex starts, five scalar starts and 90 iterations per start, on the same thirteen inputs. BASELINE_RESULTS.json preserves its full output. Its global upper bounds are shown above; its local-search maxima remain numerical diagnostics. Its total measured process time was 5.41565 seconds. The narrow global guarantee is the completed operation; a search maximum alone is not credited as one.

A stronger conventional comparison was also executed: the lead's general eight-label Gram SDP with a rational dual-residual certificate and exact Gram witness. GRAM_COMPARATOR_RESULTS.json and GRAM_COMPARATOR_VERIFIED.jsonl show that it too passes all ten asymmetric cases and the controls. Its all-case process time was 0.937078 seconds including imports, versus 0.59346 seconds for the selected final run. It uses ordinary Gram/SDP operations and a standard Clarabel solver, so the evidence supports the completed evaluator rather than a unique advantage over every strong standard method. The independently derived worker2 covariance implementation also passes every case; exact congruences and both subunit certificate transformations are retained in worker2/CROSS_CERTIFICATES.json. Every pair of corresponding certified intervals overlaps by exact rational comparison.

Every selected case also ran in its own fresh subprocess; the lead cold maximum was 0.447698 seconds including imports and internal exact verification. Independent replay maxima were 0.483 seconds (worker1) and 0.537 seconds (worker2); worker1 measured preparation plus evaluation plus a separate verifier at most 0.630 seconds. The final thirteen-case batch took 0.66 wall seconds (0.49 user, 0.07 system) and maximum RSS 104,349,696 bytes in FINAL_RESOURCE_DETAIL.txt. Its own process timer is recorded above. These observed costs are far below 300 seconds per evaluation.

The selected evaluator uses the supplied ordinary `/usr/local/bin/python3` environment: Python 3.13.2, NumPy 1.26.4, SciPy 1.17.1 and SymPy 1.14.0. The independent verifier uses SymPy without a floating optimizer. No installation or instance-answer cache is required by the selected method. The lead's optional Gram comparator uses the isolated phase-one vendor directory; its measured uncached installation cost was 6.51 seconds and is preserved separately, rather than omitted from its preparation record. No shared runtime was changed and no model API, paid service, physical action or public write was used.

## Actual failure retained and repaired

The scientific construction passed the released cases unchanged. A targeted generality audit then used a valid, poorly conditioned channel `L=(1-delta)J/3+delta I`, delta=10^-200, with D01 K. Its finite coefficient exceeds binary64 range. The exact rational interval and internal verification succeeded, but optional float display fields became Infinity, which produced non-standard JSON. This was a serialization defect, not a failed global bound. CONDITIONING_FAILURE_INPUT.json, UNMODIFIED_CONDITIONING_RESULT.json and CONDITIONING_INITIAL_FAILURE.json retain the actual input/output and strict-parser rejection.

Only the stage-two driver and verifier-output wrappers were repaired: nonfinite display diagnostics become null, and JSON serialization uses `allow_nan=False`. The exact endpoints, upper certificate and lower witness remained identical. CONDITIONING_REPAIRED_RESULT.json, CONDITIONING_REPAIRED_VERIFIED.json and SERIALIZATION_REPAIR_CHECK.json show strict JSON acceptance and exact equality of those scientific fields. BEFORE_SERIALIZATION_REPAIR_evaluate.py and BEFORE_SERIALIZATION_REPAIR_verify_result.py preserve the original wrappers. The single targeted case is not counted as an endpoint fixture.

The phase-one acquisition failures, broader fallback intervals, prototype failures and resource costs remain in the frozen phase-one evidence; this completion does not erase or reset them. The worker1 audit-helper TypeError and worker2 cross-certificate reporting error are also retained in their completion folders, with repairs confined to the helpers. No scientific evaluator repair was needed for the frozen inputs.

## Replay and remaining scope

From the completion directory:

```sh
cd /Users/harjas/Documents/ChatGPT/coordination/work/astra-method-redesign-20261026/experiments/channel_case/teams/T31/stage2
PYTHONDONTWRITEBYTECODE=1 /usr/local/bin/python3 evaluate.py ALL_CASES.json RESULTS_REPLAY.json
PYTHONDONTWRITEBYTECODE=1 /usr/local/bin/python3 verify_result.py ALL_CASES.json RESULTS_REPLAY.json > VERIFIED_REPLAY.json
PYTHONDONTWRITEBYTECODE=1 /usr/local/bin/python3 baseline_comparison.py
```

ALL_CASES.json consists only of the unchanged seven development/control cases and the six released HOLDOUT.json cases. The two workers' RESULT.md files give exact independent/alternate replay commands. Phase-one source hashes remained unchanged in those replays. All completion writes are in this stage2 directory.

The general evaluator returns rigorously checked intervals and retains a broader valid bound if numerical subunit acquisition fails. A narrow 300-second guarantee over every unbounded rational encoding is not asserted. The specified ten-case width/time endpoint, including all controls and the declared boundary/singular scope, is achieved and internally audited. Historical originality remains UNKNOWN; N965/N970, the supplied finite free representation/refinements and conventional covariance/Schur/SDP operations retain their provenance. No physical validation, generic coherent-input theorem or civilisation-level capability is claimed.
