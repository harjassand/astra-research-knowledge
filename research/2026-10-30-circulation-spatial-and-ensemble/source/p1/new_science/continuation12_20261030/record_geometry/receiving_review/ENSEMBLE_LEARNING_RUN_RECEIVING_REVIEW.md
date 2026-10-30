# Receiving check of the executed finite-instrument learner

30 October 2026. Focused actual-code review by the existing record-geometry
role. No large simulation was rerun, no new fixture was added, and no
previous proof or independent alternative was edited.

## Exact inputs and decision

The following bytes were read and copied unchanged into the adjacent
ensemble_learning_run directory. Each snapshot filename includes the first
twelve characters of its SHA-256.

| Input | SHA-256 |
|---|---|
| verify_ensemble_echo_learning.py | e58cc44b7352bb0d03a38d55c10baa0118e56f8ffb5d13ec97cd40df83864539 |
| ENSEMBLE_ECHO_LEARNING_CHECK_RESULTS.json | 7f031fd196772d9dd237b511b8c15e1fe4dbb0e1b6331c05f2ff8c9d840c821d |
| ENSEMBLE_ECHO_EXECUTED_OUTPUT.txt | b998f89a4559f807b3252a38f5f7b961a9b7178795b80e632784d017e7ba1336 |
| BINDING_RECEIVING_CLARIFICATIONS.md | 5bd97a3c721dcc633153a1394fea3e6693faddebe267c00cb1030566b844227d |

**Decision:** receive the implemented raw finite-instrument report,
pilot/fresh-validation separation, acquired-normalizer confidence and
sampled certificate at their simulated interface. The resource ledger is
consistent with the executed program. One binding interpretation requires
correction: the final paragraph of clarification Section 4 cannot add
0.01 to this one observed, data-dependent certificate and thereby obtain
an unconditional joint-calibration bound of 0.13025862798364492. Section 5
below gives the exact correction and a concrete fixed-threshold deployment
rule. Root has accepted this correction.

The script's embedded hash equals the actual reviewed script hash. The
saved stdout validation and ledger fields equal those in the results JSON.
Recomputing the reported confidence arithmetic and integer counts from
those saved fields requires no simulation; those checks also agree.

## 1. Raw prefix and reverse-prefix report

The synthetic physical state has eight values. Its visible label is one
bit. The six supplied kernels are symmetric stochastic matrices for the
uniform baseline, including deterministic involutions and fixed-time
Markov semigroups. The matrix data are used by the synthetic transition
supplier and, later, by the explicitly separated population assessment.
The scalar-report selection and validation stages do not read their
entries or any hidden output density.

Let P be the chronological four-call prefix S,C,A,T and let M_r be the
projection onto its terminal visible record r. The actual instrument is

\[
A_r=P M_r,\qquad A_r^*=M_rP^*.
\]

The code's echo_report executes exactly:

1. Draw a fresh baseline state and read \(g(Y_0)=1_{\{Y_0=1\}}\).
2. Execute P, then read and retain its real terminal label r.
3. Execute the selected u_r and then the reversed v_r.
4. Read whether the present label equals the stored r.
5. Execute the reversed prefix and read the final g.

Its literal scalar report is

\[
Z_{uv}=\frac{g(Y_0)\,1_{\{Y_{\rm middle}=r\}}\,
                   g(Y_{\rm end})}{q_r},
\qquad q_0=q_1=\tfrac12.
\]

The location of the middle check is correct: it implements M_r before
P* in the adjoint branch. Executing it after the reverse prefix would
implement a different instrument. The observed forward branch supplies
its probability once; the code does not multiply that probability twice.
It also does not draw a second state conditional on the stored r.

Writing \(a_r=A_r^*g\), the expectation is precisely

\[
\sum_r q_r^{-1}
 \langle g,A_rP_{u_r}P_{v_r}^*A_r^*g\rangle
=\sum_r q_r^{-1}
 \langle P_{u_r}^*a_r,P_{v_r}^*a_r\rangle.
\]

Every report lies in [0,2]. The reversed prefix still executes when
the middle check fails, and those calls are included in the ledger.
The model supplies exact noninvasive label readings and independent
fresh transition noise; this run does not experimentally establish those
physical suppliers.

## 2. Pilot selection and fresh validation

The finite policy library, q weights, candidate lengths and prefix are
fixed in the code. The pilot uses one reference diagonal and two entries
per candidate, with 12,000 fresh baseline trials per entry. Its selected
policy is DD_A on both retained-record branches, chosen using scalar
sample means and the declared number of post-prefix calls.

