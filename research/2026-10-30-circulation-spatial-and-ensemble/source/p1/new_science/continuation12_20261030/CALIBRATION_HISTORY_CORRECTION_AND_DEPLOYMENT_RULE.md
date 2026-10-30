# A realized confidence bound is not a fixed joint-calibration bound

30 October 2026. Binding root correction from the existing record-geometry
role's actual code/record audit. This note supersedes the last numerical
paragraph of Section 4 in `BINDING_RECEIVING_CLARIFICATIONS.md` as originally
written. Its claim of an unconditional bound 0.13025862798364492 was wrong.
The original reviewed bytes and the actual receipt are preserved.

## 1. What the executed validation actually proves

Let C be the complete random calibration history, including the pilot,
fresh normalizer samples and fresh echo samples. The algorithm computes
a data-dependent upper confidence bound eta(C). Under the actual
conditional source assumptions, there is an event E with probability at
least 0.99 on which the selected preparation's conditional joint
(retained prefix R, physical output, common later receiver) TV is at most
eta(C). In the one executed simulation,

    eta(C_observed) = 0.12025862798364492.

This is a valid 99%-confidence certificate for the selected law. It is
not a deterministic bound eta(C)<=eta(C_observed) on every successful
calibration history. Attaching the same complete random C to both output
laws requires integrating the actual conditional error over all C:

    TV_joint <= P(E_complement) + E[1_E eta(C)],

with any appropriate cap at one. One observed eta does not evaluate that
expectation. Adding 0.01 to this one observed value cannot justify the
claimed unconditional 0.1302586 bound. No sample or numerical identity
in the underlying run changes because of this correction.

## 2. A concrete valid deployment rule

The original executable declared the requested tolerance 0.16 and the
confidence level 0.99 before fresh validation; it reported pass/fail but
did not implement deployment. Complete the protocol with this fixed rule:

* If the acquired eta(C) is finite and at most 0.16, deploy the selected
  candidate after the actual common prefix.
* Otherwise execute the reference on every retained-prefix branch.

The fallback also covers unavailable or aborted qualification: an empty
pilot-qualified list, a nonpositive normalizer lower bound, or no completed
validation record. The original learner can stop at these cases. The
completed dispatch defaults to the declared reference instead of assuming
every calibration produces a certificate. `choose_policy` accepts an absent
bound and returns the reference, and the export dispatcher handles a missing
or incomplete result. The initial narrower wrapper and its successful
export are preserved in `development/`; this completion changes no sampled
calibration output and requires no new validation.

The fallback introduces exactly zero replacement error for failed
validation, including bad or nonfinite normalizer outcomes. On E the
conditional error of this completed protocol is therefore at most 0.16
for every C. On E_complement it is at most one. Consequently

    TV((C,R,later)_deployment, (C,R,later)_reference)
       <= 0.16 + 0.01 = 0.17.

The reference side carries the same calibration law and record C, and
uses its reference preparation from the same actual conditional input.
This theorem does not condition an old correlated specimen into that
input. The branch, timing and apparatus qualifications in the other
binding note remain unchanged.

The observed run passes the fixed gate, so its deployed post-prefix word
is D,D,A. The reference is D,B,D,B,D,A when R=0, and B,D,B,D,B,A when R=1.
The script `export_qualified_deployment.py` implements and exports this
literal fixed-gate selection rule using the preserved acquired result.
It does not rerun, reseed or select additional validation experiments.
It does not claim that a physical device has been built or executed.

## 3. Repeated uses and tighter bounds

For J fresh conditionally qualified uses after the same calibration,
the fixed-gate protocol has the conservative unconditional bound

    min(1, 0.01 + 0.16 J).

Calibration failure is paid once, while the qualified per-use errors add.
Neither this bound nor the successful single-use numerical certificate
promises useful accuracy for arbitrarily many substitutions. A tighter
joint bound would require a predeclared smaller gate, an acquired valid
bound on the relevant expectation, or another proved composition result.
Retrospectively declaring this run's observed bound to have been the gate
would not be valid. The much more general all-common-future result still
covers an arbitrarily long continuation **after one substitution**.

## 4. Status

This is a real correction to a retained-calibration numerical claim.
The population echo identity, finite-instrument operation, independent
fresh-validation confidence, selected three-call recipe, actual sampled
ledger and information-cost theorem remain valid at their stated scopes.
The saved result and handoff use 0.17 for the complete calibration-record
comparison and label 0.1202586 as the observed 99%-confidence certificate.
