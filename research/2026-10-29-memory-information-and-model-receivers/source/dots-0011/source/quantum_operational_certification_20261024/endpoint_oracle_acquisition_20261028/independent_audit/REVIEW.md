# Independent endpoint-comparator review — 28 October 2026

**Disposition: accepted at the scoped mathematical and exploratory simulated-data level described below.** This review is independent of the author and does not approve the separate noisy clocked encoded experiment. Originals are unmodified. Run `python independent_audit/check.py` from this folder, or supply its full path. NumPy is the only nonstandard dependency.

## Mathematical obligation

Use PTM convention M_ab = Tr(P_a N(P_b))/2, ordered I,X,Y,Z, column input and row output. Composition is left matrix multiplication. For trace-preserving qubit channels, F_e(D N)=(1+Tr(B A))/4, where A and B are their linear Bloch parts. Translations do not enter this maximally mixed input entanglement-fidelity objective; they do matter for the channel and measurement probabilities.

For a decoder with Kraus K_j, spin flip S(X)=Y X^T Y gives S D S with Kraus Y K_j* Y. This is CPTP, with linear part B and translation opposite to D's. Averaging these maps produces a unital decoder with identical objective. Proper input/output rotations diagonalize its linear part; positivity of its Choi matrix gives the four nonnegative Pauli-mixture weights. Undoing rotations makes it a mixture of unitaries. A linear objective cannot exceed the largest unitary term. This establishes the reduction over **all CPTP terminal decoders**, not merely a restricted decoder ansatz.

For A=U diag(s1,s2,s3) V^T, s1>=s2>=s3>=0, the proper-rotation solution is B=V diag(1,1,det(VU^T)) U^T. Thus F*=(1+s1+s2+det(VU^T)s3)/4. The determinant sign correction is essential (e.g. the universal-NOT channel). Rank deficiency causes no value ambiguity. The author's formula and multiplication orientation are correct.

Primary source checked directly: Karimipour, Benatti and Floreanini, *Quasi inversion of qubit channels*, arXiv:1909.06118v5 (5 October 2019), https://arxiv.org/html/1909.06118 . Theorem 1 and supplementary proof A establish the unitary reduction; equation 17 gives the equivalent average-fidelity objective. This review relies on those results and the direct proof above, **not** the paper's separate Remark 1/Remark 3 about canonical transformations. No new-theory claim is warranted for this endpoint oracle.

Independent numerical checking uses a 4x4 real symmetric quaternion objective and its largest eigenvalue, not the author's SVD implementation. This agrees with all saved oracle and fitted-matrix optimum values. It supplements rather than replaces the analytic global proof. No SDP package was available or needed.

## Native channels, leakage and acquisition

The independent program rebuilds the five Kraus channels from declared rational stereographic axis/frame constants and amplitude-damping constants using NumPy. A native operation is V A K_j A†: damping along a rotated axis followed by a fixed output rotation, not damping with its output frame automatically removed. V2 applies (D_z M_native)^T, with D_z=diag(1,exp(-strength),exp(-strength),1), and no learned inverse. The two-unit native/control window is retained even when its control is identity.

The source generator necessarily knows the channel to produce probabilities. The learner `fit(counts)` does not receive that truth, damping strengths, axes, frames or source-derived selection. It takes 18 rows of binary counts for six Pauli preparations crossed with three Pauli measurements, estimates each linear Bloch entry from opposite-input differences, and solves proper Procrustes. Translation cancels in that estimator, but is correctly included in the generated Born probabilities. Fitted matrices need not be CPTP; the synthesized proper rotation always is.

All saved counts reproduce exactly as seeded binomial aggregates. This is provenance for **simulated ordinary binary experiments**, not acquired laboratory observations, and not an event-by-event native trajectory record. Independent source reconstruction agrees with saved endpoint PTMs. Counts cover 426,240 V2 binary trials and 568,320 V1 trials. No author fitting implementation is imported by the checker. Maximum discrepancy across 2,030 numerical comparisons: approximately 1.42e-14, ordinary floating-point evidence rather than outward-rounded certification.

V1 retains inherited per-round acquired inverses. Its endpoint budgets are additional, not standalone total costs. The selected frame alone needed 4,096 shots/site =20,480 native exposures; the actual prior two-bank calibration used102,400, and the prior full experiment including holdouts used2,068,480. The amended scope and clock-cost records correctly retain these distinctions. One should not charge all historical holdouts to every conceivable new implementation, nor erase the actual historical cost when describing the completed experiment.

V2 has zero inherited inverse-training charge. At T=32, 128 endpoint shots/site across five sites cost20,480 native uses; 640/site cost102,400. Each scenario/budget/horizon is a separate counterfactual experiment. Their costs cannot be pooled into one advertised budget.

## Selection and what the scores mean

All five sites are retained. Each per-site decoder is selected from its own counts, without source-based correction or selection. Printed minimum and maximum infidelities are **posthoc descriptive source-scored ranges**, not the performance of a learner-selected site. No site-choice protocol or statistical selection guarantee is established. In particular the oracle-best site is source-informed.

The plan file and code order fix all scenarios, horizons, budgets and seeds before that run's draws; exact replay and author manifest hashes match. These artifacts do not independently prove absence of prior explorations or seed searches. Acceptance is consequently **exploratory**, consistent with the plan's explicit status, not preregistered or confirmatory. True scores have no acquired confidence bounds or held-out validation here.

## Time and comparator scope

Default channel-window duration is203T reference units per endpoint shot (201-unit background window plus2 native/control units). At T=32 this is6,496 per shot. The low-budget experiment costs4,157,440 aggregate carrier-time units, or831,488 under ideal simultaneous five-site acquisition; the high budget costs20,787,200 aggregate, or4,157,440 ideal parallel units. These numbers exclude endpoint preparation/readout and terminal pulse overhead. They are not complete laboratory wall-clock costs. Equal native-use budgets alone do not equalize time, gates or hardware.

The full-CPTP oracle is an exact source-informed ceiling **for a fixed endpoint channel and one terminal qubit decoder**. It does not optimize intermediate controls, additional quantum storage, joint processing, adaptive instruments, or changing the physical noise generator. V2 is a feasible conventional data-only alternative within its trusted ideal-control model, not the optimum over all such strategies. The source-informed oracle is not a learned decoder.

Noiseless ancillary bypasses would invalidate a general passive-memory superiority interpretation; mandatory native-channel-use tasks and a separately specified eligible storage-register set must be retained. This review does not establish the correctness of the parent clocked encoded implementation, comparative encoded advantage, hardware performance, or universal preservation under arbitrary unknown noise. It does establish that the old fixed-inverse-only baseline was too weak to represent optimal terminally corrected unencoded performance.
