# Information, action and cost contract

Theorem hypotheses are exact: finite labelled positive pi,q, population
D(pi||q)<=K>0, fixed alpha in (0,1), proposal-q initialization, reciprocal
target-independent row-stochastic Q under the public asymmetry bound A_n,
and fixed-within-run eta_n,kappa_n. Support may grow across horizons.

The sampler may draw q candidates, propose from Q and evaluate the forward and
reverse Q probabilities needed by the actual acceptance rule. The target is
evaluated up to a common unknown normalizer. q values, random uniforms and
cached evaluations may be used. No full target table, normalizer, independent
KL estimator, off-contract index service or exact arithmetic at zero cost is
supplied. Population K remains a supplied promise even on an easy null.

The theorem counts transitions of the actual lazy mixture, including rejected
attempts, global moves and every return. An absorbed process appears only in
proofs of first-hit mass. The new counter that replaces rare transitions by
holds is also a calculation with an explicit coupling error, not a changed
sampler or a free operation.

Proposal, target, forward/reverse probability evaluations, random sampling,
index generation, storage, caching, setup and numerical precision all retain
their actual resource costs. No cost-equivalence between a local and global
step is asserted. Comparing pure G at floor(alpha n/2) is a transition-law
comparison; it is not a matched wall-time or target-call benchmark.

The two-sign native construction's Q depends on public policy, K,alpha,n and
labels before any target observation. Targets are then supplied by the proof.
This meets target-independence; it does not allow target-adaptive Q. Its support
size is 1+sum_{i=0}^J M^i, with potentially enormous M and J. No such full graph
was materialized in this checkpoint. Formula calculations on a proven quotient
or control model do not reduce an actual sampler's native costs for free.

The complete-level lumping map applies to the full distributions and terminal
unions used in the construction. It is not a certificate for a new arbitrary
within-level subset's first-hit or return law. The evaluator's different
observation query is preserved as a scope warning, not rerun or called an error
in the original complete-level statement.

All principal theorems use exact-real arithmetic. The auxiliary precision note
specifies separate error models. Reciprocal-consistent screen error with an
exact target correction is different from coherent error in the target itself.
Neither an abstract edge-error bound nor a log-target oscillation bound is an
implementation theorem for a concrete floating-point evaluator. Obtaining an
error certificate and paying the evaluation/precision costs would be required
for an operational extension.

The ordinary comparator gets the same information. Analytic direct sampling
and complete enumeration are legitimate if the recipient actually has the
analytic target/table. The hybrid receives no hidden restriction on these
ordinary controls. No advantage is claimed from a support that ordinary methods
are artificially forbidden to access.

Observed integrity checks, exact new diagnostic and formula rendering costs are
recorded separately in RESOURCE_RECEIPTS.json. Inference, design, total discovery
and useful implementation costs remain unknown. No spending, paid compute,
hardware, external outreach or sharing changes were performed.