The factor four in the pilot's nominal_D_estimate is a fixed nominal
scaling used for a heuristic threshold. It has no confidence status.
It is not the normalization used by the final certificate. Arbitrary
pilot heuristics are permitted because the selected policy is then frozen
before the independent validation stage. Negative pilot distance estimates
are sampling errors, not population zeros or certified exact matches.

Validation uses a separate random stream and newly sampled baseline
states: 200,000 normalization readings and 1,200,000 trials for each of
the selected diagonal, reference diagonal and cross entry. No population
assessment is consulted to select a policy, to choose q, to reduce a
confidence radius or to decide the reported pass flag.

The confidence statement belongs to the mathematical model of independent
baseline and transition samples. A fixed seeded simulation is a reproducible
realization under that model; one run is not an empirical verification of
99% coverage or a hardware qualification of fresh conditional sources.

## 3. Unknown global normalization

The raw input is g in [0,1]. The learner's final certificate does not
substitute the population value \(Z=\mu g=1/2\). Instead it estimates Z
from fresh baseline readings and uses

\[
Z_-=0.50011-
\sqrt{\frac{\log(2/0.0025)}{2(200000)}}
=0.49602202625752445.
\]

Each of the three raw echo means has range two and radius

\[
r=2\sqrt{\frac{\log(2/0.0025)}{2(1200000)}}
=0.003337816583653633.
\]

Allocating 0.0025 failure probability to each of these four events gives
total failure at most 0.01. No independence among the four events is
needed for their union bound; the program nevertheless uses disjoint
fresh draws. With the sampled raw distance
0.0008816666666666695, the certificate is

\[
D^+=
\frac{\max\{0,\widehat D_{\rm raw}+4r\}}{Z_-^2}
=0.05784855041803483,
\]

\[
\eta(C)=\tfrac12\sqrt{D^+}
=0.12025862798364492.
\]

The radius uses the raw [0,2] range and the normalization is applied only
after bounding the nonnegative three-entry numerator. These are the
correct operations. The certificate passes the fixed requested tolerance
0.16. Conditional branch probabilities p_r are neither inserted nor
estimated; q supplies the joint-objective weights.

## 4. Exactly which records and costs are represented

The retained deployment record R in this program is the single terminal
visible label of the four-call prefix. It is stored before either later
word and used to select the corresponding reference and candidate branch.
The matrix population assessment sums the unnormalized density differences
separately over r, so it checks the joint R-and-state law, not the marginal
state obtained by erasing R.

There is no intermediate prefix sensing, recorded selector key or random
completion-time record in this fixed-call synthetic instrument. Extra
accessible physical records are not qualified by silently adding them
to the name R. In particular, candidate and reference command logs differ:
three post-prefix calls versus six. Binding clarification Section 4
correctly excludes those different preparation logs from the receiver
unless their joint laws or actual isolation/reset are separately supplied.

The raw echoes start from mu and need no rejection preparation of g mu/Z.
A later deployment input g mu/Z remains an actual additional source
requirement. Here fixed-label rejection from independent mu specimens is
an allowed ideal supplier, with its accepted label fixed and its failed
trials independent of the accepted state under that interface. The run
does not execute or price a complete future deployment/rejection cycle.

The integer operation counts reconstruct as follows.

| Quantity | Pilot | Fresh validation | Total |
|---|---:|---:|---:|
| Echo trials | 348,000 | 3,600,000 | 3,948,000 |
| Separate normalization trials | 0 | 200,000 | 200,000 |
| Baseline preparations | 348,000 | 3,800,000 | 4,148,000 |
| Kernel calls | 5,592,000 | 61,200,000 | 66,792,000 |
| Visible readings | 1,392,000 | 14,600,000 | 15,992,000 |

The pilot has 29 entries. Each echo has four visible readings. In fresh
validation, the selected diagonal, reference diagonal and cross each use
respectively 14, 20 and 17 calls, counting both copies of the four-call
prefix. These formulas reproduce the JSON ledger exactly.

The selected policy uses three rather than six calls **after** the common
prefix; including that prefix gives seven versus ten. This is a count of
supplied fixed calls, not an asserted ratio of complete apparatus cost,
duration or work. The stated ledger limits properly leave preparation/
reset work, physical sensing errors, communication, clocks and thermal
source capacity unpriced.

## 5. Binding correction: random certificates and whole calibration laws

Let C denote the random complete calibration history, delta(C) the true
conditional deployment/reference TV, and eta(C) its reported upper bound.
The successful confidence event guarantees

\[
\delta(C)\le\eta(C),
\qquad \Pr(G^c)\le\alpha.
\]

Attaching the same random C to the two physical laws gives

\[
\operatorname{TV}_{C,R,\mathrm{later}}
\le \Pr(G^c)+E[1_G\eta(C)]
\le \alpha+E[\eta(C)],
\]

with the usual cap at one. It does not give alpha plus the numerical
eta obtained in one observed calibration realization. Consequently
0.13025862798364492 is not established as an unconditional joint-C
bound by this executed run.

A concrete repair already fits the supplied learning interface. Fix
epsilon=0.16 before observing the validation data. Execute the selected
replacement only when its certificate passes that threshold; otherwise
execute the unchanged reference. On G every resulting replacement error
is at most epsilon, and a reference fallback has zero replacement error.
The valid unconditional joint-C bound is therefore

\[
\operatorname{TV}_{C,R,\mathrm{later}}\le0.01+0.16=0.17.
\]

The reviewed code computes the pass flag but does not execute a subsequent
physical deployment. The fallback must be stated as the deployment protocol,
not claimed to have been experimentally executed in that original run.
Alternatively retain only the valid 99%-confidence, data-dependent
certificate for the selected conditional law, or prove an expectation
bound on eta(C).

The printed value 0.12025862798364492 and its 99% confidence statement
remain valid. The correction concerns only the additional unconditional
interpretation in the reviewed binding note. Root accepted this finding
and supplied the separate correction and deployment wrapper reviewed
below.

## 6. Population identities remain separate

The population assessment begins only after selection and validation.
It uses the hidden matrices and the exact fixture normalizer to compute
the full joint output densities. Its reported selected TV
0.03727712878289022 is a population-model check, not an acquired estimate.
The echo and witness algebra residuals, about 3.27e-16 and 2.23e-16,
are floating-point population identities.

Likewise, withheld_full_state_receiver_gap is computed by summing the
positive part of the full hidden density difference. It equals the
population TV as it should. It is not an executed newly supplied
microscopic sensor. literal_witness_max_residual checks the mathematical
response formula; the program does not separately sample the physical
randomized witness experiment.

The retained-key failure numbers are analytic values placed in the
results object, not extra sampled trials. Their placement outside the
training data is correct. The source/program structure and the result
labels support these distinctions; promoting them to additional physical
acquisitions would require additional operations and their real costs.

At this scope, the executed run implements the intended finite-instrument
learning calculation correctly. The only load-bearing correction found
is the whole-calibration interpretation in Section 5.

## 7. Actual correction and first deployment wrapper

The following additions were read and snapshotted in the same directory.

| Input | SHA-256 |
|---|---|
| CALIBRATION_HISTORY_CORRECTION_AND_DEPLOYMENT_RULE.md | ca5265f054fc0cc0683c450c2f9c1bdb8d80e515e831628000456ec662ac94d0 |
| export_qualified_deployment.py | 45ae79959b3ea0444ab7a8fe208dfe2c483f284d50bf10178354ad4695800969 |
| QUALIFIED_DEPLOYMENT_RULE.json | 56268a534ccf8dea7fc426120b97a2eb87cf61a37595c89d400a0de7fc43eb8a |

The correction now gives the required expectation formula, rejects the
observed-bound substitution, and states the fixed 0.16 gate with reference
fallback and unconditional bound 0.17. Its repeated-use bound
min(1,0.01+0.16J) is valid under the stated fresh conditional inputs.

The first wrapper reads the preserved acquired result without sampling
or reseeding. Its finite nonnegative gate comparison selects DD_A on
both branches in this actual saved run. Its exported source hash equals
the reviewed results JSON hash; the exported script hash equals the
reviewed wrapper hash. The post-prefix execution function invokes only
the supplied operation call port, in the selected chronological order.
No new initial source, microscopic sensor or physical execution is claimed.

One total-protocol edge was referred to root: the preserved original
learner can abort before producing a result, for example if the pilot
qualification list is empty or the normalization lower-bound assertion
fails. The first wrapper handles a finite/nonfinite numerical certificate,
but not None or an absent result. To make fallback literal on every
calibration history, unavailable or aborted qualification must also
dispatch to the supplied reference. This does not change the observed
successful run or require new validation.
